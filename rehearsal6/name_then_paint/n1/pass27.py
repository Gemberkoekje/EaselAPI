# Pass 27 - break the rings: marks that cross them, in close values.
exec(open("lib2.py").read())
pc, warm, cool, arc, at, clean, head, edges, ruffle = build(s)
import math, random
p = s.palette
s.dry()

def crossmarks(cx, cy, rx, ry, seed, vbase, vamp, n, lit, szlo, szhi):
    rnd = random.Random(seed)
    for i in range(n):
        th = rnd.uniform(0, 360)
        d = math.cos(math.radians(th - lit))
        local = vbase + vamp * d
        v = max(0.32, min(0.93, local + rnd.uniform(-0.075, 0.075)))
        f0 = rnd.uniform(0.20, 0.62); f1 = f0 + rnd.uniform(0.28, 0.50)
        sw = rnd.uniform(-26, 26)
        pts = [at(cx, cy, rx, ry, f0, th),
               at(cx, cy, rx, ry, (f0+f1)/2, th + sw*0.6),
               at(cx, cy, rx, ry, f1, th + sw)]
        c = warm(pc(v), 0.11) if d > 0 else cool(pc(v), 0.09)
        s.stroke(pts, "bristle", c, size=rnd.uniform(szlo, szhi),
                 load=rnd.uniform(0.55, 0.85), pressure=[0.35, 1.0, rnd.uniform(0.3, 0.7)])

crossmarks(0.442, 0.436, 0.100, 0.092, 201, 0.700, 0.200, 20, 228, 0.010, 0.020)
crossmarks(0.640, 0.520, 0.112, 0.100, 211, 0.645, 0.215, 22, 218, 0.011, 0.022)
crossmarks(0.398, 0.586, 0.078, 0.066, 221, 0.575, 0.190, 15, 236, 0.008, 0.016)
crossmarks(0.556, 0.372, 0.050, 0.044, 231, 0.470, 0.150, 10, 242, 0.006, 0.012)

# the bud sits back: knock it down
s.glaze(arc(0.556, 0.372, 0.050, 0.044, 0.55, 0, 350, 10), p.mix("ultramarine","burnt_umber",0.5),
        opacity=0.16)
s.glaze(arc(0.556, 0.372, 0.050, 0.044, 0.90, 20, 300, 8), p.mix("ultramarine","burnt_umber",0.5),
        opacity=0.12)
# C turns away at its bottom
for t0, f, dv in ((10, 0.72, -0.20), (34, 0.92, -0.24), (56, 0.55, -0.16)):
    s.stroke(arc(0.398, 0.586, 0.078, 0.066, f, 236+180+t0, 236+180+t0+58, 7), "flat",
             cool(pc(max(0.33, 0.575 - 0.19 + dv)), 0.16), size=0.014, pressure="even", load=1.0)

print("strokes:", s.stroke_count)
print(s.look(region=span("C3","G6"), sketch=False))
