import math
import random

p = s.palette
rng = random.Random(23)
WHITE = "titanium_white"


def to_value(base, target):
    a, b = 0.0, 1.0
    for _ in range(24):
        m = (a + b) / 2
        a, b = (m, b) if p.value_of(p.mix(base, WHITE, m)) < target else (a, m)
    return p.mix(base, WHITE, (a + b) / 2)


p["sheen"] = to_value(p.mix("burnt_sienna", "cerulean", 0.45), 0.70)
p["mud_far"] = to_value(p.mix("burnt_umber", "ultramarine", 0.30), 0.56)
p["mud_mid"] = to_value(p.mix("burnt_umber", "yellow_ochre", 0.35), 0.45)
p["mud_near"] = to_value(p.mix("burnt_umber", "burnt_sienna", 0.45), 0.34)
for n in ("sheen", "mud_far", "mud_mid", "mud_near"):
    print(f"{n:9s} {p.hex(p[n])}  {p.value_of(p[n]):.2f}")

s.dry()

# repaint the flats solid - burying the confetti while nothing stands on them
bands = [
    (ribbon([(0.00, 0.424), (0.43, 0.433), (1.00, 0.419)], 0.086), "sheen", 0.05, 4),
    (ribbon([(0.00, 0.524), (0.47, 0.539), (1.00, 0.519)], 0.145), "mud_far", 0.085, -5),
    (ribbon([(0.00, 0.678), (0.52, 0.692), (1.00, 0.666)], 0.205), "mud_mid", 0.115, 7),
    (ribbon([(0.00, 0.884), (0.49, 0.900), (1.00, 0.874)], 0.300), "mud_near", 0.150, -6),
]
for sh, col, sz, ang in bands:
    s.block_in(sh, "bristle", col, direction=ang, density=1.0,
               size=sz, load=1.0, load_falloff=0.22, pressure="even")
print("after repaint", s.stroke_count)
print(s.look())
