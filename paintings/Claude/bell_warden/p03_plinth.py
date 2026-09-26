"""Pass 3: the plinth -- a mass built of planes, then what it casts on the floor."""

p["plinth_top_c"] = p.at_value(p.mix("stone_lit", "stone_mid", 0.45), 0.54)
p["plinth_front_c"] = p.at_value(p.mix("stone_mid", "stone_dark", 0.2), 0.40)
p["plinth_side_c"] = p.at_value(p.mix("stone_dark", "stone_mid", 0.35), 0.27)
p["cast"] = p.at_value(p.mix("ultramarine", "burnt_umber", 0.5), 0.14)


def lay_plinth():
    s.block_in(plinth, "flat", "stone_dark", size=0.045, density=1.0, solid=True,
               direction="axis", edge="clean")
    # Each plane along a side of its own, so the grain turns from plane to plane.
    s.block_in(plinth_front.inset(0.004), "flat", "plinth_front_c", size=0.03, density=1.0,
               solid=True, direction=[A, A2], edge="clean", opacity=1.0, pressure="even")
    s.block_in(plinth_side.inset(0.003), "flat", "plinth_side_c", size=0.018, density=1.0,
               solid=True, direction=[B, C], edge="hard", opacity=1.0, pressure="even")
    s.block_in(plinth_top, "flat", "plinth_top_c", size=0.02, density=1.0, solid=True,
               direction=[D, C], edge="hard", opacity=1.0, pressure="even")
    # The front darkening toward the floor, away from the light.
    s.dry()
    s.glaze([(0.30, 0.94), (0.44, 0.95), (0.57, 0.96)], "stone_dark", to_value=0.33,
            size=0.16, pressure="even", clip=plinth_front)


def lay_cap_and_wear():
    # The cap's lip catching the light along the front edge, one faint crack, dry brush for wear.
    s.stroke([(0.318, 0.722), (0.44, 0.731), (0.552, 0.741)], "flat", "stone_lit",
             size=0.010, opacity=0.8, load=1.0, load_falloff=0.0, pressure="even")
    s.stroke([(0.522, 0.748), (0.515, 0.79), (0.524, 0.83)], "round_hard", "stone_dark",
             size=0.0045, opacity=0.55, pressure="taper")
    s.stroke([(0.33, 0.80), (0.40, 0.815), (0.46, 0.83)], "bristle", "stone_mid",
             size=0.04, load=0.35, opacity=0.6)


def lay_cast_shadow():
    s.stroke([(0.56, 0.944), (0.70, 0.955), (0.84, 0.965)], "round_soft", "cast",
             size=0.05, opacity=0.7, pressure=[1.0, 0.6, 0.05])


lay_plinth()
lay_cap_and_wear()
lay_cast_shadow()
print(s.look(values=True, path="looks/03-plinth-values.png"))
print(s.look(region="C5:G8", path="looks/03-plinth-crop.png"))
