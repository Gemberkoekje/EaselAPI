"""The ten exercises from PAINTER.md, each look written to its own file."""

from easel import Session, Region, region, cell, polygon, blob, ellipse, ribbon, union

# 1. A value scale.
s = Session(900, 200, ground="toned_grey", seed=1, out_dir=".")
p = s.palette
dark = p.mix("ultramarine", "burnt_umber", 0.5)
lo, hi = p.value_of(dark), p.value_of("titanium_white")
for i in range(9):
    target = lo + (hi - lo) * i / 8
    band = Region(i / 9.0, 0.15, (i + 1) / 9.0, 0.85)
    s.block_in(band, "flat", p.at_value(dark, target), density=1.0, size=0.06,
               direction="axis")
    print(f"value {target:.2f}  reads {p.value_of(p.at_value(dark, target)):.2f}")
s.look(values=True, path="ex01_values.png")

# 2. One stroke, six pressures.
s = Session(900, 500, ground="toned_grey", seed=2, out_dir=".")
for i, pr in enumerate(["taper", "press_in", "lift_off", "even", "swell", "dab"]):
    y = 0.12 + i * 0.15
    s.stroke([(0.10, y), (0.50, y)], "round_soft", "titanium_white", pressure=pr,
             size=0.05, opacity=0.35, load=1.0, load_falloff=0.0, note=pr)
    s.stroke([(0.55, y), (0.92, y)], "bristle", "titanium_white", pressure=pr,
             size=0.05, opacity=0.35, load=1.0, load_falloff=0.0, note=pr)
s.look(path="ex02_pressures.png")

# 3. Paint running out.
s = Session(900, 400, texture="rough", ground="toned_grey", seed=3, out_dir=".")
for i, load in enumerate([1.0, 0.6, 0.35, 0.2]):
    y = 0.15 + i * 0.22
    s.stroke([(0.06, y), (0.94, y)], "bristle", "titanium_white",
             size=0.07, load=load, load_falloff=0.0, pressure="even")
s.look(path="ex03_loads.png")

# 4. Wet versus dry.
s = Session(800, 400, ground="white", seed=4, out_dir=".")
s.stroke([(0.10, 0.27), (0.90, 0.27)], "flat", "ultramarine", size=0.22, pressure="even")
s.stroke([(0.15, 0.27), (0.85, 0.27)], "flat", "cadmium_yellow", size=0.10, pressure="even")
s.stroke([(0.10, 0.73), (0.90, 0.73)], "flat", "ultramarine", size=0.22, pressure="even")
s.dry()
s.stroke([(0.15, 0.73), (0.85, 0.73)], "flat", "cadmium_yellow", size=0.10, pressure="even")
s.look(path="ex04_wet_dry.png")

# 5. An edge study.
s = Session(900, 300, ground="toned_grey", seed=5, out_dir=".")
left, mid, right = region("all").split_h(3)
for r in (left, mid, right):
    s.block_in(r, "bristle", "burnt_umber", density=1.0, size=0.1)
s.dry()
light = s.palette.tint("burnt_umber", 0.6)
s.block_in(left, "bristle", light, density=1.0, size=0.1, edge="hard")
s.stroke([(0.38, 0.5), (0.62, 0.5)], "round_hard", light, size=0.03)
s.smudge([(0.333, 0.40), (0.333, 0.60)])
s.look(path="ex05_edges.png")

# 6. Mixing.
p = Session(600, 200, seed=6, out_dir=".").palette
for a, b in [("cadmium_yellow", "ultramarine"), ("cadmium_red", "ultramarine"),
             ("cadmium_yellow", "cadmium_red"), ("cerulean", "titanium_white"),
             ("alizarin", "burnt_umber"), ("cadmium_red", "burnt_umber")]:
    print(a, "+", b, "->", p.hex(p.mix(a, b, 0.5)))

# 7. Draw, try, paint.
s = Session(900, 600, ground="toned_grey", seed=7, out_dir=".")
s.mark("a", *cell("C3").point(0.5, 0.5))
s.mark("b", *cell("F3").point(0.5, 0.5))
s.mark("c", *cell("D6").point(0.5, 0.5))
s.pencil(polygon([s.pt("a"), s.pt("b"), s.pt("c")]), pressure=0.7)
s.look(path="ex07a_drawing.png")
plan = [{"points": [s.pt("a"), s.pt("c")], "brush": "bristle", "size": 0.09,
         "color": "titanium_white"}]
s.rehearse(plan, region="C3:F6", path="ex07b_rehearse_bristle.png")
s.rehearse([dict(plan[0], size=0.03, brush="liner")], region="C3:F6",
           path="ex07c_rehearse_liner.png")
s.stroke(**plan[0])
s.look(region="C3:F6", path="ex07d_painted.png")

# 8. A box and a shape.
s = Session(900, 400, ground="toned_grey", seed=3, out_dir=".")
s.palette["dark"] = s.palette.mix("ultramarine", "burnt_umber", 0.45)
mass = blob(cell("B4").point(0.5, 0.5), 0.16, 0.30, wobble=0.3, seed=1)
s.block_in(mass.box, "bristle", "dark", size=0.10, direction="axis")
s.block_in(mass.shifted(0.5, 0.0), "bristle", "dark", size=0.10, direction="axis")
s.look(path="ex08_box_shape.png")

# 9. A swatch strip.
s = Session(900, 200, ground="toned_grey", seed=9, out_dir=".")
p = s.palette
plan = {"haze": p.at_value(p.mix("cerulean", "titanium_white", 0.8), 0.64),
        "deep": p.at_value(p.mix("cerulean", "burnt_umber", 0.4), 0.40),
        "dark": p.at_value(p.mix("burnt_umber", "viridian", 0.3), 0.20),
        "lit": p.at_value(p.mix("yellow_ochre", "titanium_white", 0.6), 0.78)}
for i, (name, colour) in enumerate(plan.items()):
    band = Region(0.05 + i * 0.225, 0.15, 0.25 + i * 0.225, 0.85)
    s.block_in(band, "flat", colour, size=0.04, solid=True)
    print(f"{name:5s} value {p.value_of(colour):.2f}  chroma {p.chroma_of(colour):.2f}")
s.look(path="ex09_swatches.png")

# 10. Three silhouettes. Expected, written before looking:
#   A: a round body with a small head on top and two legs: a front-on stool or a frog.
#   B: the head moved off to the left and the legs splayed: something turned, walking left.
#   C: one leg swollen into a haunch: a crouching animal, weight on one side.
s = Session(900, 600, ground="toned_grey", seed=10, out_dir=".")
big, top = ellipse((0.5, 0.6), 0.16, 0.13), ellipse((0.5, 0.44), 0.06, 0.08)
members = [ribbon([(x, 0.64), (x, 0.9)], 0.03) for x in (0.42, 0.58)]
turned = [top.shifted(-0.13, 0.04), members[0].shifted(-0.03, 0),
          members[1].shifted(0.05, 0)]
swell = ribbon([(0.40, 0.68), (0.35, 0.80), (0.37, 0.93)], 0.07, end_width=0.02)
for i, parts in enumerate(([big, top, *members], [big, *turned],
                           [big, turned[0], swell, turned[2]])):
    print(s.thumbnail({union(*parts): "burnt_umber"}, path=f"ex10_{'abc'[i]}.png"))
