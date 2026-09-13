# Planning pass. No paint: the mixtures as numbers, the value sheet against the
# bare ground, what every mass costs, and the composition as outlines.
print("palette, mixed to planned values:")
mixtures(verbose=True)
print("\nthree values:  rock %.2f / fog %.2f / glow %.2f"
      % (p.value_of("rock"), p.value_of("fog"), p.value_of("glow")))
print("split:", SPLIT, "=", sum(SPLIT.values()))
print(s.compare(PLAN))

plans = {
    "fog":       {"shape": fog(), "brush": "bristle", "size": 0.22, "density": 0.75, "direction": (4, 94)},
    "rock":      {"shape": rock(), "brush": "bristle", "size": 0.09, "density": 0.9, "direction": "axis"},
    "beam":      {"shape": beam(), "brush": "flat", "size": 0.09, "density": 1.0, "direction": "axis"},
    "tower":     {"shape": tower(), "brush": "flat", "size": 0.02, "density": 1.0, "direction": 90, "edge": "clean"},
    "lantern":   {"shape": lantern(), "brush": "flat", "size": 0.010, "density": 1.0, "direction": 90},
    "roof":      {"shape": roof(), "brush": "flat", "size": 0.010, "density": 1.0, "direction": "axis"},
}
total = 0
for name, plan in plans.items():
    c = s.cost(plan)
    total += c
    print(f"  cost {name:10s} {c:4d}")
print("costed masses total:", total)

outline = [dict(shape=fog_upper_grad(), label="fog_upper"), dict(shape=fog_mid_grad(), label="glow"),
           dict(shape=sea(), label="sea"), dict(shape=rock(), label="rock"),
           dict(shape=boulders(), label="boulders"), dict(shape=boulders2(), label="boulders2"),
           dict(shape=beam(), label="beam"), dict(shape=tower(), label="tower"),
           dict(shape=lit_face(), label="lit_face"),
           dict(shape=lantern(), label="lantern"), dict(shape=roof(), label="roof"),
           dict(shape=halo(), label="halo")]
for a, b in FLIGHTS:
    outline.append({"points": [a, b], "label": "flight"})
for x, y, r in POTS:
    outline.append(dict(shape=s.circle((x, y), r), label=None))
print(s.preview(outline, grid=True))
print(s.look(grid=True))
