# The bloom. Light through a soaped windscreen is not a clean radial fall-off, it is
# a patch broken up by the soap -- so it is scumbled across, not radiated from a centre,
# and its outer value sits a tenth above the tunnel so that edge is lost.
print("scumble costs:", s.cost({"shape": glow(), "size": 0.05}))
s.scumble(glow(), "cyan_lo", "cyan_hi", 9)

# Nothing is added on top of it here. Three rehearsals showed that any clean round
# mark laid on this scumble reads as a sticker whatever its value; the bright core and
# the water belong with the rest of the glass marks, so they are laid with them.

# The stop light: a sideways smear through the soap, its core off the middle of it.
s.stroke([(0.541, 0.343), (0.620, 0.331)], "round_soft", "hot",
         size=0.030, opacity=0.45, pressure="swell")
s.dab(0.572, 0.337, "round_hard", "hot_core", size=0.016, press=3)
print(s.look())
