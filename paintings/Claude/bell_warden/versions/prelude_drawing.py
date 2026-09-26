"""The Bell-Warden: shared mixtures, masses and the plan. Run before every pass.

The picture: a stone gargoyle crouched on a plinth in the dark lower nave of a chapel's
undercroft, lit warm from the upper left. It has to pass for a statue.
"""

p = s.palette

# ---- Mixtures, each mixed to the value it is planned at.
p["night"] = p.at_value(p.mix("ultramarine", "burnt_umber", 0.55), 0.15)
p["wall"] = p.at_value(p.mix("burnt_umber", "ultramarine", 0.30), 0.21)
p["glow"] = p.at_value(p.mix(p.mix_many(["burnt_umber", "yellow_ochre", "burnt_sienna"], [2, 2, 1]), "wall", 0.35), 0.31)
p["pillar_dark"] = p.at_value(p.mix("burnt_umber", "ultramarine", 0.45), 0.16)
p["pillar_lit"] = p.at_value(p.mix_many(["burnt_umber", "ultramarine", "yellow_ochre", "titanium_white"], [2, 1, 1, 1]), 0.25)
p["floor"] = p.at_value(p.mix("burnt_umber", "ultramarine", 0.35), 0.17)
p["floor_lit"] = p.at_value(p.mix(p.mix_many(["yellow_ochre", "burnt_umber", "titanium_white"], [2, 2, 1]), "floor", 0.3), 0.30)
p["stone_dark"] = p.at_value(p.mix_many(["burnt_umber", "ultramarine", "titanium_white"], [3, 2, 1]), 0.23)
p["stone_mid"] = p.at_value(p.mix_many(["burnt_umber", "ultramarine", "titanium_white", "yellow_ochre"], [2, 1, 3, 1]), 0.40)
p["stone_lit"] = p.at_value(p.mix_many(["yellow_ochre", "burnt_umber", "titanium_white", "ultramarine"], [2, 1, 6, 0.5]), 0.60)
p["stone_hi"] = p.at_value(p.mix_many(["yellow_ochre", "titanium_white", "burnt_sienna"], [2, 8, 0.5]), 0.72)
p["ember"] = p.mix("cadmium_yellow", "cadmium_red", 0.35)

# ---- The room: wall, pillar, floor.
wall = polygon([(-0.06, -0.06), (1.06, -0.06), (1.06, 0.87), (-0.06, 0.89)], name="wall")
glow = blob((0.30, 0.31), 0.21, 0.29, wobble=0.22, points=13, seed=5, rotate=-12, name="glow")
pillar = polygon([(0.765, -0.06), (0.885, -0.06), (0.89, 0.875), (0.76, 0.875)], name="pillar")
pillar_lit = polygon([(0.765, -0.06), (0.812, -0.06), (0.808, 0.875), (0.76, 0.875)], name="pillar lit")
floor = polygon([(-0.06, 0.86), (1.06, 0.845), (1.06, 1.06), (-0.06, 1.06)], name="floor")
pool = ellipse((0.22, 0.93), 0.22, 0.065, rotate=-3, name="pool")

# ---- The plinth: three planes, lit from the upper left. Low, so the creature owns it.
A, B, C, D = (0.315, 0.715), (0.555, 0.735), (0.635, 0.705), (0.395, 0.690)
A2, B2, C2 = (0.317, 0.925), (0.557, 0.945), (0.633, 0.905)
plinth = polygon([D, C, C2, B2, A2, A], name="plinth")
plinth_top = polygon([A, B, C, D], name="plinth top")
plinth_front = polygon([A, B, B2, A2], name="plinth front")
plinth_side = polygon([B, C, C2, B2], name="plinth side")

# ---- The Bell-Warden, in profile, facing left toward the light, one bat wing raised behind.
body = polygon([
    (0.322, 0.748), (0.312, 0.722), (0.322, 0.660), (0.318, 0.600),      # claws, paw, forearm
    (0.300, 0.540), (0.292, 0.490), (0.280, 0.455),                      # chest, throat
    (0.250, 0.445), (0.232, 0.434), (0.228, 0.428),                      # lower jaw
    (0.258, 0.414), (0.220, 0.404),                                      # open mouth, upper jaw
    (0.236, 0.384), (0.268, 0.356), (0.300, 0.338),                      # snout, brow, skull
    (0.315, 0.330), (0.360, 0.300), (0.398, 0.288), (0.365, 0.315),      # the horn
    (0.335, 0.345), (0.345, 0.365), (0.380, 0.385), (0.425, 0.380),      # nape, neck, shoulder
    (0.490, 0.400), (0.550, 0.430), (0.605, 0.480), (0.635, 0.530),      # back, rump
    (0.645, 0.590), (0.635, 0.660), (0.628, 0.705), (0.565, 0.712),      # haunch, hind foot
    (0.555, 0.660), (0.535, 0.600), (0.490, 0.585), (0.430, 0.600),      # shin, knee, belly
    (0.390, 0.580), (0.370, 0.640), (0.370, 0.700), (0.395, 0.715),      # elbow, forearm back
    (0.400, 0.748)], name="gargoyle")
wing = polygon([(0.415, 0.395), (0.430, 0.300), (0.455, 0.200), (0.470, 0.120), (0.462, 0.092),
                (0.482, 0.108), (0.550, 0.058), (0.578, 0.130), (0.632, 0.118), (0.606, 0.210),
                (0.667, 0.250), (0.612, 0.305), (0.642, 0.372), (0.586, 0.395), (0.555, 0.425),
                (0.470, 0.405)], name="wing")
wrist = (0.475, 0.115)
finger_tips = [(0.550, 0.058), (0.632, 0.118), (0.667, 0.250), (0.642, 0.372)]
tail = ribbon([(0.632, 0.600), (0.662, 0.660), (0.670, 0.750), (0.655, 0.830)], 0.020,
              end_width=0.010, name="tail")

# The planes the light finds, tiling the side that faces it.
head_top = polygon([(0.236, 0.384), (0.268, 0.356), (0.300, 0.338), (0.318, 0.340), (0.310, 0.365),
                    (0.280, 0.380), (0.250, 0.395)], name="head top")
cheek = polygon([(0.250, 0.395), (0.280, 0.380), (0.310, 0.365), (0.335, 0.360), (0.330, 0.400),
                 (0.300, 0.430), (0.265, 0.435)], name="cheek")
chest_lit = polygon([(0.292, 0.490), (0.300, 0.540), (0.318, 0.600), (0.322, 0.660), (0.318, 0.715),
                     (0.338, 0.715), (0.345, 0.660), (0.340, 0.600), (0.325, 0.540), (0.310, 0.490)],
                    name="chest lit")
shoulder_lit = polygon([(0.345, 0.365), (0.380, 0.385), (0.425, 0.380), (0.430, 0.410),
                        (0.390, 0.430), (0.355, 0.410)], name="shoulder lit")
back_lit = polygon([(0.470, 0.405), (0.550, 0.430), (0.605, 0.480), (0.590, 0.500), (0.530, 0.470),
                    (0.470, 0.440)], name="back lit")
haunch_lit = polygon([(0.535, 0.600), (0.555, 0.560), (0.600, 0.550), (0.610, 0.600), (0.580, 0.630),
                      (0.550, 0.650)], name="haunch lit")
wing_lit = polygon([(0.430, 0.300), (0.455, 0.200), (0.482, 0.108), (0.550, 0.058), (0.520, 0.140),
                    (0.490, 0.220), (0.470, 0.300), (0.450, 0.380)], name="wing lit")
face_lit = head_top

s.plan(
    why="It has to pass for a statue: the stone must read as carved stone at first glance, "
        "and only the glint of its eye and the claws gripping the plinth's edge give it away.",
    values={span("G1", "H3"): 0.17, glow: 0.31, plinth_top: 0.54, plinth_front: 0.40,
            plinth_side: 0.27, face_lit: 0.66, floor: 0.17},
    lightest=face_lit,
    subject_share=0.45,
    ground="buried",
)
