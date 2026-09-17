# Pass 12: the rock, named as the passage I would apologise for: a plain dark
# mass with a scratch for a crevice, and a boulder at the tower's foot that
# reads as a striped dome. One more plane on the hump's left slope, facing the
# beam's side of the sky; three dry-brush marks across the front face so it
# has a surface; the crevice widened at its top where two facets meet; and
# the boulder broken with a dark crack across it and a starved stroke over its
# top so it stops being a dome.
p["rock_face"] = p.at_value(p.mix("rock", "fog", 0.25), 0.22)
s.block_in(polygon([(0.80, 0.85), (0.86, 0.812), (0.90, 0.83), (0.87, 0.88), (0.82, 0.90)]),
           "flat", "rock_face", size=0.02, density=1.0, solid=True, direction=-35,
           opacity=1.0, pressure="even", note="hump, left facet")
s.stroke([(0.55, 0.95), (0.63, 0.965), (0.70, 0.955)], "bristle", "rock_cool", size=0.03, load=0.3,
         opacity=0.5, pressure="swell", note="dry brush, front face")
s.stroke([(0.74, 0.985), (0.84, 1.0)], "bristle", "rock_lit", size=0.026, load=0.3,
         opacity=0.45, pressure="taper", note="dry brush, front face, warm")
s.stroke([(0.93, 0.90), (1.0, 0.925), (1.05, 0.915)], "bristle", "rock_top", size=0.024, load=0.3,
         opacity=0.45, pressure="swell", note="dry brush, hump")
s.stroke([(0.775, 0.855), (0.795, 0.875), (0.805, 0.905)], "round_hard", "rock_deep", size=0.014,
         opacity=0.85, pressure="lift_off", note="crevice, widened at the top")
s.stroke([(TX + 0.005, 0.90), (TX + 0.035, 0.915), (TX + 0.06, 0.94)], "round_hard", "rock_deep",
         size=0.007, opacity=0.85, pressure="swell", note="crack across the boulder")
s.stroke([(TX - 0.005, 0.89), (TX + 0.03, 0.882), (TX + 0.065, 0.895)], "bristle", "rock_top",
         size=0.018, load=0.3, opacity=0.5, pressure="taper", note="dry brush over the boulder")
print(s.look(values=True))
print(s.look())
print(s.look(region="D6:H8"))
