"""The light, finished: the glare where the rays meet, the candle's warmth on Uktarl and
the table, and the rims each light leaves on what faces it.

Every mark here is one stroke and held to the thing it lies on, so a rim stays on the
silhouette it belongs to and does not run into the wall beside it.
"""

s.dry()
s.stroke(px_pts([(486, 306), (512, 296), (540, 304)]), "round_soft",
         p.at_value(p.mix("ray_lit", "glow", 0.5), 0.64), size=0.055, opacity=0.5,
         pressure="swell", clip=glow_above)
cx, cy = candle_base
s.stroke(px_pts([(cx - 30, cy - 70), (cx - 8, cy - 52), (cx + 20, cy - 66)]), "round_soft",
         p.at_value(p.mix("black", "wood_lit", 0.45), 0.25), size=0.085, opacity=0.45,
         pressure="swell", clip=uk_body, note="subject")
s.stroke(px_pts([(cx - 26, cy + 4), (cx + 4, cy + 2), (cx + 30, cy + 4)]), "round_soft",
         p.at_value(p.mix("wood_lit", "glow", 0.4), 0.44), size=0.05, opacity=0.45,
         pressure="swell", clip=table_top)

s.stroke(px_pts([(449, 412), (438, 434), (430, 470), (424, 520), (419, 572)]), "round_hard",
         "rim_light", size=0.004, opacity=0.6, pressure=[0.8, 1.0, 0.7, 0.4, 0.1],
         clip=uk_body, note="subject")
s.stroke(px_pts([(574, 408), (626, 393), (658, 344)]), "round_hard", "rim_light",
         size=0.004, opacity=0.6, pressure=[0.2, 1.0, 0.5], clip=uk_arm, note="subject")
s.stroke(px_pts([(214, 554), (242, 574), (272, 596), (302, 608)]), "round_hard",
         p.at_value("rim_light", 0.42), size=0.005, opacity=0.6, pressure=[0.2, 0.8, 1.0, 0.6],
         clip=a_body)
s.stroke(px_pts([(724, 524), (712, 550), (703, 600), (701, 660)]), "round_hard",
         "rim_light", size=0.005, opacity=0.6, pressure=[0.6, 1.0, 0.6, 0.1], clip=dp_body)
far_arc = [PXL(TABLE_C[0] + TABLE_R * math.cos(math.radians(t)), TABLE_H,
               TABLE_C[1] + TABLE_R * math.sin(math.radians(t))) for t in range(30, 151, 20)]
s.stroke(px_pts([(x, y + 3) for x, y in far_arc]), "round_hard",
         p.at_value(p.mix("wood_lit", "glow", 0.3), 0.40), size=0.004, opacity=0.55,
         pressure=[0.1, 0.6, 1.0, 1.0, 0.8, 0.5, 0.1], clip=table_top)

s.stroke(px_pts([(cx + 1, cy - 45), (cx + 1, cy - 51)]), "round_hard", "titanium_white",
         size=0.005, opacity=1.0, pressure=[1.0, 0.4])
s.dab(*s.px(512, 399), "round_hard", "gold", size=0.008, press=3, tip_wobble=0.35,
      note="subject")
