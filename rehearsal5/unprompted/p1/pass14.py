import math
import random

p = s.palette
rng = random.Random(71)
WHITE = "titanium_white"


def to_value(base, target):
    a, b = 0.0, 1.0
    for _ in range(24):
        m = (a + b) / 2
        a, b = (m, b) if p.value_of(p.mix(base, WHITE, m)) < target else (a, m)
    return p.mix(base, WHITE, (a + b) / 2)


p["rim"] = to_value(p.mix("yellow_ochre", "cadmium_red", 0.20), 0.72)
p["rim2"] = to_value(p.mix("yellow_ochre", "burnt_sienna", 0.30), 0.58)
p["lap"] = to_value(p.mix("burnt_sienna", "burnt_umber", 0.30), 0.36)
p["stem"] = to_value(p.mix("ultramarine", "burnt_umber", 0.55), 0.14)
p["warp"] = to_value(p.mix("burnt_umber", "yellow_ochre", 0.40), 0.44)
p["m_a"] = to_value(p.mix("burnt_umber", "burnt_sienna", 0.40), 0.31)
p["m_b"] = to_value(p.mix("burnt_sienna", "burnt_umber", 0.40), 0.37)
p["glint"] = to_value(p.mix("yellow_ochre", "cadmium_red", 0.15), 0.89)

# take the banding out of the near mud - full load, close in value, angled
for y, ln, sz, col in ((0.784, 0.42, 0.075, "m_a"), (0.868, 0.38, 0.085, "m_b"),
                       (0.930, 0.46, 0.070, "m_a"), (0.812, 0.34, 0.060, "m_b"),
                       (0.896, 0.40, 0.078, "m_a"), (0.968, 0.36, 0.065, "m_b")):
    x = rng.uniform(-0.05, 0.40)
    a = math.radians(rng.uniform(-14.0, 14.0))
    s.stroke([(x, y), (x + ln * math.cos(a), y + ln * math.sin(a))], "bristle", col,
             size=sz, load=1.0, load_falloff=0.15, pressure="swell")

# the boat's few deliberate marks
s.stroke([(0.232, 0.674), (0.318, 0.687)], "round_hard", "rim", size=0.005,
         pressure=[0.5, 1.0, 0.4])
s.stroke([(0.352, 0.692), (0.462, 0.701)], "round_hard", "rim", size=0.005,
         pressure=[0.4, 1.0, 0.5])
s.stroke([(0.508, 0.701), (0.566, 0.681)], "round_hard", "rim2", size=0.004,
         pressure=[0.8, 0.3])
s.stroke([(0.292, 0.629), (0.402, 0.627)], "round_hard", "rim2", size=0.004,
         pressure=[0.4, 1.0, 0.4])
s.stroke([(0.468, 0.634), (0.558, 0.655)], "round_hard", "rim2", size=0.004,
         pressure=[0.6, 1.0, 0.3])
s.stroke([(0.204, 0.652), (0.212, 0.686)], "round_hard", "stem", size=0.006,
         pressure=[1.0, 0.6])
s.stroke([(0.209, 0.656), (0.215, 0.676)], "round_hard", "rim2", size=0.003,
         pressure=[0.9, 0.3])
s.stroke([(0.588, 0.672), (0.594, 0.708)], "round_hard", "stem", size=0.005,
         pressure=[0.8, 1.0])
s.stroke([(0.250, 0.702), (0.340, 0.720), (0.418, 0.730)], "round_hard", "lap",
         size=0.004, pressure=[0.3, 1.0, 0.5])
s.stroke([(0.462, 0.733), (0.548, 0.726)], "round_hard", "lap", size=0.0035,
         pressure=[0.8, 0.2])
s.stroke([(0.330, 0.664), (0.356, 0.678)], "round_hard", "rim2", size=0.005,
         pressure=[1.0, 0.5])
s.stroke([(0.206, 0.664), (0.148, 0.706), (0.086, 0.742), (0.030, 0.758)],
         "liner", "warp", size=0.0035, pressure=[1.0, 0.9, 0.5, 0.2])

# the lightest lights, last and few
s.dab(0.470, 0.446, "round_hard", "glint", size=0.008, press=3)
s.dab(0.258, 0.461, "round_hard", "glint", size=0.007, press=3)
s.dab(0.633, 0.469, "round_hard", "glint", size=0.005, press=3)
s.dab(0.541, 0.694, "round_hard", "glint", size=0.005, press=3)
s.dab(0.912, 0.717, "round_hard", "glint", size=0.004, press=3)

print("total", s.stroke_count)
print(s.look())
print(s.look(values=True))
