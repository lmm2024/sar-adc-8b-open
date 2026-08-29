import pya

lvs = pya.LayoutVsSchematic()
lvs.read("lvs_bs/bstrap.klayout.lvs/bstrap.lvsdb")
print("layers:", lvs.layer_names()[:60])

nl = lvs.netlist()
circ = nl.circuit_by_name("bstrap")
mega = None
for net in circ.each_net():
    if "|" in net.expanded_name():
        mega = net
print("mega:", mega.expanded_name() if mega else None)

for lname in ("Metal2", "metal2", "m2", "Metal2_con", "metal2_con"):
    li = lvs.layer_by_name(lname)
    if li is not None:
        print("== layer", lname)
        r = lvs.shapes_of_net(mega, li, True)
        polys = sorted((p.bbox() for p in r.each_merged()),
                       key=lambda b: (b.left, b.bottom))
        for b in polys:
            print(f"   ({b.left/1000:.2f},{b.bottom/1000:.2f};"
                  f"{b.right/1000:.2f},{b.top/1000:.2f})")
        break
