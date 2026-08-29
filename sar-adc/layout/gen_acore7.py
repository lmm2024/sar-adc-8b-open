#!/usr/bin/env python3
"""OA-SAR8 analog core v3 -- reference-die narrow-seam floorplan:
[ main CDAC (rails inward) |58um seam| replica CDAC (rails inward) ]
Switch row split under the arrays: segment A (term,b0..b5) under main body,
segment B (b6,b7,phase-inv,TG) under replica body -- keeps the riser corridor
(x 100.4..120) and the seam clear for the 50x100 logic strip (added in core3).
Comparator R180 rides the seam top at y~101..129; TM1 straps unchanged concept.
Same blocks, same netlist topology as acore2 (acore3.cdl = renamed acore2.cdl).
"""
import pya

layout = pya.Layout()
layout.technology_name = "sg13g2"
layout.dbu = 0.001
top = layout.create_cell("oa_sar8_acore7")

layout.read("cdac_array.gds")
layout.read("cmp/sa_comp.gds")
layout.read("sw/sw_bitcell.gds")
layout.read("sw/sw_bitcell10.gds")
layout.read("sw/sw_tg.gds")
layout.read("bs/bstrap.gds")
cd = layout.cell("cdac_array")
cp = layout.cell("sa_comp")
sw = layout.cell("sw_bitcell")
sw10 = layout.cell("sw_bitcell10")
tg = layout.cell("sw_tg")
bst = layout.cell("bstrap")

L = {}
for num, name in ((8, "m1"), (19, "v1"), (10, "m2"), (29, "v2"), (30, "m3"),
                  (49, "v3"), (50, "m4"), (66, "v4"), (67, "m5"), (126, "tm1")):
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


def via3(x, y):
    x1, y1 = snap(x - 0.095), snap(y - 0.095)
    rect("v3", x1, y1, x1 + 0.19, y1 + 0.19)
    rect("m3", x - 0.2, y - 0.2, x + 0.2, y + 0.2)
    rect("m4", x - 0.2, y - 0.2, x + 0.2, y + 0.2)


def v4wire(x, y1, y2):
    rect("m4", x - 0.2, min(y1, y2), x + 0.2, max(y1, y2))


def via34(x, y):
    """M3 -> M5 stack (via3 + via4) with 0.4 pads."""
    via3(x, y)
    x1, y1 = snap(x - 0.095), snap(y - 0.095)
    rect("v4", x1, y1, x1 + 0.19, y1 + 0.19)
    rect("m5", x - 0.2, y - 0.2, x + 0.2, y + 0.2)


def v5wire(x, y1, y2):
    rect("m5", x - 0.2, min(y1, y2), x + 0.2, max(y1, y2))


def place_vs(cell, x, y):
    bc = cell.dbbox().center()
    top.insert(pya.DCellInstArray(cell.cell_index(),
                                  pya.DTrans(pya.DVector(x - bc.x, y - bc.y))))
    rect("tm1", x - 1.2, y - 1.2, x + 1.2, y + 1.2)


def vwire(x, y1, y2, hw=0.2):
    rect("m2", x - hw, min(y1, y2), x + hw, max(y1, y2))


# ================= placement =================
top.insert(pya.DCellInstArray(cd.cell_index(), pya.DTrans(2, True, pya.DVector(96.2, 0))))
top.insert(pya.DCellInstArray(cd.cell_index(), pya.DTrans(pya.DVector(198.0, 0))))
CMPX, CMPY = 147.1, 126.6
top.insert(pya.DCellInstArray(cp.cell_index(), pya.DTrans(2, False, pya.DVector(CMPX, CMPY))))

SW_P = 13.8
SWY = -18.0
# segment A under main body: term, b0..b5 ; segment B under replica: b6, b7, inv, TG
SEG_A = ["term", "b0", "b1", "b2", "b3", "b4", "b5", "b6", "b7"]
SW_XA = {n: -6.1 + i * SW_P for i, n in enumerate(SEG_A)}    # -6.1 .. 104.3 (+12.4=116.7); flush with array
SW_XB = {"inv": 119.6, "tgc": 133.4}                          # seam island, flush east of main row
SW_X = dict(SW_XA)
for n in SEG_A:
    top.insert(pya.DCellInstArray(sw10.cell_index(), pya.DTrans(pya.DVector(SW_X[n], SWY))))
top.insert(pya.DCellInstArray(sw.cell_index(), pya.DTrans(pya.DVector(SW_XB["inv"], SWY))))
top.insert(pya.DCellInstArray(tg.cell_index(), pya.DTrans(pya.DVector(SW_XB["tgc"], SWY))))
BSX = 312.0                                                   # bstrap east of TG2 (row east end)
top.insert(pya.DCellInstArray(bst.cell_index(), pya.DTrans(pya.DVector(BSX, -17.8))))

NETS = ["b7", "b6", "b5", "b4", "b3", "b2", "b1", "b0", "term"]
RAIL_A = {n: 118.2 - i * 2.2 for i, n in enumerate(NETS)}     # main risers, inward
BOT_Y = SWY + 5.5
VIN_Y = SWY + 4.7
CTL_Y = SWY + 3.9
TRKB_Y = SWY + 3.1
TRK_Y = SWY + 6.3

# ---- row rails: continuous M1 pair spanning both segments + corridor
rect("m1", -7.5, SWY - 2.2, 312.5, SWY - 1.6)                 # VSS: one continuous row
rect("m1", -7.5, SWY + 12.4, 364.0, SWY + 13.0)               # VDD: one continuous row

# ---- trk / trkb / vin buses (M3, cell-frame pass-through; vin breaks before inv)
rect("m3", -5.1, TRK_Y - 0.2, 146.8, TRK_Y + 0.2)             # trk: main row + island
rect("m3", -5.1, TRKB_Y - 0.2, 148.0, TRKB_Y + 0.2)           # trkb: main row + island + south tap
rect("m3", -5.1, VIN_Y - 0.2, 117.1, VIN_Y + 0.2)             # vinr: main bits only
# ---- gb bus (boosted gate) + jog to the bstrap gb pin
rect("m3", -5.1, -11.08, 117.9, -10.68)
via2(117.7, -10.88)
vwire(117.7, -23.3, -10.88)
via2(117.7, -23.3)
rect("m3", 117.5, -23.5, 311.4, -23.1)
via2(311.2, -23.3)
vwire(311.2, -23.3, -14.1)
rect("m3", 310.9, -14.3, 312.2, -13.9)
via2(311.2, -14.1)
# ---- bstrap out -> vinr: south band under segment B -> riser at the b7 gap
rect("m3", 116.7, -35.7, 312.9, -35.3)
via2(116.9, -35.5)
vwire(116.9, -35.5, -13.3)
via2(116.9, -13.3)
via2(312.5, -35.5)
vwire(312.5, -35.5, -19.15)
via2(312.5, -19.15)
# ---- acore-level vin pin: top-level stub onto the bstrap vin band (east,
# clear of the gb riser pad at 254.5)
rect("m3", 330.8, -11.1, 333.5, -10.7)
top.shapes(L["m3p"]).insert(pya.DBox(332.9, -11.1, 333.5, -10.7))
top.shapes(L["m3l"]).insert(pya.DText("vin", pya.DTrans(pya.DVector(333.2, -10.9))))
# ---- bstrap VDD feed (west of its boot cap)
via1(347.6, SWY + 12.7)
vwire(347.6, -10.1, SWY + 12.7)
via1(347.6, -10.1)

# ---- bit fan: below-row ladder, riser corridor at rails
FAN_Y = {n: -24.4 - i * 1.3 for i, n in enumerate(NETS)}
for n in NETS:
    xb = SW_X[n] + 0.2
    xr = RAIL_A[n]
    via2(xb, BOT_Y)
    vwire(xb, BOT_Y, FAN_Y[n] + 0.2)
    via2(xb, FAN_Y[n])
    rect("m3", min(xb, xr) - 0.2, FAN_Y[n] - 0.2, max(xb, xr) + 0.2, FAN_Y[n] + 0.2)
    if xr > 100.0:                      # rail corridor overlaps cells b5..b7: M4 riser
        via3(xr, FAN_Y[n])
        v4wire(xr, FAN_Y[n], -2.75)
        via3(xr, -2.75)
        via2(xr, -2.75)
    else:
        via2(xr, FAN_Y[n])
        vwire(xr, FAN_Y[n], -2.6)
        via2(xr, -2.75)

# ---- ctl pins (west stub per bit cell)
for k in range(8):
    xc = SW_X[f"b{k}"]
    top.shapes(L["m3p"]).insert(pya.DBox(xc - 1.0, CTL_Y - 0.2, xc - 0.4, CTL_Y + 0.2))
    top.shapes(L["m3l"]).insert(pya.DText(f"ctl{k}", pya.DTrans(pya.DVector(xc - 0.7, CTL_Y))))

# ---- term ctl hardwired to row VDD rail (M1_M3 stack)
xt = SW_XA["term"] - 0.7
vwire(xt, CTL_Y, SWY + 12.7)
via2(xt, CTL_Y)
place = pya.DCellInstArray(VS_M1_M3.cell_index(),
                           pya.DTrans(pya.DVector(xt - VS_M1_M3.dbbox().center().x,
                                                  SWY + 12.7 - VS_M1_M3.dbbox().center().y)))
top.insert(place)
rect("m1", xt - 0.5, SWY + 12.4, xt + 0.5, SWY + 13.0)
rect("m3", xt - 0.5, SWY + 12.5, xt + 0.5, SWY + 12.9)

# ---- phase inverter: ctl=trk, bot->trkb, vin->VSS
x9 = SW_XB["inv"]
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

# ---- top-plate TM1 straps, band raised to 113.9..115.9 so the M2 pin drops
# stay inside the comparator's pin zone (no threading through cell interiors).
# Drops nudged inward: 0.22 clear of the inpair outer (tail) bars at abs 140.09
# / 154.11 while still overlapping the pin verticals (139.72../..154.68).
INN_X, INP_X = 139.68, 154.53
STRAP_Y = 114.9
PIN_TOP = CMPY - 5.0
rect("tm1", -1.0, 113.9, INN_X + 1.2, 115.9)   # main strap band (west)
rect("tm1", 0.0, 100.5, 2.0, 115.9)            # bond main spine to the band
place_vs(VS_M2_TM1, INN_X, STRAP_Y)
rect("m2", INN_X - 0.2, STRAP_Y, INN_X + 0.2, PIN_TOP - 0.6)
rect("tm1", INP_X - 1.2, 113.9, 295.0, 115.9)  # replica strap band (east)
rect("tm1", 292.2, 100.5, 294.2, 115.9)        # bond replica spine to the band
place_vs(VS_M2_TM1, INP_X, STRAP_Y)
rect("m2", INP_X - 0.2, STRAP_Y, INP_X + 0.2, PIN_TOP - 0.6)

# ---- TG: bot -> main topm via deep-south bus -> west stack; vin -> VCM band
xbt = SW_XB["tgc"] + 0.2
via2(xbt, BOT_Y)
vwire(xbt, BOT_Y, -36.5)
via2(xbt, -36.5)
rect("m3", -4.2, -36.7, xbt + 0.2, -36.3)
via3(-4.0, -36.5)
v4wire(-4.0, -36.5, -3.5)
via3(-4.0, -3.5)
via2(-4.0, -3.5)
vwire(-4.0, -3.5, STRAP_Y)
place_vs(VS_M2_TM1, -4.0, STRAP_Y)
rect("tm1", -5.2, 113.9, 1.0, 115.9)

# ---- VCM: replica riser tie band (M3-M3 direct) + east hook to TG vin + pin
vwire(149.2, -9.82, VIN_Y)
via2(149.2, VIN_Y)
via2(149.2, -9.82)
rect("m3", 145.4, VIN_Y - 0.2, 149.4, VIN_Y + 0.2)
top.shapes(L["m3p"]).insert(pya.DBox(160.0, -10.02, 160.5, -9.62))
top.shapes(L["m3l"]).insert(pya.DText("vcm", pya.DTrans(pya.DVector(160.25, -9.82))))

# ---- vin + trk pins (west end, clear of the term-tie riser)
for name, y in (("trk", TRK_Y),):
    rect("m3", 2.4, y - 0.2, 5.1, y + 0.2)
    top.shapes(L["m3p"]).insert(pya.DBox(2.4, y - 0.2, 3.0, y + 0.2))
    top.shapes(L["m3l"]).insert(pya.DText(name, pya.DTrans(pya.DVector(2.7, y))))

# ---- comparator clk: cell bus (abs y 122.3..122.7, x>=120.6) + west extension
CLKY = CMPY - 4.1
rect("m3", 116.8, CLKY - 0.2, 120.8, CLKY + 0.2)
top.shapes(L["m3p"]).insert(pya.DBox(116.8, CLKY - 0.2, 117.8, CLKY + 0.2))
top.shapes(L["m3l"]).insert(pya.DText("clk_cmp", pya.DTrans(pya.DVector(117.3, CLKY))))

# ---- comparator outputs: outp west extension (to logic 'cmp'), outn east export
OUTP_Y = CMPY - 17.2                            # cell outp band abs 125.02..153.09
rect("m3", 114.7, OUTP_Y - 0.2, 125.3, OUTP_Y + 0.2)
top.shapes(L["m3p"]).insert(pya.DBox(114.7, OUTP_Y - 0.2, 115.7, OUTP_Y + 0.2))
top.shapes(L["m3l"]).insert(pya.DText("outp", pya.DTrans(pya.DVector(115.2, OUTP_Y))))
OUTN_Y = CMPY - 16.4                            # cell outn band abs 110.0..110.4
rect("m3", 168.9, OUTN_Y - 0.2, 250.0, OUTN_Y + 0.2)
top.shapes(L["m3p"]).insert(pya.DBox(249.0, OUTN_Y - 0.2, 250.0, OUTN_Y + 0.2))
top.shapes(L["m3l"]).insert(pya.DText("outn", pya.DTrans(pya.DVector(249.5, OUTN_Y))))

# ---- comparator power. West margin (x 118.4..122) is a 5-track M2 bus at 0.7
# pitch: VSS 118.5 | VDD 119.2 | clk 119.9 | cmp 120.6 | sample 121.3 (last
# three added in core3). VSS goes up-and-over the cell top (M3 @131) to a west
# leg at x=-6; VDD drops straight south from its rail (cell bottom).
via1(118.5, 128.7)
vwire(118.5, 128.7, 131.0)
via2(118.5, 131.0)
rect("m3", -8.6, 130.8, 118.7, 131.2)
via2(-8.4, 131.0)
vwire(-8.4, 131.0, SWY - 1.9)
via1(-8.4, SWY - 1.9)
rect("m1", -8.9, SWY - 2.2, 2.7, SWY - 1.6)     # (west VSS leg lands on the rail)
via1(119.2, 101.1)
vwire(119.2, 101.1, SWY + 12.7)
via1(119.2, SWY + 12.7)

# ---- VDD/VSS core pins (west ends of the row rails)
top.shapes(L["m1p"]).insert(pya.DBox(2.6, SWY - 2.1, 3.4, SWY - 1.7))
top.shapes(L["m1l"]).insert(pya.DText("VSS", pya.DTrans(pya.DVector(3.0, SWY - 1.9))))
top.shapes(L["m1p"]).insert(pya.DBox(2.6, SWY + 12.5, 3.4, SWY + 12.9))
top.shapes(L["m1l"]).insert(pya.DText("VDD", pya.DTrans(pya.DVector(3.0, SWY + 12.7))))


# ================= acore6: mirrored replica switch row (same y as main) =================
NETS2 = ["b7r", "b6r", "b5r", "b4r", "b3r", "b2r", "b1r", "b0r", "termr"]
RAIL_B = {n: 176.0 + 2.2 * i for i, n in enumerate(NETS2)}
SW_X2 = {n: 173.9 + 13.8 * i for i, n in enumerate(NETS2)}    # 173.9 .. 284.3 (+12.4=296.7): centered on replica
for n in NETS2:
    top.insert(pya.DCellInstArray(sw10.cell_index(), pya.DTrans(pya.DVector(SW_X2[n], SWY))))
tg2x = 297.9
top.insert(pya.DCellInstArray(tg.cell_index(), pya.DTrans(pya.DVector(tg2x, SWY))))
# rails already span 2.6..330 (one continuous row) -> extend to cover TG2

# per-bit path: rail pad -> (3 west bits: M3 dogleg past the ctl drops)
# -> M2 vertical with x-monotone depth -> deep M3 band (-26.75-0.82k) -> cell bot riser
VX = {"b5r": 172.4, "b6r": 173.3, "b7r": 174.4, "b4r": 182.6, "b3r": 184.8,
      "b2r": 187.0, "b1r": 189.2, "b0r": 191.4, "termr": 193.6}
DEPTH = {n: -33.31 + 0.82 * i for i, n in enumerate(
    sorted(NETS2, key=lambda k: VX[k]))}
DOG_Y = {"b7r": -3.0, "b6r": -3.9, "b5r": -4.8}
for n in NETS2:
    xr, xv, yd = RAIL_B[n], VX[n], DEPTH[n]
    xb2 = SW_X2[n] + 0.2
    if n in DOG_Y:
        yg = DOG_Y[n]
        rect("m3", xr - 0.2, yg - 0.2, xr + 0.2, -2.4)
        rect("m3", xv - 0.2, yg - 0.2, xr + 0.2, yg + 0.2)
        via34(xv, yg)
        v5wire(xv, yd, yg)
    else:
        rect("m3", xr - 0.2, -3.0, xr + 0.2, -2.4)
        via34(xv, -2.8)
        v5wire(xv, yd, -2.8)
    via34(xv, yd)
    rect("m3", xv - 0.2, yd - 0.2, xb2 + 0.2, yd + 0.2)
    via2(xb2, yd)
    vwire(xb2, yd, BOT_Y)
    via2(xb2, BOT_Y)
# static midcode ties: b7r ctl -> VSS rail, others -> VDD rail
for i, n in enumerate(NETS2):
    xt2 = SW_X2[n] - 0.7
    via2(xt2, CTL_Y)
    if i == 0:
        vwire(xt2, SWY - 1.9, CTL_Y)
        via1(xt2, SWY - 1.9)
    else:
        vwire(xt2, CTL_Y, SWY + 12.7)
        via1(xt2, SWY + 12.7)
# dead gates: gb2 (cell local 6.92..7.32 -> abs -11.08..-10.68) -> VSS ; trkb2 -> VDD
rect("m3", 171.0, -11.08, 285.1, -10.68)
via2(171.2, -10.88)
vwire(171.2, -10.88, SWY - 1.9)
via1(171.2, SWY - 1.9)
rect("m3", 170.2, TRKB_Y - 0.2, 285.1, TRKB_Y + 0.2)
via2(170.4, TRKB_Y)
vwire(170.4, TRKB_Y, SWY + 12.7)
via1(170.4, SWY + 12.7)
# vcm: replica vin band (cell local 4.5..4.9 -> abs -13.5..-13.1) spans row + TG2 vin
rect("m3", 169.4, VIN_Y - 0.2, tg2x + 0.4, VIN_Y + 0.2)
# vcm bridge to the island TG vin (157.5 riser): -9.82 band from 157.5 east to 199.0 riser
via2(169.6, VIN_Y)
vwire(169.6, VIN_Y, -9.82)
via2(169.6, -9.82)
rect("m3", 149.0, -10.02, 169.8, -9.62)
# replica top TG2: bot -> topr via east TM1 corridor
xbt2 = tg2x + 0.2
via2(xbt2, BOT_Y)
vwire(xbt2, BOT_Y, -8.9)
via2(xbt2, -8.9)
rect("m3", xbt2 - 0.2, -9.1, 299.5, -8.7)
via3(299.3, -8.9)
v4wire(299.3, -8.9, 112.0)
via3(299.3, 112.0)
via2(299.3, 112.0)
vwire(299.3, 112.0, 114.9)
place_vs(VS_M2_TM1, 299.3, 114.9)
rect("tm1", 294.0, 113.9, 300.5, 115.9)
# TG2 gates: trk / trkb via a south detour under the replica row (avoid crossing island buses)
# trk: from main trk bus end (156.0) -> riser 155.8 -> band -21.5 -> riser 335.5 -> TG2 trk band
via2(146.6, TRK_Y)
vwire(146.6, -21.5, TRK_Y)
via2(146.6, -21.5)
rect("m3", 146.4, -21.7, 305.2, -21.3)
via3(305.0, -21.5)
v4wire(305.0, -21.5, TRK_Y)
via3(305.0, TRK_Y)
# trkb: bstrap ckb band ends 158.4; TG2 trkb via band -22.4
via2(147.8, TRKB_Y)
vwire(147.8, -22.4, TRKB_Y)
via2(147.8, -22.4)
rect("m3", 147.6, -22.6, 306.4, -22.2)
via3(306.2, -22.4)
v4wire(306.2, -22.4, TRKB_Y)
via3(306.2, TRKB_Y)
rect("m3", tg2x + 12.1, TRKB_Y - 0.2, 312.2, TRKB_Y + 0.2)

layout.write("oa_sar8_acore7.gds")
b = top.dbbox()
print(f"acore7: {b.width():.0f} x {b.height():.0f} um = {b.width()*b.height()/1e6:.3f} mm2")
print(f"seam: rails 118.2 .. 176.0 -> {176.0-118.2:.1f} um wide")
