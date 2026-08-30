# OA-SAR8 数字异步控制器物理化状态

## 已完成

- `rtl/sar_ctrl_async_phys.sv`：没有任何`#`行为延时；启动和比较器完成事件驱动同一个本地事件寄存器组。
- `rtl/sar_async_delay_cells.sv`：使用IHP SG13G2真实标准延时单元和NOR门SR锁存器组成四相请求/应答延时链。
- 采样保护链实现为4个`sg13g2_dlygate4sd3_1`。
- 位间链使用1个`sg13g2_dlygate4sd2_1`的上升/返回完整握手，名义约0.9 ns。
- 558组全码字/随机输入加一个波形样例通过，`pass=559, fail=0`。
- 当前硬化结果完整保存在 `final_async_phys/`。
- PDN pitch 已由75.6 µm缩至30 µm，MSB附近新增局部VSS回流。
- 数字宏 DRC/LVS/antenna 全部通过。
- 与模拟核合并后的 Magic full-RC PEX 在10 MS/s完成33/33次转换，
  SNDR 49.6832 dB，ENOB 7.9607 bit。

## 工具容器启动后的第一条命令

```bash
cd /foss/designs/sar-adc/logic
librelane config_async.yaml
```

生成网表后必须确认专用单元没有被优化掉：

```bash
grep -R "sg13g2_dlygate4sd" runs/RUN_*/final/nl
grep -R "sg13g2_nor2_1" runs/RUN_*/final/nl
```

然后把通过的 `final/` 完整复制到 `final_async_phys/`，再做以下验收：

1. 门级SDF回标，检查每次转换恰好8次判决且token始终one-hot；
2. TT、1.5 V、27 °C提取网表，实测`sample`下降到`hold_req`上升的时间；
3. 实测每次DAC更新到`cmp_fire`再次上升的时间；
4. 根据实测值增减延时单元抽头，而不是在RTL中加入`#`；
5. 对最终抽头做DRC、LVS、PEX和10 MS/s整体FFT；更高采样率只有在
   32点ENOB仍达到目标时才可称为通过。

## 当前边界

当前 `final_async_phys/` 已完成宏级物理验证并进入整核GDS/PEX签核，不再是
仅前布局逻辑回归。异步链仍不适合用普通同步STA概括；最终功能、转换次数和
动态性能以整核提取网表闭环仿真为准。当前最高满足 ENOB ≥7.95 bit 的已验收
采样率是10 MS/s。
