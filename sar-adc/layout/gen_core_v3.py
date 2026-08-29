#!/usr/bin/env python3
"""OA-SAR8 core v3 FINAL: compact symmetric stack with the switch row.
top->bottom: replica CDAC (Y-mirror) | comparator | main CDAC | switch row x9 | SAR logic"""
import pya

layout = pya.Layout()
layout.technology_name = "sg13g2"
layout.dbu = 0.001
top = layout.create_cell("oa_sar8_core")

layout.read("cdac_array.gds")
layout.read("cmp/sa_comp.gds")
layout.read("sw/sw_bitcell.gds")
layout.read("/foss/designs/sar-adc/logic/final/gds/sar_ctrl.gds")
cd = layout.cell("cdac_array")
cp = layout.cell("sa_comp")
sw = layout.cell("sw_bitcell")
lg = layout.cell("sar_ctrl")

xc = 36.5
top.insert(pya.DCellInstArray(lg.cell_index(), pya.DTrans(pya.DVector(xc - 65, -160))))
# switch row: 9 bitcells, 13.0um pitch, under the CDAC rail exits
for i in range(9):
    top.insert(pya.DCellInstArray(sw.cell_index(), pya.DTrans(pya.DVector(-21.0 + i * 13.0, -27.0))))
top.insert(pya.DCellInstArray(cd.cell_index(), pya.DTrans(pya.DVector(0, 0))))
top.insert(pya.DCellInstArray(cp.cell_index(), pya.DTrans(pya.DVector(xc, 110.4))))
top.insert(pya.DCellInstArray(cd.cell_index(), pya.DTrans(0, True, pya.DVector(0, 244.2))))

layout.write("oa_sar8_core_v3.gds")
b = top.dbbox()
print(f"core v3 bbox: {b.width():.0f} x {b.height():.0f} um = {b.width()*b.height()/1e6:.3f} mm2")
