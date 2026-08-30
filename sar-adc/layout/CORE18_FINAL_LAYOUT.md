# OA-SAR8 core18 final layout

- Top cell: `oa_sar8_core18_final`
- Bounding box: approximately 385.0 um x 321.0 um (`0.1236 mm2`)
- Process: IHP SG13G2
- Physical verification: block-level maximum DRC 0; KLayout LVS match

Integrated changes relative to the repository baseline:

- physical asynchronous SAR controller (`sar_ctrl_async_phys`), with no RTL `#` delay;
- 30 um digital-macro PDN pitch with a local VSS stripe beside the MSB output;
- two W3 / 1200 fF bootstrapped sampling cells;
- two rows of bit-tapered CDAC switch drivers (`b0` through `b7` plus termination);
- 1.25x top-plate reset transmission gates;
- rerouted P/N DAC controls, sample, hold request, comparator handshake and power;
- unchanged binary CDAC arrays and StrongARM comparator topology.

Primary deliverables:

- `oa_sar8_core18_final.gds`
- `oa_sar8_core18_final.png`
- `core18_final_full.cdl`
- `gen_acore18_opt.py`
- `gen_core18_final.py`
- `replace_async_macro_pdnfix.py`
- `oa_sar8_core18_final_base_7p9643.gds`
- `mk_acore18_opt_cdl.py`
- `mk_core18_final_cdl.py`

The current signoff establishes geometry-rule correctness, transistor-level
connectivity, and closed-loop full-RC PEX operation at 10 MS/s. The released
PEX result is 49.6832 dB SNDR / 7.9607-bit ENOB over 33 conversions. The nine
regular-rule markers are density/fill-only checks for a bare macro; they are
not maximum-rule geometry violations.
