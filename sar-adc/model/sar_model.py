#!/usr/bin/env python3
"""OA-SAR8 behavioral model: cap-mismatch Monte Carlo -> INL/DNL, sizing the unit cap matching."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = ["Droid Sans Fallback", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

N = 8
VREF = 1.5
LSB = VREF / 2**N
NCODE = 2**N
rng = np.random.default_rng(7)

# palette (dataviz reference, light mode)
SURF, INK, INK2 = "#fcfcfb", "#0b0b0b", "#52514e"
BLUE, GRAY, RED = "#2a78d6", "#c9c8c0", "#b3261e"


def make_weights(sigma_u):
    """Binary-weighted CDAC from 2^N-1 unit caps (+1 terminator); returns bit weights and total."""
    units = rng.normal(1.0, sigma_u, 2**N)
    term = units[0]
    ws, idx = [], 1
    for b in range(N):
        ws.append(units[idx:idx + 2**b].sum())
        idx += 2**b
    return np.array(ws), sum(ws) + term


def convert_vec(v, ws, total):
    """Vectorized SAR conversion of voltage array v."""
    acc = np.zeros_like(v)
    code = np.zeros(v.shape, dtype=np.int32)
    for b in range(N - 1, -1, -1):
        trial = acc + ws[b]
        take = v > VREF * trial / total
        acc = np.where(take, trial, acc)
        code |= take.astype(np.int32) << b
    return code


def inl_dnl(ws, total, oversample=64):
    v = np.linspace(0.0, VREF, NCODE * oversample, endpoint=False)
    codes = convert_vec(v, ws, total)
    edges = np.empty(NCODE)
    edges[0] = 0.0
    for k in range(1, NCODE):
        i = np.searchsorted(codes, k)
        edges[k] = v[i] if i < len(v) else VREF
    inl = (edges - np.arange(NCODE) * LSB) / LSB
    dnl = np.diff(edges) / LSB - 1.0
    return inl[1:], dnl


def main():
    sigmas = [0.005, 0.01, 0.02]
    runs = 200
    maxinl = {s: [] for s in sigmas}
    curves = []
    for s in sigmas:
        for r in range(runs):
            ws, tot = make_weights(s)
            inl, dnl = inl_dnl(ws, tot, oversample=32)
            maxinl[s].append(np.abs(inl).max())
            if s == 0.01 and r < 30:
                curves.append(inl)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2), dpi=140)
    fig.patch.set_facecolor(SURF)
    for ax in (ax1, ax2):
        ax.set_facecolor(SURF)
        ax.grid(alpha=0.22, linewidth=0.6)
        ax.tick_params(colors=INK2)
        for sp in ax.spines.values():
            sp.set_color(INK2)

    codes = np.arange(1, NCODE)
    for c in curves:
        ax1.plot(codes, c, color=GRAY, lw=0.7)
    ax1.plot(codes, curves[0], color=BLUE, lw=1.6)
    for y in (0.5, -0.5):
        ax1.axhline(y, color=RED, lw=1.1, ls="--")
    ax1.text(NCODE - 6, 0.54, "+0.5 LSB 限", color=RED, ha="right", fontsize=8)
    ax1.set_xlabel("输出码", color=INK)
    ax1.set_ylabel("INL [LSB]", color=INK)
    ax1.set_title("INL, 30 次蒙特卡洛 @ σu=1%（蓝=其中一次）", color=INK, fontsize=10)

    pos = np.arange(len(sigmas))
    for i, s in enumerate(sigmas):
        y = np.asarray(maxinl[s])
        x = np.full_like(y, pos[i]) + rng.normal(0, 0.05, y.size)
        ax2.plot(x, y, ".", color=BLUE, alpha=0.35, ms=4)
        ax2.plot([pos[i] - 0.18, pos[i] + 0.18], [np.median(y)] * 2, color=INK, lw=2)
        yld = (y < 0.5).mean() * 100
        ax2.text(pos[i], y.max() + 0.035, f"良率 {yld:.0f}%", ha="center", color=INK2, fontsize=8)
    ax2.axhline(0.5, color=RED, lw=1.1, ls="--")
    ax2.set_xticks(pos, [f"{s*100:.1f}%" for s in sigmas])
    ax2.set_xlabel("单位电容失配 σu", color=INK)
    ax2.set_ylabel("max|INL| [LSB]", color=INK)
    ax2.set_title(f"匹配需求，{runs} 次/组（横线=中位数）", color=INK, fontsize=10)

    fig.tight_layout()
    out = __file__.rsplit("/", 1)[0] + "/mc_inl.png"
    fig.savefig(out, facecolor=SURF)
    print("saved", out)
    for s in sigmas:
        y = np.asarray(maxinl[s])
        print(f"sigma_u={s*100:.1f}%  median max|INL|={np.median(y):.3f} LSB  "
              f"p95={np.percentile(y,95):.3f}  yield(<0.5LSB)={(y<0.5).mean()*100:.1f}%")


if __name__ == "__main__":
    main()
