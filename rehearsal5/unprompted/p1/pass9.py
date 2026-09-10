import random

p = s.palette
rng = random.Random(41)
WHITE = "titanium_white"


def to_value(base, target):
    a, b = 0.0, 1.0
    for _ in range(24):
        m = (a + b) / 2
        a, b = (m, b) if p.value_of(p.mix(base, WHITE, m)) < target else (a, m)
    return p.mix(base, WHITE, (a + b) / 2)


p["post"] = to_value(p.mix("burnt_umber", "ultramarine", 0.35), 0.20)
p["post_lit"] = to_value(p.mix("yellow_ochre", "burnt_sienna", 0.40), 0.52)
p["wet"] = to_value(p.mix("burnt_sienna", "cerulean", 0.40), 0.66)
p["wet2"] = to_value(p.mix("yellow_ochre", "cadmium_red", 0.30), 0.71)

s.dry()

# bury the creek properly - three overlapping passes down the near reach
for dx, sz in ((-0.034, 0.090), (0.000, 0.090), (0.034, 0.090)):
    s.stroke([(0.876 + dx, 0.596), (0.838 + dx, 0.688), (0.802 + dx, 0.800),
              (0.772 + dx, 0.955), (0.760 + dx, 1.03)], "bristle", "mud_near",
             size=sz, pressure="even", load=1.0, load_falloff=0.2)
for dx, sz in ((-0.020, 0.055), (0.020, 0.055)):
    s.stroke([(0.850 + dx, 0.440), (0.862 + dx, 0.502), (0.884 + dx, 0.552),
              (0.872 + dx, 0.628)], "bristle", "mud_far", size=sz,
             pressure="even", load=1.0)
s.stroke([(0.995, 0.374), (0.940, 0.396), (0.888, 0.418), (0.850, 0.446)],
         "bristle", "sheen", size=0.042, pressure="even", load=1.0)

# a line of rotting withies stepping back toward the horizon
POSTS = [(0.902, 0.826, 0.112, 0.014, 0.013),
         (0.872, 0.712, 0.078, 0.011, -0.016),
         (0.848, 0.646, 0.064, 0.009, 0.004),
         (0.813, 0.561, 0.036, 0.007, 0.011),
         (0.798, 0.524, 0.032, 0.006, -0.006),
         (0.765, 0.462, 0.017, 0.005, 0.004),
         (0.751, 0.437, 0.013, 0.004, -0.003)]
for x, y, h, w, lean in POSTS:
    s.stroke([(x, y), (x + lean, y - h)], "round_hard", "post", size=w,
             pressure=[1.0, 0.7])
for x, y, h, w, lean in POSTS[:3]:
    s.stroke([(x + w * 0.5, y - h * 0.15), (x + lean + w * 0.4, y - h * 0.8)],
             "round_hard", "post_lit", size=w * 0.42, pressure=[0.4, 1.0, 0.5])
for x, y, h, w, lean in POSTS[:4]:
    s.stroke([(x - w * 1.6, y + h * 0.035), (x + w * 3.4, y + h * 0.055)],
             "bristle", "post", size=w * 0.9, load=0.65, pressure="lift_off")

# broad thin sheets of water lying on the flats
for cx, cy, ln, sz, col in [(0.255, 0.463, 0.190, 0.020, "wet"),
                            (0.470, 0.447, 0.150, 0.015, "wet2"),
                            (0.360, 0.492, 0.230, 0.026, "wet"),
                            (0.630, 0.470, 0.135, 0.017, "wet2"),
                            (0.135, 0.508, 0.145, 0.022, "wet"),
                            (0.560, 0.517, 0.175, 0.024, "wet")]:
    dy = rng.uniform(-0.008, 0.008)
    s.stroke([(cx - ln / 2, cy), (cx, cy + dy), (cx + ln / 2, cy + dy / 2)],
             "bristle", col, size=sz, load=rng.uniform(0.5, 0.8), pressure="swell")

print("total", s.stroke_count)
print(s.look())
