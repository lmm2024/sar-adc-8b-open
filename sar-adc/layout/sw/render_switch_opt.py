import pya

lv = pya.LayoutView()
lv.load_layout("sw_bitcell_opt_term.gds", 0)
lv.max_hier()
for layer in lv.each_layer():
    layer.visible = layer.source_layer in (10, 29, 30)
lv.zoom_fit()
lv.save_image("sw_bitcell_opt_term_metals.png", 2400, 1600)
print("wrote sw_bitcell_opt_term_metals.png")
