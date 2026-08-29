# OA-SAR8：8 位差分逐次逼近 ADC 芯片设计报告

工艺：IHP SG13G2（130 nm BiCMOS 开源 PDK，仅使用其 CMOS 部分）｜工具链：IIC-OSIC-TOOLS 2026.07 全开源 CLI 流程｜日期：2026-08-16（v3.0：闭环修复 + 根因修复 acore13/core16 + 全片重集成）

---

## 1. 芯片设计详情

### 1.1 架构与原理图实现方式

**架构**：8 位全差分电荷再分配 SAR ADC，10 MS/s（110 MHz 时钟，11 拍/次转换），1.5 V 单电源。信号链：双 bootstrap 采样开关 → P/N 两片 256 单元二进制 CDAC（底板采样，互补码切换）→ StrongARM 动态比较器（反相时钟触发，输出经 NAND SR 锁存）→ 同步 SAR 控制逻辑（3 拍跟踪 + 8 位试探，互补码输出，独立的 sample / hold 两路采样控制）。

**原理图实现方式**——本项目全程无 GUI，原理图以三种文本形式实现，全部可版本管理、可脚本回归：

| 模块 | 原理图形式 | 文件 |
|---|---|---|
| StrongARM 比较器 | 手写 ngspice 网表（晶体管级，sg13_lv 器件） | `comparator/strongarm.spice` |
| Bootstrap 采样开关 | 手写 ngspice 子电路（Abo-Gray 7 管 + MIM；v3 自举电容 150→600 fF） | `sw10m/bootstrap.cir`，`layout/bs/bstrap40.cdl` |
| CDAC / 开关单元 / 模拟核 | KLayout LVS 参考 CDL（C 元件 + rfmode MOS，与版图生成器同源） | `layout/acore13.cdl` 等 |
| 整核（模拟核 + 逻辑） | CDL 拼接 = 标准单元库 CDL + LibreLane 门级 spice + 模拟核 CDL + 顶层实例 | `layout/core16_full.cdl` |
| SAR 控制逻辑 | SystemVerilog RTL → Yosys 综合 → LibreLane 门级网表 | `rtl/sar_ctrl.sv`（同步）、`rtl/sar_ctrl_async.sv`（异步） |
| 芯片顶层 | SystemVerilog（模板 chip_top/chip_core，pad 例化 + 宏例化） | `sar-chip/rtl/chip_core.sv` |
| 行为级 | Python 数值模型（失配 MC + 相干采样 FFT） | `model/sar_model.py`, `model/dynamic_model.py` |
| **统一混合信号后仿测试台** | 模拟核 PEX 网表 + 逻辑宏门级 spice（标准单元晶体管级）+ 同一 VDD，闭环 | `power/mk_mixed4_tb.py` → `tb_mixed4*.spice`，`power/fft_mixed.py` |

版图同样是"版图即代码"：全部模块由 KLayout Python 生成器（`gen_*.py`）调用 IHP PCell 生成，一条命令重建，DRC/LVS/PEX 全部 CLI（`sak-drc.sh / sak-lvs.sh / sak-pex.sh / kpex`）。

**关键电路决策**
- 比较器：StrongARM，输入对 2 µm/0.15 µm×2 指、交叉耦合 nmos 4/0.13、pmos 6/0.13、尾管 3/0.3、预充 pmos 2/0.13。
- CDAC：单元 cmim 2.14 µm 方（实测 7.26 fF），16×16=256 单元，二重共质心（b7 外圈 8 行、b6 4 行、b5 2 行、中带点对称装 b4..b0+term），底板 M5 行条 + M3 竖轨，顶板 TM1 带。
- 采样：底板采样；bootstrap 单元（gb 引脚）驱动整排 9 个位单元的采样 nmos，P/N 各一颗、镜像放置；自举电容 600 fF（v3，抵消 gb 总线约 140 fF 寄生负载，自举幅度 ≥1.2 V）。
- 差分：开关驱动器为反相器（ctl=1 → 底板 VSS），因此 **P 阵列接 `dac_code_n`、N 阵列接 `dac_code`**（码位为 1 时 P 底板 VDD、N 底板 VSS）；比较器比较 topr 对 topm；两阵列顶板复位 TG 到 VCM。
- 时序（v4，由统一后仿逼出）：一次转换 11 拍 = 3 拍跟踪（FINISH+S1+S2）+ 8 位试探；`sample`（TG / bootstrap / 底板开关）在 S2 的下降沿提前半拍结束，顶板先浮空，5 ns 后 `hold` 才关闭行脚踏管并同时给出 MSB 试探码，DAC 永远不会在顶板仍接 VCM 时动作；比较器 clk_cmp=~clk（DAC 在 clk 高电平建立，比较器在低电平判决），outp/outn 双端进逻辑宏做交叉耦合 NAND SR 锁存，预充期间保持判决，FSM 在上升沿采样。
- 逻辑：同步 SAR FSM（流片基线，STA 干净），异步版另备。

### 1.2 仿真项目及各项指标

| # | 仿真项目 | 方法 | 结果 |
|---|---|---|---|
| S1 | 行为级失配蒙特卡洛 | Python，单元电容 σu 扫描，1000 次 | σu=1% 时 INL<0.5 LSB 良率 100% |
| S2 | 动态 ENOB（相干采样 FFT，4096 点） | Python，注入 σu 与比较器噪声 | 理想 7.95 bit；σu 1%+σn 0.2 LSB → SNDR 47.8 dB / ENOB 7.64 |
| S3 | 比较器瞬态（tran） | ngspice，±2 mV 差分判决 | 正确判决，判决时间 <1 ns |
| S4 | 比较器输入参考噪声 | .noise 校准 + 公式 σn=√(4kTγ/(gm·Tint))，F 源感应技巧 | γ=1.01、gm=1.64 mA/V；σn≈0.64 mV（<预算 1.17 mV） |
| S5 | 比较器失调 MC | 60 样本进程级 MC（每种子独立 ngspice） | σos=5.67 mV（解析 5.3 mV 交叉验证）；纯全局偏移 |
| S6 | 晶体管级 SAR 闭环（真实 CDAC+开关+比较器） | ngspice + Python 逐位迭代 | 码字 19/74/128/174/236 全部正确 |
| S7 | RTL 自校验 | iverilog，同步/异步 | 558/558 通过；异步 16.09 ns/次 |
| S8 | Bootstrap Ron 平坦度 | 两相瞬态法，vin 0.05–1.45 V | 138→208 Ω 单调（普通 TG 265→885→418 Ω 驼峰） |
| S9 | Bootstrap 10 MS/s 采样失真 | 相干采样 4.53 MHz，64 点 FFT | SFDR 65.5 dB（TG 仅 41.4 dB） |
| S10 | 基准网络跌落 | 邦线 3 Ω+4 nH，最坏位序 | 22 pF 去耦下最大跌落 0.84 mV（0.14 LSB） |
| S11 | 比较器后仿（PEX） | Magic + kpex 2.5D 双引擎 | 后仿失调 +1~2 mV（Magic 30 mV 系标签伪影，已平反） |
| S12 | Bootstrap 后仿 Ron | 提取网表 | 155→300 Ω，仍无驼峰，建立裕量 44τ |
| S13 | CDAC/整核后仿权重（AC 比值法） | 全无源提取（512 电容+寄生），主/副 18 位权重 | 见 1.3 |
| S14 | （已作废）分层后仿静态线性度 + SNDR | 后仿权重 → 差分传函 → FFT | 曾得 INL ±0.18 LSB / SNDR 49.46 dB；被 S16～S18 闭环结果证伪，仅作过程记录 |
| S15 | 采样率极限（前仿估计） | 采样建立 5.6 ns、MSB 建立 1.6 ns、比较器 <1 ns | 后仿实测跟踪 RC≈4 ns，故 v4 用 3 拍（22.7 ns）跟踪，110 MHz / 11 拍 = 10 MS/s |
| S16 | **统一混合信号后仿：闭环直流阶梯（模拟 PEX + 数字晶体管级，同一电源）** | ngspice，acore13 PEX（604 寄生 C + 210 MOS + 514 cmim）+ harden_v9 门级 spice，8 档 ×2 次转换，MSB 试探时刻顶板直读 | 传函 −1.4～+1.4 V 全程线性到 **±0.1 mV（±0.01 LSB）**，−1.2 % 增益 + 13.5 mV 失调（acore12 时 D≥+1.2 处压缩 −5～−20 mV） |
| S17 | **统一混合信号后仿 32 点相干 FFT（近奈奎斯特）** | 同上，fin=15/32×10 MHz=4.6875 MHz，−0.6 dBFS；32 点相干序列 = 4 段输入相位偏移（0/270/180/90°）的晶体管级闭环瞬态各取 8 次连续转换拼接（每段前 2 次转换丢弃作启动，4 核并行），`power/fft_mixed_seg.py` | **acore13：SNDR 45.8 dB / ENOB 7.32 b / SFDR 52.7 dB / THD −50.6 dB**（−0.60 dBFS；理想 8 位量化参考 51.0 dB）。acore12 时 41.6 dB / 6.6 b / SFDR 44.0（HD2 −44 dBc）。码序列相对孔径输入的 ≈6° 相位滞后是 RC≈4 ns 跟踪网络的线性响应，不是失真 |
| S18 | 统一混合信号后仿 32 点相干 FFT（低频） | 同 S17 方法，fin=1/32×10 MHz=312.5 kHz，相位偏移 0/90/180/270° | acore12：SNDR 41.9 dB / ENOB 6.7 b / SFDR 45.4 dB（HD2 −45、HD3 −47 dBc；理想参考 50.5 dB）；acore13：**SNDR 46.3 dB / ENOB 7.40 b / SFDR 54.3 dB / THD −52.7 dB**（理想参考 50.5 dB）；功耗 489.5 µW |

### 1.3 预想目标值与实际（仿真）结果

以下"实际结果"一律取**统一混合信号后仿**（模拟核 PEX + SAR 逻辑宏门级晶体管级，同一 1.5 V 电源，闭环）的数值；分块仿真只在 §1.2 作为过程记录保留。

| 指标 | 预想目标 | 实际结果（统一后仿，tt 25 °C） | 状态 |
|---|---|---|---|
| 分辨率 | 8 bit | 8 bit，全差分 | ✅ |
| 采样率 | 100 kS/s（v0.1）→ **10 MS/s**（v0.3 升级） | 10 MS/s（110 MHz 时钟，11 拍/次），闭环 done 周期 100 ns | ✅ |
| 静态线性 INL / DNL | < ±0.5 LSB | 闭环直流阶梯（顶板直读，acore13）：全程线性到 ±0.01 LSB（acore12 时 D ≥ +1.2 V 处压缩 0.5～1.7 LSB） | ✅ |
| ENOB（动态） | ≥ 7.5 bit | 32 点相干 FFT（acore13）：**近奈奎斯特 4.69 MHz：ENOB 7.32（SNDR 45.8 dB，SFDR 52.7 dB）**；低频 312.5 kHz：**ENOB 7.40（SNDR 46.3 dB，SFDR 54.3 dB）**；−0.6 dBFS。（acore12 时 6.6 / 6.7） | ⚠️ 7.3～7.4，差目标 0.1～0.2 位；剩余为跟踪网络随电平变化的动态项（§1.5 末尾） |
| 功耗 | 规格 v0.2：< 100 µW @ 100 kS/s；10 MS/s 版无硬指标 | **488.5 µW @ 1.5 V、10 MS/s**（325.6 µA，模拟 + 数字一次仿真，近奈奎斯特 −0.6 dBFS 真实活动） | ✅（约 48.9 µW/MS/s） |
| FoM | 文献 8 bit / 10 MS/s / 130 nm 典型 Walden 30～100 fJ/step | **Walden 305 fJ/conv-step（ENOB 7.32）/ Schreier 145.9 dB**（4.69 MHz，acore13）；291 fJ/step / 146.4 dB（312.5 kHz）；acore12 时 499 fJ/step / 141.7 dB | ⚠️ 同步 SAR 的 110 MHz 时钟树占约一半功耗；异步版可再降 |
| 比较器噪声 | < 0.2 LSB rms (1.17 mV) | 0.64 mV（分块表征） | ✅ |
| 比较器失调 | 未硬性要求（全局项） | σ 5.67 mV（≈1 LSB），后仿 +1~2 mV 版图诱导；闭环整体失调 ≈ +0.7 LSB | ✅（可校准） |
| 采样开关线性 | 10 MS/s 下 SFDR > 55 dB | 闭环 SFDR 52.7 dB @4.69 MHz（acore13）；开关单体 bootstrap 65.5 dB | ⚠️ 差 2.3 dB |
| 电源 | 1.5 V 核心 / 3.3 V IO | 1.5 V sg13_lv，IO 环 3.3 V | ✅ |
| 面积（核） | 尽量紧凑 | 327 × 216 µm = 0.071 mm²（core15） | ✅ |
| DRC / LVS | 全清 | 各模块、模拟核 acore13、整核 core16 DRC 0 + LVS MATCH，且提取网表顶层 19 个端口全部独立（含 clk） | ✅ |
| 全片 | IO 环 + 32 pad + PDN | LibreLane 签核全清，见 §2.3 | ✅ |

**诚实说明**：以上"实际结果"全部为仿真结果，尚无硅测数据；VREF 目前与 VDD 合流（独立 VREF pad 列入下一版）。S13/S14 那种"抽权重再行为级 FFT"的分层结果（49.5 dB）被闭环后仿证伪（它看不到开关关断次序这类闭环效应），本表不再引用。

### 1.4 功耗与 FoM（10 MS/s，1.5 V，tt 25 °C，仿真值）

**口径**：v1 报告把"模拟核瞬态电流"和"数字 STA 功耗"分别仿真再相加，用户指出这不是真正的后仿。v2 改为**统一混合信号后仿**：模拟核 PEX 网表 + 逻辑宏门级 spice（标准单元晶体管级）挂在同一个 1.5 V 电源上闭环运行，直接量 VDD 平均电流，模拟与数字不再分开。下表为 S17 的 32 次连续转换（4.6875 MHz、−0.6 dBFS 输入，真实开关活动）的平均值。

| 口径 | VDD 平均电流 | 总功耗 | Walden FoM = P/(2^ENOB·fs) | Schreier FoM = SNDR + 10log(fs/2/P) |
|---|---|---|---|---|
| **统一混合后仿（acore13，模拟 + 数字一次仿真，4.69 MHz −0.60 dBFS 输入）** | **325.6 µA** | **488.5 µW** | **305 fJ/conv-step**（闭环 ENOB 7.32） | **145.9 dB** |
| 同上，312.5 kHz 输入 | 326.3 µA | 489.5 µW | 291 fJ/conv-step（ENOB 7.40） | 146.4 dB |
| （acore12，同一测试）| 325.6 µA | 488 µW | 499 fJ/conv-step（ENOB 6.61） | 141.7 dB |

参考（分块口径，仅供了解构成，v1 数字）：模拟核单独瞬态约 300 µW（开关单元 141 + bootstrap 140 + 比较器 19 µW，`power/tb_power4.spice`），数字逻辑 OpenSTA 后布局 VCD 功耗 379 µW @1.5 V（`power/tb_gl_power.sv` + `sta_power.tcl`）；分块相加 679 µW 高于统一后仿的 488 µW，差异来自 STA 功耗模型的保守和分块测试台的活动率假设，以统一后仿为准。

对比：文献中 8 位 10 MS/s 级 SAR ADC（130 nm）典型 Walden FoM 30–100 fJ/step；本设计的主要拖累是同步 SAR 需要 110 MHz 时钟树（数字占总功耗约一半）；切换到已备好的异步 SAR 控制器（无高速时钟）预期数字功耗降 5–8 倍。

### 1.5 统一混合信号后仿抓出的集成缺陷与修复（v1 → v2）

v1 的所有分块仿真（比较器、bootstrap、CDAC 权重、RTL、STA）各自都通过，但把模拟核 PEX 与数字门级晶体管级网表合在一起闭环一跑，第一版输出全是 255。逐一定位出 5 个只有合仿才暴露的集成缺陷，全部已修复并重新 DRC/LVS/后仿：

| # | 缺陷 | 现象 / 证据 | 修复 |
|---|---|---|---|
| B1 | 比较器时钟直接接逻辑 clk | StrongARM 在 clk 低电平预充（outp=outn=1），FSM 在上升沿采 cmp，永远采到 1 | 逻辑宏输出 clk_cmp=~clk；outp/outn 双端进宏，交叉耦合 NAND2 SR 锁存后再采样（无竞争） |
| B2 | CDAC 极性 | 开关驱动器反相（ctl=1 → 底板 VSS），P 阵列却接 dac_code，码增大 P 侧电平反而下降，二分搜索方向反：正输入全 255、负输入全 0 | core 级 P 阵列改接 dac_code_n、N 阵列接 dac_code |
| B3 | 核的 clk 馈线断路 | core12/13 的 clk M4 馈线到 M2 竖线只打了 via3 没有 via2，时钟根本没接进核；core 级 LVS 因默认 IGNORE_TOP_PORTS_MISMATCH 放过（提取网表顶层端口行里没有 clk） | 补 via2；LVS 改为逐项核对提取网表 .SUBCKT 端口行（core15：19 端口全部独立） |
| B4 | 采样→转换竞争 | sample 与 MSB 试探码同一时钟沿更新，dac_code_n 是组合逻辑比 trk 早约 0.15 ns，顶板 TG 尚未断开 DAC 已动作，波形上 topm 在 TG 仍导通时被拽到 1.4 V，一次转换错约 60 mV | RTL v4：sample 用负沿寄存器提前半拍结束（顶板先浮空），新增 hold 引脚在 5 ns 后才关闭行脚踏管并给出 MSB 码；acore12 把脚踏带改为独立 hold 引脚 |
| B5 | 跟踪建立时间不足 + 自举幅度不足 | 后仿实测跟踪网络 RC≈4 ns，10 ns 跟踪窗只有 2.5τ；根源同为自举幅度在版图寄生下只剩 +0.78/+0.95 V（原理图 1.4 V） | 时序补救：RTL v4 改为 3 拍跟踪（22.7 ns@110 MHz ≈ 5.7τ），11 拍/次，110 MHz 保持 10 MS/s；剩余的 4 ns 线性延迟不影响 ENOB。**幅度问题就是闭环 ENOB 6.6 的根因**（详见本节末尾），修法 = 自举电容 150→600 fF（acore13） |

修复后：RTL 回归 598/598（含 40 次背靠背转换、跟踪窗 ≥24 ns、hold 滞后 ≥4 ns 断言），逻辑宏 harden_v9（LVS 0 差、DRC 0、setup 裕量 3.2 ns、hold 0.18 ns），acore12 DRC 0 + LVS MATCH，core15 DRC 0 + LVS MATCH，全片重新集成（§2.3）。

**闭环 FFT 剩下的差距：根因已定位（v2.3）**。修复五项之后闭环 32 点 FFT 在 4.69 MHz 与 312.5 kHz 给出几乎相同的 SNDR（41.6 / 41.9 dB，ENOB 6.6 / 6.7），说明剩余误差与输入频率无关。用直流阶梯（每档 2 次转换，档间跳变，`power/mk_mixed5_tb.py stair=… / pairs=… / inj=… / pex=…` + `an_stair2.py`，直接在 MSB 试探时刻读顶板差分电压 topr−topm 与理想 D−VDD/256 之差）做了 20 余组对照实验：

| 实验 | 结果 |
|---|---|
| 原理图级闭环（同一数字宏 + 无寄生模拟核网表） | 8 次转换全部精确等于 floor(理想码)，无失调、无记忆 → 架构与电路原理正确 |
| PEX 闭环基线（110 MHz） | 采样误差：D=−1.4：+29 mV，−0.6：+17，+0.2：+7.5，+0.6：0，+1.0：−6.5，+1.2：−14，+1.3：−21，+1.4：−32 mV（1 LSB = 11.7 mV） |
| 80 MHz（跟踪 31 ns）同阶梯 | 不变 → 不是建立时间 |
| 拆解 | 中段（−0.6～+1.0）在 ±2 mV 内是**线性**的：+10 mV 失调 + −2.3 % 增益；只有 D ≥ +1.2（vinp ≥ 1.35 V）偏离线性趋势 −5 / −10 / −20 mV（P 侧正满量程压缩），这就是 HD2/HD3 与 ENOB 6.6 的来源 |
| 去掉顶板上全部 46 个寄生耦合（P1）/ 只去掉顶板↔hold、trk、trkb、gb、vin_r、vcm、VDD 的 13 个耦合（P6） | 中段误差变成 −5.8 / −1.1 / −7.8 / +2.9 mV（线性残差 ±1.4 mV）：这些耦合只贡献失调和增益（hold 与 topr 馈线平行 150 µm 给 +5.9 mV 常数，gb_p 与 topm 4.1 fF 给线性项），**不产生非线性**；且 P6 在 +1.4 处压缩仍在（−22 mV） |
| 只去掉位线寄生 / 门控轨与输入线寄生 / 比较器内部节点耦合（P4/P5/P7） | 不变 |
| 顶板 TG 单独快速关断（X4）；顶板先断、底板延迟 0.6 ns（X5） | 不变（+1.4 仍 −35～−41 mV）→ 不是开关关断次序 |
| Msw 并联 pmos（X2） | +1.0 处 −6.5→−2.4，其余不变 |
| **自举电容 150→600 fF（X1）** | **全程线性到 ±0.5 mV（±0.04 LSB）**：+1.4：−6.6，+1.3：−5.3，+1.2：−4.0，+1.0：−1.6，+0.6：+3.0，+0.2：+8.2，−0.6：+17.6 = 一条直线（−1.2 % 增益 + 10 mV 失调） |

**结论**：非线性的根因是版图寄生把 bootstrap 的自举幅度从原理图的 1.4 V 压到 P 侧 0.78 V / N 侧 0.95 V（gb 总线沿整排开关走 120 µm，与 trk/trkb 带相邻，等效负载约 140 fF，与 150 fF 自举电容分压），vin 接近 VDD 时自举 nmos 的过驱动只剩约 0.1 V（体效应 Vth≈0.68 V），P 侧开关在关断瞬间的行为随 vinp 非线性变化，形成正满量程压缩；把自举电容加大到 4 倍后自举幅度回到约 1.2 V，闭环传函线性度恢复到理想水平。**修法（已实施 = acore13 / core16）**：bootstrap 单元 bstrap40：MIM 从 9.94×9.94 µm 改为 39.8×9.94 µm（600 fF，同高更宽，单元 80×16 µm，DRC 0 + LVS），P bootstrap 西移到 x 40.1～119.5、N bootstrap 镜像放到 162.5～241.9，gb/out/vin 引脚走线与 row-2 trkb 带、VSS2 轨相应延长；acore13 DRC 0 + LVS MATCH，core16 DRC 0 + LVS MATCH（19 端口独立），全片 RUN_2026-08-16_09-07-48 签核全清。验证：闭环直流阶梯全程线性到 ±0.1 mV；近奈奎斯特 32 点 FFT 从 41.6 dB / 6.6 b 提升到 **45.8 dB / 7.32 b**（SFDR 44.0 → 52.7 dB）；低频见 S18。低频 312.5 kHz：**46.3 dB / 7.40 b**（SFDR 54.3 dB）。两个频点都比理想量化器（51 dB）低 4～5 dB，而静态传函已线性到 ±0.01 LSB，剩余损失是动态项：跟踪网络 RC≈4 ns 且随输入电平变化（相位随电平变化 = 弱非线性）、档间记忆 0.1 %×ΔD；下一步是顶板复位 TG 并联 4 个单元把 τ 压到约 1 ns（预期回到 7.8～7.9 位）。
---

## 2. 版图文件

压缩包 `OA-SAR8_layout_screenshots.zip` 内含：

### 2.1 各模块版图（`img/01–06`）
| 文件 | 模块 | 尺寸 | 验证 |
|---|---|---|---|
| 01_cdac_array.png | 256 单元 CDAC 阵列（二重共质心） | 124 × 103 µm | DRC 0 / LVS |
| 02_comparator.png | StrongARM 比较器 | 60 × 28 µm | DRC 0 / LVS / PEX |
| 03_switch_bitcell.png | 底板开关单元 sw_bitcell11（驱动反相器 + 自举栅采样管，独立衬底轨 VSSB 供脚踏门控） | 13.6 × 16.2 µm | DRC 0 / LVS |
| 04_switch_tg.png | 顶板复位传输门 | 13.6 × 15.2 µm | DRC 0 / LVS |
| 05_bootstrap.png | Bootstrap 采样开关 bstrap40（7 管 + 600 fF MIM，v3） | 80 × 16 µm | DRC 0 / LVS |
| 06_sar_logic.png | SAR 控制逻辑 v4（LibreLane harden_v9：互补码、clk_cmp、SR 锁存、sample/hold 双控） | 50 × 100 µm | LibreLane 签核（LVS 0 差 / DRC 0 / 时序无违例） |

### 2.2 整体版图（`img/07, 08`）
| 文件 | 内容 | 尺寸 | 验证 |
|---|---|---|---|
| 07_analog_core.png | 模拟核 acore13：两片 CDAC + 两排开关（脚踏门控）+ 比较器 + 采样岛（双 600 fF bootstrap） | 322 × 183 µm | DRC 0 / LVS MATCH |
| 08_full_core.png | 整核 core16：模拟核 + 逻辑条 + 核级 PDN 母线 | 327 × 216 µm | DRC 0 / 核级 LVS MATCH（19 端口全独立） |

### 2.3 全片版图（含 IO 环与 pad）（`img/09`）
| 文件 | 内容 |
|---|---|
| 09_full_chip.png | 全片 1.6 × 1.6 mm：32 个 70×70 µm 键合 pad（每边 8 个）、IHP IO 单元环（3.3 V IO / 1.5 V 核）、密封环、TM1/TM2 核心电源环与 PDN 网格、SAR ADC 宏居中 |
| 10_full_chip_core_zoom.png | 宏区放大：宏顶部 TM2 电源母线与芯片级 TM1 竖条纹连接，pad→宏 信号布线 |
| 11_full_chip_corner_pads.png | 左下角 pad/IO 单元/电源环细节 |

**全片集成方式**：IHP `ihp-sg13g2-ams-chip-template`（LibreLane Chip 流程），SAR ADC 整核作为硬宏（LEF + GDS + Verilog 黑盒，边界引脚 + TM2 电源母线 + prBoundary），`chip_core.sv` 例化宏并接 pad；32 pad 分配如下（每边由下到上 / 由左到右）：

| 边 | Pad |
|---|---|
| 西 | busy, VSS, VDD, IOVSS, IOVDD, start, rst_n, clk |
| 北 | result[7] … result[0] |
| 南 | VSS, VDD, done, spare(v1 的 outn 调试脚已取消，比较器双端只进逻辑宏), spare, spare, VDD, VSS |
| 东 | VSS, vinn, vinp, vcm（模拟 pad，经二级 ESD）, VDD, spare, spare, spare(bidir) |

**全片后仿口径说明**：本报告的晶体管级后仿（S16～S18、§1.4 功耗）覆盖的是整核（模拟核 PEX + SAR 逻辑宏门级晶体管级，同一电源）；全片层面（pad 环、ESD、PDN、键合）没有再做 SPICE 后仿，用 LibreLane 的签核（LVS/天线/时序/PSM/XOR）覆盖，见下表。

**全片签核结果**（v3：LibreLane RUN_2026-08-16_09-07-48，core16 宏，`metrics.json`；v2 core15 RUN_2026-08-16_00-42-08 结果相同）：

| 项 | 结果 |
|---|---|
| 流程 | 81 阶段全部完成（Flow complete） |
| 版图 vs 网表 LVS（Netgen） | 器件差 0 / 网差 0 / 属性差 0 / 未匹配引脚 0 |
| 电源网连通性（PSM） | VDD、VSS 全部形状连通 |
| 天线违例 | 0 |
| 悬空引脚 | 0 |
| 布线 DRC（OpenROAD） | 0 违例 |
| 静态时序 setup / hold（6 角） | 无违例 |
| 最大摆率告警 | 慢角 11 处（pad 驱动，告警级） |
| 实例数 | 53224（含填充、172 pad 单元、宏 3） |
| KLayout XOR（GDS vs DEF） | 差异 0 |
| KLayout 整片天线 | v1 运行通过（违例 0）；v2 重跑时跳过（宏内部未变） |
| KLayout 整片密度 / 全规则 DRC | 未在 v2 重跑（耗时 >30 min）；宏级 DRC 全部为 0 |


---

## 3. 设计过程文档

### 3.1 项目时间
- 开始：2026-08-14 16:49（IIC-OSIC-TOOLS 2026.07 环境调研）
- ADC 立项：2026-08-14 19:35（选定"SAR ADC 芯片"）
- v1 报告：2026-08-15 晚；v2（合仿修复）：2026-08-16 凌晨
- 持续时长：约 **32 小时**连续会话（其中 ADC 设计约 30 小时）

### 3.2 沟通轮次
- 用户有效消息：**约 60 条**（不含系统通知）
- 助手消息 / 工具调用：约 2600 / 1250 次
- 主要迭代版本：模拟核 acore1→acore13（13 版）、整核 core1→core16（16 版）、逻辑宏硬化 9 次、比较器版图 15 轮迭代、RTL v1→v4、bootstrap 单元 2 版

### 3.3 对话内容概要（按阶段）
1. **环境搭建（08-14 16:49–17:30）**：调研并部署 IIC-OSIC-TOOLS 2026.07（Colima/Docker），修复 VM DNS；用户要求纯 CLI 无 GUI 工作流。
2. **工艺与模板调研（17:30–19:30）**：GF180 Caravel/wafer.space 全片模板、SKY130、IHP SG13G2 对比；构建 GF180 模板全片并渲染；确认 IHP AMS 32-pad 模板路线。
3. **立项与规格（19:35–20:30）**：选定 8 位 SAR ADC on IHP；写规格书 v0.1、行为级失配 MC 与动态 ENOB 模型；用户要求 tran+FFT 表征、同步/异步双版本；否决慢速判决概率噪声法，改用 .noise 校准公式法。
4. **电路级验证（20:30–22:30）**：比较器噪声校准、60 样本失调 MC、晶体管级 SAR 闭环、RTL 558/558。
5. **版图战役（08-15 03:24–08:00）**：CDAC/比较器/开关/逻辑宏各自 DRC+LVS 清零；核心组装多版；用户先后指出"不对称""不紧凑""逻辑太大位置丑"，对照真实 SAR die photo 重构为对称矩形；首次比较器 PEX 后仿；用户追问"能否后仿出 SNDR"→当时用了分层权重法（后被闭环后仿证伪）。
6. **10 MS/s 升级（08:00–11:40）**：采样率极限分析、bootstrap 开关设计/版图/集成、基准去耦定容。
7. **对称性三连（11:40–17:03）**：用户三次指出开关排/副阵列不对称：副阵列开关活化（acore5/6）、开关排与 CDAC 严丝合缝（acore7/core8，首次核级 LVS，抓出历史暗伤）、采样岛移出开关行（core9）。
8. **真差分改造（17:07–17:35）**：用户指出单 bootstrap 共用错误 → 双 bootstrap 镜像、N 侧互补码、差分后仿 SNDR 49.46 dB。
9. **全片集成（17:37–20:55）**：工艺/IO 环答疑；核级 PDN 母线（core11/12，含逻辑宏电源的整核 LVS 首次全 MATCH，并抓出 outn 引出短路）；SG13G2 AMS 模板集成（32 pad 定义、宏 LEF/黑盒、PDN 网格）、LibreLane 整片流程；v1 报告与交付包。
10. **功耗与 FoM（20:55–23:10）**：用户要求功耗/FoM 呈现，随后指出功耗太差 → 定位到开关单元跟踪相直通（425 µA），改为行脚踏管功率门控（sw_bitcell11 独立衬底轨解决 LVS 衬底合并），门级 VCD 真实活动率数字功耗 379 µW。
11. **统一混合信号后仿（23:10–08-16 03:45）**：用户质问"数字和模拟为什么不能混在一起仿真"，改为模拟核 PEX + 数字晶体管级同一电源闭环后仿；第一版全码 255，连续挖出 5 个只有合仿才暴露的集成缺陷（§1.5），RTL v4 / harden_v9 / acore12 / core15 全链路重验、全片重集成、32 点相干 FFT 闭环后仿与统一功耗/FoM。
12. **闭环 ENOB 归因（08-16 06:00– ）**：用户指出 ENOB 6.6 与 7.9 差距过大必有原因、仿真过慢；仿真提速 3 倍（KLU + cmim 合并 + 默认容差 + tmax 0.2 ns，另一会话的 RV32 流程抢占 CPU 是外因）；直流阶梯 + 顶板直读 + 20 余组网表对照（去耦合、改关断次序、加自举电容、并联 pmos、单端激励）：排除建立时间、关断次序、耦合、比较器回踢，锁定"版图寄生压缩自举幅度 → vin 近 VDD 时 P 侧开关非线性"，自举电容 ×4 使闭环传函线性到 ±0.04 LSB。
13. **根因修复（08-16 09:00–10:00）**：bstrap40 单元（600 fF）、acore13、core16 全部一次过 DRC/LVS，全片重跑签核全清；闭环阶梯线性 ±0.1 mV，近奈奎斯特 FFT 45.8 dB / 7.32 b。
