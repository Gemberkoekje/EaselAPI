"""The Bell-Warden: shared mixtures, masses and the plan. Run before every pass.

The picture: a stone gargoyle crouched on a plinth in the dark lower nave of a chapel's
undercroft, lit warm from the upper left. It has to pass for a statue.
"""

p = s.palette

# ---- Mixtures, each mixed to the value it is planned at.
p["night"] = p.at_value(p.mix("ultramarine", "burnt_umber", 0.55), 0.15)
p["wall"] = p.at_value(p.mix("burnt_umber", "ultramarine", 0.30), 0.21)
p["glow"] = p.at_value(p.mix_many(["burnt_umber", "yellow_ochre", "burnt_sienna"], [2, 2, 1]), 0.33)
p["pillar_dark"] = p.at_value(p.mix("burnt_umber", "ultramarine", 0.45), 0.16)
p["pillar_lit"] = p.at_value(p.mix_many(["burnt_umber", "ultramarine", "yellow_ochre", "titanium_white"], [2, 1, 1, 1]), 0.29)
p["floor"] = p.at_value(p.mix("burnt_umber", "ultramarine", 0.35), 0.19)
p["floor_lit"] = p.at_value(p.mix_many(["yellow_ochre", "burnt_umber", "titanium_white"], [2, 2, 1]), 0.34)
p["stone_dark"] = p.at_value(p.mix_many(["burnt_umber", "ultramarine", "titanium_white"], [3, 2, 1]), 0.23)
p["stone_mid"] = p.at_value(p.mix_many(["burnt_umber", "ultramarine", "titanium_white", "yellow_ochre"], [2, 1, 3, 1]), 0.40)
p["stone_lit"] = p.at_value(p.mix_many(["yellow_ochre", "burnt_umber", "titanium_white", "ultramarine"], [2, 1, 6, 0.5]), 0.60)
p["stone_hi"] = p.at_value(p.mix_many(["yellow_ochre", "titanium_white", "burnt_sienna"], [2, 8, 0.5]), 0.72)
p["ember"] = p.mix("cadmium_yellow", "cadmium_red", 0.35)

# ---- The room: wall, pillar, floor.
wall = polygon([(-0.06, -0.06), (1.06, -0.06), (1.06, 0.87), (-0.06, 0.89)], name="wall")
glow = ellipse((0.27, 0.36), 0.20, 0.27, rotate=-12, name="glow")
pillar = polygon([(0.765, -0.06), (0.885, -0.06), (0.89, 0.875), (0.76, 0.875)], name="pillar")
pillar_lit = polygon([(0.765, -0.06), (0.805, -0.06), (0.80, 0.875), (0.76, 0.875)], name="pillar lit")
floor = polygon([(-0.06, 0.86), (1.06, 0.845), (1.06, 1.06), (-0.06, 1.06)], name="floor")
pool = ellipse((0.26, 0.93), 0.24, 0.07, rotate=-3, name="pool")

# ---- The plinth: three planes, lit from the upper left.
A, B, C, D = (0.29, 0.645), (0.57, 0.665), (0.665, 0.625), (0.385, 0.605)
A2, B2, C2 = (0.292, 0.915), (0.572, 0.935), (0.663, 0.885)
plinth = polygon([D, C, C2, B2, A2, A], name="plinth")
plinth_top = polygon([A, B, C, D], name="plinth top")
plinth_front = polygon([A, B, B2, A2], name="plinth front")
plinth_side = polygon([B, C, C2, B2], name="plinth side")

# ---- The Bell-Warden, facing left toward the light.
head = ellipse((0.335, 0.35), 0.045, 0.058, rotate=-10, name="head")
muzzle = polygon([(0.305, 0.325), (0.268, 0.352), (0.272, 0.386), (0.315, 0.392)], name="muzzle")
torso = ellipse((0.47, 0.445), 0.10, 0.125, rotate=-25, name="torso")
near_wing = polygon([(0.415, 0.375), (0.405, 0.24), (0.43, 0.16), (0.462, 0.095), (0.49, 0.175),
                     (0.515, 0.215), (0.53, 0.275), (0.55, 0.305), (0.56, 0.365), (0.545, 0.42),
                     (0.47, 0.425)], name="near wing")
far_wing = polygon([(0.52, 0.31), (0.555, 0.215), (0.595, 0.16), (0.625, 0.115), (0.64, 0.19),
                    (0.635, 0.25), (0.645, 0.30), (0.62, 0.36), (0.585, 0.40)], name="far wing")
haunch = ellipse((0.565, 0.54), 0.062, 0.078, rotate=15, name="haunch")
hind_foot = polygon([(0.515, 0.60), (0.60, 0.598), (0.615, 0.632), (0.515, 0.638)], name="hind foot")
arm = ribbon([(0.415, 0.415), (0.39, 0.51), (0.37, 0.61)], 0.038, end_width=0.026, name="arm")
tail = ribbon([(0.61, 0.53), (0.652, 0.575), (0.668, 0.655), (0.655, 0.735)], 0.02, end_width=0.011, name="tail")
body = union(head, muzzle, torso, near_wing, far_wing, haunch, hind_foot, arm, name="gargoyle")

# The planes the light finds: the face, the chest, the near wing's leading edge, the arm.
face_lit = polygon([(0.30, 0.30), (0.335, 0.292), (0.35, 0.33), (0.34, 0.39), (0.315, 0.395),
                    (0.272, 0.386), (0.268, 0.352)], name="face lit")
chest_lit = polygon([(0.40, 0.36), (0.44, 0.35), (0.445, 0.44), (0.425, 0.52), (0.40, 0.50)], name="chest lit")
wing_edge_lit = polygon([(0.405, 0.24), (0.43, 0.16), (0.462, 0.095), (0.468, 0.13), (0.445, 0.20),
                         (0.428, 0.26), (0.425, 0.33), (0.412, 0.35)], name="wing edge lit")
arm_lit = ribbon([(0.405, 0.43), (0.382, 0.515), (0.364, 0.60)], 0.016, end_width=0.012, name="arm lit")
haunch_lit = ellipse((0.548, 0.515), 0.035, 0.04, rotate=15, name="haunch lit")

s.plan(
    why="It has to pass for a statue: the stone must read as carved stone at first glance, "
        "and only the glint of its eye and the claws gripping the plinth's edge give it away.",
    values={span("G1", "H3"): 0.17, glow: 0.32, plinth_top: 0.50, plinth_front: 0.40,
            plinth_side: 0.24, face_lit: 0.66, floor: 0.21},
    lightest=face_lit,
    subject_share=0.45,
)
