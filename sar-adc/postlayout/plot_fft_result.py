#!/usr/bin/env python3
"""Plot a compact code record and normalized spectrum from a metrics JSON."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


parser = argparse.ArgumentParser()
parser.add_argument("metrics", type=Path)
parser.add_argument("output", type=Path)
args = parser.parse_args()

metrics = json.loads(args.metrics.read_text(encoding="utf-8"))
n = int(metrics["fft_points"])
k = int(metrics["tone_bin"])
fs = float(metrics["fs_msps"])
codes = np.asarray(metrics["codes"][-n:], dtype=float)
spectrum = np.abs(np.fft.rfft(codes - np.mean(codes)))
dbfs = 20 * np.log10(np.maximum(spectrum / spectrum[k], 1e-8))
freq = np.arange(len(spectrum)) * fs / n

fig, axes = plt.subplots(2, 1, figsize=(9.2, 6.6), constrained_layout=True)
axes[0].plot(np.arange(n), codes, "o-", color="#0b7285", linewidth=1.3, markersize=3.5)
axes[0].set(xlabel="Sample", ylabel="Output code", xlim=(0, n - 1), ylim=(0, 255))
axes[0].grid(alpha=0.25)
axes[0].set_title(
    f"OA-SAR8 PEX: {fs:g} MS/s, fin={metrics['fin_hz']/1e6:.6g} MHz, "
    f"ENOB={metrics['enob_bit']:.4f} bit"
)

axes[1].stem(freq, dbfs, basefmt=" ", linefmt="#6741d9", markerfmt=" ")
axes[1].set(xlabel="Frequency (MHz)", ylabel="Magnitude (dBc)", ylim=(-100, 5))
axes[1].grid(alpha=0.25)
axes[1].annotate("carrier", (freq[k], 0), xytext=(freq[k] - 0.8, -18),
                 arrowprops={"arrowstyle": "->", "color": "#333"})

args.output.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(args.output, dpi=180)
print(args.output)
