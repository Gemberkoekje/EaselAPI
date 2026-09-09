# Pass 14b — second rehearsal of the mug mass. Rejected in 14a:
#   * step 0.022 at size 0.030-0.044 -> visible vertical slats with a sawtooth top
#   * strokes started at the rim's UPPER arc, painting pale over the whole opening
#   * left column mug_dark 0.30 read as a separate blue-violet object
#   * long strokes ran dry and left brown speckle across the bottom half
# Now: start at the rim's FRONT arc (the body's real top), 55% overlap,
# load_falloff 0.1, a narrower and lighter left edge, six tones not five.
# Run: python -m easel run painting.easel c14b_rehearse2.py
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


cool = D(M("ultramarine", "burnt_umber", 0.35), 0.45)
warmw = M("cerulean", "titanium_white", 0.93)
for name, base, v in [("m36", cool, 0.36), ("m55", cool, 0.55), ("m70", warmw, 0.70),
                      ("m80", warmw, 0.80), ("m72", warmw, 0.72), ("m62", cool, 0.62)]:
    p[name] = at_value(base, v)
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


plan = []
x = 0.318
while x < 0.636:
    t, b = FRONT(x), BOT(x)
    if b - t >= 0.012:
        col, sz = tone(x)
        plan.append({"points": [(x, t - 0.006), (x, b + 0.006)], "brush": "flat",
                     "color": col, "load": 1.0, "load_falloff": 0.1,
                     "pressure": "even", "size": sz})
    x += 0.013
print("planned strokes:", len(plan))
print(s.rehearse(plan, reference=REF, region=span("C1", "G7")))
print("strokes (unchanged):", s.stroke_count)
