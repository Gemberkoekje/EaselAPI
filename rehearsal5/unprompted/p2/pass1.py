p = s.palette
WHITE = "titanium_white"


def to_value(base, target):
    a, b = 0.0, 1.0
    for _ in range(24):
        m = (a + b) / 2
        a, b = (m, b) if p.value_of(p.mix(base, WHITE, m)) < target else (a, m)
    return p.mix(base, WHITE, (a + b) / 2)


p["deep"] = to_value(p.mix("ultramarine", "burnt_umber", 0.58), 0.16)
p["weed_g"] = to_value(p.mix("viridian", "burnt_umber", 0.48), 0.22)
p["weed_c"] = to_value(p.mix("ultramarine", "viridian", 0.45), 0.27)
p["silt"] = to_value(p.mix("burnt_umber", "viridian", 0.35), 0.33)
p["rent"] = to_value(p.mix("cerulean", "burnt_sienna", 0.20), 0.78)
p["leaf"] = to_value(p.mix("burnt_sienna", "yellow_ochre", 0.45), 0.52)
for n in ("deep", "weed_g", "weed_c", "silt", "rent", "leaf"):
    print(f"{n:7s} {p.hex(p[n])}  {p.value_of(p[n]):.2f}")

# geometry probe: blob given a point rather than a region
b1 = blob((0.5, 0.5), 0.18, 0.12, wobble=0.35, seed=3)
b2 = blob((0.5, 0.5), 0.18, wobble=0.35, seed=3)
h1 = hull([(0.2, 0.2), (0.6, 0.15), (0.7, 0.5), (0.25, 0.55)])
for nm, sh in (("blob rx ry", b1), ("blob r only", b2), ("hull", h1)):
    print(f"{nm:11s} box={sh.box} axis={round(sh.axis,1)} area={sh.area:.4f}")
print("cell D5", cell("D5"), " span C2:F5", span("C2", "F5"))

# the whole field, deepest first, crossed so it reads as paint not comb
s.block_in(region("all"), "bristle", "deep", direction=(22, 112), density=0.85,
           size=0.16, load=1.0, load_falloff=0.22, pressure="even")
print("strokes", s.stroke_count)
print(s.look(grid=True))
