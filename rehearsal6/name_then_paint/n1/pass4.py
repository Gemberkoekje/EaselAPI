# Pass 4 - the comb is printing stripes. Lay the quiet masses with a round tip.
p = s.palette
p["bg_a"] = p.tint(p.mix("ultramarine","burnt_umber",0.68), 0.075)
p["bg_b"] = p.tint(p.mix(p.mix("ultramarine","burnt_umber",0.74),"yellow_ochre",0.14), 0.13)
p["tbl_lit"] = p.desaturate(p.tint(p.mix(p.mix("burnt_umber","burnt_sienna",0.45),"yellow_ochre",0.22), 0.20), 0.30)
p["tbl_hi"]  = p.desaturate(p.tint(p.mix(p.mix("burnt_umber","burnt_sienna",0.5),"yellow_ochre",0.30), 0.28), 0.25)
for k in ("bg","bg_a","bg_b","tbl","tbl_lit","tbl_hi","tbl_dk"):
    print(f"{k:8s} {p.hex(p[k])}  v={p.value_of(p[k]):.3f}")

s.dry()
s.block_in(polygon([(0.0,0.0),(1.0,0.0),(1.0,0.79),(0.0,0.76)]), "round_hard", "bg",
           direction=(40, 130), density=1.0, size=0.13, load=1.0, pressure="even")
# barely-there modulation: two irregular masses, three hundredths of a value apart
s.block_in(blob(Region(0.03, 0.06, 0.62, 0.46), wobble=0.35, seed=11), "round_hard",
           "bg_a", direction=(33, 118), density=0.9, size=0.11, load=1.0, pressure="even")
s.block_in(blob(Region(0.12, 0.10, 0.46, 0.34), wobble=0.40, seed=3), "round_hard",
           "bg_b", direction=(25, 112), density=0.85, size=0.09, load=1.0, pressure="even")

s.dry()
tbl_mass = polygon([(0.0, 0.700), (0.40, 0.712), (1.0, 0.729), (1.0, 1.0), (0.0, 1.0)])
s.block_in(tbl_mass, "round_hard", "tbl", direction=(6, 168), density=1.0, size=0.11,
           load=1.0, pressure="even")
s.block_in(blob(Region(0.03, 0.84, 0.46, 1.00), wobble=0.30, seed=4), "round_hard",
           "tbl_lit", direction=(9, 163), density=0.95, size=0.09, load=1.0, pressure="even")
s.block_in(blob(Region(0.08, 0.90, 0.30, 1.00), wobble=0.35, seed=7), "round_hard",
           "tbl_hi", direction=(13, 157), density=0.9, size=0.07, load=1.0, pressure="even")
s.block_in(polygon([(0.70, 0.723), (1.0, 0.729), (1.0, 1.0), (0.86, 1.0)]), "round_hard",
           "tbl_dk", direction=(24, 140), density=1.0, size=0.09, load=1.0, pressure="even")

print("strokes:", s.stroke_count)
print(s.look())
print(s.look(values=True))
