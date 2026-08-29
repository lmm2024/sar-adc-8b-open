#!/usr/bin/env python3
"""OA-SAR8 core v3 -- narrow-seam reference floorplan, full assembly:
verified acore3 + 50x100 logic strip in the seam (x 122..172).
West margin = 5-track M2 bus (VSS 118.5 | VDD 119.2 | clk 119.9 | cmp 120.6 |
sample 121.3). dac_code exits EAST as M2 jogs threading the replica's wide-M3
rail zone (M2-free corridor x 176.4..181.8), down to 8 ctl tracks (y -37.8..)
that run to the split switch-row ctl stubs. Digital S-pins re-exported."""
import pya

layout = pya.Layout()
layout.technology_name = "sg13g2"
layout.dbu = 0.001
top = layout.create_cell("oa_sar8_core8")

layout.read("oa_sar8_acore7.gds")
layout.read("/foss/designs/sar-adc/logic/final/gds/sar_ctrl.gds")
ac = layout.cell("oa_sar8_acore7")
lg = layout.cell("sar_ctrl")

L = {}
for num, name in ((10, "m2"), (29, "v2"), (30, "m3"), (49, "v3"), (50, "m4"), (8, "m1")):
    L[name] = layout.layer(num, 0)
for num, tag in ((10, "m2"), (30, "m3"), (8, "m1")):
    L[tag + "p"], L[tag + "l"] = layout.layer(num, 2), layout.layer(num, 25)


def rect(lay, x1, y1, x2, y2):
    top.shapes(L[lay]).insert(pya.DBox(x1, y1, x2, y2))


def snap(v):
    return round(round(v * 100) / 100.0, 2)


def via2(x, y):
    x1, y1 = snap(x - 0.095), snap(y - 0.095)
    rect("v2", x1, y1, x1 + 0.19, y1 + 0.19)
    rect("m2", x - 0.2, y - 0.2, x + 0.2, y + 0.2)
    rect("m3", x - 0.2, y - 0.2, x + 0.2, y + 0.2)


def vwire(x, y1, y2):
    rect("m2", x - 0.2, min(y1, y2), x + 0.2, max(y1, y2))


def via3(x, y):
    x1, y1 = snap(x - 0.095), snap(y - 0.095)
    rect("v3", x1, y1, x1 + 0.19, y1 + 0.19)
    rect("m3", x - 0.2, y - 0.2, x + 0.2, y + 0.2)
    rect("m4", x - 0.2, y - 0.2, x + 0.2, y + 0.2)


def v4wire(x, y1, y2):
    rect("m4", x - 0.2, min(y1, y2), x + 0.2, max(y1, y2))


top.insert(pya.DCellInstArray(ac.cell_index(), pya.DTrans()))
LX = 122.0
top.insert(pya.DCellInstArray(lg.cell_index(), pya.DTrans(pya.DVector(LX, 0.0))))

# ---- west margin joins: clk (@82.74) -> cmp clk bus ext (y 122.5)
rect("m3", 119.7, 82.54, LX + 0.4, 82.94)
via2(119.9, 82.74)
vwire(119.9, 82.74, 122.5)
via2(119.9, 122.5)

# ---- cmp: comparator outp ext (y 109.4) -> riser 120.6 -> logic cmp (@17.22)
via2(120.6, 109.4)
vwire(120.6, 17.22, 109.4)
via2(120.6, 17.22)
rect("m3", 120.4, 17.02, LX + 0.4, 17.42)

# ---- sample (@49.98) -> riser 121.3 -> trk bus (y -11.7)
rect("m3", 121.1, 49.78, LX + 0.4, 50.18)
via2(121.3, 49.98)
vwire(121.3, -4.5, 49.98)
via2(121.3, -4.5)
via3(121.3, -4.5)
v4wire(121.3, -11.7, -4.5)
via3(121.3, -11.7)

# ---- dac_code[k]: south pins -> straight M2 drops down the seam -> ctl tracks -> stubs
DAC_X = {k: LX + 42.72 - 1.92 * k for k in range(8)}       # dac0 164.72 .. dac7 151.28
TRACK_Y = {k: -38.0 - 1.3 * k for k in range(8)}
STUB_X = {0: 7.0, 1: 20.8, 2: 34.6, 3: 48.4, 4: 62.2,
          5: 76.0, 6: 89.8, 7: 103.6}
CTL_Y = -14.1
for k in range(8):
    xd, yt, xs = DAC_X[k], TRACK_Y[k], STUB_X[k]
    vwire(xd, yt, 0.4)                                   # M2 drop into the pin metal
    via2(xd, yt)
    rect("m3", xs - 0.2, yt - 0.2, xd + 0.2, yt + 0.2)
    via2(xs, yt)
    vwire(xs, yt, CTL_Y)
    via2(xs, CTL_Y)

# ---- south digital pins re-export (M2 pins at strip bottom)
SPINS = [("rst_n", 6.24), ("start", 8.16)] + \
        [(f"result[{i}]", 10.08 + 1.92 * i) for i in range(8)] + \
        [("done", 25.44), ("busy", 27.36)]
for name, xl in SPINS:
    top.shapes(L["m2p"]).insert(pya.DBox(LX + xl - 0.05, 0.15, LX + xl + 0.05, 0.25))
    top.shapes(L["m2l"]).insert(pya.DText(name, pya.DTrans(pya.DVector(LX + xl, 0.2))))

# ---- top-level analog/power pin exports (touch the acore7 pin metal)
for name, lay_, x1, y1, x2, y2 in (("vin", "m3", 332.9, -11.1, 333.5, -10.7),
                                    ("vcm", "m3", 160.0, -10.02, 160.5, -9.62),
                                    ("outn", "m3", 249.0, 110.0, 250.0, 110.4),
                                    ("VSS", "m1", 2.6, -20.1, 3.4, -19.7),
                                    ("VDD", "m1", 2.6, -5.5, 3.4, -5.1)):
    rect(lay_, x1, y1, x2, y2)
    top.shapes(L[lay_ + "p"]).insert(pya.DBox(x1, y1, x2, y2))
    top.shapes(L[lay_ + "l"]).insert(pya.DText(name, pya.DTrans(pya.DVector((x1 + x2) / 2, (y1 + y2) / 2))))
top.shapes(L["m3l"]).insert(pya.DText("clk", pya.DTrans(pya.DVector(119.9, 100.0))))
rect("m3", 119.7, 99.8, 120.1, 100.2)
top.shapes(L["m3p"]).insert(pya.DBox(119.7, 99.8, 120.1, 100.2))

layout.write("oa_sar8_core8.gds")
b = top.dbbox()
print(f"core8: {b.width():.0f} x {b.height():.0f} um = {b.width()*b.height()/1e6:.3f} mm2")
