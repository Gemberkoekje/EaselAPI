import os
from easel import Session, Region, cell, region, blob
W = os.path.dirname(os.path.abspath(__file__))
os.chdir(W)

# 1. value scale
s = Session(900, 200, ground="toned_grey", seed=1, out_dir=W)
p = s.palette
dark = p.mix("ultramarine", "burnt_umber", 0.5)
lo, hi = p.value_of(dark), p.value_of("titanium_white")
for i in range(9):
    t = lo + (hi - lo) * i / 8
    s.block_in(Region(i/9.0, 0.15, (i+1)/9.0, 0.85), "flat", p.at_value(dark, t), density=1.0, size=0.06, direction="axis")
s.look(values=True, path=f"{W}/ex1_values.png")

# 4. wet vs dry
s = Session(800, 400, ground="white", seed=4, out_dir=W)
s.stroke([(0.10, 0.27), (0.90, 0.27)], "flat", "ultramarine", size=0.22, pressure="even")
s.stroke([(0.15, 0.27), (0.85, 0.27)], "flat", "cadmium_yellow", size=0.10, pressure="even")
s.stroke([(0.10, 0.73), (0.90, 0.73)], "flat", "ultramarine", size=0.22, pressure="even")
s.dry()
s.stroke([(0.15, 0.73), (0.85, 0.73)], "flat", "cadmium_yellow", size=0.10, pressure="even")
s.look(path=f"{W}/ex4_wetdry.png")

# 5. edge study
s = Session(900, 300, ground="toned_grey", seed=5, out_dir=W)
left, mid, right = region("all").split_h(3)
for r in (left, mid, right):
    s.block_in(r, "bristle", "burnt_umber", density=1.0, size=0.1)
s.dry()
light = s.palette.tint("burnt_umber", 0.6)
s.block_in(left, "bristle", light, density=1.0, size=0.1, edge="hard")
s.stroke([(0.38, 0.5), (0.62, 0.5)], "round_hard", light, size=0.03)
s.smudge([(0.333, 0.40), (0.333, 0.60)])
s.look(path=f"{W}/ex5_edges.png")

# 8. box vs shape
s = Session(900, 400, ground="toned_grey", seed=3, out_dir=W)
s.palette["dark"] = s.palette.mix("ultramarine", "burnt_umber", 0.45)
mass = blob(cell("B4").point(0.5, 0.5), 0.16, 0.30, wobble=0.3, seed=1)
s.block_in(mass.box, "bristle", "dark", size=0.10, direction="axis")
s.block_in(mass.shifted(0.5, 0.0), "bristle", "dark", size=0.10, direction="axis")
s.look(path=f"{W}/ex8_boxshape.png")

# grounds' values
s = Session(200, 200, seed=0, out_dir=W)
for g in ["toned_grey", "toned_warm_grey", "cool_grey", "umber_wash", "burnt_sienna", "warm_white"]:
    print(f"ground {g:16s} value {s.palette.value_of(Session(64,64,ground=g, out_dir=W).sample()):.2f}")
