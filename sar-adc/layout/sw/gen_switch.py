#!/usr/bin/env python3
"""OA-SAR8 bottom-plate switch bitcell: VREF/GND driver (inverter) + VIN
transmission gate. Same layer discipline as the comparator: M2 vertical,
M3 horizontal, gate taps at ring far legs, no vias on device bars."""
import pya

layout = pya.Layout()
layout.technology_name = "sg13g2"
layout.dbu = 0.001
top = layout.create_cell("sw_bitcell")
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
    "nsw": pcell("rfnmos", w="2.0u", l="0.13u", ng="2"),
    "psw": pcell("rfpmos", w="4.0u", l="0.13u", ng="2"),
}
T = {
    "nsw": dict(g=(0.76, 1.34, 0.96, 2.50), mid=(1.19, 1.78, 2.09, 2.06),
                olo=(1.19, 1.26, 2.09, 1.54), otop=(1.19, 2.34, 2.09, 2.54),
                grd=(0.03, 0.11, 3.25, 0.27), w=3.28),
    "psw": dict(g=(1.04, 1.62, 1.24, 2.78), mid=(1.47, 2.06, 3.37, 2.34),
                olo=(1.47, 1.54, 3.37, 1.82), otop=(1.47, 2.62, 3.37, 2.82),
                grd=(0.31, 0.39, 4.53, 0.55), w=4.84),
}


class Dev:
    def __init__(self, kind, x, y):
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


def via2(x, y, ph=0.2):
    x1, y1 = snap(x - 0.095), snap(y - 0.095)
    rect("v2", x1, y1, x1 + 0.19, y1 + 0.19)
    rect("m2", x - 0.2, y - ph, x + 0.2, y + ph)
    rect("m3", x - 0.2, y - ph, x + 0.2, y + ph)


def tie_outer(d):
    lo, hi = d.t("olo"), d.t("otop")
    xv1, xv2 = lo.left - 0.62, lo.left - 0.22
    rect("m2", xv1, lo.bottom, lo.left + 0.1, lo.top)
    rect("m2", xv1, hi.bottom, hi.left + 0.1, hi.top)
    rect("m2", xv1, lo.bottom, xv2, hi.top)
    return lo, hi, (xv1 + xv2) / 2


def gate_tap(d, y=None):
    tt = T[d.kind]
    cl, cb, cr, ct = tt["g"]
    w = tt["w"]
    fl, fr = w - cr, w - cl
    p1l = tt["mid"][2] + 0.22
    p2l = p1l + 0.40
    ty = y if y is not None else (cb + ct) / 2 + d.y
    px1, px2, vx = d.x + p1l, d.x + p2l, d.x + (fl + fr) / 2
    rect("m1", px1, d.y + cb, px2, d.y + ct)
    rect("m2", px1, ty - 0.19, px2, ty + 0.19)
    x1, y1 = snap(vx - 0.095), snap(ty - 0.095)
    rect("v1", x1, y1, x1 + 0.19, y1 + 0.19)
    return (px1 + px2) / 2, ty


def vwire(x, y1, y2):
    rect("m2", x - 0.2, min(y1, y2), x + 0.2, max(y1, y2))


def hbus(y, x1, x2):
    rect("m3", x1, y, x2, y + 0.4)


# ---- devices: nmos row (driver-n, tg-n), pmos row (driver-p, tg-p)
nd = Dev("nsw", 0.5, 0)
nt = Dev("nsw", 7.0, 0)
pd = Dev("psw", 0.0, 7.0)
pt = Dev("psw", 6.6, 7.0)

XL, XR = -1.2, 12.4
rect("m1", XL, -2.2, XR, -1.6)      # VSS
rect("m1", XL, 12.4, XR, 13.0)      # VDD(=VREF)

# driver: pd.S->VDD, nd.S->VSS (ties), drains joined = bot; gates joined = ctl
for d, rail_y, updown in ((nd, -1.6, -1), (pd, 12.55, +1)):
    lo, hi, xm = tie_outer(d)
    if updown < 0:
        vwire(xm, -1.9, lo.bottom + 0.2)
        via1(xm, -1.85)
    else:
        vwire(xm, hi.top - 0.2, 12.7)
        via1(xm, 12.65)
# tg bulks: nt guard->VSS, pt guard->VDD via guard legs
for d, y1, y2 in ((nd, -1.6, None), (nt, -1.6, None)):
    g = d.t("grd")
    rect("m1", g.left + 0.15, -1.6, g.left + 0.45, g.bottom + 0.12)
for d in (pd, pt):
    g = d.t("grd")
    rect("m1", g.left + 0.15, g.bottom + 0.05, g.left + 0.45, 12.4)
# tg source side: nt/pt "olo+otop tie" = vin side
_, _, xvin_n = tie_outer(nt)
_, _, xvin_p = tie_outer(pt)
# ---- M3 buses: bot y=5.3 | vin y=4.5 | ctl y=3.7 | trk y=5.9(M3? use 6.1) trkb y=2.9
hbus(5.3, -1.0, 12.2)   # bot
hbus(4.5, -1.0, 12.2)   # vin
hbus(3.7, -1.0, 12.2)   # ctl
hbus(2.9, -1.0, 12.2)   # trkb (pmos tg gate)
hbus(6.1, -1.0, 12.2)   # trk  (nmos tg gate)

# bot: nd.mid, pd.mid, nt.mid, pt.mid all to bot bus
for d, xr in ((nd, 5.9), (nt, 11.9)):
    b = d.t("mid")
    xx = (b.left + b.right) / 2
    yc = 1.94
    rect("m3", xx - 0.2, yc - 0.19, xr + 0.2, yc + 0.19)
    via2(xx, yc, ph=0.19)
    vwire(xr, yc, 5.5)
    via2(xr, yc, ph=0.19)
    via2(xr, 5.5)
for d, xr in ((pd, 4.82), (pt, 11.05)):
    b = d.t("mid")
    xx = (b.left + b.right) / 2
    yc = 9.22
    rect("m3", xx - 0.2, yc - 0.19, xr + 0.2, yc + 0.19)
    via2(xx, yc, ph=0.19)
    vwire(xr, 5.5, yc)
    via2(xr, yc, ph=0.19)
    via2(xr, 5.5)
# vin: nt tie down to the bus; pt tie via an elbow (offset x, avoid via merge)
vwire(xvin_n, 2.4, 4.9)
via2(xvin_n, 4.7)
xe = xvin_p - 0.6
rect("m2", xe - 0.2, 8.54, xvin_p + 0.2, 8.74)
vwire(xe, 4.5, 8.74)
via2(xe, 4.7)
# ctl: nd + pd gates
for d in (nd, pd):
    gx, gy = gate_tap(d)
    vwire(gx, 3.9, gy)
    via2(gx, 3.9)
# trk: nt gate ; trkb: pt gate
gx, gy = gate_tap(nt)
vwire(gx, 6.3, gy)
via2(gx, 6.3)
gx, gy = gate_tap(pt)
vwire(gx, 3.1, gy)
via2(gx, 3.1)

# pins
pins = (("bot", 5.3), ("vin", 4.5), ("ctl", 3.7), ("trkb", 2.9), ("trk", 6.1))
for name, y in pins:
    top.shapes(L["m3p"]).insert(pya.DBox(-1.0, y, -0.4, y + 0.4))
    top.shapes(L["m3l"]).insert(pya.DText(name, pya.DTrans(pya.DVector(-0.7, y + 0.2))))
top.shapes(L["m1p"]).insert(pya.DBox(XL, -2.1, XL + 0.8, -1.7))
top.shapes(L["m1l"]).insert(pya.DText("VSS", pya.DTrans(pya.DVector(XL + 0.4, -1.9))))
top.shapes(L["m1p"]).insert(pya.DBox(XL, 12.5, XL + 0.8, 12.9))
top.shapes(L["m1l"]).insert(pya.DText("VDD", pya.DTrans(pya.DVector(XL + 0.4, 12.7))))

layout.write("sw_bitcell.gds")
print("wrote sw_bitcell.gds bbox:", top.dbbox())

with open("sw_bitcell.cdl", "w") as f:
    f.write("""* bottom-plate driver + vin TG
.subckt sw_bitcell bot vin ctl trk trkb VDD VSS
MND bot ctl VSS VSS sg13_lv_nmos w=2.0u l=0.13u rfmode=1
MPD bot ctl VDD VDD sg13_lv_pmos w=4.0u l=0.13u rfmode=1
MNT bot trk vin VSS sg13_lv_nmos w=2.0u l=0.13u rfmode=1
MPT bot trkb vin VDD sg13_lv_pmos w=4.0u l=0.13u rfmode=1
.ends
""")
print("wrote sw_bitcell.cdl")
