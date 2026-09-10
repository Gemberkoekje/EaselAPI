import math
import random

p = s.palette
rng = random.Random(83)
WHITE = "titanium_white"


def to_value(base, target):
    a, b = 0.0, 1.0
    for _ in range(24):
        m = (a + b) / 2
        a, b = (m, b) if p.value_of(p.mix(base, WHITE, m)) < target else (a, m)
    return p.mix(base, WHITE, (a + b) / 2)


p["wet_mud"] = to_value(p.mix("burnt_umber", "ultramarine", 0.22), 0.25)
p["runnel"] = to_value(p.mix("burnt_sienna", "yellow_ochre", 0.30), 0.38)
p["weed"] = to_value(p.mix("viridian", "burnt_umber", 0.45), 0.19)
p["glint"] = to_value(p.mix("yellow_ochre", "cadmium_red", 0.15), 0.89)

s.dry()

# a wedge of wet mud running in from the near corner - the foreground dark
s.block_in(polygon([(-0.05, 0.826), (0.14, 0.882), (0.30, 0.940), (0.43, 1.02),
                    (-0.05, 1.02)]), "bristle", "wet_mud", direction="axis",
           density=1.0, size=0.045, load=1.0, load_falloff=0.18, pressure="even")

# its lit lip, broken, and some tide-line litter along it
for x0, y0, x1, y1, sz, col in ((-0.03, 0.828, 0.075, 0.852, 0.016, "runnel"),
                                (0.096, 0.866, 0.196, 0.906, 0.013, "runnel"),
                                (0.228, 0.918, 0.318, 0.962, 0.011, "runnel"),
                                (0.045, 0.900, 0.120, 0.930, 0.009, "weed"),
                                (0.175, 0.952, 0.262, 0.988, 0.008, "weed")):
    s.stroke([(x0, y0), (x1, y1)], "bristle", col, size=sz, load=0.95,
             pressure="swell")

# a few strands of weed caught on the flats, at the boat's foot
for x0, y0, x1, y1, sz in ((0.588, 0.802, 0.660, 0.812, 0.007),
                           (0.318, 0.806, 0.372, 0.796, 0.006),
                           (0.700, 0.868, 0.782, 0.882, 0.008)):
    s.stroke([(x0, y0), (x1, y1)], "bristle", "weed", size=sz, load=0.9,
             pressure="taper")

# stretch the three round glints into something lying flat on water
for x, y, w in ((0.470, 0.446, 0.020), (0.258, 0.461, 0.016), (0.633, 0.469, 0.013)):
    s.stroke([(x - w / 2, y + 0.001), (x + w / 2, y)], "round_hard", "glint",
             size=0.005, pressure=[0.35, 1.0, 0.3])

print("total", s.stroke_count)
print(s.look())
print(s.look(values=True))
