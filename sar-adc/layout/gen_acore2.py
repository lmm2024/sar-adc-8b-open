#!/usr/bin/env python3
"""OA-SAR8 analog core v2 -- textbook symmetric floorplan:
[ main CDAC (X-mirrored, rails inward) | middle: comparator top + switch row
below | replica CDAC (rails inward) ].  TM1 top-plate straps run along the top
edge from the outward spines to central stacks; comparator is R180 so its pins
face the straps. Same verified blocks, same reference netlist (acore.cdl)."""
import pya

layout = pya.Layout()
layout.technology_name = "sg13g2"
layout.dbu = 0.001
top = layout.create_cell("oa_sar8_acore2")

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
                  (126, "tm1")):
    L[name] = layout.layer(num, 0)
for num, tag in ((8, "m1"), (10, "m2"), (30, "m3"), (126, "tm1")):
    L[tag + "p"], L[tag + "l"] = layout.layer(num, 2), layout.layer(num, 25)

lib = pya.Library.library_by_name("SG13_dev", "sg13g2")


def pcell_via(b, t):
    decl = lib.layout().pcell_declaration("via_stack")
    params = {p.name: p.default for p in decl.get_parameters()}
    params.update({"b_layer": b, "t_layer": t, "vn_columns": 2, "vn_rows": 2})
    return layout.create_cell("via_stack", "SG13_dev", params)


VS_M2_TM1 = pcell_via("Metal2", "TopMetal1")
VS_M1_M3 = pcell_via("Metal1", "Metal3")


def rect(lay, x1, y1, x2, y2):
    top.shapes(L[lay]).insert(pya.DBox(x1, y1, x2, y2))


def snap(v):
    return round(round(v * 100) / 100.0, 2)


def via1(x, y):
    x1, y1 = snap(x - 0.095), snap(y - 0.095)
    rect("v1", x1, y1, x1 + 0.19, y1 + 0.19)
    rect("m1", x - 0.2, y - 0.2, x + 0.2, y + 0.2)
    rect("m2", x - 0.2, y - 0.2, x + 0.2, y + 0.2)


def via2(x, y, ph=0.2):
    x1, y1 = snap(x - 0.095), snap(y - 0.095)
    rect("v2", x1, y1, x1 + 0.19, y1 + 0.19)
    rect("m2", x - 0.2, y - ph, x + 0.2, y + ph)
    rect("m3", x - 0.2, y - ph, x + 0.2, y + ph)


def place_vs(cell, x, y):
    bc = cell.dbbox().center()
    top.insert(pya.DCellInstArray(cell.cell_index(),
                                  pya.DTrans(pya.DVector(x - bc.x, y - bc.y))))
    rect("tm1", x - 1.2, y - 1.2, x + 1.2, y + 1.2)


def vwire(x, y1, y2, hw=0.2):
    rect("m2", x - hw, min(y1, y2), x + hw, max(y1, y2))


# ================= placement =================
top.insert(pya.DCellInstArray(cd.cell_index(), pya.DTrans(2, True, pya.DVector(96.2, 0))))
top.insert(pya.DCellInstArray(cd.cell_index(), pya.DTrans(pya.DVector(282.0, 0))))
CMPX, CMPY = 189.2, 101.6
top.insert(pya.DCellInstArray(cp.cell_index(), pya.DTrans(2, False, pya.DVector(CMPX, CMPY))))
SW_P = 13.8
SWY = -18.0
SW_X = [122.0 + i * SW_P for i in range(11)]
for i in range(9):
    top.insert(pya.DCellInstArray(sw.cell_index(), pya.DTrans(pya.DVector(SW_X[i], SWY))))
top.insert(pya.DCellInstArray(sw.cell_index(), pya.DTrans(pya.DVector(SW_X[9], SWY))))
top.insert(pya.DCellInstArray(tg.cell_index(), pya.DTrans(pya.DVector(SW_X[10], SWY))))

NETS = ["b7", "b6", "b5", "b4", "b3", "b2", "b1", "b0", "term"]
RAIL_A = {n: 118.2 - i * 2.2 for i, n in enumerate(NETS)}     # main, inward
RAIL_B = {n: 260.0 + i * 2.2 for i, n in enumerate(NETS)}     # replica, inward
BOT_Y = SWY + 5.5
VIN_Y = SWY + 4.7
CTL_Y = SWY + 3.9
TRKB_Y = SWY + 3.1
TRK_Y = SWY + 6.3

# ---- inter-cell bridges (vin isolated at gaps 8-9, 9-10)
for i in range(10):
    xg1, xg2 = SW_X[i] + 12.2, SW_X[i + 1] - 1.0
    ys = [TRK_Y, TRKB_Y]
    if i not in (8, 9):
        ys.append(VIN_Y)
    for y in ys:
        rect("m3", xg1 - 0.1, y - 0.2, xg2 + 0.1, y + 0.2)
    rect("m1", SW_X[i] + 12.4, SWY - 2.2, SW_X[i + 1] - 1.1, SWY - 1.6)
    rect("m1", SW_X[i] + 12.4, SWY + 12.4, SW_X[i + 1] - 1.1, SWY + 13.0)

# ---- bit fan: below-rail ladder, corridor risers
FAN_Y = {n: -24.4 - i * 1.3 for i, n in enumerate(NETS)}
for i, n in enumerate(NETS):
    xr = RAIL_A[n]
    xb = SW_X[i] + 0.2
    via2(xb, BOT_Y)
    vwire(xb, BOT_Y, FAN_Y[n] + 0.2)
    via2(xb, FAN_Y[n])
    rect("m3", min(xb, xr) - 0.2, FAN_Y[n] - 0.2, max(xb, xr) + 0.2, FAN_Y[n] + 0.2)
    via2(xr, FAN_Y[n])
    vwire(xr, FAN_Y[n], -2.6)
    via2(xr, -2.75)

# ---- ctl pins (west stub per cell) + term hardwire to VDD rail
for i in range(8):
    top.shapes(L["m3p"]).insert(pya.DBox(SW_X[i] - 1.0, CTL_Y - 0.2,
                                         SW_X[i] - 0.4, CTL_Y + 0.2))
    top.shapes(L["m3l"]).insert(pya.DText(f"ctl{7-i}", pya.DTrans(
        pya.DVector(SW_X[i] - 0.7, CTL_Y))))
xt = SW_X[8] - 0.7
vwire(xt, CTL_Y, SWY + 12.7)
via2(xt, CTL_Y)
place = pya.DCellInstArray(VS_M1_M3.cell_index(),
                           pya.DTrans(pya.DVector(xt - VS_M1_M3.dbbox().center().x,
                                                  SWY + 12.7 - VS_M1_M3.dbbox().center().y)))
top.insert(place)
rect("m1", xt - 0.5, SWY + 12.4, xt + 0.5, SWY + 13.0)
rect("m3", xt - 0.5, SWY + 12.5, xt + 0.5, SWY + 12.9)

# ---- phase inverter (cell 9): ctl=trk, bot->trkb, vin->VSS
x9 = SW_X[9]
vwire(x9 - 0.7, CTL_Y, TRK_Y)
via2(x9 - 0.7, CTL_Y)
via2(x9 - 0.7, TRK_Y)
xb9 = x9 + 0.2
via2(xb9, BOT_Y)
vwire(xb9, TRKB_Y, BOT_Y)
via2(xb9, TRKB_Y)
xv9 = x9 + 5.0
via2(xv9, VIN_Y)
vwire(xv9, VIN_Y, SWY - 1.9)
via1(xv9, SWY - 1.9)

# ---- top-plate TM1 straps: outward spines -> central stacks -> R180 cmp pins
INN_X, INP_X = CMPX - 7.4, CMPX + 7.4          # inn=main(west), inp=replica(east)
PIN_TOP = CMPY - 5.0                            # cmp pins now upper zone (R180)
rect("tm1", -1.0, 104.9, INN_X + 1.2, 106.9)   # main strap (west band)
rect("tm1", 0.0, 100.5, 2.0, 106.9)            # bond main spine to the band
place_vs(VS_M2_TM1, INN_X, 105.9)
vwire(INN_X, PIN_TOP - 0.6, 105.9)
rect("tm1", INP_X - 1.2, 104.9, 379.0, 106.9)  # replica strap (east band)
rect("tm1", 376.2, 100.5, 378.2, 106.9)        # bond replica spine to the band
place_vs(VS_M2_TM1, INP_X, 105.9)
vwire(INP_X, PIN_TOP - 0.6, 105.9)

# ---- top TG (cell 10): bot -> main topm via west stack; vin -> VCM
xbt = SW_X[10] + 0.2
via2(xbt, BOT_Y)
vwire(xbt, BOT_Y, -8.0)
via2(xbt, -8.0)
rect("m3", -4.2, -8.2, xbt + 0.2, -7.8)
via2(-4.0, -8.0)
vwire(-4.0, -8.0, 105.9)
place_vs(VS_M2_TM1, -4.0, 105.9)
rect("tm1", -5.2, 104.9, 1.0, 106.9)

# ---- VCM: replica rail tie band (M3-M3 direct) + link to cell10 vin + pin
rect("m3", 258.0, -2.7, 279.5, -2.3)
vwire(278.5, -2.5, VIN_Y)
via2(278.5, -2.5)
via2(278.5, VIN_Y)
rect("m3", SW_X[10] + 12.2, VIN_Y - 0.2, 278.7, VIN_Y + 0.2)
top.shapes(L["m3p"]).insert(pya.DBox(279.0, -2.7, 279.5, -2.3))
top.shapes(L["m3l"]).insert(pya.DText("vcm", pya.DTrans(pya.DVector(279.2, -2.5))))

# ---- vin + trk pins (west end of the row)
for name, y in (("vin", VIN_Y), ("trk", TRK_Y)):
    top.shapes(L["m3p"]).insert(pya.DBox(SW_X[0] - 1.0, y - 0.2, SW_X[0] - 0.4, y + 0.2))
    top.shapes(L["m3l"]).insert(pya.DText(name, pya.DTrans(pya.DVector(SW_X[0] - 0.7, y))))

# ---- comparator pins: clk (M3 bar now at CMPY-4.1), outn/outp east/west bars
CLKY = CMPY - 4.1
rect("m3", 123.0, CLKY - 0.2, 163.5, CLKY + 0.2)
top.shapes(L["m3p"]).insert(pya.DBox(123.0, CLKY - 0.2, 124.0, CLKY + 0.2))
top.shapes(L["m3l"]).insert(pya.DText("clk_cmp", pya.DTrans(pya.DVector(123.5, CLKY))))
OUTN_Y = CMPY - 16.4                            # R180: outn bar flips to east
rect("m3", CMPX + 11.0, OUTN_Y - 0.2, 256.0, OUTN_Y + 0.2)
top.shapes(L["m3p"]).insert(pya.DBox(255.0, OUTN_Y - 0.2, 256.0, OUTN_Y + 0.2))
top.shapes(L["m3l"]).insert(pya.DText("outn", pya.DTrans(pya.DVector(255.5, OUTN_Y))))
OUTP_Y = CMPY - 17.2                            # outp bar to the west
rect("m3", 123.0, OUTP_Y - 0.2, CMPX - 11.0, OUTP_Y + 0.2)
top.shapes(L["m3p"]).insert(pya.DBox(123.0, OUTP_Y - 0.2, 124.0, OUTP_Y + 0.2))
top.shapes(L["m3l"]).insert(pya.DText("outp", pya.DTrans(pya.DVector(123.5, OUTP_Y))))

# ---- power: comparator rails (R180: VDD low, VSS high) -> west drops -> row rails
CMP_VSS_Y = CMPY + 2.1
CMP_VDD_Y = CMPY - 25.5
rect("m1", 120.6, CMP_VSS_Y - 0.3, CMPX - 29.5 + 0.5, CMP_VSS_Y + 0.3)
rect("m1", 119.5, CMP_VDD_Y - 0.3, CMPX - 29.5 + 0.5, CMP_VDD_Y + 0.3)
vwire(121.0, CMP_VSS_Y, SWY - 1.9)
via1(121.0, CMP_VSS_Y)
via1(121.0, SWY - 1.9)
rect("m1", 120.4, SWY - 2.2, SW_X[0] - 1.0, SWY - 1.6)
vwire(119.9, CMP_VDD_Y, SWY + 12.7)
via1(119.9, CMP_VDD_Y)
via1(119.9, SWY + 12.7)
rect("m1", 119.4, SWY + 12.4, SW_X[0] - 1.0, SWY + 13.0)

# ---- VDD/VSS core pins (west ends of row rails)
top.shapes(L["m1p"]).insert(pya.DBox(SW_X[0] - 1.2, SWY - 2.1, SW_X[0] - 0.4, SWY - 1.7))
top.shapes(L["m1l"]).insert(pya.DText("VSS", pya.DTrans(pya.DVector(SW_X[0] - 0.8, SWY - 1.9))))
top.shapes(L["m1p"]).insert(pya.DBox(SW_X[0] - 1.2, SWY + 12.5, SW_X[0] - 0.4, SWY + 12.9))
top.shapes(L["m1l"]).insert(pya.DText("VDD", pya.DTrans(pya.DVector(SW_X[0] - 0.8, SWY + 12.7))))

layout.write("oa_sar8_acore2.gds")
b = top.dbbox()
print(f"acore2: {b.width():.0f} x {b.height():.0f} um = {b.width()*b.height()/1e6:.3f} mm2")
