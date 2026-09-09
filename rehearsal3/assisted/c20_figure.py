# Pass 20 — the crewmate. Rehearsal 19 showed (a) one pass at size 0.020 over
# pale mug lands at about 0.35, not 0.23, so it needs crossing, and (b) my
# outline ran to x=0.550 when the reference stops at 0.525, and the legs' gap
# was in the wrong place. Both corrected here.
# Run: python -m easel run painting.easel c20_figure.py
REF = r"C:\temp\Level1.jpg"
p = s.palette
M, T, D, S = p.mix, p.tint, p.desaturate, p.shade

p["fig_dk"] = S(M("burnt_umber", "ultramarine", 0.14), 1.0)
p["fig_md"] = M("burnt_umber", "burnt_sienna", 0.30)
p["visor"] = T(D(M("cerulean", "burnt_umber", 0.40), 0.35), 0.55)
p["visor_hi"] = T(D(M("cerulean", "burnt_umber", 0.30), 0.25), 0.82)


def curve(knots):
    def at(x):
        for (x0, y0), (x1, y1) in zip(knots, knots[1:]):
            if x0 <= x <= x1:
                return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
        return knots[-1][1] if x > knots[-1][0] else knots[0][1]
    return at


TOPF = curve([(0.359, 0.470), (0.364, 0.432), (0.378, 0.410), (0.402, 0.398),
              (0.430, 0.395), (0.452, 0.399), (0.466, 0.412), (0.472, 0.440),
              (0.474, 0.454), (0.525, 0.456)])
BOTF = curve([(0.359, 0.598), (0.364, 0.638), (0.404, 0.646), (0.4065, 0.604),
              (0.430, 0.604), (0.4325, 0.646), (0.470, 0.644), (0.4735, 0.560),
              (0.476, 0.546), (0.525, 0.544)])

s.dry()
n0 = s.stroke_count
i = 0
x = 0.361
while x < 0.524:
    t, b = TOPF(x), BOTF(x)
    if b - t > 0.012:
        col = "fig_md" if (0.372 < x < 0.462 and t < 0.415) else "fig_dk"
        pts = [(x, t + 0.003), (x, b - 0.003)]
        s.stroke(pts if i % 2 == 0 else pts[::-1], "flat", col, size=0.018,
                 load=1.0, load_falloff=0.06, pressure="even")
        i += 1
    x += 0.011
print("figure vertical:", s.stroke_count - n0)

# cross it: horizontal rows between the same two curves, so it becomes a mass
n0 = s.stroke_count
rowspec = [(0.415, 0.372, 0.462), (0.445, 0.361, 0.470), (0.478, 0.360, 0.520),
           (0.510, 0.359, 0.522), (0.540, 0.359, 0.520), (0.572, 0.359, 0.471),
           (0.596, 0.359, 0.471), (0.625, 0.361, 0.404), (0.625, 0.432, 0.470)]
for i, (y, lx, rx) in enumerate(rowspec):
    pts = [(lx, y), (rx, y)]
    s.stroke(pts if i % 2 == 0 else pts[::-1], "flat", "fig_dk", size=0.018,
             load=1.0, load_falloff=0.08, pressure="even", opacity=0.9)
print("figure cross:", s.stroke_count - n0)

# the visor: mid lozenge, then a brighter streak in its left half
s.stroke([(0.376, 0.462), (0.412, 0.452)], "round_hard", "visor", size=0.021,
         load=1.0, pressure="even")
s.stroke([(0.379, 0.459), (0.396, 0.454)], "round_hard", "visor_hi", size=0.013,
         load=1.0, pressure="even")
s.dab(0.383, 0.458, "round_hard", "visor_hi", size=0.010)

print(s.look(region=span("C3", "F6"), reference=REF))
print("total strokes:", s.stroke_count)
