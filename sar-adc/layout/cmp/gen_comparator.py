#!/usr/bin/env python3
"""OA-SAR8 StrongARM comparator layout v3: RF pcells, M2-native wiring.

Key facts (decoded empirically): every S/D bar of the RF cells already carries
M2 with internal vias -- NEVER add vias on bars (V1.b space 0.22 vs internal
vias). Gate columns are M1-only: one via1 each. Rails: VDD/VSS on M1, CLK M2.
"""
import pya

layout = pya.Layout()
layout.technology_name = "sg13g2"
layout.dbu = 0.001
top = layout.create_cell("sa_comp")
lib = pya.Library.library_by_name("SG13_dev", "sg13g2")

L = {}
for num, name in ((8, "m1"), (19, "v1"), (10, "m2"), (29, "v2"), (30, "m3")):
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
    "tail":   pcell("rfnmos", w="3.0u", l="0.3u",  ng="2"),
    "xpmos":  pcell("rfpmos", w="6.0u", l="0.13u", ng="2"),
    "presw":  pcell("rfpmos", w="2.0u", l="0.13u", ng="1"),
}
T = {
    "inpair": dict(g=(0.76, 1.34, 0.96, 2.52), mid=(1.19, 1.79, 2.09, 2.07),
                   olo=(1.19, 1.26, 2.09, 1.54), otop=(1.19, 2.36, 2.09, 2.56),
                   grd=(0.03, 0.11, 3.25, 0.27), w=3.28),
    "xnmos":  dict(g=(0.76, 1.34, 0.96, 2.50), mid=(1.19, 1.78, 3.09, 2.06),
                   olo=(1.19, 1.26, 3.09, 1.54), otop=(1.19, 2.34, 3.09, 2.54),
                   grd=(0.03, 0.11, 4.25, 0.27), w=4.28),
    "tail":   dict(g=(0.76, 1.34, 0.96, 2.82), mid=(1.19, 1.94, 2.59, 2.22),
                   olo=(1.19, 1.26, 2.59, 1.54), otop=(1.19, 2.66, 2.59, 2.86),
                   grd=(0.03, 0.11, 3.75, 0.27), w=3.78),
    "xpmos":  dict(g=(1.04, 1.62, 1.24, 2.78), mid=(1.47, 2.06, 4.37, 2.34),
                   olo=(1.47, 1.54, 4.37, 1.82), otop=(1.47, 2.62, 4.37, 2.82),
                   grd=(0.31, 0.39, 5.53, 0.55), w=5.84),
    "presw":  dict(g=(1.04, 1.62, 1.24, 2.26), mid=(1.47, 1.54, 3.37, 1.82),
                   hi=(1.47, 2.06, 3.37, 2.34),
                   grd=(0.31, 0.39, 4.53, 0.55), w=4.84),
}


class Dev:
    def __init__(self, kind, x, y, mirror=False):
        self.kind, self.x, self.y, self.mir = kind, x, y, mirror
        tr = pya.DTrans(2, True, pya.DVector(x, y)) if mirror else \
             pya.DTrans(pya.DVector(x, y))
        top.insert(pya.DCellInstArray(CELLS[kind].cell_index(), tr))

    def t(self, name):
        x1, y1, x2, y2 = T[self.kind][name]
        if self.mir:
            return pya.DBox(self.x - x2, self.y + y1, self.x - x1, self.y + y2)
        return pya.DBox(self.x + x1, self.y + y1, self.x + x2, self.y + y2)

    def tc(self, name):
        b = self.t(name)
        return (b.left + b.right) / 2, (b.bottom + b.top) / 2


def rect(lay, x1, y1, x2, y2):
    top.shapes(L[lay]).insert(pya.DBox(x1, y1, x2, y2))


def snap(v):
    return round(round(v * 100) / 100.0, 2)


def via1(x, y):
    x1, y1 = snap(x - 0.095), snap(y - 0.095)
    rect("v1", x1, y1, x1 + 0.19, y1 + 0.19)
    rect("m1", x - 0.2, y - 0.2, x + 0.2, y + 0.2)
    rect("m2", x - 0.2, y - 0.2, x + 0.2, y + 0.2)


def gate_tap(d, y=None):
    """Tap the gate at the ring's FAR leg (mirror of the pinned column):
    local x = [w-cr, w-cl]. That side has >=0.22 clearance to the bars and
    to the guard ring, verified per variant. Returns (x, y) on M2."""
    tt = T[d.kind]
    cl, cb, cr, ct = tt["g"]
    w = tt["w"]
    fl, fr = w - cr, w - cl          # far leg local x
    bars_r = tt["mid"][2]
    p1l = bars_r + 0.22              # pad local x-range
    p2l = p1l + 0.40
    vxl = (fl + fr) / 2
    ty = y if y is not None else (cb + ct) / 2 + d.y
    if not d.mir:
        px1, px2, vx = d.x + p1l, d.x + p2l, d.x + vxl
    else:
        px1, px2, vx = d.x - p2l, d.x - p1l, d.x - vxl
    rect("m1", px1, d.y + cb, px2, d.y + ct)       # full col height: engulf the leg
    rect("m2", px1, ty - 0.19, px2, ty + 0.19)     # narrow: clear the tie arms
    rect("v1", vx - 0.095, ty - 0.095, vx + 0.095, ty + 0.095)
    return (px1 + px2) / 2, ty


def via2(x, y):
    x1, y1 = snap(x - 0.095), snap(y - 0.095)
    rect("v2", x1, y1, x1 + 0.19, y1 + 0.19)
    rect("m2", x - 0.2, y - 0.2, x + 0.2, y + 0.2)
    rect("m3", x - 0.2, y - 0.2, x + 0.2, y + 0.2)


def tie_outer(d, side="gate"):
    """L-tie: extend olo+otop beyond the bar end, join with a vertical clear of
    the mid bar (same-layer crossing was shorting S to D)."""
    lo, hi = d.t("olo"), d.t("otop")
    bar_side = (side == "bar")
    if (not d.mir) != bar_side:
        xv1, xv2 = lo.left - 0.62, lo.left - 0.22
        rect("m2", xv1, lo.bottom, lo.left + 0.3, lo.top)
        rect("m2", xv1, hi.bottom, hi.left + 0.3, hi.top)
    else:
        xv1, xv2 = lo.right + 0.22, lo.right + 0.62
        rect("m2", lo.right - 0.3, lo.bottom, xv2, lo.top)
        rect("m2", hi.right - 0.3, hi.bottom, xv2, hi.top)
    rect("m2", xv1, lo.bottom, xv2, hi.top)
    xm = (xv1 + xv2) / 2
    return lo, hi, xm


# ---------- placement (mirror-symmetric about x=0) ----------
tail = Dev("tail", -T["tail"]["w"] / 2, 0)
m1d = Dev("inpair", -8.2, 6.6)
m2d = Dev("inpair", 8.2, 6.6, mirror=True)
m3d = Dev("xnmos", -9.2, 12.6)
m4d = Dev("xnmos", 9.2, 12.6, mirror=True)
m5d = Dev("xpmos", -10.2, 19.6)
m6d = Dev("xpmos", 10.2, 19.6, mirror=True)
s1d = Dev("presw", -17.6, 19.6)
s2d = Dev("presw", 17.6, 19.6, mirror=True)
s3d = Dev("presw", -24.2, 19.6)
s4d = Dev("presw", 24.2, 19.6, mirror=True)

XL, XR = -30.0, 30.0
rect("m1", XL, -2.4, XR, -1.8)                    # VSS rail
rect("m1", XL, 25.2, XR, 25.8)                    # VDD rail

# LAYER DISCIPLINE: M2 = verticals only; M3 = horizontals only (distinct y bands)
#   tail bridge y=2.0 | clk y=3.9 | pq-low y=7.4 | outn y=16.2 | outp y=17.0 | pq-high y=17.9
def hbus(y, x1, x2):
    rect("m3", x1, y, x2, y + 0.4)
    return y + 0.2

def vwire(x, y1, y2):
    rect("m2", x - 0.2, min(y1, y2), x + 0.2, max(y1, y2))

# --- VSS: tail source tie -> M2 drop -> via1 -> rail; guard legs (M1)
_, _, txm = tie_outer(tail)
vwire(txm, -1.95, tail.t("olo").bottom + 0.1)
via1(txm, -1.9)
for d in (tail, m1d, m2d, m3d, m4d):
    g = d.t("grd")
    xl = g.right - 0.45 if (d is tail or d.mir) else g.left + 0.15
    rect("m1", xl, -1.8, xl + 0.3, g.bottom + 0.12)

# --- VDD: xpmos ties + presw hi bars -> M2 risers -> via1 -> rail; guards
for d in (m5d, m6d):
    lo, hi, xm = tie_outer(d)
    vwire(xm, hi.top - 0.1, 25.45)
    via1(xm, 25.45)
for d in (s1d, s2d, s3d, s4d):
    hb = d.t("hi")
    xm = (hb.left + hb.right) / 2
    vwire(xm, hb.top - 0.1, 25.45)
    via1(xm, 25.45)
for d in (m5d, m6d, s1d, s2d, s3d, s4d):
    g = d.t("grd")
    xl = (g.left + 0.15) if not d.mir else (g.right - 0.45)
    rect("m1", xl, g.bottom + 0.05, xl + 0.3, 25.2)

# --- CLK bus (M3 @3.9): tail tap + 4 precharge taps, M2 verticals + via2
yclk = hbus(3.9, XL + 0.3, 26.5)
tgx, tgy = gate_tap(tail)                          # pad y ~1.89-2.27, x ~0.92-1.32
vwire(tgx, tgy, yclk)
via2(tgx, yclk)
for d in (s1d, s2d, s3d, s4d):
    gx, gy = gate_tap(d)
    vwire(gx, yclk, gy)
    via2(gx, yclk)

# --- tail node bus (M3 @2.0): tail D(mid) + both input-pair S ties
ytn = hbus(2.0, -6.2, 6.2)
tdx = (tail.t("mid").left + tail.t("mid").right) / 2
vwire(tdx, ytn, tail.t("mid").top - 0.1)
via2(tdx, ytn)
for d in (m1d, m2d):
    lo, hi, xm = tie_outer(d, side="bar")          # inpair: bar side (col side hosts the input pin)
    vwire(xm, ytn, lo.bottom + 0.2)
    via2(xm, ytn)

# --- p/q: input D(mid) -> low bus (M3 @7.4) -> xnmos S tie; tie -> high bus
# (M3 @17.9) -> presw D(mid)
for inp, xn, sw, xoff in ((m1d, m3d, s1d, -1), (m2d, m4d, s2d, +1)):
    dm = inp.t("mid")
    xdm = (dm.left + dm.right) / 2
    lo, hi, xs = tie_outer(xn)
    ylow = hbus(7.4, min(xdm, xs) - 0.3, max(xdm, xs) + 0.3)
    ymb = (dm.bottom + dm.top) / 2 - 0.18
    rect("m3", min(xdm, xs) - 0.2, ymb, max(xdm, xs) + 0.2, ymb + 0.4)
    via2(xdm, ymb + 0.2)
    via2(xs, ymb + 0.2)                  # lands on the tie vertical (spans ylow..bars)
    vwire(xs, ylow, lo.bottom + 0.2)
    via2(xs, ylow)
    swd = sw.t("mid")
    xsw = (swd.left + swd.right) / 2
    yh = hbus(17.9, min(xs, xsw) - 0.3, max(xs, xsw) + 0.3)
    vwire(xs, hi.top - 0.2, yh)
    via2(xs, yh)
    vwire(xsw, yh, swd.bottom + 0.2)
    via2(xsw, yh)

# --- outn (M3 @16.2) / outp (M3 @17.0) with cross-coupled gates
def out_net(xn, xp, sw, og_n, og_p, ymid, spine_x):
    xs_all = [spine_x]
    # nmos mid: M3 stub in the bar own y-band + via2 on bar; spine carries it up
    bn = xn.t("mid")
    xxn = (bn.left + bn.right) / 2
    ybn = (bn.bottom + bn.top) / 2 - 0.2
    rect("m3", min(spine_x, xxn) - 0.2, ybn, max(spine_x, xxn) + 0.2, ybn + 0.4)
    via2(xxn, ybn + 0.2)
    via2(spine_x, ybn + 0.2)
    # pmos mid: same treatment in its own band
    bp = xp.t("mid")
    xxp = (bp.left + bp.right) / 2
    ybp = (bp.bottom + bp.top) / 2 - 0.2
    rect("m3", min(spine_x, xxp) - 0.2, ybp, max(spine_x, xxp) + 0.2, ybp + 0.4)
    via2(xxp, ybp + 0.2)
    via2(spine_x, ybp + 0.2)
    # spine vertical M2 linking nmos band, main band, pmos band
    vwire(spine_x, ybn + 0.2, ybp + 0.2)
    via2(spine_x, ymid + 0.2)
    # precharge switch mid: clean from below
    bs = sw.t("mid")
    xxs = (bs.left + bs.right) / 2
    vwire(xxs, ymid, bs.bottom + 0.2)
    via2(xxs, ymid + 0.2)
    xs_all.append(xxs)
    # cross-coupled gates
    gtaps = []
    for g in (og_n, og_p):
        gx, gy = gate_tap(g)
        vwire(gx, ymid, gy)
        gtaps.append(gx)
        xs_all.append(gx)
    if abs(gtaps[0] - gtaps[1]) < 0.6:
        gmid = sum(gtaps) / 2
        rect("m2", min(gtaps) - 0.2, ymid, max(gtaps) + 0.2, ymid + 0.4)
        via2(gmid, ymid + 0.2)
    else:
        for gx in gtaps:
            via2(gx, ymid + 0.2)
    rect("m3", min(xs_all) - 0.3, ymid, max(xs_all) + 0.3, ymid + 0.4)
    return ymid

out_net(m3d, m5d, s3d, m4d, m6d, 16.2, -9.77)
out_net(m4d, m6d, s4d, m3d, m5d, 17.0, 9.77)

# --- input pins: via1 on gate col (M2 pad clear of bars), M2 down, pin @M2
for d, name in ((m1d, "inp"), (m2d, "inn")):
    g = d.t("g")
    if not d.mir:
        px1, px2 = g.left - 0.14, g.left + 0.20
        vx = g.left + 0.04
    else:
        px1, px2 = g.right - 0.20, g.right + 0.14
        vx = g.right - 0.04
    gyc = d.y + 1.95
    rect("m1", px1, gyc - 0.19, px2, gyc + 0.19)
    rect("m2", px1, gyc - 0.19, px2, gyc + 0.19)
    rect("v1", vx - 0.095, gyc - 0.095, vx + 0.095, gyc + 0.095)
    xpin = (px1 + px2) / 2
    rect("m2", xpin - 0.17, 5.0, xpin + 0.17, gyc)
    top.shapes(L["m2p"]).insert(pya.DBox(xpin - 0.17, 5.0, xpin + 0.17, 5.6))
    top.shapes(L["m2l"]).insert(pya.DText(name, pya.DTrans(pya.DVector(xpin, 5.3))))

# --- pins
top.shapes(L["m3p"]).insert(pya.DBox(-12.0, 16.2, -11.0, 16.6))
top.shapes(L["m3l"]).insert(pya.DText("outn", pya.DTrans(pya.DVector(-11.5, 16.4))))
top.shapes(L["m3p"]).insert(pya.DBox(11.0, 17.0, 12.0, 17.4))
top.shapes(L["m3l"]).insert(pya.DText("outp", pya.DTrans(pya.DVector(11.5, 17.2))))
top.shapes(L["m1p"]).insert(pya.DBox(XL, -2.3, XL + 1.0, -1.9))
top.shapes(L["m1l"]).insert(pya.DText("VSS", pya.DTrans(pya.DVector(XL + 0.5, -2.1))))
top.shapes(L["m1p"]).insert(pya.DBox(XL, 25.3, XL + 1.0, 25.7))
top.shapes(L["m1l"]).insert(pya.DText("VDD", pya.DTrans(pya.DVector(XL + 0.5, 25.5))))
top.shapes(L["m3p"]).insert(pya.DBox(XL + 0.3, 3.9, XL + 1.3, 4.3))
top.shapes(L["m3l"]).insert(pya.DText("clk", pya.DTrans(pya.DVector(XL + 0.8, 4.1))))

layout.write("sa_comp.gds")
print("wrote sa_comp.gds bbox:", top.dbbox())

with open("sa_comp.cdl", "w") as f:
    f.write("""* StrongARM comparator reference
.subckt sa_comp inp inn clk outp outn VDD VSS
M1 p inp tail VSS sg13_lv_nmos w=2.0u l=0.15u rfmode=1
M2 q inn tail VSS sg13_lv_nmos w=2.0u l=0.15u rfmode=1
M3 outn outp p VSS sg13_lv_nmos w=4.0u l=0.13u rfmode=1
M4 outp outn q VSS sg13_lv_nmos w=4.0u l=0.13u rfmode=1
MT tail clk VSS VSS sg13_lv_nmos w=3.0u l=0.3u rfmode=1
M5 outn outp VDD VDD sg13_lv_pmos w=6.0u l=0.13u rfmode=1
M6 outp outn VDD VDD sg13_lv_pmos w=6.0u l=0.13u rfmode=1
MS1 p clk VDD VDD sg13_lv_pmos w=2.0u l=0.13u rfmode=1
MS2 q clk VDD VDD sg13_lv_pmos w=2.0u l=0.13u rfmode=1
MS3 outn clk VDD VDD sg13_lv_pmos w=2.0u l=0.13u rfmode=1
MS4 outp clk VDD VDD sg13_lv_pmos w=2.0u l=0.13u rfmode=1
.ends
""")
print("wrote sa_comp.cdl")
