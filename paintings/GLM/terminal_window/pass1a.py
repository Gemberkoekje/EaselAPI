# pass 1a -- the three big masses, biggest brush, density < 1 so the ground breathes
# depth order: wall (all canvas) -> desk band -> foreground
plan = [
    {"shape": region("all"), "brush": "flat", "color": p["room_c"], "size": 0.17,
     "density": 0.75, "direction": 3},
    {"shape": desk_band, "brush": "flat", "color": p["desk"], "size": 0.09,
     "density": 0.8, "direction": 2},
    {"shape": fore, "brush": "flat", "color": p["fore"], "size": 0.12,
     "density": 0.8, "direction": 2},
]
print(s.cost_line(plan))
s.paint(plan)
