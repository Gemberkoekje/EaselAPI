import random
rnd = random.Random(88)
p = s.palette
p["fg"]    = p.at_value(p.mix("viridian", "burnt_umber", 0.62), 0.145)
p["fgtop"] = p.at_value(p.mix("viridian", "burnt_umber", 0.58), 0.225)
p["glint"] = p.desaturate(p.at_value(p.mix("yellow_ochre", "titanium_white", 0.5), 0.70), 0.28)

# the foreground deepens as a graded field, not a bar with a lid on it
s.scumble(span("A7", "H8"), "fgtop", "fg", 7, direction="horizontal", opacity=0.34)

plan = []
for n in range(30):
    y = rnd.uniform(0.695, 0.995)
    depth = (y - 0.695) / 0.30                      # 0 far, 1 near
    if rnd.random() < depth * 0.6:
        continue
    x = rnd.uniform(-0.03, 0.94)
    ln = rnd.uniform(0.07, 0.27) * (1.0 - 0.3 * depth)
    lit = max(0.0, 1.0 - abs(x + ln / 2 - 0.76) * 1.25) * (1.0 - depth * 0.85)
    # a ripple is only ever a step off the water it lies on, and that water darkens
    p[f"r{n}"] = p.at_value("fgtop", max(0.16, 0.395 - 0.20 * depth + 0.05 * lit))
    plan.append({"points": [(x, y), (x + ln * 0.5, y + rnd.uniform(-.004, .004)),
                            (x + ln, y + rnd.uniform(-.005, .005))],
                 "brush": "bristle",
                 "color": "glint" if lit > 0.50 else f"r{n}",
                 "size": rnd.uniform(0.011, 0.024) * (1.0 + 0.5 * depth),
                 "pressure": "even", "load": 0.35 + 0.35 * lit,
                 "load_falloff": 0.92, "opacity": 0.24 + 0.42 * lit})
print(s.cost_line(plan))
s.paint(plan)
s.look(path="out/10_water2.png")
