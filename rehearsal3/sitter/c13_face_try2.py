# Pass 13: REHEARSAL of face plan B — horizontal sweeps, cooler skin.
REF = "C:/temp/Level3.jpg"
p = s.palette
p["sk_hi"]   = p.mix(p.mix("burnt_sienna", "yellow_ochre", 0.38), "titanium_white", 0.76)
p["sk_lit"]  = p.mix(p.mix("burnt_sienna", "yellow_ochre", 0.44), "titanium_white", 0.62)
p["sk_mid"]  = p.mix(p.mix("burnt_sienna", "yellow_ochre", 0.40), "titanium_white", 0.46)
p["sk_shad"] = p.desaturate(
    p.mix(p.mix("burnt_sienna", "burnt_umber", 0.45), "titanium_white", 0.32), 0.22)
p["sk_dk"]   = p.mix(p.mix("burnt_umber", "burnt_sienna", 0.35), "titanium_white", 0.12)
for n in ("sk_hi", "sk_lit", "sk_mid", "sk_shad", "sk_dk"):
    print(n, p.hex(p[n]), round(p.value_of(p[n]), 2))

# y, left x (the profile), right x (jaw / hairline), colour
ROWS = [
    (0.215, 0.4190, 0.440, "sk_lit"),
    (0.240, 0.4165, 0.468, "sk_hi"),
    (0.265, 0.4145, 0.492, "sk_hi"),
    (0.290, 0.4125, 0.515, "sk_lit"),
    (0.315, 0.4135, 0.535, "sk_lit"),
    (0.340, 0.4110, 0.552, "sk_lit"),
    (0.365, 0.4090, 0.566, "sk_lit"),
    (0.390, 0.4085, 0.578, "sk_mid"),
    (0.415, 0.4230, 0.586, "sk_mid"),
    (0.440, 0.4355, 0.588, "sk_mid"),
    (0.465, 0.4410, 0.583, "sk_mid"),
    (0.490, 0.4470, 0.572, "sk_shad"),
    (0.515, 0.4620, 0.556, "sk_shad"),
]
PRESS = ["taper", "lift_off", "even", "swell", "even", "lift_off", "even",
         "taper", "even", "swell", "even", "taper", "lift_off"]

plan = []
for (y, xl, xr, col), pr in zip(ROWS, PRESS):
    mid = (xl + xr) / 2.0
    plan.append({"points": [(xl, y), (mid, y - 0.003), (xr, y + 0.002)],
                 "brush": "flat", "color": col, "size": 0.026,
                 "load": 1.0, "pressure": pr})

# a light cross-pass so the rows are paint and not corduroy
plan += [
    {"points": [(0.430, 0.230), (0.470, 0.300), (0.500, 0.370)], "brush": "bristle",
     "color": "sk_lit", "size": 0.024, "load": 0.55, "pressure": "taper"},
    {"points": [(0.500, 0.310), (0.540, 0.380), (0.560, 0.450)], "brush": "bristle",
     "color": "sk_lit", "size": 0.024, "load": 0.55, "pressure": "swell"},
]
# two small shadows only
plan += [
    {"points": [(0.424, 0.299), (0.450, 0.303), (0.474, 0.307)], "brush": "round_soft",
     "color": "sk_shad", "size": 0.013, "load": 1.0, "opacity": 0.55, "pressure": "even"},
    {"points": [(0.419, 0.322), (0.427, 0.352), (0.431, 0.378)], "brush": "round_soft",
     "color": "sk_shad", "size": 0.010, "load": 1.0, "opacity": 0.5, "pressure": "taper"},
]
print("face plan B:", s.rehearse(plan, reference=REF, region=span("D2", "F5")))
print("strokes (unchanged):", s.stroke_count)
