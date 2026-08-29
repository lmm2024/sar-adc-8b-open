#!/usr/bin/env python3
"""Plot the SAR binary-search convergence from sar_trace.txt (real comparator in the loop)."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = ["Droid Sans Fallback", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
SURF, INK, INK2 = "#fcfcfb", "#0b0b0b", "#52514e"
BLUE, ORANGE, GREEN = "#2a78d6", "#eb6834", "#008300"

rows = np.genfromtxt("sar_trace.txt", names=True)
vins = np.unique(rows["vin"])
pick = [vins[0], vins[2]]          # 0.1113 and 0.7529

fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), dpi=140)
fig.patch.set_facecolor(SURF)
for ax, v in zip(axes, pick):
    ax.set_facecolor(SURF)
    ax.grid(alpha=0.22, lw=0.6)
    ax.tick_params(colors=INK2)
    for sp in ax.spines.values():
        sp.set_color(INK2)
    sel = rows[rows["vin"] == v]
    steps = 8 - sel["bit"]
    ax.axhline(v, color=GREEN, lw=1.4)
    ax.text(8.15, v, f"vin={v:.4f}V", color=GREEN, fontsize=8, va="center")
    ax.step(np.append(steps, 9), np.append(sel["trial_v"], sel["trial_v"][-1]),
            where="post", color=INK2, lw=0.9, alpha=0.6)
    kept = sel["cmp"] > 0.5
    ax.plot(steps[kept], sel["trial_v"][kept], "o", color=BLUE, ms=7,
            label="cmp=1（保留该位）")
    ax.plot(steps[~kept], sel["trial_v"][~kept], "x", color=ORANGE, ms=8, mew=2,
            label="cmp=0（清除该位）")
    code = int(sel["code_after"][-1])
    ax.set_title(f"vin={v:.4f}V → code={code}（真实 StrongARM 判决 ×8）",
                 color=INK, fontsize=10)
    ax.set_xlabel("逼近步（MSB→LSB）", color=INK)
    ax.set_ylabel("DAC 试探电平 [V]", color=INK)
    ax.set_xlim(0.5, 10.2)
    ax.legend(loc="best", fontsize=8, framealpha=0.9)

fig.tight_layout()
fig.savefig("sar_convergence.png", facecolor=SURF)
print("saved sar_convergence.png")
