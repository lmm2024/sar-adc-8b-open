import pya

ly = pya.Layout()
ly.read("oa_sar8_core8.gds")
top_ = ly.cell("oa_sar8_core8")
drop = ("sa_comp", "sw_bitcell", "sw_bitcell10", "sw_tg", "bstrap", "sar_ctrl")
n = 0
for host in (top_, ly.cell("oa_sar8_acore7")):
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
SW_X = {"term": -6.1, "b0": 7.7, "b1": 21.5, "b2": 35.3, "b3": 49.1,
        "b4": 62.9, "b5": 76.7, "b6": 90.5, "b7": 104.3}
NETS = ["b7", "b6", "b5", "b4", "b3", "b2", "b1", "b0", "term"]
FAN_Y = {nm: -24.4 - i * 1.3 for i, nm in enumerate(NETS)}
for nm in NETS:
    top_.shapes(m3l).insert(pya.DText(nm, pya.DTrans(
        pya.DVector(SW_X[nm] + 0.2, FAN_Y[nm]))))
top_.shapes(m3l).insert(pya.DText("topp", pya.DTrans(pya.DVector(100.0, -36.5))))
top_.shapes(m3l).insert(pya.DText("trkb", pya.DTrans(pya.DVector(100.0, -14.9))))
top_.shapes(tm1l).insert(pya.DText("topr", pya.DTrans(pya.DVector(250.0, 114.9))))
VX = {"b5r": 172.4, "b6r": 173.3, "b7r": 174.4, "b4r": 182.6, "b3r": 184.8,
      "b2r": 187.0, "b1r": 189.2, "b0r": 191.4, "termr": 193.6}
NETS2 = ["b7r", "b6r", "b5r", "b4r", "b3r", "b2r", "b1r", "b0r", "termr"]
DEPTH = {n: -33.31 + 0.82 * i for i, n in enumerate(sorted(NETS2, key=lambda k: VX[k]))}
for n in NETS2:
    top_.shapes(m3l).insert(pya.DText(n, pya.DTrans(pya.DVector(250.0, DEPTH[n]))))
top_.shapes(m3l).insert(pya.DText("vcm", pya.DTrans(pya.DVector(160.0, -9.82))))

top_.name = "oa_sar8_pas8"
ly.write("oa_sar8_pas8.gds")
print("wrote oa_sar8_pas8.gds", top_.dbbox())
