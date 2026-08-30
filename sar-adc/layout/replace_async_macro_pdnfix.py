#!/usr/bin/env python3
"""Replace only the async macro inside the frozen 7.9643-bit top-level GDS.

The signed-off analog hierarchy and all top-level routes are read from the
formal GDS.  The existing ``sar_ctrl_async_phys`` cell is then cleared and
repopulated from the candidate macro in a separate Layout object.  This avoids
cell-name conflict side effects from rebuilding the whole mixed-signal layout.
"""
from pathlib import Path

import pya


HERE = Path(__file__).resolve().parent
FORMAL_GDS = HERE / "oa_sar8_core18_final_base_7p9643.gds"
CANDIDATE_MACRO_GDS = (
    HERE.parent / "logic" / "final_async_phys" / "gds"
    / "sar_ctrl_async_phys.gds"
)
OUT_GDS = HERE / "oa_sar8_core18_final.gds"


top_layout = pya.Layout()
top_layout.read(str(FORMAL_GDS))
macro_layout = pya.Layout()
macro_layout.read(str(CANDIDATE_MACRO_GDS))

top = top_layout.cell("oa_sar8_core18_final")
old_macro = top_layout.cell("sar_ctrl_async_phys")
new_macro = macro_layout.cell("sar_ctrl_async_phys")
if top is None or old_macro is None or new_macro is None:
    raise RuntimeError("required top or macro cell is missing")
if old_macro.dbbox() != new_macro.dbbox():
    raise RuntimeError(
        f"candidate macro bbox changed: formal={old_macro.dbbox()}, "
        f"candidate={new_macro.dbbox()}"
    )

parent_refs = sum(1 for _ in old_macro.each_parent_inst())
if parent_refs != 1:
    raise RuntimeError(f"expected one async-macro parent instance, got {parent_refs}")

old_macro.clear()
old_macro.copy_tree(new_macro)

# The frozen top uses the compact M2-to-M5 ``via_stack$1`` helper twice.  Its
# M3/M4 landing rectangles are only 0.058 um^2 inside the helper hierarchy;
# the surrounding 0.4-um top-level pads make the electrical connection valid,
# but the maximal hierarchical DRC does not union those parent shapes when it
# evaluates the child's minimum-area rule.  Match the already-present parent
# pad footprint inside the helper so M3.d/M4.d are satisfied without changing
# connectivity or placement.
via_cell = top_layout.cell("via_stack$1")
if via_cell is None:
    raise RuntimeError("via_stack$1 helper is missing")
for layer_number in (30, 50):  # Metal3 and Metal4
    via_cell.shapes(top_layout.layer(layer_number, 0)).insert(
        pya.DBox(-0.2, -0.2, 0.2, 0.2)
    )

top_layout.write(str(OUT_GDS))
print(f"wrote {OUT_GDS}")
print(f"candidate macro: {CANDIDATE_MACRO_GDS}")
print(f"macro bbox: {new_macro.dbbox()}")
print(f"top bbox: {top.dbbox()}")
