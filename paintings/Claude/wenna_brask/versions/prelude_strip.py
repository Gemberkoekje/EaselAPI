"""Wenna Brask: shared mixtures, masses and the plan. Run before every pass.

The picture: Wenna Brask at the mill door at dusk, head and shoulders, turned
three-quarter to the right. A horn lantern hangs from an iron bracket on the mill wall at
her eye level, and she looks past it into the dusk, clutching her shawl at her breastbone
with both floury hands. The lantern is the only light. The mill's gable wall is dark behind
her lit profile; the cold sky is behind the shadowed side of her head.

Drawn in pixels on the 768 x 1024 canvas and converted, because a face is judged in
proportions and pixels keep them honest. The head was drawn first at a smaller size and is
scaled up by T().
"""

W, H = 768, 1024


def P(x, y):
    return (x / W, y / H)


def poly(points, name):
    return polygon([P(x, y) for x, y in points], name=name)


def T(x, y):
    """The first drawing's head, 1.3 times larger, its kerchief top at y 110."""
    return (300 + (x - 300) * 1.3, 146 + (y - 146) * 1.3 - 36)


def poly_t(points, name):
    return poly([T(x, y) for x, y in points], name)


p = s.palette

# ---- Mixtures, each mixed to the value it is planned at.
p["sky_high"] = p.at_value(p.mix_many(["ultramarine", "burnt_umber", "titanium_white"], [3, 1, 2]), 0.26)
p["sky_mid"] = p.at_value(p.mix_many(["ultramarine", "cerulean", "titanium_white", "burnt_umber"], [2, 1, 3, 0.5]), 0.35)
p["sky_low"] = p.at_value(p.mix_many(["cerulean", "titanium_white", "alizarin", "burnt_umber"], [2, 5, 0.4, 0.5]), 0.46)
p["mill"] = p.at_value(p.mix("burnt_umber", "ultramarine", 0.45), 0.145)
p["glow_wall"] = p.at_value(p.mix_many(["yellow_ochre", "burnt_umber", "burnt_sienna", "ultramarine"], [2, 2, 1, 0.3]), 0.27)
p["shawl"] = p.at_value(p.mix_many(["burnt_umber", "ultramarine", "yellow_ochre"], [3, 1, 0.5]), 0.16)
p["shawl_lit"] = p.at_value(p.mix_many(["burnt_umber", "yellow_ochre", "burnt_sienna", "titanium_white"], [2, 1, 1, 1]), 0.32)
p["dress"] = p.at_value(p.mix_many(["ultramarine", "burnt_umber", "titanium_white"], [2, 2, 1]), 0.18)
p["kerchief"] = p.at_value(p.mix_many(["burnt_sienna", "alizarin", "burnt_umber"], [2, 1, 1]), 0.24)
p["kerchief_lit"] = p.at_value(p.mix(p.mix_many(["burnt_sienna", "cadmium_red", "yellow_ochre", "titanium_white"], [2, 1, 1, 1]),
                                      p.mix_many(["burnt_umber", "ultramarine", "titanium_white"], [2, 1, 2]), 0.3), 0.42)
p["kerchief_shade"] = p.at_value(p.mix_many(["burnt_umber", "alizarin", "ultramarine"], [2, 1, 1]), 0.15)
p["skin_lit"] = p.at_value(p.mix_many(["yellow_ochre", "cadmium_red", "titanium_white"], [2, 1, 5]), 0.64)
p["skin_shade"] = p.at_value(p.mix_many(["burnt_sienna", "burnt_umber", "ultramarine", "titanium_white"], [3, 2, 1, 1]), 0.28)
p["skin_mid"] = p.at_value(p.mix("skin_lit", "skin_shade", 0.45), 0.44)
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
mill = poly([(718, -40), (808, -40), (808, 1064), (340, 1064), (340, 172)], "mill")
rake = [P(700, -30), P(380, 150)]

# ---- Wenna. Her head turned three-quarter to the right, toward the lantern.
# The kerchief: an outline nobody ruled, a bun under it at the back. It is mostly in shadow:
# a band across the crown the sky finds, and a lit crescent along its front hem, the only
# part of it that faces the lamp.
kerchief = roughen(poly([(333.8, 115.2), (294.8, 110), (255.8, 117.8), (225.9, 138.6),
                         (206.4, 169.8), (196, 212.7), (192, 262), (192, 300), (198, 336),
                         (212, 366), (232.4, 388.2), (250.6, 411.6), (268.8, 403.8),
                         (287, 375.2), (307.8, 333.6), (331.2, 290.7), (352, 251.7),
                         (367.6, 221.8), (380.6, 201), (393.6, 186.7), (385.8, 156.8),
                         (365, 132.1)], "kerchief"), amp=0.003, step=0.02, seed=3,
                   aspect=s.aspect)
kerchief_crown = poly([(248, 120), (295, 111), (334, 116), (365, 133), (372, 146), (340, 146),
                       (300, 150), (262, 160), (232, 176), (226, 150)], "kerchief crown")
kerchief_lit = poly([(333.8, 115.2), (365, 132.1), (385.8, 156.8), (393.6, 186.7),
                     (380.6, 201), (367.6, 221.8), (352, 251.7), (346, 244), (358, 214),
                     (368, 190), (370, 164), (356, 142)], "kerchief lit")
knot = poly([(258, 402), (240, 408), (226, 424), (230, 446), (248, 456), (262, 450),
             (268, 432), (270, 414)], "knot")
tails = [[P(236, 450), P(226, 486), P(230, 520)], [P(254, 456), P(258, 494), P(270, 522)]]

# The face: the shadow side is the mass; the half-tone band and the lit plane along the
# profile are shapes laid on it, drawn with the silhouette, their edge the terminator.
face = poly_t([(372, 205), (384, 212), (393, 228), (398, 245), (404, 258), (400, 268),
               (408, 282), (417, 298), (426, 314), (425, 320), (416, 326), (411, 331),
               (414, 340), (410, 346), (407, 350), (411, 356), (409, 364), (402, 370),
               (404, 380), (400, 392), (390, 400), (372, 398), (348, 392), (322, 380),
               (300, 362), (290, 350), (306, 318), (324, 285), (340, 255), (352, 232),
               (362, 216)], "face")
terminator = [(385, 196), (392, 214), (400, 240), (402, 262), (408, 282), (420, 306),
              (430, 332), (436, 348), (432, 362), (428, 378), (420, 392), (412, 410),
              (408, 432), (417, 440.2)]
face_lit = poly([(393.6, 186.7), (409.2, 195.8), (420.9, 216.6), (427.4, 238.7), (435.2, 255.6),
                 (430, 268.6), (440.4, 286.8), (452.1, 307.6), (463.8, 328.4), (462.5, 336.2),
                 (450.8, 344), (444.3, 350.5), (448.2, 362.2), (443, 370), (439.1, 375.2),
                 (444.3, 383), (441.7, 393.4), (432.6, 401.2), (435.2, 414.2), (430, 429.8),
                 (417, 440.2)] + terminator[::-1], "face lit")
face_mid = poly(terminator + [(393.6, 437.6), (392, 420), (396, 398), (400, 380), (404, 362),
                              (402, 342), (392, 318), (380, 296), (374, 270), (374, 240),
                              (372, 214), (380.6, 201)], "face mid")

# The shawl pulled up round her throat and held shut: only the neck under the jaw shows.
neck = poly([(287, 375), (300, 391), (329, 414), (362, 430), (394, 438), (417, 440),
             (424, 468), (430, 492), (292, 496), (280, 450), (274, 410)], "neck")
shawl = poly([(282, 478), (230, 500), (150, 540), (80, 590), (20, 640), (-40, 690),
              (-40, 1064), (690, 1064), (684, 900), (672, 760), (655, 660), (625, 590),
              (570, 540), (500, 506), (470, 494), (400, 484), (330, 482)], "shawl")
shoulder_lit = poly([(482, 500), (530, 512), (575, 536), (620, 580), (648, 640), (632, 656),
                     (596, 612), (548, 570), (496, 530)], "shoulder lit")

# Her left hand at her throat, knuckles out, clutching the shawl shut. The light comes from
# the upper right: the back of the hand takes it, the curled fingers are in half-tone, their
# underside and the thumb in shadow.
fist = poly([(360, 488), (372, 472), (398, 462), (430, 458), (458, 462), (476, 474),
             (482, 494), (478, 516), (466, 536), (444, 548), (414, 550), (386, 544),
             (368, 530), (360, 510)], "fist")
fist_top = poly([(372, 472), (398, 462), (430, 458), (458, 462), (476, 474), (482, 492),
                 (462, 490), (430, 489), (400, 491), (376, 490)], "back of the hand")
fist_front = poly([(376, 490), (400, 491), (430, 489), (462, 490), (482, 492), (478, 516),
                   (466, 534), (440, 530), (410, 522), (384, 512)], "curled fingers")
thumb = poly([(350, 500), (360, 486), (386, 488), (398, 500), (390, 512), (364, 514)], "thumb")
folds = [[P(378, 546), P(318, 640), P(250, 790)],
         [P(436, 552), P(430, 690), P(418, 880)],
         [P(470, 530), P(530, 640), P(590, 770)],
         [P(96, 600), P(176, 612), P(262, 600)]]

# The lantern, hung from an iron bracket on the wall: a cone cap, horn panes, a base.
bracket = [P(812, 186), P(598, 186)]
brace = [P(812, 268), P(676, 186)]
ring = [P(592, 212), P(588, 200), P(592, 190), P(598, 187), P(604, 190), P(608, 200), P(604, 212)]
cap = poly([(578, 212), (618, 212), (638, 240), (558, 240)], "cap")
lantern = poly([(560, 240), (636, 240), (634, 360), (562, 360)], "lantern")
base = poly([(552, 360), (644, 360), (646, 376), (550, 376)], "base")
flame_at = P(598, 305)

# The features, as places to aim at.
far_eye = P(*T(388, 280))
near_eye = P(*T(342, 283))
mouth = [P(*T(407, 351)), P(*T(392, 353)), P(*T(374, 357))]

s.plan(
    why="She has to read as a mother who has not slept: the lantern finds her face and "
        "her floury hands, and everything else is dusk.",
    values={span("A1", "B2"): 0.29, cell("A4"): 0.43, cell("H5"): 0.145, cell("B7"): 0.16,
            lantern: 0.76},
    lightest=lantern,
    subject_share=0.45,
)
