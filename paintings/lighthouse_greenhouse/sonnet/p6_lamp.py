# Pass 6: the lamp room -- the whole reason for the picture -- on the tower,
# before the tendrils that climb toward it. The halo first: light in the air
# belongs to the air, so it goes down before the frame that contains it, same
# as PAINTER.md's own worked example -- except this glow is picking up green
# on its way through the leaves, so it is mixed from "leaf_beam", not gold.
# Then the frame: gallery, glass, roof. The glass is not a flat colour, it is
# the vine mass the brief asks for -- planes of leaf colour tiling the pane
# the way a rock face is planes and not marks (PAINTING.md, "A mass built of
# planes"), with the mullions painted *last*, on top of the packed green, so
# the frame still reads as a frame over what has outgrown it. A few tendrils
# spill past the roof and the gallery; the rest of the mass stays inside the
# glass, because this is a lighthouse only *starting* to be a greenhouse.
s.glaze([(0.36, 0.11), (0.435, 0.095), (0.51, 0.115)], "beam_far", opacity=0.22,
        size=0.10, pressure="swell", note="halo, wide")
s.glaze([(0.41, 0.10), (0.46, 0.105)], "beam", opacity=0.20, size=0.05,
        pressure="swell", note="halo, close")

s.stroke(gallery(), "flat", "iron", size=0.013, opacity=0.95, load=1.0,
         load_falloff=0.0, jitter=0.0, pressure="even", note="gallery plate")

s.block_in(lantern(), "flat", "leaf_dark", size=0.010, density=1.0, solid=True,
           direction=90, opacity=1.0, pressure="even", note="glass, packed with vines")
s.stroke([(0.408, 0.112), (0.420, 0.086), (0.436, 0.082)], "round_hard", "leaf_mid",
         size=0.020, opacity=0.9, load=0.8, pressure="swell", note="foliage clump, left")
s.stroke([(0.438, 0.114), (0.452, 0.090), (0.463, 0.084)], "round_hard", "leaf_lit",
         size=0.017, opacity=0.9, load=0.8, pressure="swell", note="foliage clump, right, lit")
s.dab(0.444, 0.100, "round_hard", "leaf_beam", size=0.012, press=2, note="foliage, backlit")
s.dab(0.424, 0.104, "round_hard", "tomato", size=0.008, press=2, note="a tomato against the glass")

s.block_in(roof(), "flat", "iron", size=0.011, density=1.0, solid=True,
           direction="axis", note="roof")
for x in (0.415, 0.435, 0.455):
    s.stroke([(x, 0.081), (x, 0.117)], "liner", "iron", size=0.004, opacity=0.9,
              pressure="even", note="mullion")
s.stroke([(0.398, 0.118), (0.472, 0.118)], "flat", "iron", size=0.010, opacity=0.95,
         load=1.0, load_falloff=0.0, jitter=0.0, pressure="even", note="glass sill")

# vines spilling past the frame -- the conversion is still in progress, so only
# a little escapes
s.stroke([(0.448, 0.083), (0.458, 0.062), (0.452, 0.045)], "round_hard", "leaf_mid",
         size=0.010, load=0.85, opacity=0.85, pressure="taper", note="tendril, over the roof")
s.stroke([(0.400, 0.118), (0.386, 0.145), (0.390, 0.178)], "round_hard", "leaf_dark",
         size=0.011, load=0.8, opacity=0.8, pressure="taper", note="tendril, down from the gallery")
s.dab(0.454, 0.040, "round_hard", "leaf_lit", size=0.007, press=2, note="leaf, over the roof")

# climbing tendrils on the tower body, bridging the stairs to the lamp room --
# sparse, because this is meant to look recent. round_hard, not bristle: a
# bristle mark below about size 0.025 is a comb of gapped ticks, not a line,
# and these vines are thinner than that.
s.stroke([(0.435, 0.60), (0.428, 0.50), (0.433, 0.40), (0.424, 0.30), (0.430, 0.20)],
         "round_hard", "leaf_mid", size=0.009, load=0.85, opacity=0.85, pressure="taper",
         note="tendril climbing, main")
s.stroke([(0.478, 0.46), (0.472, 0.38), (0.477, 0.30)], "round_hard", "leaf_mid", size=0.007,
         load=0.8, opacity=0.75, pressure="taper", note="tendril climbing, shorter")
for x, y in [(0.430, 0.52), (0.426, 0.36), (0.475, 0.40), (0.432, 0.23)]:
    s.dab(x, y, "round_hard", "leaf_mid", size=0.006, press=1, note="leaf on the vine")
print(s.look(values=True))
print(s.look())
print(s.look(region="C1:F3"))
