#!/usr/bin/env python3
"""Render the final optimized asynchronous SAR ADC layout."""
import pya


view = pya.LayoutView()
view.load_layout("oa_sar8_core18_final.gds", 0)
view.max_hier()
view.set_config("grid-visible", "false")
view.set_config("text-visible", "false")
view.zoom_fit()
view.save_image("oa_sar8_core18_final.png", 2600, 1900)
print("wrote oa_sar8_core18_final.png")
