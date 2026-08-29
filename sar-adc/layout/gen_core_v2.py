#!/usr/bin/env python3
"""OA-SAR8 core v2: COMPACT SYMMETRIC stack.
bottom->top: SAR logic | main CDAC | comparator strip | replica CDAC (Y-mirror).
The two CDACs mirror about the comparator axis -> matched, short, symmetric
top-plate connections by construction."""
import pya

layout = pya.Layout()
layout.technology_name = "sg13g2"
layout.dbu = 0.001
top = layout.create_cell("oa_sar8_core")

layout.read("cdac_array.gds")
layout.read("cmp/sa_comp.gds")
layout.read("/foss/designs/sar-adc/logic/final/gds/sar_ctrl.gds")
cd = layout.cell("cdac_array")
cp = layout.cell("sa_comp")
lg = layout.cell("sar_ctrl")

xc = 36.5                                # common vertical axis
# SAR logic at the bottom (130x110), centered
top.insert(pya.DCellInstArray(lg.cell_index(), pya.DTrans(pya.DVector(xc - 65, -121))))
# main CDAC: y -3..103
top.insert(pya.DCellInstArray(cd.cell_index(), pya.DTrans(pya.DVector(0, 0))))
# comparator strip centered on the axis, just above the main array
top.insert(pya.DCellInstArray(cp.cell_index(), pya.DTrans(pya.DVector(xc, 110.4))))
# replica CDAC: mirrored about the horizontal axis (M0), stacked above
top.insert(pya.DCellInstArray(cd.cell_index(), pya.DTrans(0, True, pya.DVector(0, 244.2))))

layout.write("oa_sar8_core_v2.gds")
b = top.dbbox()
print(f"core bbox: {b}  ->  {b.width():.0f} x {b.height():.0f} um")
