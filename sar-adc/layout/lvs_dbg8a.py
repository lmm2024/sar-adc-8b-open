import pya

lvs = pya.LayoutVsSchematic()
lvs.read("lvs_a8/oa_sar8_acore8.klayout.lvs/oa_sar8_acore8.lvsdb")
xr = lvs.xref()

st = {getattr(pya.NetlistCrossReference, s): s for s in
      ("Match", "NoMatch", "Mismatch", "MatchWithWarning", "Skipped")}

for cp in xr.each_circuit_pair():
    a, b = cp.first(), cp.second()
    name = (a.name if a else "-") + " / " + (b.name if b else "-")
    print(f"[{st.get(cp.status(), cp.status())}] {name}")
    if st.get(cp.status()) in ("Match", "MatchWithWarning"):
        continue
    n = 0
    for np in xr.each_net_pair(cp):
        if st.get(np.status()) not in ("Match", "MatchWithWarning"):
            fa, fb = np.first(), np.second()
            print("   net:", fa.expanded_name() if fa else None, "<->",
                  fb.expanded_name() if fb else None, st.get(np.status()))
            n += 1
            if n > 14:
                break
    n = 0
    for dp in xr.each_device_pair(cp):
        if st.get(dp.status()) not in ("Match", "MatchWithWarning"):
            fa, fb = dp.first(), dp.second()
            print("   dev:", (fa.expanded_name() if fa else None),
                  "<->", (fb.expanded_name() if fb else None), st.get(dp.status()))
            n += 1
            if n > 9:
                break
