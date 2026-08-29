#!/usr/bin/env python3
"""Build the LVS reference netlist for oa_sar8_core17_async."""
import re
from pathlib import Path


HERE = Path(__file__).resolve().parent
CORE16 = HERE / "core16_full.cdl"
ACORE13 = HERE / "acore13.cdl"
ASYNC_SPICE = (
    HERE.parent
    / "logic/runs/RUN_2026-08-20_POSTDAC_PENDING/final/spice/sar_ctrl_async_phys.spice"
)
OUT = HERE / "core17_async_full.cdl"


def find_subckt(lines, name):
    start = next(
        i for i, line in enumerate(lines)
        if re.match(rf"\s*\.subckt\s+{re.escape(name)}(?:\s|$)", line, re.I)
    )
    end = next(
        i for i in range(start + 1, len(lines))
        if re.match(r"\s*\.ends(?:\s|$)", lines[i], re.I)
    )
    return start, end


# Reuse the repository's transistor-level SG13G2 standard-cell CDL library.
old = CORE16.read_text().splitlines()
old_logic_start, old_logic_end = find_subckt(old, "sar_ctrl")
old_top_start, old_top_end = find_subckt(old, "oa_sar8_core16")
stdcell_head = old[:old_logic_start]

# Use the complete, already LVS-matched analog reference from acore13.cdl.
analog = ACORE13.read_text().splitlines()

# The OpenROAD final SPICE contains empty abstract-view declarations followed
# by the extracted async macro.  The former are removed because transistor-
# level versions are already present in stdcell_head.
logic_text = ASYNC_SPICE.read_text()
logic_text = re.sub(
    r"\* Black-box entry subcircuit[^\n]*\n"
    r"\s*\.subckt\s+\S+[^\n]*\n\s*\.ends\s*\n",
    "",
    logic_text,
    flags=re.I,
)
logic_lines = logic_text.splitlines()
logic_start, logic_end = find_subckt(logic_lines, "sar_ctrl_async_phys")
logic = logic_lines[logic_start:logic_end + 1]

# Join continuation lines only to recover the exact top-macro port ordering.
joined = []
for line in logic:
    if line.startswith("+") and joined:
        joined[-1] += " " + line[1:].strip()
    else:
        joined.append(line)
ports = re.match(
    r"\s*\.subckt\s+sar_ctrl_async_phys\s+(.*)", joined[0], re.I
).group(1).split()
unused_debug_ports = {"cmp_fault", "cmp_valid"}
unused_debug_ports.update(f"bit_active[{bit}]" for bit in range(8))
ports = [port for port in ports if port not in unused_debug_ports]

# KLayout only promotes child pins that connect outside the child hierarchy.
# The ten debug-only outputs have no top-level route, so make them internal
# nets in the schematic macro too by dropping them from its formal port list.
body_start = 1
while body_start < len(logic) and logic[body_start].startswith("+"):
    body_start += 1
logic = [".subckt sar_ctrl_async_phys " + " ".join(ports)] + logic[body_start:]

net = {"VDD": "VDD", "VSS": "VSS", "busy": "busy", "done": "done",
       "cmp_fire": "clk_cmp", "cmp_p": "outp", "cmp_n": "outn",
       "hold_req": "hold", "sample": "trk", "rst_n": "rst_n",
       "track": "track", "cmp_fault": "cmp_fault_i",
       "cmp_valid": "cmp_valid_i"}
for bit in range(8):
    net[f"bit_active[{bit}]"] = f"bit_active_i[{bit}]"
    net[f"result[{bit}]"] = f"result[{bit}]"
    # Physical polarity contract: P-side row gets the complement; N-side row
    # gets the true code, matching gen_core17_async.py and acore13.cdl.
    net[f"dac_code[{bit}]"] = f"ctl{bit}n"
    net[f"dac_code_n[{bit}]"] = f"ctl{bit}"

top_ports = ["vinp", "vinn", "vcm", "VDD", "VSS", "track", "busy", "done",
             "rst_n"] + [f"result[{bit}]" for bit in range(8)]
top = [
    ".subckt oa_sar8_core17_async " + " ".join(top_ports),
    "Xacore vinp vinn vcm clk_cmp trk hold "
    "ctl7 ctl6 ctl5 ctl4 ctl3 ctl2 ctl1 ctl0 outp outn VDD VSS "
    "ctl0n ctl1n ctl2n ctl3n ctl4n ctl5n ctl6n ctl7n oa_sar8_acore13",
    "Xlogic " + " ".join(net.get(port, port) for port in ports)
    + " sar_ctrl_async_phys",
    ".ends",
    "",
]

OUT.write_text(
    "\n".join(stdcell_head + logic + analog + top),
    newline="\n",
)
print("async ports:", ports)
print(f"wrote {OUT.name}: {len(OUT.read_text().splitlines())} lines")
