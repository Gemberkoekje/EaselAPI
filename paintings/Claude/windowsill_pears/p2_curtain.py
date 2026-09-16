# Pass 2: grey the wall while it is cheap, then the curtain in front of wall and pane.
p = s.palette
p["wall"] = p.desaturate(p["wall"], 0.4)
print("wall now", p.hex(p["wall"]), "value", round(p.value_of(p["wall"]), 2))
s.block_in(Region(-0.02, -0.02, 0.15, 0.62), "flat", "wall", density=0.9, size=0.10,
           direction=84, load=1.0, overhang=0, note="wall left, greyer")
s.block_in(Region(0.69, -0.02, 0.77, 0.62), "flat", "wall", density=0.9, size=0.08,
           direction=84, load=1.0, overhang=0, note="wall sliver right, greyer")

curtain = polygon([(0.735, -0.02), (1.03, -0.02), (1.03, 0.67), (0.80, 0.675),
                   (0.72, 0.645), (0.74, 0.55), (0.725, 0.40), (0.745, 0.20)])
plan = {"shape": curtain.inset(0.04), "brush": "bristle", "size": 0.09,
        "density": 0.9, "direction": (86, 70)}
print("curtain box", curtain.box, "cost", s.cost(plan))
s.block_in(curtain.inset(0.04), "bristle", "curtain", density=0.9, size=0.09,
           direction=(86, 70), load=1.0, note="curtain")
# three folds, wet into the curtain, none the same width or the same slant
s.stroke([(0.79, 0.00), (0.785, 0.30), (0.775, 0.63)], "bristle", "curtain_fold",
         size=0.035, pressure=[0.6, 1.0, 0.7], note="fold")
s.stroke([(0.875, -0.01), (0.885, 0.35), (0.87, 0.62)], "bristle", "curtain_fold",
         size=0.045, pressure=[0.5, 0.9, 1.0], note="fold")
s.stroke([(0.955, 0.02), (0.95, 0.40), (0.965, 0.60)], "bristle", "curtain_fold",
         size=0.028, pressure=[0.8, 0.6, 0.9], note="fold")
print("strokes:", s.stroke_count)
print(s.look(grid=True))
