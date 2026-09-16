p = s.palette
p["pd"]   = p.at_value(p.mix("burnt_umber", "viridian", 0.42), 0.155)
p["pf"]   = p.desaturate(p.at_value(p.mix("yellow_ochre", "viridian", 0.45), 0.455), 0.42)
p["pwet"] = p.at_value(p.mix("burnt_umber", "viridian", 0.52), 0.145)
p["pgrn"] = p.at_value(p.mix("viridian", "burnt_umber", 0.30), 0.255)

P = piles()
ORDER = [3, 2, 1, 0]
SPEC = {0: (+1, "ragged", 0.815), 1: (-1, "hard", 0.760),
        2: (+1, "ragged", 0.726), 3: (-1, "hard", 0.700)}

shafts = []
for i in ORDER:
    q, (side, edge, wl) = P[i], SPEC[i]
    w = q.bounds[2] - q.bounds[0]
    shafts.append({"region": q, "brush": "flat", "color": "pd", "direction": "axis",
                   "density": 1.0, "solid": True, "size": max(0.034, w * 0.78),
                   "edge": edge, "note": "subject"})
print(s.cost_line(shafts))
s.paint(shafts)

marks = []
for i in ORDER:
    q, (side, edge, wl) = P[i], SPEC[i]
    x0, x1, top = q.bounds[0], q.bounds[2], q.bounds[1]
    w = x1 - x0
    cx = (x0 + x1) / 2 + side * w * 0.31
    marks.append({"points": [(cx, top + 0.10), (cx + side * 0.003, (top + wl) * 0.5),
                             (cx - side * 0.002, wl - 0.04)],
                  "brush": "flat", "color": "pf", "size": w * 0.15,
                  "pressure": [0.0, 0.4, 1.0], "load": 0.85,
                  "load_falloff": 0.80, "note": "subject"})
    # weathering: two broken streaks, not thirty
    for k, off in enumerate((-0.22, 0.12)):
        marks.append({"points": [(x0 + w * (0.5 + off), top + 0.16 + k * 0.05),
                                 (x0 + w * (0.5 + off * 0.7), wl - 0.09)],
                      "brush": "bristle", "color": "pgrn", "size": w * 0.16,
                      "pressure": "even", "load": 0.30, "load_falloff": 0.95,
                      "note": "subject"})
    # the weed line where it meets the water, and a broken reflection under it
    marks.append({"points": [(x0 + w * 0.06, wl - 0.016), (x1 - w * 0.06, wl - 0.008)],
                  "brush": "bristle", "color": "pwet", "size": w * 0.34,
                  "pressure": "even", "load": 0.8, "note": "subject"})
    marks.append({"points": [(x0 + w * 0.36, wl + 0.004), (x0 + w * 0.46, wl + 0.062)],
                  "brush": "round_hard", "color": "pwet", "size": w * 0.30,
                  "pressure": [1.0, 0.15], "load": 0.5, "load_falloff": 0.95,
                  "tip_wobble": 0.6, "note": "subject"})
s.paint(marks)
s.look(path="out/07_piles.png")
