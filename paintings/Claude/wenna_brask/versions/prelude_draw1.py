"""Wenna Brask: shared mixtures, masses and the plan. Run before every pass.

The picture: Wenna Brask at the mill at dusk, head and shoulders, turned three-quarter to
the right. She holds a horn lantern up at eye level, her elbow out, and peers past it into
the dusk. The lantern is the only light. The mill's gable wall is dark behind her lit
profile; the cold sky is behind the shadowed side of her head.

Drawn in pixels on the 768 x 1024 canvas and converted, because a face is judged in
proportions and pixels keep them honest.
"""

W, H = 768, 1024


def P(x, y):
    return (x / W, y / H)


def poly(points, name):
    return polygon([P(x, y) for x, y in points], name=name)


p = s.palette

# ---- Mixtures, each mixed to the value it is planned at.
p["sky_high"] = p.at_value(p.mix_many(["ultramarine", "burnt_umber", "titanium_white"], [3, 1, 2]), 0.26)
p["sky_mid"] = p.at_value(p.mix_many(["ultramarine", "cerulean", "titanium_white", "burnt_umber"], [2, 1, 3, 0.5]), 0.35)
p["sky_low"] = p.at_value(p.mix_many(["cerulean", "titanium_white", "alizarin", "burnt_umber"], [2, 5, 0.4, 0.5]), 0.46)
p["mill"] = p.at_value(p.mix("burnt_umber", "ultramarine", 0.45), 0.145)
p["glow_wall"] = p.at_value(p.mix_many(["burnt_sienna", "burnt_umber", "yellow_ochre"], [2, 2, 1]), 0.27)
p["shawl"] = p.at_value(p.mix_many(["burnt_umber", "ultramarine", "yellow_ochre"], [3, 1, 0.5]), 0.16)
p["shawl_lit"] = p.at_value(p.mix_many(["burnt_umber", "yellow_ochre", "burnt_sienna", "titanium_white"], [2, 1, 1, 1]), 0.32)
p["dress"] = p.at_value(p.mix_many(["ultramarine", "burnt_umber", "titanium_white"], [2, 2, 1]), 0.18)
p["kerchief"] = p.at_value(p.mix_many(["burnt_sienna", "alizarin", "burnt_umber"], [2, 1, 1]), 0.24)
p["kerchief_lit"] = p.at_value(p.mix_many(["burnt_sienna", "cadmium_red", "yellow_ochre", "titanium_white"], [2, 1, 1, 1]), 0.44)
p["kerchief_shade"] = p.at_value(p.mix_many(["burnt_umber", "alizarin", "ultramarine"], [2, 1, 1]), 0.15)
p["skin_lit"] = p.at_value(p.mix_many(["yellow_ochre", "cadmium_red", "titanium_white"], [2, 1, 5]), 0.64)
p["skin_mid"] = p.at_value(p.mix_many(["burnt_sienna", "yellow_ochre", "titanium_white", "cadmium_red"], [2, 1, 2, 0.5]), 0.42)
p["skin_shade"] = p.at_value(p.mix_many(["burnt_sienna", "burnt_umber", "ultramarine", "titanium_white"], [3, 2, 1, 1]), 0.25)
p["skin_core"] = p.at_value(p.mix_many(["burnt_umber", "burnt_sienna", "ultramarine"], [2, 1, 1]), 0.17)
p["hair"] = p.at_value(p.mix_many(["burnt_umber", "ultramarine"], [3, 1]), 0.16)
p["hair_lit"] = p.at_value(p.mix_many(["burnt_sienna", "yellow_ochre", "titanium_white"], [2, 1, 1]), 0.46)
p["iron"] = p.at_value(p.mix("burnt_umber", "ultramarine", 0.5), 0.145)
p["horn"] = p.at_value(p.mix_many(["cadmium_yellow", "yellow_ochre", "burnt_sienna", "titanium_white"], [2, 2, 0.5, 2]), 0.76)
p["flame"] = p.at_value(p.mix("lemon_yellow", "titanium_white", 0.6), 0.93)
p["flour"] = p.at_value(p.mix_many(["titanium_white", "yellow_ochre"], [8, 1]), 0.80)

# ---- The setting: the sky behind everything, the mill's gable wall in front of it. The
# rake of the roof runs down to the right side of her head and disappears behind the
# kerchief; the wall's corner is hidden behind her head and neck.
sky = poly([(-40, -40), (808, -40), (808, 760), (-40, 760)], "sky")
mill = poly([(640, -40), (808, -40), (808, 1064), (300, 1064), (300, 175)], "mill")
rake = [P(640, -20), P(300, 175)]

# ---- Wenna. Her head turned three-quarter to the right, toward the lantern.
kerchief = poly([(372, 205), (366, 182), (350, 163), (326, 150), (296, 146), (266, 152),
                 (243, 168), (228, 192), (220, 225), (219, 262), (225, 300), (236, 335),
                 (248, 360), (262, 378), (276, 372), (290, 350), (306, 318), (324, 285),
                 (340, 255), (352, 232), (362, 216)], "kerchief")
knot = poly([(236, 362), (222, 376), (226, 396), (242, 402), (258, 392), (262, 376)], "knot")
face = poly([(372, 205), (384, 212), (393, 228), (398, 245), (404, 258), (400, 268),
             (408, 282), (417, 298), (426, 314), (425, 320), (416, 326), (411, 331),
             (414, 340), (410, 346), (407, 350), (411, 356), (409, 364), (402, 370),
             (404, 380), (400, 392), (390, 400), (372, 398), (348, 392), (322, 380),
             (300, 362), (290, 350), (306, 318), (324, 285), (340, 255), (352, 232),
             (362, 216)], "face")
neck = poly([(300, 362), (322, 380), (348, 392), (372, 398), (386, 402), (390, 430),
             (398, 470), (268, 470), (266, 430), (262, 392), (276, 372), (290, 350)], "neck")
shawl = poly([(262, 440), (230, 452), (180, 470), (120, 500), (70, 535), (25, 575),
              (-40, 630), (-40, 1064), (560, 1064), (556, 900), (548, 760), (536, 640),
              (520, 560), (500, 522), (470, 480), (430, 466), (398, 462), (360, 472),
              (330, 476), (300, 468)], "shawl")
dress = poly([(470, 470), (505, 520), (530, 560), (548, 640), (556, 760), (562, 1064),
              (500, 1064), (500, 560)], "dress")

# Her left arm, raised: elbow out at shoulder height, forearm up, the lantern hung from her fist.
upper_arm = poly([(470, 458), (600, 444), (700, 446), (740, 452), (758, 478), (745, 505),
                  (700, 508), (600, 514), (505, 522)], "upper arm")
cuff = poly([(698, 452), (738, 440), (752, 480), (712, 500)], "cuff")
forearm = poly([(632, 204), (660, 196), (704, 334), (741, 473), (703, 483), (664, 345)], "forearm")
fist = blob(P(626, 178), 0.032, 0.022, wobble=0.15, points=11, seed=4, name="fist")

# The lantern: a cone cap, a body of horn panes between iron straps, a base.
cap = poly([(604, 212), (648, 212), (666, 236), (586, 236)], "cap")
lantern = poly([(588, 236), (664, 236), (662, 338), (590, 338)], "lantern")
base = poly([(580, 338), (670, 338), (672, 352), (578, 352)], "base")
ring = [P(612, 213), P(606, 200), P(614, 190), P(626, 188), P(638, 190), P(646, 200), P(640, 213)]
flame_at = P(626, 290)

# The features, as places to aim at.
far_eye = P(388, 280)
near_eye = P(342, 283)
mouth = [P(407, 351), P(392, 353), P(374, 357)]

s.plan(
    why="She has to read as a mother who has not slept: the lantern finds her face and "
        "her floury hand, and everything else is dusk.",
    values={span("A1", "B3"): 0.32, cell("A4"): 0.42, cell("H2"): 0.14, cell("B7"): 0.16,
            lantern: 0.76},
    lightest=lantern,
    subject_share=0.45,
)
