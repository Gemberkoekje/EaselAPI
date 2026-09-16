import math, random
rnd = random.Random(9021)
p = s.palette
p["hot"]  = p.desaturate(p.at_value(p.mix("lemon_yellow", "titanium_white", 0.45), 0.815), 0.22)
p["warm"] = p.desaturate(p.at_value(p.mix("yellow_ochre", "titanium_white", 0.50), 0.700), 0.25)
p["rim"]  = p.desaturate(p.at_value(p.mix("yellow_ochre", "titanium_white", 0.42), 0.615), 0.32)

plan = []
# caustics tighten where the light actually reaches: the last two joists
for i in (5, 6):
    d = 1.0 - (1.0 - i / 6) ** 2.0
    ly, ry = -0.02 + d * 0.740, -0.11 + d * 0.655
    face = 0.055 - 0.025 * d
    for _ in range(7):
        x = rnd.uniform(0.50, 0.99)
        near = max(0.0, 1.0 - abs(x - 0.82) * 1.5)
        if near < 0.2:
            continue
        ln = rnd.uniform(0.05, 0.15) * (0.6 + near)
        amp, ph = face * rnd.uniform(0.15, 0.33), rnd.uniform(0, 6.3)
        y0 = ly + (ry - ly) * x + rnd.uniform(-0.30, 0.20) * face
        pts = [(x + ln * j / 6,
                y0 + (ry - ly) * ln * j / 6 + amp * math.sin(ph + j * 1.55))
               for j in range(7)]
        plan.append({"points": pts, "brush": "liner",
                     "color": "hot" if near > 0.65 else "warm",
                     "size": 0.0035 + 0.004 * near,
                     "pressure": [0.0, 1.0, 0.3, 0.85, 0.0], "load": 0.75,
                     "load_falloff": 0.85, "opacity": 0.35 + 0.45 * near,
                     "note": "subject"})

# the water directly under the slot takes the light hardest
for _ in range(9):
    x = rnd.uniform(0.46, 0.99)
    y = rnd.uniform(0.690, 0.735)
    ln = rnd.uniform(0.045, 0.16)
    plan.append({"points": [(x, y), (x + ln * 0.5, y + rnd.uniform(-.003, .003)),
                            (x + ln, y + rnd.uniform(-.004, .004))],
                 "brush": "bristle", "color": "hot" if rnd.random() < 0.4 else "warm",
                 "size": rnd.uniform(0.008, 0.017), "pressure": "even",
                 "load": 0.35, "load_falloff": 0.95,
                 "opacity": rnd.uniform(0.35, 0.72)})

# the pile standing in the light takes a rim down its lit side
q = piles()[1]
x0, x1 = q.bounds[0], q.bounds[2]
plan.append({"points": [(x0 + 0.004, 0.44), (x0 + 0.002, 0.60), (x0 + 0.005, 0.735)],
             "brush": "liner", "color": "rim", "size": 0.0055,
             "pressure": [0.0, 0.6, 1.0], "load": 0.8, "load_falloff": 0.55,
             "opacity": 0.6, "note": "subject"})
print(s.cost_line(plan))
s.paint(plan)
s.look(path="out/14_focal.png")
