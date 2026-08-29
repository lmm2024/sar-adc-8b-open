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
top = layout.create_cell("oa_sar8_acore9")

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
    rect("m5", snap(x - 0.2), snap(y - 0.22), snap(x + 0.2), snap(y + 0.22))


def v5wire(x, y1, y2):
    rect("m5", snap(x - 0.2), snap(min(y1, y2)), snap(x + 0.2), snap(max(y1, y2)))


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
SW_X = dict(SW_XA)
for n in SEG_A:
    top.insert(pya.DCellInstArray(sw10.cell_index(), pya.DTrans(pya.DVector(SW_X[n], SWY))))
# ---- row 2 (control/sampling island), centered under the seam: inv | TG | TG2 | bstrap
Y2 = -50.0
SW_XB = {"inv": 120.4, "tgc": 134.2, "tg2": 148.0}
BSX = 70.6                                                     # bstrap_p (west, normal)
BSXN = 219.4                                                   # bstrap_n origin (east, X-mirrored: spans 170.5..220.0)
top.insert(pya.DCellInstArray(sw.cell_index(), pya.DTrans(pya.DVector(SW_XB["inv"], Y2))))
top.insert(pya.DCellInstArray(tg.cell_index(), pya.DTrans(pya.DVector(SW_XB["tgc"], Y2))))
top.insert(pya.DCellInstArray(tg.cell_index(), pya.DTrans(pya.DVector(SW_XB["tg2"], Y2))))
top.insert(pya.DCellInstArray(bst.cell_index(), pya.DTrans(pya.DVector(BSX, Y2 + 0.2))))
top.insert(pya.DCellInstArray(bst.cell_index(), pya.DTrans(2, True, pya.DVector(BSXN, Y2 + 0.2))))
# row-2 bus y's (cell-local offsets identical to row 1)
BOT2, VIN2, CTL2, TRKB2, TRK2 = Y2 + 5.5, Y2 + 4.7, Y2 + 3.9, Y2 + 3.1, Y2 + 6.3

NETS = ["b7", "b6", "b5", "b4", "b3", "b2", "b1", "b0", "term"]
RAIL_A = {n: 118.2 - i * 2.2 for i, n in enumerate(NETS)}     # main risers, inward
BOT_Y = SWY + 5.5
VIN_Y = SWY + 4.7
CTL_Y = SWY + 3.9
TRKB_Y = SWY + 3.1
TRK_Y = SWY + 6.3

# ---- row rails: continuous M1 pair spanning both segments + corridor
rect("m1", -7.5, SWY - 2.2, 298.5, SWY - 1.6)                 # VSS: main + replica rows
rect("m1", -7.5, SWY + 12.4, 298.5, SWY + 13.0)               # VDD: main + replica rows
# row-2 rails + feeds (M2 verticals in the seam, x 150/151 clear of everything above)
rect("m1", 67.5, Y2 - 2.2, 222.5, Y2 - 1.6)                    # VSS2 (both bstraps + island)
rect("m1", 119.2, Y2 + 12.4, 161.0, Y2 + 13.0)                 # VDD2 (island only; bstraps have their own rails)
via1(67.8, SWY - 1.9)
vwire(67.8, Y2 - 1.9, SWY - 1.9)
via1(67.8, Y2 - 1.9)
via1(160.6, SWY + 12.7)
vwire(160.6, Y2 + 12.7, SWY + 12.7)
via1(160.6, Y2 + 12.7)

# ---- trk / trkb / vin buses (M3, cell-frame pass-through; vin breaks before inv)
rect("m3", -5.1, TRK_Y - 0.2, 121.6, TRK_Y + 0.2)             # trk: main row (+ drop to row 2 + sample tap 121.3)
rect("m3", -5.1, TRKB_Y - 0.2, 119.4, TRKB_Y + 0.2)           # trkb: main row (+ drop to row 2)
rect("m3", -5.1, VIN_Y - 0.2, 117.1, VIN_Y + 0.2)             # vinr: main bits only
# ---- gb bus (boosted gate) + jog to the bstrap gb pin
rect("m3", -5.1, -11.08, 117.9, -10.68)
via2(117.7, -10.88)
vwire(117.7, -35.6, -10.88)
via2(117.7, -35.6)
rect("m3", 69.2, -35.8, 117.9, -35.4)                          # gb_p shelf
via2(69.4, -35.6)
vwire(69.4, Y2 + 3.9, -35.6)
via2(69.4, Y2 + 3.9)
rect("m3", 69.2, Y2 + 3.7, 70.8, Y2 + 4.1)                     # -> bstrap_p g pin (west end)

# ---- bstrap out -> vinr: south band under segment B -> riser at the b7 gap
via2(116.9, -13.3)
vwire(116.9, -37.4, -13.3)
via2(116.9, -37.4)
rect("m3", 68.4, -37.6, 117.1, -37.2)                          # out_p shelf
via2(68.6, -37.4)
vwire(68.6, Y2 - 1.0, -37.4)
via2(68.6, Y2 - 1.0)
rect("m3", 68.4, Y2 - 1.2, 70.8, Y2 - 0.8)                     # -> bstrap_p out pin (west end)

# ---- acore-level vin pin: top-level stub onto the bstrap vin band (east,
# clear of the gb riser pad at 254.5)
rect("m3", 67.5, Y2 + 6.9, 70.6, Y2 + 7.3)
top.shapes(L["m3p"]).insert(pya.DBox(67.5, Y2 + 6.9, 68.1, Y2 + 7.3))
top.shapes(L["m3l"]).insert(pya.DText("vinp", pya.DTrans(pya.DVector(67.8, Y2 + 7.1))))
# vinn pin (bstrap_n vin band east end: mirrored local -0.4..19.6 -> abs 199.8..219.8)
rect("m3", 219.4, Y2 + 6.9, 222.5, Y2 + 7.3)
top.shapes(L["m3p"]).insert(pya.DBox(221.9, Y2 + 6.9, 222.5, Y2 + 7.3))
top.shapes(L["m3l"]).insert(pya.DText("vinn", pya.DTrans(pya.DVector(222.2, Y2 + 7.1))))
# ---- bstrap VDD feed (west of its boot cap)
rect("m1", 118.4, Y2 + 12.4, 119.4, Y2 + 13.0)                 # VDD2 west extension (M1)
rect("m1", 118.4, Y2 + 7.6, 119.0, Y2 + 13.0)                  # M1 drop to the bstrap_p VDD rail level
rect("m1", 118.4, Y2 + 7.6, 119.9, Y2 + 8.2)                   # joins bstrap_p rail (XR edge at 119.5)
rect("m1", 161.0, Y2 + 12.4, 170.7, Y2 + 13.0)                 # VDD2 east extension (M1)
rect("m1", 170.1, Y2 + 7.6, 170.7, Y2 + 13.0)                  # M1 drop to the bstrap_n VDD rail level
rect("m1", 170.1, Y2 + 7.6, 171.0, Y2 + 8.2)                   # joins bstrap_n rail (XR edge at 170.5)
rect("m1", 219.0, Y2 + 7.7, 220.6, Y2 + 8.1)                   # touch the mirrored VDD pin box (east end)

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
# trk / trkb drops from row 1 to row 2 (seam x 118.4 / 119.2)
via2(118.4, TRK_Y)
vwire(118.4, -34.5, TRK_Y)
via2(118.4, -34.5)
rect("m3", 118.2, -34.7, 162.0, -34.3)                         # trk shelf
via2(161.8, -34.5)
vwire(161.8, TRK2, -34.5)
via2(161.8, TRK2)
rect("m3", 119.2, TRK2 - 0.2, 162.0, TRK2 + 0.2)               # row-2 trk band: inv..TG2
via2(119.2, TRKB_Y)
vwire(119.2, -35.4, TRKB_Y)
via2(119.2, -35.4)
rect("m3", 119.0, -35.6, 163.6, -35.2)                         # trkb shelf
via2(163.4, -35.4)
vwire(163.4, TRKB2, -35.4)
via2(163.4, TRKB2)
rect("m3", 70.0, TRKB2 - 0.2, 220.0, TRKB2 + 0.2)              # row-2 trkb band: bstrap_p ckb .. island .. bstrap_n ckb
vwire(x9 - 0.7, CTL2, TRK2)
via2(x9 - 0.7, CTL2)
via2(x9 - 0.7, TRK2)
xb9 = x9 + 0.2
via2(xb9, BOT2)
vwire(xb9, TRKB2, BOT2)
via2(xb9, TRKB2)
xv9 = x9 + 5.0
via2(xv9, VIN2)
vwire(xv9, VIN2, Y2 - 1.9)
via1(xv9, Y2 - 1.9)

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
via2(xbt, BOT2)
vwire(xbt, BOT2, -36.5)
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
rect("m3", 133.0, VIN2 - 0.2, 160.6, VIN2 + 0.2)               # row-2 vcm band: TG vin .. TG2 vin
via2(133.2, VIN2)
vwire(133.2, VIN2, -9.82)                                       # riser to the -9.82 vcm bridge
via2(133.2, -9.82)
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
tg2x = SW_XB["tg2"]
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
# ---- replica (N-side) row is LIVE: ctl pins ctl0n..ctl7n, termr ctl -> VDD, gb_n bus, trkb bus, vinn_r bus
for k in range(8):
    n = f"b{k}r"
    xc = SW_X2[n]
    top.shapes(L["m3p"]).insert(pya.DBox(xc - 1.0, CTL_Y - 0.2, xc - 0.4, CTL_Y + 0.2))
    top.shapes(L["m3l"]).insert(pya.DText(f"ctl{k}n", pya.DTrans(pya.DVector(xc - 0.7, CTL_Y))))
xt2 = SW_X2["termr"] - 0.7
via2(xt2, CTL_Y)
vwire(xt2, CTL_Y, SWY + 12.7)
via1(xt2, SWY + 12.7)
# gb_n bus (cell gb band abs -11.08..-10.68) across the replica row -> riser at west end -> shelf -> bstrap_n g pin (east end 219.8..220.4 @ Y2+3.9)
rect("m3", 171.0, -11.08, 285.1, -10.68)
via2(171.2, -10.88)
vwire(171.2, -35.6, -10.88)
via2(171.2, -35.6)
rect("m3", 171.0, -35.8, 220.8, -35.4)                         # gb_n shelf
via2(220.6, -35.6)
vwire(220.6, Y2 + 3.9, -35.6)
via2(220.6, Y2 + 3.9)
rect("m3", 219.2, Y2 + 3.7, 220.8, Y2 + 4.1)                   # -> bstrap_n g pin (east end)
# trkb bus across the replica row, fed from the main trkb bus via the -35.4 shelf (extend shelf east) 
rect("m3", 170.2, TRKB_Y - 0.2, 285.1, TRKB_Y + 0.2)
via2(170.4, TRKB_Y)
vwire(170.4, TRKB_Y, -35.4)
via2(170.4, -35.4)
rect("m3", 163.2, -35.6, 170.6, -35.2)                         # trkb shelf east extension (joins 163.4 riser pad)
# vinn_r bus (VIN_Y) across the replica row <- bstrap_n out (east end pin @ Y2-1.0, x 219.2..220.4)
rect("m3", 169.4, VIN_Y - 0.2, 285.1, VIN_Y + 0.2)
via2(169.6, VIN_Y)
vwire(169.6, VIN_Y, -37.4)
via2(169.6, -37.4)
rect("m3", 169.4, -37.6, 221.6, -37.2)                         # out_n shelf
via2(221.4, -37.4)
vwire(221.4, Y2 - 1.0, -37.4)
via2(221.4, Y2 - 1.0)
rect("m3", 219.2, Y2 - 1.2, 221.6, Y2 - 0.8)                   # -> bstrap_n out pin (east end)
# vcm bridge to the island TG vin (157.5 riser): -9.82 band from 157.5 east to 199.0 riser

rect("m3", 133.0, -10.02, 160.5, -9.62)
# replica top TG2: bot -> topr via east TM1 corridor
xbt2 = tg2x + 0.2
via2(xbt2, BOT2)
vwire(xbt2, BOT2, -24.6)
via2(xbt2, -24.6)
rect("m3", xbt2 - 0.2, -24.8, 299.5, -24.4)                    # topr feed band under the replica row
via3(299.3, -24.6)
v4wire(299.3, -24.6, 112.0)
via3(299.3, 112.0)
via2(299.3, 112.0)
vwire(299.3, 112.0, 114.9)
place_vs(VS_M2_TM1, 299.3, 114.9)
rect("tm1", 294.0, 113.9, 300.5, 115.9)
# TG2 gates: trk / trkb via a south detour under the replica row (avoid crossing island buses)
# trk: from main trk bus end (156.0) -> riser 155.8 -> band -21.5 -> riser 335.5 -> TG2 trk band

# trkb: bstrap ckb band ends 158.4; TG2 trkb via band -22.4


layout.write("oa_sar8_acore9.gds")
b = top.dbbox()
print(f"acore9: {b.width():.0f} x {b.height():.0f} um = {b.width()*b.height()/1e6:.3f} mm2")
print(f"seam: rails 118.2 .. 176.0 -> {176.0-118.2:.1f} um wide")
