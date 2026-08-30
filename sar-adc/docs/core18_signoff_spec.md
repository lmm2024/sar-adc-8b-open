# OA-SAR8 core18 release specification

## Scope

This is an 8-bit fully differential SAR ADC in IHP SG13G2. The released core
combines the transistor-level sampling/CDAC/comparator front end with a
standard-cell digital asynchronous SAR controller. Only the sample clock is
external; no behavioral bit clock, digital calibration, or `#` delay is used
in the extracted closed-loop simulation.

## Accepted operating point

| Item | Released value |
|---|---|
| Process corner | TT (`mos_tt + cap_typ`) |
| Supply | 1.5 V |
| Temperature | 27 °C |
| Resolution | 8 bit |
| Sampling rate | 10 MS/s |
| TRACK duration | 25 ns |
| Differential input common mode | 0.75 V |
| Dynamic input | 4.6875 MHz, 0.70 V peak per side |
| Full-RC PEX ENOB | 7.9607 bit |
| Full-RC PEX SNDR | 49.6832 dB |
| ENOB acceptance threshold | ≥7.95 bit |

At 312.5 kHz input with all other conditions unchanged, the continuous PEX
run measures 47.3143 dB SNDR / 7.5672-bit ENOB and completes 33/33 conversions.

The 10.5 MS/s phase-equivalent screen completes every conversion but measures
7.7755-bit ENOB, so it is not an accepted operating point. Single-conversion
smoke tests at 12–18 MS/s demonstrate sequence completion only.

## Physical acceptance

- Complete-core LVS: MATCH.
- Complete-core maximum/block DRC: 0.
- Digital macro DRC/LVS/antenna: pass.
- Full-RC extraction: Magic `m=3`, coupling threshold 10000, resistance
  threshold 1000, hierarchy option 1.
- Bare-macro full-rule density markers are resolved during filled full-chip
  integration and are not waived as geometry errors.

## Verification boundary

The released ENOB is deterministic TT PEX performance. It does not replace
PVT, mismatch, transient-noise, extracted IR-drop/EM, package, or silicon
characterization. Those are future sign-off extensions and must be reported
separately from the released typical-corner result.
