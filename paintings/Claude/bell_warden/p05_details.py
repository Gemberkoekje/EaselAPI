"""Pass 5: the core shadow, the clear light, and what gives it away -- the eye and the claws."""

p["face_c"] = p.at_value(p.mix("stone_lit", "stone_hi", 0.4), 0.64)
p["claw"] = p.at_value(p.mix("stone_shade", "night", 0.4), 0.21)
p["core"] = p.at_value(p.mix("stone_shade", "night", 0.35), 0.22)
p["membrane_core"] = p.at_value(p.mix("membrane", "night", 0.3), 0.24)
p["ridge"] = p.at_value(p.mix("stone_hi", "stone_lit", 0.4), 0.66)


def lay_core_shadow():
    # The far side turns away into shadow: a deeper band cut from a copy moved further off.
    s.block_in(body.shifted(0.050, 0.075), "flat", "core", size=0.045, density=1.0, solid=True,
               direction=-30, edge="hard", clip=body, opacity=1.0, pressure="even", note="subject")
    s.block_in(wing.shifted(0.045, 0.055), "flat", "membrane_core", size=0.04, density=1.0,
               solid=True, direction=[(0.55, 0.06), (0.64, 0.37)], edge="hard", clip=wing,
               opacity=1.0, pressure="even", note="subject")


def lay_head():
    # The far horn, behind and in shadow, so the head reads horned rather than long-eared.
    s.stroke([(0.330, 0.346), (0.352, 0.334), (0.372, 0.326), (0.386, 0.318)], "round_hard",
             "core", size=0.013, opacity=0.95, pressure=[1.0, 0.8, 0.5, 0.05], note="subject")
    s.stroke([(0.333, 0.340), (0.356, 0.329), (0.378, 0.320)], "round_hard", "mid_c",
             size=0.004, opacity=0.8, pressure=[0.6, 1.0, 0.1], tip_wobble=0.35, note="subject")
    # The lightest plane in the picture: the brow and the snout's top, facing the light.
    s.block_in(head_top.inset(0.002), "flat", "face_c", size=0.012, density=1.0, solid=True,
               direction=[(0.236, 0.384), (0.300, 0.338)], edge="hard", opacity=1.0,
               pressure="even", note="subject")
    s.stroke([(0.262, 0.359), (0.276, 0.350), (0.290, 0.344)], "round_hard", "stone_hi",
             size=0.006, opacity=0.9, pressure=[0.3, 1.0, 0.4], tip_wobble=0.35, note="subject")
    # The near horn catches the light along its upper edge and curls at the tip.
    s.stroke([(0.318, 0.332), (0.345, 0.307), (0.375, 0.292), (0.398, 0.287), (0.408, 0.274)],
             "round_hard", "stone_lit", size=0.006, opacity=0.85,
             pressure=[0.5, 1.0, 0.7, 0.3, 0.05], note="subject")


def lay_maw():
    s.stroke([(0.257, 0.414), (0.242, 0.416), (0.227, 0.419)], "round_hard", "night",
             size=0.010, opacity=0.95, pressure=[1.0, 0.6, 0.15], note="subject")
    s.stroke([(0.2335, 0.408), (0.2345, 0.4145)], "round_hard", "stone_hi", size=0.0035,
             opacity=0.85, pressure=[1.0, 0.2], tip_wobble=0.35, note="subject")
    s.stroke([(0.2465, 0.4095), (0.2470, 0.4140)], "round_hard", "stone_lit", size=0.003,
             opacity=0.8, pressure=[1.0, 0.25], tip_wobble=0.35, note="subject")


def lay_eye():
    # The give-away: a socket in shadow, and in it an ember a statue could not have.
    s.stroke([(0.271, 0.373), (0.280, 0.370), (0.289, 0.371)], "round_hard", "night",
             size=0.011, opacity=0.9, pressure=[0.5, 1.0, 0.6], note="subject")
    s.dab(0.2808, 0.3712, "round_hard", "ember", size=0.0068, press=2, tip_wobble=0.7,
          note="subject")
    p["eye_glow"] = p.mix(s.sample(ellipse((0.281, 0.371), 0.016, 0.014)), "ember", 0.55)
    s.glaze([(0.274, 0.371), (0.289, 0.371)], "eye_glow", opacity=0.2, size=0.022, note="subject")


def lay_claws():
    # Three claws hooked over the plinth's front edge, none the same length, and the paw's shadow.
    s.stroke([(0.322, 0.713), (0.345, 0.716), (0.372, 0.719), (0.398, 0.722)], "round_soft",
             "core", size=0.012, opacity=0.6, pressure=[0.4, 1.0, 1.0, 0.3], note="subject")
    for pts, size in (([(0.321, 0.721), (0.315, 0.738), (0.320, 0.758)], 0.0095),
                      ([(0.345, 0.723), (0.341, 0.742), (0.347, 0.762)], 0.0090),
                      ([(0.371, 0.725), (0.370, 0.740), (0.377, 0.753)], 0.0078)):
        s.stroke(pts, "round_hard", "claw", size=size, opacity=0.95,
                 pressure=[1.0, 0.75, 0.1], tip_wobble=0.35, note="subject")
    s.stroke([(0.318, 0.723), (0.3135, 0.737)], "round_hard", "stone_lit", size=0.0035,
             opacity=0.85, pressure=[1.0, 0.2], tip_wobble=0.35, note="subject")
    s.stroke([(0.342, 0.726), (0.3395, 0.741)], "round_hard", "stone_lit", size=0.0032,
             opacity=0.75, pressure=[1.0, 0.2], tip_wobble=0.35, note="subject")


def lay_lights():
    # A clear light: the edges facing the lamp, smallest brush, fewest strokes.
    s.stroke([(0.294, 0.492), (0.303, 0.545), (0.317, 0.600), (0.321, 0.655)], "round_hard",
             "ridge", size=0.006, opacity=0.9, pressure=[0.4, 1.0, 0.7, 0.1], tip_wobble=0.35, note="subject")
    s.stroke([(0.352, 0.370), (0.384, 0.388), (0.430, 0.384), (0.492, 0.404), (0.548, 0.434)],
             "round_hard", "stone_lit", size=0.006, opacity=0.85, pressure=[0.3, 1.0, 0.8, 0.5, 0.05],
             tip_wobble=0.35, note="subject")
    s.stroke([(0.421, 0.380), (0.434, 0.298), (0.457, 0.198), (0.473, 0.122)], "round_hard",
             "ridge", size=0.005, opacity=0.9, pressure=[0.2, 0.9, 1.0, 0.3], tip_wobble=0.35, note="subject")
    s.stroke([(0.540, 0.604), (0.556, 0.586), (0.576, 0.576)], "round_hard", "stone_lit",
             size=0.008, opacity=0.8, pressure=[0.3, 1.0, 0.2], tip_wobble=0.35, note="subject")


def lay_stone():
    for pts, size in (([(0.40, 0.500), (0.47, 0.522), (0.53, 0.556)], 0.034),
                      ([(0.365, 0.610), (0.390, 0.560)], 0.028)):
        s.stroke(pts, "bristle", "mid_c", size=size, load=0.3, opacity=0.45, note="subject")


lay_core_shadow()
s.dry()
lay_head()
lay_maw()
lay_eye()
lay_claws()
s.dry()
lay_lights()
lay_stone()
# The plinth's front stays below the head: one film, aimed at a value.
s.glaze([(0.30, 0.83), (0.44, 0.84), (0.57, 0.85)], "stone_dark", to_value=0.33, size=0.26,
        pressure="even", clip=plinth_front)
print(s.look(region="B3:D7", sketch=False, path="looks/05-details-crop.png"))
print(s.look(sketch=False, path="looks/05-details.png"))
