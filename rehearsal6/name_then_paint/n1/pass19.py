# Pass 19 - model bloom B as arcs round the dome, then its edges and notches.
import math, random
p = s.palette
grey = p.mix("ultramarine", "burnt_sienna", 0.50)
LO = p.tint(grey, 0.36)
HI = p.mix("titanium_white", "yellow_ochre", 0.07)
def pc(v):
    a, b = 0.0, 1.0
    for _ in range(20):
        m = (a + b) / 2
        a, b = (m, b) if p.value_of(p.mix(LO, HI, m)) < v else (a, m)
    c = p.mix(LO, HI, (a + b) / 2)
    return c
def warm(c, k=0.10):  return p.mix(c, p.mix("yellow_ochre","cadmium_red",0.3), k)
def cool(c, k=0.10):  return p.mix(c, "ultramarine", k)

def arc(cx, cy, rx, ry, f, t0, t1, steps=7, squash=1.0):
    pts = []
    for i in range(steps):
        th = math.radians(t0 + (t1 - t0) * i / (steps - 1))
        pts.append((cx + f * rx * math.cos(th), cy + f * ry * math.sin(th) * squash))
    return pts

def dome(cx, cy, rx, ry, seed, vbase, vamp, sz, lit=225.0):
    rnd = random.Random(seed)
    rings = [(0.30, -0.10), (0.50, -0.02), (0.68, 0.04), (0.84, 0.06), (0.98, -0.02)]
    n = 0
    for f, dv in rings:
        segs = 5 if f > 0.6 else 4
        for k in range(segs):
            t0 = lit - 180 + (360.0 / segs) * k + rnd.uniform(-14, 14)
            t1 = t0 + 360.0 / segs + rnd.uniform(6, 26)
            mid = (t0 + t1) / 2
            d = math.cos(math.radians(mid - lit))
            v = max(0.34, min(0.90, vbase + vamp * d + dv + rnd.uniform(-0.03, 0.03)))
            c = warm(pc(v), 0.13) if d > 0 else cool(pc(v), 0.10)
            s.stroke(arc(cx, cy, rx, ry, f * rnd.uniform(0.94, 1.06), t0, t1),
                     "flat", c, size=sz * rnd.uniform(0.8, 1.35),
                     pressure=("even" if k % 2 else [0.7, 1.0, 0.6]), load=1.0)
            n += 1
    return n

s.dry()
n = dome(0.640, 0.520, 0.112, 0.100, 5, 0.64, 0.21, 0.022)
print("arc strokes:", n)

# the hollow centre where the petals fold in
s.stroke(arc(0.640, 0.520, 0.112, 0.100, 0.16, 40, 300, 6), "round_hard",
         cool(pc(0.44), 0.14), size=0.016, pressure="even")
s.stroke([(0.628,0.512),(0.648,0.506),(0.664,0.518)], "round_hard",
         p.mix(pc(0.52), p["pet_heart"], 0.45), size=0.010, pressure=[0.5,1.0,0.4])

print("strokes:", s.stroke_count)
print(s.look(region=span("E4","G6"), sketch=False))
