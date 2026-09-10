import math

p = s.palette
WHITE = "titanium_white"


def to_value(base, target):
    a, b = 0.0, 1.0
    for _ in range(24):
        m = (a + b) / 2
        a, b = (m, b) if p.value_of(p.mix(base, WHITE, m)) < target else (a, m)
    return p.mix(base, WHITE, (a + b) / 2)


p["frond"] = p.desaturate(to_value(p.mix("viridian", "burnt_umber", 0.55), 0.175), 0.45)
p["shade"] = to_value(p.mix("burnt_umber", "ultramarine", 0.45), 0.115)
p["leaf_w"] = p.desaturate(to_value(p.mix("burnt_sienna", "yellow_ochre", 0.40), 0.47), 0.30)
p["leaf_d"] = p.desaturate(to_value(p.mix("burnt_umber", "alizarin", 0.28), 0.28), 0.35)
p["leaf_p"] = p.desaturate(to_value(p.mix("yellow_ochre", "cadmium_red", 0.30), 0.63), 0.30)
p["leaf_x"] = p.desaturate(to_value(p.mix("burnt_umber", "viridian", 0.30), 0.245), 0.55)
p["vein"] = to_value(p.mix("burnt_umber", "ultramarine", 0.35), 0.19)
for n in ("frond", "shade", "leaf_w", "leaf_d", "leaf_p", "leaf_x"):
    print(f"{n:7s} {p.hex(p[n])}  {p.value_of(p[n]):.2f}")

plan = []

FRONDS = [([(0.86, 0.020), (0.72, 0.098), (0.612, 0.196), (0.556, 0.300)], 0.010),
          ([(0.98, 0.170), (0.836, 0.216), (0.700, 0.296), (0.612, 0.404)], 0.007),
          ([(0.470, 0.050), (0.524, 0.162), (0.514, 0.292), (0.460, 0.406)], 0.009),
          ([(0.300, 0.238), (0.392, 0.332), (0.438, 0.454), (0.418, 0.580)], 0.008),
          ([(0.130, 0.468), (0.254, 0.514), (0.354, 0.600), (0.402, 0.718)], 0.007),
          ([(0.646, 0.238), (0.560, 0.352), (0.468, 0.430), (0.356, 0.470)], 0.006),
          ([(0.040, 0.756), (0.192, 0.804), (0.332, 0.858), (0.474, 0.872)], 0.012),
          ([(0.702, 0.628), (0.792, 0.714), (0.838, 0.830), (0.818, 0.962)], 0.009)]
for pts, sz in FRONDS:
    plan.append(dict(points=pts, brush="bristle", color="frond", size=sz, load=0.65,
                     pressure=[0.4, 1.0, 0.8, 0.3], label="frond"))

#   cx      cy     len   ang    size    colour     shadow?  vein?
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
          (0.762, 0.414, 0.026, -8, 0.007, "leaf_p", False, False)]
for cx, cy, ln, ang, sz, col, sh, vn in LEAVES:
    a = math.radians(ang)
    dx, dy = ln / 2 * math.cos(a), ln / 2 * math.sin(a)
    if sh:
        plan.append(dict(points=[(cx - dx * 1.12 + 0.008, cy - dy * 1.12 + 0.006),
                                 (cx + dx * 1.12 + 0.008, cy + dy * 1.12 + 0.006)],
                         brush="bristle", color="shade", size=sz * 1.35, load=0.8,
                         pressure="swell", label="leaf shadow"))
    plan.append(dict(points=[(cx - dx, cy - dy), (cx + dx, cy + dy)], brush="round_hard",
                     color=col, size=sz, pressure="swell", label="leaf"))
    if vn:
        plan.append(dict(points=[(cx - dx * 0.66, cy - dy * 0.66),
                                 (cx + dx * 0.78, cy + dy * 0.78)], brush="liner",
                         color="vein", size=sz * 0.13, pressure=[0.85, 0.3],
                         label="vein"))

# the curled leaf: a short dark sliver inside a pale blade, not a symmetrical mouth
plan += [
    dict(points=[(0.676, 0.726), (0.716, 0.716)], brush="round_hard", color="vein",
         size=0.009, pressure="even", label="curl inside"),
    dict(points=[(0.662, 0.738), (0.724, 0.732), (0.752, 0.742)], brush="round_hard",
         color="leaf_p", size=0.008, pressure="swell", label="curl near rim"),
]

print(s.rehearse(plan))
print(s.rehearse(plan, region=span("D5", "H8")))
