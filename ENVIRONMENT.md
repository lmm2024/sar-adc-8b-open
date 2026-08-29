# Environment (portable, fully open source)

Everything in this repository was designed, simulated, laid out and verified with the
**IIC-OSIC-TOOLS** container image (JKU) and the **IHP SG13G2** open PDK. No GUI is
needed: every step is a shell command executed inside the container.

## 1. Container

| Item | Value used for this project |
|---|---|
| Image | `docker.io/hpretl/iic-osic-tools:2026.07` (Ubuntu 24.04, `IIC_OSIC_TOOLS_VERSION=2026.07`) |
| Host | macOS (Apple Silicon) with **Colima** (`colima start --cpu 4 --memory 12 --disk 60`); any Docker host works |
| Mount | repository root → `/foss/designs` (the scripts use absolute paths `/foss/designs/sar-adc/...` and `/foss/designs/sar-chip/...`) |
| Start | `./start_x.sh` / `./start_vnc.sh` from the IIC-OSIC-TOOLS repo, or `docker run -d --name iic -v $PWD:/foss/designs hpretl/iic-osic-tools:2026.07 tail -f /dev/null` |
| Shell | **always** `docker exec <container> bash -lc "…"` (the `-l` login shell sets `PATH` for `klayout`, `ngspice`, `librelane`, `sak-*.sh`, `verilator`) |

Tool versions inside the image (as printed by the tools):

| Tool | Version |
|---|---|
| KLayout | 0.30.9 (layout generation, DRC, LVS, PEX via `sak-drc.sh / sak-lvs.sh / sak-pex.sh` in `/foss/tools/sak`) |
| ngspice | 46, compiled with the KLU solver (`.option klu`) |
| LibreLane | 3.1.0.dev2 (Yosys 0.67, OpenROAD 26Q3-850, Magic 8.3.678, netgen) |
| Icarus Verilog | 14.0 (devel s20260301) |
| kpex | 0.3.12 (2.5-D extraction, used as a second opinion for the comparator) |
| PDK | IHP SG13G2, `/foss/pdks/ihp-sg13g2`, commit `84374023ee8b4b126bebbba67fcbada0a9c0ff0b` |

`tools/run.sh` wraps `docker exec … bash -lc` (set `CONTAINER=<name>`; the default is the
name Colima gives the xvnc container, `iic-osic-tools_xvnc_uid_$(id -u)`).

## 2. Pitfalls we hit (so you do not have to)

* Use `bash -lc`. Without the login shell `verilator`, `sak-*.sh` and `librelane` are not on `PATH`.
* KLayout PCells: the RF-family MOS PCells carry their own M2 + internal vias on the S/D bars;
  add vias only on top of those bars, never inside the bar spacing (V1.b). Pin boxes must be
  fully covered by metal (Pin.f). Via coordinates snap to 0.01 µm.
* LVS reference netlists (CDL) must carry `rfmode=1` on the MOS devices, otherwise KLayout LVS
  finds zero device pairs.
* `sak-lvs.sh` runs with `IGNORE_TOP_PORTS_MISMATCH`: **always inspect the `.SUBCKT` port line of
  `*_extracted.cir`**. A floating top-level pin (we had a missing via on `clk`) still "matches".
* Mixed-signal post-layout decks: use `spice/sg13g2_stdcell.spice` (transistor level) for the
  standard cells, join `+` continuation lines, tie the PEX `sub` node to `0`, and **`.save` only the
  vectors you need**, otherwise ngspice-46 aborts with *"memory required … more than memory
  available"* on long transients.
* Speed knobs that keep the results identical (measured 3.3× on this design): `.option klu`,
  merge the 514 `cap_cmim` unit instances per net pair, default `chgtol/abstol`, `tran … 0.2n`.
  Run one ngspice per core with `OMP_NUM_THREADS=1`.
* Inside `docker exec … bash -lc "pkill -f pattern"` the pattern also matches the calling shell
  and kills it (exit 143). Use `pkill -x ngspice`.
* Rendering the full-chip GDS: the top cell carries a huge PDK "device registration" box; use
  `zoom_box(0,0,1600,1600)` instead of `zoom_fit()`.
* Adding an S-side pin to the LibreLane macro re-spaces the whole pin row (0.96 µm pitch):
  regenerate `logic/pins.py` output and update the core generator coordinates.
