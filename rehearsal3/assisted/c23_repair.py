# Pass 23 — work down the compare list, largest first.
#   F2,F4,F5,F6,G4,E7,E8,D8 are -0.12..-0.16: my wood is too dark. The seam pass
#     in c11 went over the light band at opacity 0.55 and knocked it all back.
#   D2,D4,D5,D6,E5 are +0.15..+0.22: the darks are not dark enough. Small brushes
#     do not cover, so restate the interiors with a fat one.
# Run: python -m easel run painting.easel c23_repair.py
REF = r"C:\temp\Level1.jpg"
p = s.palette
M, T, D, S = p.mix, p.tint, p.desaturate, p.shade


def at_value(base, target):
    if p.value_of(base) < target:
        lo, hi, f = 0.0, 1.0, T
    else:
        lo, hi, f = 0.0, 1.0, S
    for _ in range(24):
        mid = (lo + hi) / 2
        if (p.value_of(f(base, mid)) < target) == (f is T):
            lo = mid
        else:
            hi = mid
    return f(base, (lo + hi) / 2)


p["wood_br"] = at_value(D(M("yellow_ochre", "burnt_umber", 0.30), 0.26), 0.60)
p["wood_br2"] = at_value(D(M("yellow_ochre", "burnt_sienna", 0.25), 0.30), 0.56)
p["fig_dk"] = S(M("burnt_umber", "ultramarine", 0.14), 1.0)
p["tea"] = S(M("ultramarine", "burnt_umber", 0.55), 1.0)
p["shad_core"] = S(M("ultramarine", "burnt_umber", 0.50), 1.0)
for k in ("wood_br", "wood_br2", "fig_dk"):
    print(f"{k:9s} {p.hex(p[k])} {p.value_of(p[k]):.3f}")

s.dry()

# --- 1. the lit wood, right of the mug and along the bottom ---------------
n0 = s.stroke_count
s.block_in(span("F1", "G8"), "flat", "wood_br", density=0.75, size=0.16,
           direction="diagonal")
s.stroke([(0.62, 0.955), (1.00, 0.86)], "flat", "wood_br2", size=0.08,
         load=1.0, load_falloff=0.15, pressure="even", opacity=0.8)
s.stroke([(1.00, 0.78), (0.50, 0.90)], "flat", "wood_br2", size=0.07,
         load=1.0, load_falloff=0.15, pressure="even", opacity=0.8)
s.stroke([(0.46, 0.965), (0.98, 0.94)], "flat", "wood_br", size=0.07,
         load=1.0, load_falloff=0.15, pressure="even", opacity=0.8)
s.stroke([(0.62, 0.700), (0.68, 0.845)], "flat", "wood_br", size=0.09,
         load=1.0, load_falloff=0.15, pressure="even", opacity=0.7)
print("wood lift:", s.stroke_count - n0)

# --- 2. the crewmate's interior, fat brush so it actually covers -----------
n0 = s.stroke_count
for i, (y, lx, rx, sz) in enumerate([(0.425, 0.378, 0.462, 0.038),
                                     (0.480, 0.368, 0.515, 0.048),
                                     (0.530, 0.368, 0.515, 0.048),
                                     (0.578, 0.368, 0.464, 0.045),
                                     (0.620, 0.372, 0.462, 0.032)]):
    pts = [(lx, y), (rx, y)]
    s.stroke(pts if i % 2 == 0 else pts[::-1], "flat", "fig_dk", size=sz,
             load=1.0, load_falloff=0.05, pressure="even", opacity=1.0)
print("figure solid:", s.stroke_count - n0)

# --- 3. the tea's interior ------------------------------------------------
n0 = s.stroke_count
for i, (y, lx, rx, sz) in enumerate([(0.170, 0.430, 0.590, 0.035),
                                     (0.215, 0.404, 0.612, 0.048),
                                     (0.262, 0.398, 0.598, 0.044),
                                     (0.300, 0.400, 0.540, 0.030)]):
    pts = [(lx, y), (rx, y)]
    s.stroke(pts if i % 2 == 0 else pts[::-1], "flat", "tea", size=sz,
             load=1.0, load_falloff=0.05, pressure="even", opacity=1.0)
print("tea solid:", s.stroke_count - n0)

# --- 4. the shadow's core, and push it further left and down --------------
n0 = s.stroke_count
for i, (y, lx, rx, sz) in enumerate([(0.690, 0.300, 0.575, 0.045),
                                     (0.735, 0.292, 0.552, 0.045),
                                     (0.640, 0.306, 0.372, 0.036),
                                     (0.640, 0.530, 0.600, 0.036),
                                     (0.780, 0.300, 0.505, 0.040)]):
    pts = [(lx, y), (rx, y)]
    s.stroke(pts if i % 2 == 0 else pts[::-1], "flat", "shad_core", size=sz,
             load=1.0, load_falloff=0.08, pressure="even", opacity=0.9)
print("shadow core:", s.stroke_count - n0)

print(s.look(reference=REF))
print("total strokes:", s.stroke_count)
