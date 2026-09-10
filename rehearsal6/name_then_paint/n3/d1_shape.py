import math
def arc(cx, cy, rx, ry, a0, a1, n=36):
    return [(cx+rx*math.cos(a0+(a1-a0)*i/(n-1.0)),
             cy+ry*math.sin(a0+(a1-a0)*i/(n-1.0))) for i in range(n)]
pts = arc(0.393, 0.630, 0.128, 0.064, 0, 2*math.pi)
raw = polygon(pts)
ins = raw.inset(0.011)
print("raw   box:", raw.box, "area:", round(raw.area, 5), "closed:", raw.closed is not None)
print("inset box:", ins.box, "area:", round(ins.area, 5))
e = ellipse(span("C5", "F6"))
print("ellipse(span) box:", e.box, "area:", round(e.area, 5))
e2 = ellipse((0.393, 0.630), 0.128, 0.064)
print("ellipse(pt,rx,ry) box:", e2.box, "area:", round(e2.area, 5))
print(s.preview(raw))
print(s.preview(ins))
print(s.preview(e2))
