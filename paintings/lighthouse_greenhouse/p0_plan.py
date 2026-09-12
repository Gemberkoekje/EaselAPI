# Planning pass. No paint: the mixtures as numbers, the value sheet against the
# bare ground, what every mass would cost, and the composition as outlines.
print("palette, mixed to planned values:")
mixtures(verbose=True)
print("\nthree carrying values:  rock %.2f / tower %.2f / fog %.2f   beam %.2f"
      % (p.value_of("rock"), p.value_of("tower_mid"),
         p.value_of("fog_low"), p.value_of("beam")))
print("split:", SPLIT, "=", sum(SPLIT.values()))
print(s.compare(PLAN))

plans = {
    "fog under":  {"shape": fog_field(), "brush": "bristle", "size": 0.19,
                   "density": 0.7, "direction": (8, 98)},
    "sea":        {"shape": sea(), "brush": "flat", "size": 0.13,
                   "density": 0.8, "direction": 4},
    "rock":       {"shape": rock(), "brush": "bristle", "size": 0.105,
                   "density": 0.85, "direction": ("axis", 62)},
    "beam":       {"shape": beam(), "brush": "bristle", "size": 0.085,
                   "density": 0.75, "direction": "axis"},
    "tower":      {"shape": tower(), "brush": "flat", "size": 0.035,
                   "density": 1.0, "direction": 90, "edge": "clean"},
    "tower mid":  {"shape": tower_mid_face(), "brush": "flat", "size": 0.026,
                   "density": 1.0, "direction": 90},
    "tower lit":  {"shape": tower_lit_face(), "brush": "flat", "size": 0.020,
                   "density": 1.0, "direction": 90},
    "gallery":    {"shape": gallery(), "brush": "flat", "size": 0.014,
                   "density": 1.0, "direction": "axis"},
    "lantern":    {"shape": lantern(), "brush": "flat", "size": 0.028,
                   "density": 1.0, "direction": 90},
    "vines":      {"shape": vines(), "brush": "bristle", "size": 0.040,
                   "density": 0.95, "direction": (35, 115)},
    "roof":       {"shape": roof(), "brush": "flat", "size": 0.020,
                   "density": 1.0, "direction": "axis"},
}
total = 0
for name, plan in plans.items():
    c = s.cost(plan, share=0)
    total += c
    print(f"  cost {name:10s} {c:4d}")
print("costed masses total:", total,
      "(the scumbles are n each: fog 9, sea 7, halo 7, rock face 6)")
for k in ("rock", "vines", "lantern", "beam"):
    print(" ", s.cost_line(plans[k]).splitlines()[-1].strip())

outline = [dict(shape=fog_lower(), label="fog_lower"),
           dict(shape=sea(), label="sea"),
           dict(shape=rock(), label="rock"),
           dict(shape=beam(), label="beam"),
           dict(shape=halo(), label="halo"),
           dict(shape=tower(), label="tower"),
           dict(shape=tower_lit_face(), label="lit face"),
           dict(shape=gallery(), label="gallery"),
           dict(shape=lantern(), label="lantern"),
           dict(shape=vines(), label="vines"),
           dict(shape=roof(), label="roof")]
outline += [dict(points=pts, brush="round_hard", size=w, label="")
            for pts, w in STAIRS]
outline += [dict(points=[(x - r, y), (x + r, y)], brush="round_hard",
                 size=r * 1.4, label="") for x, y, r, *_ in POTS]
print(s.preview(outline, grid=True))
print(s.look(grid=True))
