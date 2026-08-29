import pya

ly = pya.Layout()
ly.read("oa_sar8_core3.gds")
top_ = ly.cell("oa_sar8_core3")
drop = ("sa_comp", "sw_bitcell", "sw_tg", "sar_ctrl")
n = 0
for host in (top_, ly.cell("oa_sar8_acore3")):
    for inst in list(host.each_inst()):
        if inst.cell.name in drop:
            inst.delete()
            n += 1
print("removed", n, "active-cell instances")
for lnum in (8, 10, 30):                       # drop dangling pin boxes + labels
    for dt in (2, 25):                          # (digital re-exports, old pins)
        ld = ly.find_layer(lnum, dt)
        if ld is not None:
            top_.shapes(ld).clear()
print("cleared top-level pin/label shapes")

m3l = ly.layer(30, 25)
tm1l = ly.layer(126, 25)
SW_X = {"term": 4.0, "b0": 17.8, "b1": 31.6, "b2": 45.4, "b3": 59.2,
        "b4": 73.0, "b5": 86.8, "b6": 198.0, "b7": 211.8}
NETS = ["b7", "b6", "b5", "b4", "b3", "b2", "b1", "b0", "term"]
FAN_Y = {nm: -24.4 - i * 1.3 for i, nm in enumerate(NETS)}
for nm in NETS:
    top_.shapes(m3l).insert(pya.DText(nm, pya.DTrans(
        pya.DVector(SW_X[nm] + 0.2, FAN_Y[nm]))))
top_.shapes(m3l).insert(pya.DText("topp", pya.DTrans(pya.DVector(100.0, -36.5))))
top_.shapes(m3l).insert(pya.DText("trkb", pya.DTrans(pya.DVector(100.0, -14.9))))
top_.shapes(tm1l).insert(pya.DText("topr", pya.DTrans(pya.DVector(250.0, 114.9))))

top_.name = "oa_sar8_pas3"
ly.write("oa_sar8_pas3.gds")
print("wrote oa_sar8_pas3.gds", top_.dbbox())
