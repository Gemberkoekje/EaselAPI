"""Uktarl: the cape held out, the body, the raised arm, the collar.

The wing first, since his body overlaps its inner edge: the crimson lining, lit where the
candle below reaches it, and the folds falling from the hand. Then the black of him, laid
over it, the arm crossing the wing's top, and the collar, black outside and red within,
which frames the face that goes on in the next pass.
"""
uk_collar_red = poly_px([(492, 392), (476, 366), (458, 338), (478, 346), (495, 366), (512, 384), (529, 366), (551, 342), (576, 330), (565, 362), (549, 384), (532, 392)], "the collar's red inside")  # the prelude's, as it then stood
s.block_in(uk_wing, "flat", "lining", size=0.028, solid=True, edge="hard",
           direction=[(0.62, 0.45), (0.64, 0.80)], note="subject")
s.dry()
s.block_in(uk_wing_lit, "flat", "lining_lit", size=0.022, solid=True, edge="hard",
           clip=uk_wing, direction=[(0.60, 0.62), (0.66, 0.80)], note="subject")
for run in terminator(uk_wing_lit, uk_wing, aspect=s.aspect):
    s.stroke(run, "flat", p.mix("lining", "lining_lit", 0.5), size=0.012, opacity=0.6,
             load=1.0, load_falloff=0.0, pressure="taper", clip=uk_wing, note="subject")
for fold in UK_FOLDS:
    s.stroke(px_pts(fold), "round_hard", p.at_value(p.mix("lining", "black", 0.5), 0.16),
             size=0.008, opacity=0.75, pressure=[0.2, 1.0, 0.8, 0.1], clip=uk_wing,
             note="subject")

s.block_in(uk_body, "flat", "black", size=0.04, solid=True, edge="hard", direction=90,
           note="subject")
s.block_in(uk_arm, "flat", "black", size=0.018, solid=True, edge="hard", direction="axis",
           note="subject")
s.block_in(uk_collar, "flat", "black", size=0.014, solid=True, edge="hard",
           direction="axis", note="subject")
s.dry()
s.block_in(uk_collar_red, "flat", "lining_lit", size=0.010, solid=True, edge="hard",
           direction=90, note="subject")
s.block_in(uk_jabot, "flat", "face_mid", size=0.010, solid=True, edge="hard", direction=90,
           note="subject")
