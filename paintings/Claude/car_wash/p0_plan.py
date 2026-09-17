# Planning pass. No paint: the mixtures as numbers, the value plan measured against
# the bare ground, and what every mass costs before any of it is spent.
print("palette, mixed to planned values:")
mixtures(verbose=True)
print("\nthree values:  dark %.2f / mid %.2f / light %.2f"
      % (p.value_of(p["frame"]), p.value_of(p["haze"]), p.value_of(p["cyan_hi"])))
print(s.compare(PLAN))

plans = {
    "tunnel":    {"shape": Region(-0.04, -0.05, 1.04, 0.885), "brush": "bristle",
                  "size": 0.16, "density": 0.65, "direction": (14, 100)},
    "arch":      {"shape": archband(), "brush": "bristle", "size": 0.11,
                  "density": 0.75, "direction": (160, 28)},
    "arch core": {"shape": archcore(), "brush": "bristle", "size": 0.06,
                  "density": 0.55, "direction": (148, 40)},
    "bloom":     {"shape": glow(), "size": 0.05},
    "brush":     {"shape": brushmass(), "brush": "bristle", "size": 0.085,
                  "density": 0.80, "direction": (82, 103)},
    "dash":      {"shape": dash(), "brush": "flat", "size": 0.060,
                  "density": 1.0, "direction": "axis", "edge": "clean"},
    "binnacle":  {"shape": binnacle(), "brush": "flat", "size": 0.052,
                  "density": 1.0, "direction": "axis", "edge": "clean"},
    "pillar L":  {"shape": pillar_l(), "brush": "flat", "size": 0.030,
                  "density": 1.0, "direction": "axis", "edge": "clean"},
    "pillar R":  {"shape": pillar_r(), "brush": "flat", "size": 0.024,
                  "density": 1.0, "direction": "axis", "edge": "clean"},
    "mirror":    {"shape": mirror(), "brush": "flat", "size": 0.018,
                  "density": 1.0, "direction": "axis", "edge": "clean"},
}
total = 0
for name, plan in plans.items():
    c = s.cost(plan)
    total += c
    print(f"  cost {name:10s} {c:4d}")
print("costed masses total:", total)
