#!/usr/bin/env python3
"""OA-SAR8 core floorplan: main CDAC + replica CDAC (mirrored, pseudo-diff
matching) + SAR logic macro + comparator site. Verified blocks placed as-is."""
import pya

layout = pya.Layout()
layout.technology_name = "sg13g2"
layout.dbu = 0.001
top = layout.create_cell("oa_sar8_core")

cdac = layout.read("cdac_array.gds")
logic = layout.read("/foss/designs/sar-adc/logic/final/gds/sar_ctrl.gds")
cd = layout.cell("cdac_array")
lg = layout.cell("sar_ctrl")

l_bnd = layout.layer(189, 0)   # prBoundary-ish marker
l_txt = layout.layer(63, 0)

# main CDAC at origin; replica mirrored about x -> matched orientation pair
top.insert(pya.DCellInstArray(cd.cell_index(), pya.DTrans(pya.DVector(0, 0))))
top.insert(pya.DCellInstArray(cd.cell_index(),
                              pya.DTrans(2, True, pya.DVector(230.0, 110.0))))  # R180+mirror

# comparator site between the arrays (from pin-map recon: ~40x25um needed)
top.shapes(l_bnd).insert(pya.DBox(112, 35, 152, 60))
top.shapes(l_txt).insert(pya.DText("COMPARATOR SITE 40x25", pya.DTrans(pya.DVector(114, 47))))

# SAR logic macro below the comparator channel
top.insert(pya.DCellInstArray(lg.cell_index(), pya.DTrans(pya.DVector(112, -130))))

layout.write("oa_sar8_core_fp.gds")
print("floorplan written:", top.dbbox())
