#!/usr/bin/env python3
"""Build the hierarchical LVS reference for oa_sar8_acore18_opt."""
from pathlib import Path


here = Path(__file__).resolve().parent
text = (here / "acore13.cdl").read_text(encoding="utf-8")
text = text.replace("oa_sar8_acore13", "oa_sar8_acore18_opt")

# Main and replica arrays use identical bit-specific physical cells.
for prefix in ("Xsw", "Xswr"):
    for inst, bit in enumerate(range(7, -1, -1)):
        name = f"{prefix}{inst}"
        lines = text.splitlines()
        for i, line in enumerate(lines):
            if line.startswith(name + " "):
                lines[i] = line.rsplit(" ", 1)[0] + f" sw_bitcell_opt_b{bit}"
        text = "\n".join(lines) + "\n"

for name in ("Xsw8", "Xswr8"):
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith(name + " "):
            lines[i] = line.rsplit(" ", 1)[0] + " sw_bitcell_opt_term"
    text = "\n".join(lines) + "\n"

for name in ("Xsw10", "Xtgr"):
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith(name + " "):
            lines[i] = line.rsplit(" ", 1)[0] + " sw_tg_opt"
    text = "\n".join(lines) + "\n"

text = text.replace("Xboot vinp vinr trkb gb VDD VSS bstrap40",
                    "Xboot vinp vinr trkb gb VDD VSS bstrap_opt_w2_c1200")
text = text.replace("Xbootn vinn vinnr trkb gbn VDD VSS bstrap40",
                    "Xbootn vinn vinnr trkb gbn VDD VSS bstrap_opt_w2_c1200")

extra = []
for path in [here / "bs" / "bstrap_opt_w2_c1200.cdl",
             here / "sw" / "sw_tg_opt.cdl",
             here / "sw" / "sw_bitcell_opt_term.cdl"]:
    extra.append(path.read_text(encoding="utf-8").strip())
for bit in range(8):
    extra.append((here / "sw" / f"sw_bitcell_opt_b{bit}.cdl").read_text(encoding="utf-8").strip())

out = here / "acore18_opt.cdl"
out.write_text(text.rstrip() + "\n\n" + "\n\n".join(extra) + "\n", encoding="utf-8")
print(out)
