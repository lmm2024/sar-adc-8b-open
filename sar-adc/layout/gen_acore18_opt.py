#!/usr/bin/env python3
"""Generate the final optimized analog core from the signed-off acore13 topology.

Only the blocks changed by the latest TT front-simulation campaign are replaced:
two 1200-fF/W2 bootstrap cells, eighteen bit-tapered switch cells, and two
W2/W4 top-plate reset transmission gates.  CDAC, comparator and footer topology
remain identical to acore13.  The source transformation keeps the already
signed-off acore13 routing algorithm readable while giving the wider cells a
non-overlapping floorplan.
"""
from pathlib import Path


src = Path("gen_acore13.py").read_text(encoding="utf-8")


def once(old, new):
    global src
    if src.count(old) != 1:
        raise RuntimeError(f"expected one source block, found {src.count(old)}: {old[:80]!r}")
    src = src.replace(old, new)


once('top = layout.create_cell("oa_sar8_acore13")',
     'top = layout.create_cell("oa_sar8_acore18_opt")')

once('''layout.read("sw/sw_bitcell.gds")
layout.read("sw/sw_bitcell10.gds")
layout.read("sw/sw_bitcell11.gds")
layout.read("sw/sw_tg.gds")
layout.read("bs/bstrap40.gds")
cd = layout.cell("cdac_array")
cp = layout.cell("sa_comp")
sw = layout.cell("sw_bitcell")
sw10 = layout.cell("sw_bitcell10")
sw11 = layout.cell("sw_bitcell11")
tg = layout.cell("sw_tg")
bst = layout.cell("bstrap40")''', '''layout.read("sw/sw_bitcell.gds")
layout.read("sw/sw_bitcell10.gds")
for _n in ["term"] + [f"b{k}" for k in range(8)]:
    layout.read(f"sw/sw_bitcell_opt_{_n}.gds")
layout.read("sw/sw_tg_opt.gds")
layout.read("bs/bstrap_opt_w2_c1200.gds")
cd = layout.cell("cdac_array")
cp = layout.cell("sa_comp")
sw = layout.cell("sw_bitcell")
sw10 = layout.cell("sw_bitcell10")
sw_opt = {n: layout.cell(f"sw_bitcell_opt_{n}") for n in ["term"] + [f"b{k}" for k in range(8)]}
tg = layout.cell("sw_tg_opt")
bst = layout.cell("bstrap_opt_w2_c1200")''')

old_place = '''SW_P = 13.8
SWY = -18.0
# segment A under main body: term, b0..b5 ; segment B under replica: b6, b7, inv, TG
SEG_A = ["term", "b0", "b1", "b2", "b3", "b4", "b5", "b6", "b7"]
SW_XA = {n: -6.1 + i * SW_P for i, n in enumerate(SEG_A)}    # -6.1 .. 104.3 (+12.4=116.7); flush with array
SW_X = dict(SW_XA)
for n in SEG_A:
    top.insert(pya.DCellInstArray(sw11.cell_index(), pya.DTrans(pya.DVector(SW_X[n], SWY))))
# ---- row 2 (control/sampling island), centered under the seam: inv | TG | TG2 | bstrap
Y2 = -50.0
SW_XB = {"inv": 120.4, "tgc": 134.2, "tg2": 148.0}
BSX = 40.7                                                     # bstrap_p (west, normal): bstrap40 rails span BSX-0.6..BSX+78.8 -> east edge stays 119.5
BSXN = 241.3                                                   # bstrap_n origin (east, X-mirrored: rails span 162.5..241.9)
top.insert(pya.DCellInstArray(sw.cell_index(), pya.DTrans(pya.DVector(SW_XB["inv"], Y2))))
top.insert(pya.DCellInstArray(tg.cell_index(), pya.DTrans(pya.DVector(SW_XB["tgc"], Y2))))
top.insert(pya.DCellInstArray(tg.cell_index(), pya.DTrans(pya.DVector(SW_XB["tg2"], Y2))))
top.insert(pya.DCellInstArray(bst.cell_index(), pya.DTrans(pya.DVector(BSX, Y2 + 0.2))))
top.insert(pya.DCellInstArray(bst.cell_index(), pya.DTrans(2, True, pya.DVector(BSXN, Y2 + 0.2))))'''

new_place = '''SWY = -18.0
GAP = 0.60
SEG_A = ["term", "b0", "b1", "b2", "b3", "b4", "b5", "b6", "b7"]
# Preserve the signed-off seam: the widest b7 cell still ends at x=116.7.
SW_XA = {"b7": 116.7 - sw_opt["b7"].dbbox().right}
for _i in range(len(SEG_A) - 2, -1, -1):
    _n, _next = SEG_A[_i], SEG_A[_i + 1]
    SW_XA[_n] = SW_XA[_next] - sw_opt[_n].dbbox().width() - GAP
SW_X = dict(SW_XA)
for n in SEG_A:
    top.insert(pya.DCellInstArray(sw_opt[n].cell_index(), pya.DTrans(pya.DVector(SW_X[n], SWY))))
P_LEFT = min(SW_X[n] + sw_opt[n].dbbox().left for n in SEG_A)
P_RIGHT = max(SW_X[n] + sw_opt[n].dbbox().right for n in SEG_A)
VSSX = P_LEFT - 1.10
_nseq = ["b7", "b6", "b5", "b4", "b3", "b2", "b1", "b0", "term"]
_nx = 173.9
for _n in _nseq[:-1]:
    _nx += sw_opt[_n].dbbox().width() + GAP
N_RIGHT = _nx + sw_opt["term"].dbbox().right

# Control island stays in the central seam.  The large boot capacitors face
# outward, so their active pins sit beside the island without overlap.
Y2 = -50.0
SW_XB = {"inv": 120.4, "tgc": 134.2, "tg2": 148.8}
BSX = 118.0
BSXN = 174.0
top.insert(pya.DCellInstArray(sw.cell_index(), pya.DTrans(pya.DVector(SW_XB["inv"], Y2))))
top.insert(pya.DCellInstArray(tg.cell_index(), pya.DTrans(pya.DVector(SW_XB["tgc"], Y2))))
top.insert(pya.DCellInstArray(tg.cell_index(), pya.DTrans(pya.DVector(SW_XB["tg2"], Y2))))
top.insert(pya.DCellInstArray(bst.cell_index(), pya.DTrans(2, True, pya.DVector(BSX, Y2 + 0.2))))
top.insert(pya.DCellInstArray(bst.cell_index(), pya.DTrans(pya.DVector(BSXN, Y2 + 0.2))))'''
once(old_place, new_place)

# Wider row rails and pass-through buses.
for old, new in {
    'rect("m1", -7.3, SWY - 2.2, 118.9, SWY - 1.6)': 'rect("m1", P_LEFT, SWY - 2.2, 118.9, SWY - 1.6)',
    'rect("m1", 172.7, SWY - 2.2, 298.5, SWY - 1.6)': 'rect("m1", 172.7, SWY - 2.2, N_RIGHT, SWY - 1.6)',
    'rect("m1", -7.5, SWY + 12.4, 298.5, SWY + 13.0)': 'rect("m1", P_LEFT, SWY + 12.4, N_RIGHT, SWY + 13.0)',
    'rect("m3", -5.1, TRK_Y - 0.2, 121.6, TRK_Y + 0.2)': 'rect("m3", P_LEFT + 0.2, TRK_Y - 0.2, 121.6, TRK_Y + 0.2)',
    'rect("m3", -5.1, TRKB_Y - 0.2, 119.4, TRKB_Y + 0.2)': 'rect("m3", P_LEFT + 0.2, TRKB_Y - 0.2, 119.4, TRKB_Y + 0.2)',
    'rect("m3", -5.1, VIN_Y - 0.2, 117.1, VIN_Y + 0.2)': 'rect("m3", P_LEFT + 0.2, VIN_Y - 0.2, 117.1, VIN_Y + 0.2)',
    'rect("m3", -5.1, -11.08, 117.9, -10.68)': 'rect("m3", P_LEFT + 0.2, -11.08, 117.9, -10.68)',
}.items():
    once(old, new)

# Bootstrap pin routing: both 1200-fF cells have their pins at the central edge.
once('''rect("m3", 39.3, -35.8, 117.9, -35.4)                          # gb_p shelf
via2(39.5, -35.6)
vwire(39.5, Y2 + 3.9, -35.6)
via2(39.5, Y2 + 3.9)
rect("m3", 39.3, Y2 + 3.7, 40.9, Y2 + 4.1)                     # -> bstrap_p g pin (west end)''', '''rect("m3", 117.5, -35.8, 118.2, -35.4)
vwire(117.7, Y2 + 3.9, -35.6)
via2(117.7, Y2 + 3.9)
rect("m3", 117.5, Y2 + 3.7, 118.2, Y2 + 4.1)''')
once('''via2(116.9, -13.3)
vwire(116.9, -37.4, -13.3)
via2(116.9, -37.4)
rect("m3", 38.5, -37.6, 117.1, -37.2)                          # out_p shelf
via2(38.7, -37.4)
vwire(38.7, Y2 - 1.0, -37.4)
via2(38.7, Y2 - 1.0)
rect("m3", 38.5, Y2 - 1.2, 40.9, Y2 - 0.8)                     # -> bstrap_p out pin (west end)''', '''via34(116.9, -13.3)
rect("m5", 116.7, -13.5, 118.2, -13.1)
v5wire(118.0, Y2 - 1.0, -13.3)
via34(118.0, Y2 - 1.0)''')
once('''rect("m3", 37.6, Y2 + 6.9, 40.7, Y2 + 7.3)
top.shapes(L["m3p"]).insert(pya.DBox(37.6, Y2 + 6.9, 38.2, Y2 + 7.3))
top.shapes(L["m3l"]).insert(pya.DText("vinp", pya.DTrans(pya.DVector(37.9, Y2 + 7.1))))
# vinn pin (bstrap_n vin band east end: mirrored local -0.4..19.6 -> abs 199.8..219.8)
rect("m3", 241.3, Y2 + 6.9, 244.4, Y2 + 7.3)
top.shapes(L["m3p"]).insert(pya.DBox(243.8, Y2 + 6.9, 244.4, Y2 + 7.3))
top.shapes(L["m3l"]).insert(pya.DText("vinn", pya.DTrans(pya.DVector(244.1, Y2 + 7.1))))''', '''rect("m3", BSX - 0.4, Y2 + 6.9, BSX + 0.4, Y2 + 7.3)
top.shapes(L["m3p"]).insert(pya.DBox(BSX - 0.4, Y2 + 6.9, BSX + 0.4, Y2 + 7.3))
top.shapes(L["m3l"]).insert(pya.DText("vinp", pya.DTrans(pya.DVector(BSX, Y2 + 7.1))))
rect("m3", BSXN - 0.4, Y2 + 6.9, BSXN + 0.4, Y2 + 7.3)
top.shapes(L["m3p"]).insert(pya.DBox(BSXN - 0.4, Y2 + 6.9, BSXN + 0.4, Y2 + 7.3))
top.shapes(L["m3l"]).insert(pya.DText("vinn", pya.DTrans(pya.DVector(BSXN, Y2 + 7.1))))''')

once('''rect("m1", 118.4, Y2 + 12.4, 119.4, Y2 + 13.0)                 # VDD2 west extension (M1)
rect("m1", 118.4, Y2 + 7.6, 119.0, Y2 + 13.0)                  # M1 drop to the bstrap_p VDD rail level
rect("m1", 118.4, Y2 + 7.6, 119.9, Y2 + 8.2)                   # joins bstrap_p rail (XR edge at 119.5)
rect("m1", 161.0, Y2 + 12.4, 163.0, Y2 + 13.0)                 # VDD2 east extension (M1)
rect("m1", 162.1, Y2 + 7.6, 162.7, Y2 + 13.0)                  # M1 drop to the bstrap_n VDD rail level
rect("m1", 162.1, Y2 + 7.6, 163.0, Y2 + 8.2)                   # joins bstrap_n rail (west edge at 162.5)
rect("m1", 240.9, Y2 + 7.7, 242.5, Y2 + 8.1)                   # touch the mirrored VDD pin box (east end)''', '''rect("m1", BSX - 0.4, Y2 + 7.6, 119.8, Y2 + 8.2)
rect("m1", 119.2, Y2 + 7.6, 119.8, Y2 + 13.0)
rect("m1", 160.4, Y2 + 12.4, BSXN + 0.4, Y2 + 13.0)
rect("m1", BSXN - 0.4, Y2 + 7.6, BSXN + 0.4, Y2 + 13.0)''')

once('rect("m1", 39.6, Y2 - 2.2, 243.0, Y2 - 1.6)',
     'rect("m1", BSX - 0.4, Y2 - 2.2, BSXN + 0.4, Y2 - 1.6)')
once('rect("m3", 40.3, TRKB2 - 0.2, 242.2, TRKB2 + 0.2)',
     'rect("m3", BSX - 0.2, TRKB2 - 0.2, BSXN + 0.2, TRKB2 + 0.2)')

# Replica row: variable pitch, same signed-off inner edge.
once('''SW_X2 = {n: 173.9 + 13.8 * i for i, n in enumerate(NETS2)}    # 173.9 .. 284.3 (+12.4=296.7): centered on replica
for n in NETS2:
    top.insert(pya.DCellInstArray(sw11.cell_index(), pya.DTrans(pya.DVector(SW_X2[n], SWY))))''', '''SW_X2 = {"b7r": 173.9}
for _i in range(1, len(NETS2)):
    _prev, _n = NETS2[_i - 1], NETS2[_i]
    _prev_base = _prev[:-1]
    SW_X2[_n] = SW_X2[_prev] + sw_opt[_prev_base].dbbox().width() + GAP
for n in NETS2:
    top.insert(pya.DCellInstArray(sw_opt[n[:-1]].cell_index(), pya.DTrans(pya.DVector(SW_X2[n], SWY))))
N_RIGHT = max(SW_X2[n] + sw_opt[n[:-1]].dbbox().right for n in NETS2)''')

for old, new in {
    'rect("m3", 171.0, -11.08, 285.1, -10.68)': 'rect("m3", 171.0, -11.08, N_RIGHT, -10.68)',
    'rect("m3", 171.0, -35.8, 242.7, -35.4)': 'rect("m3", 171.0, -35.8, BSXN + 0.2, -35.4)',
    'via2(242.5, -35.6)': 'via2(BSXN, -35.6)',
    'vwire(242.5, Y2 + 3.9, -35.6)': 'vwire(BSXN, Y2 + 3.9, -35.6)',
    'via2(242.5, Y2 + 3.9)': 'via2(BSXN, Y2 + 3.9)',
    'rect("m3", 241.1, Y2 + 3.7, 242.7, Y2 + 4.1)': 'rect("m3", BSXN - 0.2, Y2 + 3.7, BSXN + 0.2, Y2 + 4.1)',
    'rect("m3", 170.2, TRKB_Y - 0.2, 285.1, TRKB_Y + 0.2)': 'rect("m3", 170.2, TRKB_Y - 0.2, N_RIGHT, TRKB_Y + 0.2)',
    'rect("m3", 169.4, VIN_Y - 0.2, 285.1, VIN_Y + 0.2)': 'rect("m3", 169.4, VIN_Y - 0.2, N_RIGHT, VIN_Y + 0.2)',
    'rect("m3", 169.4, -37.6, 243.5, -37.2)': 'rect("m3", 169.4, -37.6, BSXN + 0.2, -37.2)',
    'via2(243.3, -37.4)': 'via3(BSXN, -37.4)',
    'vwire(243.3, Y2 - 1.0, -37.4)': 'v4wire(BSXN, Y2 - 1.0, -37.4)',
    'via2(243.3, Y2 - 1.0)': 'via3(BSXN, Y2 - 1.0)',
    'rect("m3", 241.1, Y2 - 1.2, 243.5, Y2 - 0.8)': 'rect("m3", BSXN - 0.2, Y2 - 1.2, BSXN + 0.2, Y2 - 0.8)',
    'rect("m1", 172.7, SWY - 3.2, 298.5, SWY - 2.6)': 'rect("m1", 172.7, SWY - 3.2, N_RIGHT, SWY - 2.6)',
    'rect("m3", -9.6, GLOB_Y - 0.2, 312.0, GLOB_Y + 0.2)': 'rect("m3", -9.6, GLOB_Y - 0.2, N_RIGHT + 14.0, GLOB_Y + 0.2)',
    'rect("m3", 118.0, TRKB_S - 0.2, 312.0, TRKB_S + 0.2)': 'rect("m3", 118.0, TRKB_S - 0.2, N_RIGHT + 14.0, TRKB_S + 0.2)',
}.items():
    once(old, new)

once('''for fx in (300.5, 305.5):
    footer(fx, -34.0, SWY - 1.9, TRKB_S, GLOB_Y)
rect("m1", 118.9, SWY - 2.2, 129.6, SWY - 1.6)                    # gated P rail extends under its footers
rect("m1", 298.5, SWY - 2.2, 310.5, SWY - 1.6)                    # gated N rail extends under its footers
layout.write("oa_sar8_acore13.gds")''', '''for fx in (N_RIGHT + 2.0, N_RIGHT + 7.0):
    footer(fx, -34.0, SWY - 1.9, TRKB_S, GLOB_Y)
rect("m1", 118.9, SWY - 2.2, 129.6, SWY - 1.6)
rect("m1", N_RIGHT, SWY - 2.2, N_RIGHT + 12.0, SWY - 1.6)
layout.write("oa_sar8_acore18_opt.gds")''')
once('print(f"acore13: {b.width():.0f} x {b.height():.0f} um = {b.width()*b.height()/1e6:.3f} mm2")',
     'print(f"acore18_opt: {b.width():.0f} x {b.height():.0f} um = {b.width()*b.height()/1e6:.3f} mm2")')

# The tapered P row grows westward.  Move the global VSS service leg by the
# same amount so it remains outside the device guard rings.
for old, new in (
    ("-9.6", "VSSX - 1.2"), ("-9.5", "VSSX - 1.1"),
    ("-9.2", "VSSX - 0.8"), ("-9.1", "VSSX - 0.7"),
    ("-8.9", "VSSX - 0.5"), ("-8.7", "VSSX - 0.3"),
    ("-8.6", "VSSX - 0.2"), ("-8.4", "VSSX"),
    ("-7.6", "VSSX + 0.8"),
):
    src = src.replace(old, new)

exec(compile(src, "gen_acore18_opt.expanded.py", "exec"))
print("P_CTL", {k: SW_X[f"b{k}"] - 0.7 for k in range(8)})
print("N_CTL", {k: SW_X2[f"b{k}r"] - 0.7 for k in range(8)})
