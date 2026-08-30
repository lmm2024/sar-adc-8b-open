# core18 PDN-fixed release candidate (2026-08-30)

This directory contains compact evidence for the released digital-asynchronous
OA-SAR8 core. The analog hierarchy, top-level routing, SAR RTL, and SAR signal
path are unchanged from the frozen 7.9643-bit reference. Only the physical
power distribution of `sar_ctrl_async_phys` was changed.

## Physical change

- Digital-macro PDN pitch: 75.6 µm → 30 µm.
- Added a local VSS stripe at x=55.08 µm.
- The MSB output buffer is at x=58.08 µm, reducing its VSS return distance
  from about 33 µm to about 3 µm.
- The existing `via_stack$1` M3/M4 minimum-area repair is retained.

The change removes the old full-RC PEX convergence hotspot without adding an
MSB buffer or changing logical behavior. The rejected one-sided
`sg13g2_buf_2` experiment is not part of this release.

## Verification summary

| Check | Result |
|---|---|
| Digital macro DRC/LVS/antenna | pass / pass / pass |
| Complete-core LVS | MATCH |
| Complete-core maximum DRC | 0 |
| Complete-core regular DRC | 9 density/fill-only markers |
| PEX | Magic full RC, `-m 3 -t 10000 -r 1000 -y 1` |
| 10 MS/s near-Nyquist | 33/33, 49.6832 dB SNDR, 7.9607-bit ENOB |
| 10 MS/s, 312.5 kHz input | 33/33, 47.3143 dB SNDR, 7.5672-bit ENOB |
| 10.5 MS/s phase screen | 7.7755-bit ENOB, below the 7.95-bit target |
| 257-point DC transfer screen | 257/257 complete, monotonic on grid; codes 11–251 |

The nine regular-DRC markers are the expected bare-macro density checks
(`AFil.g`, `GFil.g`, `M1.j`–`M5.j`, `TM1.c`, `TM2.c`). They are not geometry,
spacing, short, or connectivity errors. Density fill belongs at full-chip
integration, followed by a new full-chip DRC/LVS run.

The digital macro metrics retain one max-fanout constraint warning. It is not
a DRC/LVS/antenna failure; max slew and max capacitance are both zero, and the
closed-loop full-RC PEX result is used as the functional timing acceptance.

The 257-point static-transfer screen uses a 10.9375 mV grid (one nominal
full-scale LSB). It is strictly monotonic, with 19 codes not hit by this coarse
grid and a maximum best-fit residual of 3.56 code LSB. These values indicate
where a finer transition sweep should focus; they are not transition-level
DNL/INL sign-off.

## Important files

- `../../layout/oa_sar8_core18_final.gds`: released GDS.
- `../../layout/oa_sar8_core18_final_base_7p9643.gds`: frozen base used by the
  deterministic macro-replacement flow.
- `../../layout/core18_final_full.cdl`: LVS source netlist.
- `../../layout/pex_core18_final_w2_rc/oa_sar8_core18_final.pex.spice`:
  checked-in full-RC PEX netlist.
- `../../logic/final_async_phys/`: complete hardened digital macro views.
- `../../layout/replace_async_macro_pdnfix.py`: physical rebuild step.
- `../../postlayout/run_core18_pex.py`: continuous-deck PEX runner.
- `results/`: compact metrics and sample codes.
- `reports/`: key DRC/LVS/PEX console logs.

See the repository root `REPRODUCE_SIGNOFF.md` for exact commands.
