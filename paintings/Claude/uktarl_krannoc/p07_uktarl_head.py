"""Uktarl's head: stage white, lit from below by the candle.

A form turned toward the light, lit from beneath: the shadow mass first (the whole head),
then the brow's half-tone and the lit plane, which share the terminator, set at the brow
line so the eyes sit in the light. The far cheek turns away. Then the features as few
marks: the eyes, the brows, the nose's shade side, a thin smirk and its fangs. Then the
wig, its widow's peak, and the lantern behind him finding the top of it.
"""

s.block_in(uk_head_poly, "flat", "face_shade", size=0.012, solid=True, edge="hard",
           direction=90, note="subject")
s.dry()
s.block_in(uk_face_band, "flat", "face_mid", size=0.008, solid=True, edge="hard",
           clip=uk_head_poly, direction=px_pts([UK_TERM[0], UK_TERM[-1]]), note="subject")
s.block_in(uk_face_lit, "flat", "face_lit", size=0.012, solid=True, edge="hard",
           clip=uk_head_poly, direction=95, note="subject")
s.stroke(px_pts(UK_TERM), "flat", p.mix("face_mid", "face_lit", 0.5), size=0.006,
         opacity=0.6, load=1.0, load_falloff=0.0, pressure="taper", clip=uk_head_poly,
         note="subject")
s.dry()
s.block_in(uk_cheek_shade, "flat", p.mix("face_mid", "face_lit", 0.35), size=0.006,
           solid=True, edge="hard", clip=uk_head_poly, direction=100, opacity=0.8,
           note="subject")

eye_dark = p.at_value(p.mix("face_shade", "black", 0.7), 0.17)
for (ex, ey), lift in zip(uk_eyes, (0, -1)):
    s.stroke(px_pts([(ex - 6, ey + 1), (ex, ey - 1.5 + lift), (ex + 6, ey + lift)]),
             "round_hard", eye_dark, size=0.0068, opacity=0.95, pressure=[0.5, 1.0, 0.6],
             note="subject")
for ex, ey in uk_eyes:                       # the candle, caught low in each eye
    s.dab(*s.px(ex + 1, ey + 1), "round_hard", "wax", size=0.0040, press=3, note="subject")
for brow in uk_brows:
    s.stroke(px_pts(brow), "round_hard", "hair", size=0.0055, opacity=0.95,
             pressure=[0.5, 1.0, 0.25], note="subject")
s.stroke(px_pts(uk_nose_side), "round_hard", "face_mid", size=0.005, opacity=0.6,
         pressure=[0.2, 1.0, 0.5], note="subject")
s.stroke(px_pts(uk_mouth), "round_hard", p.at_value(p.mix("lining", "black", 0.3), 0.20),
         size=0.0048, opacity=0.95, pressure=[0.3, 1.0, 0.9, 0.4], note="subject")
for top, tip in uk_fangs:
    s.stroke(px_pts([top, tip]), "round_hard", "card", size=0.0045, opacity=1.0,
             pressure=[1.0, 0.3], note="subject")

s.block_in(uk_hair, "flat", "hair", size=0.009, solid=True, edge="hard", direction=0,
           note="subject")
s.stroke(px_pts(uk_hair_top), "round_hard", "rim_light", size=0.004, opacity=0.7,
         pressure=[0.1, 0.6, 1.0, 0.7, 0.2], note="subject")
