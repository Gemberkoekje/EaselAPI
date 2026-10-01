"""Uktarl's Room: the projection, the drawing, the mixtures and the plan. Runs before every pass.

The picture: Dungeon of the Mad Mage, level 1, area 6c, seen from the doorway in the south
wall. The whole north wall is a stone relief: a rugged mountain hollowed into caverns full
of tiny carved dwarves, and behind it carved rays of sunlight fanning out to the edges of
the wall. Four Undertakers in vampire costume play cards at a decrepit table near the
door. Uktarl Krannoc has risen behind it to greet the party, one arm holding his cape out
like a wing, a fan of cards in the other hand. Behind him a lantern stands on the rim of
the stone tub he sleeps in, so the lamplight on the relief, and the carved sun's rays,
both spread from behind his head.

Distances are in metres, places on the canvas in pixels of the 1024 x 768 canvas.
"""

import math

CW, CH = 1024, 768

# ---- The projection. A camera 1.62 m up at the doorway, looking straight at the north
# wall. Everything on the wall is a frontal plane, so it is drawn straight in pixels.
CAM_E, CAM_F, CAM_VX, CAM_VY = 1.62, 1.20, 0.50, 0.46
WALL_D, WALL_HW, WALL_TOP = 7.4, 3.05, 3.6


def PR(xm, hm, dm):
    """Screen place of a point xm metres right of the axis, hm up, dm away."""
    return (CAM_VX + xm * CAM_F / dm, CAM_VY - (hm - CAM_E) * CAM_F * s.aspect / dm)


def PXL(xm, hm, dm):
    """The same point in pixels."""
    x, y = PR(xm, hm, dm)
    return (x * CW, y * CH)


def px_pts(points):
    return [s.px(x, y) for x, y in points]


def poly_px(points, name=""):
    return polygon(px_pts(points), name=name)


def ell_px(cx, cy, rx, ry, rotate=0, name=""):
    return ellipse(s.px(cx, cy), *s.px(rx, ry), rotate=rotate, name=name)


def clip_px(points, x0=-2, y0=-2, x1=CW + 2, y1=CH + 2):
    """A polygon in pixels cut off at the frame (Sutherland-Hodgman)."""
    def cut(pts, inside, meet):
        out = []
        for i, cur in enumerate(pts):
            prev = pts[i - 1]
            if inside(cur):
                if not inside(prev):
                    out.append(meet(prev, cur))
                out.append(cur)
            elif inside(prev):
                out.append(meet(prev, cur))
        return out

    def at_x(xc):
        return lambda a, b: (xc, a[1] + (b[1] - a[1]) * (xc - a[0]) / (b[0] - a[0]))

    def at_y(yc):
        return lambda a, b: (a[0] + (b[0] - a[0]) * (yc - a[1]) / (b[1] - a[1]), yc)

    pts = list(points)
    for inside, meet in ((lambda q: q[0] >= x0, at_x(x0)), (lambda q: q[0] <= x1, at_x(x1)),
                         (lambda q: q[1] >= y0, at_y(y0)), (lambda q: q[1] <= y1, at_y(y1))):
        pts = cut(pts, inside, meet)
        if not pts:
            break
    return pts


# ---- The north wall and the floor.
wall_base_y = PXL(0, 0, WALL_D)[1]                    # where the relief meets the floor
wall = poly_px(clip_px([(-40, -40), (CW + 40, -40), (CW + 40, wall_base_y + 4),
                        (-40, wall_base_y + 4)]), "wall")
floor = poly_px(clip_px([(-40, wall_base_y - 4), (CW + 40, wall_base_y - 4),
                         (CW + 40, CH + 40), (-40, CH + 40)]), "floor")
floor_l = poly_px(clip_px([(-40, wall_base_y - 4), (514, wall_base_y - 4), (514, CH + 40),
                           (-40, CH + 40)]), "floor, left")
floor_r = poly_px(clip_px([(510, wall_base_y - 4), (CW + 40, wall_base_y - 4),
                           (CW + 40, CH + 40), (510, CH + 40)]), "floor, right")

# ---- The carved sun: its rays leave a point behind Uktarl's head and fan out to the
# edges of the wall. Angles are on the canvas, counter-clockwise from the right.
SUN = (512, 334)
RAYS = [  # (centre angle, half-width), irregular on purpose: carved, not ruled
    (6, 2.6), (19, 3.6), (33, 2.8), (46, 4.0), (60, 3.0), (73, 3.8), (87, 2.8),
    (100, 3.9), (113, 3.0), (127, 4.1), (141, 2.9), (154, 3.7), (168, 2.7),
]


def ray_shape(angle, half, r0=52, r1=1500, name=""):
    a0, a1 = math.radians(angle - half), math.radians(angle + half)
    cx, cy = SUN
    pts = [(cx + r0 * math.cos(a0), cy - r0 * math.sin(a0)),
           (cx + r1 * math.cos(a0), cy - r1 * math.sin(a0)),
           (cx + r1 * math.cos(a1), cy - r1 * math.sin(a1)),
           (cx + r0 * math.cos(a1), cy - r0 * math.sin(a1))]
    return poly_px(clip_px(pts, y1=wall_base_y), name)


rays = [ray_shape(a, h, name=f"ray {i}") for i, (a, h) in enumerate(RAYS)]

# ---- The mountain, carved in front of the rays: its peak hidden behind Uktarl's head,
# a second, lower one to the right, the slopes broken into crags down to the floor.
mountain_line = [(-30, 520), (0, 522), (38, 498), (78, 506), (118, 470), (160, 478),
                 (205, 440), (246, 448), (288, 408), (328, 414), (368, 380), (410, 386),
                 (448, 352), (478, 336), (506, 322), (534, 336), (566, 352), (604, 376),
                 (640, 368), (676, 386), (712, 362), (742, 378), (778, 412), (812, 406),
                 (850, 440), (890, 448), (928, 476), (968, 470), (1004, 500), (1054, 506)]
mountain = poly_px(clip_px(mountain_line + [(1054, wall_base_y + 4),
                                            (-30, wall_base_y + 4)]), "mountain")

# The relief's planes: each crag's face turned toward the middle of the wall, where the
# lamp is, takes the light. Peaks and dips are read off the mountain's own line.
MT_L_PEAKS = [(118, 470), (205, 440), (288, 408), (368, 380), (448, 352)]
MT_L_DIPS = [(160, 478), (246, 448), (328, 414), (410, 386), (478, 336)]
MT_R_PEAKS = [(640, 368), (712, 362), (812, 406), (890, 448), (968, 470)]
MT_R_DIPS = [(604, 376), (676, 386), (778, 412), (850, 440), (928, 476)]
mt_planes_l = [poly_px([pk, dp, (dp[0] - 8, dp[1] + 58), (pk[0] + 14, pk[1] + 92)],
                       f"left facet {i}") for i, (pk, dp) in enumerate(zip(MT_L_PEAKS, MT_L_DIPS))]
mt_planes_r = [poly_px([pk, (pk[0] - 14, pk[1] + 92), (dp[0] + 8, dp[1] + 58), dp],
                       f"right facet {i}") for i, (pk, dp) in enumerate(zip(MT_R_PEAKS, MT_R_DIPS))]
# The caverns, where they show between the figures: a cave mouth is an arch, not a hole.
CAVES = [(262, 505, 20, 14), (372, 468, 18, 12), (64, 566, 22, 15), (884, 522, 22, 15),
         (968, 568, 18, 12), (858, 596, 15, 10), (420, 422, 14, 10)]


def cave_shape(cx, cy, rx, ry, name=""):
    arch = [(cx + rx * math.cos(math.radians(t)), cy - ry * math.sin(math.radians(t)))
            for t in range(0, 181, 20)]
    return poly_px(arch + [(cx - rx * 0.9, cy + ry * 0.45), (cx + rx * 0.9, cy + ry * 0.5)],
                   name)


caves = [cave_shape(*c, name=f"cavern {i}") for i, c in enumerate(CAVES)]

# ---- Uktarl Krannoc, standing behind the table, facing the doorway. His left arm (on our
# right) holds the cape out like a wing; his right hand holds the marked deck's fan of
# cards at his chest. The high collar flares behind his head, the right point taller.
uk_head = ell_px(512, 344, 24, 34, rotate=-6, name="Uktarl's head")
uk_collar = poly_px([(488, 398), (468, 370), (446, 330), (470, 338), (490, 360), (512, 380),
                     (532, 360), (556, 334), (588, 320), (572, 362), (554, 386), (536, 398)],
                    "collar")
# The slicked wig: a dark cap over the head's top, its widow's peak pointing down the
# forehead. The face is what of the head it leaves.
uk_hair = poly_px([(487, 344), (488, 326), (497, 314), (510, 309), (524, 310), (534, 318),
                   (538, 334), (537, 346), (530, 336), (521, 331), (513, 342), (506, 332),
                   (496, 334)], "wig")
uk_body = poly_px([(488, 392), (466, 398), (447, 410), (436, 432), (428, 470), (422, 520),
                   (416, 575), (410, 640), (590, 640), (588, 560), (584, 480), (580, 430),
                   (574, 408), (548, 395), (536, 392)], "Uktarl's body")
uk_arm = ribbon(px_pts([(572, 414), (626, 398), (662, 346)]), 0.030, end_width=0.020,
                name="the raised arm")
uk_hand = ell_px(668, 334, 10, 12, name="the raised hand")
uk_wing = poly_px([(574, 408), (626, 392), (660, 338), (676, 330), (690, 352), (700, 396),
                   (698, 440), (708, 482), (700, 528), (704, 570), (690, 606), (680, 640),
                   (590, 640), (584, 480), (580, 430)], "the cape held out")
uk_cards_hand = ell_px(482, 470, 12, 10, name="the hand with the cards")
# The cape's lining where the candle below finds it, and the folds that fall from the hand.
uk_wing_lit = poly_px([(588, 468), (636, 470), (662, 512), (684, 566), (676, 604), (662, 640),
                       (590, 640)], "the lining the candle finds")
UK_FOLDS = [[(660, 352), (646, 446), (634, 552), (630, 630)],
            [(668, 354), (680, 452), (680, 548), (668, 620)],
            [(656, 358), (622, 438), (606, 520)]]
# The collar is mostly its red inside, seen from the front: two flaps flaring from the neck,
# each laid along its own length, with the black of the outside as a rim along the edge.
uk_collar_l = poly_px([(489, 398), (468, 370), (446, 330), (470, 338), (490, 360), (506, 380),
                       (502, 396)], "collar, left flap")
uk_collar_r = poly_px([(535, 398), (528, 380), (534, 360), (556, 334), (588, 320), (572, 362),
                       (554, 386)], "collar, right flap")
UK_COLLAR_EDGES = [[(446, 330), (456, 352), (468, 370), (480, 386), (489, 398)],
                   [(588, 320), (580, 342), (572, 362), (562, 376), (554, 386)]]
uk_jabot = poly_px([(500, 382), (524, 382), (529, 404), (522, 438), (512, 458), (503, 438),
                    (495, 404)], "the cravat")

# ---- The table: round, near the door, its top lit by a candle.
TABLE_C, TABLE_R, TABLE_H = (0.0, 3.5), 0.62, 0.78


def table_top_pts(n=36, hm=TABLE_H):
    cx, cd = TABLE_C
    return [PXL(cx + TABLE_R * math.cos(t), hm, cd + TABLE_R * math.sin(t))
            for t in (2 * math.pi * i / n for i in range(n))]


table_top = poly_px(table_top_pts(), "table top")
candle_at = PXL(0.10, TABLE_H, 3.40)

# ---- The other three, each a different costume so they are three of a kind and not one
# printed three times. At the left end a bandit in a long black wig parted in the middle,
# turned toward the door; at the far right the doppelganger, bald with pointed ears,
# hunched over its cards; nearest us a hooded bandit with its back to us, looking round.
a_head = ell_px(186, 494, 27, 37, rotate=6, name="left bandit's face")
a_hair = poly_px([(186, 452), (160, 462), (150, 494), (152, 540), (144, 580), (174, 574),
                  (198, 566), (224, 574), (230, 540), (222, 498), (214, 464)], "left wig")
a_body = poly_px([(140, 560), (176, 548), (214, 552), (242, 572), (272, 594), (304, 606),
                  (306, 640), (292, 700), (110, 700), (118, 610)], "left bandit")
d_head = ell_px(752, 482, 24, 34, rotate=-8, name="doppelganger's head")
d_ears = [poly_px([(730, 474), (714, 457), (729, 487)], "left ear"),
          poly_px([(774, 470), (790, 453), (776, 483)], "right ear")]
d_body = poly_px([(708, 540), (728, 516), (776, 512), (800, 530), (820, 580), (826, 690),
                  (700, 690), (698, 600)], "doppelganger")
b_hood = poly_px([(338, 536), (316, 540), (298, 552), (286, 572), (280, 596), (282, 620),
                  (290, 640), (304, 654), (334, 660), (362, 654), (378, 638), (386, 614),
                  (386, 588), (378, 564), (362, 546)], "near bandit's hood")
# Its head turned to the right, toward the doorway: the profile past the hood's edge,
# brow, nose, lips, chin, which the candle finds.
b_face = poly_px([(380, 584), (390, 592), (393, 604), (400, 616), (393, 620), (395, 628),
                  (390, 634), (380, 640), (376, 614)], "near bandit's profile")
b_body = poly_px([(300, 640), (250, 660), (214, 700), (196, 780), (520, 780), (500, 712),
                  (452, 666), (384, 640)], "near bandit")

# ---- The tub, carved into the floor beneath the relief, to the right: what shows of it
# past the doppelganger.
tub = poly_px([PXL(0.5, 0, WALL_D - 0.05), PXL(2.6, 0, WALL_D - 0.05),
               PXL(2.6, 0, WALL_D - 1.25), PXL(0.5, 0, WALL_D - 1.25)], "tub")
# The tub, as a hollow thing seen from the doorway: the far inner wall fills the opening,
# since the near rim hides the tub's floor from this height. A heaped blanket rises above
# the near rim; its corner hangs over the edge.
TUB_X0, TUB_X1, TUB_DF, TUB_DN = 0.5, 2.6, WALL_D - 0.02, WALL_D - 1.22
tub_far_wall = poly_px([PXL(TUB_X0, 0, TUB_DF), PXL(TUB_X1, 0, TUB_DF),
                        PXL(TUB_X1, 0, TUB_DN), PXL(TUB_X0, 0, TUB_DN)], "tub's far wall")
_rim_y = PXL(2.0, 0.0, TUB_DN)[1]
tub_heap = poly_px([(818, _rim_y + 3), (822, 652), (838, 643), (858, 641), (876, 646),
                    (890, 638), (912, 635), (930, 642), (946, 651), (962, 648), (980, 656),
                    (994, _rim_y + 3)], "blanket heap")
tub_flap = poly_px([PXL(2.10, 0.0, TUB_DN + 0.02), PXL(2.32, 0.0, TUB_DN + 0.02),
                    (PXL(2.30, 0.0, TUB_DN)[0] - 2, PXL(2.30, 0.0, TUB_DN)[1] + 16),
                    (PXL(2.16, 0.0, TUB_DN)[0] + 3, PXL(2.16, 0.0, TUB_DN)[1] + 12)],
                   "blanket's corner over the rim")
tub_near_rim = [PXL(1.0, 0.0, TUB_DN), PXL(1.9, 0.0, TUB_DN), PXL(2.6, 0.0, TUB_DN)]
lantern_at = PXL(0.25, 1.00, WALL_D - 0.8)   # on a crate by the tub
glow_at = PXL(0.25, 1.00, WALL_D)            # the nearest point of the relief to it

# ---- Mixtures, each mixed to the value it is planned at.
p = s.palette
# The wall: warm stone, from the dark corners to the lamp-lit middle.
p["wall_far"] = p.at_value(p.mix_many(["burnt_umber", "ultramarine", "yellow_ochre",
                                       "titanium_white"], [3, 1, 1, 1]), 0.16)
p["wall"] = p.at_value(p.mix_many(["burnt_umber", "yellow_ochre", "titanium_white",
                                   "ultramarine"], [3, 1.2, 1.5, 0.6]), 0.23)
# The rays: the relief's old gilding, worn.
p["ray"] = p.at_value(p.mix_many(["yellow_ochre", "burnt_sienna", "titanium_white",
                                  "burnt_umber"], [3, 0.6, 2, 0.5]), 0.40)
# The mountain: the relief's stone, a dusky violet against the gold.
p["ray_hi"] = p.at_value(p.mix_many(["yellow_ochre", "cadmium_yellow", "titanium_white",
                                     "burnt_umber"], [3, 0.5, 2.2, 0.4]), 0.44)
p["ray_lo"] = p.at_value(p.mix_many(["yellow_ochre", "burnt_umber", "titanium_white",
                                     "burnt_sienna"], [2.5, 1, 1.6, 0.4]), 0.36)
p["mount"] = p.at_value(p.mix_many(["burnt_umber", "alizarin", "ultramarine",
                                    "titanium_white"], [2, 0.6, 0.7, 2]), 0.30)
p["mount_lit"] = p.at_value(p.mix("mount", "yellow_ochre", 0.3), 0.42)
p["mount_mid"] = p.at_value(p.mix("mount", "yellow_ochre", 0.15), 0.35)
p["mount_dark"] = p.at_value(p.mix("mount", "ultramarine", 0.2), 0.22)
p["mount_deep"] = p.at_value(p.mix_many(["burnt_umber", "alizarin", "ultramarine",
                                         "titanium_white"], [2, 0.5, 0.8, 0.8]), 0.20)
p["crevice"] = p.at_value(p.mix("burnt_umber", "ultramarine", 0.45), 0.145)
p["cavern"] = p.at_value(p.mix("burnt_umber", "ultramarine", 0.35), 0.14)
p["dwarf"] = p.at_value(p.mix_many(["yellow_ochre", "burnt_sienna", "titanium_white"],
                                   [3, 1, 1.5]), 0.46)
# The lamplight on the relief.
p["ray_lit"] = p.at_value(p.mix_many(["yellow_ochre", "cadmium_yellow", "titanium_white",
                                      "burnt_sienna"], [3, 0.8, 3, 0.3]), 0.60)
p["glow"] = p.at_value(p.mix_many(["yellow_ochre", "cadmium_yellow", "titanium_white",
                                   "burnt_sienna"], [2, 1, 3, 0.4]), 0.62)
# The floor and the tub.
p["floor"] = p.at_value(p.mix_many(["burnt_umber", "ultramarine", "yellow_ochre"],
                                   [3, 1, 0.5]), 0.15)
p["rim"] = p.at_value(p.mix_many(["yellow_ochre", "burnt_umber", "titanium_white"],
                                 [2, 1, 2]), 0.40)
p["tub_wall"] = p.at_value(p.mix_many(["burnt_umber", "ultramarine", "yellow_ochre",
                                       "titanium_white"], [3, 1, 0.8, 0.5]), 0.19)
p["bedroll_lit"] = p.at_value(p.mix_many(["viridian", "yellow_ochre", "titanium_white",
                                          "burnt_umber"], [1, 1.5, 1.5, 1]), 0.36)
p["bedroll"] = p.at_value(p.mix_many(["viridian", "burnt_umber", "yellow_ochre",
                                      "titanium_white"], [1, 2, 1, 1]), 0.24)
# The costumes: black, a crimson lining, and the lamp's rim along them.
p["black"] = p.at_value(p.mix("ultramarine", "burnt_umber", 0.5), 0.14)
p["rim_light"] = p.at_value(p.mix_many(["yellow_ochre", "titanium_white", "burnt_sienna"],
                                       [2, 2, 0.5]), 0.50)
p["lining"] = p.at_value(p.mix_many(["alizarin", "cadmium_red", "burnt_umber"], [3, 1, 1]),
                         0.20)
p["lining_lit"] = p.at_value(p.mix_many(["cadmium_red", "alizarin", "yellow_ochre",
                                         "titanium_white"], [3, 2, 0.5, 0.6]), 0.32)
# The faces: stage white, and the doppelganger's grey-green.
p["face_lit"] = p.at_value(p.mix_many(["titanium_white", "yellow_ochre", "cadmium_red"],
                                      [8, 1.2, 0.2]), 0.72)
p["face_shade"] = p.at_value(p.mix_many(["titanium_white", "ultramarine", "burnt_umber",
                                         "alizarin"], [3, 1, 1, 0.3]), 0.36)
p["face_mid"] = p.at_value(p.mix("face_lit", "face_shade", 0.5), 0.53)
p["d_skin"] = p.at_value(p.mix_many(["titanium_white", "viridian", "yellow_ochre",
                                     "burnt_umber"], [5, 0.6, 0.5, 0.5]), 0.50)
p["hair"] = p.at_value(p.mix("burnt_umber", "ultramarine", 0.45), 0.14)
# The table.
p["wood"] = p.at_value(p.mix_many(["burnt_umber", "burnt_sienna", "ultramarine"],
                                  [3, 1, 0.5]), 0.17)
p["wood_lit"] = p.at_value(p.mix_many(["burnt_sienna", "yellow_ochre", "burnt_umber",
                                       "titanium_white"], [2, 1.5, 1, 1.2]), 0.44)
# Small things.
p["wax"] = p.at_value(p.mix_many(["titanium_white", "yellow_ochre"], [6, 1]), 0.80)
p["flame"] = p.at_value(p.mix("lemon_yellow", "titanium_white", 0.6), 0.94)
p["gold"] = p.at_value(p.mix_many(["cadmium_yellow", "yellow_ochre", "titanium_white"],
                                  [2, 2, 1]), 0.66)
p["copper"] = p.at_value(p.mix_many(["burnt_sienna", "cadmium_red", "yellow_ochre",
                                     "titanium_white"], [3, 1, 1, 1]), 0.42)
p["silver"] = p.at_value(p.mix_many(["titanium_white", "ultramarine", "burnt_umber"],
                                    [6, 0.5, 0.4]), 0.70)
p["card"] = p.at_value(p.mix_many(["titanium_white", "yellow_ochre"], [10, 1]), 0.80)

# ---- Places the plan holds the painting to.
pl_corner = cell("A1")
pl_glow = ell_px(410, 198, 8, 8, name="the lit gilding above his head")
pl_mountain = ell_px(904, 528, 26, 18, name="the mountain's right flank")
pl_floor = ell_px(56, 704, 36, 26, name="the floor at the left")
pl_face = ell_px(512, 358, 13, 15, name="Uktarl's face")
pl_table = ell_px(604, 668, 36, 12, name="the table top by the candle")
pl_near = ell_px(330, 736, 60, 24, name="the near bandit's back")

s.plan(
    why="Four vampires at cards beneath a carved sunrise: its rays fan out from behind "
        "Uktarl's head like a saint's halo, and no real vampire would stand in it.",
    values={pl_corner: 0.22, pl_glow: 0.50, pl_mountain: 0.22, pl_floor: 0.15,
            pl_face: 0.68, pl_table: 0.46, pl_near: 0.14},
    lightest=pl_face,
    subject_share=0.30,
    ground="buried",
)

# ---- Uktarl's head, drawn from its own outline so the planes share its edges. Local
# coordinates are in head radii, v downward; the head tilts six degrees.
UK_HC, UK_RX, UK_RY, UK_TILT = (512, 344), 24, 34, math.radians(-6)


def hp(u, v):
    cx, cy = UK_HC
    return (cx + u * UK_RX * math.cos(UK_TILT) - v * UK_RY * math.sin(UK_TILT),
            cy + u * UK_RX * math.sin(UK_TILT) + v * UK_RY * math.cos(UK_TILT))


def head_arc(t0, t1, n):
    """The head's outline, narrowing toward a pointed chin below the middle."""
    pts = []
    for i in range(n + 1):
        t = math.radians(t0 + (t1 - t0) * i / n)
        below = max(0.0, math.sin(t))
        pts.append(hp(math.cos(t) * (1 - 0.30 * below ** 1.5), math.sin(t) * (1 + 0.06 * below)))
    return pts


uk_head_poly = poly_px(head_arc(0, 360, 40)[:-1], "Uktarl's head")
# Lit from the candle below him and to our right: everything under the brow line takes the
# light, the right side highest; the forehead above it turns away into shade. The eyes sit
# in the lit face, so they can be found as dark marks on a light ground.
UK_TERM = [hp(0.96, -0.46), hp(0.50, -0.33), hp(0.0, -0.28), hp(-0.50, -0.25),
           hp(-0.97, -0.20)]
uk_face_lit = poly_px(head_arc(-26, 168, 20) + UK_TERM[::-1][1:-1], "the lit face")
uk_face_band = poly_px(UK_TERM + [hp(-0.92, -0.36), hp(-0.45, -0.42), hp(0.0, -0.45),
                                  hp(0.48, -0.50), hp(0.90, -0.62)], "the brow's half-tone")
# The cheek on our left turns away from the candle: a band of half-tone along it.
uk_cheek_shade = poly_px(head_arc(100, 172, 10) + [hp(-0.62, -0.10), hp(-0.56, 0.30),
                                                   hp(-0.34, 0.66)], "the far cheek")
uk_eyes = [hp(-0.42, -0.10), hp(0.42, -0.15)]
uk_mouth = [hp(-0.34, 0.52), hp(-0.08, 0.56), hp(0.18, 0.55), hp(0.40, 0.46)]
uk_fangs = [(hp(-0.16, 0.55), hp(-0.17, 0.66)), (hp(0.17, 0.555), hp(0.17, 0.665))]
uk_brows = [[hp(-0.74, -0.24), hp(-0.46, -0.34), hp(-0.14, -0.27)],
            [hp(0.14, -0.31), hp(0.46, -0.42), hp(0.80, -0.50)]]
uk_nose_side = [hp(-0.07, -0.06), hp(-0.10, 0.12), hp(-0.06, 0.26)]
uk_hair_top = head_arc(-160, -15, 12)

# ---- The relief right round Uktarl, where the lantern behind him lights it most: three
# places that share his silhouette's edges, so light can be laid up to him and not on him.
glow_left = poly_px([(446, 330), (456, 352), (468, 370), (480, 386), (489, 398), (466, 398),
                     (447, 410), (436, 432), (428, 470), (422, 520), (416, 575), (410, 640),
                     (90, 640), (90, 180), (446, 180)], "the relief left of him")
glow_right = poly_px([(668, 322), (676, 330), (690, 352), (700, 396), (698, 440), (708, 482),
                      (700, 528), (704, 570), (690, 606), (680, 640), (950, 640), (950, 180),
                      (668, 180)], "the relief right of him")
glow_above = poly_px([(380, 220), (650, 220), (650, 322), (588, 320), (556, 334), (538, 336),
                      (536, 326), (528, 314), (512, 308), (496, 312), (488, 326), (487, 340),
                      (490, 360), (470, 338), (446, 330), (380, 330)], "the relief above him")

# ---- The doppelganger's head, drawn as Uktarl's is: bald, egg-shaped, turned three-quarter
# toward the doorway, lit by the candle from below and to our left.
DP_HC, DP_RX, DP_RY, DP_TILT = (752, 482), 22, 33, math.radians(-8)


def dp(u, v):
    cx, cy = DP_HC
    return (cx + u * DP_RX * math.cos(DP_TILT) - v * DP_RY * math.sin(DP_TILT),
            cy + u * DP_RX * math.sin(DP_TILT) + v * DP_RY * math.cos(DP_TILT))


def dp_arc(t0, t1, n):
    pts = []
    for i in range(n + 1):
        t = math.radians(t0 + (t1 - t0) * i / n)
        below = max(0.0, math.sin(t))
        above = max(0.0, -math.sin(t))
        pts.append(dp(math.cos(t) * (1 - 0.38 * below ** 1.4 + 0.06 * above),
                      math.sin(t) * (1 + 0.04 * below)))
    return pts


dp_head = poly_px(dp_arc(0, 360, 40)[:-1], "the doppelganger's head")
dp_ears = [poly_px([dp(-0.92, -0.20), dp(-1.62, -0.66), dp(-1.10, -0.02), dp(-0.95, 0.12)],
                   "its left ear"),
           poly_px([dp(0.92, -0.22), dp(1.58, -0.70), dp(1.08, -0.04), dp(0.93, 0.10)],
                   "its right ear")]
DP_TERM = [dp(0.30, -0.98), dp(0.38, -0.50), dp(0.30, -0.05), dp(0.38, 0.40), dp(0.20, 0.86)]
dp_lit = poly_px(dp_arc(-108, 116, 22)[::-1] + DP_TERM[1:-1], "its lit side")
dp_lit = poly_px(dp_arc(110, 252, 18) + DP_TERM, "its lit side")
dp_eyes = [dp(-0.42, -0.12), dp(0.36, -0.16)]
dp_nose = [dp(-0.04, -0.08), dp(-0.10, 0.18), dp(-0.06, 0.32)]
dp_mouth = [dp(-0.30, 0.56), dp(-0.06, 0.60), dp(0.16, 0.57)]
dp_body = poly_px([(712, 548), (722, 524), (740, 514), (766, 512), (788, 520), (806, 540),
                   (822, 586), (828, 690), (698, 690), (700, 600)], "the doppelganger")
dp_collar = poly_px([(724, 524), (736, 504), (750, 514), (764, 508), (778, 500), (786, 522),
                     (772, 536), (734, 536)], "its coat collar, buttoned to the jaw")

# ---- The table's near edge (the arc nearest us) and its thickness, and where the
# candle stands on it.
table_near_arc = [PXL(TABLE_C[0] + TABLE_R * math.cos(math.radians(t)), TABLE_H,
                      TABLE_C[1] - TABLE_R * math.sin(math.radians(t)))
                  for t in range(200, 341, 20)]
candle_base = PXL(0.10, TABLE_H, 3.40)

# ---- The bandit at the left end: a long black wig parted in the middle, a pale face
# turned toward the doorway, a plum dress, one arm reaching onto the table. The candle is
# to our right of her, so three quarters of the face she turns to it takes the light.
AH_C, AH_RX, AH_RY, AH_TILT = (188, 496), 22, 31, math.radians(7)


def ah(u, v):
    cx, cy = AH_C
    return (cx + u * AH_RX * math.cos(AH_TILT) - v * AH_RY * math.sin(AH_TILT),
            cy + u * AH_RX * math.sin(AH_TILT) + v * AH_RY * math.cos(AH_TILT))


def ah_arc(t0, t1, n):
    pts = []
    for i in range(n + 1):
        t = math.radians(t0 + (t1 - t0) * i / n)
        below = max(0.0, math.sin(t))
        pts.append(ah(math.cos(t) * (1 - 0.28 * below ** 1.5), math.sin(t)))
    return pts


a_face = poly_px(ah_arc(0, 360, 36)[:-1], "her face")
A_TERM = [ah(-0.12, -0.98), ah(-0.30, -0.55), ah(-0.40, -0.05), ah(-0.40, 0.42), ah(-0.30, 0.86)]
a_lit = poly_px(ah_arc(-96, 104, 20) + A_TERM[::-1][1:-1], "her lit side")
a_eyes = [ah(-0.40, -0.10), ah(0.40, -0.13)]
a_lips = [ah(-0.20, 0.56), ah(0.04, 0.60), ah(0.26, 0.55)]
a_neck = poly_px([(180, 524), (199, 522), (201, 546), (178, 549)], "her neck")
a_hand = ell_px(298, 612, 12, 7, rotate=-10, name="her hand on the table")

# ---- What is on the table, and in the hands over it.
a_lower = poly_px([(116, 680), (300, 680), (300, 690), (250, 780), (100, 780)], "her lap")
d_lower = poly_px([(698, 680), (828, 680), (836, 780), (704, 780)], "its lap")
uk_fan_hand = (484, 474)
UK_FAN = [(-44, 24), (-8, 28), (28, 25)]          # each card's angle and length
a_fan_hand = (300, 610)
A_FAN = [(-152, 19), (-112, 20)]
d_hand = [(726, 604), (712, 610), (700, 612)]
D_FAN = [(-45, 17), (-88, 18)]
TABLE_CARDS = [((462, 676), (488, 670)), ((490, 690), (515, 688)), ((628, 668), (652, 672))]
COIN_STACKS = [((412, 650), 14, "copper"), ((598, 642), 18, "gold"), ((668, 664), 12, "silver"),
               ((452, 698), 10, "gold")]
LOOSE_COINS = [((432, 680), 0.0075, "gold"), ((622, 690), 0.0068, "silver"),
               ((390, 668), 0.0070, "copper")]
silver_ring = (568, 682)
