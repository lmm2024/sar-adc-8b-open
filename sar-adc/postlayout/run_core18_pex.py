#!/usr/bin/env python3
"""Run the complete OA-SAR8 core18 full-RC extracted netlist in ngspice.

The extracted top contains the optimized analog front end and the placed and
routed asynchronous controller.  ``track`` is the only conversion stimulus:
its falling edge starts the real request/acknowledge loop.  No behavioural bit
clock or fixed conversion delay is added by this testbench.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import re
import subprocess
from pathlib import Path

import numpy as np


SAR_ADC = Path(__file__).resolve().parent.parent
PEX = (SAR_ADC / "layout" / "pex_core18_final_w2_rc"
       / "oa_sar8_core18_final.pex.spice")
# Keep every generated deck/result in one repository-level build directory.
# The batch runners and REPRODUCE_SIGNOFF.md use the same location.
BUILD = SAR_ADC / "build" / "core18_pex"
MODELS = Path("/foss/pdks/ihp-sg13g2/libs.tech/ngspice/models")


def joined_subckt_ports(text: str, name: str) -> list[str]:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if re.match(rf"(?i)^\.subckt\s+{re.escape(name)}(?:\s|$)", line):
            merged = line
            cursor = index + 1
            while cursor < len(lines) and lines[cursor].startswith("+"):
                merged += " " + lines[cursor][1:].strip()
                cursor += 1
            return merged.split()[2:]
    raise ValueError(f"subcircuit {name!r} not found")


def make_deck(args: argparse.Namespace, tag: str) -> tuple[Path, Path, list[str]]:
    pex_text = PEX.read_text(encoding="utf-8", errors="replace")
    ports = joined_subckt_ports(pex_text, "oa_sar8_core18_final")
    required = {
        "track", "rst_n", "done", "busy", "vinp", "vinn", "vcm",
        "VDD", "VSS", *(f"result[{bit}]" for bit in range(8)),
    }
    missing = sorted(required - set(ports))
    if missing:
        raise RuntimeError(f"PEX top is missing ports: {missing}")

    period_ns = 1000.0 / args.fs_msps
    if not (0.0 < args.track_ns < period_ns):
        raise ValueError("track-ns must lie between zero and one sample period")
    low_ns = period_ns - args.track_ns
    # A bootstrap cannot start in the boosted TRACK phase from an uninitialized
    # UIC state.  Hold it off through reset first so its storage capacitor is
    # physically precharged, then acquire for exactly track_ns.  This avoids
    # counting a non-physical cold-start sample as ADC data.
    startup_precharge_ns = 6.0
    first_fall_ns = startup_precharge_ns + args.track_ns
    # Stop just before the falling edge that would launch sample N+1.
    if args.post_fall_ns is None:
        stop_ns = first_fall_ns + args.samples * period_ns - 0.1
    else:
        if args.post_fall_ns <= 0:
            raise ValueError("post-fall-ns must be positive")
        stop_ns = first_fall_ns + (args.samples - 1) * period_ns + args.post_fall_ns
    fin_hz = args.tone_bin / args.fft_points * args.fs_msps * 1e6

    def conn(port: str) -> str:
        aliases = {"VDD": "vdd", "VSS": "0"}
        aliases.update({f"result[{bit}]": f"result{bit}" for bit in range(8)})
        return aliases.get(port, port)

    BUILD.mkdir(parents=True, exist_ok=True)
    deck = BUILD / f"tb_{tag}.spice"
    wave = BUILD / f"wave_{tag}.csv"
    if args.dc is None:
        sources = (
            f"Vinp vinp 0 dc 0.75 sin(0.75 {args.amplitude:g} {fin_hz:.12g} 0 0 {args.phase_deg:g})\n"
            f"Vinn vinn 0 dc 0.75 sin(0.75 {-args.amplitude:g} {fin_hz:.12g} 0 0 {args.phase_deg:g})"
        )
    else:
        sources = (
            f"Vinp vinp 0 {0.75 + args.dc / 2:.12g}\n"
            f"Vinn vinn 0 {0.75 - args.dc / 2:.12g}"
        )

    result_vectors = " ".join(f"v(result{bit})" for bit in range(7, -1, -1))
    debug_nodes = [
        "v(xdut.sar_ctrl_async_phys_0.sample)",
        "v(xdut.sar_ctrl_async_phys_0.hold_req)",
        "v(xdut.sar_ctrl_async_phys_0.cmp_fire)",
        "v(xdut.sar_ctrl_async_phys_0.cmp_p)",
        "v(xdut.sar_ctrl_async_phys_0.cmp_n)",
        # Analog observability: the two top-plate/comparator-input nodes and
        # the two flattened sampled-input distribution nodes.
        "v(xdut.oa_sar8_acore18_opt_0.sw_tg_opt_0.bot)",
        "v(xdut.oa_sar8_acore18_opt_0.sw_tg_opt_1.bot)",
        "v(xdut.oa_sar8_acore18_opt_0.bstrap_opt_w2_c1200_1.out)",
    ]
    # Magic names flattened standard-cell boundary nets after their physical
    # instance.  Recording every retained delay-cell A/X node makes a failed
    # asynchronous transition traceable without guessing a behavioural net.
    delay_pattern = re.compile(
        r"^(sar_ctrl_async_phys_0\.sg13g2_dlygate4sd[123]_1_\d+\."
        r"(?:A|X))(?:\.t\d+)?$"
    )
    choices: dict[str, list[str]] = {}
    for token in re.findall(r"\S+", pex_text):
        match = delay_pattern.match(token)
        if match:
            choices.setdefault(match.group(1), []).append(token)
    # Prefer the unsplit pin, otherwise the t0 extraction terminal, otherwise
    # the first terminal segment.  Internal .n# diffusion nodes are excluded.
    delay_nodes = []
    for pin, nodes in sorted(choices.items()):
        delay_nodes.append(min(nodes, key=lambda node: (
            node != pin, not node.endswith(".t0"), len(node), node
        )))
    debug_nodes.extend(f"v(xdut.{node})" for node in delay_nodes)
    clock_pattern = re.compile(
        r"^(sar_ctrl_async_phys_0\.sg13g2_dfrbpq_1_\d+\.CLK)"
        r"(?:\.t\d+)?$"
    )
    clock_choices: dict[str, list[str]] = {}
    for token in re.findall(r"\S+", pex_text):
        match = clock_pattern.match(token)
        if match:
            clock_choices.setdefault(match.group(1), []).append(token)
    for pin, nodes in sorted(clock_choices.items()):
        node = min(nodes, key=lambda item: (
            item != pin, not item.endswith(".t0"), len(item), item
        ))
        debug_nodes.append(f"v(xdut.{node})")
    debug_vectors = " ".join(debug_nodes)
    deck.write_text(f"""* OA-SAR8 core18 complete full-RC PEX, TT 1.5 V, 27 C
.lib {MODELS / 'cornerMOSlv.lib'} mos_tt
.lib {MODELS / 'cornerCAP.lib'} cap_typ
.option temp=27 abstol=1e-12 reltol=3e-3 vntol=1e-5 chgtol=1e-13 method=trap trtol=10 itl4=500 klu rshunt=1e11

.include {PEX}

VDD vdd 0 1.5
VCM vcm 0 0.75
{sources}
Vrst rst_n 0 pwl(0 0 5n 0 5.1n 1.5)
* Low during reset precharges the bootstrap; high=acquire; falling starts SAR.
Vtrack track 0 pulse(0 1.5 {startup_precharge_ns:g}n 0.05n 0.05n {args.track_ns:g}n {period_ns:g}n)

Xdut {' '.join(conn(port) for port in ports)} oa_sar8_core18_final
{''.join(f'Cload{bit} result{bit} 0 5f' + chr(10) for bit in range(8))}
Cdone done 0 5f
Cbusy busy 0 5f

.save v(track) v(done) v(busy) {result_vectors} v(vinp) v(vinn) i(VDD) {debug_vectors}
.control
set filetype=ascii
set wr_singlescale
set wr_vecnames
tran {args.tstep_ns:g}n {stop_ns:g}n uic
wrdata {wave} v(track) v(done) v(busy) {result_vectors} v(vinp) v(vinn) i(VDD) {debug_vectors}
quit
.endc
.end
""", encoding="utf-8")
    return deck, wave, ports


def read_wave(path: Path) -> tuple[np.ndarray, list[str]]:
    header = path.read_text(encoding="utf-8", errors="replace").splitlines()[0].split()
    data = np.loadtxt(path, skiprows=1)
    if data.ndim == 1:
        data = data.reshape(1, -1)
    return data, header


def rising_times(t: np.ndarray, values: np.ndarray, threshold: float = 0.75) -> np.ndarray:
    indices = np.flatnonzero((values[:-1] < threshold) & (values[1:] >= threshold))
    return t[indices] + (threshold - values[indices]) * (
        t[indices + 1] - t[indices]
    ) / (values[indices + 1] - values[indices])


def falling_times(t: np.ndarray, values: np.ndarray, threshold: float = 0.75) -> np.ndarray:
    indices = np.flatnonzero((values[:-1] > threshold) & (values[1:] <= threshold))
    return t[indices] + (values[indices] - threshold) * (
        t[indices + 1] - t[indices]
    ) / (values[indices] - values[indices + 1])


def analyse(args: argparse.Namespace, tag: str, wave: Path) -> dict:
    data, names = read_wave(wave)
    expected = ["time", "v(track)", "v(done)", "v(busy)"]
    if [name.lower() for name in names[:4]] != expected:
        raise RuntimeError(f"unexpected wrdata columns: {names}")
    t = data[:, 0]
    track, done = data[:, 1], data[:, 2]
    bit_columns = data[:, 4:12]
    track_edges = falling_times(t, track)
    all_done_edges = rising_times(t, done)
    # ``uic`` can create a harmless sub-nanosecond output transition while the
    # extracted standard-cell nodes acquire their reset state.  Pair one real
    # DONE with each TRACK falling edge, inside that sample period, instead of
    # counting a pre-aperture startup transition as an ADC conversion.
    paired_track_edges: list[float] = []
    paired_done_edges: list[float] = []
    for sample, track_edge in enumerate(track_edges):
        period_end = (track_edges[sample + 1]
                      if sample + 1 < len(track_edges) else float("inf"))
        candidates = all_done_edges[
            (all_done_edges > track_edge) & (all_done_edges < period_end)
        ]
        if len(candidates):
            paired_track_edges.append(float(track_edge))
            paired_done_edges.append(float(candidates[0]))
    track_edges = np.asarray(paired_track_edges)
    done_edges = np.asarray(paired_done_edges)
    codes: list[int] = []
    for edge in done_edges:
        index = int(np.searchsorted(t, edge + 0.25e-9))
        index = min(index, len(t) - 1)
        bits = bit_columns[index] > 0.75
        code = sum(int(bit) << (7 - offset) for offset, bit in enumerate(bits))
        codes.append(code)
    count = len(done_edges)
    conversion_ns = ((done_edges - track_edges) * 1e9).tolist()
    metrics: dict[str, object] = {
        "pex_mode": "Magic full-RC (m=3)",
        "corner": "IHP SG13G2 mos_tt + cap_typ, 1.5 V, 27 C",
        "fs_msps": args.fs_msps,
        "track_ns": args.track_ns,
        "requested_samples": args.samples,
        "completed_samples": len(codes),
        "codes": codes,
        "conversion_time_ns_min": min(conversion_ns) if conversion_ns else None,
        "conversion_time_ns_mean": float(np.mean(conversion_ns)) if conversion_ns else None,
        "conversion_time_ns_max": max(conversion_ns) if conversion_ns else None,
    }
    if args.dc is None and len(codes) >= args.fft_points:
        record = np.asarray(codes[-args.fft_points:], dtype=float)
        centered = record - np.mean(record)
        spectrum = np.fft.rfft(centered)
        power = np.abs(spectrum) ** 2
        power[0] = 0.0
        signal_power = power[args.tone_bin]
        nd_power = np.sum(power) - signal_power
        sndr = 10.0 * math.log10(signal_power / nd_power)
        metrics.update({
            "fft_points": args.fft_points,
            "tone_bin": args.tone_bin,
            "fin_hz": args.tone_bin / args.fft_points * args.fs_msps * 1e6,
            "sndr_db": sndr,
            "enob_bit": (sndr - 1.76) / 6.02,
        })
    out_json = BUILD / f"metrics_{tag}.json"
    out_json.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    out_csv = BUILD / f"samples_{tag}.csv"
    with out_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["sample", "code", "track_fall_s", "done_rise_s", "conversion_ns"])
        for index in range(count):
            writer.writerow([index, codes[index], track_edges[index], done_edges[index], conversion_ns[index]])
    return metrics


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fs-msps", type=float, required=True)
    parser.add_argument("--track-ns", type=float, required=True)
    parser.add_argument("--samples", type=int, default=4)
    parser.add_argument("--fft-points", type=int, default=64)
    parser.add_argument("--tone-bin", type=int, default=29)
    parser.add_argument("--amplitude", type=float, default=0.70,
                        help="single-ended sine amplitude; differential peak is twice this")
    parser.add_argument("--phase-deg", type=float, default=0.0,
                        help="sine phase in degrees; default preserves signoff deck")
    parser.add_argument("--dc", type=float, default=None,
                        help="constant differential input in volts")
    parser.add_argument("--tstep-ns", type=float, default=0.05)
    parser.add_argument("--post-fall-ns", type=float, default=None,
                        help="stop this many ns after the final TRACK falling edge")
    parser.add_argument("--tag", default=None)
    args = parser.parse_args()
    tag = args.tag or f"{args.fs_msps:g}m_track{args.track_ns:g}n_{args.samples}"
    deck, wave, _ = make_deck(args, tag)
    log = BUILD / f"ngspice_{tag}.log"
    with log.open("w", encoding="utf-8") as handle:
        process = subprocess.run(["ngspice", "-b", str(deck)], stdout=handle,
                                 stderr=subprocess.STDOUT, text=True)
    if process.returncode:
        raise RuntimeError(f"ngspice failed; see {log}")
    log_text = log.read_text(encoding="utf-8", errors="replace")
    if "simulation(s) aborted" in log_text or "Timestep too small" in log_text:
        raise RuntimeError(f"ngspice transient aborted before stop time; see {log}")
    metrics = analyse(args, tag, wave)
    print(json.dumps(metrics, indent=2))
    print(f"deck={deck}")
    print(f"wave={wave}")
    print(f"log={log}")


if __name__ == "__main__":
    main()
