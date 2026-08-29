#!/usr/bin/env python3
"""OA-SAR8 analog core: both CDACs + comparator + switch row + top TG + phase
inverter, FULLY INTERCONNECTED. Layer discipline: M2 vertical / M3 horizontal.
Pins: vin, vcm, clk_cmp, trk, ctl0..7 (term driver hardwired to VDD), outp,
outn, VDD, VSS."""
import pya

layout = pya.Layout()
layout.technology_name = "sg13g2"
layout.dbu = 0.001
top = layout.create_cell("oa_sar8_acore")

layout.read("cdac_array.gds")
layout.read("cmp/sa_comp.gds")
layout.read("sw/sw_bitcell.gds")
layout.read("sw/sw_tg.gds")
cd = layout.cell("cdac_array")
cp = layout.cell("sa_comp")
sw = layout.cell("sw_bitcell")
tg = layout.cell("sw_tg")

L = {}
for num, name in ((8, "m1"), (19, "v1"), (10, "m2"), (29, "v2"), (30, "m3"),
                  (67, "m5"), (126, "tm1"), (125, "tv1")):
    L[name] = layout.layer(num, 0)
for num, tag in ((8, "m1"), (10, "m2"), (30, "m3"), (126, "tm1")):
    L[tag + "p"], L[tag + "l"] = layout.layer(num, 2), layout.layer(num, 25)

lib = pya.Library.library_by_name("SG13_dev", "sg13g2")


def pcell_via(b, t, cols=2, rows=2):
    decl = lib.layout().pcell_declaration("via_stack")
    params = {p.name: p.default for p in decl.get_parameters()}
    params.update({"b_layer": b, "t_layer": t, "vn_columns": cols, "vn_rows": rows})
    return layout.create_cell("via_stack", "SG13_dev", params)


VS_M2_TM1 = pcell_via("Metal2", "TopMetal1")
VS_M1_M3 = pcell_via("Metal1", "Metal3")


def rect(lay, x1, y1, x2, y2):
    top.shapes(L[lay]).insert(pya.DBox(x1, y1, x2, y2))


def snap(v):
    return round(round(v * 100) / 100.0, 2)


def via2(x, y, ph=0.2, pw=0.2):
    x1, y1 = snap(x - 0.095), snap(y - 0.095)
    rect("v2", x1, y1, x1 + 0.19, y1 + 0.19)
    rect("m2", x - pw, y - ph, x + pw, y + ph)
    rect("m3", x - pw, y - ph, x + pw, y + ph)


def place(cell, x, y, mirror=False):
    tr = pya.DTrans(0, True, pya.DVector(x, y)) if mirror else \
         pya.DTrans(pya.DVector(x, y))
    top.insert(pya.DCellInstArray(cell.cell_index(), tr))


def place_vs(cell, x, y, pads=None, pad=1.0):
    bc = cell.dbbox().center()
    top.insert(pya.DCellInstArray(cell.cell_index(),
                                  pya.DTrans(pya.DVector(x - bc.x, y - bc.y))))
    for lay in (pads or []):
        rect(lay, x - pad, y - pad, x + pad, y + pad)


def vwire(x, y1, y2, hw=0.2):
    rect("m2", x - hw, min(y1, y2), x + hw, max(y1, y2))


# ================= placement =================
SW_P = 13.8
place(cd, 0, 0)                       # main CDAC: rails x -22..-4.4 @2.2, y -3..103.2
place(cp, 36.5, 110.4)                # comparator
place(cd, 0, 244.2, mirror=True)      # replica: rails bottom at y 141..143
for i in range(9):                    # switch row (bits b7..b0 + term)
    place(sw, -21.6 + i * SW_P, -27.0)
place(sw, -21.6 + 9 * SW_P, -27.0)    # 10th: phase inverter (ctl=trk_in -> bot=trkb)
place(tg, -21.6 + 10 * SW_P, -27.0)   # top-plate track TG

RAIL_X = {n: -22.0 + i * 2.2 for i, n in
          enumerate(["b7", "b6", "b5", "b4", "b3", "b2", "b1", "b0", "term"])}
SW_X = [-21.6 + i * SW_P for i in range(11)]
SW_BOT_Y = -27.0 + 5.5                # bot bus center y (abs)
SW_VIN_Y = -27.0 + 4.7
SW_CTL_Y = -27.0 + 3.9
SW_TRKB_Y = -27.0 + 3.1
SW_TRK_Y = -27.0 + 6.3

# ---- inter-cell bridges on the abutment gaps (vin, trk, trkb, VDD, VSS)
for i in range(10):
    xg1 = SW_X[i] + 12.2              # bus end of cell i
    xg2 = SW_X[i + 1] - 1.0           # bus start of cell i+1
    ys = [SW_TRK_Y, SW_TRKB_Y]
    if i not in (8, 9):
        ys.append(SW_VIN_Y)           # isolate cell9 vin (phase inverter)
    for y in ys:
        rect("m3", xg1 - 0.1, y - 0.2, xg2 + 0.1, y + 0.2)
    rect("m1", SW_X[i] + 12.4, -29.2, SW_X[i + 1] - 1.2 + 0.1, -28.6)
    rect("m1", SW_X[i] + 12.4, -14.6, SW_X[i + 1] - 1.2 + 0.1, -14.0)

# ---- bit fan: sw bot (cells 0..8) -> M3 tracks -> rail bottoms
FAN_Y = {n: -14.6 + i * 1.3 for i, n in
         enumerate(["b7", "b6", "b5", "b4", "b3", "b2", "b1", "b0", "term"])}
for i, n in enumerate(["b7", "b6", "b5", "b4", "b3", "b2", "b1", "b0", "term"]):
    xr = RAIL_X[n]
    if i == 0:                        # rail sits inside cell0 bus span: direct
        via2(xr, SW_BOT_Y)
        vwire(xr, SW_BOT_Y, -2.6)
        via2(xr, -2.75)
        continue
    xb = SW_X[i] + 0.2                # riser x: clear corridor at cell left edge
    via2(xb, SW_BOT_Y)
    vwire(xb, SW_BOT_Y, FAN_Y[n] + 0.2)
    via2(xb, FAN_Y[n])
    rect("m3", min(xb, xr) - 0.2, FAN_Y[n] - 0.2, max(xb, xr) + 0.2, FAN_Y[n] + 0.2)
    via2(xr, FAN_Y[n])
    vwire(xr, FAN_Y[n], -2.6)
    via2(xr, -2.75)

# ---- ctl pins for cells 0..7 (term cell ctl -> VDD hardwire)
for i in range(8):
    xc_ = SW_X[i] - 0.7
    top.shapes(L["m3p"]).insert(pya.DBox(SW_X[i] - 1.0, SW_CTL_Y - 0.2,
                                         SW_X[i] - 0.4, SW_CTL_Y + 0.2))
    top.shapes(L["m3l"]).insert(pya.DText(f"ctl{7-i}", pya.DTrans(
        pya.DVector(xc_, SW_CTL_Y))))
# term ctl -> VDD rail (drive output LOW=GND permanently)
xt = SW_X[8] - 0.7
vwire(xt, SW_CTL_Y, -14.3)
via2(xt, SW_CTL_Y)
place_vs(VS_M1_M3, xt, -14.3, pads=["m1", "m3"], pad=0.5)

# ---- phase inverter (cell 9): ctl9 = trk input; its bot = trkb
x9 = SW_X[9]
# feed trk bus into ctl9: jog at the cell's left edge
vwire(x9 - 0.7, SW_CTL_Y, SW_TRK_Y)
via2(x9 - 0.7, SW_CTL_Y)
via2(x9 - 0.7, SW_TRK_Y)
# tie the isolated cell9 vin segment to VSS (its TG then passes 0 harmlessly)
xv9 = x9 + 5.0
via2(xv9, SW_VIN_Y)
vwire(xv9, SW_VIN_Y, -28.9)
x1, y1 = snap(xv9 - 0.095), snap(-28.9 - 0.095)
rect("v1", x1, y1, x1 + 0.19, y1 + 0.19)
rect("m1", xv9 - 0.2, -29.1, xv9 + 0.2, -28.7)
rect("m2", xv9 - 0.2, -29.1, xv9 + 0.2, -28.7)
# its bot bus (= !trk) -> trkb bus: local riser
xb9 = x9 + 0.2
via2(xb9, SW_BOT_Y)
vwire(xb9, SW_TRKB_Y, SW_BOT_Y)
via2(xb9, SW_TRKB_Y)
# inverter cell's own vin/trk/trkb stubs are bridged already; disable its TG:
# its trk segment between cell9 and cell10 carries real trk (fine: TG input vin
# bus is the shared vin -> its TG just tracks vin onto its bot=trkb during trk.
# To keep trkb clean, cut its TG by NOT bridging vin into cell9?  vin bridge for
# gap 8->9 must remain for... simpler: cell9 TG ON during track drives bot=vin;
# that fights the inverter. FIX: isolate cell9 vin: skip vin bridge at gap 8->9
# and 9->10 (done below by overdrawing? cannot un-draw) -> handled: bridges for
# vin were drawn for all gaps above; instead we re-route cell10 vin from the
# main vin pin side. To truly isolate, we redraw gap bridges selectively:
# (implemented: vin bridges skipped at 8->9, 9->10 by erasing is impossible ->
#  we drew them; accepted v1 quirk documented in report)

# ---- top-plate links: main topp -> TG -> comparator inn; replica topp -> inp
SPINE_X = 95.2                        # CDAC TM1 spine center (real: 94.2..96.2)
CMP_INN_X = 36.5 + 7.4               # comparator inn pin x (mirrored input)
CMP_INP_X = 36.5 - 7.4
CMP_PIN_Y = 110.4 + 5.3
# main: TM1 strap from spine top to a stack above the comparator inn x
rect("tm1", CMP_INN_X - 1.0, 102.0, SPINE_X + 1.0, 104.0)
place_vs(VS_M2_TM1, CMP_INN_X, 103.0, pads=["tm1"], pad=1.2)
vwire(CMP_INN_X, 103.0, CMP_PIN_Y + 0.3)
# replica: TM1 strap from its spine bottom (y ~141) to stack above inp
rect("tm1", CMP_INP_X - 1.0, 139.4, SPINE_X + 1.0, 141.4)
place_vs(VS_M2_TM1, CMP_INP_X, 140.4, pads=["tm1"], pad=1.2)
vwire(CMP_INP_X, 137.0, 140.4)
via2(CMP_INP_X, 136.8)
rect("m3", 2.8, 136.6, CMP_INP_X + 0.2, 137.0)     # west along the roof
via2(3.0, 136.8)
vwire(3.0, 115.6, 136.8)
via2(3.0, 115.6)
rect("m3", 2.8, 115.4, CMP_INP_X + 0.2, 115.8)     # east under the cell edge
via2(CMP_INP_X, 115.6)
rect("m2", CMP_INP_X - 0.17, 115.4, CMP_INP_X + 0.17, 116.0)

# ---- top TG (cell 10): bot -> main topp (via TM1 stack), vin -> VCM net
x10 = SW_X[10]
xbt = x10 + 0.2
via2(xbt, SW_BOT_Y)
vwire(xbt, SW_BOT_Y, -8.0)
via2(xbt, -8.0)
rect("m3", xbt - 0.2, -8.2, 121.0, -7.8)      # M3 east to below the spine col
via2(120.8, -8.0)
vwire(120.8, -8.0, 102.8)
place_vs(VS_M2_TM1, 120.8, 103.0, pads=["tm1"], pad=1.2)
rect("tm1", SPINE_X - 1.0, 102.0, 122.0, 104.0)   # joins main topp strap

# ---- VCM: replica bots band + top TG vin + core pin
VCM_Y = 143.0
rect("m3", -27.0, VCM_Y - 0.3, -3.0, VCM_Y + 0.3)
for n, xr in RAIL_X.items():
    via2(xr, VCM_Y)                    # replica rails (M3) touch band? same layer:
# NOTE replica rails ARE M3 verticals ending y ~141.0..246 - band overlaps them
# at 143 -> same-layer touch = connected (all shorted to VCM by design).
top.shapes(L["m3p"]).insert(pya.DBox(-27.0, VCM_Y - 0.3, -26.2, VCM_Y + 0.3))
top.shapes(L["m3l"]).insert(pya.DText("vcm", pya.DTrans(pya.DVector(-26.6, VCM_Y))))
# route VCM down the left edge to the top-TG vin: M2 west spine
vwire(-26.0, VCM_Y, -26.8, hw=0.3)
via2(-26.0, VCM_Y)
# connect to cell10 vin: M3 band at SW_VIN_Y-3.0 from -26 to cell10 vin riser
rect("m3", -26.3, -26.8, x10 + 5.7, -26.4)
via2(-26.0, -26.6)
vwire(x10 + 5.5, -26.6, SW_VIN_Y)
via2(x10 + 5.5, -26.6)
via2(x10 + 5.5, SW_VIN_Y)

# ---- vin core pin (west end of switch-row vin bus)
top.shapes(L["m3p"]).insert(pya.DBox(SW_X[0] - 1.0, SW_VIN_Y - 0.2,
                                     SW_X[0] - 0.4, SW_VIN_Y + 0.2))
top.shapes(L["m3l"]).insert(pya.DText("vin", pya.DTrans(
    pya.DVector(SW_X[0] - 0.7, SW_VIN_Y))))
# trk core pin (west end)
top.shapes(L["m3p"]).insert(pya.DBox(SW_X[0] - 1.0, SW_TRK_Y - 0.2,
                                     SW_X[0] - 0.4, SW_TRK_Y + 0.2))
top.shapes(L["m3l"]).insert(pya.DText("trk", pya.DTrans(
    pya.DVector(SW_X[0] - 0.7, SW_TRK_Y))))

# ---- comparator hookups: clk pin (M3 west), outputs -> east pins
top.shapes(L["m3p"]).insert(pya.DBox(6.8, 114.3, 7.8, 114.7))
top.shapes(L["m3l"]).insert(pya.DText("clk_cmp", pya.DTrans(pya.DVector(7.3, 114.5))))
# comparator clk pin at its west edge (36.5-30+0.3.. y 110.4+3.9): extend M3
rect("m3", 6.8, 114.3, 36.5 - 29.5, 114.7)
# outn/outp pins: extend their M3 bars to east pins
rect("m3", 36.5 + 11.0, 127.4, 101.0, 127.8)      # outp bar y=110.4+17.0
top.shapes(L["m3p"]).insert(pya.DBox(100.0, 127.4, 101.0, 127.8))
top.shapes(L["m3l"]).insert(pya.DText("outp", pya.DTrans(pya.DVector(100.5, 127.6))))
rect("m3", 36.5 - 12.0, 126.6, -26.0, 127.0)      # outn bar y=110.4+16.2 west
top.shapes(L["m3p"]).insert(pya.DBox(-26.0, 126.6, -25.0, 127.0))
top.shapes(L["m3l"]).insert(pya.DText("outn", pya.DTrans(pya.DVector(-25.5, 126.8))))

# ---- power: TM1 spines west(VSS)/east... keep simple: M1 rails already in
# blocks; declare rail pin stubs as core pins (VDD/VSS) at switch row ends
top.shapes(L["m1p"]).insert(pya.DBox(SW_X[0] - 1.2, -29.2, SW_X[0] - 0.4, -28.6))
top.shapes(L["m1l"]).insert(pya.DText("VSS", pya.DTrans(pya.DVector(SW_X[0] - 0.8, -28.9))))
top.shapes(L["m1p"]).insert(pya.DBox(SW_X[0] - 1.2, -14.6, SW_X[0] - 0.4, -14.0))
top.shapes(L["m1l"]).insert(pya.DText("VDD", pya.DTrans(pya.DVector(SW_X[0] - 0.8, -14.3))))
# ---- comparator power hookup: extend rails west (M1), drop M2 on west flank
CMP_VSS_Y = 110.4 - 2.1               # rail centers
CMP_VDD_Y = 110.4 + 25.5
rect("m1", -23.4, CMP_VSS_Y - 0.3, 7.0, CMP_VSS_Y + 0.3)
rect("m1", -24.4, CMP_VDD_Y - 0.3, 7.0, CMP_VDD_Y + 0.3)
# VSS drop at x=-22.5 down to switch-row VSS rail
vwire(-23.0, CMP_VSS_Y, -28.9)
x1, y1 = snap(-23.0 - 0.095), snap(CMP_VSS_Y - 0.095)
rect("v1", x1, y1, x1 + 0.19, y1 + 0.19)
x1, y1 = snap(-23.0 - 0.095), snap(-28.9 - 0.095)
rect("v1", x1, y1, x1 + 0.19, y1 + 0.19)
rect("m1", -23.2, -29.1, -22.8, -28.7)
rect("m2", -23.3, CMP_VSS_Y - 0.3, -22.8, CMP_VSS_Y + 0.3)
# VDD drop at x=-23.6, rail extended west to meet it
rect("m1", -24.4, -14.6, -22.8, -14.0)
vwire(-24.2, CMP_VDD_Y, -14.3)
x1, y1 = snap(-24.2 - 0.095), snap(CMP_VDD_Y - 0.095)
rect("v1", x1, y1, x1 + 0.19, y1 + 0.19)
x1, y1 = snap(-24.2 - 0.095), snap(-14.3 - 0.095)
rect("v1", x1, y1, x1 + 0.19, y1 + 0.19)
rect("m1", -24.4, -14.5, -24.0, -14.1)
rect("m2", -24.6, CMP_VDD_Y - 0.3, -24.0, CMP_VDD_Y + 0.3)

layout.write("oa_sar8_acore.gds")
b = top.dbbox()
print(f"acore bbox: {b.width():.0f} x {b.height():.0f} um")
