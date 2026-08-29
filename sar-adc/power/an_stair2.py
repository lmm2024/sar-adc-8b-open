#!/usr/bin/env python3
"""Decompose the closed-loop sampling error: d_pre = topr-topm just before hold (hi-Z window,
after the switches opened), d_msb = at MSB trial (hold+4ns); S = d_msb - d_pre = the part revealed
by the DAC step (sampled charge x DAC), gain_eff = S/(D-VDD/256)."""
import sys, numpy as np
names = ['done','r7','r6','r5','r4','r3','r2','r1','r0','trk','hold','vinp','vinn','i','outp','outn','clkcmp','topr','topm']
c = {n: 1+2*i for i,n in enumerate(names)}
rows = []
for f in sys.argv[1:]:
    d = np.loadtxt(f); t = d[:,0]
    done = d[:,c['done']]; trk = d[:,c['trk']]; hold = d[:,c['hold']]
    hi = done > 0.75; edges = [e for e in (np.where(hi[1:] & ~hi[:-1])[0]+1) if t[e] > 5e-9]
    hh = hold > 0.75; hrise = t[np.where(hh[1:] & ~hh[:-1])[0]+1]
    th = trk > 0.75; tfall = t[np.where(~th[1:] & th[:-1])[0]+1]
    def at(name, tt):
        k = np.searchsorted(t, tt); return d[min(k, len(t)-1), c[name]]
    for j, e in enumerate(edges):
        k = np.searchsorted(t, t[e]+1e-9)
        code = int(''.join('1' if d[k,c['r%d'%b]]>0.75 else '0' for b in range(7,-1,-1)),2)
        ta = tfall[tfall < t[e]][-1]; thold = hrise[(hrise > ta) & (hrise < t[e])][0]
        D = at('vinp', ta) - at('vinn', ta)
        pre_top = (at('topm', ta-0.3e-9)-0.75, at('topr', ta-0.3e-9)-0.75)
        d_pre = at('topr', thold-0.3e-9) - at('topm', thold-0.3e-9)
        cm_pre = (at('topr', thold-0.3e-9) + at('topm', thold-0.3e-9))/2 - 0.75
        d_msb = at('topr', thold+4.0e-9) - at('topm', thold+4.0e-9)
        S = d_msb - d_pre; g = S/(D - 1.5/256)
        err = d_msb - (D - 1.5/256)
        rows.append((f.split('_')[1] if '_' in f else f, j, D, code, code-(D/1.5*128+127.5), 1e3*d_pre, 1e3*cm_pre, 1e3*d_msb, g, 1e3*err))
print(f"{'run':>8} {'j':>2} {'D':>6} {'code':>4} {'cerr':>5} | {'d_pre':>7} {'cm_pre':>7} | {'d_msb':>8} {'gain_eff':>8} | {'err':>7}")
for r in rows:
    print(f"{r[0]:>8} {r[1]:>2} {r[2]:+6.2f} {r[3]:>4} {r[4]:+5.2f} | {r[5]:+7.2f} {r[6]:+7.2f} | {r[7]:+8.2f} {r[8]:8.4f} | {r[9]:+7.2f}")
