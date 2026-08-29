#!/usr/bin/env python3
"""Generate the OA-SAR8 optimized switch family with KLayout batch mode.

Run this script inside the IIC-OSIC-TOOLS container from layout/sw.  It keeps
the validated W3/W6 LSB/terminator driver, applies the mild 2**(bit/6) taper,
and uses W2/W4 sampling and top-plate transmission gates.  These sizes retain
the TT settling result while reducing the PEX-visible hold-edge charge step.
"""
from __future__ import annotations

import json
import math
import os
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent


def run_generator(script: str, **variables: str) -> None:
    env = os.environ.copy()
    env.update({name: str(value) for name, value in variables.items()})
    subprocess.run(["klayout", "-zz", "-r", script], cwd=HERE,
                   env=env, check=True)


def main() -> None:
    manifest: list[dict[str, float | str | int]] = []

    # Fixed one-unit termination cell.
    run_generator(
        "gen_switch11.py", CELLNAME="sw_bitcell_opt_term",
        OUTGDS="sw_bitcell_opt_term.gds",
        NDRV_W="3.0", PDRV_W="6.0", NTG_W="2.0", PTG_W="4.0",
    )
    manifest.append({"cell": "sw_bitcell_opt_term", "role": "termination",
                     "ndrv_um": 3.0, "pdrv_um": 6.0,
                     "ntg_um": 2.0, "ptg_um": 4.0})

    # LSB first.  Taper is intentionally much gentler than binary weighting.
    for bit in range(8):
        scale = 2.0 ** (bit / 6.0)
        # SG13G2 RF PCells must land on the manufacturing grid.  Quantizing
        # the gentle taper to 0.2 um keeps both W and W/2 on a 0.1 um grid.
        ndrv = round((3.0 * scale) / 0.2) * 0.2
        pdrv = 2.0 * ndrv
        cell = f"sw_bitcell_opt_b{bit}"
        run_generator(
            "gen_switch11.py", CELLNAME=cell, OUTGDS=cell + ".gds",
            NDRV_W=f"{ndrv:.8g}", PDRV_W=f"{pdrv:.8g}",
            NTG_W="2.0", PTG_W="4.0",
        )
        manifest.append({"cell": cell, "role": "cdac_bit", "bit": bit,
                         "ndrv_um": ndrv, "pdrv_um": pdrv,
                         "ntg_um": 2.0, "ptg_um": 4.0})

    run_generator(
        "gen_sw_tg.py", CELLNAME="sw_tg_opt", OUTGDS="sw_tg_opt.gds",
        NTG_W="2.0", PTG_W="4.0",
    )
    manifest.append({"cell": "sw_tg_opt", "role": "top_plate_tg",
                     "ntg_um": 2.0, "ptg_um": 4.0})

    (HERE / "optimized_switch_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    print("wrote optimized_switch_manifest.json")


if __name__ == "__main__":
    main()
