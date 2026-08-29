import pya

lv = pya.LayoutView()
lv.load_layout("oa_sar8_core9.gds", 0)
lv.max_hier()
for l in lv.each_layer():
    l.visible = True
lv.zoom_fit()
lv.save_image("oa_sar8_core9.png", 2600, 1560)
print("rendered oa_sar8_core9.png")
