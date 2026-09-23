# Edges, last but one. Attention belongs at the lamp; the lower-right corner, where rock
# meets dark water, is where the eye should be let go -- so that boundary is lost in
# places, with starved marks at a value between the two, laid across it, no two alike.
# One more across the join of the two rock faces; the tower seated in its grass.
p["rock_sea"] = p.at_value(p.mix("land", "sea_near", 0.5), 0.22)
p["face_join"] = p.mix("lit_dim", "cliff", 0.5)
s.stroke([(0.688, 0.840), (0.711, 0.823), (0.737, 0.816)], "bristle", "rock_sea",
         size=0.030, load=0.55, opacity=0.5, pressure="swell")
s.stroke([(0.786, 0.957), (0.812, 0.939), (0.841, 0.934)], "bristle", "rock_sea",
         size=0.036, load=0.5, opacity=0.45, pressure="taper")
s.stroke([(0.818, 1.012), (0.846, 0.987), (0.880, 0.980)], "bristle", "rock_sea",
         size=0.042, load=0.45, opacity=0.5, pressure="swell")
s.stroke([(0.566, 0.604), (0.583, 0.589), (0.602, 0.583)], "bristle", "face_join",
         size=0.022, load=0.5, opacity=0.5, pressure="swell", clip=headland)
s.stroke([(TX - 0.030, 0.5445), (TX - 0.004, 0.5405), (TX + 0.031, 0.5425)], "bristle",
         "grass", size=0.011, load=0.55, opacity=0.65, pressure="swell")
s.dry()
