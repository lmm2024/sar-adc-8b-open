import pya
ly = pya.Layout()
ly.read("final/gds/sar_ctrl.gds")
top_ = ly.cell("sar_ctrl")
print("bbox:", top_.dbbox())
for lnum, lname in ((8, "M1"), (10, "M2"), (30, "M3"), (50, "M4"), (67, "M5")):
    for ld in ly.layer_indexes():
        info = ly.get_info(ld)
        if info.layer == lnum and info.datatype == 25:
            for s in top_.shapes(ld).each():
                if s.is_text():
                    t = s.dtext
                    print(f"{lname} {t.string:14s} x={t.x:8.2f} y={t.y:8.2f}")
