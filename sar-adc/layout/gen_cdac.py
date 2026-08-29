#!/usr/bin/env python3
"""OA-SAR8 CDAC array generator: 16x16 cmim units, 2-fold common-centroid.

Row plan (mirror-symmetric about array center):
  rows 0-3,12-15 -> b7 (128u)   rows 4-5,10-11 -> b6 (64u)   rows 6,9 -> b5 (32u)
  rows 7,8 (center band, point-symmetric pairs (7,c)<->(8,15-c)):
    cols 0-7 b4, 8-11 b3, 12-13 b2, 14 b1, 15: b0 @(7,15) / term @(8,0-mirror)
Wiring: bottom plates = Metal5 row straps (full rows) / stubs into a center
Metal3 channel (mixed rows); per-bit vertical Metal3 rails on the left edge.
Top plates: TopMetal1 row straps + right-edge spine. Pins on Metal3/TopMetal1.
Run inside container: klayout -zz -r gen_cdac.py
"""
import pya

# ---- geometry constants (um)
CW = 2.2            # cap w=l  -> C = 1.5f * 4.84 = 7.26 fF
PITCH = 6.0
NROW = NCOL = 16
GAP = 8.0           # extra center channel between rows 7 and 8
CH_L = 22.0         # left routing channel width (9 rails)
RAIL_P = 2.2        # rail pitch
M5_STRAP = 1.2
TM1_STRAP = 2.0

NETS = ["b7", "b6", "b5", "b4", "b3", "b2", "b1", "b0", "term"]

layout = pya.Layout()
layout.technology_name = "sg13g2"
layout.dbu = 0.001
top = layout.create_cell("cdac_array")

l_m3 = layout.layer(30, 0)
l_m3pin = layout.layer(30, 2)
l_m3lbl = layout.layer(30, 25)
l_m2 = layout.layer(10, 0)
l_m5 = layout.layer(67, 0)
l_tm1 = layout.layer(126, 0)
l_tm1pin = layout.layer(126, 2)
l_tm1lbl = layout.layer(126, 25)

lib = pya.Library.library_by_name("SG13_dev", "sg13g2")
decl = lib.layout().pcell_declaration("cmim")
params = {p.name: p.default for p in decl.get_parameters()}
params["Calculate"] = "w&l"
params["C"] = "7.26f"
cap_cell = layout.create_cell("cmim", "SG13_dev", params)

vd = lib.layout().pcell_declaration("via_stack")
vparams = {p.name: p.default for p in vd.get_parameters()}
vparams["b_layer"] = "Metal3"
vparams["t_layer"] = "Metal5"
vparams["vn_columns"] = 2
vparams["vn_rows"] = 2
via_m3m5 = layout.create_cell("via_stack", "SG13_dev", vparams)
v1params = dict(vparams)
v1params["b_layer"] = "Metal2"
v1params["vn_columns"] = 1
v1params["vn_rows"] = 1
via_m2m5 = layout.create_cell("via_stack", "SG13_dev", v1params)
v2params = dict(vparams)
v2params["b_layer"] = "Metal2"
v2params["t_layer"] = "Metal3"
v2params["vn_columns"] = 2
v2params["vn_rows"] = 2
via_m2m3 = layout.create_cell("via_stack", "SG13_dev", v2params)
via_bc = via_m3m5.dbbox().center()


def place_via(x, y, pad=1.0, cell=None, pad_layers=None):
    vc = cell or via_m3m5
    bc = vc.dbbox().center()
    top.insert(pya.DCellInstArray(vc.cell_index(),
                                  pya.DTrans(pya.DVector(x - bc.x, y - bc.y))))
    for lay in (pad_layers or [l_m3, l_m5]):
        box(lay, x - pad, y - pad, x + pad, y + pad)


def row_y(r):
    return r * PITCH + (GAP if r >= 8 else 0.0)


def bit_of(r, c):
    if r in (0, 1, 2, 3, 12, 13, 14, 15):
        return "b7"
    if r in (4, 5, 10, 11):
        return "b6"
    if r in (6, 9):
        return "b5"
    cc = c if r == 7 else 15 - c          # pair index via point symmetry
    if r == 8 and c == 0:
        return "term"
    if cc <= 7:
        return "b4"
    if cc <= 11:
        return "b3"
    if cc <= 13:
        return "b2"
    if cc == 14:
        return "b1"
    return "b0"                            # (7,15)


def box(lay, x1, y1, x2, y2):
    top.shapes(lay).insert(pya.DBox(x1, y1, x2, y2))


counts = {n: 0 for n in NETS}
for r in range(NROW):
    for c in range(NCOL):
        x, y = c * PITCH, row_y(r)
        top.insert(pya.DCellInstArray(cap_cell.cell_index(),
                                      pya.DTrans(pya.DVector(x, y))))
        counts[bit_of(r, c)] += 1

# ---- full-row Metal5 straps (b7/b6/b5) + left extension
FULLROW = {r: bit_of(r, 0) for r in range(NROW) if r not in (7, 8)}
rail_x = {n: -CH_L + i * RAIL_P for i, n in enumerate(NETS)}
for r, net in FULLROW.items():
    y = row_y(r) + CW / 2 - M5_STRAP / 2
    box(l_m5, rail_x[net] - 0.6, y, (NCOL - 1) * PITCH + CW, y + M5_STRAP)
    place_via(rail_x[net], y + M5_STRAP / 2, pad=1.0)

# ---- center-band stubs into the channel (Metal5 -> via -> Metal3 track)
chan_y0 = row_y(7) + CW + 1.6              # channel spans between rows 7 and 8
track_y = {n: chan_y0 + i * 1.6 for i, n in enumerate(["b4", "b3", "b2", "b1", "b0", "term"])}
for r in (7, 8):
    for c in range(NCOL):
        net = bit_of(r, c)
        x, y = c * PITCH, row_y(r)
        cx = x + 0.45 if r == 7 else x + 1.75   # stagger row-7 vs row-8 columns
        ty = track_y[net]
        if r == 7:
            box(l_m5, cx - 0.25, y + CW, cx + 0.25, ty + 0.3)
        else:
            box(l_m5, cx - 0.25, ty - 0.3, cx + 0.25, y)
        place_via(cx, ty, pad=0.36, cell=via_m2m5, pad_layers=[l_m2, l_m5])
# channel Metal2 horizontal tracks out to the left rails, dropping onto each rail
for n, ty in track_y.items():
    box(l_m2, rail_x[n] - 0.6, ty - 0.35, (NCOL - 1) * PITCH + CW, ty + 0.35)
    place_via(rail_x[n], ty, pad=0.8, cell=via_m2m3, pad_layers=[l_m2, l_m3])

# ---- vertical Metal3 net rails (left edge) + pins
y_top_pin = row_y(15) + CW + 3.0
for n in NETS:
    x = rail_x[n]
    box(l_m3, x - 0.6, -3.0, x + 0.6, y_top_pin)
    box(l_m3pin, x - 0.6, y_top_pin - 2.0, x + 0.6, y_top_pin)
    top.shapes(l_m3lbl).insert(pya.DText(n, pya.DTrans(pya.DVector(x, y_top_pin - 1.0))))

# ---- TopMetal1 top-plate straps + right spine + pin
spine_x = (NCOL - 1) * PITCH + CW + 2.0
for r in range(NROW):
    y = row_y(r) + CW / 2 - TM1_STRAP / 2
    box(l_tm1, 0, y, spine_x + TM1_STRAP, y + TM1_STRAP)
box(l_tm1, spine_x, 0, spine_x + TM1_STRAP, y_top_pin)
box(l_tm1pin, spine_x, y_top_pin - 3.0, spine_x + TM1_STRAP, y_top_pin)
top.shapes(l_tm1lbl).insert(pya.DText("topp", pya.DTrans(pya.DVector(spine_x + 1.0, y_top_pin - 1.5))))

layout.write("cdac_array.gds")
print("counts per net:", counts)
assert counts == {"b7": 128, "b6": 64, "b5": 32, "b4": 16, "b3": 8,
                  "b2": 4, "b1": 2, "b0": 1, "term": 1}, "unit budget broken!"
print("wrote cdac_array.gds")

# ---- matching LVS reference netlist
with open("cdac_array.ref.spice", "w") as f:
    f.write("* CDAC reference netlist (auto-generated)\n")
    f.write(".subckt cdac_array b7 b6 b5 b4 b3 b2 b1 b0 term topp\n")
    for n in NETS:
        f.write(f"C{n} topp {n} cap_cmim w=2.14u l=2.14u m={counts[n]}\n")
    f.write(".ends\n")
print("wrote cdac_array.ref.spice")
