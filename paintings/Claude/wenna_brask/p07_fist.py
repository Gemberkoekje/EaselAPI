"""Pass 7: the fist, redrawn. It failed twice as a mass with planes (a disc, then a bun): the
fault was the drawing, an oval with nothing in it that says hand. Redrawn as the fist people
know -- four finger segments side by side, facing us, no two the same width, the thumb lying
across their lower half -- with the lamp above and to the right lighting the knuckle tops."""

fist2 = poly([(358, 482), (366, 466), (386, 458), (414, 455), (444, 454), (470, 458),
              (486, 470), (490, 492), (486, 516), (474, 536), (450, 548), (420, 552),
              (390, 548), (368, 536), (358, 514)], "fist, redrawn")
thumb2 = poly([(352, 524), (364, 512), (396, 508), (426, 511), (438, 520), (428, 530),
               (396, 536), (366, 542)], "thumb, redrawn")
p["crease"] = p.at_value(p.mix("skin_shade", "skin_core", 0.4), 0.24)
p["knuckle_hi"] = p.at_value(p.mix("skin_lit", "titanium_white", 0.25), 0.72)
HOLD = dict(clip=fist2, note="subject")

s.dry()


def lay_fist():
    s.block_in(fist2, "flat", "skin_mid", size=0.03, density=1.0, solid=True, direction=85,
               edge="hard", note="subject")
    # The side away from the lamp.
    s.stroke([P(364, 472), P(360, 500), P(368, 532)], "round_soft", "skin_shade", size=0.024,
             opacity=0.75, pressure=[0.6, 1.0, 0.7], **HOLD)


def lay_fingers():
    # The joints between the segments: three creases, none the same length or lean, the
    # middle one longest, the last half lost.
    for pts, size, op in (([P(393, 466), P(391, 490), P(389, 512)], 0.0045, 0.85),
                          ([P(424, 462), P(423, 490), P(421, 518)], 0.005, 0.9),
                          ([P(456, 463), P(457, 486)], 0.004, 0.6)):
        s.stroke(pts, "round_hard", "crease", size=size, opacity=op, pressure=[1.0, 0.8, 0.3],
                 tip_wobble=0.35, **HOLD)
    # Where the fingers turn under into the palm.
    s.stroke([P(440, 520), P(462, 518), P(480, 512)], "round_hard", "crease", size=0.004,
             opacity=0.8, pressure=[0.3, 1.0, 0.6], tip_wobble=0.35, **HOLD)
    # The knuckle tops take the lamp, brightest nearest it.
    s.stroke([P(396, 461), P(406, 458), P(416, 459)], "round_hard", "skin_lit", size=0.005,
             opacity=0.8, pressure=[0.2, 1.0, 0.3], tip_wobble=0.35, **HOLD)
    s.stroke([P(428, 458), P(440, 456), P(451, 458)], "round_hard", "skin_lit", size=0.0055,
             opacity=0.85, pressure=[0.3, 1.0, 0.4], tip_wobble=0.35, **HOLD)
    s.stroke([P(460, 459), P(474, 463), P(486, 474)], "round_hard", "knuckle_hi", size=0.006,
             opacity=0.9, pressure=[0.4, 1.0, 0.3], tip_wobble=0.35, **HOLD)


def lay_thumb():
    s.block_in(thumb2, "flat", "skin_mid", size=0.014, density=1.0, solid=True,
               direction=[(0.46, 0.51), (0.56, 0.50)], edge="hard", note="subject")
    s.stroke([P(362, 514), P(396, 509), P(428, 512)], "round_hard", "skin_lit", size=0.005,
             opacity=0.85, pressure=[0.3, 1.0, 0.5], tip_wobble=0.35, clip=thumb2, note="subject")
    # Its own shadow on the fingers below it.
    s.stroke([P(372, 543), P(400, 540), P(428, 532)], "round_soft", "crease", size=0.008,
             opacity=0.7, pressure=[0.5, 1.0, 0.4], **HOLD)


def lay_flour():
    for pts, size, load in (([P(430, 470), P(448, 474), P(466, 476)], 0.013, 0.25),
                            ([P(398, 480), P(410, 486)], 0.011, 0.22)):
        s.stroke(pts, "bristle", "flour", size=size, load=load, opacity=0.55, **HOLD)


lay_fist()
lay_fingers()
lay_thumb()
lay_flour()
print(s.look(region="C4:E5", path="looks/07-fist-crop.png"))
