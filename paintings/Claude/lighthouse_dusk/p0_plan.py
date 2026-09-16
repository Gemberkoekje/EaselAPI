# Planning pass. No paint: the mixtures as numbers, the value sheet against the
# bare ground, what every mass costs, and the composition as outlines.
print("palette, mixed to planned values:")
mixtures(verbose=True)
print("\nthree values:  rock %.2f / sea_far %.2f / glow %.2f"
      % (p.value_of("rock"), p.value_of("sea_far"), p.value_of("glow")))
print("split:", SPLIT, "=", sum(SPLIT.values()))
print(s.compare(PLAN))

plans = {
    "sky under":  {"shape": sky(), "brush": "bristle", "size": 0.20, "density": 0.7, "direction": (5, 95)},
    "headland":   {"shape": headland(), "brush": "bristle", "size": 0.09, "density": 0.9, "direction": ("axis", 70)},
    "boulders":   {"shape": boulders(), "brush": "flat", "size": 0.03, "density": 1.0, "direction": "axis"},
    "tower":      {"shape": tower(), "brush": "flat", "size": 0.02, "density": 1.0, "direction": 90, "edge": "clean"},
    "band":       {"shape": band(), "brush": "flat", "size": 0.012, "density": 1.0, "direction": 90},
    "lantern":    {"shape": lantern(), "brush": "flat", "size": 0.012, "density": 1.0, "direction": 90},
    "roof":       {"shape": roof(), "brush": "flat", "size": 0.010, "density": 1.0, "direction": "axis"},
}
total = 0
for name, plan in plans.items():
    c = s.cost(plan)
    total += c
    print(f"  cost {name:10s} {c:4d}")
print("costed masses total:", total, "(scumbles are n each: sky 8+8+7, sea 10, tower form 6, halo 6)")

outline = [dict(shape=sky_upper(), label="sky_upper"), dict(shape=glow_patch(), label="glow"),
           dict(shape=sea(), label="sea"), dict(shape=headland(), label="headland"),
           dict(shape=boulders(), label="boulders"), dict(shape=tower(), label="tower"),
           dict(shape=band(), label="band"), dict(shape=lantern(), label="lantern"),
           dict(shape=roof(), label="roof"), dict(shape=halo(), label="halo"),
           dict(shape=s.circle(MOON, 0.034), label="moon")]
print(s.preview(outline, grid=True))
print(s.look(grid=True))
