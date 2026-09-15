s.marks.clear()
plan = [
    {"region": slot(),  "brush": "bristle", "color": "opening",
     "density": 1.0, "size": 0.10, "solid": True, "direction": [(0.26, 0.72), VP]},
    {"region": deck(),  "brush": "bristle", "color": "deck",
     "density": 0.75, "size": 0.18, "direction": "cross", "edge": "hard"},
    {"region": water(), "brush": "bristle", "color": "water",
     "density": 0.75, "size": 0.15, "direction": "horizontal", "edge": "hard"},
]
print(s.cost_line(plan))
s.paint(plan)
s.look(values=True, path="out/04_values.png")
s.look(path="out/04_masses.png")
print(s.compare({deck(): 0.22, water(): 0.28, slot(): 0.80}))
