# Pass 23 - the flat chisel fanned into a sunburst. Carve with a round tip instead.
exec(open("lib.py").read())
pc, warm, cool, arc, at, dome, finish = make(s)
import math, random
p = s.palette
s.dry()
CX, CY, RX, RY = 0.640, 0.520, 0.112, 0.100

def carve(cx, cy, rx, ry, t0, t1, colour, seed, base=1.08, amp=0.055, k=6, sz=0.024, step=15):
    rnd = random.Random(seed)
    th = t0
    while th < t1:
        b = min(t1, th + step + rnd.uniform(-3, 5))
        pts = []
        for i in range(6):
            a = th + (b - th) * i / 5
            r = base + amp * math.sin(math.radians(k * a) + seed) + rnd.uniform(-0.015, 0.015)
            pts.append((cx + r*rx*math.cos(math.radians(a)), cy + r*ry*math.sin(math.radians(a))))
        s.stroke(pts, "round_hard", colour, size=sz*rnd.uniform(0.85, 1.2),
                 pressure="even", load=1.0)
        th = b

# flatten the sunburst and the swatches first
carve(CX, CY, RX, RY, 244, 424, "bg", 11, base=1.24, amp=0.0, sz=0.075, step=26)
s.block_in(polygon([(0.648,0.586),(0.716,0.578),(0.772,0.532),(0.800,0.560),
                    (0.760,0.626),(0.678,0.640)]), "flat", "bg", direction=(37,127),
           density=1.0, size=0.026, load=1.0, pressure="even")
s.block_in(polygon([(0.648,0.616),(0.790,0.628),(0.800,0.664),(0.640,0.652)]), "flat",
           "tbl", direction=(6,168), density=1.0, size=0.022, load=1.0, pressure="even")
# now the ruffle
carve(CX, CY, RX, RY, 246, 424, "bg", 3)
carve(CX, CY, RX, RY, 58, 122, "bg", 7, base=1.10, amp=0.045, sz=0.020)

# a few lit petal edges, subtle
rnd = random.Random(19)
for th, w, dv, f in ((214, 46, 0.13, 0.86), (250, 38, 0.16, 0.72), (188, 34, 0.11, 0.94),
                     (286, 30, 0.10, 0.80), (160, 28, 0.09, 0.66)):
    d = math.cos(math.radians(th - 225))
    v = min(0.93, 0.645 + 0.215*d + dv)
    s.stroke(arc(CX, CY, RX, RY, f, th-w/2, th+w/2, 6), "round_hard", warm(pc(v), 0.10),
             size=0.006*rnd.uniform(0.8, 1.5), pressure=[0.3, 1.0, 0.35])
# and two hanging petals, painted rather than stamped
for cxo, cyo, rxo, ryo, v, rot in ((0.700,0.598,0.030,0.020,0.54,-24),
                                   (0.662,0.616,0.024,0.016,0.48,14)):
    el = ellipse(Region(cxo-rxo, cyo-ryo, cxo+rxo, cyo+ryo), rotate=rot)
    s.block_in(el.inset(0.004), "flat", cool(pc(v), 0.10), direction="axis",
               density=1.0, size=0.007, load=1.0, pressure="even")
    s.stroke([(cxo-rxo*0.8, cyo-ryo*0.35), (cxo-rxo*0.1, cyo-ryo*0.8), (cxo+rxo*0.7, cyo-ryo*0.3)],
             "liner", pc(min(0.90, v+0.20)), size=0.004, pressure=[0.3,1.0,0.25])
s.dab(0.586, 0.464, "round_hard", "titanium_white", size=0.010, press=3)
s.dab(0.612, 0.440, "round_hard", p.mix("titanium_white", "yellow_ochre", 0.10),
      size=0.008, press=3)

print("strokes:", s.stroke_count)
print(s.look(region=span("E4","G6"), sketch=False))
