# Verified results

## Released PDN-fixed core18

Unless noted otherwise, results use the checked-in
`oa_sar8_core18_final.pex.spice` (Magic full-RC, `m=3`), IHP SG13G2 TT
(`mos_tt + cap_typ`), 1.5 V, 27 °C, ngspice `trap`, `reltol=3e-3`,
`chgtol=1e-13`, `rshunt=1e11`, and `tstep=0.05 ns`.

| Test | Result |
|---|---:|
| Sampling rate | **10 MS/s** |
| Input | 4.6875 MHz, 0.70 V single-ended amplitude |
| Completed conversions | 33/33 |
| FFT | 32 points, coherent bin 15 |
| SNDR | **49.6832 dB** |
| ENOB | **7.9607 bit** |
| SFDR | **57.1875 dB** |
| THD (2nd–5th) | **−55.3358 dB** |
| Conversion time | 34.30–34.93 ns, mean 34.56 ns |
| Average VDD current | 398.32 µA |
| Average power | 597.48 µW |
| Walden FoM | 239.84 fJ/conv-step |
| Schreier FoM | 148.91 dB |

Power is integrated from the first valid TRACK falling edge through the last
DONE rising edge, matching the original repository's reporting convention.

The frozen pre-fix reference measured 49.7050 dB / 7.9643 bit. The released
PDN fix therefore changes ENOB by only −0.0036 bit while removing the known
low-frequency PEX convergence hotspot.

## Low-frequency dynamic result

The baseline-aligned low-frequency test uses the same 10 MS/s clock,
TRACK=25 ns, amplitude, solver, 33 continuous conversions, and 32-point FFT;
only the coherent tone changes to bin 1 (312.5 kHz).

| Metric | Result |
|---|---:|
| Completed conversions | 33/33 |
| SNDR | 47.3143 dB |
| ENOB | 7.5672 bit |
| SFDR | 54.3107 dB |
| THD (2nd–5th) | −55.7824 dB |
| Average power | 596.90 µW |
| Walden FoM | 314.74 fJ/conv-step |
| Schreier FoM | 146.55 dB |

This run completes without the old `timestep too small` failure and improves
on the Arcadia baseline's 7.40-bit low-frequency result. It is lower than the
near-Nyquist result, so the near-Nyquist number must not be treated as a
frequency-independent guarantee. The deterministic 32-point record remains
sensitive to static curvature, sample-history effects, and the placement of
harmonics in the short coherent FFT.

## Speed boundary

| Test | Method | ENOB | Status |
|---|---|---:|---|
| 10 MS/s, TRACK=25 ns | continuous 33-conversion sign-off | **7.9607** | pass |
| 10.5 MS/s, TRACK=25 ns | 32 independent phase-equivalent PEX conversions | 7.7755 | below 7.95 target |
| 12/14/16/18 MS/s | one-cycle PEX smoke | not an FFT result | conversion completes |

The highest sampling rate currently accepted against ENOB ≥ 7.95 bit is
therefore **10 MS/s**. One-cycle completion at higher rates is not presented
as an ENOB claim.

## Physical verification

- Digital asynchronous macro: DRC pass, LVS pass, antenna pass.
- Digital macro reports one max-fanout constraint warning; max slew, max
  capacitance, and routed-geometry violation counts are zero.
- Complete core: LVS MATCH.
- Complete core block-level maximum DRC: 0.
- Complete core regular DRC: 9 density/fill markers because this is a bare
  macro, not a filled full-chip context. There are no spacing, short, or
  connectivity errors in the maximum rule-set run.
- PEX: Magic full RC with `-m 3 -t 10000 -r 1000 -y 1`.

## Baseline comparison

| Metric | Arcadia baseline | Released core18 | Change |
|---|---:|---:|---:|
| Near-Nyquist SNDR | 45.8 dB | 49.683 dB | +3.88 dB |
| Near-Nyquist ENOB | 7.32 bit | 7.9607 bit | +0.641 bit |
| SFDR | 52.7 dB | 57.188 dB | +4.49 dB |
| THD | −50.6 dB | −55.336 dB | −4.74 dB |
| Power | 488.5 µW | 597.5 µW | +109.0 µW |
| Walden FoM | 305 fJ/step | 239.8 fJ/step | 21.4% lower |
| Schreier FoM | 145.9 dB | 148.91 dB | +3.01 dB |

The original baseline's low-frequency reference was 46.3 dB / 7.40 bit at
312.5 kHz; the released core18 reaches 47.314 dB / 7.567 bit. Static-transfer
results are recorded under `sar-adc/signoff/core18_pdnfix_20260830/` when the
full sweep is complete.
