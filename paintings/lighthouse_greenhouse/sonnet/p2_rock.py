# Pass 2: the rock the tower stands on, in front of the fog, behind the tower.
# A mass built of planes, not a mass with marks on it: the block-in's dark left
# showing as shadow, a narrow uneven strip under the ridge taking the fog's
# cool light, a face turned up toward the glow taking its warmth, and the mid
# bulk between -- each a shape tiling part of the whole, at full opacity and
# even pressure so they read as planes and not as passes. Crevices and a
# little dry brush last.
def rock_top_strip():
    return polygon([(-0.06, 0.815), (0.07, 0.784), (0.15, 0.795), (0.21, 0.766),
                    (0.29, 0.758), (0.345, 0.708), (0.40, 0.690), (0.465, 0.700),
                    (0.52, 0.688), (0.565, 0.706), (0.615, 0.752), (0.685, 0.765),
                    (0.765, 0.793), (0.86, 0.784), (1.06, 0.815), (1.06, 0.845),
                    (0.86, 0.814), (0.765, 0.823), (0.685, 0.795), (0.615, 0.782),
                    (0.565, 0.736), (0.52, 0.718), (0.465, 0.730), (0.40, 0.720),
                    (0.345, 0.738), (0.29, 0.788), (0.21, 0.796), (0.15, 0.825),
                    (0.07, 0.814), (-0.06, 0.845)])

def rock_lit_face():   # turned up toward the glow and the beam
    return polygon([(0.565, 0.706), (0.615, 0.752), (0.685, 0.765), (0.765, 0.793),
                    (0.83, 0.805), (0.80, 0.835), (0.73, 0.818), (0.66, 0.80),
                    (0.60, 0.772), (0.565, 0.740)])

def rock_mid_bulk():
    return polygon([(-0.06, 0.865), (0.10, 0.845), (0.25, 0.835), (0.40, 0.805),
                    (0.55, 0.795), (0.70, 0.835), (0.90, 0.855), (1.06, 0.875),
                    (1.06, 1.06), (-0.06, 1.06)])

s.block_in(rock(), "flat", "rock", size=0.09, density=1.0, solid=True,
           direction="axis", edge="clean", note="rock mass")
s.block_in(rock_mid_bulk(), "flat", "rock_mid", size=0.05, density=1.0, solid=True,
           direction="axis", opacity=1.0, pressure="even", note="mid bulk")
s.block_in(rock_top_strip(), "flat", "rock_cool", size=0.018, density=1.0, solid=True,
           direction="axis", opacity=1.0, pressure="even", note="top strip, cool")
s.block_in(rock_lit_face(), "flat", "rock_warm", size=0.02, density=1.0, solid=True,
           direction="axis", opacity=1.0, pressure="even", note="lit face, warm")
s.stroke([(0.395, 0.700), (0.415, 0.730), (0.435, 0.762), (0.455, 0.80)], "round_hard",
         "rock_deep", size=0.008, opacity=0.9, pressure="taper", note="crevice, under the tower")
s.stroke([(0.165, 0.768), (0.205, 0.789), (0.245, 0.805), (0.29, 0.828)], "round_hard",
         "rock_deep", size=0.007, opacity=0.85, pressure="lift_off", note="crevice, left")
s.stroke([(0.665, 0.762), (0.70, 0.782), (0.735, 0.808)], "round_hard", "rock_deep",
         size=0.0065, opacity=0.8, pressure="taper", note="crevice, right")
s.stroke([(0.10, 0.80), (0.22, 0.82)], "bristle", "rock_mid", size=0.028, load=0.35,
         opacity=0.55, pressure="taper", note="dry brush")
s.stroke([(0.62, 0.79), (0.73, 0.815)], "bristle", "rock_warm", size=0.024, load=0.3,
         opacity=0.5, pressure="taper", note="dry brush, lit side")
print(s.look(values=True))
print(s.look())
