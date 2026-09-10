import math
import random

p = s.palette
rng = random.Random(57)
WHITE = "titanium_white"


def to_value(base, target):
    a, b = 0.0, 1.0
    for _ in range(24):
        m = (a + b) / 2
        a, b = (m, b) if p.value_of(p.mix(base, WHITE, m)) < target else (a, m)
    return p.mix(base, WHITE, (a + b) / 2)


p["m_lo"] = to_value(p.mix("burnt_umber", "burnt_sienna", 0.35), 0.28)
p["m_hi"] = to_value(p.mix("burnt_sienna", "yellow_ochre", 0.45), 0.41)
p["sh"] = to_value(p.mix("burnt_umber", "ultramarine", 0.32), 0.28)

s.dry()

# bury the shadow slab and the two smudge lozenges
for y0, y1, sz in ((0.798, 0.806, 0.070), (0.830, 0.838, 0.070), (0.862, 0.856, 0.060)):
    s.stroke([(0.10, y0), (0.38, y1), (0.70, y0 - 0.006)], "bristle", "mud_near",
             size=sz, pressure="even", load=1.0, load_falloff=0.2)

# put the worked surface back into the near mud
for _ in range(12):
    x = rng.uniform(-0.02, 0.80)
    y = rng.uniform(0.790, 0.995)
    ln = rng.uniform(0.09, 0.24)
    a = math.radians(rng.uniform(-13.0, 13.0))
    s.stroke([(x, y), (x + ln * math.cos(a), y + ln * math.sin(a))], "bristle",
             rng.choice(["m_lo", "m_hi", "mud_near", "m_lo"]),
             size=rng.uniform(0.020, 0.052), load=rng.uniform(0.6, 0.95),
             pressure=rng.choice(["taper", "swell", "lift_off"]))

# the shadow, as broken marks hugging the hull rather than a filled slab
for x0, x1, y0, y1, sz in ((0.238, 0.360, 0.792, 0.806, 0.026),
                           (0.330, 0.470, 0.800, 0.806, 0.030),
                           (0.440, 0.556, 0.800, 0.788, 0.024),
                           (0.290, 0.420, 0.818, 0.822, 0.018)):
    s.stroke([(x0, y0), (x1, y1)], "bristle", "sh", size=sz,
             load=0.85, pressure="swell")

print("total", s.stroke_count)
print(s.look(region=span("A5", "H8")))
