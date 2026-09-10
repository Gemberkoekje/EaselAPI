p = s.palette

def to_value(base, target):
    other = "titanium_white" if p.value_of(base) < target else "burnt_umber"
    lo, hi = 0.0, 1.0
    for _ in range(28):
        mid = (lo + hi) / 2.0
        v = p.value_of(p.mix(base, other, mid))
        if (v < target) == (other == "titanium_white"):
            lo = mid
        else:
            hi = mid
    return p.mix(base, other, (lo + hi) / 2.0)

p["eyew2"] = to_value(p.desaturate(p.mix("yellow_ochre", "cerulean", 0.35), 0.6), 0.46)
p["teeth2"] = to_value(p.desaturate(p.mix("yellow_ochre", "titanium_white", 0.5), 0.4), 0.58)

plan = [
    dict(points=[(0.396, 0.242), (0.391, 0.312), (0.388, 0.376)], brush="flat",
         color="deep", size=0.028, pressure="even"),
    dict(points=[(0.390, 0.372), (0.401, 0.414), (0.408, 0.452)], brush="flat",
         color="deep", size=0.026, pressure="even"),
    dict(points=[(0.405, 0.448), (0.415, 0.492), (0.431, 0.532)], brush="flat",
         color="bgL", size=0.028, pressure="even"),

    dict(points=[(0.4475, 0.3045), (0.4665, 0.3025)], brush="round_hard",
         color="skin_d", size=0.014),
    dict(points=[(0.4585, 0.3025), (0.4655, 0.3035)], brush="round_hard",
         color="eyew2", size=0.006),
    dict(points=[(0.4520, 0.3055), (0.4535, 0.3055)], brush="round_hard",
         color="iris", size=0.0085),
    dict(points=[(0.4435, 0.2955), (0.4665, 0.2985)], brush="liner",
         color="hair_d", size=0.0045),

    dict(points=[(0.4135, 0.3505), (0.4085, 0.3705)], brush="round_hard",
         color="skin_l", size=0.005),
    dict(points=[(0.4295, 0.3995), (0.4335, 0.4025)], brush="round_hard",
         color="beard", size=0.006),
    dict(points=[(0.4185, 0.4135), (0.4435, 0.4065), (0.4635, 0.4165)],
         brush="bristle", color="beard", size=0.012),
    dict(points=[(0.4385, 0.4475), (0.4555, 0.4495)], brush="round_hard",
         color="iris", size=0.007),
    dict(points=[(0.4425, 0.4595), (0.4585, 0.4615)], brush="round_hard",
         color="lip", size=0.005),
    dict(points=[(0.4305, 0.4765), (0.4445, 0.5165), (0.4685, 0.5445)],
         brush="bristle", color="beard", size=0.018),
]
print(s.rehearse(plan, reference="ref.jpg", region=span("D3", "D4")))
