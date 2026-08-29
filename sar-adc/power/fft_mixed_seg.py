#!/usr/bin/env python3
"""32-point coherent FFT from 4 phase-offset segments of the unified mixed-signal
post-layout run (tb_mixed4_s0..s3): segment k carries the input phase 270*k deg so
its samples m=0..7 are the global coherent samples n=8k+m (fin = 15/32 fs). The first
SKIP conversions of every segment are discarded (start-up), the next 8 are used.
Also reports the average supply current over the analysed conversions."""
import sys
import numpy as np

BASE = sys.argv[1] if len(sys.argv) > 1 else "/foss/designs/sar-adc/power/mixed4_s{}_out.csv"
NSEG, PER, SKIP = 4, 8, 2
NFFT, FS, VDD = 32, 10e6, 1.5
BIN = int(sys.argv[2]) if len(sys.argv) > 2 else 15
names = ['done', 'r7', 'r6', 'r5', 'r4', 'r3', 'r2', 'r1', 'r0', 'trk', 'hold', 'vinp', 'vinn', 'i', 'outp', 'outn', 'clkcmp']
c = {n: 1 + 2 * i for i, n in enumerate(names)}

def read_seg(k):
    d = np.loadtxt(BASE.format(k))
    t = d[:, 0]
    done = d[:, c['done']]
    hi = done > 0.75
    edges = [e for e in (np.where(hi[1:] & ~hi[:-1])[0] + 1) if t[e] > 5e-9]
    trk = d[:, c['trk']]
    codes, dsamp, tdone, taper = [], [], [], []
    for e in edges:
        kk = np.searchsorted(t, t[e] + 1e-9)
        bits = [1 if d[kk, c['r%d' % b]] > 0.75 else 0 for b in range(7, -1, -1)]
        codes.append(int(''.join(map(str, bits)), 2))
        idx = np.where(trk[:e] > 0.75)[0]
        dsamp.append(d[idx[-1], c['vinp']] - d[idx[-1], c['vinn']])
        taper.append(t[idx[-1]])
        tdone.append(t[e])
    i = -d[:, c['i']]
    return np.array(codes), np.array(dsamp), np.array(tdone), np.array(taper), t, i

x, ideal, itot, tt = [], [], [], []
for k in range(NSEG):
    codes, dsamp, tdone, taper, t, i = read_seg(k)
    assert len(codes) >= SKIP + PER, f"segment {k}: only {len(codes)} conversions"
    sel = slice(SKIP, SKIP + PER)
    x.extend(codes[sel]); ideal.extend(dsamp[sel] / 1.5 * 128 + 127.5)
    t0, t1 = taper[SKIP], tdone[SKIP + PER - 1]
    m = (t >= t0) & (t <= t1)
    itot.append(np.trapezoid(i[m], t[m]) / (t1 - t0)); tt.append(t1 - t0)
    print(f"seg {k}: {len(codes)} conv, used {codes[sel].tolist()}, aperture period {np.median(np.diff(taper))*1e9:.2f} ns, Iavg {itot[-1]*1e6:.1f} uA")
x = np.array(x, float); ideal = np.array(ideal)
print("codes (32):", x.astype(int).tolist())
print("code - ideal(D@aperture) [LSB]:", np.round(x - ideal, 1).tolist())

def spectrum(sig_in, label):
    X = np.fft.rfft(sig_in - sig_in.mean()); P = np.abs(X) ** 2
    sig = P[BIN]
    nb = [k for k in range(1, NFFT // 2 + 1) if k != BIN]
    noise = sum(P[k] for k in nb)
    harm = sorted(set(min((BIN * h) % NFFT, NFFT - (BIN * h) % NFFT) for h in range(2, 6)))
    sndr = 10 * np.log10(sig / noise); enob = (sndr - 1.76) / 6.02
    sfdr = 10 * np.log10(sig / max(P[k] for k in nb))
    thd = 10 * np.log10(sum(P[h] for h in harm) / sig)
    dbfs = 20 * np.log10(np.sqrt(sig) / (NFFT / 2) / 128.0)
    print(f"[{label}] fin={BIN/NFFT*FS/1e6:.4f} MHz N={NFFT}: {dbfs:.2f} dBFS | SNDR {sndr:.2f} dB | ENOB {enob:.2f} b | SFDR {sfdr:.1f} dB | THD {thd:.1f} dB (harmonic bins {harm})")
    print("   spectrum dBc:", [round(10 * np.log10(P[k] / sig), 1) for k in range(1, NFFT // 2 + 1)])
    return sndr, enob, sfdr, thd

sndr, enob, sfdr, thd = spectrum(x, "ADC codes, transistor-level closed loop")
spectrum(np.round(ideal), "ideal 8-bit quantiser of the same aperture samples (reference)")
iavg = float(np.average(itot, weights=tt))
P = iavg * VDD
print(f"avg supply current {iavg*1e6:.1f} uA -> P = {P*1e6:.1f} uW @ {VDD} V (analog core PEX + digital gate-level, one supply, real activity)")
print(f"FoM_W = {P/(2**enob*FS)*1e15:.1f} fJ/conv-step ; FoM_S = {sndr + 10*np.log10(FS/2/P):.1f} dB")
