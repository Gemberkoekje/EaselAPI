import math
import random


def torn(pts, amp=0.018, per=0.035, seed=0):
    """Subdivide a polyline and jitter it perpendicular - a ragged boundary."""
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


weed_lo = polygon(torn([(-0.03, 0.500), (0.28, 0.585), (0.55, 0.700), (0.80, 0.760),
                        (1.03, 0.735), (1.03, 1.03), (-0.03, 1.03)], 0.030, 0.060, 1))
weed_up = polygon(torn([(-0.03, -0.03), (0.42, -0.03), (0.36, 0.180), (0.20, 0.330),
                        (0.06, 0.430), (-0.03, 0.470)], 0.028, 0.055, 2))
weed_rt = polygon(torn([(1.03, 0.040), (0.86, 0.215), (0.80, 0.410), (0.86, 0.560),
                        (1.03, 0.640)], 0.026, 0.050, 3))
silt = polygon(torn([(0.30, 0.640), (0.52, 0.610), (0.68, 0.680), (0.60, 0.800),
                     (0.36, 0.815), (0.24, 0.735)], 0.022, 0.045, 4))

r1 = ribbon([(0.720, 0.075), (0.655, 0.155), (0.600, 0.226)], 0.050, 0.098)
r2 = ribbon([(0.600, 0.222), (0.500, 0.318), (0.415, 0.418)], 0.098, 0.074)
r3 = ribbon([(0.415, 0.415), (0.335, 0.505), (0.265, 0.600)], 0.074, 0.034)
r4 = ribbon([(0.265, 0.598), (0.215, 0.690), (0.168, 0.784)], 0.034, 0.011)
b1 = hull([(0.545, 0.292), (0.660, 0.332), (0.738, 0.396), (0.628, 0.386),
           (0.545, 0.346)])
b2 = hull([(0.588, 0.184), (0.500, 0.146), (0.432, 0.162), (0.520, 0.206)])
i1 = blob((0.302, 0.800), 0.036, 0.026, wobble=0.42, seed=7)
i2 = blob((0.778, 0.548), 0.022, 0.016, wobble=0.42, seed=11)
i3 = blob((0.152, 0.376), 0.028, 0.020, wobble=0.42, seed=13)

shapes = [weed_lo, weed_up, weed_rt, silt, r1, r2, r3, r4, b1, b2, i1, i2, i3]
for nm, sh in zip(["weed_lo", "weed_up", "weed_rt", "silt", "r1", "r2", "r3", "r4",
                   "b1", "b2", "i1", "i2", "i3"], shapes):
    print(f"{nm:8s} box={sh.box} axis={round(sh.axis,1)} area={sh.area:.4f}")
print(s.preview(shapes, grid=True))
