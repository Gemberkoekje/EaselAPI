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

# ---- The Bell-Warden: one crouched silhouette, head jutting left toward the light.
body = polygon([
    (0.330, 0.745), (0.325, 0.700), (0.322, 0.620), (0.312, 0.540),      # front leg, chest
    (0.290, 0.480), (0.262, 0.455), (0.238, 0.425), (0.232, 0.395),      # neck, jaw, muzzle
    (0.248, 0.368), (0.280, 0.335), (0.305, 0.315), (0.335, 0.300),      # snout, brow, skull
    (0.360, 0.315), (0.372, 0.290), (0.368, 0.200), (0.405, 0.075),      # near wing's edge
    (0.430, 0.135), (0.460, 0.190), (0.490, 0.225), (0.515, 0.285),      # its trailing edge
    (0.535, 0.240), (0.565, 0.165), (0.605, 0.085), (0.625, 0.160),      # far wing
    (0.630, 0.250), (0.645, 0.330), (0.640, 0.410), (0.660, 0.490),      # back, haunch
    (0.662, 0.580), (0.645, 0.660), (0.640, 0.705), (0.585, 0.715),      # hind leg and foot
    (0.555, 0.660), (0.500, 0.630), (0.440, 0.660), (0.410, 0.715),      # belly, between legs
    (0.405, 0.745)], name="gargoyle")
tail = ribbon([(0.636, 0.60), (0.664, 0.66), (0.670, 0.75), (0.655, 0.83)], 0.020,
              end_width=0.010, name="tail")

# The planes the light finds.
face_lit = polygon([(0.248, 0.368), (0.280, 0.335), (0.305, 0.318), (0.325, 0.330), (0.315, 0.370),
                    (0.295, 0.400), (0.262, 0.410), (0.238, 0.400)], name="face lit")
wing_edge_lit = polygon([(0.372, 0.290), (0.368, 0.200), (0.405, 0.075), (0.415, 0.100),
                         (0.386, 0.200), (0.386, 0.290)], name="wing edge lit")
chest_lit = polygon([(0.290, 0.480), (0.312, 0.540), (0.322, 0.620), (0.325, 0.700), (0.346, 0.700),
                     (0.350, 0.600), (0.345, 0.520), (0.330, 0.470), (0.310, 0.460)], name="chest lit")
shoulder_lit = polygon([(0.340, 0.400), (0.380, 0.360), (0.410, 0.380), (0.400, 0.440),
                        (0.360, 0.460)], name="shoulder lit")
haunch_lit = polygon([(0.540, 0.520), (0.580, 0.490), (0.600, 0.520), (0.590, 0.580),
                      (0.550, 0.600)], name="haunch lit")

s.plan(
    why="It has to pass for a statue: the stone must read as carved stone at first glance, "
        "and only the glint of its eye and the claws gripping the plinth's edge give it away.",
    values={span("G1", "H3"): 0.17, glow: 0.31, plinth_top: 0.54, plinth_front: 0.40,
            plinth_side: 0.27, face_lit: 0.66, floor: 0.17},
    lightest=face_lit,
    subject_share=0.45,
    ground="buried",
)
