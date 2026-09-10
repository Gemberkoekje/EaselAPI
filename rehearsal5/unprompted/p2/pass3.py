import math
import random

p = s.palette
WHITE = "titanium_white"


def to_value(base, target):
    a, b = 0.0, 1.0
    for _ in range(24):
        m = (a + b) / 2
        a, b = (m, b) if p.value_of(p.mix(base, WHITE, m)) < target else (a, m)
    return p.mix(base, WHITE, (a + b) / 2)


def torn(pts, amp=0.018, per=0.035, seed=0):
    rng = random.Random(seed)
    out = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        d = math.hypot(x1 - x0, y1 - y0)
        n = max(2, int(d / per))
        nx, ny = -(y1 - y0) / d, (x1 - x0) / d
        for i in range(n):
            t = i / n
            j = rng.uniform(-amp, amp)
            out.append((x0 + (x1 - x0) * t + nx * j, y0 + (y1 - y0) * t + ny * j))
    out.append(pts[-1])
    return out


p["deep"] = p.desaturate(to_value(p.mix("ultramarine", "burnt_umber", 0.58), 0.155), 0.35)
p["w_lo"] = p.desaturate(to_value(p.mix("viridian", "burnt_umber", 0.45), 0.210), 0.55)
p["w_up"] = p.desaturate(to_value(p.mix("burnt_umber", "ultramarine", 0.38), 0.185), 0.55)
p["w_rt"] = p.desaturate(to_value(p.mix("viridian", "ultramarine", 0.35), 0.240), 0.60)
p["w_si"] = p.desaturate(to_value(p.mix("burnt_umber", "viridian", 0.30), 0.265), 0.60)
for n in ("deep", "w_lo", "w_up", "w_rt", "w_si"):
    print(f"{n:5s} {p.hex(p[n])}  {p.value_of(p[n]):.2f}")

s.dry()
s.block_in(region("all"), "bristle", "deep", direction=(22, 112), density=0.95,
           size=0.15, load=1.0, load_falloff=0.22, pressure="even")

weed_lo = polygon(torn([(-0.03, 0.500), (0.28, 0.585), (0.55, 0.700), (0.80, 0.760),
                        (1.03, 0.735), (1.03, 1.03), (-0.03, 1.03)], 0.030, 0.060, 1))
weed_up = polygon(torn([(-0.03, -0.03), (0.42, -0.03), (0.36, 0.180), (0.20, 0.330),
                        (0.06, 0.430), (-0.03, 0.470)], 0.028, 0.055, 2))
weed_rt = polygon(torn([(1.03, 0.040), (0.86, 0.215), (0.80, 0.410), (0.86, 0.560),
                        (1.03, 0.640)], 0.026, 0.050, 3))
silt = polygon(torn([(0.30, 0.640), (0.52, 0.610), (0.68, 0.680), (0.60, 0.800),
                     (0.36, 0.815), (0.24, 0.735)], 0.022, 0.045, 4))

for sh, col, sz in ((weed_lo, "w_lo", 0.110), (weed_up, "w_up", 0.090),
                    (weed_rt, "w_rt", 0.070), (silt, "w_si", 0.055)):
    s.block_in(sh, "bristle", col, direction="axis", density=0.92, size=sz,
               load=1.0, load_falloff=0.2, pressure="even")

print("strokes", s.stroke_count)
print(s.look())
print(s.look(values=True))
