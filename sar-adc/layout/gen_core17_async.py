#!/usr/bin/env python3
"""Assemble the repository analog core with the physical async SAR macro.

This is the first layout-level integration of sar_ctrl_async_phys.  It keeps
the DRC/LVS-clean acore13 geometry intact and places the 65 x 100 um digital
macro in the central CDAC seam.  All protocol-sensitive nets leave the macro
on M3 and change to M4 before crossing the analog switch rows.
"""
import pya

ASYNC_GDS = "../logic/runs/RUN_2026-08-20_POSTDAC_PENDING/final/gds/sar_ctrl_async_phys.gds"
TOP_NAME = "oa_sar8_core17_async"


layout = pya.Layout()
layout.technology_name = "sg13g2"
layout.dbu = 0.001
top = layout.create_cell(TOP_NAME)
layout.read("oa_sar8_acore13.gds")
# Both source GDS files contain common SG13G2 helper-cell names.  Rename only
# conflicting cells from the second file so KLayout preserves both clean
# hierarchies instead of merging their contents under one name.
load_options = pya.LoadLayoutOptions()
load_options.cell_conflict_resolution = pya.LoadLayoutOptions.RenameCell
layout.read(ASYNC_GDS, load_options)
ac = layout.cell("oa_sar8_acore13")
lg = layout.cell("sar_ctrl_async_phys")

L = {}
for num, name in ((8, "m1"), (19, "v1"), (10, "m2"), (29, "v2"),
                  (30, "m3"), (49, "v3"), (50, "m4"), (66, "v4"),
                  (67, "m5"), (126, "tm1"), (134, "tm2")):
    L[name] = layout.layer(num, 0)
for num, tag in ((8, "m1"), (10, "m2"), (30, "m3"), (50, "m4"),
                 (67, "m5"), (126, "tm1"), (134, "tm2")):
    L[tag + "p"] = layout.layer(num, 2)
    L[tag + "l"] = layout.layer(num, 25)


def rect(layer, x1, y1, x2, y2):
    top.shapes(L[layer]).insert(pya.DBox(x1, y1, x2, y2))


def snap(v):
    return round(round(v * 100) / 100.0, 2)


def via2(x, y):
    x1, y1 = snap(x - 0.095), snap(y - 0.095)
    rect("v2", x1, y1, x1 + 0.19, y1 + 0.19)
    rect("m2", x - 0.2, y - 0.2, x + 0.2, y + 0.2)
    rect("m3", x - 0.2, y - 0.2, x + 0.2, y + 0.2)


def via3(x, y):
    x1, y1 = snap(x - 0.095), snap(y - 0.095)
    rect("v3", x1, y1, x1 + 0.19, y1 + 0.19)
    rect("m3", x - 0.2, y - 0.2, x + 0.2, y + 0.2)
    rect("m4", x - 0.2, y - 0.2, x + 0.2, y + 0.2)


def via4(x, y):
    x1, y1 = snap(x - 0.095), snap(y - 0.095)
    rect("v4", x1, y1, x1 + 0.19, y1 + 0.19)
    rect("m4", x - 0.2, y - 0.2, x + 0.2, y + 0.2)
    rect("m5", x - 0.2, y - 0.2, x + 0.2, y + 0.2)


def m2v(x, y1, y2):
    rect("m2", x - 0.2, min(y1, y2), x + 0.2, max(y1, y2))


def m4v(x, y1, y2):
    rect("m4", x - 0.2, min(y1, y2), x + 0.2, max(y1, y2))


def m5v(x, y1, y2):
    rect("m5", x - 0.2, min(y1, y2), x + 0.2, max(y1, y2))


def pin(layer, name, box, at):
    top.shapes(L[layer + "p"]).insert(pya.DBox(*box))
    top.shapes(L[layer + "l"]).insert(pya.DText(name, pya.DTrans(pya.DVector(*at))))


# Existing analog core plus the new physical asynchronous controller.
top.insert(pya.DCellInstArray(ac.cell_index(), pya.DTrans()))
LX, LY = 122.0, 145.0
top.insert(pya.DCellInstArray(lg.cell_index(), pya.DTrans(pya.DVector(LX, LY))))

# Comparator outputs -> asynchronous decision inputs.
# cmp_p: analog outp y=109.4 to macro west pin center y=9.66.
rect("m3", 120.4, LY + 9.46, LX + 0.4, LY + 9.86)
via2(120.6, LY + 9.66)
m2v(120.6, LY + 9.66, 109.4)
via2(120.6, 109.4)
# cmp_n: analog outn bar y=110.2 to macro west pin center y=25.62.
rect("m3", 116.8, LY + 25.42, LX + 0.4, LY + 25.82)
via2(117.0, LY + 25.62)
m2v(117.0, LY + 25.62, 110.2)
via2(117.0, 110.2)
rect("m3", 116.8, 110.0, 169.1, 110.4)

# Macro-generated comparator fire, sample gate and bottom-plate hold request.
# M4 is used for the long verticals so these nets can cross the analog M2/M3
# seam routing without accidental shorts.
for yp, x, ya in ((57.54, 121.6, 122.5),  # cmp_fire -> comparator clock
                  (73.50, 120.8, -11.7),  # sample -> track/bootstrap bus
                  (89.46, 120.0, -25.65)): # hold_req -> footer band
    yp += LY
    # Cover the complete 0.4 um macro pin landing.  Matching both its exact
    # DEF center and width avoids creating a narrow notch at the block edge.
    rect("m3", x - 0.2, yp - 0.2, LX + 0.4, yp + 0.2)
    via3(x, yp)
    m4v(x, yp, ya)
    via3(x, ya)
if True:
    rect("m3", 119.7, 122.3, 121.8, 122.7)

# External track input.  Keep the top-level landing next to the macro; a chip
# wrapper can lift it to pads without crossing the precision CDAC.
rect("m3", 118.8, LY + 41.38, LX + 0.4, LY + 41.78)
pin("m3", "track", (118.8, LY + 41.38, 119.6, LY + 41.78),
    (119.2, LY + 41.58))

# DAC controls.  Every macro E-side pin first jogs outward on M3, then changes
# to a unique M4 vertical track.  P-row drivers are inverting, hence P takes
# dac_code_n and N takes dac_code, matching the repository polarity contract.
DAC_Y = {k: 70.14 - 2.52 * k for k in range(8)}
DACN_Y = {k: 90.30 - 2.52 * k for k in range(8)}
TRACK_Y = {k: -55.0 - 1.3 * k for k in range(8)}
TRACKN_Y = {k: -65.4 - 1.3 * k for k in range(8)}
STUB_X = {0: 7.0, 1: 20.8, 2: 34.6, 3: 48.4,
          4: 62.2, 5: 76.0, 6: 89.8, 7: 103.6}
STUBN_X = {k: 173.2 + 13.8 * (7 - k) for k in range(8)}
DROPN_X = dict(STUBN_X)
DROPN_X[7] = 176.0
DROPN_X[6] = 188.1
CTL_Y = -14.1

routes = []
# Centers selected by scan_m4_corridors.py.  Each complete vertical corridor
# is empty in acore13 and has at least 0.6 um clearance to existing M4.
DROP_X_P = [194.6, 195.7, 196.8, 231.0, 201.8, 202.9, 206.7, 207.8]
DROP_X_N = [208.9, 212.7, 213.8, 237.0, 218.7, 219.8, 220.9, 224.7]
for k in range(8):
    routes.append((f"dac_code_n[{k}]", LY + DACN_Y[k], DROP_X_P[k],
                   TRACK_Y[k], STUB_X[k], STUB_X[k]))
for k in range(8):
    routes.append((f"dac_code[{k}]", LY + DAC_Y[k], DROP_X_N[k],
                   TRACKN_Y[k], STUBN_X[k], DROPN_X[k]))

for _name, yp, xd, yt, xp, xs in routes:
    rect("m3", LX + 64.6, yp - 0.2, xd + 0.2, yp + 0.2)
    via3(xd, yp)
    m4v(xd, yp, yt)
    via3(xd, yt)
    rect("m3", min(xd, xs) - 0.2, yt - 0.2, max(xd, xs) + 0.2, yt + 0.2)
    via3(xs, yt)
    if xs != xp:
        m4v(xs, yt, CTL_Y)
        via3(xs, CTL_Y)
        rect("m3", min(xs, xp) - 0.2, CTL_Y - 0.2,
             max(xs, xp) + 0.2, CTL_Y + 0.2)
    else:
        m4v(xs, yt, -22.0)
        via3(xs, -22.0)
        via2(xs, -22.0)
        m2v(xs, -22.0, CTL_Y)
        via2(xs, CTL_Y)

# Re-export digital status and reset as top-level M3 landings immediately east
# of the macro.  They remain accessible to the later pad-ring wrapper.
E_PINS = [("rst_n", 4.62)]
E_PINS += [(f"result[{k}]", 7.14 + 2.52 * k) for k in range(8)]
E_PINS += [("done", 27.30), ("busy", 29.82)]
for name, y in E_PINS:
    y += LY
    rect("m3", LX + 64.6, y - 0.2, LX + 66.2, y + 0.2)
    pin("m3", name, (LX + 65.0, y - 0.2, LX + 66.2, y + 0.2),
        (LX + 65.8, y))

# Power distribution: join the macro's TM1 VDD/VSS stripes (x=19/25 local)
# and the analog rails to the same wide TM2 landing bars used by core16.
lib = pya.Library.library_by_name("SG13_dev", "sg13g2")


def via_stack(bottom, top_layer, cols=2):
    decl = lib.layout().pcell_declaration("via_stack")
    params = {p.name: p.default for p in decl.get_parameters()}
    params.update({"b_layer": bottom, "t_layer": top_layer,
                   "vn_columns": cols, "vn_rows": cols})
    return layout.create_cell("via_stack", "SG13_dev", params)


VS_M1_TM1 = via_stack("Metal1", "TopMetal1")
VS_M2_TM1 = via_stack("Metal2", "TopMetal1")
VS_TM1_TM2 = via_stack("TopMetal1", "TopMetal2")


def place_vs(cell, x, y):
    c = cell.dbbox().center()
    top.insert(pya.DCellInstArray(cell.cell_index(),
               pya.DTrans(pya.DVector(x - c.x, y - c.y))))


rect("tm2", -15.0, 133.0, 300.5, 136.0)
rect("tm2", -15.0, 138.5, 300.5, 141.5)
# Digital vertical TM1 stripes.
rect("tm1", LX + 17.9, 134.5, LX + 20.1, LY + 7.34)
place_vs(VS_TM1_TM2, LX + 19.0, 134.5)
rect("tm1", LX + 23.9, 140.0, LX + 26.1, LY + 7.34)
place_vs(VS_TM1_TM2, LX + 25.0, 140.0)
# Analog VSS and VDD connections retained from core16.
rect("m2", -8.6, 131.0, -8.2, 140.0)
place_vs(VS_M2_TM1, -8.4, 140.0)
place_vs(VS_TM1_TM2, -8.4, 140.0)
rect("m1", -15.0, -5.6, -7.5, -5.0)
place_vs(VS_M1_TM1, -13.4, -5.3)
rect("tm1", -14.6, -6.4, -12.2, 135.8)
place_vs(VS_TM1_TM2, -13.4, 134.5)
pin("tm2", "VDD", (-15.0, 133.0, 300.5, 136.0), (142.0, 134.5))
pin("tm2", "VSS", (-15.0, 138.5, 300.5, 141.5), (142.0, 140.0))

# Analog input/common-mode exports, matching the corrected core16 geometry.
XW, XE, YS = -15.0, 300.5, -76.0
rect("m3", XW, -43.1, 38.2, -42.7)
pin("m3", "vinp", (XW, -43.1, XW + 1.5, -42.7), (XW + 0.75, -42.9))
rect("m3", 243.8, -43.1, XE, -42.7)
pin("m3", "vinn", (XE - 1.5, -43.1, XE, -42.7), (XE - 0.75, -42.9))
via3(160.6, -45.3)
m4v(160.6, YS, -45.3)
pin("m4", "vcm", (160.4, YS, 160.8, YS + 1.5), (160.6, YS + 0.75))

layout.write(TOP_NAME + ".gds")
b = top.dbbox()
print(f"{TOP_NAME}: {b.width():.1f} x {b.height():.1f} um = "
      f"{b.width()*b.height()/1e6:.4f} mm2")
