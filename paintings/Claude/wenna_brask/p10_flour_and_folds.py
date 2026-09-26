"""Pass 10: the floury hand, and the cloth that is most of the picture.

The why promises floury hands, and the flour on the fist went under the rolled edge with the
rest of it: it goes back on the fingers, and where the hand has held the shawl. Then the shawl,
the largest mass and still the flattest: its folds take the cool sky on the side turned to
it, and the lamp on the side turned to the lamp."""

fist2 = poly([(358, 482), (366, 466), (386, 458), (414, 455), (444, 454), (470, 458),
              (486, 470), (490, 492), (486, 516), (474, 536), (450, 548), (420, 552),
              (390, 548), (368, 536), (358, 514)], "fist, redrawn")
p["fold_cool"] = p.at_value(p.mix("shawl", "sky_mid", 0.3), 0.20)
p["fold_warm"] = p.at_value(p.mix("shawl", "shawl_lit", 0.6), 0.26)

s.dry()
# Flour on the fingers: starved, broken, no two alike.
for pts, size, load, op in (([P(396, 469), P(412, 474), P(428, 471)], 0.012, 0.22, 0.65),
                            ([P(440, 481), P(455, 487)], 0.010, 0.20, 0.55),
                            ([P(465, 470), P(478, 477)], 0.009, 0.20, 0.5)):
    s.stroke(pts, "bristle", "flour", size=size, load=load, opacity=op, clip=fist2,
             note="subject")
# ...and on the cloth she has been holding.
s.stroke([P(400, 522), P(430, 530), P(458, 536)], "bristle", "flour", size=0.02, load=0.15,
         opacity=0.35, clip=shawl)
s.stroke([P(428, 600), P(446, 616), P(458, 640)], "bristle", "flour", size=0.024, load=0.12,
         opacity=0.28, clip=shawl)

# The folds: cool on the side the sky finds, warm on the side the lamp finds.
for pts, colour, size, load, op in (
        ([P(232, 540), P(164, 642), P(112, 782)], "fold_cool", 0.03, 0.40, 0.50),
        ([P(302, 562), P(264, 702), P(236, 880)], "fold_cool", 0.024, 0.35, 0.40),
        ([P(538, 584), P(578, 684), P(598, 824)], "fold_warm", 0.03, 0.45, 0.50)):
    s.stroke(pts, "bristle", colour, size=size, load=load, opacity=op, pressure="swell",
             clip=shawl)

print(s.look(path="looks/10-flour-folds.png"))
print(s.look(region="C4:F6", path="looks/10-flour-crop.png"))
