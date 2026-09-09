# Pass 14a — rehearse the mug's light mass before paying for it.
# Run: python -m easel run painting.easel c14a_rehearse.py
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


cool = D(M("ultramarine", "burnt_umber", 0.30), 0.35)
p["mug_hi"] = at_value(M("cerulean", "titanium_white", 0.94), 0.88)
p["mug_body"] = at_value(cool, 0.78)
p["mug_mid"] = at_value(cool, 0.62)
p["mug_dim"] = at_value(cool, 0.42)
p["mug_dark"] = at_value(cool, 0.30)
for k in ("mug_hi", "mug_body", "mug_mid", "mug_dim", "mug_dark"):
    print(f"{k:9s} {p.hex(p[k])} {p.value_of(p[k]):.3f}")


def curve(knots):
    def at(x):
        for (x0, y0), (x1, y1) in zip(knots, knots[1:]):
            if x0 <= x <= x1:
                return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
        return knots[-1][1] if x > knots[-1][0] else knots[0][1]
    return at


TOP = curve([(0.312, 0.192), (0.335, 0.148), (0.380, 0.120), (0.440, 0.105),
             (0.500, 0.103), (0.558, 0.117), (0.602, 0.145), (0.630, 0.183),
             (0.636, 0.222)])
BOT = curve([(0.312, 0.192), (0.330, 0.353), (0.350, 0.531), (0.360, 0.620),
             (0.377, 0.638), (0.410, 0.658), (0.456, 0.669), (0.505, 0.663),
             (0.542, 0.644), (0.570, 0.518), (0.600, 0.383), (0.636, 0.222)])

plan = []
x = 0.316
while x < 0.638:
    t, b = TOP(x), BOT(x)
    if b - t >= 0.01:
        if x < 0.352:
            col = "mug_dark"
        elif x < 0.395:
            col = "mug_dim"
        elif x < 0.455:
            col = "mug_mid"
        elif x < 0.560:
            col = "mug_body"
        else:
            col = "mug_hi"
        plan.append({"points": [(x, t - 0.004), (x, b + 0.004)], "brush": "flat",
                     "color": col, "load": 1.0, "pressure": "even",
                     "size": 0.030 if (x < 0.36 or x > 0.60) else 0.044})
    x += 0.022
print("planned strokes:", len(plan))
print(s.rehearse(plan, reference=REF, region=span("C1", "G7")))
print("strokes (unchanged):", s.stroke_count)
