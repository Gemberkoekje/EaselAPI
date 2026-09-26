"""PAINTER.md's nine exercises, each look written to its own file."""
from easel import Session, Region, region, cell, blob

# 1. A value scale.
s = Session(900, 200, ground="toned_grey", seed=1, out_dir="out")
p = s.palette
dark = p.mix("ultramarine", "burnt_umber", 0.5)
lo, hi = p.value_of(dark), p.value_of("titanium_white")
for i in range(9):
    target = lo + (hi - lo) * i / 8
    band = Region(i / 9.0, 0.15, (i + 1) / 9.0, 0.85)
    s.block_in(band, "flat", p.at_value(dark, target), density=1.0, size=0.06, direction="axis")
    print(f"1: value {target:.2f}  reads {p.value_of(p.at_value(dark, target)):.2f}")
s.look(values=True, path="out/ex1-values.png")

# 2. One stroke, six pressures.
s = Session(900, 500, ground="toned_grey", seed=2, out_dir="out")
for i, pr in enumerate(["taper", "press_in", "lift_off", "even", "swell", "dab"]):
    y = 0.12 + i * 0.15
    s.stroke([(0.10, y), (0.50, y)], "round_soft", "titanium_white", pressure=pr,
             size=0.05, opacity=0.35, load=1.0, load_falloff=0.0, note=pr)
    s.stroke([(0.55, y), (0.92, y)], "bristle", "titanium_white", pressure=pr,
             size=0.05, opacity=0.35, load=1.0, load_falloff=0.0, note=pr)
s.look(path="out/ex2-pressures.png")

# 3. Paint running out.
s = Session(900, 400, texture="rough", ground="toned_grey", seed=3, out_dir="out")
for i, load in enumerate([1.0, 0.6, 0.35, 0.2]):
    y = 0.15 + i * 0.22
    s.stroke([(0.06, y), (0.94, y)], "bristle", "titanium_white",
             size=0.07, load=load, load_falloff=0.0, pressure="even")
s.look(path="out/ex3-load.png")

# 4. Wet versus dry.
s = Session(800, 400, ground="white", seed=4, out_dir="out")
s.stroke([(0.10, 0.27), (0.90, 0.27)], "flat", "ultramarine", size=0.22, pressure="even")
s.stroke([(0.15, 0.27), (0.85, 0.27)], "flat", "cadmium_yellow", size=0.10, pressure="even")
s.stroke([(0.10, 0.73), (0.90, 0.73)], "flat", "ultramarine", size=0.22, pressure="even")
s.dry()
s.stroke([(0.15, 0.73), (0.85, 0.73)], "flat", "cadmium_yellow", size=0.10, pressure="even")
s.look(path="out/ex4-wet-dry.png")

# 5. An edge study.
s = Session(900, 300, ground="toned_grey", seed=5, out_dir="out")
left, mid, right = region("all").split_h(3)
for r in (left, mid, right):
    s.block_in(r, "bristle", "burnt_umber", density=1.0, size=0.1)
s.dry()
light = s.palette.tint("burnt_umber", 0.6)
s.block_in(left, "bristle", light, density=1.0, size=0.1, edge="hard")
s.stroke([(0.38, 0.5), (0.62, 0.5)], "round_hard", light, size=0.03)
s.smudge([(0.333, 0.40), (0.333, 0.60)])
s.look(path="out/ex5-edges.png")

# 6. Mixing.
pal = Session(600, 200, seed=6).palette
for a, b in [("cadmium_yellow", "ultramarine"), ("cadmium_red", "ultramarine"),
             ("cadmium_yellow", "cadmium_red"), ("cerulean", "titanium_white")]:
    print("6:", a, "+", b, "->", pal.hex(pal.mix(a, b, 0.5)))

# 7. Draw, try, paint.
s = Session(900, 600, ground="toned_grey", seed=7, out_dir="out")
s.mark("a", *cell("C3").point(0.5, 0.5))
s.mark("b", *cell("F3").point(0.5, 0.5))
s.mark("c", *cell("D6").point(0.5, 0.5))
s.pencil([s.pt("a"), s.pt("b"), s.pt("c"), s.pt("a")], pressure=0.7)
s.look(path="out/ex7-drawing.png")
plan = [{"points": [s.pt("a"), s.pt("c")], "brush": "bristle", "size": 0.09,
         "color": "titanium_white"}]
s.rehearse(plan, region="C3:F6")
s.rehearse([dict(plan[0], size=0.03, brush="liner")], region="C3:F6")
s.stroke(**plan[0])
s.look(region="C3:F6", path="out/ex7-painted.png")

# 8. A box and a shape.
s = Session(900, 400, ground="toned_grey", seed=3, out_dir="out")
s.palette["dark"] = s.palette.mix("ultramarine", "burnt_umber", 0.45)
mass = blob(cell("B4").point(0.5, 0.5), 0.16, 0.30, wobble=0.3, seed=1)
s.block_in(mass.box, "bristle", "dark", size=0.10, direction="axis")
s.block_in(mass.shifted(0.5, 0.0), "bristle", "dark", size=0.10, direction="axis")
s.look(path="out/ex8-box-shape.png")

# 9. A swatch strip -- this painting's own mixtures, not the example's: dusk and lantern.
s = Session(900, 200, ground="toned_grey", seed=9, out_dir="out")
p = s.palette
swatches = {
    "dusk": p.at_value(p.mix("ultramarine", "cerulean", 0.5), 0.42),
    "night": p.at_value(p.mix("ultramarine", "burnt_umber", 0.55), 0.15),
    "skin_lit": p.at_value(p.mix_many(["yellow_ochre", "cadmium_red", "titanium_white"], [2, 1, 5]), 0.68),
    "skin_shade": p.at_value(p.mix_many(["burnt_sienna", "burnt_umber", "ultramarine"], [3, 2, 1]), 0.24),
}
for i, (name, colour) in enumerate(swatches.items()):
    band = Region(0.05 + i * 0.225, 0.15, 0.25 + i * 0.225, 0.85)
    s.block_in(band, "flat", colour, size=0.04, solid=True)
    print(f"9: {name:10s} value {p.value_of(colour):.2f}  chroma {p.chroma_of(colour):.2f}")
s.look(path="out/ex9-swatches.png")
