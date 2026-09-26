"""Pass 4: the Bell-Warden's masses -- the silhouette in shadow, then the planes the light finds."""

near_wing = polygon([(0.372, 0.29), (0.368, 0.20), (0.405, 0.075), (0.43, 0.135), (0.46, 0.19),
                     (0.49, 0.225), (0.515, 0.285), (0.49, 0.33), (0.43, 0.34), (0.39, 0.33)],
                    name="near wing")
p["membrane"] = p.at_value(p.mix("stone_mid", "stone_dark", 0.45), 0.33)
p["chest_c"] = p.at_value(p.mix("stone_lit", "stone_mid", 0.35), 0.54)
p["shoulder_c"] = p.at_value(p.mix("stone_lit", "stone_mid", 0.55), 0.49)
p["haunch_c"] = p.at_value(p.mix("stone_mid", "stone_lit", 0.4), 0.44)
p["face_c"] = p.at_value(p.mix("stone_lit", "stone_hi", 0.5), 0.66)


def lay_silhouette():
    # The whole creature, solid, in the shadow stone: held to its outline so the wing tips stay.
    s.block_in(body, "flat", "stone_dark", size=0.04, density=1.0, solid=True,
               direction="axis", edge="hard", note="subject")
    s.block_in(tail, "flat", "stone_dark", size=0.012, density=1.0, solid=True,
               direction=[(0.636, 0.60), (0.67, 0.75)], edge="hard", note="subject")


def lay_wings():
    # The near wing's membrane takes a little light; the far one stays in shadow, with a rim.
    s.block_in(near_wing, "flat", "membrane", size=0.03, density=1.0, solid=True,
               direction=[(0.368, 0.20), (0.405, 0.075)], edge="hard", opacity=1.0,
               pressure="even", note="subject")
    s.stroke([(0.538, 0.235), (0.566, 0.165), (0.603, 0.092)], "round_hard", "stone_mid",
             size=0.008, opacity=0.85, load=1.0, load_falloff=0.0,
             pressure=[0.3, 1.0, 0.1], note="subject")


def lay_planes():
    # Each plane a tile along a side of its own; the one facing the light is the lightest.
    for face, colour, size, side in (
            (haunch_lit, "haunch_c", 0.016, [(0.540, 0.520), (0.580, 0.490)]),
            (shoulder_lit, "shoulder_c", 0.016, [(0.340, 0.400), (0.380, 0.360)]),
            (chest_lit, "chest_c", 0.014, [(0.312, 0.540), (0.325, 0.700)]),
            (wing_edge_lit, "stone_lit", 0.010, [(0.368, 0.200), (0.405, 0.075)]),
            (face_lit, "face_c", 0.014, [(0.248, 0.368), (0.305, 0.318)])):
        s.block_in(face, "flat", colour, size=size, density=1.0, solid=True, direction=side,
                   edge="hard", opacity=1.0, pressure="even", note="subject")
    # The chest turns: a half-strength stroke down the join between its lit plane and the shadow.
    s.stroke([(0.332, 0.47), (0.347, 0.53), (0.350, 0.61), (0.347, 0.69)], "flat",
             p.mix("chest_c", "stone_dark", 0.5), size=0.010, opacity=0.6, load=1.0,
             load_falloff=0.0, pressure="even", note="subject")


lay_silhouette()
lay_wings()
lay_planes()
print(s.look(values=True, path="looks/04-gargoyle-values.png"))
print(s.look(region="B1:G7", path="looks/04-gargoyle-crop.png"))
