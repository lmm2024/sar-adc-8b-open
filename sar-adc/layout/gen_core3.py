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
top = layout.create_cell("oa_sar8_core3")

layout.read("oa_sar8_acore3.gds")
layout.read("/foss/designs/sar-adc/logic/final/gds/sar_ctrl.gds")
ac = layout.cell("oa_sar8_acore3")
lg = layout.cell("sar_ctrl")

L = {}
for num, name in ((10, "m2"), (29, "v2"), (30, "m3")):
    L[name] = layout.layer(num, 0)
for num, tag in ((10, "m2"), (30, "m3")):
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
vwire(121.3, -11.7, 49.98)
via2(121.3, -11.7)

# ---- dac_code[k] east fan: pin -> M2 jog -> corridor drop -> ctl track -> stub
DAC_Y = {0: 91.14, 1: 79.38, 2: 67.62, 3: 55.86, 4: 44.10,
         5: 32.34, 6: 20.58, 7: 8.82}
DROP_X = {0: 181.3, 1: 180.6, 2: 179.9, 3: 179.2, 4: 178.5,
          5: 177.8, 6: 177.1, 7: 176.4}                 # higher pin -> east drop
TRACK_Y = {k: -37.8 - 1.3 * k for k in range(8)}
STUB_X = {0: 17.1, 1: 30.9, 2: 44.7, 3: 58.5, 4: 72.3,
          5: 86.1, 6: 197.3, 7: 211.1}                  # cell west stubs (acore3)
CTL_Y = -14.1
for k in range(8):
    yp, xd, yt, xs = DAC_Y[k], DROP_X[k], TRACK_Y[k], STUB_X[k]
    via2(LX + 49.8, yp)                                  # on the M3 #E pin
    rect("m2", LX + 49.6, yp - 0.2, xd + 0.2, yp + 0.2)  # M2 jog over M3 rails
    vwire(xd, yt, yp)
    via2(xd, yt)
    rect("m3", min(xd, xs) - 0.2, yt - 0.2, max(xd, xs) + 0.2, yt + 0.2)
    via2(xs, yt)
    vwire(xs, yt, CTL_Y)
    via2(xs, CTL_Y)

# ---- south digital pins re-export (M2 pins at strip bottom)
SPINS = [("rst_n", 3.36), ("start", 7.20)] + \
        [(f"result[{i}]", 11.04 + 3.84 * i) for i in range(8)] + \
        [("done", 41.76), ("busy", 45.60)]
for name, xl in SPINS:
    top.shapes(L["m2p"]).insert(pya.DBox(LX + xl - 0.05, 0.15, LX + xl + 0.05, 0.25))
    top.shapes(L["m2l"]).insert(pya.DText(name, pya.DTrans(pya.DVector(LX + xl, 0.2))))

layout.write("oa_sar8_core3.gds")
b = top.dbbox()
print(f"core3: {b.width():.0f} x {b.height():.0f} um = {b.width()*b.height()/1e6:.3f} mm2")
