#!/usr/bin/env python3
"""OA-SAR8 REAL core: charge-redistribution CDAC (cmim caps) + switch matrix +
StrongARM comparator, converting by actual charge redistribution.

Feedback loop solved by iterative re-simulation: iteration k replays the whole
conversion from t=0 with all switch history, then decides bit k from the real
comparator output. 8 iterations = one conversion, charge continuity guaranteed.
"""
import subprocess
import numpy as np

N = 8
VDD, VCM = 1.5, 0.9
LSB = VDD / 2**N
T_TRK = 15e-9          # track phase
T_BIT = 12e-9          # per-bit phase (settle 8ns, clk fire 8..11ns)
T_DEC = 10.5e-9        # decision readout inside phase
EDGE = 0.2e-9

NETLIST = """* OA-SAR8 real core: CDAC + switches + StrongARM (generated)
.lib cornerMOSlv.lib mos_tt
.lib cornerCAP.lib cap_typ
.param vdd=1.5
.param vcm=0.9

VDD vdd 0 {{vdd}}
VCMs vcm 0 {{vcm}}
VIN vin 0 {vin}

* ---- CDAC: binary-weighted cmim, unit 2.2x2.2um (~7fF), 255u + 1u terminator
{caps}
XCd top botd cap_cmim w=2.2u l=2.2u m=1

* ---- track switches: top->VCM, bottoms->VIN
Stop top vcm ctrk 0 swm
{trksw}
Strkd botd vin ctrk 0 swm

* ---- conversion switches: bottoms -> VREF(vdd) or GND
{convsw}
Sgd botd 0 cinv 0 swm
.model swm sw vt=0.75 vh=0.05 ron=100 roff=1e12

* ---- pseudo-differential reference: replica floating node, kickback -> common-mode
XCrep topr 0 cap_cmim w=2.2u l=2.2u m=256
Strep topr vcm ctrk 0 swm

* ---- StrongARM comparator: inp=topr(float@VCM), inn=top (outp HIGH <=> vin>vdac)
XM1 p   topr tail 0  sg13_lv_nmos w=2u l=0.15u ng=2
XM2 q   top tail 0   sg13_lv_nmos w=2u l=0.15u ng=2
XM3 outn outp p 0    sg13_lv_nmos w=4u l=0.13u ng=2
XM4 outp outn q 0    sg13_lv_nmos w=4u l=0.13u ng=2
XM5 outn outp vdd vdd sg13_lv_pmos w=6u l=0.13u ng=2
XM6 outp outn vdd vdd sg13_lv_pmos w=6u l=0.13u ng=2
XS1 p    clk vdd vdd sg13_lv_pmos w=2u l=0.13u ng=1
XS2 q    clk vdd vdd sg13_lv_pmos w=2u l=0.13u ng=1
XS3 outn clk vdd vdd sg13_lv_pmos w=2u l=0.13u ng=1
XS4 outp clk vdd vdd sg13_lv_pmos w=2u l=0.13u ng=1
XMt tail clk 0 0     sg13_lv_nmos w=3u l=0.3u ng=2

* ---- controls
Vctrk ctrk 0 pwl({pwl_trk})
Vcinv cinv 0 pwl({pwl_inv})
Vclk  clk  0 pwl({pwl_clk})
{ctrl}

.control
set wr_vecnames
set wr_singlescale
tran 100p {tend}
wrdata {out} v(outp) v(outn) v(top) v(clk)
quit
.endc
.end
"""


def pwl(points):
    return " ".join(f"{t:.4g} {v:g}" for t, v in points)


def step_pwl(transitions, v0):
    """transitions: [(t, vnew)]; builds PWL with EDGE ramps."""
    pts, v = [(0, v0)], v0
    for t, vn in transitions:
        pts += [(t, v), (t + EDGE, vn)]
        v = vn
    return pwl(pts)


def build(vin, decisions, nphases):
    caps, trksw, ctrl, convsw = [], [], [], []
    tend = T_TRK + nphases * T_BIT
    for b in range(N):
        caps.append(f"XC{b} top bot{b} cap_cmim w=2.2u l=2.2u m={2**b}")
        trksw.append(f"Strk{b} bot{b} vin ctrk 0 swm")
        convsw.append(f"Sr{b} bot{b} vdd cr{b} 0 swm")
        convsw.append(f"Sg{b} bot{b} 0 cg{b} 0 swm")
        # phase k tests bit (N-1-k); build this bit's REF/GND control timelines
        bit = b
        k_trial = N - 1 - bit                      # phase index when this bit is tried
        ref_tr, gnd_tr = [], []
        for k in range(nphases):
            t0 = T_TRK + k * T_BIT
            if k < k_trial:
                ref_v, gnd_v = 0, VDD              # not yet tried: bottom at GND
            elif k == k_trial:
                ref_v, gnd_v = VDD, 0              # trial: bottom at VREF
            else:                                  # after trial: per decision
                kept = decisions[k_trial]
                ref_v, gnd_v = (VDD, 0) if kept else (0, VDD)
            ref_tr.append((t0, ref_v))
            gnd_tr.append((t0, gnd_v))
        ctrl.append(f"Vcr{b} cr{b} 0 pwl({step_pwl(ref_tr, 0)})")
        ctrl.append(f"Vcg{b} cg{b} 0 pwl({step_pwl(gnd_tr, 0)})")
    # track control: on during track, off after
    pwl_trk = step_pwl([(T_TRK, 0)], VDD)
    pwl_inv = step_pwl([(T_TRK, VDD)], 0)          # terminator bottom to GND after track
    # comparator clock: one pulse per phase at +8..+11ns
    clk_tr = []
    for k in range(nphases):
        t0 = T_TRK + k * T_BIT
        clk_tr += [(t0 + 8e-9, VDD), (t0 + 11e-9, 0)]
    pwl_clk = step_pwl(clk_tr, 0)
    return NETLIST.format(vin=vin, caps="\n".join(caps), trksw="\n".join(trksw),
                          convsw="\n".join(convsw), ctrl="\n".join(ctrl),
                          pwl_trk=pwl_trk, pwl_inv=pwl_inv, pwl_clk=pwl_clk,
                          tend=f"{tend*1e9:.1f}n", out="core_out.csv")


def convert(vin, verbose=True):
    decisions = []
    for k in range(N):
        deck = build(vin, decisions + [None], k + 1)
        open("core_run.spice", "w").write(deck)
        subprocess.run(["ngspice", "-b", "-o", "core_run.log", "core_run.spice"],
                       capture_output=True)
        d = np.genfromtxt("core_out.csv", names=True)
        tdec = T_TRK + k * T_BIT + T_DEC
        sep = np.interp(tdec, d["time"], d["voutp"] - d["voutn"])
        decisions.append(bool(sep > 0))
        if verbose:
            print(f"  phase {k} (bit {N-1-k}): sep={sep:+.2f}V -> {int(sep > 0)}")
    code = sum((1 << (N - 1 - k)) for k, dec in enumerate(decisions) if dec)
    return code, d


def main():
    tests = [0.1113, 0.7529, 1.3857]
    results = []
    for v in tests:
        print(f"converting vin={v} V ...")
        code, wave = convert(v)
        exp = min(255, int(v / LSB))
        results.append((v, code, exp, wave))
        print(f"  => code={code}  expected={exp}  {'OK' if abs(code-exp) <= 1 else 'MISMATCH'}")
    np.save("last_wave.npy", results[-1][3])
    # keep the mid-scale waveform for plotting
    for v, code, exp, wave in results:
        if abs(v - 0.7529) < 1e-6:
            np.save("wave_mid.npy", wave)
    print("DONE")


if __name__ == "__main__":
    main()
