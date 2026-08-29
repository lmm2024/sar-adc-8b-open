import pya

ly = pya.Layout()
ly.read("bstrap.gds")
tc = ly.cell("bstrap")
l2n = pya.LayoutToNetlist(pya.RecursiveShapeIterator(ly, tc, []))

lay = {}
for (num, dt), nm in {(8, 0): "m1", (19, 0): "v1", (10, 0): "m2", (29, 0): "v2",
                      (30, 0): "m3", (49, 0): "v3", (50, 0): "m4", (66, 0): "v4",
                      (67, 0): "m5", (129, 0): "vmim", (36, 0): "mim",
                      (126, 0): "tm1", (125, 0): "tv1"}.items():
    lay[nm] = l2n.make_layer(ly.layer(num, dt), nm)
for nm in lay:
    l2n.connect(lay[nm])
for a, v, b in (("m1", "v1", "m2"), ("m2", "v2", "m3"), ("m3", "v3", "m4"),
                ("m4", "v4", "m5"), ("mim", "vmim", "tm1"), ("m5", "tv1", "tm1")):
    l2n.connect(lay[a], lay[v])
    l2n.connect(lay[v], lay[b])
l2n.extract_netlist()

probes = [("VSSrail", "m1", 1.0, -2.1), ("VDDrail", "m1", 1.0, 7.7),
          ("vin", "m3", 0.0, 6.9), ("out", "m3", 0.0, -1.2),
          ("ckb", "m3", 0.0, 2.9), ("g", "m3", 12.5, 3.7),
          ("cb", "m3", 8.0, 4.5), ("ct", "m3", 25.0, 5.3),
          ("x", "m3", 3.2, 6.1), ("captop", "tm1", 42.0, 10.5),
          ("capbot", "m5", 37.2, 4.5)]
seen = {}
for nm, ln, x, y in probes:
    net = l2n.probe_net(lay[ln], pya.DPoint(x, y))
    key = net.expanded_name() if net else "none"
    seen.setdefault(key, []).append(nm)
for k, v in seen.items():
    print(f"net {k}: {v}")
