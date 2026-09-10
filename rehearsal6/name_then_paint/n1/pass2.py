# Pass 2 - repaint the two far masses properly: a stepped glow, a darker table.
p = s.palette

p["bg"]      = p.mix("ultramarine", "burnt_umber", 0.62)
p["bg_1"]    = p.tint(p.mix("ultramarine","burnt_umber",0.66), 0.12)
p["bg_2"]    = p.tint(p.mix("ultramarine","burnt_umber",0.70), 0.20)
p["bg_3"]    = p.tint(p.mix(p.mix("ultramarine","burnt_umber",0.74),"yellow_ochre",0.16), 0.26)

p["tbl"]     = p.desaturate(p.tint(p.mix("burnt_umber","burnt_sienna",0.40), 0.16), 0.25)
p["tbl_dk"]  = p.mix(p.mix("burnt_umber","burnt_sienna",0.35), "ultramarine", 0.32)
p["tbl_lit"] = p.desaturate(p.tint(p.mix(p.mix("burnt_umber","burnt_sienna",0.45),"yellow_ochre",0.25), 0.30), 0.28)
p["tbl_hi"]  = p.desaturate(p.tint(p.mix(p.mix("burnt_umber","burnt_sienna",0.5),"yellow_ochre",0.35), 0.40), 0.22)

for k in ("bg","bg_1","bg_2","bg_3","tbl","tbl_dk","tbl_lit","tbl_hi"):
    print(f"{k:8s} {p.hex(p[k])}  v={p.value_of(p[k]):.3f}")

s.dry()

# --- kill the stipple: cover the whole glow area, then build it as steps -------
s.block_in(ellipse(Region(0.06, 0.02, 0.82, 0.70)).inset(0.05), "flat", "bg",
           direction=(28, 116), density=1.0, size=0.12, load=1.0, pressure="even")

for shape, col, ang in (
        (ellipse(Region(0.09, 0.04, 0.78, 0.66)), "bg_1", (22, 108)),
        (ellipse(Region(0.17, 0.10, 0.67, 0.56)), "bg_2", (34, 122)),
        (ellipse(Region(0.25, 0.17, 0.57, 0.46)), "bg_3", (16, 100))):
    s.block_in(shape.inset(0.045), "flat", col, direction=ang, density=1.0,
               size=0.09, load=1.0, pressure="even")

# lose the joins while the paint is still wet
for pts in ([(0.14, 0.30), (0.19, 0.16)], [(0.30, 0.09), (0.46, 0.07)],
            [(0.66, 0.20), (0.71, 0.36)], [(0.58, 0.53), (0.44, 0.60)],
            [(0.24, 0.50), (0.16, 0.42)], [(0.63, 0.11), (0.70, 0.24)]):
    s.smudge(pts, size=0.042)

# --- the table, covered solidly and much darker --------------------------------
s.dry()
tbl_mass = polygon([(0.0, 0.700), (0.40, 0.712), (1.0, 0.729), (1.0, 1.0), (0.0, 1.0)])
s.block_in(tbl_mass, "flat", "tbl", direction=(4, 167), density=1.0, size=0.10,
           load=1.0, pressure="even")

# the near-left passage where the light reaches the wood - a shape, not a band
s.block_in(blob(Region(0.00, 0.80, 0.56, 1.00), wobble=0.30, seed=4), "bristle",
           "tbl_lit", direction=(7, 158), density=0.95, size=0.09, load=1.0)
s.block_in(blob(Region(0.05, 0.86, 0.36, 1.00), wobble=0.35, seed=9), "bristle",
           "tbl_hi", direction=(11, 150), density=0.85, size=0.07, load=0.95)

# the far right of the table sinks away
s.block_in(polygon([(0.66, 0.72), (1.0, 0.729), (1.0, 1.0), (0.80, 1.0)]), "flat",
           "tbl_dk", direction=(21, 143), density=1.0, size=0.09, load=1.0, pressure="even")
s.smudge([(0.72, 0.78), (0.69, 0.92)], size=0.045)
s.smudge([(0.55, 0.86), (0.62, 0.97)], size=0.040)

print("strokes:", s.stroke_count)
print(s.look())
print(s.look(values=True))
