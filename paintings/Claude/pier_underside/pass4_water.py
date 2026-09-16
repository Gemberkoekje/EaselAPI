p = s.palette
p["water_deep"] = p.at_value(p.mix("viridian", "burnt_umber", 0.58), 0.170)
p["water_top"]  = p.desaturate(p.at_value(p.mix("viridian", "cerulean", 0.40), 0.340), 0.45)
p["refl"]       = p.desaturate(p.at_value(p.mix("yellow_ochre", "viridian", 0.40), 0.50), 0.35)
p["refl_hi"]    = p.desaturate(p.at_value(p.mix("yellow_ochre", "titanium_white", 0.5), 0.66), 0.30)

# the field first: lit where it lies under the slot, dark in the foreground
s.scumble(water(), "water_top", "water_deep", 9, direction="horizontal", opacity=0.42)
s.look(path="out/06a_water_field.png")

# then the slot's reflection, broken, and only where the slot actually is
REFL = [(0.36, 0.716, 0.62, 0.702, 0.020),
        (0.55, 0.735, 0.88, 0.716, 0.026),
        (0.70, 0.700, 1.02, 0.686, 0.016),
        (0.44, 0.760, 0.74, 0.745, 0.014),
        (0.82, 0.756, 1.02, 0.742, 0.020)]
plan = []
for x0, y0, x1, y1, w in REFL:
    plan.append({"points": [(x0, y0), ((x0 + x1) / 2, (y0 + y1) / 2 + 0.004), (x1, y1)],
                 "brush": "bristle", "color": "refl", "size": w,
                 "pressure": [0.2, 1.0, 0.55, 0.9, 0.15], "load": 0.5,
                 "load_falloff": 0.9})
print(s.cost_line(plan))
s.paint(plan)
s.look(path="out/06_water.png")
