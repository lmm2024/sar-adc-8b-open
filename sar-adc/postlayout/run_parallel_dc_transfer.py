#!/usr/bin/env python3
"""Run an extracted static-transfer sweep as independent real conversions.

This avoids a single very long PEX deck while keeping the signed-off ADC,
solver options, reset, acquisition, and asynchronous conversion sequence.
The default 257-point grid has one nominal 8-bit LSB per input step and is a
functional/static-linearity screen.  Finer DNL sign-off needs 513 or more
points; the report records the actual grid resolution explicitly.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import subprocess
import sys
from pathlib import Path

import numpy as np


SCRIPT_DIR = Path(__file__).resolve().parent
SAR_ADC = SCRIPT_DIR.parent
BUILD = SAR_ADC / "build" / "core18_pex"


def run_one(index: int, vdiff: float, post_fall_ns: float, resume: bool) -> tuple[int, float, int, float]:
    tag = f"dc_transfer_i{index:04d}"
    metrics_path = BUILD / f"metrics_{tag}.json"
    if resume and metrics_path.exists():
        metrics = json.loads(metrics_path.read_text())
        if metrics.get("completed_samples") == 1:
            return index, vdiff, int(metrics["codes"][0]), float(metrics["conversion_time_ns_mean"])
    command = [
        sys.executable, str(SCRIPT_DIR / "run_core18_pex.py"),
        "--fs-msps", "10", "--track-ns", "25", "--samples", "1",
        "--dc", f"{vdiff:.12g}", "--tstep-ns", "0.05",
        "--post-fall-ns", f"{post_fall_ns:g}", "--tag", tag,
    ]
    subprocess.run(command, cwd=SAR_ADC, check=True, stdout=subprocess.DEVNULL)
    metrics = json.loads(metrics_path.read_text())
    if metrics["completed_samples"] != 1:
        raise RuntimeError(f"point {index} ({vdiff:+.9f} V) did not complete")
    return index, vdiff, int(metrics["codes"][0]), float(metrics["conversion_time_ns_mean"])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vmin", type=float, default=-1.4)
    parser.add_argument("--vmax", type=float, default=1.4)
    parser.add_argument("--points", type=int, default=257)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--post-fall-ns", type=float, default=45.0)
    parser.add_argument("--tag", default="dc257")
    parser.add_argument("--resume", action="store_true",
                        help="reuse completed per-point metrics from an interrupted identical sweep")
    args = parser.parse_args()
    if args.points < 3:
        raise ValueError("points must be at least 3")

    levels = np.linspace(args.vmin, args.vmax, args.points)
    results: dict[int, tuple[float, int, float]] = {}
    with concurrent.futures.ProcessPoolExecutor(max_workers=args.workers) as pool:
        jobs = [
            pool.submit(run_one, index, float(vdiff), args.post_fall_ns, args.resume)
            for index, vdiff in enumerate(levels)
        ]
        for future in concurrent.futures.as_completed(jobs):
            index, vdiff, code, conversion_ns = future.result()
            results[index] = (vdiff, code, conversion_ns)
            print(f"point {index:04d}: vdiff={vdiff:+.9f} V code={code}", flush=True)

    ordered = [results[index] for index in range(args.points)]
    vdiff = np.asarray([item[0] for item in ordered])
    codes = np.asarray([item[1] for item in ordered], dtype=int)
    conversion_ns = np.asarray([item[2] for item in ordered])
    slope, intercept = np.polyfit(vdiff, codes, 1)
    fitted = slope * vdiff + intercept
    residual = codes - fitted
    monotonic = bool(np.all(np.diff(codes) >= 0))
    observed = sorted(set(int(code) for code in codes))
    missing_between_observed_extremes = sorted(set(range(min(observed), max(observed) + 1)) - set(observed))

    metrics = {
        "method": "independent full-RC PEX conversions on a uniform differential-DC grid",
        "corner": "IHP SG13G2 mos_tt + cap_typ, 1.5 V, 27 C",
        "fs_msps": 10.0,
        "track_ns": 25.0,
        "vmin_vdiff_v": args.vmin,
        "vmax_vdiff_v": args.vmax,
        "points": args.points,
        "grid_step_v": float(levels[1] - levels[0]),
        "nominal_fullscale_lsb_v": float((args.vmax - args.vmin) / 256.0),
        "completed_points": len(ordered),
        "monotonic_on_test_grid": monotonic,
        "observed_code_min": int(codes.min()),
        "observed_code_max": int(codes.max()),
        "missing_codes_on_test_grid": missing_between_observed_extremes,
        "best_fit_code_per_v": float(slope),
        "best_fit_offset_code": float(intercept),
        "max_abs_code_residual_lsb": float(np.max(np.abs(residual))),
        "conversion_time_ns_min": float(conversion_ns.min()),
        "conversion_time_ns_mean": float(conversion_ns.mean()),
        "conversion_time_ns_max": float(conversion_ns.max()),
        "qualification": (
            "257-point functional/static-linearity screen; transition-level DNL/INL sign-off "
            "requires a finer input grid and endpoint/best-fit convention"
        ),
    }
    out_json = BUILD / f"metrics_{args.tag}.json"
    out_csv = BUILD / f"samples_{args.tag}.csv"
    out_json.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    np.savetxt(
        out_csv,
        np.column_stack((np.arange(args.points), vdiff, codes, conversion_ns, residual)),
        delimiter=",",
        header="index,vdiff_v,code,conversion_ns,best_fit_residual_lsb",
        comments="",
        fmt=["%d", "%.12g", "%d", "%.12g", "%.12g"],
    )
    print(json.dumps(metrics, indent=2))
    print(f"metrics={out_json}")
    print(f"samples={out_csv}")


if __name__ == "__main__":
    main()
