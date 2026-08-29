#!/usr/bin/env python3
"""OA-SAR8 bootstrapped sampling switch layout (single-phase Abo-Gray).
Canonical mid-bar tap: via2 ON the bar + M3 stub in the bar's own y-band
escaping EAST past the bar end and the gate-tap pad, then an M2 riser OUTSIDE
the bar x-range (M2 risers must never cross bar bands on-layer).
Bands: out -1.2 | ckb 2.9 | g 3.7 | cb 4.5 | ct 5.3 | x 6.1 | vin 6.9."""
import pya

layout = pya.Layout()
layout.technology_name = "sg13g2"
layout.dbu = 0.001
import os
CELLNAME = os.environ.get("CELLNAME", "bstrap")
top = layout.create_cell(CELLNAME)
lib = pya.Library.library_by_name("SG13_dev", "sg13g2")

L = {}
for num, name in ((8, "m1"), (19, "v1"), (10, "m2"), (29, "v2"), (30, "m3"),
                  (67, "m5"), (126, "tm1")):
    L[name] = layout.layer(num, 0)
for num, tag in ((8, "m1"), (10, "m2"), (30, "m3")):
    L[tag + "p"], L[tag + "l"] = layout.layer(num, 2), layout.layer(num, 25)


def pcell(name, **pp):
    decl = lib.layout().pcell_declaration(name)
    params = {p.name: p.default for p in decl.get_parameters()}
    params.update(pp)
    return layout.create_cell(name, "SG13_dev", params)


CELLS = {
    "inpair": pcell("rfnmos", w="2.0u", l="0.15u", ng="2"),
    "xnmos":  pcell("rfnmos", w="4.0u", l="0.13u", ng="2"),
    "presw":  pcell("rfpmos", w="2.0u", l="0.13u", ng="1"),
}
T = {
    "inpair": dict(g=(0.76, 1.34, 0.96, 2.52), mid=(1.19, 1.79, 2.09, 2.07),
                   olo=(1.19, 1.26, 2.09, 1.54), otop=(1.19, 2.36, 2.09, 2.56),
                   grd=(0.03, 0.11, 3.25, 0.27), w=3.28),
    "xnmos":  dict(g=(0.76, 1.34, 0.96, 2.50), mid=(1.19, 1.78, 3.09, 2.06),
                   olo=(1.19, 1.26, 3.09, 1.54), otop=(1.19, 2.34, 3.09, 2.54),
                   grd=(0.03, 0.11, 4.25, 0.27), w=4.28),
    "presw":  dict(g=(1.04, 1.62, 1.24, 2.26), mid=(1.47, 1.54, 3.37, 1.82),
                   hi=(1.47, 2.06, 3.37, 2.34),
                   grd=(0.31, 0.39, 4.53, 0.55), w=4.84),
}
import os
CAPW = float(os.environ.get("CAPW", "0"))          # 0 = original 150 fF square; else explicit width (um) at l=9.94
CAP = pcell("cmim", Calculate="w&l", C="150f") if CAPW == 0 else pcell("cmim", Calculate="C", w=f"{CAPW}u", l="9.94u")
OUTGDS = os.environ.get("OUTGDS", CELLNAME + ".gds")


class Dev:
    def __init__(self, kind, x, y=0.0):
        self.kind, self.x, self.y, self.mir = kind, x, y, False
        top.insert(pya.DCellInstArray(CELLS[kind].cell_index(),
                                      pya.DTrans(pya.DVector(x, y))))

    def t(self, name):
        x1, y1, x2, y2 = T[self.kind][name]
        return pya.DBox(self.x + x1, self.y + y1, self.x + x2, self.y + y2)


def rect(lay, x1, y1, x2, y2):
    top.shapes(L[lay]).insert(pya.DBox(x1, y1, x2, y2))


def snap(v):
    return round(round(v * 100) / 100.0, 2)


def via1(x, y):
    x1, y1 = snap(x - 0.095), snap(y - 0.095)
    rect("v1", x1, y1, x1 + 0.19, y1 + 0.19)
    rect("m1", x - 0.2, y - 0.2, x + 0.2, y + 0.2)
    rect("m2", x - 0.2, y - 0.2, x + 0.2, y + 0.2)


def via2(x, y):
    x1, y1 = snap(x - 0.095), snap(y - 0.095)
    rect("v2", x1, y1, x1 + 0.19, y1 + 0.19)
    rect("m2", x - 0.2, y - 0.2, x + 0.2, y + 0.2)
    rect("m3", x - 0.2, y - 0.2, x + 0.2, y + 0.2)


def gate_tap(d):
    tt = T[d.kind]
    cl, cb_, cr, ct_ = tt["g"]
    w = tt["w"]
    fl, fr = w - cr, w - cl
    bars_r = tt["mid"][2]
    p1l, p2l = bars_r + 0.22, bars_r + 0.62
    ty = (cb_ + ct_) / 2 + d.y
    px1, px2, vx = d.x + p1l, d.x + p2l, d.x + (fl + fr) / 2
    rect("m1", px1, d.y + cb_, px2, d.y + ct_)
    rect("m2", px1, ty - 0.19, px2, ty + 0.19)
    rect("v1", vx - 0.095, ty - 0.095, vx + 0.095, ty + 0.095)
    return (px1 + px2) / 2, ty


def tie_outer(d):
    lo, hi = d.t("olo"), d.t("otop")
    xv1, xv2 = lo.left - 0.62, lo.left - 0.22
    rect("m2", xv1, lo.bottom, lo.left + 0.3, lo.top)
    rect("m2", xv1, hi.bottom, hi.left + 0.3, hi.top)
    rect("m2", xv1, lo.bottom, xv2, hi.top)
    return lo, hi, (xv1 + xv2) / 2


def vwire(x, y1, y2):
    rect("m2", x - 0.17, min(y1, y2), x + 0.17, max(y1, y2))


def mid_tap(d, bar="mid"):
    """Slim via2 on the bar (0.3-tall M2 pad clears the neighbor bars) + M3
    in-band stub escaping east past the gate pad + escape x for the riser."""
    b = d.t(bar)
    bars_r = T[d.kind]["mid"][2]
    ym = (b.bottom + b.top) / 2
    xb = (b.left + b.right) / 2
    xe = d.x + bars_r + 1.1
    x1, y1 = snap(xb - 0.095), snap(ym - 0.095)
    rect("v2", x1, y1, x1 + 0.19, y1 + 0.19)
    rect("m2", xb - 0.2, ym - 0.15, xb + 0.2, ym + 0.15)
    rect("m3", xb - 0.2, ym - 0.2, xe + 0.2, ym + 0.2)
    via2(xe, ym)
    return xe, ym


# ---------- placement (pitch 4.6 leaves escape corridors) ----------
mn_g = Dev("inpair", 0.0)
mn_cb = Dev("inpair", 4.6)
mn_c = Dev("inpair", 9.2)
mn_bt = Dev("inpair", 13.8)
msw = Dev("xnmos", 18.4)
mp_gt = Dev("presw", 24.0)
mp_ct = Dev("presw", 29.7)

XL, XR = -0.6, (48.9 if CAPW == 0 else 38.3 + CAPW + 0.7)
rect("m1", XL, -2.4, XR, -1.8)                    # VSS rail
rect("m1", XL, 7.4, XR, 8.0)                      # VDD rail

Y = dict(out=-1.2, ckb=2.9, g=3.7, cb=4.5, ct=5.3, x=6.1, vin=6.9)


def hband(name, x1, x2):
    y = Y[name]
    rect("m3", x1, y - 0.2, x2, y + 0.2)
    return y


# ---- VSS: MN_g + MN_cb outer ties drop onto the guard-ring strip
for d in (mn_g, mn_cb):
    lo, hi, xm = tie_outer(d)
    g = d.t("grd")
    ym = (g.bottom + g.top) / 2
    vwire(xm, ym - 0.15, lo.bottom + 0.1)
    rect("m1", xm - 0.2, ym - 0.15, xm + 0.2, ym + 0.15)
    rect("m2", xm - 0.2, ym - 0.15, xm + 0.2, ym + 0.15)
    rect("v1", snap(xm - 0.095), snap(ym - 0.095), snap(xm - 0.095) + 0.19,
         snap(ym - 0.095) + 0.19)
for d in (mn_g, mn_cb, mn_c, mn_bt, msw):
    g = d.t("grd")
    xl = g.left + 0.15
    rect("m1", xl, -1.8, xl + 0.3, g.bottom + 0.12)

# ---- ckb band: gates of MN_g, MN_cb, MP_gt
yck = hband("ckb", -0.4, 28.2)
for d in (mn_g, mn_cb, mp_gt):
    gx, gy = gate_tap(d)
    vwire(gx, gy, yck)
    via2(gx, yck)

# ---- g band: Msw gate + MN_bt gate + MP_ct gate + MN_c mid + MP_gt mid
yg = hband("g", -0.4, 34.1)   # west-extended: gb pin
for d in (msw, mn_bt, mp_ct):
    gx, gy = gate_tap(d)
    vwire(gx, gy, yg)
    via2(gx, yg)
for d in (mn_c, mp_gt):
    xe, ym = mid_tap(d)
    vwire(xe, ym, yg)
    via2(xe, yg)

# ---- cb band: MN_bt mid + MN_cb mid + cap bottom stack
ycb = hband("cb", 7.4, 37.4)
for d in (mn_bt, mn_cb):
    xe, ym = mid_tap(d)
    vwire(xe, ym, ycb)
    via2(xe, ycb)

# ---- ct band: MP_gt hi bar (tap from above: top bar, clean) + MP_ct mid +
# nwell ring taps + cap top stack
yct = hband("ct", 24.7, 37.4)
b = mp_gt.t("hi")
xm = (b.left + b.right) / 2
vwire(xm, b.top - 0.1, yct)
via2(xm, yct)
xe, ym = mid_tap(mp_ct)
vwire(xe, ym, yct)
via2(xe, yct)
for d in (mp_gt, mp_ct):
    g = d.t("grd")
    xw = g.left + 0.6
    ym = (g.bottom + g.top) / 2
    rect("m1", xw - 0.2, ym - 0.15, xw + 0.2, ym + 0.15)
    rect("v1", snap(xw - 0.095), snap(ym - 0.095),
         snap(xw - 0.095) + 0.19, snap(ym - 0.095) + 0.19)
    rect("m2", xw - 0.2, ym - 0.15, xw + 0.2, ym + 0.15)
    vwire(xw, ym, yct)
    via2(xw, yct)

# ---- VDD: MP_ct hi bar riser (top bar: clean above) + MN_c gate
b = mp_ct.t("hi")
xm = (b.left + b.right) / 2
vwire(xm, b.top - 0.1, 7.7)
via1(xm, 7.7)
gx, gy = gate_tap(mn_c)
vwire(gx, gy, 7.7)
via1(gx, 7.7)

# ---- x band: MN_c outer ties + MN_g mid (escape riser)
yx = hband("x", 2.8, 10.4)
lo, hi, xm = tie_outer(mn_c)
vwire(xm, lo.bottom + 0.2, yx)
via2(xm, yx)
xe, ym = mid_tap(mn_g)
vwire(xe, ym, yx)
via2(xe, yx)

# ---- vin band: MN_bt outers + Msw outers + pin
yv = hband("vin", -0.4, 19.6)
for d in (mn_bt, msw):
    lo, hi, xm = tie_outer(d)
    vwire(xm, lo.bottom + 0.2, yv)
    via2(xm, yv)
top.shapes(L["m3p"]).insert(pya.DBox(-0.4, yv - 0.2, 0.2, yv + 0.2))
top.shapes(L["m3l"]).insert(pya.DText("vin", pya.DTrans(pya.DVector(-0.1, yv))))

# ---- out band (south): Msw mid escape riser DOWN outside the bar range
yo = hband("out", -0.4, 23.2)
xe, ym = mid_tap(msw)
vwire(xe, yo, ym)
via2(xe, yo)
top.shapes(L["m3p"]).insert(pya.DBox(-0.4, yo - 0.2, 0.2, yo + 0.2))
top.shapes(L["m3l"]).insert(pya.DText("out", pya.DTrans(pya.DVector(-0.1, yo))))

# ---- boot cap east: bottom plate M5 -> M3/M5 stack on cb band;
# top plate TM1 bridge -> M2/TM1 stack -> ct band riser
cb_ = CAP.dbbox()
CX, CY = 38.3 - cb_.left, 2.6 - cb_.bottom
top.insert(pya.DCellInstArray(CAP.cell_index(), pya.DTrans(pya.DVector(CX, CY))))
cap = pya.DBox(cb_.left + CX, cb_.bottom + CY, cb_.right + CX, cb_.top + CY)


def stack(blayer, tlayer, x, y):
    decl = lib.layout().pcell_declaration("via_stack")
    params = {p.name: p.default for p in decl.get_parameters()}
    params.update({"b_layer": blayer, "t_layer": tlayer,
                   "vn_columns": 2, "vn_rows": 2})
    c = layout.create_cell("via_stack", "SG13_dev", params)
    bc = c.dbbox().center()
    top.insert(pya.DCellInstArray(c.cell_index(),
                                  pya.DTrans(pya.DVector(x - bc.x, y - bc.y))))


rect("m5", cap.left - 1.6, ycb - 0.5, cap.left + 0.2, ycb + 0.5)
stack("Metal3", "Metal5", cap.left - 1.1, ycb)
rect("tm1", cap.left - 2.9, 9.3, cap.right, 11.7)
stack("Metal2", "TopMetal1", cap.left - 1.6, 10.5)   # M5 pad clears the plate
vwire(cap.left - 1.6, yct, 10.5)
via2(cap.left - 1.6, yct)

# ---- gb pin (the boosted gate bus, west end of the g band)
top.shapes(L["m3p"]).insert(pya.DBox(-0.4, yg - 0.2, 0.2, yg + 0.2))
top.shapes(L["m3l"]).insert(pya.DText("gb", pya.DTrans(pya.DVector(-0.1, yg))))

# ---- ckb pin (west) + VDD/VSS pins
top.shapes(L["m3p"]).insert(pya.DBox(-0.4, yck - 0.2, 0.2, yck + 0.2))
top.shapes(L["m3l"]).insert(pya.DText("ckb", pya.DTrans(pya.DVector(-0.1, yck))))
top.shapes(L["m1p"]).insert(pya.DBox(XL, -2.3, XL + 0.8, -1.9))
top.shapes(L["m1l"]).insert(pya.DText("VSS", pya.DTrans(pya.DVector(XL + 0.4, -2.1))))
top.shapes(L["m1p"]).insert(pya.DBox(XL, 7.5, XL + 0.8, 7.9))
top.shapes(L["m1l"]).insert(pya.DText("VDD", pya.DTrans(pya.DVector(XL + 0.4, 7.7))))

layout.write(OUTGDS)
print("wrote", OUTGDS, "bbox:", top.dbbox(), "cap", CAP.dbbox())

with open(OUTGDS.replace(".gds", ".cdl"), "w") as f:
    f.write(f"""* bootstrapped sampling switch reference
.subckt {CELLNAME} vin out ckb gb VDD VSS
Msw  out gb  vin VSS sg13_lv_nmos w=4.0u l=0.13u rfmode=1
MN_c gb  VDD x   VSS sg13_lv_nmos w=2.0u l=0.15u rfmode=1
MN_g x   ckb VSS VSS sg13_lv_nmos w=2.0u l=0.15u rfmode=1
MN_cb cb ckb VSS VSS sg13_lv_nmos w=2.0u l=0.15u rfmode=1
MP_ct ct gb  VDD ct  sg13_lv_pmos w=2.0u l=0.13u rfmode=1
MN_bt cb gb  vin VSS sg13_lv_nmos w=2.0u l=0.15u rfmode=1
MP_gt gb ckb ct  ct  sg13_lv_pmos w=2.0u l=0.13u rfmode=1
Cb   ct  cb  cap_cmim w={CAPW if CAPW else 9.94}u l=9.94u
.ends
""")
print("wrote bstrap.cdl")
