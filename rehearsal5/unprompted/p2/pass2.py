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


p["weed_g"] = to_value(p.mix("viridian", "burnt_umber", 0.48), 0.22)
p["warm_black"] = to_value(p.mix("burnt_umber", "alizarin", 0.32), 0.19)
p["weed_c"] = to_value(p.mix("ultramarine", "viridian", 0.45), 0.27)
p["silt"] = to_value(p.mix("burnt_umber", "viridian", 0.32), 0.33)
for n in ("weed_g", "warm_black", "weed_c", "silt"):
    print(f"{n:11s} {p.hex(p[n])}  {p.value_of(p[n]):.2f}")

weed_lo = polygon(torn([(-0.03, 0.500), (0.28, 0.585), (0.55, 0.700), (0.80, 0.760),
                        (1.03, 0.735), (1.03, 1.03), (-0.03, 1.03)], 0.030, 0.060, 1))
weed_up = polygon(torn([(-0.03, -0.03), (0.42, -0.03), (0.36, 0.180), (0.20, 0.330),
                        (0.06, 0.430), (-0.03, 0.470)], 0.028, 0.055, 2))
weed_rt = polygon(torn([(1.03, 0.040), (0.86, 0.215), (0.80, 0.410), (0.86, 0.560),
                        (1.03, 0.640)], 0.026, 0.050, 3))
silt = polygon(torn([(0.30, 0.640), (0.52, 0.610), (0.68, 0.680), (0.60, 0.800),
                     (0.36, 0.815), (0.24, 0.735)], 0.022, 0.045, 4))

for sh, col, sz, den in ((weed_lo, "weed_g", 0.110, 0.90),
                         (weed_up, "warm_black", 0.090, 0.88),
                         (weed_rt, "weed_c", 0.070, 0.90),
                         (silt, "silt", 0.055, 0.92)):
    s.block_in(sh, "bristle", col, direction="axis", density=den, size=sz,
               load=1.0, load_falloff=0.2, pressure="even")
print("strokes", s.stroke_count)
print(s.look(grid=True))

# --- the rent, revised: a chain of linked pools, not one ribbon ---------------
L1 = hull([(0.618, 0.108), (0.672, 0.056), (0.752, 0.082), (0.760, 0.148),
           (0.700, 0.186), (0.634, 0.166)])
L2 = blob((0.576, 0.264), 0.066, 0.050, wobble=0.45, seed=21)
L3 = hull([(0.404, 0.360), (0.482, 0.352), (0.512, 0.406), (0.460, 0.452),
           (0.398, 0.428)])
L4 = blob((0.322, 0.524), 0.046, 0.036, wobble=0.45, seed=23)
L5 = blob((0.238, 0.646), 0.030, 0.024, wobble=0.45, seed=25)
BR = hull([(0.560, 0.296), (0.664, 0.330), (0.742, 0.392), (0.630, 0.384),
           (0.556, 0.344)])
BL = hull([(0.556, 0.212), (0.478, 0.168), (0.418, 0.184), (0.500, 0.232)])
I1 = blob((0.302, 0.806), 0.036, 0.026, wobble=0.42, seed=7)
I2 = blob((0.786, 0.548), 0.022, 0.016, wobble=0.42, seed=11)
I3 = blob((0.148, 0.372), 0.030, 0.021, wobble=0.42, seed=13)
print(s.preview([L1, L2, L3, L4, L5, BR, BL, I1, I2, I3], grid=True))
