# Planning pass. No paint: the mixtures as numbers, the value sheet against the
# bare ground, what every mass costs, and the composition as outlines.
print("ground value:", round(p.value_of(s.sample()), 2))
print("palette, mixed to planned values:")
mixtures(verbose=True)
print("split:", SPLIT, "=", sum(SPLIT.values()))
print(s.compare(PLAN))

plans = {
    "fog under": {"shape": fog(), "brush": "flat", "size": 0.20, "density": 0.8, "direction": (4, 94)},
    "beam":      {"shape": beam(), "brush": "bristle", "size": 0.05, "density": 1.0, "direction": "axis"},
    "rocks":     {"shape": rocks(), "brush": "flat", "size": 0.07, "density": 1.0, "direction": "axis", "edge": "clean"},
    "tower":     {"shape": tower(), "brush": "flat", "size": 0.02, "density": 1.0, "direction": 90, "edge": "clean"},
    "lit face":  {"shape": lit_face(), "brush": "flat", "size": 0.016, "density": 1.0, "direction": 90},
    "lantern":   {"shape": lantern(), "brush": "flat", "size": 0.02, "density": 1.0, "direction": 90},
    "roof":      {"shape": roof(), "brush": "flat", "size": 0.012, "density": 1.0, "direction": "axis"},
}
total = 0
for name, plan in plans.items():
    c = s.cost(plan)
    total += c
    print(f"  cost {name:10s} {c:4d}")
print("costed masses total:", total)

outline = [dict(shape=fog_upper(), label="fog_upper"), dict(shape=beam(), label="beam"),
           dict(shape=sea(), label="sea"), dict(shape=rocks(), label="rocks"),
           dict(shape=tower(), label="tower"), dict(shape=lit_face(), label="lit"),
           dict(shape=lantern(), label="lantern"), dict(shape=roof(), label="roof"),
           dict(shape=halo(), label="halo")]
for k in range(3):
    outline.append(dict(points=stair_arc(k), brush="flat", size=0.012, label=f"stair{k}"))
print(s.preview(outline, grid=True))
print(s.look(grid=True))
