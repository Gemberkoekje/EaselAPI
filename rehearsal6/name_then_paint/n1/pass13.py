# Pass 13 - foliage: the dark mass under the blooms, then leaves, then stems.
p = s.palette
p["leaf_dk"] = p.mix("viridian", "burnt_umber", 0.58)
p["leaf_cl"] = p.mix(p.mix("viridian", "yellow_ochre", 0.25), "ultramarine", 0.22)
p["leaf_md"] = p.mix(p.mix("viridian", "yellow_ochre", 0.42), "burnt_umber", 0.28)
p["leaf_lt"] = p.tint(p.mix(p.mix("viridian", "yellow_ochre", 0.58), "burnt_umber", 0.18), 0.20)
p["stem"]    = p.mix(p.mix("viridian", "yellow_ochre", 0.48), "burnt_umber", 0.42)
for k in ("leaf_dk","leaf_cl","leaf_md","leaf_lt","stem"):
    print(f"{k:8s} {p.hex(p[k])}  v={p.value_of(p[k]):.3f}")
s.dry()

# the dark bed the blooms sit in
s.block_in(blob(Region(0.352, 0.566, 0.726, 0.688), wobble=0.34, seed=13), "flat",
           "leaf_dk", direction=(24, 152), density=1.0, size=0.038, load=1.0,
           pressure="even")
s.block_in(blob(Region(0.410, 0.584, 0.640, 0.664), wobble=0.40, seed=5), "bristle",
           "leaf_cl", direction=(16, 140), density=0.8, size=0.026, load=0.8)

leaves = [
    (ribbon([(0.334,0.548),(0.284,0.578),(0.230,0.630)], 0.046, 0.007), "leaf_md", 0.022),
    (ribbon([(0.348,0.598),(0.302,0.640),(0.268,0.684)], 0.040, 0.006), "leaf_dk", 0.020),
    (ribbon([(0.724,0.564),(0.780,0.610),(0.830,0.666)], 0.050, 0.008), "leaf_md", 0.024),
    (ribbon([(0.700,0.614),(0.744,0.664),(0.758,0.708)], 0.038, 0.006), "leaf_dk", 0.019),
    (ribbon([(0.548,0.628),(0.590,0.674),(0.588,0.714)], 0.042, 0.008), "leaf_cl", 0.021),
    (ribbon([(0.474,0.638),(0.452,0.686),(0.472,0.718)], 0.034, 0.006), "leaf_dk", 0.017),
    (ribbon([(0.592,0.396),(0.650,0.368),(0.708,0.382)], 0.034, 0.006), "leaf_cl", 0.017),
    (ribbon([(0.318,0.500),(0.286,0.462),(0.268,0.416)], 0.030, 0.005), "leaf_dk", 0.015),
]
for shp, col, sz in leaves:
    s.block_in(shp.inset(sz * 0.5), "bristle", col, direction="axis", density=0.95,
               size=sz, load=0.95)

# light along the top of two of them only
s.stroke([(0.330,0.552),(0.288,0.578),(0.244,0.618)], "round_hard", "leaf_lt",
         size=0.008, pressure=[0.8,0.5,0.2])
s.stroke([(0.732,0.572),(0.782,0.614),(0.816,0.650)], "round_hard", "leaf_lt",
         size=0.009, pressure=[0.7,1.0,0.3])
s.stroke([(0.556,0.636),(0.586,0.672)], "round_hard", p.mix(p["leaf_lt"],"leaf_md",0.4),
         size=0.006, pressure=[0.6,0.2])

# stems out of the pot into the flowers
s.stroke([(0.424,0.700),(0.428,0.668),(0.420,0.640)], "round_hard", "stem",
         size=0.008, pressure=[0.5,1.0,0.6])
s.stroke([(0.452,0.700),(0.478,0.664),(0.512,0.628)], "round_hard", "stem",
         size=0.007, pressure=[0.4,1.0,0.5])
s.stroke([(0.396,0.696),(0.386,0.664),(0.392,0.638)], "round_hard",
         p.mix(p["stem"], "burnt_umber", 0.35), size=0.006, pressure=[0.4,0.9,0.4])

print("strokes:", s.stroke_count)
print(s.look(sketch=False))
