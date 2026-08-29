import pya

lvs = pya.LayoutVsSchematic()
lvs.read("lvs_bs/bstrap.klayout.lvs/bstrap.lvsdb")
nl = lvs.netlist()
circ = nl.circuit_by_name("bstrap")
for net in circ.each_net():
    name = net.expanded_name()
    if "|" not in name:
        continue
    print("=== mega net:", name)
    for lname, linfo in (("via1", (19, 0)), ("via2", (29, 0))):
        li = lvs.internal_layout().find_layer(*linfo)
        if li is None:
            print(lname, ": layer not in db")
            continue
        try:
            r = lvs.shapes_of_net(net, li, True)
        except Exception as e:
            print(lname, "err", e)
            continue
        pts = []
        for p in r.each_merged():
            b = p.bbox()
            pts.append((round(b.center().x / 1000.0, 2),
                        round(b.center().y / 1000.0, 2)))
        print(f"{lname}: {len(pts)}")
        for p in sorted(pts):
            print("   ", p)
