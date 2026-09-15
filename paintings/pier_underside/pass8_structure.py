import random
rnd = random.Random(31)
p = s.palette
p["brace"] = p.at_value(p.mix("burnt_umber", "viridian", 0.45), 0.165)
p["brlit"] = p.desaturate(p.at_value(p.mix("yellow_ochre", "viridian", 0.45), 0.335), 0.45)
p["crust"] = p.desaturate(p.at_value(p.mix("titanium_white", "yellow_ochre", 0.40), 0.545), 0.42)
p["crustd"]= p.at_value(p.mix("burnt_umber", "viridian", 0.35), 0.175)

# cross-bracing: the diagonals a pier actually has, and the ones this picture needs
BRACE = [((0.175, 0.238), (0.404, 0.404), 0.020),
         ((0.404, 0.300), (0.176, 0.452), 0.017),
         ((0.445, 0.436), (0.611, 0.515), 0.012),
         ((0.862, 0.330), (0.641, 0.470), 0.014),
         ((0.912, 0.505), (0.999, 0.470), 0.011)]
plan = []
for (a, b, w) in BRACE:
    mid = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + 0.004)
    plan.append({"points": [a, mid, b], "brush": "flat", "color": "brace",
                 "size": w, "pressure": [0.55, 1.0, 0.8], "load": 0.9,
                 "load_falloff": 0.3, "note": "subject"})
    plan.append({"points": [(a[0], a[1] + w * 0.6), (mid[0], mid[1] + w * 0.6),
                            (b[0], b[1] + w * 0.6)],
                 "brush": "flat", "color": "brlit", "size": w * 0.34,
                 "pressure": [0.0, 0.7, 1.0], "load": 0.7,
                 "load_falloff": 0.7, "note": "subject"})

# the crust at each waterline: a starved brush breaking in from the silhouette
P, WL = piles(), {0: 0.815, 1: 0.760, 2: 0.726, 3: 0.700}
for i, q in enumerate(P):
    x0, x1, wl = q.bounds[0], q.bounds[2], WL[i]
    w = x1 - x0
    for k in range(6 - i):
        yy = wl - rnd.uniform(0.012, 0.085)
        side = rnd.choice((-1, 1))
        xs = (x0 if side < 0 else x1) - side * w * rnd.uniform(0.02, 0.22)
        ln = w * rnd.uniform(0.30, 0.72)
        plan.append({"points": [(xs, yy), (xs + side * ln, yy + rnd.uniform(-.004, .004))],
                     "brush": "round_hard",
                     "color": "crust" if rnd.random() < 0.55 else "crustd",
                     "size": w * rnd.uniform(0.10, 0.19), "pressure": [1.0, 0.25],
                     "tip_wobble": 0.75, "load": 0.30, "load_falloff": 0.95,
                     "opacity": rnd.uniform(0.45, 0.85), "note": "subject"})
print(s.cost_line(plan))
s.paint(plan)
s.look(path="out/11_structure.png")
