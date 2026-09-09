# Pass 15 — paint the mug's light mass. Third try; 14a and 14b were rehearsals.
# Fixed since 14b: at_value() reached 0.80 by SHADING white-with-cerulean, and
# shade() adds umber, so the highlights came out olive (#bfd0cb). All the mug
# tones are now tints of one blue-grey, so they stay in the same family.
# Run: python -m easel run painting.easel c15_mugpaint.py
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


BLUEGREY = D(M("cerulean", "burnt_umber", 0.32), 0.22)
for name, v in [("m36", 0.36), ("m55", 0.55), ("m70", 0.70), ("m80", 0.80),
                ("m72", 0.72), ("m62", 0.62), ("m88", 0.88)]:
    p[name] = at_value(BLUEGREY, v)
    print(f"{name} {p.hex(p[name])} {p.value_of(p[name]):.3f}")


def curve(knots):
    def at(x):
        for (x0, y0), (x1, y1) in zip(knots, knots[1:]):
            if x0 <= x <= x1:
                return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
        return knots[-1][1] if x > knots[-1][0] else knots[0][1]
    return at


FRONT = curve([(0.312, 0.192), (0.333, 0.258), (0.368, 0.290), (0.415, 0.310),
               (0.470, 0.318), (0.525, 0.310), (0.578, 0.288), (0.618, 0.258),
               (0.636, 0.222)])
BOT = curve([(0.312, 0.192), (0.330, 0.353), (0.350, 0.531), (0.360, 0.620),
             (0.377, 0.638), (0.410, 0.658), (0.456, 0.669), (0.505, 0.663),
             (0.542, 0.644), (0.570, 0.518), (0.600, 0.383), (0.636, 0.222)])


def tone(x):
    if x < 0.337:
        return "m36", 0.026
    if x < 0.368:
        return "m55", 0.034
    if x < 0.420:
        return "m70", 0.046
    if x < 0.548:
        return "m80", 0.050
    if x < 0.600:
        return "m72", 0.042
    return "m62", 0.030


s.dry()
n0 = s.stroke_count
x = 0.318
while x < 0.636:
    t, b = FRONT(x), BOT(x)
    if b - t >= 0.012:
        col, sz = tone(x)
        s.stroke([(x, t - 0.006), (x, b + 0.006)], "flat", col, size=sz,
                 load=1.0, load_falloff=0.1, pressure="even")
    x += 0.013
print("vertical:", s.stroke_count - n0)

# cross-passes: close the mass and kill the vertical banding; alternate direction
n0 = s.stroke_count
rows = [(0.345, "m70", 0.030), (0.400, "m80", 0.036), (0.455, "m80", 0.036),
        (0.520, "m80", 0.034), (0.580, "m72", 0.030), (0.628, "m70", 0.024)]
for i, (y, col, sz) in enumerate(rows):
    lx = 0.312 + (y - 0.192) * 0.112
    rx = 0.636 - (y - 0.222) * 0.223
    a, b = (lx + 0.014, y), (rx - 0.012, y)
    if i % 2:
        a, b = b, a
    s.stroke([a, b], "flat", col, size=sz, load=0.95, load_falloff=0.15,
             pressure="even", opacity=0.6)
# the base: run along the arc so the sawtooth bottom becomes a curve
s.stroke([(0.362, 0.622), (0.410, 0.655), (0.456, 0.664), (0.505, 0.658),
          (0.540, 0.640)], "flat", "m62", size=0.020, load=1.0, pressure="even")
print("cross:", s.stroke_count - n0)

print(s.look(region=span("C1", "G7"), reference=REF))
print("total strokes:", s.stroke_count)
