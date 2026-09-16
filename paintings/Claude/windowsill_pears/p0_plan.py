# Planning pass: palette to numbers, costs of the big masses, no paint spent.
p = s.palette

def to_value(base, target, name=""):
    """Return `base` pushed to read `target` in greyscale: white up, umber/ultramarine down."""
    dark = p.mix("ultramarine", "burnt_umber", 0.55)
    v = p.value_of(base)
    if abs(v - target) < 0.005:
        return base
    going_up = v < target
    other = "titanium_white" if going_up else dark
    a, b = 0.0, 1.0
    for _ in range(24):
        mid = (a + b) / 2
        mv = p.value_of(p.mix(base, other, mid))
        if (mv < target) == going_up:
            a = mid
        else:
            b = mid
    return p.mix(base, other, (a + b) / 2)

targets = {
    "window":      (p.desaturate("cerulean", 0.45),                              0.82),
    "wall":        (p.mix("yellow_ochre", "burnt_umber", 0.30),                  0.48),
    "wall_low":    (p.mix("burnt_umber", "ultramarine", 0.30),                   0.30),
    "curtain":     (p.mix("yellow_ochre", "titanium_white", 0.40),               0.70),
    "curtain_fold":(p.mix("yellow_ochre", "burnt_umber", 0.30),                  0.52),
    "sill":        (p.mix("yellow_ochre", "burnt_sienna", 0.20),                 0.62),
    "sill_shadow": (p.mix(p.mix("burnt_umber", "ultramarine", 0.40), "yellow_ochre", 0.25), 0.30),
    "dark":        (p.mix("ultramarine", "burnt_umber", 0.55),                   0.15),
    "mug":         (p.desaturate(p.mix("cerulean", "ultramarine", 0.45), 0.35),  0.36),
    "mug_in":      (p.mix("ultramarine", "burnt_umber", 0.40),                   0.20),
    "mug_lit":     (p.desaturate(p.mix("cerulean", "ultramarine", 0.30), 0.30),  0.58),
    "pear_shadow": (p.mix(p.mix("yellow_ochre", "viridian", 0.35), "burnt_umber", 0.35), 0.28),
    "pear_mid":    (p.mix("yellow_ochre", "viridian", 0.22),                     0.44),
    "pear_lit":    (p.mix("cadmium_yellow", "yellow_ochre", 0.45),               0.66),
    "pear_hi":     (p.mix("cadmium_yellow", "yellow_ochre", 0.30),               0.86),
}
for name, (base, target) in targets.items():
    p[name] = to_value(base, target, name)
    print(f"{name:13s} {p.hex(p[name])}  value {p.value_of(p[name]):.2f}  (target {target:.2f})")

print("ground value:", round(p.value_of(p.mix("yellow_ochre","burnt_umber",0.3)),2), "(wall base, for reference)")

# Cost the big masses before spending anything.
plans = {
    "window pane":  {"shape": Region(0.14, 0.00, 0.72, 0.60), "brush": "flat", "size": 0.16, "density": 0.9, "direction": 12},
    "wall left":    {"shape": Region(0.00, 0.00, 0.17, 0.62), "brush": "flat", "size": 0.10, "density": 0.9, "direction": 84},
    "wall right":   {"shape": Region(0.68, 0.00, 1.00, 0.62), "brush": "flat", "size": 0.12, "density": 0.9, "direction": 84},
    "curtain":      {"shape": polygon([(0.74,-0.02),(1.02,-0.02),(1.02,0.66),(0.80,0.68),(0.72,0.66)]), "brush": "bristle", "size": 0.09, "density": 0.9, "direction": ("axis", 90)},
    "sill":         {"shape": Region(-0.02, 0.60, 1.02, 0.78), "brush": "flat", "size": 0.10, "density": 1.0, "direction": 4},
    "wall low":     {"shape": Region(-0.02, 0.78, 1.02, 1.02), "brush": "flat", "size": 0.14, "density": 0.9, "direction": (8, 98)},
    "mug body":     {"shape": polygon([(0.55,0.41),(0.68,0.41),(0.67,0.67),(0.56,0.67)]), "brush": "flat", "size": 0.03, "density": 1.0, "direction": 90},
    "pear 1":       {"shape": blob((0.33, 0.58), 0.085, wobble=0.2, seed=3), "brush": "bristle", "size": 0.03, "density": 1.0, "direction": ("axis", 90)},
    "pear 2":       {"shape": blob((0.47, 0.60), 0.075, wobble=0.2, seed=4), "brush": "bristle", "size": 0.03, "density": 1.0, "direction": ("axis", 90)},
    "pear 3 lying": {"shape": ellipse((0.40, 0.715), 0.10, 0.052), "brush": "bristle", "size": 0.03, "density": 1.0, "direction": 90},
}
total = 0
for name, plan in plans.items():
    c = s.cost(plan)
    total += c
    print(f"cost {name:13s} {c:4d}")
print("cost total of the listed masses:", total)
print("stroke_count now:", s.stroke_count)
print(s.look(grid=True))
