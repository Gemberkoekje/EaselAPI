"""Pass 4: the Bell-Warden's masses -- the wing behind, the body in shadow, then the lit planes."""

p["stone_shade"] = p.at_value(p.mix_many(["burnt_umber", "ultramarine", "titanium_white", "yellow_ochre"],
                                          [3, 1.5, 2, 0.5]), 0.28)
p["membrane"] = p.at_value(p.mix("stone_shade", "stone_mid", 0.3), 0.30)
p["membrane_lit"] = p.at_value(p.mix("stone_mid", "stone_shade", 0.3), 0.37)
p["side_c"] = p.at_value(p.mix("stone_mid", "stone_lit", 0.2), 0.40)
p["ridge_c"] = p.at_value(p.mix("stone_lit", "stone_mid", 0.3), 0.52)
p["cheek_c"] = p.at_value(p.mix("stone_mid", "stone_lit", 0.3), 0.42)
p["face_c"] = p.at_value(p.mix("stone_lit", "stone_hi", 0.4), 0.62)

# The lit side of the body as one connected shape: the chest and foreleg's front, up over the
# shoulder and along under the back, down the front of the haunch.
lit_side = polygon([(0.280, 0.455), (0.292, 0.490), (0.300, 0.540), (0.318, 0.600), (0.322, 0.660),
                    (0.318, 0.715), (0.345, 0.715), (0.350, 0.640), (0.345, 0.560), (0.370, 0.475),
                    (0.440, 0.445), (0.520, 0.465), (0.580, 0.505), (0.600, 0.560), (0.575, 0.620),
                    (0.600, 0.600), (0.628, 0.560), (0.635, 0.530), (0.605, 0.480), (0.550, 0.430),
                    (0.490, 0.400), (0.425, 0.380), (0.380, 0.385), (0.345, 0.365), (0.320, 0.400),
                    (0.300, 0.430)], name="lit side")


def lay_wing():
    # Behind the body: the membrane, its upper part catching the light, the bones on it.
    s.block_in(wing, "flat", "membrane", size=0.04, density=1.0, solid=True,
               direction=[(0.43, 0.30), (0.47, 0.12)], edge="hard", note="subject")
    s.block_in(wing_lit, "flat", "membrane_lit", size=0.025, density=1.0, solid=True,
               direction=[(0.43, 0.30), (0.47, 0.12)], edge="hard", opacity=1.0,
               pressure="even", note="subject")
    s.stroke([(0.418, 0.392), (0.432, 0.300), (0.456, 0.200), (0.474, 0.118)], "round_hard",
             "stone_lit", size=0.013, opacity=0.9, load=1.0, load_falloff=0.0,
             pressure=[0.9, 1.0, 0.8, 0.5], note="subject")
    for tip, size, colour, opacity in zip(finger_tips, (0.007, 0.006, 0.0055, 0.005),
                                          ("stone_lit", "stone_mid", "stone_mid", "stone_dark"),
                                          (0.85, 0.8, 0.7, 0.7)):
        s.stroke([wrist, tip], "round_hard", colour, size=size, opacity=opacity, load=1.0,
                 load_falloff=0.0, pressure=[1.0, 0.6, 0.15], smooth=False, note="subject")


def lay_body():
    s.block_in(body, "flat", "stone_shade", size=0.05, density=1.0, solid=True,
               direction="axis", edge="hard", note="subject")
    s.block_in(tail, "flat", "stone_shade", size=0.012, density=1.0, solid=True,
               direction=[(0.632, 0.60), (0.67, 0.75)], edge="hard", note="subject")


def lay_planes():
    # A form that turns: the lit side as one shape on the shadow, then the join, half strength.
    s.block_in(lit_side, "flat", "side_c", size=0.022, density=1.0, solid=True,
               direction="axis", edge="hard", opacity=1.0, pressure="even", note="subject")
    join = p.mix("side_c", "stone_shade", 0.5)
    s.stroke([(0.347, 0.70), (0.349, 0.63), (0.346, 0.56), (0.372, 0.478), (0.44, 0.448),
              (0.52, 0.468), (0.578, 0.508), (0.598, 0.56)], "flat", join, size=0.012,
             opacity=0.6, load=1.0, load_falloff=0.0, pressure="even", note="subject")
    # The head: its cheek a little lit, its top the lightest plane in the picture.
    s.block_in(cheek, "flat", "cheek_c", size=0.016, density=1.0, solid=True,
               direction=[(0.250, 0.395), (0.310, 0.365)], edge="hard", opacity=1.0,
               pressure="even", note="subject")
    s.block_in(head_top, "flat", "face_c", size=0.012, density=1.0, solid=True,
               direction=[(0.236, 0.384), (0.300, 0.338)], edge="hard", opacity=1.0,
               pressure="even", note="subject")


lay_wing()
lay_body()
lay_planes()
print(s.look(values=True, path="looks/04-gargoyle-values.png"))
print(s.look(region="B1:G7", path="looks/04-gargoyle-crop.png"))
