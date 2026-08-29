# Verified results

All entries below use the checked-in `oa_sar8_core18_final.pex.spice` (Magic full-RC, m=3), IHP SG13G2 TT (`mos_tt + cap_typ`), 1.5 V, 27 °C, ngspice `trap`, `reltol=3e-3`, `chgtol=1e-13`, `rshunt=1e11`, `tstep=0.05 ns`, 33 conversions and a 32-point FFT with tone bin 15.

| Test | Samples | SNDR (dB) | ENOB (bit) | Status |
|---|---:|---:|---:|---|
| 10 MS/s, TRACK=25 ns | 33/33 | 49.7050 | 7.9643 | sign-off |
| 10.5 MS/s, TRACK=25 ns | 33/33 | 47.8904 | 7.6629 | speed A/B |
| 10.5 MS/s, TRACK=30 ns | 33/33 | 48.4165 | 7.7503 | speed A/B |
| 10.5 MS/s, TRACK=40 ns | 33/33 | 46.8753 | 7.4942 | speed A/B |

The 10.5 MS/s tests complete all asynchronous conversions; their ENOB loss is therefore associated mainly with sampling/settling and input-aperture behavior, not an incomplete SAR sequence. No 10.5 MS/s result is claimed as a sign-off result.

Compact metrics and sample-code CSV files are under `results/core18_pex/`.
