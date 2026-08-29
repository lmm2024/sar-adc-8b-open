#!/usr/bin/env python3
"""Bisection: write PEX netlist variants with all parasitic C's touching a set of nets removed."""
import re, sys
SRC = "/foss/designs/sar-adc/layout/pex_a12/oa_sar8_acore12.pex.spice"
txt = open(SRC).read().split("\n")
lines = []
for ln in txt:
    if ln.startswith("+") and lines: lines[-1] += " " + ln[1:]
    else: lines.append(ln)
GROUPS = {
  "P1_tops":   {"sw_tg_0.bot", "cdac_array_1.topp"},
  "P2_gb":     {"bstrap_1.gb", "bstrap_0.gb"},
  "P3_ctl":    {"bstrap_1.ckb", "trk", "hold"},
  "P4_bits":   None,   # regex below: sw_bitcell11_*.bot, cdac_array_0.b*, cdac_array_0.term (bit lines)
  "P5_rails":  {"sw_bitcell11_8.VSS", "sw_bitcell11_17.VSS", "bstrap_1.out", "bstrap_0.out"},
  "P6_topctl": "TOPCTL",   # only top <-> control/fixed nets (hold, trk, trkb, gb, vinr, vcm, VDD, VSS)
  "P7_topcmp": "TOPCMP",   # only top <-> comparator internal nodes / outputs / clk_cmp
  "P8_hold":   "SET:hold",
  "P9_trk":    "SET:trk,bstrap_1.ckb",
  "P10_gbvin": "SET:bstrap_1.gb,bstrap_0.gb,bstrap_1.out,bstrap_0.out",
}
TOPS = {"sw_tg_0.bot", "cdac_array_1.topp"}
CTL = {"hold", "trk", "bstrap_1.ckb", "bstrap_1.gb", "bstrap_0.gb", "bstrap_1.out", "bstrap_0.out", "vcm", "VDD", "VSS", "0"}
CMP = {"a_28008_23477#", "a_26184_21025#", "a_30632_22281#", "outp", "outn", "clk_cmp"}
for name, nets in GROUPS.items():
    out = []; removed = 0
    for ln in lines:
        m = re.match(r"^[Cc]\S+\s+(\S+)\s+(\S+)\s+", ln)
        if m:
            a, b = m.group(1), m.group(2)
            if nets is None:
                hit = any(re.match(r"^(sw_bitcell11_\d+\.bot|cdac_array_0\.(b\d|term))$", x) for x in (a, b))
            elif nets == "TOPCTL":
                hit = (a in TOPS and b in CTL) or (b in TOPS and a in CTL)
            elif nets == "TOPCMP":
                hit = (a in TOPS and b in CMP) or (b in TOPS and a in CMP)
            elif isinstance(nets, str) and nets.startswith("SET:"):
                S = set(nets[4:].split(","))
                hit = (a in TOPS and b in S) or (b in TOPS and a in S)
            else:
                hit = a in nets or b in nets
            if hit:
                removed += 1; continue
        out.append(ln)
    open(f"/foss/designs/sar-adc/power/pex_{name}.spice", "w").write("\n".join(out))
    print(name, "removed", removed, "caps")
