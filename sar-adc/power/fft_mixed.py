#!/usr/bin/env python3
"""Coherent-FFT analysis of the unified mixed-signal post-layout run (tb_mixed4):
codes are read at the 'done' edges, the last NFFT consecutive conversions are used,
fin = BIN/NFFT * fs (coherent, rectangular window). Also reports the average supply
current over the analysed record (single VDD: analog core PEX + gate-level SAR logic)."""
import sys
import numpy as np

CSV = sys.argv[1] if len(sys.argv) > 1 else "/foss/designs/sar-adc/power/mixed4_out.csv"
NFFT = int(sys.argv[2]) if len(sys.argv) > 2 else 32
BIN = int(sys.argv[3]) if len(sys.argv) > 3 else 15
FS = 10e6
VDD = 1.5

d = np.loadtxt(CSV)
t = d[:, 0]
names = ['done', 'r7', 'r6', 'r5', 'r4', 'r3', 'r2', 'r1', 'r0', 'trk', 'hold', 'vinp', 'vinn', 'i', 'outp', 'outn', 'clkcmp']
c = {n: 1 + 2 * i for i, n in enumerate(names)}
done = d[:, c['done']]
hi = done > 0.75
edges = np.where(hi[1:] & ~hi[:-1])[0] + 1
edges = [e for e in edges if t[e] > 5e-9]
codes, tdone, dsamp = [], [], []
trk = d[:, c['trk']]
for e in edges:
    k = np.searchsorted(t, t[e] + 1e-9)
    bits = [1 if d[k, c['r%d' % b]] > 0.75 else 0 for b in range(7, -1, -1)]
    codes.append(int(''.join(map(str, bits)), 2))
    tdone.append(t[e])
    idx = np.where(trk[:e] > 0.75)[0]
    dsamp.append(d[idx[-1], c['vinp']] - d[idx[-1], c['vinn']] if len(idx) else float('nan'))
codes = np.array(codes)
print(f"{len(codes)} conversions; done period = {np.median(np.diff(tdone))*1e9:.2f} ns")
if len(codes) < NFFT + 1:
    print("not enough conversions for the FFT"); sys.exit(0)
x = codes[-NFFT:].astype(float)
ds = np.array(dsamp[-NFFT:])
ideal = ds / 1.5 * 128 + 127.5
print("codes:", x.astype(int).tolist())
print("code - ideal(D@aperture) [LSB]:", np.round(x - ideal, 1).tolist())
X = np.fft.rfft(x - x.mean())
P = np.abs(X) ** 2
sig = P[BIN]
harm = [((BIN * h) % NFFT) for h in range(2, 6)]
harm = [h if h <= NFFT // 2 else NFFT - h for h in harm]
noise_bins = [k for k in range(1, NFFT // 2 + 1) if k != BIN]
noise = sum(P[k] for k in noise_bins)
sndr = 10 * np.log10(sig / noise)
spur = max(P[k] for k in noise_bins)
sfdr = 10 * np.log10(sig / spur)
thd = 10 * np.log10(sum(P[h] for h in set(harm)) / sig)
enob = (sndr - 1.76) / 6.02
amp = np.sqrt(2 * sig) / (NFFT / 2) / 2  # LSB amplitude estimate (rfft scaling): |X|=A*N/2
amp_dbfs = 20 * np.log10(np.sqrt(sig) / (NFFT / 2) / 128.0)
print(f"fin = {BIN/NFFT*FS/1e6:.4f} MHz  fs = {FS/1e6:.1f} MS/s  N = {NFFT}")
print(f"signal {amp_dbfs:.2f} dBFS | SNDR {sndr:.2f} dB | ENOB {enob:.2f} b | SFDR {sfdr:.1f} dB | THD {thd:.1f} dB")
print("harmonic bins:", sorted(set(harm)), "spectrum (dBc):", [round(10*np.log10(P[k]/sig),1) for k in range(1, NFFT//2+1)])
# power over the analysed record (from the first analysed sampling instant to the last done)
i = -d[:, c['i']]
t0, t1 = tdone[-NFFT - 1], tdone[-1]
m = (t >= t0) & (t <= t1)
iavg = np.trapezoid(i[m], t[m]) / (t1 - t0)
print(f"avg supply current {iavg*1e6:.1f} uA over {(t1-t0)*1e6:.2f} us -> P = {iavg*VDD*1e6:.1f} uW @ {VDD} V (analog + digital, one supply)")
fs_eff = 1.0 / np.median(np.diff(tdone))
print(f"FoM_W = {iavg*VDD/(2**enob*fs_eff)*1e15:.1f} fJ/conv-step ; FoM_S = {sndr + 10*np.log10(fs_eff/2/(iavg*VDD)):.1f} dB")
