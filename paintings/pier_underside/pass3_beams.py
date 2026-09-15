p = s.palette
p["bounce"] = p.desaturate(p.mix("yellow_ochre", "viridian", 0.52), 0.62)
print("bounce", p.hex(p["bounce"]), "chroma", round(p.chroma_of(p["bounce"]), 3))

N = 6
VARY = [1.00, 0.78, 1.18, 0.86, 1.10, 0.72, 0.95]     # no two joists alike
plan = []
for i in range(N + 1):
    d = 1.0 - (1.0 - i / N) ** 2.0
    ly, ry = -0.02 + d * 0.740, -0.11 + d * 0.655
    if ry < -0.05:
        continue
    t, v = d, VARY[i]
    face = (0.055 - 0.025 * t) * v
    gap  = max(0.026, (0.034 - 0.011 * t) * v)
    sag  = 0.007 * (1 - t)
    p[f"js{i}"] = p.at_value("beam", 0.150 + 0.040 * t)
    p[f"jl{i}"] = p.at_value("bounce", 0.190 + 0.205 * t)

    mid = (ly + ry) / 2 + sag
    plan.append({"points": [(-0.03, ly - gap), (0.5, mid - gap), (1.03, ry - gap)],
                 "brush": "bristle", "color": f"js{i}", "size": gap,
                 "pressure": "even", "load": 0.85, "note": "subject"})
    # joist 2 is deliberately lost -- an edge that goes, so not every one is found
    if i == 2:
        continue
    plan.append({"points": [(-0.03, ly), (0.5, mid), (1.03, ry)],
                 "brush": "flat", "color": f"jl{i}", "size": face,
                 "pressure": [0.3, 1.0, 0.7, 0.55, 0.25], "load": 0.95,
                 "load_falloff": 0.2, "note": "subject"})

print(s.cost_line(plan))
s.paint(plan)
s.look(path="out/05_beams.png")
