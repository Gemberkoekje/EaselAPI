import math, random
rnd = random.Random(704)
p = s.palette
p["cst"]  = p.desaturate(p.at_value(p.mix("yellow_ochre", "titanium_white", 0.55), 0.60), 0.25)
p["cst2"] = p.desaturate(p.at_value(p.mix("lemon_yellow", "titanium_white", 0.40), 0.74), 0.30)

N = 6
plan = []
for i in range(2, N + 1):
    d = 1.0 - (1.0 - i / N) ** 2.0
    ly, ry = -0.02 + d * 0.740, -0.11 + d * 0.655
    face = 0.055 - 0.025 * d
    for _ in range(7):
        x = rnd.uniform(0.04, 0.99)
        near = max(0.0, 1.0 - (abs(x - 0.80) * 1.05 + (1.0 - d) * 0.85))
        if near < 0.14:
            continue
        ln = rnd.uniform(0.07, 0.20) * (0.55 + near)
        amp = face * rnd.uniform(0.13, 0.30)
        ph, k = rnd.uniform(0, 6.3), rnd.uniform(2.2, 4.0)
        y0 = ly + (ry - ly) * x + rnd.uniform(-0.28, 0.24) * face
        pts = []
        for j in range(7):                       # a wavy filament, not a dot
            u = j / 6
            px = x + ln * u
            pts.append((px, y0 + (ry - ly) * ln * u + amp * math.sin(ph + k * u * 3.1)))
        plan.append({"points": pts, "brush": "liner",
                     "color": "cst2" if near > 0.60 and rnd.random() < 0.4 else "cst",
                     "size": (0.0035 + 0.0045 * near) * rnd.uniform(0.7, 1.35),
                     "pressure": [0.0, 0.9, 0.4, 1.0, 0.2], "load": 0.7,
                     "load_falloff": 0.85, "opacity": 0.28 + 0.42 * near,
                     "note": "subject"})
print(s.cost_line(plan))
s.paint(plan)
s.look(path="out/09_caustics.png")
