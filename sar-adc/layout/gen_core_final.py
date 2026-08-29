#!/usr/bin/env python3
"""OA-SAR8 FINAL core: verified analog core + SAR logic macro + digital fan.
Digital fan: M2 verticals / M3 horizontals in the gap band between logic (top
edge y=-50) and switch row (bottom y=-29.2); detour bands under the macro for
bottom-edge pins. Chip-level pins (clk, rst_n, start, result...) re-exported."""
import pya

layout = pya.Layout()
layout.technology_name = "sg13g2"
layout.dbu = 0.001
top = layout.create_cell("oa_sar8_core_final")

layout.read("oa_sar8_acore.gds")
layout.read("/foss/designs/sar-adc/logic/final/gds/sar_ctrl.gds")
ac = layout.cell("oa_sar8_acore")
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
LX, LY = -28.5, -160.0
top.insert(pya.DCellInstArray(lg.cell_index(), pya.DTrans(pya.DVector(LX, LY))))

SW_P = 13.8
SW_X = [-21.6 + i * SW_P for i in range(11)]
CTL_Y = -23.1                                     # acore ctl stub center y

# logic pin coords (from extracted labels, logic-local)
RIGHT = {"dac_code[0]": 61.74, "dac_code[1]": 56.70, "dac_code[2]": 42.42,
         "dac_code[4]": 60.90, "dac_code[6]": 43.26, "clk": 36.54}
TOPP = {"dac_code[3]": 75.36, "dac_code[7]": 50.40}
BOT = {"dac_code[5]": 67.68, "cmp": 66.72}
LEFT = {"sample": 64.26}

# fan tracks (M3) in the gap band
TRACK = {"dac_code[7]": -47.0, "dac_code[6]": -45.7, "dac_code[5]": -44.4,
         "dac_code[4]": -43.1, "dac_code[3]": -41.8, "dac_code[2]": -40.5,
         "dac_code[1]": -39.2, "dac_code[0]": -37.9, "clk": -36.6,
         "cmp": -35.3, "sample": -33.9}

# --- right-edge pins -> east risers -> tracks
xr0 = LX + 129.8                                   # 101.3
riser_x = {}
for k, name in enumerate(sorted(RIGHT)):
    riser_x[name] = 102.2 + k * 0.7
for name, yl in RIGHT.items():
    yp = LY + yl
    xr_ = riser_x[name]
    rect("m3", xr0 - 0.1, yp - 0.2, xr_ + 0.2, yp + 0.2)   # east stub off the pin
    via2(xr_, yp)
    vwire(xr_, yp, TRACK[name])
    via2(xr_, TRACK[name])

# --- top-edge pins (M2): straight risers
for name, xl in TOPP.items():
    xp = LX + xl
    vwire(xp, LY + 109.8, TRACK[name])
    via2(xp, TRACK[name])

# --- bottom-edge pins: detour bands under the macro, east flank risers
for k, (name, xl) in enumerate(sorted(BOT.items())):
    xp = LX + xl
    yband = -162.4 - k * 1.3
    xflank = 106.4 + k * 0.7
    vwire(xp, LY + 0.6, yband)                     # M2 stub reaching into the pin
    via2(xp, yband)
    rect("m3", xp - 0.2, yband - 0.2, xflank + 0.2, yband + 0.2)
    via2(xflank, yband)
    vwire(xflank, yband, TRACK[name])
    via2(xflank, TRACK[name])

# --- left-edge pin (sample): west riser -> track
yp = LY + LEFT["sample"]
rect("m3", LX - 1.4, yp - 0.2, LX + 0.1, yp + 0.2)
via2(LX - 1.2, yp)
vwire(LX - 1.2, yp, TRACK["sample"])
via2(LX - 1.2, TRACK["sample"])

# --- tracks themselves + drops to acore ctl stubs
for i in range(8):
    name = f"dac_code[{7 - i}]"
    xc_ = SW_X[i] - 0.7
    src_x = {**{n: riser_x[n] for n in RIGHT}, **{n: LX + x for n, x in TOPP.items()},
             "dac_code[5]": 106.4, "cmp": 107.1}.get(name)
    rect("m3", min(xc_, src_x) - 0.2, TRACK[name] - 0.2,
         max(xc_, src_x) + 0.2, TRACK[name] + 0.2)
    via2(xc_, TRACK[name])
    vwire(xc_, TRACK[name], CTL_Y)
    via2(xc_, CTL_Y)

# --- sample -> trk stub (acore west)
rect("m3", -29.5, TRACK["sample"] - 0.2, -22.1, TRACK["sample"] + 0.2)
via2(-22.3, TRACK["sample"])
vwire(-22.3, TRACK["sample"], -20.7)
via2(-22.3, -20.7)
rect("m3", LX - 1.4, TRACK["sample"] - 0.2, LX - 1.0, TRACK["sample"] + 0.2)

# --- cmp: comparator outp east pin down to its track, then to logic cmp riser
rect("m3", 47.5, 127.4, 101.0, 127.8)              # ensure outp bar reach (drawn in acore)
via2(100.8, 127.6)
vwire(100.8, 127.6, -35.1)
via2(100.8, TRACK["cmp"])
rect("m3", 100.6, TRACK["cmp"] - 0.2, 107.3, TRACK["cmp"] + 0.2)

# --- clk: logic clk riser joins comparator clk_cmp via west route
rect("m3", -28.9, TRACK["clk"] - 0.2, riser_x["clk"] + 0.2, TRACK["clk"] + 0.2)
via2(-28.7, TRACK["clk"])
vwire(-28.7, TRACK["clk"], 114.5)
via2(-28.7, 114.5)
rect("m3", -28.9, 114.3, 7.8, 114.7)               # joins acore clk_cmp bar

# --- chip-level pin re-exports (labels at logic pin sites)
for name, yl in (("done", 72.66), ("result[0]", 70.14), ("result[1]", 58.38),
                 ("result[2]", 41.58), ("result[4]", 73.50), ("result[6]", 40.74)):
    top.shapes(L["m3p"]).insert(pya.DBox(xr0 - 0.1, LY + yl - 0.05, xr0, LY + yl + 0.05))
    top.shapes(L["m3l"]).insert(pya.DText(name, pya.DTrans(pya.DVector(xr0 - 0.2, LY + yl))))
for name, yl in (("busy", 65.10), ("rst_n", 74.34), ("start", 61.74)):
    top.shapes(L["m3p"]).insert(pya.DBox(LX, LY + yl - 0.05, LX + 0.1, LY + yl + 0.05))
    top.shapes(L["m3l"]).insert(pya.DText(name, pya.DTrans(pya.DVector(LX + 0.2, LY + yl))))
for name, xl in (("result[3]", 76.32), ("result[7]", 53.28)):
    top.shapes(L["m2p"]).insert(pya.DBox(LX + xl - 0.05, LY + 109.7, LX + xl + 0.05, LY + 109.8))
    top.shapes(L["m2l"]).insert(pya.DText(name, pya.DTrans(pya.DVector(LX + xl, LY + 109.6))))
top.shapes(L["m3l"]).insert(pya.DText("clk", pya.DTrans(pya.DVector(riser_x["clk"], TRACK["clk"]))))

layout.write("oa_sar8_core_final.gds")
b = top.dbbox()
print(f"FINAL core: {b.width():.0f} x {b.height():.0f} um = {b.width()*b.height()/1e6:.3f} mm2")
