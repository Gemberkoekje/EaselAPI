p = s.palette
def at_value(base, target, other="titanium_white"):
    a, b = 0.0, 1.0
    for _ in range(24):
        m = (a+b)/2
        if p.value_of(p.mix(base, other, m)) < target: a = m
        else: b = m
    return (a+b)/2
warm  = p.mix("yellow_ochre","burnt_sienna",0.30)
umboc = p.mix("burnt_umber","yellow_ochre",0.50)
def V(base, v): return p.mix(base,"titanium_white", at_value(base,v))

p["wall_hi"]   = V(warm, 0.71)
p["wall_lit"]  = V(warm, 0.60)
p["wall_mid"]  = V(warm, 0.52)
p["wall_dim"]  = V(warm, 0.42)
p["ceiling"]   = V(umboc, 0.31)
p["dark"]      = p.mix("ultramarine","burnt_umber",0.55)
p["dark_soft"] = V(p.mix("ultramarine","burnt_umber",0.6), 0.19)
p["pale_cool"] = V(p.mix("ultramarine","burnt_sienna",0.5), 0.62)
p["blue_dim"]  = V(p.mix("ultramarine","burnt_sienna",0.35), 0.23)
for n in ("wall_hi","wall_lit","wall_mid","wall_dim","ceiling","dark","dark_soft","pale_cool","blue_dim"):
    print(f"{n:10s} {p.hex(p[n])} {p.value_of(p[n]):.2f}")

# --- right wall: a plane with a slanted, broken left edge, not a box
wall = polygon([(0.735,0.0),(1.0,0.0),(1.0,0.46),(0.925,0.48),(0.855,0.40),(0.795,0.33),(0.757,0.19)])
s.block_in(wall, "flat", "wall_mid", direction=(96,), density=0.95, size=0.085, load=1.0)
s.block_in(polygon([(0.875,0.0),(1.0,0.0),(1.0,0.30),(0.905,0.26)]), "bristle", "wall_hi",
           direction=(102,), density=0.9, size=0.07, load=1.0)
s.stroke([(0.96,0.05),(0.985,0.36)], "flat", "wall_lit", size=0.05, pressure="even")
s.dry()

# --- ceiling band, laid along its own slight slope
ceil = polygon([(0.255,0.0),(0.735,0.0),(0.715,0.135),(0.44,0.155),(0.27,0.115)])
s.block_in(ceil, "bristle", "ceiling", direction=(-4,), density=0.85, size=0.075, load=0.85)
s.stroke([(0.30,0.055),(0.62,0.030)], "bristle", "wall_dim", size=0.028, load=0.55, pressure="swell")
s.dab(0.685, 0.022, "round_hard", "wall_hi", size=0.035, press=3)
s.dry()

# --- warm wall left of the head, and the lit strip in the doorway
s.block_in(polygon([(0.13,0.0),(0.30,0.0),(0.275,0.16),(0.14,0.20)]), "bristle", "wall_dim",
           direction=(78,), density=0.85, size=0.07, load=0.9)
s.stroke([(0.098,0.005),(0.086,0.255)], "flat", "wall_mid", size=0.048, pressure="even")
s.stroke([(0.043,0.30),(0.030,0.45)], "flat", "pale_cool", size=0.075, pressure="swell")
s.stroke([(0.062,0.245),(0.052,0.40)], "bristle", "pale_cool", size=0.04, load=0.6)
s.dry()

# --- warm wall behind the hair, right of the head
s.block_in(polygon([(0.615,0.175),(0.775,0.16),(0.79,0.42),(0.64,0.44)]), "bristle", "wall_dim",
           direction=(84,), density=0.85, size=0.07, load=0.9)
s.dry()

# --- the cool patch (window/screen) at F2
s.block_in(polygon([(0.655,0.125),(0.755,0.135),(0.752,0.245),(0.66,0.24)]), "flat", "blue_dim",
           direction=(6,), density=0.9, size=0.045, load=1.0)
s.dry()

# --- the dark shelving mass behind the head (far, goes under everything)
darkbg = polygon([(0.248,0.105),(0.40,0.075),(0.505,0.115),(0.505,0.30),(0.455,0.375),
                  (0.437,0.52),(0.335,0.50),(0.258,0.395)])
s.block_in(darkbg, "bristle", "dark", direction="axis", density=1.0, size=0.062, load=1.0)
s.block_in(blob(cell("A2").point(0.5,0.55), 0.075, 0.062, wobble=0.35, seed=4), "flat", "dark_soft",
           direction=(20,), density=0.9, size=0.05, load=1.0)
print("strokes:", s.stroke_count)
