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
p["glow_wall"] = p.at_value(p.mix_many(["burnt_sienna", "burnt_umber", "yellow_ochre"], [2, 2, 1]), 0.27)
p["shawl"] = p.at_value(p.mix_many(["burnt_umber", "ultramarine", "yellow_ochre"], [3, 1, 0.5]), 0.16)
p["shawl_lit"] = p.at_value(p.mix_many(["burnt_umber", "yellow_ochre", "burnt_sienna", "titanium_white"], [2, 1, 1, 1]), 0.32)
p["dress"] = p.at_value(p.mix_many(["ultramarine", "burnt_umber", "titanium_white"], [2, 2, 1]), 0.18)
p["kerchief"] = p.at_value(p.mix_many(["burnt_sienna", "alizarin", "burnt_umber"], [2, 1, 1]), 0.24)
p["kerchief_lit"] = p.at_value(p.mix(p.mix_many(["burnt_sienna", "cadmium_red", "yellow_ochre", "titanium_white"], [2, 1, 1, 1]),
                                      p.mix_many(["burnt_umber", "ultramarine", "titanium_white"], [2, 1, 2]), 0.3), 0.42)
p["kerchief_shade"] = p.at_value(p.mix_many(["burnt_umber", "alizarin", "ultramarine"], [2, 1, 1]), 0.15)
p["skin_lit"] = p.at_value(p.mix_many(["yellow_ochre", "cadmium_red", "titanium_white"], [2, 1, 5]), 0.64)
p["skin_shade"] = p.at_value(p.mix_many(["burnt_sienna", "burnt_umber", "ultramarine", "titanium_white"], [3, 2, 1, 1]), 0.25)
p["skin_mid"] = p.at_value(p.mix("skin_lit", "skin_shade", 0.45), 0.42)
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
kerchief = poly_t([(372, 205), (366, 182), (350, 163), (326, 150), (296, 146), (266, 152),
                   (243, 168), (228, 192), (220, 225), (219, 262), (225, 300), (236, 335),
                   (248, 360), (262, 378), (276, 372), (290, 350), (306, 318), (324, 285),
                   (340, 255), (352, 232), (362, 216)], "kerchief")
knot = poly([(258, 402), (240, 408), (226, 424), (230, 446), (248, 456), (262, 450),
             (268, 432), (270, 414)], "knot")
tails = [[P(236, 450), P(226, 486), P(230, 520)], [P(254, 456), P(258, 494), P(270, 522)]]
face = poly_t([(372, 205), (384, 212), (393, 228), (398, 245), (404, 258), (400, 268),
               (408, 282), (417, 298), (426, 314), (425, 320), (416, 326), (411, 331),
               (414, 340), (410, 346), (407, 350), (411, 356), (409, 364), (402, 370),
               (404, 380), (400, 392), (390, 400), (372, 398), (348, 392), (322, 380),
               (300, 362), (290, 350), (306, 318), (324, 285), (340, 255), (352, 232),
               (362, 216)], "face")
neck = poly([(287, 375), (300, 391), (329, 414), (362, 430), (394, 438), (417, 440),
             (424, 468), (438, 548), (296, 552), (286, 496), (278, 450), (274, 410)], "neck")
shawl = poly([(270, 520), (220, 540), (150, 570), (80, 610), (20, 650), (-40, 690),
              (-40, 1064), (690, 1064), (684, 900), (672, 760), (655, 660), (625, 600),
              (580, 565), (520, 552), (482, 548), (430, 560), (362, 552), (320, 540)], "shawl")

# Her left hand at her throat, knuckles out, clutching the shawl shut; the thumb on the
# side toward the middle of her. The shawl's folds run out of the fist.
fist = poly([(362, 552), (380, 536), (410, 527), (444, 526), (470, 533), (482, 548),
             (478, 572), (466, 592), (440, 604), (408, 606), (382, 598), (366, 580)], "fist")
thumb = poly([(352, 560), (366, 546), (392, 548), (404, 562), (394, 574), (368, 576)], "thumb")
folds = [[P(384, 604), P(318, 690), P(252, 820)],
         [P(430, 608), P(424, 720), P(414, 870)],
         [P(472, 590), P(538, 680), P(596, 800)],
         [P(96, 606), P(176, 628), P(262, 640)]]

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
