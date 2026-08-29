#!/usr/bin/env python3
"""StrongARM fast characterization: waveform plot + deterministic noise estimate.

sigma_n = sqrt(4*k*T*gamma / (gm*Tint)) with gm*Tint = A_int * Cpq.
A_int and Tint are measured from the clean transient; Cpq is a stated estimate.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = ["Droid Sans Fallback", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

SURF, INK, INK2 = "#fcfcfb", "#0b0b0b", "#52514e"
BLUE, ORANGE, RED = "#2a78d6", "#eb6834", "#b3261e"

KT = 1.380649e-23 * 300
GAMMA = 1.0          # conservative for short-channel
CPQ = 20e-15         # estimated cap at P/Q (Cgs(M3)+Cdb(M1)+Cdb(S1)+wire), first cut
DV = 2e-3            # applied differential input of the main run


def load(f):
    d = np.genfromtxt(f, names=True)
    return d["time"], d


def main():
    t, d = load("sa_p2mv.csv")
    tn = t * 1e9

    clk = d["vclk"]
    p, q = d["vp"], d["vq"]
    outp, outn = d["voutp"], d["voutn"]

    # clk rising edge
    ir = np.argmax(clk > 0.75)
    t0 = tn[ir]

    # integration ends when the faster of P/Q has dropped one Vthn (~0.45 V)
    vth_drop = 0.45
    fall = np.minimum(p, q)
    ie = ir + np.argmax(fall[ir:] < (1.5 - vth_drop))
    tint = (tn[ie] - t0) * 1e-9

    # integration gain: differential development at end of integration / dv
    a_int = abs((p[ie] - q[ie])) / DV
    gmtint = a_int * CPQ
    sigma_n = np.sqrt(4 * KT * GAMMA / gmtint)

    # decision time: outputs separated by >1V
    idec = ir + np.argmax(np.abs(outp[ir:] - outn[ir:]) > 1.0)
    tdec = tn[idec] - t0

    print(f"Tint          = {tint*1e12:.0f} ps")
    print(f"A_int         = {a_int:.1f} V/V (dv={DV*1e3:.1f}mV -> {abs(p[ie]-q[ie])*1e3:.1f}mV at P/Q)")
    print(f"gm*Tint       = {gmtint:.3e} (with Cpq={CPQ*1e15:.0f}fF)")
    print(f"sigma_n(est)  = {sigma_n*1e6:.0f} uV rms   (budget 1170 uV)")
    print(f"decision time = {tdec:.2f} ns @ dv=2mV")

    # check polarity + small-signal run resolves — sample at END OF EVAL phase (t=9.8ns),
    # not at the end of the trace (precharge has already reset the outputs there)
    ieval = np.argmin(np.abs(tn - 9.8))
    _, dm = load("sa_n2mv.csv")
    _, ds = load("sa_p0m2.csv")
    sep_p = outp[ieval] - outn[ieval]
    sep_m = dm["voutp"][ieval] - dm["voutn"][ieval]
    sep_s = ds["voutp"][ieval] - ds["voutn"][ieval]
    ok_pol = sep_p * sep_m < 0 and abs(sep_p) > 1.0 and abs(sep_m) > 1.0
    ok_small = abs(sep_s) > 1.0 and (sep_s * sep_p > 0)
    print(f"outp-outn @eval end: +2mV:{sep_p:+.2f}V  -2mV:{sep_m:+.2f}V  +0.2mV:{sep_s:+.2f}V")
    print(f"polarity flip: {'PASS' if ok_pol else 'FAIL'};  0.2mV resolve: {'PASS' if ok_small else 'FAIL'}")
    print(f"convention: inp>inn -> outp {'HIGH' if sep_p > 0 else 'LOW'} (SAR cmp wiring follows this)")

    fig, ax = plt.subplots(figsize=(9.5, 4.4), dpi=140)
    fig.patch.set_facecolor(SURF)
    ax.set_facecolor(SURF)
    ax.grid(alpha=0.22, lw=0.6)
    ax.tick_params(colors=INK2)
    for sp in ax.spines.values():
        sp.set_color(INK2)

    ax.plot(tn, clk, color=INK2, lw=1.0, ls=":", label="clk")
    ax.plot(tn, p, color=ORANGE, lw=1.4, label="P / Q（积分节点）")
    ax.plot(tn, q, color=ORANGE, lw=1.4, alpha=0.55)
    ax.plot(tn, outp, color=BLUE, lw=1.7, label="outp / outn")
    ax.plot(tn, outn, color=BLUE, lw=1.7, alpha=0.55)
    ax.axvspan(t0, t0 + tint * 1e9, color=ORANGE, alpha=0.08)
    ax.text(t0 + tint * 1e9 / 2, 1.62, f"积分相 {tint*1e12:.0f} ps", ha="center",
            color=ORANGE, fontsize=8)
    ax.annotate(f"判决 {tdec:.1f} ns", xy=(t0 + tdec, 1.25), color=BLUE, fontsize=8,
                xytext=(t0 + tdec + 1.2, 1.45),
                arrowprops=dict(arrowstyle="->", color=BLUE, lw=0.8))
    ax.set_xlabel("时间 [ns]", color=INK)
    ax.set_ylabel("电压 [V]", color=INK)
    ax.set_title(f"StrongARM 干净瞬态 @ Δvin=2mV：σn 估计 {sigma_n*1e6:.0f} µV（预算 1170 µV）",
                 color=INK, fontsize=10)
    ax.legend(loc="center right", fontsize=8, framealpha=0.9)
    ax.set_xlim(1.0, 8.0)
    fig.tight_layout()
    fig.savefig("strongarm_tran.png", facecolor=SURF)
    print("saved strongarm_tran.png")


if __name__ == "__main__":
    main()
