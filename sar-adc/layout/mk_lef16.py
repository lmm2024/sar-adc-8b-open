#!/usr/bin/env python3
"""Generate an abstract LEF + Verilog blackbox for oa_sar8_core16 from its GDS.
PIN geometry = pin-layer boxes carrying a label; OBS = merged drawing per layer
(minus pin boxes) so the top-level router avoids the macro internals."""
import pya

CELL = "oa_sar8_core16"
LAYERS = {8: "Metal1", 10: "Metal2", 30: "Metal3", 50: "Metal4", 67: "Metal5",
          126: "TopMetal1", 134: "TopMetal2"}
POWER = {"VDD": "POWER", "VSS": "GROUND"}
INPUTS = {"vinp", "vinn", "vcm", "clk", "rst_n", "start"}

ly = pya.Layout()
ly.read(f"{CELL}.gds")
top = ly.cell(CELL)
bb = top.dbbox()
# shift the whole macro so its lower-left sits at (0,0): LibreLane/OpenROAD want FOREIGN 0 0
shift = pya.DTrans(pya.DVector(-bb.left, -bb.bottom))
for ld in ly.layer_indexes():
    top.shapes(ld).transform(shift)
for inst in top.each_inst():
    inst.transform(shift)
bb = top.dbbox()
assert abs(bb.left) < 1e-6 and abs(bb.bottom) < 1e-6, bb
top.shapes(ly.layer(189, 0)).insert(pya.DBox(0, 0, bb.right, bb.top))   # prBoundary
ox, oy = 0.0, 0.0
W, H = bb.width(), bb.height()
opts = pya.SaveLayoutOptions()
opts.set_format_from_filename(f"{CELL}_lef.gds")
opts.add_cell(top.cell_index())
ly.write(f"{CELL}_lef.gds", opts)
print("shifted GDS bbox:", bb)

pins = {}                                   # name -> [(layer, box)]
for lnum, lname in LAYERS.items():
    lp, ll = ly.find_layer(lnum, 2), ly.find_layer(lnum, 25)
    if lp is None or ll is None:
        continue
    boxes = [s.dbbox() for s in top.shapes(lp).each() if s.is_box()]
    for s in top.shapes(ll).each():
        if not s.is_text():
            continue
        t = s.dtext
        name = t.string
        p = pya.DPoint(t.x, t.y)
        for b in boxes:
            if b.contains(p) or b.enlarged(0.05, 0.05).contains(p):
                pins.setdefault(name, []).append((lname, b))
                break

lines = ["VERSION 5.7 ;", "  NOWIREEXTENSIONATPIN ON ;", '  DIVIDERCHAR "/" ;', '  BUSBITCHARS "[]" ;',
         f"MACRO {CELL}", "  CLASS BLOCK ;", f"  FOREIGN {CELL} 0.000 0.000 ;",
         "  ORIGIN 0.000 0.000 ;", f"  SIZE {W:.3f} BY {H:.3f} ;"]
for name in sorted(pins):
    if name in POWER:
        lines += [f"  PIN {name}", "    DIRECTION INOUT ;", f"    USE {POWER[name]} ;"]
    elif name in INPUTS:
        lines += [f"  PIN {name}", "    DIRECTION INPUT ;", "    USE SIGNAL ;"]
    else:
        lines += [f"  PIN {name}", "    DIRECTION OUTPUT ;", "    USE SIGNAL ;"]
    lines.append("    PORT")
    for lname, b in pins[name]:
        lines += [f"      LAYER {lname} ;",
                  f"        RECT {b.left-ox:.3f} {b.bottom-oy:.3f} {b.right-ox:.3f} {b.top-oy:.3f} ;"]
    lines += ["    END", f"  END {name}"]
# OBS: per-layer merged region minus pin boxes (with a small halo)
lines.append("  OBS")
for lnum, lname in LAYERS.items():
    ld = ly.find_layer(lnum, 0)
    if ld is None:
        continue
    reg = pya.Region(top.begin_shapes_rec(ld))
    if reg.is_empty():
        continue
    reg.merge()
    for name, lst in pins.items():
        for pl, b in lst:
            if pl == lname:
                reg -= pya.Region(pya.DBox(b).enlarged(0.5, 0.5).to_itype(ly.dbu))
    lines.append(f"    LAYER {lname} ;")
    for p in reg.each_merged():
        b = p.bbox().to_dtype(ly.dbu)
        lines.append(f"      RECT {b.left-ox:.3f} {b.bottom-oy:.3f} {b.right-ox:.3f} {b.top-oy:.3f} ;")
lines += ["  END", f"END {CELL}", "END LIBRARY"]
open(f"{CELL}.lef", "w").write("\n".join(lines) + "\n")
print("LEF pins:", sorted(pins), "size", W, H, "origin", ox, oy)

# Verilog blackbox
ports = []
for name in sorted(pins):
    ports.append(name)
vh = [f"module {CELL} (", "`ifdef USE_POWER_PINS", "    inout VDD,", "    inout VSS,", "`endif"]
sig = [p for p in ports if p not in POWER and not p.startswith("result[")]
sig.append("[7:0] result")
for i, p in enumerate(sig):
    d = "input " if p in INPUTS else "output"
    vh.append(f"    {d} {p}" + ("," if i < len(sig) - 1 else ""))
vh += [");", "endmodule"]
open(f"{CELL}.v", "w").write("\n".join(vh) + "\n")
print("wrote", f"{CELL}.v")
