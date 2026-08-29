#!/usr/bin/env python3
"""OA-SAR8 FINAL core v2 -- textbook rectangle:
[CDAC_A | comparator(top) + SAR logic(center) + switch row(bottom) | CDAC_B].
Logic has south-facing control pins -> straight drops to 4 reused gap tracks;
cmp/clk/sample take three dedicated laterals just under the row top."""
import pya

layout = pya.Layout()
layout.technology_name = "sg13g2"
layout.dbu = 0.001
top = layout.create_cell("oa_sar8_core2")

layout.read("oa_sar8_acore2.gds")
layout.read("/foss/designs/sar-adc/logic/final/gds/sar_ctrl.gds")
ac = layout.cell("oa_sar8_acore2")
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
    rect("m2", x - 0.17, min(y1, y2), x + 0.17, max(y1, y2))


top.insert(pya.DCellInstArray(ac.cell_index(), pya.DTrans()))
LX, LY = 124.6, 0.0
top.insert(pya.DCellInstArray(lg.cell_index(), pya.DTrans(pya.DVector(LX, LY))))

SW_P = 13.8
SW_X = [122.0 + i * SW_P for i in range(11)]
CTL_Y = -18.0 + 3.9
TRK_Y = -18.0 + 6.3

DAC = {7: 41.76, 6: 53.28, 5: 64.80, 4: 76.32, 3: 87.84, 2: 99.36, 1: 110.88, 0: 122.40}
GAP_T = [-1.0, -1.9, -2.8, -3.7]          # 4 reused gap tracks (mod 4)

# --- dac_code[k] south drops -> gap track -> ctl stub riser
for k in range(8):
    xp = LX + DAC[k]                       # pin x
    xc = SW_X[7 - k] - 0.7                 # ctl_k stub x
    yt = GAP_T[k % 4]
    vwire(xp, LY + 0.4, yt)                # drop into the pin metal
    via2(xp, yt)
    rect("m3", min(xp, xc) - 0.2, yt - 0.2, max(xp, xc) + 0.2, yt + 0.2)
    via2(xc, yt)
    vwire(xc, yt, CTL_Y)
    via2(xc, CTL_Y)

# --- cmp: pin (131.8) -> lateral y=-6.0 -> west riser x=123.0 -> outp bar (84.4)
XCMP = LX + 7.20
vwire(XCMP, LY + 0.4, -6.0)
via2(XCMP, -6.0)
rect("m3", 122.8, -6.2, XCMP + 0.2, -5.8)
via2(123.0, -6.0)
vwire(123.0, -6.0, 84.4)
via2(123.2, 84.4)
rect("m2", 122.83, 84.2, 123.4, 84.6)

# --- clk: pin (154.8) -> lateral y=-6.9 -> west riser x=123.9 -> clk bar (97.5)
XCLK = LX + 30.24
vwire(XCLK, LY + 0.4, -6.9)
via2(XCLK, -6.9)
rect("m3", 123.7, -7.1, XCLK + 0.2, -6.7)
via2(123.9, -6.9)
vwire(123.9, -6.9, 97.5)
via2(123.9, 97.5)
top.shapes(L["m2p"]).insert(pya.DBox(123.73, 60.0, 124.07, 60.8))
top.shapes(L["m2l"]).insert(pya.DText("clk", pya.DTrans(pya.DVector(123.9, 60.4))))

# --- sample: pin (143.3) -> lateral y=-7.8 -> west riser x=117.0 -> trk stub
XSMP = LX + 18.72
vwire(XSMP, LY + 0.4, -4.6)
via2(XSMP, -4.6)
rect("m3", 116.8, -4.8, XSMP + 0.2, -4.4)
via2(117.0, -4.6)
vwire(117.0, -11.7, -4.6)
via2(117.0, -11.7)
rect("m3", 116.8, -11.9, SW_X[0] - 0.4, -11.5)

# --- chip-level pin re-exports
for name, xl in (("result[0]", 8.16), ("result[1]", 20.64), ("result[2]", 33.12),
                 ("result[3]", 45.60), ("result[4]", 58.08), ("result[5]", 70.56),
                 ("result[6]", 83.04), ("result[7]", 95.52), ("done", 108.00),
                 ("busy", 120.48)):
    top.shapes(L["m2p"]).insert(pya.DBox(LX + xl - 0.05, LY + 71.7, LX + xl + 0.05, LY + 71.8))
    top.shapes(L["m2l"]).insert(pya.DText(name, pya.DTrans(pya.DVector(LX + xl, LY + 71.75))))
for name, yl in (("rst_n", 18.06), ("start", 54.18)):
    top.shapes(L["m3p"]).insert(pya.DBox(LX, LY + yl - 0.05, LX + 0.1, LY + yl + 0.05))
    top.shapes(L["m3l"]).insert(pya.DText(name, pya.DTrans(pya.DVector(LX + 0.05, LY + yl))))

layout.write("oa_sar8_core2.gds")
b = top.dbbox()
print(f"FINAL core2: {b.width():.0f} x {b.height():.0f} um = {b.width()*b.height()/1e6:.3f} mm2")
