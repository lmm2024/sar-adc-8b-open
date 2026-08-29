import pya
gds = '/foss/designs/sar-chip/flow/librelane/runs/RUN_2026-08-15_20-52-37/final/gds/chip_top.gds'
lv = pya.LayoutView()
lv.load_layout(gds, 0)
lv.max_hier()
for l in lv.each_layer():
    s = l.source
    l.visible = True
    for bad in ('63/0', '189/0', '235/0', '235/4', '63/4'):
        if s.startswith(bad + '@') or s.startswith(bad + ' '):
            l.visible = False
lv.zoom_box(pya.DBox(560, 620, 960, 900))
lv.save_image('/foss/designs/sar-adc/report/img/10_full_chip_core_zoom.png', 2400, 1680)
lv.zoom_box(pya.DBox(0, 0, 500, 500))
lv.save_image('/foss/designs/sar-adc/report/img/11_full_chip_corner_pads.png', 2400, 2400)
print('rendered')
