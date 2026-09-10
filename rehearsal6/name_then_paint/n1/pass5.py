# Pass 5 - quiet masses with `flat`, and modulation too small to draw an edge.
p = s.palette
p["bg_a"] = p.tint(p.mix("ultramarine","burnt_umber",0.68), 0.045)
p["bg_b"] = p.tint(p.mix(p.mix("ultramarine","burnt_umber",0.76),"yellow_ochre",0.12), 0.075)
p["tbl_lit"] = p.desaturate(p.tint(p.mix(p.mix("burnt_umber","burnt_sienna",0.45),"yellow_ochre",0.20), 0.16), 0.32)
p["tbl_hi"]  = p.desaturate(p.tint(p.mix(p.mix("burnt_umber","burnt_sienna",0.5),"yellow_ochre",0.28), 0.23), 0.28)
for k in ("bg","bg_a","bg_b","tbl","tbl_lit","tbl_hi","tbl_dk"):
    print(f"{k:8s} {p.hex(p[k])}  v={p.value_of(p[k]):.3f}")

s.dry()
s.block_in(polygon([(0.0,0.0),(1.0,0.0),(1.0,0.79),(0.0,0.76)]), "flat", "bg",
           direction=(40, 130), density=1.0, size=0.14, load=1.0, pressure="even")
s.block_in(polygon([(0.0,0.02),(0.44,0.0),(0.66,0.22),(0.55,0.52),(0.18,0.58),(0.0,0.40)]),
           "flat", "bg_a", direction=(31, 119), density=1.0, size=0.11, load=1.0, pressure="even")
s.block_in(polygon([(0.06,0.06),(0.36,0.05),(0.50,0.22),(0.34,0.40),(0.10,0.36)]),
           "flat", "bg_b", direction=(22, 108), density=1.0, size=0.09, load=1.0, pressure="even")

s.dry()
tbl_mass = polygon([(0.0, 0.702), (0.34, 0.709), (0.71, 0.719), (1.0, 0.729),
                    (1.0, 1.0), (0.0, 1.0)])
s.block_in(tbl_mass, "flat", "tbl", direction=(6, 168), density=1.0, size=0.11,
           load=1.0, pressure="even", overhang=0)
s.block_in(polygon([(0.0,0.845),(0.22,0.812),(0.47,0.845),(0.52,0.95),(0.30,1.0),(0.0,1.0)]),
           "flat", "tbl_lit", direction=(9, 163), density=1.0, size=0.09,
           load=1.0, pressure="even", overhang=0)
s.block_in(polygon([(0.03,0.905),(0.20,0.878),(0.33,0.94),(0.26,1.0),(0.05,1.0)]),
           "flat", "tbl_hi", direction=(14, 158), density=1.0, size=0.07,
           load=1.0, pressure="even", overhang=0)
s.block_in(polygon([(0.72, 0.721), (1.0, 0.729), (1.0, 1.0), (0.88, 1.0)]), "flat",
           "tbl_dk", direction=(26, 138), density=1.0, size=0.09, load=1.0,
           pressure="even", overhang=0)

print("strokes:", s.stroke_count)
print(s.look())
print(s.look(values=True))
