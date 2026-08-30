# PEX hotspot diagnosis and PDN-only repair

## Failure signature

The frozen 7.9643-bit GDS reproduced a deterministic ngspice
`timestep too small` failure for a 312.5 kHz input near 41.4705 ns, before the
first DONE pulse. Parasitic bisection localized the numerical/electrical
hotspot to `xdut.a_26364_45710#`, a high-fanout asynchronous-control output in
the digital macro. The failure was input-trajectory dependent, which explains
why the near-Nyquist 10 MS/s record could pass while the low-frequency record
failed.

The original digital macro was only 65 µm wide, while the PDN pitch was
75.6 µm. The MSB-side output circuitry therefore returned through roughly
33 µm of local Metal1 to the only useful VSS stripe. Full-RC extraction turned
that return path into a sensitive nonlinear switching node.

## Rejected repair

A one-sided `sg13g2_buf_2` on the MSB output removed the immediate numerical
failure but changed a critical output sample from code 14 to 15. The complete
32-point record fell to 7.7237-bit ENOB, so that circuit-level change was
rejected.

## Released repair

The accepted candidate keeps the RTL, cell logic, and SAR signal path intact.
It changes only the digital macro PDN:

- vertical/horizontal pitch: 75.6 µm → 30 µm;
- local VSS stripe: x=55.08 µm;
- MSB output buffer: x=58.08 µm;
- approximate local return distance: 33 µm → 3 µm.

The new macro was substituted into the frozen top-level GDS in place, keeping
the analog hierarchy and top-level signal routing unchanged. The existing
hierarchical `via_stack$1` M3/M4 minimum-area pads were then reapplied.

## A/B evidence

- Old GDS, 312.5 kHz: failure at about 41.4705 ns, 0 DONE.
- PDN-fixed GDS, same low-frequency two-cycle test: 2/2 conversions, codes
  137 and 160, conversion time 34.45–34.54 ns, no timestep or singular-matrix
  error.
- PDN-fixed GDS, 10 MS/s continuous 33-conversion FFT: 49.6832 dB SNDR,
  7.9607-bit ENOB.
- Frozen reference, same 10 MS/s test: 49.7050 dB SNDR, 7.9643-bit ENOB.

This is why the repair is treated as a physical power-integrity correction,
not an algorithmic or behavioral workaround.
