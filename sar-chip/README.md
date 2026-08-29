# sar-chip: OA-SAR8 in the IHP SG13G2 AMS chip template

This directory holds only what differs from the upstream template plus the final artifacts.
Everything else (pad cells, PDN scripts, Makefile, verification flow, logos) is taken verbatim
from **iic-jku/ihp-sg13g2-ams-chip-template @ `d193dd2`**
(https://github.com/iic-jku/ihp-sg13g2-ams-chip-template, Solderpad Hardware License v2.1).

## Rebuild the full chip

```bash
git clone https://github.com/iic-jku/ihp-sg13g2-ams-chip-template.git sar-chip-full
cd sar-chip-full && git checkout d193dd2
# our changes on top of the template
patch -p0 < ../sar-chip/upstream_d193dd2.patch          # rtl/chip_top.sv rtl/chip_core.sv flow/librelane/{config.yaml,pdn_cfg.tcl}
mkdir -p macros/oa_sar8/final && cp -r ../sar-chip/macros/oa_sar8/final/* macros/oa_sar8/final/
# run inside the IIC-OSIC-TOOLS container (repository root mounted at /foss/designs)
librelane flow/librelane/config.yaml --pdk ihp-sg13g2 --pdk-root /foss/pdks --manual-pdk \
   --save-views-to flow/final/ --skip KLayout.DRC --skip Magic.DRC --skip KLayout.Antenna --skip KLayout.Density
```

The macro `oa_sar8_core16` (GDS shifted to origin + `prBoundary`, LEF with boundary pins and
full-length TopMetal2 power bars, Verilog black box) is produced by
`sar-adc/layout/mk_lef16.py` from `sar-adc/layout/oa_sar8_core16.gds`.

## What changed vs. upstream

| File | Change |
|---|---|
| `rtl/chip_top.sv` | pad counts (VDD/VSS 4+4, 15 outputs, 1 bidir, 3 analog) |
| `rtl/chip_core.sv` | instantiates `oa_sar8_core16` (vinp/vinn/vcm on analog pads via secondary ESD, start on input pad 0, result/done/busy on output pads 0..9) |
| `flow/librelane/config.yaml` | pad lists, `MACROS: oa_sar8_core16` (location 600, 651), `RSZ_DONT_TOUCH_LIST` for the analog pad nets |
| `flow/librelane/pdn_cfg.tcl` | dedicated `sar_adc` PDN grid: TopMetal2 stripes pitch 100 / offset 109.2 landing on the macro's TM2 bars, TM1↔TM2 connect |

## Final artifacts

* `layout/chip_top.gds.gz` : final 1.6 × 1.6 mm chip (32 pads), LibreLane run `RUN_2026-08-16_09-07-48`
* `layout/chip_top_render.png` : rendered top view
* `final/metrics.json`, `final/metrics.csv`, `final/reports/*` : signoff (LVS 0 diff, antenna 0, setup/hold no violation, XOR 0)
* `macros/oa_sar8/final/{gds,lef,vh}/oa_sar8_core16.*` : the SAR ADC hard macro as used by the chip

Pad map (bottom→top / left→right): West `busy, VSS, VDD, IOVSS, IOVDD, start, rst_n, clk`;
North `result[7]…result[0]`; South `VSS, VDD, done, spare, spare, spare, VDD, VSS`;
East `VSS, vinn, vinp, vcm, VDD, spare, spare, spare(bidir)`.
