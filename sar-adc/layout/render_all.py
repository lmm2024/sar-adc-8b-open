import pya, sys
jobs = [
    ("cdac_array.gds", "cdac_array", "01_cdac_array.png"),
    ("cmp/sa_comp.gds", "sa_comp", "02_comparator.png"),
    ("sw/sw_bitcell10.gds", "sw_bitcell10", "03_switch_bitcell.png"),
    ("sw/sw_tg.gds", "sw_tg", "04_switch_tg.png"),
    ("bs/bstrap.gds", "bstrap", "05_bootstrap.png"),
    ("/foss/designs/sar-adc/logic/final/gds/sar_ctrl.gds", "sar_ctrl", "06_sar_logic.png"),
    ("oa_sar8_acore9.gds", "oa_sar8_acore9", "07_analog_core.png"),
    ("oa_sar8_core11.gds", "oa_sar8_core11", "08_full_core.png"),
]
for gds, cell, png in jobs:
    lv = pya.LayoutView()
    lv.load_layout(gds, 0)
    lv.max_hier()
    for l in lv.each_layer():
        l.visible = True
    lv.zoom_fit()
    lv.save_image("/foss/designs/sar-adc/report/img/" + png, 2400, 1600)
    print("rendered", png)
