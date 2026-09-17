exec(open("pears.py").read())
plan = []
for k, shp in SHAPES.items():
    c = s.cost({"shape": shp, "brush": "flat", "size": 0.02, "direction": "axis"})
    print(k, "box", shp.box, "cost@0.02", c,
          "cost@0.025", s.cost({"shape": shp, "brush": "flat", "size": 0.025, "direction": "axis"}),
          "top", tuple(round(v, 3) for v in TOPS[k]))
    plan.append({"shape": shp, "brush": "flat", "size": 0.02, "direction": "axis", "label": k})
print(s.preview(plan, grid=True))
