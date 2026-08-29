# sar-adc-8b-open — 8-bit differential SAR ADC (core18 sign-off)

这是基于 IHP SG13G2 开源 PDK 的 8 位全差分 SAR ADC。当前主线是 **core18 模拟前端 + 数字异步 SAR 控制宏 + Magic full-RC PEX**，流程可在 IIC-OSIC-TOOLS Docker 容器内无 GUI 执行。

本仓库以 `Arcadia-1/open-analog-sar-8b` 为起点，但原仓库仅作参考。定制晶体管级异步实验和大规模诊断波形不属于当前发布主线；旧 README 已改名为 `README_BASELINE_REFERENCE.md`。

## 当前签核结果

条件：IHP SG13G2、mos_tt + cap_typ、1.5 V、27 °C、Magic full-RC PEX、ngspice trap、33 次转换、32 点 FFT、TRACK=25 ns。

| 采样率 | 完成情况 | SNDR | ENOB |
|---:|---:|---:|---:|
| 10 MS/s | 33/33 | 49.705 dB | **7.9643 bit** |
| 10.5 MS/s、TRACK=25 ns | 33/33 | 47.890 dB | 7.6629 bit |
| 10.5 MS/s、TRACK=30 ns | 33/33 | 48.417 dB | 7.7503 bit |
| 10.5 MS/s、TRACK=40 ns | 33/33 | 46.875 dB | 7.4942 bit |

10 MS/s 是当前正式签核结果；10.5 MS/s 记录为速度优化实验，尚未达到 7.95-bit 目标。

## 目录结构

```text
sar-adc/
  docs/                 规格
  model/                行为模型和 ENOB/INL 分析
  rtl/                  当前数字异步 SAR 控制器 RTL
  tb/                   RTL 自检 testbench
  comparator/           StrongARM block 仿真
  sw10m/                bootstrap 采样开关仿真
  layout/               KLayout 生成脚本、CDL、core18 GDS 和 PEX
  logic/                异步宏配置及其已硬化物理视图
  postlayout/           当前 core18 PEX 测试台和分析脚本
  power/                旧版/参考混合信号分析脚本
  report/               设计报告和图像
results/core18_pex/     签核和速度 A/B 的 compact metrics/sample codes
sar-chip/               旧 core16 全片集成参考流程
tools/run.sh            Docker exec 包装器
```

## 复现环境

请先阅读 `ENVIRONMENT.md` 和 `THIRD_PARTY.md`。使用：

```text
docker.io/hpretl/iic-osic-tools:2026.07
IHP SG13G2 PDK commit 84374023ee8b4b126bebbba67fcbada0a9c0ff0b
```

PDK 和 Docker 镜像是外部依赖，不随仓库分发。

## 当前 core18 PEX 复现

容器内工作目录为 `/foss/designs/sar-adc`：

```bash
python3 postlayout/run_core18_pex.py \
  --fs-msps 10 --track-ns 25 --samples 33 \
  --fft-points 32 --tone-bin 15 --amplitude 0.70 \
  --tstep-ns 0.05 --tag repro_10m
```

脚本会使用 `layout/pex_core18_final_w2_rc/oa_sar8_core18_final.pex.spice`，生成测试台、波形、样本码和 ENOB metrics。对照结果见 `results/core18_pex/` 和 `RESULTS.md`。

## 版图流程

当前 core18 版图入口：

```bash
cd /foss/designs/sar-adc/layout
klayout -zz -r gen_acore18_opt.py
klayout -zz -r gen_core18_final.py
sak-drc.sh -k -w drc_core18 oa_sar8_core18_final
sak-lvs.sh -k -w lvs_core18 -s core18_final_full.cdl \
  -l oa_sar8_core18_final.gds -c oa_sar8_core18_final
sak-pex.sh -k -w pex_core18 oa_sar8_core18_final
```

重新生成后必须重新检查 DRC、LVS、PEX，并重新运行 PEX ENOB。不要覆盖已签核 GDS，建议使用新的工作目录或 tag。

## 许可证和范围

代码和版图文件按 `LICENSE` 说明发布；IHP PDK、标准单元库和 IIC-OSIC-TOOLS 受其各自许可证约束。`sar-chip/` 是早期 core16 全片集成参考，不应误认为当前 core18 签核版。
