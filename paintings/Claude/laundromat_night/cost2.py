fig = figure()
print("figure box:", [round(v, 3) for v in (fig.box.x0, fig.box.y0, fig.box.x1, fig.box.y1)])
print("area", round(fig.area, 5), " inset(0.006) area", round(fig.inset(0.006).area, 5),
      " inset(0.008)", round(fig.inset(0.008).area, 5))
for sz in (0.010, 0.013, 0.016):
    for ed in ("ragged", "clean"):
        plan = {"shape": fig, "brush": "flat", "color": "figure", "density": 1.0,
                "solid": True, "size": sz, "direction": "axis", "edge": ed}
        print(f"  figure size {sz}  {ed:7s} -> {s.cost(plan):3d}")
band = machine_band()
print("  band  ->", s.cost({"shape": band, "brush": "flat", "color": "machine",
                            "density": 1.0, "solid": True, "size": 0.024,
                            "direction": "axis"}))
print(s.preview([{"shape": fig.inset(0.006), "label": "figure inset"},
                 {"shape": band, "label": "band"}], region="E4:F6", grid="fine"))
