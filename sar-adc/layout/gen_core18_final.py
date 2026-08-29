#!/usr/bin/env python3
"""Assemble the optimized analog front end and the physical async controller."""
from pathlib import Path


src = Path("gen_core17_async.py").read_text(encoding="utf-8")


def once(old, new):
    global src
    if src.count(old) != 1:
        raise RuntimeError(f"expected one source block, found {src.count(old)}: {old[:80]!r}")
    src = src.replace(old, new)


once('TOP_NAME = "oa_sar8_core17_async"', 'TOP_NAME = "oa_sar8_core18_final"')
once('layout.read("oa_sar8_acore13.gds")', 'layout.read("oa_sar8_acore18_opt.gds")')
once('ac = layout.cell("oa_sar8_acore13")', 'ac = layout.cell("oa_sar8_acore18_opt")')

once('''STUB_X = {0: 7.0, 1: 20.8, 2: 34.6, 3: 48.4,
          4: 62.2, 5: 76.0, 6: 89.8, 7: 103.6}
STUBN_X = {k: 173.2 + 13.8 * (7 - k) for k in range(8)}
DROPN_X = dict(STUBN_X)
DROPN_X[7] = 176.0
DROPN_X[6] = 188.1''', '''STUB_X = {0: -13.52, 1: 1.22, 2: 16.36, 3: 31.90,
    4: 47.84, 5: 64.38, 6: 81.52, 7: 99.26}
P_DROPN_X = {0: -14.32, 1: 0.42, 2: 15.56, 3: 31.10,
             4: 47.04, 5: 63.58, 6: 82.50, 7: 98.46}
STUBN_X = {0: 289.78, 1: 274.64, 2: 259.10, 3: 243.16,
           4: 226.62, 5: 209.48, 6: 191.74, 7: 173.20}
# Short bottom-only M4 drops are moved onto verified empty corridors, then
# jogged on M3 to the exact control pin.
DROPN_X = {0: 288.98, 1: 273.84, 2: 258.30, 3: 243.96,
           4: 225.82, 5: 208.68, 6: 192.50, 7: 170.80}''')

once('''DROP_X_P = [194.6, 195.7, 196.8, 231.0, 201.8, 202.9, 206.7, 207.8]
DROP_X_N = [208.9, 212.7, 213.8, 237.0, 218.7, 219.8, 220.9, 224.7]''', '''DROP_X_P = [194.6, 195.7, 196.8, 231.0, 201.8, 202.9, 206.7, 207.8]
DROP_X_N = [212.7, 218.7, 224.7, 236.7, 242.7, 248.7, 254.7, 266.7]''')

once('''routes.append((f"dac_code_n[{k}]", LY + DACN_Y[k], DROP_X_P[k],
                   TRACK_Y[k], STUB_X[k], STUB_X[k]))''', '''routes.append((f"dac_code_n[{k}]", LY + DACN_Y[k], DROP_X_P[k],
                   TRACK_Y[k], STUB_X[k], P_DROPN_X[k]))''')

# Expand the chip-level supply bars and reconnect the west-shifted analog VSS.
src = src.replace('rect("tm2", -15.0, 133.0, 300.5, 136.0)',
                  'rect("tm2", -45.0, 133.0, 340.0, 136.0)')
src = src.replace('rect("tm2", -15.0, 138.5, 300.5, 141.5)',
                  'rect("tm2", -45.0, 138.5, 340.0, 141.5)')
for old, new in (("-8.6", "-34.9"), ("-8.2", "-34.5"), ("-8.4", "-34.7")):
    src = src.replace(old, new)
src = src.replace('pin("tm2", "VDD", (-15.0, 133.0, 300.5, 136.0), (142.0, 134.5))',
                  'pin("tm2", "VDD", (-45.0, 133.0, 340.0, 136.0), (147.5, 134.5))')
src = src.replace('pin("tm2", "VSS", (-15.0, 138.5, 300.5, 141.5), (142.0, 140.0))',
                  'pin("tm2", "VSS", (-45.0, 138.5, 340.0, 141.5), (147.5, 140.0))')

once('''# Analog input/common-mode exports, matching the corrected core16 geometry.
XW, XE, YS = -15.0, 300.5, -76.0
rect("m3", XW, -43.1, 38.2, -42.7)
pin("m3", "vinp", (XW, -43.1, XW + 1.5, -42.7), (XW + 0.75, -42.9))
rect("m3", 243.8, -43.1, XE, -42.7)
pin("m3", "vinn", (XE - 1.5, -43.1, XE, -42.7), (XE - 0.75, -42.9))''', '''# Precision inputs stay directly on the central-edge bootstrap pins; a pad-ring
# wrapper may lift these later without crossing the MIM capacitors.  Export
# both the label and the pin-purpose rectangle: KLayout LVS can follow the
# child-cell label alone, but Magic PEX requires a top-level pin marker to
# retain vinp/vinn in the flattened subcircuit interface.
YS = -76.0
pin("m3", "vinp", (117.6, -43.1, 118.4, -42.7), (118.0, -42.9))
pin("m3", "vinn", (173.6, -43.1, 174.4, -42.7), (174.0, -42.9))''')

exec(compile(src, "gen_core18_final.expanded.py", "exec"))
