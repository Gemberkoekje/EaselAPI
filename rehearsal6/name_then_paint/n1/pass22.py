# Pass 22 - ruffle bloom B's silhouette by painting the background along it.
exec(open("lib.py").read())
pc, warm, cool, arc, at, dome, finish = make(s)
import math
p = s.palette
s.dry()
CX, CY, RX, RY = 0.640, 0.520, 0.112, 0.100

def carve(cx, cy, rx, ry, t0, t1, colour, seed, base=1.10, amp=0.075, k=5, sz=0.026, step=17):
    import random
    rnd = random.Random(seed)
    th = t0
    while th < t1:
        b = min(t1, th + step + rnd.uniform(-4, 6))
        pts = []
        n = 6
        for i in range(n):
            a = th + (b - th) * i / (n - 1)
            r = base + amp * math.sin(math.radians(k * a) + seed) + rnd.uniform(-0.02, 0.02)
            pts.append((cx + r*rx*math.cos(math.radians(a)), cy + r*ry*math.sin(math.radians(a))))
        s.stroke(pts, "flat", colour, size=sz*rnd.uniform(0.85, 1.2),
                 pressure=("even" if rnd.random() < 0.6 else [0.8, 1.0, 0.7]), load=1.0)
        th = b

carve(CX, CY, RX, RY, 250, 420, "bg", 3)
carve(CX, CY, RX, RY, 60, 118, "bg", 7, base=1.12, amp=0.06, sz=0.022)

# two petals hanging off the bottom right, crossing the table edge
for cxo, cyo, rxo, ryo, v, rot in ((0.702,0.600,0.032,0.021,0.52,-22),
                                   (0.666,0.618,0.026,0.017,0.47,12),
                                   (0.744,0.548,0.024,0.016,0.58,-46)):
    el = ellipse(Region(cxo-rxo, cyo-ryo, cxo+rxo, cyo+ryo), rotate=rot)
    s.block_in(el.inset(0.0045), "flat", cool(pc(v), 0.10), direction="axis",
               density=1.0, size=0.009, load=1.0, pressure="even")
    s.stroke([(cxo-rxo*0.75, cyo-ryo*0.45), (cxo, cyo-ryo*0.85), (cxo+rxo*0.65, cyo-ryo*0.35)],
             "round_hard", pc(min(0.92, v+0.18)), size=0.004, pressure=[0.35,1.0,0.25])

print("strokes:", s.stroke_count)
print(s.look(region=span("E4","G6"), sketch=False))
