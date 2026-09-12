for d in ((4, 94), (5, 173), 5):
    plan = {"shape": fascia(), "brush": "bristle", "color": "facade",
            "density": 0.9, "size": 0.030, "direction": d}
    print(f"  direction {str(d):10s} -> {s.cost(plan):3d}")
print(s.cost_line({"shape": fascia(), "brush": "bristle", "color": "facade",
                   "density": 0.9, "size": 0.030, "direction": (4, 94)}))
