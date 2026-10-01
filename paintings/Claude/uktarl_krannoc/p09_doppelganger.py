"""The doppelganger, at the far right of the table: a bald vampire with pointed ears,
hunched, its head turned to stare at the doorway.

Its body first, black against the lamplit relief, then the head as Uktarl's was laid: the
shade mass, then the lit side the candle reaches (the candle is below it and to our left),
sharing a terminator. Then the ears, the deep sockets, the nose's ridge, a small mouth.
"""

s.block_in(dp_body, "flat", "black", size=0.03, solid=True, edge="hard", direction=95)
p["d_shade"] = p.at_value(p.mix("d_skin", "black", 0.45), 0.27)
for ear in dp_ears:
    s.block_in(ear, "flat", "d_shade", size=0.008, solid=True, edge="hard", direction="axis")
s.block_in(dp_head, "flat", "d_shade", size=0.012, solid=True, edge="hard", direction=95)
s.dry()
s.block_in(dp_lit, "flat", "d_skin", size=0.010, solid=True, edge="hard", clip=dp_head,
           direction=95)
s.stroke(px_pts(DP_TERM), "flat", p.mix("d_skin", "d_shade", 0.5), size=0.006, opacity=0.6,
         load=1.0, load_falloff=0.0, pressure="taper", clip=dp_head)
s.stroke(px_pts([dp(-0.95, -0.08), dp(-1.30, -0.40)]), "round_hard", "d_skin",
         size=0.005, opacity=0.8, pressure=[1.0, 0.2], clip=dp_ears[0])
eye_d = p.at_value(p.mix("d_shade", "black", 0.7), 0.16)
for ex, ey in dp_eyes:
    s.stroke(px_pts([(ex - 5, ey), (ex, ey - 1.5), (ex + 5, ey + 0.5)]), "round_hard", eye_d,
             size=0.0075, opacity=0.95, pressure=[0.5, 1.0, 0.6])
s.stroke(px_pts(dp_nose), "round_hard", p.at_value(p.mix("d_skin", "face_lit", 0.5), 0.62),
         size=0.0045, opacity=0.85, pressure=[0.3, 1.0, 0.6])
s.stroke(px_pts(dp_mouth), "round_hard", eye_d, size=0.0045, opacity=0.9,
         pressure=[0.4, 1.0, 0.4])
mx, my = dp(-0.06, 0.60)
s.stroke(px_pts([(mx, my - 1), (mx, my + 4)]), "round_hard", "card", size=0.004,
         opacity=0.9, pressure=[1.0, 0.4])
s.block_in(dp_collar, "flat", "black", size=0.010, solid=True, edge="hard", direction=0)
