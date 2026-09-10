# Pass 15 - reset the green haze; a compact dark foliage instead.
p = s.palette
s.dry()

# --- clear everything the green touched ---------------------------------------
s.block_in(polygon([(0.225,0.395),(0.865,0.375),(0.865,0.628),(0.225,0.594)]), "flat",
           "bg", direction=(36, 126), density=1.0, size=0.055, load=1.0, pressure="even")
s.block_in(polygon([(0.225,0.596),(0.322,0.604),(0.322,0.706),(0.225,0.700)]), "flat",
           "tbl", direction=(7, 167), density=1.0, size=0.030, load=1.0, pressure="even")
s.block_in(polygon([(0.516,0.610),(0.865,0.632),(0.865,0.742),(0.516,0.716)]), "flat",
           "tbl", direction=(6, 168), density=1.0, size=0.032, load=1.0, pressure="even")
s.block_in(polygon([(0.520,0.700),(0.780,0.708),(0.865,0.714),(0.865,0.780),(0.620,0.766),(0.512,0.732)]),
           "flat", "tbl_far", direction=(11, 152), density=1.0, size=0.030, load=1.0, pressure="even")

# --- a compact, dark foliage --------------------------------------------------
fol = polygon([(0.366,0.600),(0.432,0.572),(0.520,0.566),(0.602,0.582),(0.662,0.606),
               (0.686,0.640),(0.638,0.666),(0.554,0.654),(0.470,0.652),(0.406,0.666),(0.360,0.648)])
s.block_in(fol.inset(0.014), "flat", "leaf_dk", direction=(21, 155), density=1.0,
           size=0.028, load=1.0, pressure="even")
s.block_in(blob(Region(0.402,0.582,0.548,0.636), wobble=0.42, seed=21), "flat",
           "leaf_md", direction=(30, 130), density=1.0, size=0.020, load=1.0, pressure="even")
s.block_in(blob(Region(0.572,0.596,0.660,0.646), wobble=0.45, seed=8), "flat",
           "leaf_cl", direction=(44, 116), density=1.0, size=0.017, load=1.0, pressure="even")

for shp, col, sz in (
        (ribbon([(0.352,0.596),(0.306,0.638),(0.272,0.684)], 0.038, 0.006), "leaf_dk", 0.018),
        (ribbon([(0.664,0.618),(0.706,0.660),(0.722,0.700)], 0.040, 0.006), "leaf_md", 0.019),
        (ribbon([(0.478,0.640),(0.456,0.684),(0.474,0.714)], 0.032, 0.006), "leaf_dk", 0.016),
        (ribbon([(0.560,0.630),(0.596,0.672),(0.592,0.708)], 0.036, 0.007), "leaf_dk", 0.018)):
    s.block_in(shp.inset(sz * 0.5), "flat", col, direction="axis", density=1.0,
               size=sz, load=1.0, pressure="even")
s.stroke([(0.350,0.602),(0.312,0.640),(0.282,0.672)], "round_hard", "leaf_lt",
         size=0.006, pressure=[0.6,0.35,0.12])
s.stroke([(0.670,0.626),(0.704,0.662)], "round_hard", "leaf_lt",
         size=0.006, pressure=[0.55,0.18])

# --- the rim, in front of all of it -------------------------------------------
s.stroke([(0.320,0.662),(0.362,0.646),(0.418,0.640),(0.474,0.646),(0.516,0.664)],
         "flat", p.mix(p["terra_mid"], p["terra_hi"], 0.50), size=0.014,
         pressure="even", load=1.0)
s.stroke([(0.334,0.652),(0.400,0.646),(0.462,0.652)], "round_hard", "pot_in",
         size=0.008, pressure=[0.4,0.9,0.4])
s.stroke([(0.322,0.668),(0.366,0.692),(0.418,0.698),(0.470,0.692),(0.512,0.670)],
         "flat", p.mix(p["terra_mid"], p["terra_hi"], 0.66), size=0.017,
         pressure="even", load=1.0)
s.stroke([(0.330,0.666),(0.376,0.688),(0.422,0.694)], "round_hard", "terra_hi",
         size=0.006, pressure=[0.45,1.0,0.25])
s.stroke([(0.340,0.686),(0.392,0.708),(0.446,0.712),(0.494,0.700)], "round_hard",
         "terra_sh", size=0.006, pressure=[0.3,0.9,0.9,0.35])
s.stroke([(0.428,0.694),(0.432,0.666),(0.424,0.642)], "round_hard", "stem",
         size=0.007, pressure=[0.5,1.0,0.5])
s.stroke([(0.458,0.696),(0.482,0.666),(0.508,0.638)], "round_hard", "stem",
         size=0.006, pressure=[0.4,0.9,0.4])

print("strokes:", s.stroke_count)
print(s.look(sketch=False))
print(s.look(region=span("C4","G7"), sketch=False))
