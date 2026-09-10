import math
import random

p = s.palette
rng = random.Random(131)
WHITE = "titanium_white"


def to_value(base, target):
    a, b = 0.0, 1.0
    for _ in range(24):
        m = (a + b) / 2
        a, b = (m, b) if p.value_of(p.mix(base, WHITE, m)) < target else (a, m)
    return p.mix(base, WHITE, (a + b) / 2)


p["dark_film"] = p.mix("ultramarine", "burnt_umber", 0.50)
p["weed_x"] = p.desaturate(to_value(p.mix("viridian", "burnt_umber", 0.55), 0.185), 0.50)
p["weed_y"] = p.desaturate(to_value(p.mix("burnt_umber", "viridian", 0.40), 0.245), 0.50)
p["leaf_s"] = p.desaturate(to_value(p.mix("burnt_umber", "burnt_sienna", 0.35), 0.36), 0.35)
p["leaf_v"] = p.desaturate(to_value(p.mix("yellow_ochre", "burnt_umber", 0.40), 0.55), 0.35)
p["spark"] = p.desaturate(to_value(p.mix("cerulean", "yellow_ochre", 0.25), 0.93), 0.20)
print("dark_film", p.hex(p["dark_film"]), round(p.value_of(p["dark_film"]), 2))

s.dry()

# knock the pale silt back with a film rather than burying the leaves on it
s.glaze([(0.235, 0.662), (0.400, 0.638), (0.560, 0.652)], "dark_film",
        opacity=0.30, size=0.075)
s.glaze([(0.250, 0.730), (0.360, 0.744), (0.470, 0.726)], "dark_film",
        opacity=0.26, size=0.070)
s.glaze([(0.290, 0.800), (0.440, 0.812), (0.600, 0.786)], "dark_film",
        opacity=0.24, size=0.065)
s.glaze([(0.520, 0.688), (0.640, 0.700)], "dark_film", opacity=0.22, size=0.060)

# and the strip running down the right edge, so it stops pulling the eye off
s.glaze([(0.905, 0.060), (0.880, 0.280), (0.905, 0.480), (0.940, 0.640)],
        "dark_film", opacity=0.26, size=0.110)
s.glaze([(0.975, 0.120), (0.960, 0.400), (0.985, 0.620)], "dark_film",
        opacity=0.22, size=0.080)

# break the woodgrain in the weed - crossing it, close in value
for _ in range(8):
    x = rng.uniform(-0.05, 1.00)
    y = rng.uniform(0.560, 1.00)
    a = math.radians(rng.uniform(58, 118))
    ln = rng.uniform(0.06, 0.16)
    s.stroke([(x, y), (x + ln * math.cos(a), y + ln * math.sin(a))], "bristle",
             rng.choice(["weed_x", "weed_y"]), size=rng.uniform(0.016, 0.042),
             load=rng.uniform(0.8, 1.0), pressure="swell")

# leaves that are not lozenges: seen end-on, and one half sunk
for cx, cy, sz, col in ((0.196, 0.212, 0.016, "leaf_s"), (0.628, 0.470, 0.013, "leaf_s"),
                        (0.462, 0.842, 0.015, "leaf_v"), (0.842, 0.690, 0.012, "leaf_s")):
    s.dab(cx, cy, "round_hard", col, size=sz, press=3)
s.stroke([(0.060, 0.874), (0.126, 0.848), (0.196, 0.856)], "round_hard", "leaf_v",
         size=0.019, pressure=[0.4, 1.0, 0.6])
s.stroke([(0.552, 0.246), (0.598, 0.276)], "round_hard", "leaf_s", size=0.014,
         pressure="swell")
# half-sink two of the lozenges under the water's skin
s.stroke([(0.336, 0.916), (0.362, 0.900)], "bristle", "dark_film", size=0.018,
         load=0.9, pressure="swell")
s.stroke([(0.722, 0.752), (0.756, 0.746)], "bristle", "dark_film", size=0.016,
         load=0.9, pressure="swell")

# the lightest lights, last and few
s.dab(0.700, 0.086, "round_hard", "spark", size=0.010, press=3)
s.dab(0.556, 0.246, "round_hard", "spark", size=0.008, press=3)
s.dab(0.470, 0.362, "round_hard", "spark", size=0.006, press=3)
s.dab(0.318, 0.512, "round_hard", "spark", size=0.005, press=3)
s.dab(0.646, 0.336, "round_hard", "spark", size=0.006, press=3)

print("strokes", s.stroke_count)
print(s.look())
print(s.look(values=True))
