exec(open("_pal.py").read())
exec(open("_geom.py").read())
p["wall_edge"] = at(p.mix(_warmgrey, "ultramarine", 0.30), 0.355)
p["sill_mid"]  = at(p.mix(_warmgrey, "yellow_ochre", 0.40), 0.55)
s.dry()

# knock the right-hand bar back into the wall
s.block_in(polygon([(0.905,0.0),(1.0,0.0),(1.0,0.668),(0.918,0.652)]).inset(0.012),
           "flat", "wall_edge", direction=(93,), density=1.0, size=0.030,
           pressure="even", load=1.0)
s.smudge([(0.912, 0.04), (0.922, 0.34)], size=0.048)
s.smudge([(0.918, 0.30), (0.928, 0.63)], size=0.048)
s.dry()

# --- glazing bars, on the glass and behind everything else ------------------
s.stroke([(0.292, -0.02), (0.286, 0.615)], "flat", "bar", size=0.026,
         pressure="even", load=1.0, note="mullion")
s.stroke([(0.018, 0.298), (0.566, 0.281)], "flat", "bar", size=0.022,
         pressure="even", load=1.0, note="transom")
s.stroke([(0.300, 0.02), (0.295, 0.60)], "liner", "bar_lit", size=0.006,
         pressure=[0.3, 1.0, 0.7, 0.2], load=1.0)
s.stroke([(0.030, 0.290), (0.560, 0.273)], "liner", "bar_lit", size=0.005,
         pressure=[0.2, 0.9, 0.5, 0.9, 0.3], load=1.0)

# --- the right jamb: covers the torn glass/wall join ------------------------
s.block_in(JAMB, "flat", "bar", direction=(90,), density=1.0, size=0.030,
           pressure="even", load=1.0)
s.stroke([(0.556, 0.0), (0.549, 0.618)], "liner", "bar_lit", size=0.007,
         pressure=[0.9, 0.5, 1.0, 0.6], load=1.0, note="lit inner arris")
s.stroke([(0.604, 0.02), (0.598, 0.628)], "liner", "wall_dk", size=0.005,
         pressure=[0.4, 1.0, 0.6], load=1.0)

# --- the sill: nearer than the window -------------------------------------
s.block_in(SILL, "flat", "sill_lit", direction=(3, 169), density=0.95,
           size=0.048, pressure="even", load=1.0, load_falloff=0.25)
s.block_in(polygon([(0.44,0.628),(1.0,0.650),(1.0,0.760),(0.46,0.735)]).inset(0.020),
           "flat", "sill_hot", direction=(4, 172), density=0.9, size=0.040,
           pressure="even", load=1.0)
s.block_in(polygon([(0.0,0.612),(0.26,0.618),(0.24,0.752),(0.0,0.748)]).inset(0.018),
           "flat", "sill_mid", direction=(2, 174), density=0.9, size=0.038,
           pressure="even", load=1.0)
s.smudge([(0.255, 0.640), (0.262, 0.740)], size=0.042)
s.smudge([(0.452, 0.648), (0.458, 0.742)], size=0.040)

s.block_in(FACE, "flat", "sill_face", direction=(3, 165), density=1.0,
           size=0.036, pressure="even", load=1.0, load_falloff=0.25)
s.block_in(UNDER, "flat", "under", direction=(2, 100), density=1.0,
           size=0.055, pressure="even", load=1.0, load_falloff=0.25)
print(s.stroke_count)
print(s.look())
