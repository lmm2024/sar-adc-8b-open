# OA-SAR8异步控制器物理化状态

## 已完成

- `rtl/sar_ctrl_async_phys.sv`：没有任何`#`行为延时；启动和比较器完成事件驱动同一个本地事件寄存器组。
- `rtl/sar_async_delay_cells.sv`：使用IHP SG13G2真实标准延时单元和NOR门SR锁存器组成四相请求/应答延时链。
- 采样保护链初始实现为4个`sg13g2_dlygate4sd3_1`。
- 位间链使用1个`sg13g2_dlygate4sd2_1`的上升/返回完整握手，名义约0.9 ns。
- 558组全码字/随机输入加一个波形样例通过，`pass=559, fail=0`。
- 21 MS/s、64点已有IHP晶体管比较器事件回放：512次判决、512次trial检查、0错误、0输出码差异、ENOB 8.0107 bit。

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

然后复制或记录该次run的GDS、LEF、SPICE和SDF，再做以下验收：

1. 门级SDF回标，检查每次转换恰好8次判决且token始终one-hot；
2. TT、1.5 V、27 °C提取网表，实测`sample`下降到`hold_req`上升的时间；
3. 实测每次DAC更新到`cmp_fire`再次上升的时间；
4. 根据实测值增减延时单元抽头，而不是在RTL中加入`#`；
5. 对最终抽头做DRC、LVS、PEX和21 MS/s整体FFT。

## 当前边界

这是可进入综合/布局布线的第一版电路和已通过的前布局逻辑回归，不等同于已经完成GDS签核。`config_async.yaml`必须在仓库指定的IIC-OSIC-TOOLS 2026.07容器中首次运行并根据工具日志调整；最终延时只能由布局后提取结果确定。
