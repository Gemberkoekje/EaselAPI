# Pass 14 - the foliage was turquoise and it buried the rim. Both back.
p = s.palette
p["leaf_dk"] = p.mix(p.mix("viridian","burnt_umber",0.62), "ultramarine", 0.10)
p["leaf_cl"] = p.mix(p.mix("viridian","burnt_umber",0.48), "ultramarine", 0.30)
p["leaf_md"] = p.mix(p.mix("viridian","yellow_ochre",0.45), "burnt_umber", 0.45)
p["leaf_lt"] = p.mix(p.mix("viridian","yellow_ochre",0.60), "burnt_umber", 0.22)
p["leaf_wm"] = p.mix(p.mix("yellow_ochre","viridian",0.40), "burnt_umber", 0.35)
for k in ("leaf_dk","leaf_cl","leaf_md","leaf_lt","leaf_wm","stem"):
    print(f"{k:8s} {p.hex(p[k])}  v={p.value_of(p[k]):.3f}")
s.dry()

fol = polygon([(0.348,0.596),(0.398,0.566),(0.470,0.558),(0.560,0.566),(0.642,0.582),
               (0.704,0.604),(0.732,0.648),(0.702,0.688),(0.638,0.666),(0.556,0.652),
               (0.478,0.648),(0.410,0.662),(0.364,0.682),(0.336,0.646)])
s.block_in(fol.inset(0.017), "flat", "leaf_dk", direction=(22, 154), density=1.0,
           size=0.034, load=1.0, pressure="even")
s.block_in(blob(Region(0.400,0.578,0.560,0.638), wobble=0.42, seed=21), "bristle",
           "leaf_md", direction=(28, 132), density=0.7, size=0.020, load=0.7)
s.block_in(blob(Region(0.578,0.592,0.700,0.652), wobble=0.45, seed=8), "bristle",
           "leaf_cl", direction=(41, 118), density=0.65, size=0.018, load=0.65)
# holes: the dark behind, showing between leaves
for a, b, sz in ([(0.436,0.612),(0.466,0.596)], 0.0, 0.013), ([(0.596,0.618),(0.628,0.634)], 0.0, 0.011), \
                ([(0.522,0.588),(0.548,0.600)], 0.0, 0.010):
    s.stroke(a, "bristle", "bg", size=sz, pressure="taper", load=0.7)

# the leaves again, muted; only two of them catch anything
leaves = [
    (ribbon([(0.334,0.548),(0.284,0.578),(0.230,0.630)], 0.046, 0.007), "leaf_md", 0.022),
    (ribbon([(0.348,0.598),(0.302,0.640),(0.268,0.684)], 0.040, 0.006), "leaf_dk", 0.020),
    (ribbon([(0.724,0.564),(0.780,0.610),(0.830,0.666)], 0.050, 0.008), "leaf_wm", 0.024),
    (ribbon([(0.700,0.614),(0.744,0.664),(0.758,0.708)], 0.038, 0.006), "leaf_dk", 0.019),
    (ribbon([(0.548,0.628),(0.590,0.674),(0.588,0.714)], 0.042, 0.008), "leaf_md", 0.021),
    (ribbon([(0.474,0.638),(0.452,0.686),(0.472,0.718)], 0.034, 0.006), "leaf_dk", 0.017),
    (ribbon([(0.592,0.396),(0.650,0.368),(0.708,0.382)], 0.034, 0.006), "leaf_dk", 0.017),
    (ribbon([(0.318,0.500),(0.286,0.462),(0.268,0.416)], 0.030, 0.005), "leaf_dk", 0.015),
]
for shp, col, sz in leaves:
    s.block_in(shp.inset(sz * 0.5), "bristle", col, direction="axis", density=0.95,
               size=sz, load=0.95)
s.stroke([(0.330,0.552),(0.288,0.578),(0.246,0.616)], "round_hard", "leaf_lt",
         size=0.007, pressure=[0.7,0.4,0.15])
s.stroke([(0.734,0.574),(0.784,0.616),(0.814,0.648)], "round_hard", "leaf_lt",
         size=0.008, pressure=[0.6,0.9,0.25])

# --- the near rim goes back in front of the foliage ---------------------------
s.stroke([(0.322,0.668),(0.366,0.692),(0.418,0.698),(0.470,0.692),(0.512,0.670)],
         "flat", p.mix(p["terra_mid"], p["terra_hi"], 0.66), size=0.017,
         pressure="even", load=1.0)
s.stroke([(0.330,0.666),(0.376,0.688),(0.422,0.694)], "round_hard", "terra_hi",
         size=0.006, pressure=[0.45,1.0,0.25])
s.stroke([(0.340,0.686),(0.392,0.708),(0.446,0.712),(0.494,0.700)], "round_hard",
         "terra_sh", size=0.006, pressure=[0.3,0.9,0.9,0.35])
s.stroke([(0.318,0.664),(0.340,0.676)], "round_hard", "terra_sh", size=0.007,
         pressure=[0.7,0.3])
# stems out through the rim
s.stroke([(0.428,0.694),(0.432,0.666),(0.424,0.640)], "round_hard", "stem",
         size=0.007, pressure=[0.5,1.0,0.5])
s.stroke([(0.458,0.696),(0.482,0.664),(0.510,0.632)], "round_hard", "stem",
         size=0.006, pressure=[0.4,0.9,0.4])

print("strokes:", s.stroke_count)
print(s.look(sketch=False))
