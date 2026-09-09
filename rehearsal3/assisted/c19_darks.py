# Pass 19 — compare() in tenths says the mug's left face and the band under the
# front lip are 0.22-0.28 in the reference and 0.52-0.65 on my canvas. My eye
# read that passage as "pale mug"; the numbers say it is nearly as dark as the
# tea. Fix the darks, then rehearse the figure.
# Run: python -m easel run painting.easel c19_darks.py
REF = r"C:\temp\Level1.jpg"
p = s.palette
M, T, D, S = p.mix, p.tint, p.desaturate, p.shade

p["tea"] = S(M("ultramarine", "burnt_umber", 0.55), 1.0)
p["under"] = T(S(M("ultramarine", "burnt_umber", 0.50), 1.0), 0.10)
p["face_dk"] = T(S(M("ultramarine", "burnt_umber", 0.42), 1.0), 0.16)
p["fig_dk"] = S(M("burnt_umber", "ultramarine", 0.14), 1.0)
p["fig_md"] = M("burnt_umber", "burnt_sienna", 0.32)
p["fig_lt"] = T(M("burnt_umber", "burnt_sienna", 0.55), 0.13)
p["visor"] = T(D(M("cerulean", "burnt_umber", 0.40), 0.35), 0.55)
for k in ("tea", "under", "face_dk", "fig_dk", "fig_md", "fig_lt", "visor"):
    print(f"{k:8s} {p.hex(p[k])} {p.value_of(p[k]):.3f}")

s.dry()
n0 = s.stroke_count
# tea reaches further down and further left than I had it
for i, (y, lx, rx) in enumerate([(0.270, 0.378, 0.605), (0.290, 0.374, 0.585),
                                 (0.308, 0.380, 0.556), (0.322, 0.398, 0.522)]):
    a, b = ((lx, y), (rx, y)) if i % 2 == 0 else ((rx, y), (lx, y))
    s.stroke([a, b], "flat", "tea", size=0.022, load=1.0, load_falloff=0.05,
             pressure="even")
# the shadow the lip throws on the body just under it
s.stroke([(0.355, 0.330), (0.420, 0.348), (0.500, 0.352), (0.556, 0.340)],
         "flat", "under", size=0.024, load=1.0, load_falloff=0.1, pressure="even")
s.stroke([(0.545, 0.352), (0.470, 0.364), (0.400, 0.358), (0.352, 0.344)],
         "flat", "under", size=0.018, load=1.0, load_falloff=0.1, pressure="even")
# the mug's shaded left face, from under the lip down to the figure
for i, x in enumerate([0.334, 0.346, 0.358, 0.370]):
    a, b = ((x, 0.320), (x, 0.470)) if i % 2 == 0 else ((x, 0.470), (x, 0.320))
    s.stroke([a, b], "flat", "face_dk", size=0.016, load=1.0, load_falloff=0.1,
             pressure="even", opacity=0.85)
print("darks:", s.stroke_count - n0)

# --- rehearse the figure ---------------------------------------------------
def curve(knots):
    def at(x):
        for (x0, y0), (x1, y1) in zip(knots, knots[1:]):
            if x0 <= x <= x1:
                return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
        return knots[-1][1] if x > knots[-1][0] else knots[0][1]
    return at


TOPF = curve([(0.355, 0.470), (0.362, 0.432), (0.380, 0.410), (0.414, 0.399),
              (0.450, 0.397), (0.478, 0.404), (0.500, 0.422), (0.508, 0.450),
              (0.512, 0.472), (0.550, 0.475)])
BOTF = curve([(0.355, 0.625), (0.378, 0.652), (0.425, 0.655), (0.428, 0.628),
              (0.452, 0.628), (0.455, 0.655), (0.505, 0.652), (0.513, 0.598),
              (0.550, 0.592)])

plan = []
x = 0.357
while x < 0.550:
    t, b = TOPF(x), BOTF(x)
    col = "fig_md" if (0.375 < x < 0.470 and t < 0.45) else "fig_dk"
    plan.append({"points": [(x, t + 0.004), (x, b - 0.004)][::(1 if len(plan) % 2 == 0 else -1)],
                 "brush": "flat", "color": col, "size": 0.020, "load": 1.0,
                 "load_falloff": 0.08, "pressure": "even"})
    x += 0.013
print("figure plan:", len(plan))
print(s.rehearse(plan, reference=REF, region=span("C3", "F6")))
print("total strokes:", s.stroke_count)
