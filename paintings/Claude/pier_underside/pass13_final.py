import math, random
rnd = random.Random(4242)
p = s.palette
p["spark"] = p.at_value(p.mix("titanium_white", "lemon_yellow", 0.18), 0.935)
p["farlit"] = p.desaturate(p.at_value(p.mix("yellow_ochre", "titanium_white", 0.60), 0.865), 0.20)
p["carry"] = p.desaturate(p.at_value(p.mix("yellow_ochre", "titanium_white", 0.45), 0.535), 0.35)

plan = []
# the far water in the slot, which is the brightest thing and should say so
for x, y, ln, w in ((0.50, 0.6565, 0.20, 0.0085), (0.72, 0.6335, 0.24, 0.0075),
                    (0.86, 0.6125, 0.15, 0.0065), (0.60, 0.6455, 0.13, 0.0055)):
    plan.append({"points": [(x, y), (x + ln * 0.5, y - 0.0018), (x + ln, y + 0.001)],
                 "brush": "flat", "color": "farlit", "size": w, "pressure": [0.2, 1.0, 0.3],
                 "load": 0.95, "load_falloff": 0.35, "opacity": 0.62})

# sparkles: long enough to be a mark rather than the tip's own disc
for x, y, ln in ((0.690, 0.7085, 0.055), (0.820, 0.7165, 0.044), (0.606, 0.7015, 0.038),
                 (0.906, 0.7245, 0.036), (0.762, 0.6955, 0.030), (0.526, 0.7135, 0.027)):
    plan.append({"points": [(x, y), (x + ln * 0.55, y + 0.0012), (x + ln, y - 0.0008)],
                 "brush": "liner", "color": "spark", "size": 0.0042,
                 "pressure": [0.0, 1.0, 0.15], "load": 0.95, "load_falloff": 0.5,
                 "opacity": 0.92})

# carry a little of that light back along the joists, so it does not all pool right
for i in (4, 5, 6):
    d = 1.0 - (1.0 - i / 6) ** 2.0
    ly, ry = -0.02 + d * 0.740, -0.11 + d * 0.655
    face = 0.055 - 0.025 * d
    for _ in range(3):
        x = rnd.uniform(0.17, 0.52)
        ln = rnd.uniform(0.05, 0.13)
        y0 = ly + (ry - ly) * x + rnd.uniform(-0.25, 0.18) * face
        pts = [(x + ln * j / 5, y0 + (ry - ly) * ln * j / 5
                + face * 0.20 * math.sin(j * 1.7 + i)) for j in range(6)]
        plan.append({"points": pts, "brush": "liner", "color": "carry",
                     "size": 0.0035, "pressure": [0.0, 0.9, 0.2, 0.7, 0.0],
                     "load": 0.7, "load_falloff": 0.9,
                     "opacity": rnd.uniform(0.22, 0.42), "note": "subject"})
print(s.cost_line(plan))
s.paint(plan)
s.look(path="out/16_final.png")
