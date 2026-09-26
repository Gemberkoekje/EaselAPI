"""Pass 5: what gives it away -- the eye and the claws -- and the head's light, the maw, the stone."""

p["face_c"] = p.at_value(p.mix("stone_lit", "stone_hi", 0.4), 0.64)
p["claw"] = p.at_value(p.mix("stone_shade", "night", 0.4), 0.22)


def lay_head():
    # The lightest plane in the picture: the brow and the snout's top, facing the light.
    s.block_in(head_top.inset(0.002), "flat", "face_c", size=0.012, density=1.0, solid=True,
               direction=[(0.236, 0.384), (0.300, 0.338)], edge="hard", opacity=1.0,
               pressure="even", note="subject")
    s.stroke([(0.262, 0.359), (0.276, 0.350), (0.290, 0.344)], "round_hard", "stone_hi",
             size=0.006, opacity=0.9, pressure=[0.3, 1.0, 0.4], note="subject")
    # The horn catches the light along its upper edge and loses it toward the tip.
    s.stroke([(0.318, 0.332), (0.345, 0.307), (0.375, 0.292), (0.398, 0.287)], "round_hard",
             "stone_lit", size=0.006, opacity=0.85, pressure=[0.5, 1.0, 0.6, 0.05],
             note="subject")


def lay_maw():
    s.stroke([(0.226, 0.419), (0.242, 0.416), (0.257, 0.414)], "round_hard", "night",
             size=0.009, opacity=0.95, pressure=[0.4, 1.0, 0.5], note="subject")
    s.stroke([(0.2335, 0.408), (0.2345, 0.4145)], "round_hard", "stone_hi", size=0.0035,
             opacity=0.85, pressure=[1.0, 0.2], note="subject")
    s.stroke([(0.2465, 0.4095), (0.2470, 0.4140)], "round_hard", "stone_lit", size=0.003,
             opacity=0.8, pressure=[1.0, 0.25], note="subject")


def lay_eye():
    # The give-away: a socket in shadow, and in it an ember a statue could not have.
    s.stroke([(0.270, 0.373), (0.280, 0.370), (0.290, 0.371)], "round_hard", "night",
             size=0.013, opacity=0.9, pressure=[0.5, 1.0, 0.6], note="subject")
    s.dab(0.2815, 0.3712, "round_hard", "ember", size=0.0075, press=2, tip_wobble=0.7,
          note="subject")
    s.glaze([(0.274, 0.371), (0.289, 0.371)], "ember", opacity=0.18, size=0.022,
            note="subject")


def lay_claws():
    # Three claws hooked over the plinth's front edge, none the same length.
    for pts, size in (([(0.320, 0.723), (0.316, 0.737), (0.321, 0.753)], 0.0075),
                      ([(0.344, 0.725), (0.342, 0.742), (0.347, 0.758)], 0.0070),
                      ([(0.370, 0.727), (0.371, 0.739), (0.376, 0.749)], 0.0060)):
        s.stroke(pts, "round_hard", "claw", size=size, opacity=0.95,
                 pressure=[1.0, 0.7, 0.1], note="subject")
    s.stroke([(0.318, 0.724), (0.315, 0.735)], "round_hard", "stone_lit", size=0.003,
             opacity=0.85, pressure=[1.0, 0.2], note="subject")
    s.stroke([(0.342, 0.727), (0.3405, 0.739)], "round_hard", "stone_lit", size=0.0028,
             opacity=0.75, pressure=[1.0, 0.2], note="subject")
    s.stroke([(0.316, 0.716), (0.336, 0.718), (0.360, 0.720)], "round_hard", "stone_lit",
             size=0.005, opacity=0.7, pressure=[0.6, 1.0, 0.3], note="subject")


def lay_stone():
    # A knee catching the light, and dry brush across the shade so it reads as stone.
    s.stroke([(0.540, 0.604), (0.556, 0.586), (0.576, 0.576)], "round_hard", "stone_lit",
             size=0.008, opacity=0.8, pressure=[0.3, 1.0, 0.2], note="subject")
    for pts, size in (([(0.40, 0.500), (0.47, 0.522), (0.53, 0.556)], 0.034),
                      ([(0.365, 0.610), (0.390, 0.560)], 0.028),
                      ([(0.585, 0.620), (0.612, 0.668)], 0.026)):
        s.stroke(pts, "bristle", "stone_mid", size=size, load=0.3, opacity=0.5, note="subject")


lay_head()
lay_maw()
lay_eye()
lay_claws()
lay_stone()
print(s.look(region="B3:D7", path="looks/05-details-crop.png"))
print(s.look(values=True, path="looks/05-details-values.png"))
