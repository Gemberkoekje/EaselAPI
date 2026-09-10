# Pass 18 - rehearse a radiating petal set on bloom B. Nothing is spent here.
import math
p = s.palette
grey = p.mix("ultramarine", "burnt_sienna", 0.50)
lo, hi = p.tint(grey, 0.40), p.mix("titanium_white", "yellow_ochre", 0.08)
vlo, vhi = p.value_of(lo), p.value_of(hi)
def petal_colour(v):
    a, b = 0.0, 1.0
    for _ in range(20):
        m = (a + b) / 2
        a, b = (m, b) if p.value_of(p.mix(lo, hi, m)) < v else (a, m)
    return p.mix(lo, hi, (a + b) / 2)

def petals(cx, cy, rx, ry, n, base, amp, seed, sz0, lit_dir=225.0):
    import random
    rnd = random.Random(seed)
    out = []
    for i in range(n):
        th = (360.0 / n) * i + rnd.uniform(-9, 9)
        r = math.radians(th)
        d = math.cos(math.radians(th - lit_dir))
        v = max(0.30, min(0.94, base + amp * d + rnd.uniform(-0.035, 0.035)))
        ext = rnd.uniform(0.86, 1.10)
        r0 = rnd.uniform(0.24, 0.42)
        x0, y0 = cx + r0 * rx * math.cos(r), cy + r0 * ry * math.sin(r)
        x1, y1 = cx + ext * rx * math.cos(r), cy + ext * ry * math.sin(r)
        px, py = -math.sin(r), math.cos(r)
        bow = rnd.uniform(-0.30, 0.30) * rx
        xm, ym = (x0 + x1) / 2 + px * bow, (y0 + y1) / 2 + py * bow * (ry / rx)
        out.append({"points": [(x0, y0), (xm, ym), (x1, y1)], "brush": "round_hard",
                    "color": petal_colour(v), "size": sz0 * rnd.uniform(0.70, 1.45),
                    "pressure": [0.30, 1.0, rnd.uniform(0.35, 0.8)]})
    return out

plan = petals(0.640, 0.520, 0.112, 0.100, 17, 0.63, 0.20, 5, 0.020)
print(len(plan), "petals; value range",
      round(min(p.value_of(q["color"]) for q in plan), 3),
      round(max(p.value_of(q["color"]) for q in plan), 3))
s.rehearse(plan, region=span("E4","G6"))
print("strokes:", s.stroke_count)
