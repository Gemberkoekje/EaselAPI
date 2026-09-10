import math
import random

p = s.palette
rng = random.Random(31)
WHITE = "titanium_white"


def to_value(base, target):
    a, b = 0.0, 1.0
    for _ in range(24):
        m = (a + b) / 2
        a, b = (m, b) if p.value_of(p.mix(base, WHITE, m)) < target else (a, m)
    return p.mix(base, WHITE, (a + b) / 2)


p["ch_f"] = to_value(p.mix("yellow_ochre", "cadmium_red", 0.24), 0.82)
p["ch_m"] = to_value(p.mix("cerulean", "burnt_sienna", 0.26), 0.62)
p["ch_n"] = to_value(p.mix("ultramarine", "burnt_sienna", 0.38), 0.45)
p["j_sf"] = p.mix(p["sheen"], p["mud_far"], 0.5)
p["j_fm"] = p.mix(p["mud_far"], p["mud_mid"], 0.5)
p["j_mn"] = p.mix(p["mud_mid"], p["mud_near"], 0.5)

# --- lose the band joins: many small marks, close in value, angled ------------
joins = [(0.468, "j_sf", ("sheen", "mud_far"), 0.020, 0.040),
         (0.598, "j_fm", ("mud_far", "mud_mid"), 0.026, 0.055),
         (0.780, "j_mn", ("mud_mid", "mud_near"), 0.034, 0.075)]
for y0, jc, (ca, cb), smin, smax in joins:
    x = -0.03
    while x < 1.0:
        ln = rng.uniform(0.09, 0.22)
        dy = rng.uniform(-0.030, 0.030)
        ang = rng.uniform(-11.0, 11.0)
        a = math.radians(ang)
        col = rng.choice([jc, jc, ca, cb])
        s.stroke([(x, y0 + dy), (x + ln * math.cos(a), y0 + dy + ln * math.sin(a))],
                 "bristle", col, size=rng.uniform(smin, smax),
                 load=rng.uniform(0.7, 1.0), pressure=rng.choice(["taper", "swell"]))
        x += ln * rng.uniform(0.5, 0.8)

# --- the creek, back to front -------------------------------------------------
s.block_in(ribbon([(0.985, 0.383), (0.936, 0.402), (0.884, 0.424), (0.852, 0.452)],
                  0.008, 0.020), "flat", "ch_f", direction="axis", density=1.0,
           size=0.010, pressure="even", load=1.0)
s.block_in(ribbon([(0.852, 0.449), (0.862, 0.500), (0.884, 0.548), (0.874, 0.616)],
                  0.020, 0.034), "flat", "ch_m", direction="axis", density=1.0,
           size=0.015, pressure="even", load=1.0)
s.block_in(ribbon([(0.874, 0.612), (0.836, 0.686), (0.800, 0.790), (0.772, 0.920),
                   (0.760, 1.010)], 0.034, 0.062), "flat", "ch_n", direction="axis",
           density=1.0, size=0.018, pressure="even", load=1.0)

print("total", s.stroke_count)
print(s.look(grid=True))
