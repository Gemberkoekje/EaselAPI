import math
import random

p = s.palette
rng = random.Random(97)
WHITE = "titanium_white"


def to_value(base, target):
    a, b = 0.0, 1.0
    for _ in range(24):
        m = (a + b) / 2
        a, b = (m, b) if p.value_of(p.mix(base, WHITE, m)) < target else (a, m)
    return p.mix(base, WHITE, (a + b) / 2)


p["rip_lt"] = p.desaturate(to_value(p.mix("cerulean", "burnt_umber", 0.30), 0.62), 0.30)
p["rip_md"] = p.desaturate(to_value(p.mix("cerulean", "burnt_umber", 0.45), 0.46), 0.35)
p["rip_dk"] = p.desaturate(to_value(p.mix("ultramarine", "burnt_umber", 0.50), 0.26), 0.40)
p["field_up"] = p.desaturate(to_value(p.mix("viridian", "burnt_umber", 0.40), 0.235), 0.55)
p["cool"] = p.desaturate(to_value(p.mix("cerulean", "ultramarine", 0.35), 0.55), 0.30)

s.dry()

# knock the orange lobe back with a cool film rather than repainting it
s.glaze([(0.556, 0.318), (0.640, 0.348), (0.734, 0.388)], "cool", opacity=0.30)
s.glaze([(0.566, 0.336), (0.660, 0.372)], "cool", opacity=0.22)

POOLS = [(0.688, 0.120, 0.075, 0.070, "rip_lt"), (0.576, 0.264, 0.070, 0.052, "rip_lt"),
         (0.650, 0.352, 0.090, 0.045, "rip_md"), (0.452, 0.400, 0.058, 0.050, "rip_md"),
         (0.500, 0.198, 0.075, 0.038, "rip_md"), (0.322, 0.524, 0.048, 0.036, "rip_md"),
         (0.238, 0.646, 0.032, 0.024, "rip_dk")]

WIND = 24.0

# ripples inside the pools - across the comb, so the striping goes
for cx, cy, rx, ry, col in POOLS:
    for _ in range(3):
        a = math.radians(WIND + rng.uniform(-7, 7))
        ln = rx * rng.uniform(1.1, 1.7)
        ox = rng.uniform(-rx * 0.5, rx * 0.5)
        oy = rng.uniform(-ry * 0.6, ry * 0.6)
        s.stroke([(cx + ox - ln / 2, cy + oy - ln * 0.5 * math.tan(a)),
                  (cx + ox + ln / 2, cy + oy + ln * 0.5 * math.tan(a))],
                 "bristle", col, size=max(0.006, ry * rng.uniform(0.20, 0.34)),
                 load=rng.uniform(0.55, 0.85), pressure="swell")

# the same wind across the dark field, barely above it
for _ in range(22):
    x = rng.uniform(-0.05, 1.00)
    y = rng.uniform(-0.02, 1.00)
    a = math.radians(WIND + rng.uniform(-8, 8))
    ln = rng.uniform(0.09, 0.30)
    s.stroke([(x, y), (x + ln * math.cos(a), y + ln * math.sin(a))], "bristle",
             "field_up", size=rng.uniform(0.010, 0.030), load=rng.uniform(0.45, 0.75),
             pressure=rng.choice(["taper", "swell", "lift_off"]))

print("strokes", s.stroke_count)
print(s.look())
