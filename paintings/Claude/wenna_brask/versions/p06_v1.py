"""Pass 6: the hand and the cloth. The shawl bunched in the fist, the knuckles and the thumb,
the folds running out of the fist and fading away from the lamp, the sky's cool light on the
shoulder and on the back of the kerchief, and flour on the hand that holds it all shut."""

p["cloth_turn"] = p.mix("shawl", "shawl_lit", 0.5)
p["cool_rim"] = p.at_value(p.mix("shawl", "sky_mid", 0.45), 0.24)
p["kerchief_rim"] = p.at_value(p.mix("kerchief_shade", "sky_mid", 0.45), 0.27)
p["knuckle_hi"] = p.at_value(p.mix("skin_lit", "titanium_white", 0.3), 0.74)

bunch = poly([(386, 470), (394, 454), (416, 446), (446, 445), (470, 452), (480, 468),
              (462, 464), (432, 462), (404, 466)], "bunched shawl")


def lay_bunch():
    # The shawl gathered up out of the top of the fist: it is holding something.
    s.block_in(bunch, "flat", "shawl", size=0.012, density=1.0, solid=True, direction=-5,
               edge="hard", note="subject")
    s.stroke([P(398, 452), P(424, 446), P(452, 447), P(472, 455)], "round_hard", "cloth_turn",
             size=0.005, opacity=0.8, pressure=[0.2, 0.9, 1.0, 0.3], tip_wobble=0.35,
             note="subject")


def lay_knuckles():
    # Two valleys between the knuckles, not three; two knuckle tops catching the lamp.
    for pts, size in (([P(405, 463), P(403, 476)], 0.0045), ([P(445, 460), P(443, 474)], 0.004)):
        s.stroke(pts, "round_hard", "skin_shade", size=size, opacity=0.85,
                 pressure=[1.0, 0.3], tip_wobble=0.35, clip=fist, note="subject")
    s.stroke([P(412, 464), P(420, 461), P(430, 463)], "round_hard", "knuckle_hi", size=0.005,
             opacity=0.85, pressure=[0.3, 1.0, 0.4], tip_wobble=0.35, clip=fist, note="subject")
    s.stroke([P(452, 462), P(462, 463), P(472, 470)], "round_hard", "knuckle_hi", size=0.0045,
             opacity=0.8, pressure=[0.4, 1.0, 0.2], tip_wobble=0.35, clip=fist, note="subject")
    # The back of the hand turns away below the knuckles; the thumb's top takes a little light.
    s.stroke([P(392, 522), P(420, 532), P(452, 534)], "round_soft", "skin_shade", size=0.02,
             opacity=0.5, pressure=[0.4, 1.0, 0.5], clip=fist, note="subject")
    s.stroke([P(352, 499), P(370, 489), P(392, 491)], "round_hard", "skin_mid", size=0.005,
             opacity=0.8, pressure=[0.3, 1.0, 0.5], tip_wobble=0.35, note="subject")


def lay_folds():
    # Ridges running out of the fist, lit on the side toward the lamp, fading with distance
    # from it; none the same length or weight.
    s.stroke([P(474, 534), P(532, 640), P(588, 764)], "bristle", "shawl_lit", size=0.034,
             load=0.5, opacity=0.6, pressure=[1.0, 0.7, 0.15])
    s.stroke([P(438, 552), P(434, 660), P(424, 820)], "bristle", "shawl_lit", size=0.028,
             load=0.45, opacity=0.45, pressure=[0.9, 0.5, 0.05])
    s.stroke([P(380, 546), P(330, 628), P(268, 740)], "bristle", "cloth_turn", size=0.03,
             load=0.4, opacity=0.4, pressure=[0.8, 0.5, 0.05])


def lay_rims():
    # The sky finds the top of the left shoulder and the back of the kerchief: cool, thin, and
    # inside the edge, so the shapes turn rather than being outlined.
    s.stroke([P(24, 640), P(110, 578), P(200, 526), P(270, 492)], "round_soft", "cool_rim",
             size=0.016, opacity=0.6, pressure=[0.2, 0.8, 1.0, 0.4], clip=shawl)
    s.stroke([P(230, 138), P(204, 180), P(194, 240), P(196, 300), P(212, 356)], "round_soft",
             "kerchief_rim", size=0.014, opacity=0.6, pressure=[0.3, 1.0, 1.0, 0.7, 0.1],
             clip=kerchief, note="subject")
    # One ridge in the kerchief, running from the crown down to the knot.
    s.stroke([P(318, 176), P(292, 270), P(266, 386)], "bristle", "kerchief", size=0.022,
             load=0.45, opacity=0.5, pressure=[0.8, 0.6, 0.1], clip=kerchief, note="subject")


def lay_flour():
    # Flour dust on the hand and where it has held the shawl: starved, broken, no two alike.
    for pts, size, load in (([P(410, 474), P(430, 478), P(452, 476)], 0.014, 0.25),
                            ([P(446, 500), P(462, 508)], 0.012, 0.22),
                            ([P(392, 502), P(404, 510)], 0.010, 0.2)):
        s.stroke(pts, "bristle", "flour", size=size, load=load, opacity=0.6, clip=fist,
                 note="subject")
    s.stroke([P(420, 560), P(446, 572), P(462, 590)], "bristle", "flour", size=0.02, load=0.18,
             opacity=0.35)


lay_bunch()
lay_knuckles()
lay_folds()
lay_rims()
lay_flour()
print(s.look(region="C4:F6", path="looks/06-hand-crop.png"))
print(s.look(path="looks/06-hand-cloth.png"))
