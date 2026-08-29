import pya

lvs = pya.LayoutVsSchematic()
lvs.read("lvs_c11/oa_sar8_core11.klayout.lvs/oa_sar8_core11.lvsdb")
xr = lvs.xref()

st = {getattr(pya.NetlistCrossReference, s): s for s in
      ("Match", "NoMatch", "Mismatch", "MatchWithWarning", "Skipped")}

for cp in xr.each_circuit_pair():
    a, b = cp.first(), cp.second()
    if not a or a.name != "oa_sar8_acore9":
        continue
    print("=== oa_sar8_acore9 pair, status:", st.get(cp.status()))
    print("-- layout pins:", [p.name() for p in a.each_pin()])
    print("-- schem  pins:", [p.name() for p in b.each_pin()] if b else None)
    for np_ in xr.each_net_pair(cp):
        fa, fb = np_.first(), np_.second()
        print("  net", (fa.expanded_name() if fa else "-").ljust(14),
              "<->", (fb.expanded_name() if fb else "-").ljust(8),
              st.get(np_.status()))
    for pp in xr.each_pin_pair(cp):
        fa, fb = pp.first(), pp.second()
        print("  pin", (fa.name() if fa else "-"), "<->",
              (fb.name() if fb else "-"), st.get(pp.status()))
