#!/usr/bin/env python3
"""Plot the measured full-RC static-transfer screening record.

The input is the CSV produced by ``run_parallel_dc_transfer.py``.  This plot
shows the sampled code transfer and best-fit residual only; it intentionally
does not label the one-nominal-LSB grid as transition-level DNL/INL sign-off.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("samples", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--title", default="OA-SAR8 full-RC static-transfer screen")
    args = parser.parse_args()

    data = np.genfromtxt(args.samples, delimiter=",", names=True)
    vdiff = data["vdiff_v"]
    code = data["code"]
    residual = data["best_fit_residual_lsb"]

    figure, axes = plt.subplots(
        2, 1, figsize=(8.2, 6.2), sharex=True,
        gridspec_kw={"height_ratios": [2.2, 1.0]}, constrained_layout=True,
    )
    axes[0].step(vdiff, code, where="mid", color="#1769aa", linewidth=1.2)
    axes[0].set_ylabel("Output code")
    axes[0].set_ylim(-5, 260)
    axes[0].grid(True, alpha=0.25)
    axes[0].set_title(args.title)

    axes[1].plot(vdiff, residual, color="#c0392b", linewidth=1.0)
    axes[1].axhline(0.0, color="black", linewidth=0.7, alpha=0.7)
    axes[1].set_xlabel("Differential DC input (V)")
    axes[1].set_ylabel("Best-fit residual\n(code LSB)")
    axes[1].grid(True, alpha=0.25)

    figure.text(
        0.5, 0.002,
        "257-point functional screen; not transition-level DNL/INL sign-off",
        ha="center", va="bottom", fontsize=8, color="#555555",
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(args.out, dpi=180)


if __name__ == "__main__":
    main()
