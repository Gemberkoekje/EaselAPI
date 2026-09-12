# Pass 6. The last of the hollow thing's three depths: the near edge. Nothing here
# is a new idea -- it is the mass that makes the lit field an opening, and every
# member of it is a stroke rather than a block-in, because a thing much longer than
# it is wide is a stroke and block_in would comb it.
s.dry()

# A window frame is the one or two things in a picture that really are ruled, and
# these members are 0.009-0.021 wide, where the default jitter of 0.02 wanders
# further than the member is thick: the first rehearsal beaded every one of them
# into a chain of separate blocks. So jitter and size_jitter both go to zero, which
# is the ruled-line recipe, and the ends run off past the joints so none of them
# terminates inside the picture.
FR = dict(load=1.0, load_falloff=0.0, opacity=1.0, pressure="even",
          jitter=0.0, size_jitter=0.0)

# Head and sill. The sill is the heavier of the two, as a sill is, and both run past
# the jambs so neither has a termination inside the picture.
s.stroke([(0.156, 0.3375), (0.450, 0.3305), (0.730, 0.3345)], "flat", "frame",
         size=0.014, note="subject frame", **FR)
s.stroke([(0.154, 0.6085), (0.450, 0.6125), (0.732, 0.6085)], "flat", "frame",
         size=0.021, note="subject frame", **FR)

# The jambs, at slightly different widths because two members of a frame are not
# the same member twice.
s.stroke([(0.1735, 0.324), (0.1725, 0.470), (0.1745, 0.618)], "flat", "frame",
         size=0.013, note="subject frame", **FR)
s.stroke([(0.7185, 0.322), (0.7195, 0.470), (0.7175, 0.620)], "flat", "frame",
         size=0.011, note="subject frame", **FR)

# Two mullions, unevenly spaced -- 0.164, 0.212 and 0.171 between the four
# verticals, so the eye cannot find a rhythm in them. The right one is thinner and
# is allowed to be eaten by the bloom at the top, which is both what happens to a
# thin dark bar in front of a bright light and the picture's one properly lost edge.
s.stroke([(0.3365, 0.338), (0.3355, 0.475), (0.3370, 0.611)], "flat", "frame",
         size=0.011, note="subject frame", **FR)
s.stroke([(0.5485, 0.344), (0.5475, 0.470), (0.5490, 0.609)], "flat", "frame",
         size=0.0085, jitter=0.0, size_jitter=0.0, load=1.0, load_falloff=0.0,
         opacity=1.0, pressure=[0.10, 0.75, 1.0], note="subject frame")

# The door's frame, and the push bar across its glass -- the one mark that says
# this is a door somebody comes out of.
s.stroke([(0.7805, 0.326), (0.7815, 0.520), (0.7808, 0.702)], "flat", "frame",
         size=0.011, note="subject door frame", **FR)
s.stroke([(0.8965, 0.328), (0.8955, 0.520), (0.8962, 0.702)], "flat", "frame",
         size=0.010, note="subject door frame", **FR)
s.stroke([(0.774, 0.3315), (0.838, 0.3300), (0.902, 0.3345)], "flat", "frame",
         size=0.012, note="subject door frame", **FR)
s.stroke([(0.776, 0.5585), (0.838, 0.5600), (0.900, 0.5575)], "flat", "frame",
         size=0.009, note="subject door frame", **FR)
s.stroke([(0.788, 0.4685), (0.840, 0.4670), (0.891, 0.4690)], "round_hard",
         p.at_value("mach_hi", 0.640), size=0.0055, opacity=0.9, load=1.0,
         load_falloff=0.0, pressure=[0.25, 1.0, 0.30], note="subject door bar")
print(s.budget_line())
