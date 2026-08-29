# open-analog-sar-8b — OA-SAR8, an 8-bit differential SAR ADC on IHP SG13G2, built entirely with open-source CLI tools

> 中文速览：这是一个 8 位全差分 SAR ADC（10 MS/s、1.5 V）从规格、行为模型、RTL、晶体管级电路、
> 版图即代码（KLayout PCell 生成器）、DRC/LVS/PEX、逻辑宏硬化（LibreLane）、统一混合信号后仿到
> 32 pad 全片集成的完整仓库，全程在 IIC-OSIC-TOOLS 2026.07 容器里用命令行完成，无 GUI。
> 复现步骤见下文 “Reproduce”；环境见 `ENVIRONMENT.md`；设计报告（含五个只有合仿才抓到的
> 集成 bug 与 ENOB 根因分析）见 `sar-adc/report/OA-SAR8_设计报告.md`。

* Process: **IHP SG13G2** (130 nm BiCMOS open PDK, CMOS devices only) · Tools: IIC-OSIC-TOOLS 2026.07 (KLayout, ngspice, LibreLane/OpenROAD/Yosys, Icarus, Magic/netgen, kpex)
* Architecture: fully differential charge-redistribution SAR, dual bootstrapped sampling switches (600 fF boost caps), 2 × 256-unit MIM CDAC (double common-centroid), StrongARM comparator on the opposite clock phase with a NAND SR latch, synchronous SAR FSM (11 clocks per conversion, 3 track clocks, separate `sample`/`hold` timing), power-gated bottom-plate drivers
* Silicon views: analog core `oa_sar8_acore13` (322 × 183 µm), core with SAR logic `oa_sar8_core16` (327 × 216 µm, DRC 0, LVS match with all 19 top ports), full chip 1.6 × 1.6 mm / 32 pads in the JKU AMS chip template (LibreLane signoff: LVS 0 diff, antenna 0, timing clean, XOR 0)

## Results (unified mixed-signal post-layout simulation, tt 25 °C, 1.5 V, 10 MS/s @ 110 MHz clock)

The analog core **PEX netlist** (604 parasitic C, 210 MOS, 514 MIM units) and the **gate-level SAR logic
on transistor-level standard cells** run in one ngspice transient on one VDD, closed loop.
32-point coherent FFT = 4 phase-offset segments × 8 conversions (start-up conversions discarded).

| Input | SNDR | ENOB | SFDR | THD | I(VDD) | Power | Walden FoM | Schreier FoM |
|---|---|---|---|---|---|---|---|---|
| 4.6875 MHz, −0.60 dBFS (near Nyquist) | 45.8 dB | 7.32 b | 52.7 dB | −50.6 dB | 325.6 µA | 488.5 µW | 305 fJ/conv-step | 145.9 dB |
| 312.5 kHz, −0.58 dBFS | 46.3 dB | 7.40 b | 54.3 dB | −52.7 dB | 326.3 µA | 489.5 µW | 291 fJ/conv-step | 146.4 dB |

DC staircase (top-plate differential read at the MSB trial): transfer function linear to **±0.1 mV
(±0.01 LSB)** over −1.4…+1.4 V; −1.2 % gain, +13.5 mV offset. Ideal 8-bit quantiser on the same
samples: 50.5–51.0 dB. The remaining 4–5 dB are dynamic (track network τ ≈ 4 ns whose delay depends
on the input level, 0.1 %·ΔD memory); the planned fix is a 4× wider top-plate reset switch.
Schematic-level closed loop (same digital, no parasitics) is exact to floor(ideal code).

Everything is simulation; there is no silicon yet.

## Repository map

```
sar-adc/
  docs/spec.md                 specification (v0.1 → v0.3, 10 MS/s)
  model/                       behavioural model: capacitor-mismatch Monte-Carlo, coherent-FFT ENOB
  rtl/sar_ctrl.sv              SAR controller v4 (+ sar_ctrl_async.sv, an asynchronous alternative)
  tb/                          self-checking RTL testbench (598 checks incl. 40 back-to-back conversions)
  comparator/                  StrongARM: transient, .noise calibration, offset MC, transistor-in-the-loop SAR
  sw10m/                       bootstrapped switch: Ron flatness, 10 MS/s THD, reference-network droop
  core/                        early "real core" (cmim CDAC + switches + comparator, python-in-the-loop)
  layout/                      layout-as-code (KLayout Python, IHP PCells) — see below
  logic/                       LibreLane config for the SAR logic macro + hardened views (final/)
  power/                       mixed-signal post-layout deck generator, FFT / staircase analysis, power decks
  report/                      design report (zh), 11 layout screenshots, deliverable packaging script
sar-chip/                      full chip: diff vs the JKU AMS template + macro + final GDS/reports (see sar-chip/README.md)
ENVIRONMENT.md                 container, tool versions, PDK commit, pitfalls
tools/run.sh                   docker-exec wrapper
```

Layout generators (final versions; the numbered older versions document the evolution):

| Block | Generator | Reference netlist | Output |
|---|---|---|---|
| CDAC 16×16 cmim, double common-centroid | `layout/gen_cdac.py` | `layout/cdac_array.cdl` (inside acore CDL) | `layout/cdac_array.gds` |
| StrongARM comparator | `layout/cmp/gen_comparator.py` | `layout/cmp/sa_comp.cdl` | `layout/cmp/sa_comp.gds` |
| bottom-plate switch cell (inverting driver + bootstrapped nmos, separate substrate rail) | `layout/sw/gen_switch11.py` | `layout/sw/sw_bitcell11.cdl` | `layout/sw/sw_bitcell11.gds` |
| top-plate reset TG | `layout/sw/gen_sw_tg.py` | `layout/sw/sw_tg.cdl` | `layout/sw/sw_tg.gds` |
| bootstrapped switch (Abo-Gray, 600 fF) | `CAPW=39.8 CELLNAME=bstrap40 layout/bs/gen_bootstrap.py` | `layout/bs/bstrap40.cdl` | `layout/bs/bstrap40.gds` |
| analog core (arrays, switch rows, island, comparator, footers) | `layout/gen_acore13.py` | `layout/acore13.cdl` | `layout/oa_sar8_acore13.gds`, PEX `layout/pex_a13/` |
| core = analog core + SAR logic macro + core PDN | `layout/gen_core16.py` | `layout/core16_full.cdl` (`mk_core16_cdl.py`) | `layout/oa_sar8_core16.gds`, LEF/blackbox via `mk_lef16.py` |

## Reproduce

All commands run inside the container (`ENVIRONMENT.md`); `tools/run.sh <dir> "<cmd>"` does the
`docker exec … bash -lc` for you. Set `QT_QPA_PLATFORM=offscreen` for KLayout batch scripts.

1. **Environment** – start IIC-OSIC-TOOLS 2026.07 with this repository mounted at `/foss/designs`.
2. **RTL regression** –
   `tools/run.sh sar-adc "iverilog -g2012 -o /tmp/t.vvp tb/tb_sar_ctrl.sv tb/sg13g2_sim_models.sv rtl/sar_ctrl.sv && vvp /tmp/t.vvp | tail -3"`
   → `RESULT: pass=598 fail=0`. Behavioural models: `python3 model/sar_model.py`, `python3 model/dynamic_model.py`.
3. **Circuit blocks** – `ngspice -b comparator/strongarm.spice`, `ngspice -b comparator/sar_loop.spice`,
   `ngspice -b sw10m/tb_ron.spice`, `ngspice -b sw10m/tb_thd.spice` (see the headers of each deck).
4. **Layout generation, DRC, LVS, PEX** (in `sar-adc/layout`, each generator writes its GDS + CDL):
   ```
   klayout -zz -r gen_cdac.py ; (cd cmp && klayout -zz -r gen_comparator.py)
   (cd sw && klayout -zz -r gen_switch11.py && klayout -zz -r gen_sw_tg.py)
   (cd bs && CAPW=39.8 CELLNAME=bstrap40 klayout -zz -r gen_bootstrap.py)
   klayout -zz -r gen_acore13.py
   sak-drc.sh -k -w drc_a13 oa_sar8_acore13
   sak-lvs.sh -k -w lvs_a13 -s acore13.cdl -l oa_sar8_acore13.gds -c oa_sar8_acore13
   sak-pex.sh -k -w pex_a13 oa_sar8_acore13          # -> pex_a13/oa_sar8_acore13.pex.spice
   ```
5. **SAR logic macro** (in `sar-adc/logic`): `librelane config.yaml`, copy `runs/RUN_*/final` to `logic/final`,
   `klayout -zz -r pins.py` prints the pin coordinates used by `gen_core16.py`.
6. **Core assembly** (in `sar-adc/layout`): `klayout -zz -r gen_core16.py`, `sak-drc.sh -k -w drc_c16 oa_sar8_core16`,
   `sak-lvs.sh -k -w lvs_c16 -s core16_full.cdl -l oa_sar8_core16.gds -c oa_sar8_core16`
   (check that the `.SUBCKT` line of `lvs_c16/…/oa_sar8_core16_extracted.cir` lists all 19 ports),
   `klayout -zz -r mk_lef16.py` → `oa_sar8_core16.lef`, `oa_sar8_core16.v`, `oa_sar8_core16_lef.gds`.
7. **Unified mixed-signal post-layout simulation** (in `sar-adc/power`, needs step 4 and 5 outputs):
   ```
   python3 mk_mixed6_tb.py 870n 0 _stHi klu merge stair=0.6,1.4,1.3,1.2   # DC staircase deck
   OMP_NUM_THREADS=1 ngspice -b tb_mixed6_stHi.spice ; python3 an_stair2.py mixed6_stHi_out.csv
   for k in 0 1 2 3; do python3 mk_mixed6_tb.py 1080n $(( (270*k)%360 )) _fN$k klu merge; done   # 4 FFT segments (fin = 15/32 fs)
   for k in 0 1 2 3; do OMP_NUM_THREADS=1 ngspice -b tb_mixed6_fN$k.spice & done; wait
   python3 fft_mixed_seg.py /foss/designs/sar-adc/power/mixed6_fN{}_out.csv 15   # SNDR/ENOB/SFDR + power + FoM
   ```
   Options of the deck generator: `stair=…` / `pairs=vp:vn,…` (DC levels), `inj=<file>` (extra elements inside the
   core, used for the boost-capacitor experiments), `pex=<netlist>` (parasitic bisection), `sch` (schematic-level core).
8. **Full chip** – see `sar-chip/README.md` (LibreLane Chip flow of the JKU template with the `oa_sar8_core16` macro).
9. **Report** – `sar-adc/report/OA-SAR8_设计报告.md` (Chinese; `md2html.py`, `mk_deliver.sh` rebuild the HTML and the zip).

## What the unified post-layout simulation found (short version)

Every block simulated fine on its own; the first closed-loop transistor-level run of PEX analog core +
gate-level logic returned code 255 for every sample. Five integration defects, all invisible to
block-level simulation, were found and fixed (details in the report, §1.5):

1. comparator clocked with the logic clock (StrongARM sampled during precharge) → `clk_cmp = ~clk` + NAND SR latch in the macro
2. CDAC polarity: the switch driver inverts, so the P array must take `dac_code_n` and the N array `dac_code`
3. the core's `clk` feed had a via3 but no via2 (the clock never reached the logic; core-level LVS was run with top-port mismatches ignored)
4. sampling and first DAC step on the same clock edge (DAC moved 0.15 ns before the top-plate switch opened) → early `sample`, separate `hold`
5. layout parasitics loading the bootstrap gate bus reduced the boost from 1.4 V to 0.78/0.95 V → P-side compression near full scale (HD2/HD3, ENOB 6.6) → boost capacitor 150 → 600 fF (acore13): static transfer linear to ±0.01 LSB, ENOB 7.3–7.4

## Status / next steps

* v3.0 (2026-08-16): closed-loop post-layout ENOB 7.32 (4.69 MHz) / 7.40 (312.5 kHz), 488 µW, FoM 305 fJ/step; full-chip signoff clean.
* Next: 4× wider top-plate reset TG (track τ 4 → 1 ns, ENOB → ~7.9 expected), asynchronous SAR controller (digital ≈ half of the power), separate VREF pad, KLayout full-chip density/DRC rerun.

## License

Original files: Apache-2.0. Files derived from iic-jku/ihp-sg13g2-ams-chip-template keep SHL-2.1 (see `sar-chip/README.md`).
The IHP SG13G2 PDK and IIC-OSIC-TOOLS are used under their own licenses and are not part of this repository.
