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
top = layout.create_cell("oa_sar8_acore3")

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
top.insert(pya.DCellInstArray(cd.cell_index(), pya.DTrans(pya.DVector(198.0, 0))))
CMPX, CMPY = 147.1, 126.6
top.insert(pya.DCellInstArray(cp.cell_index(), pya.DTrans(2, False, pya.DVector(CMPX, CMPY))))

SW_P = 13.8
SWY = -18.0
# segment A under main body: term, b0..b5 ; segment B under replica: b6, b7, inv, TG
SEG_A = ["term", "b0", "b1", "b2", "b3", "b4", "b5"]
SW_XA = {n: 4.0 + i * SW_P for i, n in enumerate(SEG_A)}
SW_XB = {"b6": 198.0, "b7": 211.8, "inv": 225.6, "tgc": 239.4}
SW_X = {**SW_XA, **{k: v for k, v in SW_XB.items() if k in ("b6", "b7")}}
for n in SEG_A + ["b6", "b7"]:
    top.insert(pya.DCellInstArray(sw.cell_index(), pya.DTrans(pya.DVector(SW_X[n], SWY))))
top.insert(pya.DCellInstArray(sw.cell_index(), pya.DTrans(pya.DVector(SW_XB["inv"], SWY))))
top.insert(pya.DCellInstArray(tg.cell_index(), pya.DTrans(pya.DVector(SW_XB["tgc"], SWY))))

NETS = ["b7", "b6", "b5", "b4", "b3", "b2", "b1", "b0", "term"]
RAIL_A = {n: 118.2 - i * 2.2 for i, n in enumerate(NETS)}     # main risers, inward
BOT_Y = SWY + 5.5
VIN_Y = SWY + 4.7
CTL_Y = SWY + 3.9
TRKB_Y = SWY + 3.1
TRK_Y = SWY + 6.3

# ---- row rails: continuous M1 pair spanning both segments + corridor
rect("m1", 2.6, SWY - 2.2, 254.0, SWY - 1.6)                  # VSS
rect("m1", 2.6, SWY + 12.4, 254.0, SWY + 13.0)                # VDD

# ---- trk / trkb / vin buses (M3, cell-frame pass-through; vin breaks before inv)
rect("m3", 5.0, TRK_Y - 0.2, 251.7, TRK_Y + 0.2)              # trk: all cells + TG
rect("m3", 5.0, TRKB_Y - 0.2, 251.7, TRKB_Y + 0.2)            # trkb: all cells + TG
rect("m3", 5.0, VIN_Y - 0.2, 224.1, VIN_Y + 0.2)              # vin: bits only (stop b7)

# ---- bit fan: below-row ladder, riser corridor at rails
FAN_Y = {n: -24.4 - i * 1.3 for i, n in enumerate(NETS)}
for n in NETS:
    xb = SW_X[n] + 0.2
    xr = RAIL_A[n]
    via2(xb, BOT_Y)
    vwire(xb, BOT_Y, FAN_Y[n] + 0.2)
    via2(xb, FAN_Y[n])
    rect("m3", min(xb, xr) - 0.2, FAN_Y[n] - 0.2, max(xb, xr) + 0.2, FAN_Y[n] + 0.2)
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
via2(-4.0, -36.5)
vwire(-4.0, -36.5, STRAP_Y)
place_vs(VS_M2_TM1, -4.0, STRAP_Y)
rect("tm1", -5.2, 113.9, 1.0, 115.9)

# ---- VCM: replica riser tie band (M3-M3 direct) + east hook to TG vin + pin
rect("m3", 174.0, -2.7, 256.0, -2.3)
vwire(255.5, -2.5, VIN_Y)
via2(255.5, -2.5)
via2(255.5, VIN_Y)
rect("m3", 251.5, VIN_Y - 0.2, 255.7, VIN_Y + 0.2)
top.shapes(L["m3p"]).insert(pya.DBox(255.5, -2.7, 256.0, -2.3))
top.shapes(L["m3l"]).insert(pya.DText("vcm", pya.DTrans(pya.DVector(255.7, -2.5))))

# ---- vin + trk pins (west end, clear of the term-tie riser)
for name, y in (("vin", VIN_Y), ("trk", TRK_Y)):
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
rect("m3", -6.2, 130.8, 118.7, 131.2)
via2(-6.0, 131.0)
vwire(-6.0, 131.0, SWY - 1.9)
via1(-6.0, SWY - 1.9)
rect("m1", -6.5, SWY - 2.2, 2.7, SWY - 1.6)     # west extension of the VSS rail
via1(119.2, 101.1)
vwire(119.2, 101.1, SWY + 12.7)
via1(119.2, SWY + 12.7)

# ---- VDD/VSS core pins (west ends of the row rails)
top.shapes(L["m1p"]).insert(pya.DBox(2.6, SWY - 2.1, 3.4, SWY - 1.7))
top.shapes(L["m1l"]).insert(pya.DText("VSS", pya.DTrans(pya.DVector(3.0, SWY - 1.9))))
top.shapes(L["m1p"]).insert(pya.DBox(2.6, SWY + 12.5, 3.4, SWY + 12.9))
top.shapes(L["m1l"]).insert(pya.DText("VDD", pya.DTrans(pya.DVector(3.0, SWY + 12.7))))

layout.write("oa_sar8_acore3.gds")
b = top.dbbox()
print(f"acore3: {b.width():.0f} x {b.height():.0f} um = {b.width()*b.height()/1e6:.3f} mm2")
print(f"seam: rails 118.2 .. 176.0 -> {176.0-118.2:.1f} um wide")
