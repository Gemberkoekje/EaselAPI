# Planning pass. No paint: the mixtures as numbers, the value plan against the bare
# ground, and what every mass would charge before any of it is spent.
print("palette, mixed to planned values:")
mixtures(verbose=True)
print("\nthree values:  dark %.2f / mid %.2f / light %.2f"
      % (p.value_of(p["facade"]), p.value_of(p["wet_mid"]), p.value_of(p["interior"])))
print("ground reads   %.2f" % p.value_of(s.sample()))
print(s.compare(PLAN))

plans = {
    "sky":        {"shape": sky(), "brush": "flat", "size": 0.20,
                   "density": 0.62, "direction": (12, 100)},
    "facade":     {"shape": facade(), "brush": "bristle", "size": 0.155,
                   "density": 0.72, "direction": (8, 96)},
    "sidewalk":   {"shape": sidewalk(), "brush": "flat", "size": 0.055,
                   "density": 0.9, "direction": "axis"},
    "road":       {"shape": road(), "brush": "bristle", "size": 0.14,
                   "density": 0.8, "direction": (6, 84)},
    "win back":   {"shape": window_open().inset(0.012), "brush": "flat",
                   "size": 0.024, "density": 1.0, "solid": True, "direction": "axis"},
    "win top":    {"shape": polygon([(0.180,0.344),(0.714,0.342),(0.712,0.436),(0.178,0.440)]),
                   "brush": "flat", "size": 0.020, "density": 1.0, "solid": True},
    "door back":  {"shape": door_open().inset(0.008), "brush": "flat",
                   "size": 0.018, "density": 1.0, "solid": True, "direction": "axis"},
    "machines":   {"shape": machine_band(), "brush": "flat", "size": 0.020,
                   "density": 1.0, "solid": True, "direction": "axis"},
    "figure":     {"shape": figure(), "brush": "flat", "size": 0.012,
                   "density": 1.0, "solid": True, "direction": "axis", "edge": "clean"},
    "reflection": {"shape": reflection(), "brush": "bristle", "size": 0.085,
                   "density": 0.85, "direction": (88, 70)},
    "door refl":  {"shape": door_reflection(), "brush": "bristle", "size": 0.05,
                   "density": 0.85, "direction": (86, 72)},
}
total = 0
for name, plan in plans.items():
    c = s.cost(plan)
    total += c
    print(f"  cost {name:11s} {c:4d}")
print("costed masses total:", total)
