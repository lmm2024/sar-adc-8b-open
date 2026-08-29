import pya
gds = "/foss/designs/sar-chip/flow/librelane/runs/RUN_2026-08-15_20-52-37/final/gds/chip_top.gds"
lv = pya.LayoutView()
lv.load_layout(gds, 0)
lv.max_hier()
for l in lv.each_layer():
    src = l.source
    # hide annotation/text/registration layers: keep only drawing (dt 0) of metal/via/device layers
    l.visible = ('/0' in src) and not src.startswith('63/') and not src.startswith('189/') and not src.startswith('235/')
lv.zoom_fit()
lv.save_image("/foss/designs/sar-adc/report/img/09_full_chip.png", 2400, 2400)
lv.zoom_box(pya.DBox(560, 620, 960, 900))
lv.save_image("/foss/designs/sar-adc/report/img/10_full_chip_core_zoom.png", 2400, 1680)
lv.zoom_box(pya.DBox(0, 0, 500, 500))
lv.save_image("/foss/designs/sar-adc/report/img/11_full_chip_corner_pads.png", 2400, 2400)
print("rendered")
