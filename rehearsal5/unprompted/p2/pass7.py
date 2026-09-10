import math
import random

p = s.palette
rng = random.Random(127)
WHITE = "titanium_white"


def to_value(base, target):
    a, b = 0.0, 1.0
    for _ in range(24):
        m = (a + b) / 2
        a, b = (m, b) if p.value_of(p.mix(base, WHITE, m)) < target else (a, m)
    return p.mix(base, WHITE, (a + b) / 2)


p["frond"] = p.desaturate(to_value(p.mix("viridian", "burnt_umber", 0.50), 0.205), 0.45)
p["shade"] = to_value(p.mix("burnt_umber", "ultramarine", 0.45), 0.115)
p["leaf_w"] = p.desaturate(to_value(p.mix("burnt_sienna", "yellow_ochre", 0.40), 0.47), 0.30)
p["leaf_d"] = p.desaturate(to_value(p.mix("burnt_umber", "alizarin", 0.28), 0.28), 0.35)
p["leaf_p"] = p.desaturate(to_value(p.mix("yellow_ochre", "cadmium_red", 0.30), 0.63), 0.30)
p["leaf_x"] = p.desaturate(to_value(p.mix("burnt_umber", "viridian", 0.30), 0.245), 0.55)
p["vein"] = to_value(p.mix("burnt_umber", "ultramarine", 0.35), 0.19)

s.dry()

# break the straight left edge of the right-hand strip
for x, y, ln, ang, sz in ((0.812, 0.135, 0.085, 74, 0.024), (0.806, 0.330, 0.070, 96, 0.020),
                          (0.826, 0.492, 0.060, 68, 0.018), (0.798, 0.610, 0.050, 108, 0.016)):
    a = math.radians(ang)
    s.stroke([(x - ln / 2 * math.cos(a), y - ln / 2 * math.sin(a)),
              (x + ln / 2 * math.cos(a), y + ln / 2 * math.sin(a))],
             "bristle", "shade", size=sz, load=0.9, pressure="swell")

FRONDS = [([(0.86, 0.020), (0.72, 0.098), (0.612, 0.196), (0.556, 0.300)], 0.011),
          ([(0.98, 0.170), (0.836, 0.216), (0.700, 0.296), (0.612, 0.404)], 0.008),
          ([(0.470, 0.050), (0.524, 0.162), (0.514, 0.292), (0.460, 0.406)], 0.010),
          ([(0.300, 0.238), (0.392, 0.332), (0.438, 0.454), (0.418, 0.580)], 0.009),
          ([(0.130, 0.468), (0.254, 0.514), (0.354, 0.600), (0.402, 0.718)], 0.008),
          ([(0.646, 0.238), (0.560, 0.352), (0.468, 0.430), (0.356, 0.470)], 0.007),
          ([(0.040, 0.756), (0.192, 0.804), (0.332, 0.858), (0.474, 0.872)], 0.013),
          ([(0.702, 0.628), (0.792, 0.714), (0.838, 0.830), (0.818, 0.962)], 0.010)]
for pts, sz in FRONDS:
    s.stroke(pts, "bristle", "frond", size=sz, load=0.8,
             pressure=[0.4, 1.0, 0.8, 0.3])

LEAVES = [(0.072, 0.108, 0.104, 28, 0.027, "leaf_w", True, True),
          (0.870, 0.152, 0.048, -34, 0.012, "leaf_x", False, False),
          (0.248, 0.310, 0.034, 62, 0.009, "leaf_d", False, False),
          (0.598, 0.106, 0.072, 14, 0.017, "leaf_d", False, False),
          (0.442, 0.398, 0.030, -52, 0.008, "leaf_d", False, False),
          (0.702, 0.740, 0.094, 6, 0.024, "leaf_p", True, True),
          (0.330, 0.906, 0.056, -20, 0.014, "leaf_w", True, False),
          (0.912, 0.848, 0.072, 40, 0.018, "leaf_x", False, False),
          (0.086, 0.638, 0.042, -26, 0.011, "leaf_x", False, False),
          (-0.012, 0.428, 0.082, 12, 0.020, "leaf_w", True, True),
          (0.522, 0.562, 0.038, 70, 0.010, "leaf_d", False, False),
          (0.762, 0.414, 0.026, -8, 0.007, "leaf_p", False, False),
          (0.944, 0.470, 0.052, -58, 0.013, "leaf_w", False, False),
          (0.878, 0.302, 0.038, 22, 0.010, "leaf_x", False, False),
          (0.400, 0.702, 0.064, -34, 0.016, "leaf_w", True, False),
          (0.564, 0.792, 0.044, 50, 0.011, "leaf_d", False, False),
          (0.178, 0.762, 0.036, -12, 0.009, "leaf_p", False, False)]
for cx, cy, ln, ang, sz, col, sh, vn in LEAVES:
    a = math.radians(ang)
    dx, dy = ln / 2 * math.cos(a), ln / 2 * math.sin(a)
    if sh:
        s.stroke([(cx - dx * 1.12 + 0.008, cy - dy * 1.12 + 0.006),
                  (cx + dx * 1.12 + 0.008, cy + dy * 1.12 + 0.006)],
                 "bristle", "shade", size=sz * 1.35, load=0.8, pressure="swell")
    s.stroke([(cx - dx, cy - dy), (cx + dx, cy + dy)], "round_hard", col,
             size=sz, pressure="swell")
    if vn:
        s.stroke([(cx - dx * 0.66, cy - dy * 0.66), (cx + dx * 0.78, cy + dy * 0.78)],
                 "liner", "vein", size=sz * 0.13, pressure=[0.85, 0.3])

s.stroke([(0.676, 0.726), (0.716, 0.716)], "round_hard", "vein", size=0.009,
         pressure="even")
s.stroke([(0.662, 0.738), (0.724, 0.732), (0.752, 0.742)], "round_hard", "leaf_p",
         size=0.008, pressure="swell")

print("strokes", s.stroke_count)
print(s.look())
