from easel import Session, Region, region, blob, cell

out = {}

# 1. value scale
s = Session(900, 200, ground="toned_grey", seed=1)
p = s.palette
dark = p.mix("ultramarine", "burnt_umber", 0.5)
lo, hi = p.value_of(dark), p.value_of("titanium_white")
print(f"E1 darkest={lo:.2f} white={hi:.2f}")
for i in range(9):
    target = lo + (hi - lo) * i / 8
    band = Region(i / 9.0, 0.15, (i + 1) / 9.0, 0.85)
    s.block_in(band, "flat", p.at_value(dark, target), density=1.0, size=0.06)
out["e1"] = s.look(values=True)

# 3. paint running out
s = Session(900, 400, texture="rough", ground="toned_grey", seed=3)
for i, load in enumerate([1.0, 0.6, 0.35, 0.2]):
    y = 0.15 + i * 0.22
    s.stroke([(0.06, y), (0.94, y)], "bristle", "titanium_white",
             size=0.07, load=load, load_falloff=0.0, pressure="even")
out["e3"] = s.look()

# 6. mixing
p6 = Session(600, 200, seed=6).palette
for a, b in [("cadmium_yellow", "ultramarine"), ("cadmium_red", "ultramarine"),
             ("cadmium_yellow", "cadmium_red"), ("cerulean", "titanium_white")]:
    print("E6", a, "+", b, "->", p6.hex(p6.mix(a, b, 0.5)))

# 8. box vs shape
s = Session(900, 400, ground="toned_grey", seed=3)
s.palette["dark"] = s.palette.mix("ultramarine", "burnt_umber", 0.45)
mass = blob(cell("B4").point(0.5, 0.5), 0.16, 0.30, wobble=0.3, seed=1)
s.block_in(mass.box, "bristle", "dark", size=0.10, direction="axis")
s.block_in(mass.shifted(0.5, 0.0), "bristle", "dark", size=0.10, direction="axis")
out["e8"] = s.look()

# 9. swatch strip -- and the pigments available
s = Session(900, 200, ground="toned_grey", seed=9)
p = s.palette
print("E9 PIGMENTS:", sorted(p.pigments) if hasattr(p, "pigments") else "?")
print("E9 grounds value check")
for name, colour in {"probe": p.mix("cerulean", "burnt_umber", 0.4)}.items():
    print(" ", name, p.hex(colour), f"v={p.value_of(colour):.2f}")
out["e9"] = s.look()

for k, v in out.items():
    print("LOOK", k, v)
