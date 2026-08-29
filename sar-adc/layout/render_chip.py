import pya
gds = "/foss/designs/sar-chip/flow/librelane/runs/RUN_2026-08-15_20-52-37/final/gds/chip_top.gds"
lv = pya.LayoutView()
lv.load_layout(gds, 0)
lv.max_hier()
for l in lv.each_layer():
    l.visible = True
lv.zoom_fit()
lv.save_image("/foss/designs/sar-adc/report/img/09_full_chip.png", 2400, 2400)
# zoom on the core macro region
lv.zoom_box(pya.DBox(560, 600, 960, 900))
lv.save_image("/foss/designs/sar-adc/report/img/10_full_chip_core_zoom.png", 2400, 1800)
print("rendered chip")
