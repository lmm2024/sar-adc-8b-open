#!/usr/bin/env python3
"""Tally P($9)/Q($16) couplings in the kpex 2.5D netlist. Units: A=aF, F=fF."""
from collections import defaultdict

caps = []
sufs = defaultdict(int)
for ln in open("sa_comp_k25d_pex_netlist.spice"):
    t = ln.split()
    if t and t[0].startswith("C"):
        n1, n2 = t[1].lstrip("\\"), t[2].lstrip("\\")
        v = t[3].upper()
        if v.endswith("FF"):
            x = float(v[:-2]); sufs["fF"] += 1
        elif v.endswith("AF"):
            x = float(v[:-2]) / 1000; sufs["aF"] += 1
        elif v.endswith("A"):
            x = float(v[:-1]) / 1000; sufs["A"] += 1
        elif v.endswith("F"):
            x = float(v[:-1]); sufs["F"] += 1
        else:
            x = float(v) * 1e15; sufs["raw"] += 1
        caps.append((n1, n2, x))
print("C lines:", len(caps), dict(sufs))

for node, tag in (("$9", "P"), ("$16", "Q")):
    per = defaultdict(float)
    for a, b, v in caps:
        if a == node or b == node:
            per[b if a == node else a] += v
    print(f"\n{tag} = {node}  total {sum(per.values()):.3f} fF")
    for k, v in sorted(per.items(), key=lambda x: -x[1]):
        print(f"   {k:<10s} {v:8.4f} fF")

pv = sum(v for a, b, v in caps if ("$9" in (a, b)) and ("VSS" in (a, b)))
qv = sum(v for a, b, v in caps if ("$16" in (a, b)) and ("VSS" in (a, b)))
print(f"\nP-VSS {pv:.4f} vs Q-VSS {qv:.4f}  delta {pv-qv:+.4f} fF")
