#!/usr/bin/env python3
"""OA-SAR8 dynamic test: coherent sine -> FFT -> SNDR/SFDR/ENOB, comparator noise budget."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = ["Droid Sans Fallback", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

from sar_model import make_weights  # noqa: E402  (same directory)

N = 8
VREF = 1.5
LSB = VREF / 2**N
FS = 100e3
NFFT = 4096
MBIN = 101                      # odd, coprime with NFFT -> coherent sampling
FIN = MBIN / NFFT * FS
AMP = 0.475 * VREF              # -0.44 dBFS

SURF, INK, INK2 = "#fcfcfb", "#0b0b0b", "#52514e"
BLUE, GRAY, RED = "#2a78d6", "#c9c8c0", "#b3261e"
rng = np.random.default_rng(11)


def convert_vec_noisy(v, ws, total, sn_lsb, rng):
    """SAR conversion; independent comparator noise draw at EVERY bit decision."""
    acc = np.zeros_like(v)
    code = np.zeros(v.shape, np.int32)
    for b in range(N - 1, -1, -1):
        trial = acc + ws[b]
        vdac = VREF * trial / total
        vn = rng.normal(0.0, sn_lsb * LSB, v.shape) if sn_lsb > 0 else 0.0
        take = (v + vn) > vdac
        acc = np.where(take, trial, acc)
        code |= take.astype(np.int32) << b
    return code


def sndr_sfdr(codes):
    x = codes.astype(float)
    x -= x.mean()
    P = np.abs(np.fft.rfft(x)) ** 2
    P[0] = 0.0
    sig = P[MBIN]
    noi = P[1:].sum() - sig
    sndr = 10 * np.log10(sig / noi)
    spur = np.delete(P[1:], MBIN - 1).max()
    sfdr = 10 * np.log10(sig / spur)
    enob = (sndr - 1.76) / 6.02
    return sndr, sfdr, enob, P


def main():
    t = np.arange(NFFT) / FS
    vin = VREF / 2 + AMP * np.sin(2 * np.pi * FIN * t)

    ws_ideal = np.array([2.0**b for b in range(N)])
    tot_ideal = 2.0**N
    ws_m, tot_m = make_weights(0.01)          # one 1%-mismatch instance

    sndr0, sfdr0, enob0, _ = sndr_sfdr(convert_vec_noisy(vin, ws_ideal, tot_ideal, 0.0, rng))
    sndr1, sfdr1, enob1, P1 = sndr_sfdr(convert_vec_noisy(vin, ws_m, tot_m, 0.2, rng))
    print(f"ideal      : SNDR={sndr0:5.2f} dB  SFDR={sfdr0:5.2f} dB  ENOB={enob0:.2f} bit")
    print(f"mm1%+n0.2  : SNDR={sndr1:5.2f} dB  SFDR={sfdr1:5.2f} dB  ENOB={enob1:.2f} bit")

    sn_list = [0.0, 0.1, 0.2, 0.3, 0.5, 0.8, 1.2]
    enob_mean, enob_min = [], []
    for sn in sn_list:
        es = []
        for _ in range(5):
            _, _, e, _ = sndr_sfdr(convert_vec_noisy(vin, ws_m, tot_m, sn, rng))
            es.append(e)
        enob_mean.append(np.mean(es))
        enob_min.append(np.min(es))
        print(f"sigma_n={sn:.1f} LSB -> ENOB mean={np.mean(es):.2f} min={np.min(es):.2f}")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.3), dpi=140)
    fig.patch.set_facecolor(SURF)
    for ax in (ax1, ax2):
        ax.set_facecolor(SURF)
        ax.grid(alpha=0.22, linewidth=0.6)
        ax.tick_params(colors=INK2)
        for sp in ax.spines.values():
            sp.set_color(INK2)

    # spectrum of the realistic case, dBFS (full-scale sine amplitude = 2^N/2 codes)
    pfs = (2**N / 2 * NFFT / 2) ** 2
    f_khz = np.arange(len(P1)) * FS / NFFT / 1e3
    db = 10 * np.log10(np.maximum(P1, 1e-12) / pfs)
    ax1.plot(f_khz[1:], db[1:], color=BLUE, lw=0.8)
    ax1.set_ylim(-110, 5)
    ax1.set_xlabel("频率 [kHz]", color=INK)
    ax1.set_ylabel("幅度 [dBFS]", color=INK)
    ax1.set_title("输出频谱：σu=1% + 比较器噪声 0.2 LSB（4096 点相干采样）",
                  color=INK, fontsize=10)
    ax1.text(0.97, 0.95,
             f"SNDR = {sndr1:.1f} dB\nSFDR = {sfdr1:.1f} dB\nENOB = {enob1:.2f} bit",
             transform=ax1.transAxes, ha="right", va="top", color=INK, fontsize=9,
             bbox=dict(facecolor=SURF, edgecolor=INK2, boxstyle="round,pad=0.4"))

    ax2.plot(sn_list, enob_mean, "-o", color=BLUE, lw=1.8, ms=5, label="ENOB 均值(5 seeds)")
    ax2.plot(sn_list, enob_min, "--", color=INK2, lw=1.0, label="最差")
    ax2.axhline(7.5, color=RED, ls="--", lw=1.1)
    ax2.text(1.18, 7.52, "目标 7.5 bit", color=RED, fontsize=8, ha="right")
    ax2.axvline(0.2, color=INK2, ls=":", lw=1.0)
    ax2.text(0.22, ax2.get_ylim()[0] + 0.05, "设计预算 σn=0.2 LSB (ENOB 7.63)", color=INK2, fontsize=8)
    ax2.set_xlabel("比较器输入参考噪声 σn [LSB]", color=INK)
    ax2.set_ylabel("ENOB [bit]", color=INK)
    ax2.set_title("噪声预算：ENOB vs 比较器噪声（含 σu=1% 失配）", color=INK, fontsize=10)
    ax2.legend(loc="lower left", fontsize=8, framealpha=0.9)

    fig.tight_layout()
    out = __file__.rsplit("/", 1)[0] + "/dynamic_enob.png"
    fig.savefig(out, facecolor=SURF)
    print("saved", out)


if __name__ == "__main__":
    main()
