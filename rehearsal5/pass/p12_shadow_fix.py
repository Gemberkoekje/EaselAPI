REF = "C:/temp/Level1.jpg"
p = s.palette

def dv(base, target, dark):
    lo, hi = 0.0, 1.0
    for _ in range(24):
        mid = (lo + hi) / 2
        if p.value_of(p.mix(base, dark, mid)) > target:
            lo = mid
        else:
            hi = mid
    return p.mix(base, dark, (lo + hi) / 2)

warm_dark = p.mix("ultramarine", "burnt_umber", 0.72)
wood = p.desaturate(p.mix("burnt_umber", "yellow_ochre", 0.38), 0.22)
p["shad_ring"] = dv(wood, 0.345, warm_dark)
print("shad_ring", p.hex(p["shad_ring"]), round(p.value_of(p["shad_ring"]), 3))

s.dry()

# --- kill the hard bar across the shadow ---------------------------------
for a, b, size, ang in [((0.335, 0.688), (0.578, 0.676), 0.056, 0),
                        ((0.575, 0.712), (0.332, 0.722), 0.056, 0),
                        ((0.345, 0.748), (0.560, 0.740), 0.050, 0),
                        ((0.400, 0.665), (0.560, 0.658), 0.046, 0)]:
    s.stroke([a, b], "flat", "shad_core", size=size, pressure="even",
             load=1.0, load_falloff=0.0, note="kill bar")

# --- put the lit wood back where the botched ring was --------------------
for a, b, size, col in [((0.585, 0.505), (0.760, 0.500), 0.060, "wood_light"),
                        ((0.755, 0.548), (0.585, 0.553), 0.060, "wood_light"),
                        ((0.590, 0.598), (0.755, 0.592), 0.058, "wood_light"),
                        ((0.750, 0.634), (0.592, 0.640), 0.050, "wood_light")]:
    s.stroke([a, b], "flat", col, size=size, pressure="even",
             load=1.0, load_falloff=0.0, note="erase ring")
print("repairs", s.stroke_count)

# --- soften the shadow's outline by straddling it dry --------------------
for pts, size in [([(0.322, 0.630), (0.308, 0.700), (0.330, 0.766)], 0.045),
                  ([(0.350, 0.792), (0.420, 0.842), (0.496, 0.830)], 0.045),
                  ([(0.548, 0.792), (0.590, 0.718), (0.612, 0.646)], 0.040)]:
    s.stroke(pts, "bristle", "shad_pen", size=size, load=0.5, pressure="swell",
             note="soften shadow edge")
print("soften", s.stroke_count)

# --- the handle's cast shadow, rehearsed not painted ---------------------
ring = [{"points": [(0.612, 0.552), (0.640, 0.527), (0.676, 0.524), (0.706, 0.546)],
         "brush": "round_hard", "color": "shad_ring", "size": 0.020, "pressure": "swell"},
        {"points": [(0.706, 0.546), (0.718, 0.571), (0.704, 0.594)],
         "brush": "round_hard", "color": "shad_ring", "size": 0.017, "pressure": "even"},
        {"points": [(0.700, 0.596), (0.666, 0.608), (0.632, 0.598), (0.616, 0.578)],
         "brush": "round_hard", "color": "shad_ring", "size": 0.019, "pressure": "swell"}]
print("ring A round_hard:", s.rehearse(ring, reference=REF, region=span("E5", "G6")))
fat = [dict(d, size=d["size"] * 1.7, brush="bristle") for d in ring]
print("ring B bristle fat:", s.rehearse(fat, reference=REF, region=span("E5", "G6")))

print(s.look(region=span("C5", "G7"), reference=REF))
print(s.look(reference=REF))
