#!/usr/bin/env python3
"""Assemble the core14 LVS reference netlist: stdcell CDL (from core13_full.cdl head)
+ harden_v8 sar_ctrl spice (continuations joined, black boxes dropped) + acore11
blocks (from core13_full.cdl) + new top level (P row <- dac_code_n, N row <- dac_code,
comparator outputs -> cmp/cmp_n, clk_cmp from the macro, no outn export)."""
import re
old = open("core13_full.cdl").read().split("\n")
i_sar = next(i for i, l in enumerate(old) if l.startswith(".subckt sar_ctrl "))
i_sar_end = next(i for i in range(i_sar, len(old)) if old[i].strip() == ".ends")
i_top = next(i for i, l in enumerate(old) if l.startswith(".subckt oa_sar8_core13"))
head = old[:i_sar]
mid = old[i_sar_end + 1:i_top]

lg = open("/foss/designs/sar-adc/logic/final/spice/sar_ctrl.spice").read().split("\n")
joined = []
for ln in lg:
    if ln.startswith("+") and joined:
        joined[-1] += " " + ln[1:].strip()
    else:
        joined.append(ln)
lgj = "\n".join(joined)
lgj = re.sub(r"\* Black-box entry subcircuit for \S+ abstract view\n\.subckt \S+[^\n]*\n\.ends\n", "", lgj)
ports = re.search(r"\.subckt sar_ctrl ([^\n]*)", lgj).group(1).split()
print("sar_ctrl ports:", ports)

lmap = {f"dac_code[{k}]": f"ctl{k}n" for k in range(8)}          # N row <- dac_code
lmap.update({f"dac_code_n[{k}]": f"ctl{k}" for k in range(8)})   # P row <- dac_code_n
lmap.update({"cmp": "outp", "cmp_n": "outn", "clk_cmp": "clk_cmp", "sample": "trk", "clk": "clk"})
top = [".subckt oa_sar8_core14 vinp vinn vcm VDD VSS busy done result[0] result[1] result[2] result[3] result[4] result[5] result[6] result[7] rst_n start clk",
       "Xacore vinp vinn vcm clk_cmp trk ctl7 ctl6 ctl5 ctl4 ctl3 ctl2 ctl1 ctl0 outp outn VDD VSS ctl0n ctl1n ctl2n ctl3n ctl4n ctl5n ctl6n ctl7n oa_sar8_acore11",
       "Xlogic " + " ".join(lmap.get(p, p) for p in ports) + " sar_ctrl",
       ".ends", ""]
out = "\n".join(head) + "\n" + lgj + "\n" + "\n".join(mid) + "\n" + "\n".join(top)
open("core14_full.cdl", "w").write(out)
print("core14_full.cdl written", len(out.split(chr(10))), "lines")
