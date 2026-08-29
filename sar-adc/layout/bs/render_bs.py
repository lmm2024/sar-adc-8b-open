import pya

lv = pya.LayoutView()
lv.load_layout("bstrap.gds", 0)
lv.max_hier()
for l in lv.each_layer():
    l.visible = True
lv.zoom_fit()
lv.save_image("bstrap.png", 2600, 1560)
print("rendered bstrap.png")
