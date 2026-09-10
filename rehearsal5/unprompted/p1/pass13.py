import math
import random

p = s.palette
rng = random.Random(63)
WHITE = "titanium_white"


def to_value(base, target):
    a, b = 0.0, 1.0
    for _ in range(24):
        m = (a + b) / 2
        a, b = (m, b) if p.value_of(p.mix(base, WHITE, m)) < target else (a, m)
    return p.mix(base, WHITE, (a + b) / 2)


p["m_a"] = to_value(p.mix("burnt_umber", "burnt_sienna", 0.40), 0.31)
p["m_b"] = to_value(p.mix("burnt_sienna", "burnt_umber", 0.40), 0.37)
p["sh"] = to_value(p.mix("burnt_umber", "ultramarine", 0.32), 0.28)
p["rim"] = to_value(p.mix("yellow_ochre", "cadmium_red", 0.20), 0.72)
p["rim2"] = to_value(p.mix("yellow_ochre", "burnt_sienna", 0.30), 0.58)
p["lap"] = to_value(p.mix("burnt_sienna", "burnt_umber", 0.35), 0.34)
p["stem"] = to_value(p.mix("ultramarine", "burnt_umber", 0.55), 0.14)
p["warp"] = to_value(p.mix("burnt_umber", "yellow_ochre", 0.40), 0.44)

s.dry()

# bury the orange grit - two shapes, both stopping clear of the withy feet
s.block_in(polygon([(0.00, 0.784), (0.16, 0.770), (0.33, 0.790), (0.50, 0.772),
                    (0.66, 0.792), (0.845, 0.778), (0.845, 0.900), (0.00, 0.900)]),
           "bristle", "mud_near", direction=-5, density=1.0, size=0.070,
           load=1.0, load_falloff=0.2, pressure="even")
s.block_in(ribbon([(0.00, 0.950), (0.50, 0.962), (1.00, 0.944)], 0.140),
           "bristle", "mud_near", direction=4, density=1.0, size=0.080,
           load=1.0, load_falloff=0.2, pressure="even")

# surface, at full load and close in value so it reads as paint not grit
for _ in range(8):
    x = rng.uniform(-0.02, 0.78)
    y = rng.uniform(0.800, 0.998)
    ln = rng.uniform(0.14, 0.30)
    a = math.radians(rng.uniform(-11.0, 11.0))
    s.stroke([(x, y), (x + ln * math.cos(a), y + ln * math.sin(a))], "bristle",
             rng.choice(["m_a", "m_b"]), size=rng.uniform(0.030, 0.062),
             load=1.0, load_falloff=0.15, pressure=rng.choice(["swell", "taper"]))

# the shadow, again, hugging the hull
for x0, x1, y0, y1, sz in ((0.240, 0.372, 0.792, 0.804, 0.024),
                           (0.352, 0.484, 0.800, 0.804, 0.028),
                           (0.452, 0.560, 0.798, 0.786, 0.020)):
    s.stroke([(x0, y0), (x1, y1)], "bristle", "sh", size=sz, load=0.9,
             pressure="swell")

print("total", s.stroke_count)
print(s.look())

# --- rehearse the boat's fine marks before spending them ----------------------
detail = [
    dict(points=[(0.232, 0.674), (0.318, 0.687)], brush="round_hard", color="rim",
         size=0.005, pressure=[0.5, 1.0, 0.4], label="sheer 1"),
    dict(points=[(0.352, 0.692), (0.462, 0.701)], brush="round_hard", color="rim",
         size=0.005, pressure=[0.4, 1.0, 0.5], label="sheer 2"),
    dict(points=[(0.508, 0.701), (0.566, 0.681)], brush="round_hard", color="rim2",
         size=0.004, pressure=[0.8, 0.3], label="sheer 3"),
    dict(points=[(0.292, 0.629), (0.402, 0.627)], brush="round_hard", color="rim2",
         size=0.004, pressure=[0.4, 1.0, 0.4], label="far gunwale 1"),
    dict(points=[(0.468, 0.634), (0.558, 0.655)], brush="round_hard", color="rim2",
         size=0.004, pressure=[0.6, 1.0, 0.3], label="far gunwale 2"),
    dict(points=[(0.203, 0.645), (0.213, 0.684)], brush="round_hard", color="stem",
         size=0.007, pressure=[1.0, 0.6], label="stem"),
    dict(points=[(0.209, 0.652), (0.216, 0.676)], brush="round_hard", color="rim2",
         size=0.003, pressure=[0.9, 0.3], label="stem light"),
    dict(points=[(0.588, 0.666), (0.594, 0.706)], brush="round_hard", color="stem",
         size=0.006, pressure=[0.8, 1.0], label="transom"),
    dict(points=[(0.250, 0.702), (0.340, 0.720), (0.418, 0.730)], brush="round_hard",
         color="lap", size=0.004, pressure=[0.3, 1.0, 0.5], label="lap 1"),
    dict(points=[(0.462, 0.733), (0.548, 0.726)], brush="round_hard", color="lap",
         size=0.004, pressure=[0.8, 0.2], label="lap 1b"),
    dict(points=[(0.272, 0.724), (0.366, 0.746), (0.432, 0.756)], brush="round_hard",
         color="lap", size=0.0035, pressure=[0.4, 1.0, 0.3], label="lap 2"),
    dict(points=[(0.330, 0.664), (0.356, 0.678)], brush="round_hard", color="rim2",
         size=0.005, pressure=[1.0, 0.5], label="thwart"),
    dict(points=[(0.206, 0.664), (0.148, 0.706), (0.086, 0.742), (0.030, 0.758)],
         brush="liner", color="warp", size=0.0035, pressure=[1.0, 0.9, 0.5, 0.2],
         label="mooring warp"),
]
print(s.rehearse(detail, region=span("B5", "F8")))
print(s.rehearse(detail))
