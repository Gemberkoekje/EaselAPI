import math
import random

p = s.palette
rng = random.Random(103)
WHITE = "titanium_white"


def to_value(base, target):
    a, b = 0.0, 1.0
    for _ in range(24):
        m = (a + b) / 2
        a, b = (m, b) if p.value_of(p.mix(base, WHITE, m)) < target else (a, m)
    return p.mix(base, WHITE, (a + b) / 2)


p["frond"] = to_value(p.mix("burnt_umber", "ultramarine", 0.45), 0.115)
p["frond2"] = p.desaturate(to_value(p.mix("viridian", "burnt_umber", 0.55), 0.175), 0.45)
p["leaf_w"] = p.desaturate(to_value(p.mix("burnt_sienna", "yellow_ochre", 0.40), 0.50), 0.22)
p["leaf_d"] = p.desaturate(to_value(p.mix("burnt_umber", "alizarin", 0.30), 0.30), 0.30)
p["leaf_p"] = p.desaturate(to_value(p.mix("yellow_ochre", "cadmium_red", 0.30), 0.62), 0.25)
p["vein"] = to_value(p.mix("burnt_umber", "ultramarine", 0.35), 0.20)
for n in ("frond", "frond2", "leaf_w", "leaf_d", "leaf_p", "vein"):
    print(f"{n:7s} {p.hex(p[n])}  {p.value_of(p[n]):.2f}")

plan = []

# fronds - long thin strands crossing the pools, lost on the dark field
FRONDS = [([(0.86, 0.020), (0.72, 0.098), (0.612, 0.196), (0.556, 0.300)], 0.007, "frond"),
          ([(0.98, 0.170), (0.836, 0.216), (0.700, 0.296), (0.612, 0.404)], 0.005, "frond"),
          ([(0.470, 0.055), (0.520, 0.160), (0.512, 0.290), (0.462, 0.404)], 0.006, "frond"),
          ([(0.300, 0.240), (0.390, 0.330), (0.436, 0.452), (0.418, 0.578)], 0.006, "frond2"),
          ([(0.135, 0.470), (0.252, 0.512), (0.352, 0.598), (0.400, 0.716)], 0.005, "frond2"),
          ([(0.640, 0.240), (0.560, 0.352), (0.470, 0.430), (0.360, 0.470)], 0.004, "frond"),
          ([(0.055, 0.760), (0.190, 0.802), (0.330, 0.856), (0.470, 0.870)], 0.008, "frond2"),
          ([(0.700, 0.630), (0.790, 0.712), (0.836, 0.828), (0.820, 0.960)], 0.006, "frond2")]
for pts, sz, col in FRONDS:
    plan.append(dict(points=pts, brush="round_hard", color=col, size=sz,
                     pressure=[0.35, 1.0, 0.8, 0.25], label="frond"))

# leaves - a round_hard stroke under `swell` is already a leaf shape
LEAVES = [(0.140, 0.128, 0.075, 34, 0.020, "leaf_w"),
          (0.836, 0.196, 0.062, -22, 0.017, "leaf_p"),
          (0.246, 0.312, 0.052, 62, 0.014, "leaf_w"),
          (0.596, 0.108, 0.058, 18, 0.015, "leaf_d"),
          (0.446, 0.396, 0.046, -48, 0.012, "leaf_d"),
          (0.686, 0.726, 0.068, 8, 0.018, "leaf_w"),
          (0.352, 0.900, 0.080, -16, 0.021, "leaf_p"),
          (0.884, 0.862, 0.055, 44, 0.015, "leaf_w"),
          (0.096, 0.626, 0.060, -30, 0.016, "leaf_w")]
for cx, cy, ln, ang, sz, col in LEAVES:
    a = math.radians(ang)
    dx, dy = ln / 2 * math.cos(a), ln / 2 * math.sin(a)
    plan.append(dict(points=[(cx - dx, cy - dy), (cx + dx, cy + dy)], brush="round_hard",
                     color=col, size=sz, pressure="swell", label="leaf"))
    plan.append(dict(points=[(cx - dx * 0.7, cy - dy * 0.7), (cx + dx * 0.8, cy + dy * 0.8)],
                     brush="liner", color="vein", size=sz * 0.16,
                     pressure=[0.9, 0.4], label="vein"))

# one curled leaf, with an inside: far rim, the cup, near rim
plan += [
    dict(points=[(0.548, 0.596), (0.596, 0.566), (0.652, 0.578)], brush="round_hard",
         color="leaf_p", size=0.014, pressure="swell", label="curl far rim"),
    dict(points=[(0.566, 0.604), (0.614, 0.594), (0.648, 0.600)], brush="round_hard",
         color="leaf_d", size=0.011, pressure="even", label="curl cup"),
    dict(points=[(0.552, 0.616), (0.606, 0.626), (0.658, 0.612)], brush="round_hard",
         color="leaf_w", size=0.010, pressure="swell", label="curl near rim"),
]

print(s.rehearse(plan))
print(s.rehearse(plan, region=span("D1", "H4")))
