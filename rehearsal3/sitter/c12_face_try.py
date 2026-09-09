# Pass 12: REHEARSAL of the whole face mass + modelling, before spending 22 strokes.
REF = "C:/temp/Level3.jpg"
p = s.palette
p["sk_hi"]  = p.mix(p.mix("yellow_ochre", "cadmium_red", 0.12), "titanium_white", 0.72)
p["sk_lit"] = p.mix(p.mix("yellow_ochre", "cadmium_red", 0.18), "titanium_white", 0.55)
p["sk_mid"] = p.mix(p.mix("burnt_sienna", "yellow_ochre", 0.55), "titanium_white", 0.40)
p["sk_shad"] = p.desaturate(
    p.mix(p.mix("burnt_sienna", "burnt_umber", 0.40), "titanium_white", 0.30), 0.20)
p["sk_dk"]  = p.mix(p.mix("burnt_umber", "burnt_sienna", 0.35), "titanium_white", 0.14)
for n in ("sk_hi", "sk_lit", "sk_mid", "sk_shad", "sk_dk"):
    print(n, p.hex(p[n]), round(p.value_of(p[n]), 2))


def edge(knots):
    def at(x):
        for (x0, y0), (x1, y1) in zip(knots, knots[1:]):
            if x0 <= x <= x1:
                return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
        return knots[-1][1]
    return at


top = edge([(0.400, 0.200), (0.420, 0.210), (0.437, 0.248), (0.458, 0.270),
            (0.482, 0.288), (0.512, 0.306), (0.542, 0.327), (0.568, 0.350),
            (0.600, 0.380)])
bot = edge([(0.400, 0.398), (0.420, 0.400), (0.440, 0.410), (0.460, 0.424),
            (0.482, 0.442), (0.512, 0.470), (0.542, 0.502), (0.568, 0.476),
            (0.600, 0.440)])

base = []
xs = [0.418 + i * 0.0164 for i in range(11)]
for i, x in enumerate(xs):
    col = "sk_mid" if i < 2 else "sk_lit"
    base.append({"points": [(x, top(x) - 0.004), (x, bot(x) + 0.004)],
                 "brush": "flat", "color": col, "size": 0.040,
                 "load": 1.0, "pressure": "even"})

model = [
    # forehead light
    {"points": [(0.424, 0.232), (0.462, 0.256), (0.492, 0.278)], "brush": "bristle",
     "color": "sk_hi", "size": 0.030, "load": 1.0, "pressure": "swell"},
    {"points": [(0.421, 0.258), (0.452, 0.278), (0.478, 0.296)], "brush": "bristle",
     "color": "sk_hi", "size": 0.022, "load": 1.0, "pressure": "taper"},
    # cheek light
    {"points": [(0.492, 0.322), (0.532, 0.352), (0.560, 0.392)], "brush": "bristle",
     "color": "sk_hi", "size": 0.036, "load": 1.0, "pressure": "swell"},
    {"points": [(0.470, 0.330), (0.505, 0.362), (0.532, 0.400)], "brush": "bristle",
     "color": "sk_lit", "size": 0.030, "load": 1.0, "pressure": "taper"},
    # eye socket shadow
    {"points": [(0.428, 0.300), (0.452, 0.306), (0.478, 0.312)], "brush": "round_soft",
     "color": "sk_shad", "size": 0.020, "load": 1.0, "pressure": "even"},
    # side of the nose
    {"points": [(0.419, 0.318), (0.427, 0.348), (0.432, 0.378)], "brush": "bristle",
     "color": "sk_shad", "size": 0.016, "load": 1.0, "pressure": "taper"},
    # under the cheekbone, turning into the beard
    {"points": [(0.462, 0.382), (0.502, 0.408), (0.540, 0.440)], "brush": "bristle",
     "color": "sk_shad", "size": 0.024, "load": 0.9, "pressure": "taper"},
    # shadow under the nose
    {"points": [(0.410, 0.394), (0.428, 0.398), (0.444, 0.396)], "brush": "round_hard",
     "color": "sk_dk", "size": 0.012, "load": 1.0, "pressure": "even"},
    # temple, just under the hairline
    {"points": [(0.440, 0.256), (0.478, 0.288), (0.512, 0.316)], "brush": "bristle",
     "color": "sk_mid", "size": 0.018, "load": 0.8, "pressure": "taper"},
    # neck / under-jaw
    {"points": [(0.498, 0.536), (0.545, 0.556), (0.592, 0.556)], "brush": "flat",
     "color": "sk_mid", "size": 0.034, "load": 1.0, "pressure": "even"},
    {"points": [(0.506, 0.566), (0.552, 0.582), (0.588, 0.576)], "brush": "flat",
     "color": "sk_shad", "size": 0.028, "load": 1.0, "pressure": "even"},
]

print("face rehearsal:", s.rehearse(base + model, reference=REF,
                                    region=span("D2", "F5")))
print("strokes (unchanged):", s.stroke_count)
