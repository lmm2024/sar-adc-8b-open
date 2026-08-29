import pya
layout = pya.Layout(); layout.technology_name = "sg13g2"; layout.dbu = 0.001
top = layout.create_cell("tdev")
lib = pya.Library.library_by_name("SG13_dev", "sg13g2")
decl = lib.layout().pcell_declaration("rfnmos")
params = {p.name: p.default for p in decl.get_parameters()}
params.update({"w": "2.0u", "l": "0.15u", "ng": "2"})
c = layout.create_cell("rfnmos", "SG13_dev", params)
top.insert(pya.DCellInstArray(c.cell_index(), pya.DTrans()))
lm1, lm1p, lm1l = layout.layer(8,0), layout.layer(8,2), layout.layer(8,25)
lm2, lm2p, lm2l = layout.layer(10,0), layout.layer(10,2), layout.layer(10,25)
def lab(lay_lbl, lay_pin, x, y, name):
    top.shapes(lay_pin).insert(pya.DBox(x-0.08, y-0.08, x+0.08, y+0.08))
    top.shapes(lay_lbl).insert(pya.DText(name, pya.DTrans(pya.DVector(x, y))))
# candidates from probe: vertical col (0.86, 1.9); horiz bar1 (1.6, 1.40); horiz bar2 (1.6, 1.93); M2 top bar (1.6, 2.46); guard bottom (1.6, 0.19)
lab(lm1l, lm1p, 0.86, 1.9, "t_vcol")
lab(lm1l, lm1p, 1.64, 1.40, "t_bar1")
lab(lm1l, lm1p, 1.64, 1.93, "t_bar2")
lab(lm2l, lm2p, 1.64, 2.46, "t_m2top")
lab(lm1l, lm1p, 1.64, 0.19, "t_guard")
layout.write("tdev.gds")
print("ok")
