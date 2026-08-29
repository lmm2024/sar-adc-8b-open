#!/usr/bin/env python3
"""OA-SAR8 bottom-plate switch bitcell: VREF/GND driver (inverter) + VIN
transmission gate. Same layer discipline as the comparator: M2 vertical,
M3 horizontal, gate taps at ring far legs, no vias on device bars."""
import os
import pya

layout = pya.Layout()
layout.technology_name = "sg13g2"
layout.dbu = 0.001
CELLNAME = os.environ.get("CELLNAME", "sw_tg")
NTG_W = float(os.environ.get("NTG_W", "2.0"))
PTG_W = float(os.environ.get("PTG_W", "4.0"))
OUTGDS = os.environ.get("OUTGDS", CELLNAME + ".gds")
top = layout.create_cell(CELLNAME)
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
    "nsw": pcell("rfnmos", w=f"{NTG_W}u", l="0.13u", ng="2"),
    "psw": pcell("rfpmos", w=f"{PTG_W}u", l="0.13u", ng="2"),
}
NU = NTG_W / 2.0
PU = PTG_W / 2.0
T = {
    "nsw": dict(g=(0.76, 1.34, 0.96, 2.50), mid=(1.19, 1.78, 1.09 + NU, 2.06),
                olo=(1.19, 1.26, 1.09 + NU, 1.54), otop=(1.19, 2.34, 1.09 + NU, 2.54),
                grd=(0.03, 0.11, 2.25 + NU, 0.27), w=2.28 + NU),
    "psw": dict(g=(1.04, 1.62, 1.24, 2.78), mid=(1.47, 2.06, 1.37 + PU, 2.34),
                olo=(1.47, 1.54, 1.37 + PU, 1.82), otop=(1.47, 2.62, 1.37 + PU, 2.82),
                grd=(0.31, 0.39, 2.53 + PU, 0.55), w=2.84 + PU),
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


# ---- devices: TG only
# Align both halves so their VIN and BOT routing channels remain separated
# after increasing the TG to W2.5/W5.
nt = Dev("nsw", 7.0, 0)
pt = Dev("psw", 7.0, 7.0)

XL = -1.2
XR = max(nt.x + T["nsw"]["w"], pt.x + T["psw"]["w"]) + 0.5
BUS_R = XR - 0.2
rect("m1", XL, -2.2, XR, -1.6)      # VSS
rect("m1", XL, 12.4, XR, 13.0)      # VDD(=VREF)

# driver: pd.S->VDD, nd.S->VSS (ties), drains joined = bot; gates joined = ctl
# tg bulks: nt guard->VSS, pt guard->VDD via guard legs
g = nt.t("grd")
rect("m1", g.left + 0.15, -1.6, g.left + 0.45, g.bottom + 0.12)
g = pt.t("grd")
rect("m1", g.left + 0.15, g.bottom + 0.05, g.left + 0.45, 12.4)
# tg source side: nt/pt "olo+otop tie" = vin side
_, _, xvin_n = tie_outer(nt)
_, _, xvin_p = tie_outer(pt)
# ---- M3 buses: bot y=5.3 | vin y=4.5 | ctl y=3.7 | trk y=5.9(M3? use 6.1) trkb y=2.9
hbus(5.3, -1.0, BUS_R)   # bot
hbus(4.5, -1.0, BUS_R)   # vin
hbus(2.9, -1.0, BUS_R)   # trkb (pmos tg gate)
hbus(6.1, -1.0, BUS_R)   # trk  (nmos tg gate)

# bot: nd.mid, pd.mid, nt.mid, pt.mid all to bot bus
for d, xr in ((nt, BUS_R - 0.3),):
    b = d.t("mid")
    xx = (b.left + b.right) / 2
    yc = 1.94
    rect("m3", xx - 0.2, yc - 0.19, xr + 0.2, yc + 0.19)
    via2(xx, yc, ph=0.19)
    vwire(xr, yc, 5.5)
    via2(xr, yc, ph=0.19)
    via2(xr, 5.5)
# Share the right-hand BOT drop; routing through the p-device body can touch
# its internal gate contact and short BOT to TRKB.
for d, xr in ((pt, BUS_R - 0.3),):
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
xe = xvin_p - 1.0
rect("m2", xe - 0.2, 8.54, xvin_p + 0.2, 8.74)
vwire(xe, 4.5, 8.74)
via2(xe, 4.7)
# trk: nt gate ; trkb: pt gate
gx, gy = gate_tap(nt)
vwire(gx, 6.3, gy)
via2(gx, 6.3)
gx, gy = gate_tap(pt)
vwire(gx, 3.1, gy)
via2(gx, 3.1)

# pins
pins = (("bot", 5.3), ("vin", 4.5), ("trkb", 2.9), ("trk", 6.1))
for name, y in pins:
    top.shapes(L["m3p"]).insert(pya.DBox(-1.0, y, -0.4, y + 0.4))
    top.shapes(L["m3l"]).insert(pya.DText(name, pya.DTrans(pya.DVector(-0.7, y + 0.2))))
top.shapes(L["m1p"]).insert(pya.DBox(XL, -2.1, XL + 0.8, -1.7))
top.shapes(L["m1l"]).insert(pya.DText("VSS", pya.DTrans(pya.DVector(XL + 0.4, -1.9))))
top.shapes(L["m1p"]).insert(pya.DBox(XL, 12.5, XL + 0.8, 12.9))
top.shapes(L["m1l"]).insert(pya.DText("VDD", pya.DTrans(pya.DVector(XL + 0.4, 12.7))))

layout.write(OUTGDS)
print("wrote", OUTGDS, "bbox:", top.dbbox())

OUTCDL = OUTGDS.replace(".gds", ".cdl")
with open(OUTCDL, "w") as f:
    f.write(f"""* parameterized plain transmission gate
.subckt {CELLNAME} bot vin trk trkb VDD VSS
MNT bot trk vin VSS sg13_lv_nmos w={NTG_W}u l=0.13u rfmode=1
MPT bot trkb vin VDD sg13_lv_pmos w={PTG_W}u l=0.13u rfmode=1
.ends
""")
print("wrote", OUTCDL, "TG", NTG_W, PTG_W)
