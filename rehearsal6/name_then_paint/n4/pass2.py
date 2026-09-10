exec(open("_pal.py").read())
exec(open("_geom.py").read())
s.dry()

# --- the wall again, flat and crossed instead of a bristle comb -------------
s.block_in(WALL, "flat", "wall", direction=(104, 18), density=1.0,
           size=0.135, pressure="even", load=1.0, load_falloff=0.2)
s.block_in(polygon([(0.548,0.03),(0.712,0.0),(0.735,0.63),(0.552,0.618)]),
           "flat", "wall_lit", direction=(94, 170), density=0.7, size=0.075,
           pressure="even", load=0.5)
s.block_in(polygon([(0.840,0.0),(1.0,0.0),(1.0,0.34),(0.885,0.46)]),
           "flat", "wall_dk", direction=(112, 24), density=0.65, size=0.085,
           pressure="even", load=0.5)
s.block_in(polygon([(0.60,0.50),(1.0,0.55),(1.0,0.665),(0.585,0.63)]),
           "flat", "wall_dk", direction=(8,), density=0.6, size=0.055,
           pressure="even", load=0.45)

# --- the glass again -------------------------------------------------------
s.block_in(GLASS, "flat", "glass", direction=(98, 12), density=1.0,
           size=0.15, pressure="even", load=1.0, load_falloff=0.2)
s.block_in(HOT.inset(0.035), "flat", "glass_hot", direction=(118, 30), density=0.7,
           size=0.09, pressure="even", load=0.55)
# something vague outside, low in the pane
s.block_in(blob((0.150,0.470), 0.180, 0.135, wobble=0.35, seed=9).inset(0.03),
           "flat", "glass_low", direction=(6, 82), density=0.6, size=0.07,
           pressure="even", load=0.5)
s.block_in(blob((0.310,0.520), 0.120, 0.090, wobble=0.4, seed=12).inset(0.025),
           "flat", "glass_far", direction=(14,), density=0.5, size=0.055,
           pressure="even", load=0.45)
print(s.stroke_count)
print(s.look())
