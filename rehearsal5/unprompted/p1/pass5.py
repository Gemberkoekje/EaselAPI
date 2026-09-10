p = s.palette
WHITE = "titanium_white"


def to_value(base, target):
    a, b = 0.0, 1.0
    for _ in range(24):
        m = (a + b) / 2
        a, b = (m, b) if p.value_of(p.mix(base, WHITE, m)) < target else (a, m)
    return p.mix(base, WHITE, (a + b) / 2)


p["shore"]    = to_value(p.mix("ultramarine", "burnt_umber", 0.50), 0.27)
p["sheen"]    = to_value(p.mix("burnt_sienna", "cerulean", 0.45), 0.70)
p["mud_far"]  = to_value(p.mix("burnt_umber", "ultramarine", 0.30), 0.55)
p["mud_mid"]  = to_value(p.mix("burnt_umber", "yellow_ochre", 0.35), 0.46)
p["mud_near"] = to_value(p.mix("burnt_umber", "burnt_sienna", 0.40), 0.38)
for n in ("shore", "sheen", "mud_far", "mud_mid", "mud_near"):
    print(f"{n:9s} {p.hex(p[n])}  {p.value_of(p[n]):.2f}")

s.dry()

# the far shore: a lumpy strip, not a rule
bank = polygon([
    (0.00, 0.358), (0.07, 0.350), (0.13, 0.355), (0.19, 0.343), (0.24, 0.348),
    (0.31, 0.340), (0.36, 0.353), (0.44, 0.349), (0.50, 0.357), (0.58, 0.350),
    (0.63, 0.359), (0.70, 0.353), (0.77, 0.345), (0.83, 0.353), (0.90, 0.348),
    (1.00, 0.356), (1.00, 0.390), (0.00, 0.392),
])
s.block_in(bank, "flat", "shore", direction="axis", density=1.0,
           size=0.014, load=1.0, load_falloff=0.2, pressure="even")

bands = [
    (ribbon([(0.00, 0.424), (0.43, 0.432), (1.00, 0.420)], 0.082), "sheen",    0.05, 3),
    (ribbon([(0.00, 0.524), (0.47, 0.538), (1.00, 0.520)], 0.140), "mud_far",  0.08, -4),
    (ribbon([(0.00, 0.676), (0.52, 0.690), (1.00, 0.668)], 0.200), "mud_mid",  0.11, 6),
    (ribbon([(0.00, 0.880), (0.49, 0.896), (1.00, 0.872)], 0.290), "mud_near", 0.14, -5),
]
for sh, col, sz, ang in bands:
    s.block_in(sh, "flat", col, direction=ang, density=0.95,
               size=sz, load=1.0, load_falloff=0.25, pressure="even")

print("strokes", s.stroke_count)
print(s.look(grid=True))
print(s.look(values=True))
