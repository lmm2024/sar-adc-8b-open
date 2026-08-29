# Report images for the v4/harden_v9/acore12/core15 state. Run in the container:
#   klayout -zz -r render_v15.py [-rd chip=<chip_top.gds>]
import pya
OUT = "/foss/designs/sar-adc/report/img/"
jobs = [
    ("cdac_array.gds", "cdac_array", "01_cdac_array.png"),
    ("cmp/sa_comp.gds", "sa_comp", "02_comparator.png"),
    ("sw/sw_bitcell11.gds", "sw_bitcell11", "03_switch_bitcell.png"),
    ("sw/sw_tg.gds", "sw_tg", "04_switch_tg.png"),
    ("bs/bstrap40.gds", "bstrap40", "05_bootstrap.png"),
    ("/foss/designs/sar-adc/logic/final/gds/sar_ctrl.gds", "sar_ctrl", "06_sar_logic.png"),
    ("oa_sar8_acore13.gds", "oa_sar8_acore13", "07_analog_core.png"),
    ("oa_sar8_core16.gds", "oa_sar8_core16", "08_full_core.png"),
]
for gds, cell, png in jobs:
    lv = pya.LayoutView()
    lv.load_layout(gds, 0)
    lv.max_hier()
    for l in lv.each_layer():
        l.visible = True
    lv.zoom_fit()
    lv.save_image(OUT + png, 2400, 1600)
    print("rendered", png)
try:
    chip
except NameError:
    chip = ""
if chip:
    lv = pya.LayoutView()
    lv.load_layout(chip, 0)
    lv.max_hier()
    for l in lv.each_layer():
        src = l.source
        l.visible = ('/0' in src) and not src.startswith('63/') and not src.startswith('189/') and not src.startswith('235/')
    lv.zoom_box(pya.DBox(0, 0, 1600, 1600))          # top cell carries a huge registration box: zoom to the die
    lv.save_image(OUT + "09_full_chip.png", 2400, 2400)
    lv.zoom_box(pya.DBox(560, 620, 960, 900))
    lv.save_image(OUT + "10_full_chip_core_zoom.png", 2400, 1680)
    lv.zoom_box(pya.DBox(0, 0, 500, 500))
    lv.save_image(OUT + "11_full_chip_corner_pads.png", 2400, 2400)
    print("rendered chip")
