"""Pass 4: the Bell-Warden's masses -- the wing behind, the body in shadow, then the lit planes."""

p["membrane"] = p.at_value(p.mix("stone_mid", "stone_dark", 0.5), 0.31)
p["membrane_lit"] = p.at_value(p.mix("stone_mid", "stone_lit", 0.2), 0.42)
p["chest_c"] = p.at_value(p.mix("stone_lit", "stone_mid", 0.35), 0.54)
p["shoulder_c"] = p.at_value(p.mix("stone_lit", "stone_mid", 0.55), 0.49)
p["back_c"] = p.at_value(p.mix("stone_mid", "stone_lit", 0.2), 0.42)
p["haunch_c"] = p.at_value(p.mix("stone_mid", "stone_lit", 0.4), 0.45)
p["cheek_c"] = p.at_value(p.mix("stone_mid", "stone_lit", 0.3), 0.44)
p["face_c"] = p.at_value(p.mix("stone_lit", "stone_hi", 0.5), 0.66)


def lay_wing():
    # Behind the body: the membrane, its upper part catching the light, the bones on it.
    s.block_in(wing, "flat", "membrane", size=0.04, density=1.0, solid=True,
               direction=[(0.43, 0.30), (0.47, 0.12)], edge="hard", note="subject")
    s.block_in(wing_lit, "flat", "membrane_lit", size=0.02, density=1.0, solid=True,
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
    s.block_in(body, "flat", "stone_dark", size=0.05, density=1.0, solid=True,
               direction="axis", edge="hard", note="subject")
    s.block_in(tail, "flat", "stone_dark", size=0.012, density=1.0, solid=True,
               direction=[(0.632, 0.60), (0.67, 0.75)], edge="hard", note="subject")


def lay_planes():
    # The side facing the light, as tiles; the head's top is the lightest thing in the picture.
    for face, colour, size, side in (
            (back_lit, "back_c", 0.018, [(0.470, 0.405), (0.550, 0.430)]),
            (haunch_lit, "haunch_c", 0.018, [(0.555, 0.560), (0.600, 0.550)]),
            (shoulder_lit, "shoulder_c", 0.016, [(0.345, 0.365), (0.380, 0.385)]),
            (chest_lit, "chest_c", 0.014, [(0.300, 0.540), (0.322, 0.660)]),
            (cheek, "cheek_c", 0.016, [(0.250, 0.395), (0.310, 0.365)]),
            (head_top, "face_c", 0.012, [(0.236, 0.384), (0.300, 0.338)])):
        s.block_in(face, "flat", colour, size=size, density=1.0, solid=True, direction=side,
                   edge="hard", opacity=1.0, pressure="even", note="subject")
    # The chest turns: a half-strength stroke down the join into the shadow.
    s.stroke([(0.312, 0.49), (0.327, 0.54), (0.342, 0.60), (0.346, 0.66), (0.340, 0.71)], "flat",
             p.mix("chest_c", "stone_dark", 0.5), size=0.010, opacity=0.6, load=1.0,
             load_falloff=0.0, pressure="even", note="subject")


lay_wing()
lay_body()
lay_planes()
print(s.look(values=True, path="looks/04-gargoyle-values.png"))
print(s.look(region="B1:G7", path="looks/04-gargoyle-crop.png"))
