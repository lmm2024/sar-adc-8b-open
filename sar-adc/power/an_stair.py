#!/usr/bin/env python3
"""Analyse staircase runs with top-plate voltages saved: per conversion print the code,
the ideal, and the analog sampling error measured directly at the MSB trial."""
import sys, numpy as np
names = ['done','r7','r6','r5','r4','r3','r2','r1','r0','trk','hold','vinp','vinn','i','outp','outn','clkcmp','topr','topm']   # PEX: sw_tg_0.bot = replica top (topr), cdac_array_1.topp = main top (topm)
c = {n: 1+2*i for i,n in enumerate(names)}
for f in sys.argv[1:]:
    d = np.loadtxt(f); t = d[:,0]
    done = d[:,c['done']]; trk = d[:,c['trk']]; hold = d[:,c['hold']]
    hi = done > 0.75; edges = [e for e in (np.where(hi[1:] & ~hi[:-1])[0]+1) if t[e] > 5e-9]
    hh = hold > 0.75; hrise = t[np.where(hh[1:] & ~hh[:-1])[0]+1]
    th = trk > 0.75; tfall = t[np.where(~th[1:] & th[:-1])[0]+1]
    def at(name, tt):
        k = np.searchsorted(t, tt); return d[min(k, len(t)-1), c[name]]
    print('==', f)
    for j, e in enumerate(edges):
        k = np.searchsorted(t, t[e]+1e-9)
        code = int(''.join('1' if d[k,c['r%d'%b]]>0.75 else '0' for b in range(7,-1,-1)),2)
        ta = tfall[tfall < t[e]][-1]; thold = hrise[(hrise > ta) & (hrise < t[e])][0]
        D = at('vinp', ta) - at('vinn', ta)
        ideal = D/1.5*128 + 127.5
        pre = at('topr', ta-0.3e-9) - at('topm', ta-0.3e-9)      # tracking residual (should be 0)
        pm, pr = at('topm', ta-0.3e-9), at('topr', ta-0.3e-9)
        post = at('topr', ta+2.0e-9) - at('topm', ta+2.0e-9)     # after switches open, before hold
        msb = at('topr', thold+4.0e-9) - at('topm', thold+4.0e-9)  # at MSB trial (DAC settled)
        exp_msb = D - 1.5/256
        print(f' conv{j} D={D:+.3f} code={code:3d} ideal={ideal:6.2f} err={code-ideal:+.2f} | track-res topm={pm-0.75:+.4f} topr={pr-0.75:+.4f} d={pre:+.4f} | post-open d={post:+.4f} | MSB d={msb:+.4f} exp={exp_msb:+.4f} samp-err={ (msb-exp_msb)*1e3:+.2f} mV ({(msb-exp_msb)/0.01172:+.2f} LSB)')
