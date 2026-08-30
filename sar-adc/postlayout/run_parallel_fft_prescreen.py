#!/usr/bin/env python3
"""Fast phase-equivalent PEX screen before a monolithic 33-sample signoff.

Each job performs one real extracted conversion.  Phase ``i * k/N`` shifts
the waveform segment seen during the first acquisition to the segment that
sample ``i`` sees in the monolithic deck.  This is only a screening tool; a
passing rate must still be confirmed by ``run_core18_pex.py`` in one deck.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np


SCRIPT_DIR = Path(__file__).resolve().parent
SAR_ADC = SCRIPT_DIR.parent
BUILD = SAR_ADC / "build" / "core18_pex"


def run_one(fs: float, n: int, k: int, amp: float, index: int) -> tuple[int, int]:
    phase = (360.0 * k * index / n) % 360.0
    tag = f"prescreen_{fs:g}m_n{n}_k{k}_i{index:02d}"
    command = [
        sys.executable, str(SCRIPT_DIR / "run_core18_pex.py"),
        "--fs-msps", str(fs), "--track-ns", "25", "--samples", "1",
        "--fft-points", str(n), "--tone-bin", str(k),
        "--amplitude", str(amp), "--phase-deg", str(phase),
        "--tstep-ns", "0.05", "--tag", tag,
    ]
    subprocess.run(command, cwd=SAR_ADC, check=True, stdout=subprocess.DEVNULL)
    metrics = json.loads((BUILD / f"metrics_{tag}.json").read_text())
    if metrics["completed_samples"] != 1:
        raise RuntimeError(f"sample {index} did not complete")
    return index, int(metrics["codes"][0])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fs-msps", type=float, required=True)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--fft-points", type=int, default=32)
    parser.add_argument("--tone-bin", type=int, default=15)
    parser.add_argument("--amplitude", type=float, default=0.70)
    args = parser.parse_args()

    # The monolithic analyzer discards startup sample 0 and FFTs samples 1..N.
    codes: dict[int, int] = {}
    with concurrent.futures.ProcessPoolExecutor(max_workers=args.workers) as pool:
        futures = [
            pool.submit(run_one, args.fs_msps, args.fft_points,
                        args.tone_bin, args.amplitude, index)
            for index in range(1, args.fft_points + 1)
        ]
        for future in concurrent.futures.as_completed(futures):
            index, code = future.result()
            codes[index] = code
            print(f"sample {index:02d}: code={code}", flush=True)

    record = np.asarray([codes[index] for index in range(1, args.fft_points + 1)], dtype=float)
    spectrum = np.fft.rfft(record - np.mean(record))
    power = np.abs(spectrum) ** 2
    power[0] = 0.0
    signal = power[args.tone_bin]
    noise_distortion = np.sum(power) - signal
    sndr = 10.0 * math.log10(signal / noise_distortion)
    metrics = {
        "method": "phase-equivalent independent full-RC conversions; prescreen only",
        "fs_msps": args.fs_msps,
        "fft_points": args.fft_points,
        "tone_bin": args.tone_bin,
        "codes": record.astype(int).tolist(),
        "sndr_db": sndr,
        "enob_bit": (sndr - 1.76) / 6.02,
    }
    out = BUILD / f"metrics_prescreen_{args.fs_msps:g}m.json"
    out.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(json.dumps(metrics, indent=2))
    print(f"metrics={out}")


if __name__ == "__main__":
    main()
