# Pass 13. The last few marks, and they go to the picture rather than to the
# surroundings -- passes 11 and 12 were both surroundings and took the subject's
# share of the budget from 45% down to 40%, which is under what was planned.
#
# Cropping into the window showed the real fault: the run of machines is one
# continuous plane with four discs on it, so it reads as a counter rather than as
# separate machines. Two joints are what it wants, and they are information rather
# than decoration.
s.dry()

# Two joints between machines. The third falls behind the left mullion, which is why
# there are two -- and one is clearer than the other, because a joint in shadow and
# a joint in light are not the same mark.
s.stroke([(0.2668, 0.5210), (0.2660, 0.5620), (0.2672, 0.6015)], "round_hard",
         p.at_value("mach_dk", 0.395), size=0.0050, opacity=0.80, load=1.0,
         load_falloff=0.0, pressure=[0.3, 1.0, 0.55], note="subject machines")
s.stroke([(0.4362, 0.5190), (0.4372, 0.5600), (0.4358, 0.6005)], "round_hard",
         p.at_value("mach_dk", 0.445), size=0.0040, opacity=0.60, load=1.0,
         load_falloff=0.0, pressure=[0.2, 0.9, 0.35], note="subject machines")

# An opening through to the back of the shop was rehearsed here and thrown away.
# Cropped in, it read as a pale slab with hard edges floating on the wall rather
# than as a hole in it, and with nine incidents already in this picture a tenth that
# does not read is clutter. The plainness of this bay is not a fault -- it is the
# quiet that lets the machines and the figure carry the window.
# the corner where the right bay's wall turns, so that bay has a depth too
s.stroke([(0.6960, 0.3660), (0.6985, 0.4400), (0.6955, 0.5040)], "bristle",
         p.at_value("wall_lo", 0.700), size=0.020, load=0.85, opacity=0.40,
         pressure="swell", note="subject interior")

# Folded laundry on the table: the brightest thing inside after the tubes, and the
# one mark in the shop that says somebody has been working in here.
s.stroke([(0.6720, 0.5055), (0.7085, 0.5035)], "flat",
         p.at_value("interior", 0.865), size=0.017, load=1.0, load_falloff=0.0,
         opacity=0.95, pressure="even", note="subject table")
s.stroke([(0.6740, 0.5140), (0.7080, 0.5120)], "round_hard",
         p.at_value("machine", 0.555), size=0.0040, opacity=0.75, load=1.0,
         load_falloff=0.0, pressure=[0.3, 1.0, 0.3], note="subject table")

# A card taped inside the glass. Lit from behind, so it is a silhouette rather than
# a white notice -- which is the thing a painter gets backwards about a shop window.
s.stroke([(0.2030, 0.4165), (0.2425, 0.4140)], "flat",
         p.at_value("wall_lo", 0.575), size=0.021, load=1.0, load_falloff=0.0,
         opacity=0.90, pressure="even", jitter=0.004, note="subject notice")
print(s.budget_line())
