# OA-SAR8 core18 final layout

- Top cell: `oa_sar8_core18_final`
- Bounding box: approximately 385.0 um x 321.0 um (`0.1236 mm2`)
- Process: IHP SG13G2
- Physical verification: KLayout DRC 0; KLayout LVS match

Integrated changes relative to the repository baseline:

- physical asynchronous SAR controller (`sar_ctrl_async_phys`), with no RTL `#` delay;
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
- `mk_acore18_opt_cdl.py`
- `mk_core18_final_cdl.py`

The current signoff establishes geometry-rule correctness and transistor-level
connectivity.  Extracted-parasitic timing/ENOB validation is the next step and
is not implied by DRC/LVS alone.
