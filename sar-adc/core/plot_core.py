#!/usr/bin/env python3
"""Plot the REAL charge-redistribution conversion waveform (vin=1.3857 run)."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = ["Droid Sans Fallback", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
SURF, INK, INK2 = "#fcfcfb", "#0b0b0b", "#52514e"
BLUE, ORANGE, GREEN, RED = "#2a78d6", "#eb6834", "#008300", "#b3261e"

VCM, VREF, VIN = 0.9, 1.5, 1.3857
T_TRK, T_BIT = 15, 12

d = np.genfromtxt("core_out.csv", names=True)
t = d["time"] * 1e9

fig, ax = plt.subplots(figsize=(11, 4.6), dpi=140)
fig.patch.set_facecolor(SURF)
ax.set_facecolor(SURF)
ax.grid(alpha=0.22, lw=0.6)
ax.tick_params(colors=INK2)
for sp in ax.spines.values():
    sp.set_color(INK2)

ax.plot(t, d["vtop"], color=BLUE, lw=1.6, label="CDAC top plate（真实电荷再分配）")
ax.plot(t, d["vclk"] * 0.12 + 0.05, color=INK2, lw=0.8, ls=":", label="比较器 clk（缩放）")
ax.axhline(VCM, color=GREEN, lw=1.2, ls="--")
ax.text(2, VCM + 0.02, "VCM = 0.9V（判决门限）", color=GREEN, fontsize=8)

ax.axvspan(0, T_TRK, color=ORANGE, alpha=0.10)
ax.text(T_TRK / 2, 1.32, "采样\n(top→VCM,\nbot→vin)", ha="center", color=ORANGE, fontsize=7)
bits = "11101100"
for k in range(8):
    t0 = T_TRK + k * T_BIT
    ax.axvline(t0, color=INK2, lw=0.5, alpha=0.4)
    ax.text(t0 + T_BIT / 2, 1.38, f"b{7-k}\n={bits[k]}", ha="center", color=INK, fontsize=8)

ax.set_xlabel("时间 [ns]", color=INK)
ax.set_ylabel("电压 [V]", color=INK)
ax.set_title("OA-SAR8 真核心一次完整转换：vin=1.3857V → code=236（cmim 电容阵列 + StrongARM）",
             color=INK, fontsize=10)
ax.legend(loc="center right", fontsize=8, framealpha=0.9)
fig.tight_layout()
fig.savefig("core_conversion.png", facecolor=SURF)
print("saved core_conversion.png")
