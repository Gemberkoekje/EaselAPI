# Eight marks, and two of them are repairs of the kind the closing checklist
# asks about: the surf along the rock came back as a pale scalloped line running
# the whole width of it, which is an outline round a painted shape, and the last
# plane on the rock read as a smooth slab again.
s.dry()

# Break the line, so the water's edge is found in two places and absent between.
for path, v, size in (([(0.545, 0.876), (0.608, 0.892)], 0.190, 0.016),
                      ([(0.700, 0.916), (0.762, 0.944)], 0.175, 0.014)):
    s.stroke(path, "bristle", p.at_value("rock", v), size=size, load=0.8,
             opacity=0.9, pressure="swell", note="edges")

# Break the slab, at an angle it does not have.
for path, v, size, load, op in (
        ([(0.58, 0.958), (0.74, 0.928), (0.88, 0.952)], 0.205, 0.020, 0.35, 0.55),
        ([(0.82, 0.998), (1.02, 0.960)], 0.185, 0.016, 0.40, 0.6)):
    s.stroke(path, "bristle", p.at_value("rock", v), size=size, load=load,
             opacity=op, pressure="lift_off", note="rock")

# Rust off the gallery ironwork, running down the whitewash. Warm, where every
# other stain on this tower is green, and that is the only reason for it.
s.stroke([(0.2865, 0.290), (0.2920, 0.352)], "bristle",
         p.at_value(p.mix("pot", "stain", 0.5), 0.325), size=0.007, load=0.5,
         opacity=0.6, pressure=[1.0, 0.5, 0.0], note="subject tower")
s.stroke([(0.2215, 0.278), (0.2180, 0.318)], "bristle",
         p.at_value(p.mix("pot", "stain", 0.5), 0.295), size=0.005, load=0.45,
         opacity=0.45, pressure="lift_off", note="subject tower")

# One clump at the left of the vine mass, which was reading as a single dark lump
# with light only on its right.
s.stroke([(0.1815, 0.172), (0.1985, 0.165)], "bristle",
         p.at_value("leaf_mid", 0.300), size=0.014, load=0.8, opacity=0.85,
         pressure="swell", note="subject lantern")

# And the last mark on the picture: the light on the rim of the nearest pot.
# One, because every highlight added makes the others count for less.
s.dab(0.3275, 0.7545, "round_hard", p.at_value("pot_lit", 0.66), size=0.006,
      press=3, tip_wobble=0.35, note="subject pot")

print(s.look())
print(s.look(values=True))
