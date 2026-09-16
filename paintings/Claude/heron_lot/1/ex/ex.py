import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from easel import Session, Region, region, cell, blob

# 1. A value scale.
s = Session(900, 200, ground="toned_grey", seed=1, out_dir="out1")
p = s.palette
dark = p.mix("ultramarine", "burnt_umber", 0.5)
lo, hi = p.value_of(dark), p.value_of("titanium_white")
print("EX1 floor", round(lo,3), "ceiling", round(hi,3))
for i in range(9):
    target = lo + (hi - lo) * i / 8
    band = Region(i / 9.0, 0.15, (i + 1) / 9.0, 0.85)
    s.block_in(band, "flat", p.at_value(dark, target), density=1.0, size=0.06)
    print(f"  asked {target:.2f}  reads {p.value_of(p.at_value(dark, target)):.2f}")
print("EX1", s.look(values=True))

# 2. One stroke, six pressures.
s = Session(900, 500, ground="toned_grey", seed=2, out_dir="out2")
for i, pr in enumerate(["taper", "press_in", "lift_off", "even", "swell", "dab"]):
    y = 0.12 + i * 0.15
    s.stroke([(0.10, y), (0.50, y)], "round_soft", "titanium_white", pressure=pr,
             size=0.05, opacity=0.35, load=1.0, load_falloff=0.0, note=pr)
    s.stroke([(0.55, y), (0.92, y)], "bristle", "titanium_white", pressure=pr,
             size=0.05, opacity=0.35, load=1.0, load_falloff=0.0, note=pr)
print("EX2", s.look())

# 3. Paint running out.
s = Session(900, 400, texture="rough", ground="toned_grey", seed=3, out_dir="out3")
for i, load in enumerate([1.0, 0.6, 0.35, 0.2]):
    y = 0.15 + i * 0.22
    s.stroke([(0.06, y), (0.94, y)], "bristle", "titanium_white",
             size=0.07, load=load, load_falloff=0.0, pressure="even")
print("EX3", s.look())

# 4. Wet versus dry.
s = Session(800, 400, ground="white", seed=4, out_dir="out4")
s.stroke([(0.10, 0.27), (0.90, 0.27)], "flat", "ultramarine", size=0.22, pressure="even")
s.stroke([(0.15, 0.27), (0.85, 0.27)], "flat", "cadmium_yellow", size=0.10, pressure="even")
s.stroke([(0.10, 0.73), (0.90, 0.73)], "flat", "ultramarine", size=0.22, pressure="even")
s.dry()
s.stroke([(0.15, 0.73), (0.85, 0.73)], "flat", "cadmium_yellow", size=0.10, pressure="even")
print("EX4", s.look())

# 5. An edge study.
s = Session(900, 300, ground="toned_grey", seed=5, out_dir="out5")
left, mid, right = region("all").split_h(3)
for r in (left, mid, right):
    s.block_in(r, "bristle", "burnt_umber", density=1.0, size=0.1)
s.dry()
s.block_in(left,  "bristle", s.palette.tint("burnt_umber", 0.6), density=1.0, size=0.1)
s.stroke([(0.02, 0.5), (0.31, 0.5)], "round_hard",
         s.palette.tint("burnt_umber", 0.6), size=0.03)
s.smudge([(0.35, 0.3), (0.35, 0.7)])
print("EX5", s.look())

# 6. Mixing.
p = Session(600, 200, seed=6, out_dir="out6").palette
for a, b in [("cadmium_yellow", "ultramarine"), ("cadmium_red", "ultramarine"),
             ("cadmium_yellow", "cadmium_red"), ("cerulean", "titanium_white")]:
    print("EX6", a, "+", b, "->", p.hex(p.mix(a, b, 0.5)))

# 7. Draw, try, paint.
s = Session(900, 600, ground="toned_grey", seed=7, out_dir="out7")
s.mark("a", *cell("C3").point(0.5, 0.5))
s.mark("b", *cell("F3").point(0.5, 0.5))
s.mark("c", *cell("D6").point(0.5, 0.5))
s.pencil([s.pt("a"), s.pt("b"), s.pt("c"), s.pt("a")], pressure=0.7)
print("EX7 draw", s.look())
plan = [{"points": [s.pt("a"), s.pt("c")], "brush": "bristle", "size": 0.09,
         "color": "titanium_white"}]
print("EX7 reh-a", s.rehearse(plan, region="C3:F6"))
print("EX7 reh-b", s.rehearse([dict(plan[0], size=0.03, brush="liner")], region="C3:F6"))
s.stroke(**plan[0])
print("EX7 paint", s.look(region="C3:F6"), "count", s.stroke_count)

# 8. A box and a shape.
s = Session(900, 400, ground="toned_grey", seed=3, out_dir="out8")
s.palette["dark"] = s.palette.mix("ultramarine", "burnt_umber", 0.45)
mass = blob(cell("B4").point(0.5, 0.5), 0.16, 0.30, wobble=0.3, seed=1)
s.block_in(mass.box, "bristle", "dark", size=0.10, direction="axis")
s.block_in(mass.shifted(0.5, 0.0), "bristle", "dark", size=0.10, direction="axis")
print("EX8", s.look())

# 9. A swatch strip.
s = Session(900, 200, ground="toned_grey", seed=9, out_dir="out9")
p = s.palette
plan = {"fog": p.at_value(p.mix("cerulean", "titanium_white", 0.8), 0.64),
        "sea": p.at_value(p.mix("cerulean", "burnt_umber", 0.4), 0.40),
        "rock": p.at_value(p.mix("burnt_umber", "viridian", 0.3), 0.20),
        "lit": p.at_value(p.mix("yellow_ochre", "titanium_white", 0.6), 0.78)}
for i, (name, colour) in enumerate(plan.items()):
    band = Region(0.05 + i * 0.225, 0.15, 0.25 + i * 0.225, 0.85)
    s.block_in(band, "flat", colour, size=0.08, solid=True)
    print(f"EX9 {name:5s} value {p.value_of(colour):.2f}  chroma {p.chroma_of(colour):.2f}")
print("EX9", s.look())
