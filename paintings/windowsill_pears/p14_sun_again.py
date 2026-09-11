exec(open("helpers.py").read())
exec(open("pears.py").read())
p = s.palette
p["glow"] = to_value(p["glow"], 0.87)
s.dry()
# bury the bars: the upper pane again, then the wall where the bars spilled
s.block_in(Region(0.155, -0.02, 0.68, 0.34), "flat", "window", density=1.0, size=0.12,
           direction=12, load=1.0, overhang=0, note="upper pane, bars buried")
s.block_in(Region(0.03, -0.02, 0.155, 0.24), "flat", "wall", density=1.0, size=0.06,
           direction=84, load=1.0, overhang=0, note="wall where the sun spilled")
# the sun as one region with a diagonal lower edge, laid along that diagonal
sun = polygon([(0.15, -0.02), (0.64, -0.02), (0.57, 0.10), (0.38, 0.27), (0.15, 0.27)])
plan = {"shape": sun.inset(0.03), "brush": "flat", "size": 0.08, "direction": 22, "density": 0.9}
print("sun cost", s.cost(plan))
s.block_in(sun.inset(0.03), "flat", "glow", density=0.9, size=0.08, direction=22,
           opacity=0.6, load=1.0, note="sun in the pane, one region")
# calm the striped sill patch and the dotty middle fold
s.stroke([(-0.02, 0.665), (0.21, 0.668)], "round_soft", "sill_lit", size=0.045, opacity=0.5,
         pressure="even", load=1.0, note="sill light merged")
s.stroke([(0.90, 0.12), (0.905, 0.48)], "round_soft", "curtain", size=0.04, opacity=0.4,
         pressure="even", load=1.0, note="middle fold calmed")
print("strokes:", s.stroke_count)
print(s.look(region="C3:E5"))
print(s.look())
