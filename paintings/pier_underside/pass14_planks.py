import random
rnd = random.Random(1717)
p = s.palette
p["plk_d"] = p.at_value(p.mix("burnt_umber", "viridian", 0.38), 0.185)
p["plk_l"] = p.desaturate(p.at_value(p.mix("yellow_ochre", "viridian", 0.40), 0.272), 0.50)

# the decking above the joists runs the other way: barely there, and crossing
plan = []
for k in range(13):
    y0 = -0.04 + k * 0.052 + rnd.uniform(-0.012, 0.012)
    frac = rnd.uniform(0.35, 0.78)                  # none of them crosses the whole span
    x0 = rnd.uniform(-0.03, 0.30)
    x1 = x0 + frac * (VP[0] - x0)
    y1 = y0 + (VP[1] - y0) * frac * rnd.uniform(0.85, 1.0)
    plan.append({"points": [(x0, y0), ((x0 + x1) / 2, (y0 + y1) / 2 + 0.004), (x1, y1)],
                 "brush": "bristle",
                 "color": "plk_l" if rnd.random() < 0.42 else "plk_d",
                 "size": rnd.uniform(0.013, 0.027), "pressure": [0.25, 1.0, 0.15],
                 "load": 0.42, "load_falloff": 0.9,
                 "opacity": rnd.uniform(0.16, 0.34), "note": "subject"})
print(s.cost_line(plan))
s.paint(plan)
s.look(path="out/18_planks.png")
