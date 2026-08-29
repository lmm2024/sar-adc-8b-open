# usage: klayout -zz -r probe_box.py -rd gds=X.gds -rd cell=C -rd box=x1,y1,x2,y2 -rd layers=10,30
import pya
ly = pya.Layout(); ly.read(gds)
c = ly.cell(cell)
x1, y1, x2, y2 = [float(v) for v in box.split(",")]
b = pya.DBox(x1, y1, x2, y2)
for ln in [int(v) for v in layers.split(",")]:
    li = ly.layer(ln, 0)
    it = c.begin_shapes_rec_touching(li, b)
    n = 0
    seen = set()
    while not it.at_end():
        sh = it.shape(); tr = it.dtrans()
        bb = (sh.dbbox().transformed(tr))
        key = (round(bb.left,2), round(bb.bottom,2), round(bb.right,2), round(bb.top,2))
        if key not in seen:
            seen.add(key); n += 1
            if n <= 25:
                print(f"L{ln}: {key} cell={it.cell().name}")
        it.next()
    print(f"layer {ln}: {n} distinct shapes touching {box}")
