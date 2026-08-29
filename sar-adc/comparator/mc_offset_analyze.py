#!/usr/bin/env python3
"""Extract comparator offset from each MC ramp run; report sigma and histogram."""
import glob
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = ["Droid Sans Fallback", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
SURF, INK, INK2, BLUE, RED = "#fcfcfb", "#0b0b0b", "#52514e", "#2a78d6", "#b3261e"

# ramp: vin_diff = -15mV .. +15mV over 0..130ns; clk: eval windows, sample at 2.9n + k*4n
T_END = 258e-9
V0, V1 = -30e-3, 30e-3


def vos_of(f):
    d = np.genfromtxt(f, names=True)
    t = d["time"]
    sep = d["voutp"] - d["voutn"]
    ts = np.arange(2.9e-9, 257e-9, 4e-9)          # decision sample times
    dec = np.interp(ts, t, sep) > 0               # True = outp high = (diff > Vos)
    diffs = V0 + (V1 - V0) * ts / T_END           # ramp value at each decision
    if dec.all():
        return None                                # offset below -15mV (out of window)
    if not dec.any():
        return None
    # last False -> first True transition
    idx = np.where(np.diff(dec.astype(int)) == 1)[0]
    if len(idx) == 0:
        return None
    i = idx[-1]
    return 0.5 * (diffs[i] + diffs[i + 1])         # Vos between the two levels


def main():
    files = sorted(glob.glob("mc/mc_run_[0-9]*"))
    vos = np.array([v for v in (vos_of(f) for f in files) if v is not None])
    n_oow = len(files) - len(vos)
    mu, sd = vos.mean(), vos.std(ddof=1)
    print(f"runs={len(files)}  valid={len(vos)}  out-of-window={n_oow}")
    print(f"Vos mean={mu*1e3:+.2f} mV   sigma={sd*1e3:.2f} mV   (quantization ~0.27mV -> now 0.94mV window step)")
    print(f"3-sigma = {3*sd*1e3:.1f} mV = {3*sd/ (1.5/256):.1f} LSB (global shift only, no INL impact)")

    fig, ax = plt.subplots(figsize=(7.5, 4.0), dpi=140)
    fig.patch.set_facecolor(SURF)
    ax.set_facecolor(SURF)
    ax.grid(alpha=0.22, lw=0.6)
    ax.tick_params(colors=INK2)
    for sp in ax.spines.values():
        sp.set_color(INK2)
    ax.hist(vos * 1e3, bins=15, color=BLUE, edgecolor=SURF, linewidth=1.5)
    ax.axvline(mu * 1e3, color=INK, lw=1.4)
    ax.axvline((mu + sd) * 1e3, color=RED, ls="--", lw=1.0)
    ax.axvline((mu - sd) * 1e3, color=RED, ls="--", lw=1.0)
    ax.set_xlabel("比较器失调 Vos [mV]", color=INK)
    ax.set_ylabel("样本数", color=INK)
    ax.set_title(f"StrongARM 失调蒙特卡洛（{len(vos)} 样本，mos_tt_mismatch）："
                 f"σos = {sd*1e3:.2f} mV", color=INK, fontsize=10)
    fig.tight_layout()
    fig.savefig("offset_mc.png", facecolor=SURF)
    print("saved offset_mc.png")


if __name__ == "__main__":
    main()
