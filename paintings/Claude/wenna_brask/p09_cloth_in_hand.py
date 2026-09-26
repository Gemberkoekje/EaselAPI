"""Pass 9: the cloth in her hand. The fist still read as a loaf of bread: a pale rounded thing
set on the shawl, holding nothing. Rehearsed first with cloth bunched round it -- a fold above,
the cloth pulled out below, a bunch at the side -- and that read as a bun in a dark cup with a
lid on it. Third failure of one passage, so the idea changed, not the brush: the shawl's rolled
edge comes up over the lower half of the fist, and her fingers curl over it. That is the
picture people know -- a hand gripping a blanket's edge -- and it hides the bulk that made the
hand too big beside her face."""

over = poly([(350, 520), (372, 512), (410, 508), (450, 502), (492, 494), (500, 540),
             (470, 572), (430, 584), (392, 578), (356, 560)], "the shawl's edge over the fist")
p["cloth_turn"] = p.mix("shawl", "shawl_lit", 0.5)

s.dry()
s.block_in(over, "flat", "shawl", size=0.014, density=1.0, solid=True, direction=-8,
           edge="hard", note="subject")
# The rolled edge takes the lamp, more of it toward the lamp; the fingers' shadow on it.
s.stroke([P(356, 519), P(392, 511), P(440, 504), P(490, 495)], "round_hard", "cloth_turn",
         size=0.007, opacity=0.85, pressure=[0.2, 0.6, 0.9, 1.0], tip_wobble=0.35,
         clip=over, note="subject")
s.stroke([P(446, 506), P(470, 501), P(492, 497)], "round_hard", "shawl_lit", size=0.004,
         opacity=0.8, pressure=[0.3, 1.0, 0.6], tip_wobble=0.35, clip=over, note="subject")
print(s.look(region="C4:E5", path="looks/09-cloth-crop.png"))
print(s.look(path="looks/09-cloth.png"))
