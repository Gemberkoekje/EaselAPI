"""The bandit at the left end of the table, turned toward the doorway.

Her body first, a dark plum dress, the arm reaching onto the table; the wig's whole
silhouette over it, black; then her neck and her face on the wig, the face laid as the
others were, shade first and then the side the candle reaches, sharing a terminator. A few
marks for the features, dark lips, and two strands of the wig falling over the face's
edges, which is what puts the face inside the hair rather than on it.
"""

p["plum"] = p.at_value(p.mix_many(["alizarin", "ultramarine", "burnt_umber",
                                   "titanium_white"], [2, 1.2, 1, 0.5]), 0.17)
s.block_in(a_body, "flat", "plum", size=0.055, solid=True, edge="hard", direction=100)
s.block_in(a_hair, "flat", "hair", size=0.03, solid=True, edge="hard", direction=95)
s.dry()
s.block_in(a_neck, "flat", p.at_value(p.mix("face_shade", "black", 0.3), 0.28), size=0.02,
           solid=True, edge="hard", direction=90)
s.block_in(a_face, "flat", "face_shade", size=0.012, solid=True, edge="hard", direction=95)
s.dry()
s.block_in(a_lit, "flat", "face_lit", size=0.011, solid=True, edge="hard", clip=a_face,
           direction=95)
s.stroke(px_pts(A_TERM), "flat", p.mix("face_mid", "face_lit", 0.5), size=0.006,
         opacity=0.6, load=1.0, load_falloff=0.0, pressure="taper", clip=a_face)
s.stroke(px_pts([(196, 527), (199, 545)]), "round_hard", "face_mid", size=0.007,
         opacity=0.8, pressure="taper", clip=a_neck)
eye_a = p.at_value(p.mix("face_shade", "black", 0.7), 0.17)
for ex, ey in a_eyes:
    s.stroke(px_pts([(ex - 5, ey + 1), (ex, ey - 1), (ex + 5, ey)]), "round_hard", eye_a,
             size=0.0065, opacity=0.95, pressure=[0.5, 1.0, 0.6])
s.stroke(px_pts(a_lips), "round_hard", "lining", size=0.0055, opacity=0.95,
         pressure=[0.4, 1.0, 0.5])
for strand in ([ah(-0.80, -0.85), ah(-1.02, -0.20), ah(-0.95, 0.50), ah(-1.05, 1.10)],
               [ah(0.70, -0.92), ah(0.98, -0.30), ah(1.00, 0.40), ah(1.10, 1.05)]):
    s.stroke(px_pts(strand), "round_hard", "hair", size=0.007, opacity=0.95,
             pressure=[0.5, 1.0, 1.0, 0.6])
s.block_in(a_hand, "flat", "face_mid", size=0.008, solid=True, edge="hard", direction=0)
