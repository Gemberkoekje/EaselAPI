"""Pass 4: the Bell-Warden's masses -- the wing behind, the body in shadow, then the lit planes."""

p["stone_shade"] = p.at_value(p.mix_many(["burnt_umber", "ultramarine", "titanium_white", "yellow_ochre"],
                                          [3, 1.5, 2, 0.5]), 0.28)
p["membrane"] = p.at_value(p.mix("stone_shade", "stone_mid", 0.3), 0.30)
p["membrane_lit"] = p.at_value(p.mix("stone_mid", "stone_shade", 0.3), 0.37)
p["mid_c"] = p.at_value(p.mix("stone_mid", "stone_shade", 0.3), 0.36)
p["lit_c"] = p.at_value(p.mix("stone_lit", "stone_mid", 0.3), 0.50)

# Light from the upper left. Copies of the silhouette moved away from the light, laid over it
# in turn, leave a rim of light along every edge facing the light and a band of mid inside it.
rim_in = body.shifted(0.010, 0.016)
mid_in = body.shifted(0.026, 0.040)


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
    # Chiaroscuro: the whole creature in the light first, then the mid and the shade laid over
    # it from copies moved away from the light, each held to its own outline and to the body.
    s.block_in(body, "flat", "lit_c", size=0.05, density=1.0, solid=True,
               direction="axis", edge="hard", note="subject")
    s.block_in(rim_in, "flat", "mid_c", size=0.045, density=1.0, solid=True, direction="axis",
               edge="hard", clip=body, opacity=1.0, pressure="even", note="subject")
    s.block_in(mid_in, "flat", "stone_shade", size=0.045, density=1.0, solid=True,
               direction="axis", edge="hard", clip=body, opacity=1.0, pressure="even",
               note="subject")
    s.block_in(tail, "flat", "stone_shade", size=0.012, density=1.0, solid=True,
               direction=[(0.632, 0.60), (0.67, 0.75)], edge="hard", note="subject")
    s.stroke([(0.640, 0.61), (0.664, 0.665), (0.668, 0.75)], "round_hard", "mid_c",
             size=0.006, opacity=0.8, load=1.0, load_falloff=0.0, pressure=[0.8, 1.0, 0.2],
             note="subject")


lay_wing()
lay_body()
print(s.look(values=True, path="looks/04-gargoyle-values.png"))
print(s.look(region="B1:G7", path="looks/04-gargoyle-crop.png"))
