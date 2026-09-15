from easel import Session, region, blob, cell

s = Session(900, 300, ground="toned_grey", seed=5, out_dir="out_ex5")
left, mid, right = region("all").split_h(3)
for r in (left, mid, right):
    s.block_in(r, "bristle", "burnt_umber", density=1.0, size=0.1)
s.dry()
s.block_in(left,  "bristle", s.palette.tint("burnt_umber", 0.6), density=1.0, size=0.1)
s.stroke([(0.02, 0.5), (0.31, 0.5)], "round_hard", s.palette.tint("burnt_umber", 0.6), size=0.03)
s.smudge([(0.35, 0.3), (0.35, 0.7)])
print("ex5", s.look())

p = Session(600, 200, seed=6, out_dir="out_ex6").palette
for a, b in [("cadmium_yellow", "ultramarine"), ("cadmium_red", "ultramarine"),
             ("cadmium_yellow", "cadmium_red"), ("cerulean", "titanium_white"),
             ("burnt_sienna", "ultramarine"), ("yellow_ochre", "cadmium_red"),
             ("burnt_umber", "viridian"), ("alizarin", "viridian")]:
    m = p.mix(a, b, 0.5)
    print(f"{a:16s}+ {b:16s}-> {p.hex(m)}  v={p.value_of(m):.2f} c={p.chroma_of(m):.2f}")

s8 = Session(900, 400, ground="toned_grey", seed=3, out_dir="out_ex8")
s8.palette["dark"] = s8.palette.mix("ultramarine", "burnt_umber", 0.45)
mass = blob(cell("B4").point(0.5, 0.5), 0.16, 0.30, wobble=0.3, seed=1)
s8.block_in(mass.box, "bristle", "dark", size=0.10, direction="axis")
s8.block_in(mass.shifted(0.5, 0.0), "bristle", "dark", size=0.10, direction="axis")
print("ex8", s8.look())
