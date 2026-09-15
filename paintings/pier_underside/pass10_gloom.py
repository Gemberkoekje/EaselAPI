import random
rnd = random.Random(515)
p = s.palette
p["ghost"]  = p.at_value(p.mix("burnt_umber", "viridian", 0.40), 0.185)
p["ghostl"] = p.desaturate(p.at_value(p.mix("yellow_ochre", "viridian", 0.50), 0.268), 0.50)
p["fix"]    = p.at_value(p.mix("burnt_umber", "viridian", 0.45), 0.170)
p["crustw"] = p.desaturate(p.at_value(p.mix("titanium_white", "yellow_ochre", 0.45), 0.415), 0.45)

plan = []
# bury the crust dashes that read as painted stripes, in the shape of the passage
for yy in (0.756, 0.772, 0.788, 0.742):
    plan.append({"points": [(0.005, yy + 0.004), (0.06, yy), (0.115, yy + 0.005)],
                 "brush": "bristle", "color": "fix", "size": 0.030,
                 "pressure": "even", "load": 1.0, "load_falloff": 0.0, "opacity": 0.78})

# two pilings further back, all but lost in the murk
for cx, top, bot, w in ((0.255, 0.075, 0.742, 0.040), (0.318, 0.215, 0.726, 0.026)):
    q = ribbon([(cx, top), (cx - 0.004, (top + bot) / 2), (cx + 0.003, bot)], w, w * 0.84)
    plan.append({"region": q, "brush": "bristle", "color": "ghost", "direction": "axis",
                 "density": 0.88, "size": w * 0.70, "edge": "ragged", "opacity": 0.72})
    plan.append({"points": [(cx + w * 0.30, top + 0.09), (cx + w * 0.32, bot - 0.10)],
                 "brush": "flat", "color": "ghostl", "size": w * 0.20,
                 "pressure": [0.0, 0.5, 1.0], "load": 0.6, "load_falloff": 0.7,
                 "opacity": 0.55})

# the crust again, worked in from the silhouette with a starved brush
for cx, w, wl in ((0.145, 0.105, 0.815), (0.255, 0.040, 0.742)):
    for k in range(7):
        yy = wl - rnd.uniform(0.010, 0.095)
        side = rnd.choice((-1, 1))
        xs = cx + side * w * rnd.uniform(0.30, 0.52)
        ln = w * rnd.uniform(0.18, 0.46)
        plan.append({"points": [(xs, yy), (xs - side * ln, yy + rnd.uniform(-.005, .005))],
                     "brush": "round_hard", "color": "crustw",
                     "size": w * rnd.uniform(0.09, 0.17), "tip_wobble": 0.8,
                     "pressure": [1.0, 0.2], "load": 0.26, "load_falloff": 0.96,
                     "opacity": rnd.uniform(0.35, 0.62), "note": "subject"})
print(s.cost_line(plan))
s.paint(plan)
s.look(path="out/13_gloom.png")
