import math
import random

p = s.palette
rng = random.Random(17)
WHITE = "titanium_white"


def to_value(base, target):
    a, b = 0.0, 1.0
    for _ in range(24):
        m = (a + b) / 2
        a, b = (m, b) if p.value_of(p.mix(base, WHITE, m)) < target else (a, m)
    return p.mix(base, WHITE, (a + b) / 2)


p["rill_d"] = to_value(p.mix("burnt_umber", "ultramarine", 0.28), 0.33)
p["rill_l"] = to_value(p.mix("yellow_ochre", "burnt_sienna", 0.35), 0.60)
p["silt"] = to_value(p.mix("burnt_sienna", "ultramarine", 0.30), 0.43)
p["pud_c"] = to_value(p.mix("cerulean", "burnt_sienna", 0.32), 0.73)
p["pud_w"] = to_value(p.mix("yellow_ochre", "cadmium_red", 0.28), 0.78)
p["ch_f"] = to_value(p.mix("yellow_ochre", "cadmium_red", 0.24), 0.81)
p["ch_m"] = to_value(p.mix("cerulean", "burnt_sienna", 0.28), 0.66)
p["ch_n"] = to_value(p.mix("ultramarine", "burnt_sienna", 0.42), 0.50)

s.dry()


def drain_x(y):
    pts = [(0.40, 0.86), (0.46, 0.836), (0.56, 0.878), (0.63, 0.866),
           (0.70, 0.812), (0.80, 0.766), (0.95, 0.723), (1.05, 0.706)]
    for (y0, x0), (y1, x1) in zip(pts, pts[1:]):
        if y0 <= y <= y1:
            t = (y - y0) / (y1 - y0)
            return x0 + t * (x1 - x0)
    return 0.80


# rills draining across the flats toward the creek - kills the horizontal banding
n = 0
for _ in range(34):
    y = 0.40 + (rng.random() ** 0.75) * 0.60
    x = rng.uniform(-0.02, 1.00)
    depth = (y - 0.375) / 0.63
    ln = 0.05 + depth * rng.uniform(0.10, 0.30)
    dx = drain_x(min(y, 1.0)) - x
    ang = math.degrees(math.atan2(0.035 + depth * 0.05, dx if abs(dx) > 0.02 else 0.02))
    ang = max(-52.0, min(52.0, ang - 90.0 if dx < 0 else 90.0 - ang))
    ang += rng.uniform(-7.0, 7.0)
    a = math.radians(ang)
    col = rng.choice(["rill_d", "rill_l", "silt", "silt", "mud_far", "mud_near"])
    sz = 0.008 + depth * rng.uniform(0.010, 0.040)
    s.stroke([(x, y), (x + ln * math.cos(a), y + ln * math.sin(a))], "bristle", col,
             size=sz, load=rng.uniform(0.5, 0.95), pressure=rng.choice(
                 ["taper", "lift_off", "swell", "press_in"]))
    n += 1

# standing water caught flat on the mud
for x, y, w, c in [(0.115, 0.470, 0.070, "pud_c"), (0.335, 0.452, 0.052, "pud_w"),
                   (0.612, 0.442, 0.044, "pud_c"), (0.470, 0.497, 0.085, "pud_w"),
                   (0.185, 0.560, 0.105, "pud_c"), (0.745, 0.512, 0.062, "pud_w"),
                   (0.055, 0.640, 0.120, "pud_c"), (0.905, 0.690, 0.115, "pud_w"),
                   (0.380, 0.905, 0.170, "pud_c")]:
    s.stroke([(x - w / 2, y), (x + w / 2, y + rng.uniform(-0.006, 0.006))], "flat", c,
             size=0.010 + w * 0.10, pressure="even", load=1.0)
    n += 1

# the creek, back to front, bright at the horizon and cooler as it nears
s.block_in(ribbon([(0.985, 0.383), (0.930, 0.404), (0.868, 0.428), (0.836, 0.462)],
                  0.010, 0.030), "flat", "ch_f", direction="axis", density=1.0,
           size=0.014, pressure="even", load=1.0)
s.block_in(ribbon([(0.836, 0.458), (0.848, 0.508), (0.878, 0.556), (0.866, 0.630)],
                  0.030, 0.050), "flat", "ch_m", direction="axis", density=1.0,
           size=0.022, pressure="even", load=1.0)
s.block_in(ribbon([(0.866, 0.624), (0.812, 0.700), (0.766, 0.802), (0.726, 0.935),
                   (0.706, 1.010)], 0.050, 0.095), "flat", "ch_n", direction="axis",
           density=1.0, size=0.034, pressure="even", load=1.0)

print("marks this pass", n, "total", s.stroke_count)
print(s.look(grid=True))
