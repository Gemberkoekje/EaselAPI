# Pass 3: the headland, in front of the sea and the sky, behind the tower. A solid
# dark mass with a clean, jagged silhouette, and then its planes -- not marks on
# it, but the three planes it is made of, each a shape that tiles part of the
# mass: a narrow, uneven strip under the ridge that faces the sky and takes its
# cool light, a seaward face that looks right toward the glow and takes the warm
# one, and a mid bulk between; the dark of the block-in is what is left in shadow.
# The planes are laid at full opacity with even pressure so that they are planes
# and not stacks of passes, and kept a brush's half-width inside the silhouette so
# nothing fringes past it. Crevices and a little dry brush last.
# Earlier versions laid the planes as facets -- slabs, then bristle streaks --
# and both came back as things stuck on a smooth hull.
p["rock_cool"] = p.at_value(p.mix("rock", "sky_mid", 0.5), 0.26)
p["rock_warm"] = p.at_value(p.mix("rock_lit", "rock", 0.3), 0.29)
p["rock_mid2"] = p.at_value(p.mix("rock", "burnt_sienna", 0.35), 0.21)
p["rock_deep"] = p.at_value("rock", 0.14)

def top_strip():    # the ridge, seen at a low angle: an uneven strip under it
    return polygon([(-0.05, 0.556), (0.03, 0.547), (0.08, 0.569), (0.13, 0.564),
                    (0.19, 0.598), (0.23, 0.604), (0.29, 0.619), (0.34, 0.614),
                    (0.40, 0.648), (0.45, 0.674), (0.475, 0.68),
                    (0.455, 0.695), (0.41, 0.675), (0.37, 0.66), (0.33, 0.632),
                    (0.30, 0.64), (0.25, 0.63), (0.21, 0.618), (0.17, 0.62),
                    (0.12, 0.60), (0.07, 0.605), (0.02, 0.585), (-0.05, 0.58)])

def seaward_face():  # the face that looks right, toward the glow
    return polygon([(0.485, 0.68), (0.515, 0.71), (0.545, 0.752), (0.565, 0.798),
                    (0.60, 0.874), (0.62, 0.94), (0.61, 0.97), (0.565, 0.90),
                    (0.525, 0.82), (0.49, 0.75), (0.46, 0.705)])

def mid_bulk():      # the body between, warmer than the shadow and barely lighter
    return polygon([(0.0, 0.625), (0.14, 0.64), (0.30, 0.675), (0.43, 0.725),
                    (0.47, 0.78), (0.40, 0.86), (0.20, 0.80), (0.05, 0.74),
                    (-0.03, 0.70)])

s.block_in(headland(), "flat", "rock", size=0.08, density=1.0, solid=True,
           direction="axis", edge="clean", note="headland")
s.block_in(mid_bulk(), "flat", "rock_mid2", size=0.05, density=1.0, solid=True,
           direction="axis", opacity=1.0, pressure="even", note="mid bulk")
s.block_in(top_strip(), "flat", "rock_cool", size=0.018, density=1.0, solid=True,
           direction="axis", opacity=1.0, pressure="even", note="top strip, cool")
s.block_in(seaward_face(), "flat", "rock_warm", size=0.02, density=1.0, solid=True,
           direction="axis", opacity=1.0, pressure="even", note="seaward face, warm")
s.stroke([(0.27, 0.665), (0.32, 0.705), (0.40, 0.765)], "round_hard", "rock_deep", size=0.014,
         opacity=0.9, pressure="taper", note="crevice")
s.stroke([(0.465, 0.725), (0.495, 0.79), (0.515, 0.86)], "round_hard", "rock_deep", size=0.012,
         opacity=0.9, pressure="taper", note="crevice, seaward")
s.stroke([(-0.02, 0.625), (0.08, 0.645)], "round_hard", "rock_deep", size=0.014,
         opacity=0.8, pressure="lift_off", note="crevice, left")
# dry brush: a few broken marks so the planes have a surface
s.stroke([(0.06, 0.66), (0.20, 0.70)], "bristle", "rock_cool", size=0.03, load=0.35,
         opacity=0.6, pressure="taper", note="dry brush")
s.stroke([(0.24, 0.74), (0.36, 0.80)], "bristle", "rock_warm", size=0.025, load=0.3,
         opacity=0.5, pressure="taper", note="dry brush")
s.stroke([(0.50, 0.80), (0.56, 0.88)], "bristle", "rock_mid2", size=0.02, load=0.35,
         opacity=0.6, pressure="taper", note="dry brush, seaward")
print(s.look(values=True))
print(s.look())
