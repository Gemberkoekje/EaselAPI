"""Pass 8: the last third, on what surrounds the subject and on the passage to apologise for.

The fist is half again too large for her face and nearly as light, so its lower and outer
parts go down into the dark it sits in, leaving the knuckles the lamp finds. The shawl gets
its drape and the lamp's fall-off across it. Then the few lights the face has earned, the
flame's core, and one edge lost where nothing is happening."""

fist2 = poly([(358, 482), (366, 466), (386, 458), (414, 455), (444, 454), (470, 458),
              (486, 470), (490, 492), (486, 516), (474, 536), (450, 548), (420, 552),
              (390, 548), (368, 536), (358, 514)], "fist, redrawn")
p["fist_dim"] = p.at_value(p.mix("skin_shade", "shawl", 0.35), 0.24)
p["shawl_warm"] = p.at_value(p.mix_many(["shawl", "burnt_sienna", "yellow_ochre"], [6, 1, 0.5]), 0.19)
p["shawl_cool"] = p.at_value(p.mix("shawl", "sky_mid", 0.25), 0.16)
p["shawl_glow"] = p.at_value(p.mix("shawl", "shawl_lit", 0.45), 0.22)
p["flame_core"] = p.at_value(p.mix("flame", "titanium_white", 0.7), 0.95)
p["turn"] = p.mix("skin_lit", "skin_mid", 0.5)

s.plan(ground="buried")


def dim_the_fist():
    # Further from the lamp than her face: its lower, outer side into the dark. A film, so the
    # creases and the thumb under it still show.
    s.dry()
    s.glaze([P(364, 488), P(380, 534), P(430, 552), P(480, 530)], "fist_dim", opacity=0.5,
            size=0.06, pressure=[0.8, 1.0, 1.0, 0.6], clip=fist2)
    s.dry()
    s.stroke([P(352, 484), P(350, 500), P(354, 516)], "flat", "shawl", size=0.008, load=1.0,
             load_falloff=0.0, opacity=1.0, pressure="even")


def drape_the_shawl():
    # Long starved marks along the fall of the cloth, warm toward the lamp and cool toward the
    # sky, no two at one angle or one length.
    for pts, colour, size, load, op in (
            ([P(250, 522), P(184, 700), P(122, 1030)], "shawl_warm", 0.05, 0.35, 0.45),
            ([P(150, 562), P(76, 760), P(22, 1030)], "shawl_cool", 0.045, 0.30, 0.40),
            ([P(332, 566), P(302, 790), P(292, 1030)], "shawl_cool", 0.04, 0.30, 0.35),
            ([P(560, 566), P(602, 770), P(626, 1030)], "shawl_warm", 0.045, 0.35, 0.45),
            ([P(498, 612), P(520, 830), P(538, 1030)], "shawl_cool", 0.035, 0.30, 0.35)):
        s.stroke(pts, "bristle", colour, size=size, load=load, opacity=op, pressure="swell",
                 clip=shawl)
    # The lamp's light falling off across her chest, strongest up toward it.
    s.dry()
    s.glaze([P(478, 546), P(566, 604), P(646, 704)], "shawl_glow", opacity=0.30, size=0.15,
            pressure=[1.0, 0.6, 0.1], clip=shawl)
    s.dry()


def light_the_face():
    # The lights the face has earned, smallest brush, fewest marks.
    for pts, size, op in (([P(456, 325), P(462, 331)], 0.004, 0.85),
                          ([P(441, 290), P(450, 308)], 0.003, 0.7),
                          ([P(418, 222), P(428, 240)], 0.005, 0.6),
                          ([P(386, 314), P(399, 317)], 0.005, 0.5),
                          ([P(429, 415), P(433, 424)], 0.004, 0.6)):
        s.stroke(pts, "round_hard", "skin_hi", size=size, opacity=op, pressure=[0.3, 1.0],
                 tip_wobble=0.35, clip=face, note="subject")
    s.dab(*P(367, 287), "round_hard", "skin_hi", size=0.0025, press=1, tip_wobble=0.35,
          clip=face, note="subject")
    # The shadow side's rim, lost where it is thinnest, at the temple.
    s.stroke([P(340, 258), P(352, 262), P(364, 258)], "bristle", "turn", size=0.022,
             load=0.45, opacity=0.4, pressure="swell", clip=face, note="subject")
    # The throat's edge toward the lamp.
    s.stroke([P(418, 444), P(424, 466), P(428, 486)], "round_hard", "skin_mid", size=0.006,
             opacity=0.6, pressure=[0.3, 1.0, 0.4], tip_wobble=0.35, clip=neck, note="subject")


def finish_the_rest():
    s.dab(*P(598, 307), "round_hard", "flame_core", size=0.004, press=2, tip_wobble=0.5,
          note="subject")
    s.stroke([P(232, 412), P(226, 428), P(232, 446)], "round_hard", "kerchief_rim",
             size=0.005, opacity=0.6, pressure=[0.3, 1.0, 0.3], tip_wobble=0.35)
    # Lose the shawl's lower right into the wall: nothing is happening there.
    between = p.mix("shawl", "mill", 0.5)
    for pts, size in (([P(668, 900), P(690, 930), P(716, 944)], 0.04),
                      ([P(662, 980), P(688, 1002), P(712, 1020)], 0.036)):
        s.stroke(pts, "bristle", between, size=size, load=0.5, opacity=0.5, pressure="taper")


dim_the_fist()
drape_the_shawl()
light_the_face()
finish_the_rest()
print(s.look(path="looks/08-finish.png"))
print(s.look(values=True, path="looks/08-finish-values.png"))
print(s.look(region="C2:F5", path="looks/08-finish-crop.png"))
