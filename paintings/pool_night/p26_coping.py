s.dry()
# The near coping is the longest edge in the picture and was one even value down its
# whole length. Darkened at both ends, brightest opposite the lit water, and one mark
# run out across its outer edge so it is not a ruled strip.
s.glaze([(0.605, 1.030), (0.675, 0.955), (0.750, 0.888)], p.at_value("deck", 0.34),
        opacity=0.38, size=0.075, pressure="swell")
s.glaze([(0.885, 0.735), (0.945, 0.672), (0.995, 0.625)], p.at_value("deck", 0.36),
        opacity=0.32, size=0.060, pressure="taper")
s.stroke([(0.745, 0.872), (0.805, 0.805), (0.862, 0.742)], "bristle",
         p.at_value("deck", 0.56), size=0.030, load=0.40, opacity=0.55,
         load_falloff=0.45, pressure="swell")
s.stroke([(0.800, 0.856), (0.870, 0.892)], "bristle", p.at_value("deck", 0.36),
         size=0.034, load=0.45, opacity=0.45, load_falloff=0.4, pressure="taper")
print(s.look(region="E6:H8"))
