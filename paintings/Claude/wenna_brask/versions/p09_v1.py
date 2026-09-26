"""Pass 9: the cloth in her hand. The fist still read as a loaf of bread: a pale rounded thing
set on the shawl, holding nothing. The shawl is what it holds, so the shawl comes up round it
-- a fold above the knuckles, the cloth pulled taut out of the bottom of the grip, a bunch on
the lamp side -- which also makes the hand smaller, as it should be beside her face."""

bunch_top = poly([(368, 470), (374, 452), (392, 444), (412, 445), (424, 453), (408, 459),
                  (388, 465)], "fold above the fist")
cloth_below = poly([(372, 540), (400, 544), (436, 542), (470, 530), (488, 520), (496, 548),
                    (470, 572), (430, 584), (392, 578), (366, 560)], "cloth below the fist")
cloth_side = poly([(478, 470), (494, 474), (502, 500), (498, 526), (484, 530), (486, 500)],
                  "cloth beside the fist")
p["cloth_turn"] = p.mix("shawl", "shawl_lit", 0.5)
EDGE = dict(opacity=0.8, tip_wobble=0.35)

s.dry()
for mass, direction in ((bunch_top, -8), (cloth_below, -20), (cloth_side, 80)):
    s.block_in(mass, "flat", "shawl", size=0.012, density=1.0, solid=True,
               direction=direction, edge="hard", note="subject")
# Each fold's edge toward the lamp takes its light: brightest on the lamp side.
s.stroke([P(378, 452), P(394, 445), P(414, 446)], "round_hard", "cloth_turn", size=0.005,
         pressure=[0.3, 1.0, 0.5], note="subject", **EDGE)
s.stroke([P(426, 547), P(460, 537), P(488, 524)], "round_hard", "shawl_lit", size=0.006,
         pressure=[0.2, 0.8, 1.0], note="subject", **EDGE)
s.stroke([P(494, 478), P(500, 500), P(496, 522)], "round_hard", "shawl_lit", size=0.005,
         pressure=[1.0, 0.7, 0.2], note="subject", **EDGE)
print(s.look(region="C4:E5", path="looks/09-cloth-crop.png"))
print(s.look(path="looks/09-cloth.png"))
