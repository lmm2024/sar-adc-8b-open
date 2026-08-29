import pya

ly = pya.Layout()
ly.read("bstrap.gds")
tc = ly.cell("bstrap")
l2n = pya.LayoutToNetlist(pya.RecursiveShapeIterator(ly, tc, []))
lay = {}
for (num, dt), nm in {(8, 0): "m1", (19, 0): "v1", (10, 0): "m2", (29, 0): "v2",
                      (30, 0): "m3", (49, 0): "v3", (50, 0): "m4", (66, 0): "v4",
                      (67, 0): "m5", (129, 0): "vmim", (36, 0): "mim",
                      (126, 0): "tm1"}.items():
    lay[nm] = l2n.make_layer(ly.layer(num, dt), nm)
for nm in lay:
    l2n.connect(lay[nm])
for a, v, b in (("m1", "v1", "m2"), ("m2", "v2", "m3"), ("m3", "v3", "m4"),
                ("m4", "v4", "m5"), ("m5", "vmim", "tm1"), ("m5", "mim", "tm1")):
    l2n.connect(lay[a], lay[v])
    l2n.connect(lay[v], lay[b])
l2n.extract_netlist()

net = l2n.probe_net(lay["m1"], pya.DPoint(1.0, -2.1))
print("net:", net.expanded_name())
for nm in ("v1", "v2"):
    r = l2n.shapes_of_net(net, lay[nm], True)
    pts = sorted((round(p.bbox().center().x / 1000, 2),
                  round(p.bbox().center().y / 1000, 2)) for p in r.each_merged())
    print(f"{nm} x{len(pts)}:", pts)
r = l2n.shapes_of_net(net, lay["m3"], True)
print("tall/odd M3:")
for p in r.each_merged():
    b = p.bbox()
    if (b.top - b.bottom) > 500:
        print(f"   ({b.left/1000:.2f},{b.bottom/1000:.2f};{b.right/1000:.2f},{b.top/1000:.2f})")
r = l2n.shapes_of_net(net, lay["m2"], True)
print("wide M2 (>1.3):")
for p in r.each_merged():
    b = p.bbox()
    if (b.right - b.left) > 1300:
        print(f"   ({b.left/1000:.2f},{b.bottom/1000:.2f};{b.right/1000:.2f},{b.top/1000:.2f})")
