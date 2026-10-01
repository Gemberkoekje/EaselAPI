"""The bandit nearest us, its back to the doorway, its hooded head turned to look round.

The nearest and darkest mass, laid over everything it stands in front of: the cloak in a
warm black, the hood on it. The candle is beyond it and to our right, so all that takes
light is the profile at the hood's edge and a rim along the hood and the shoulder that
face the flame. One dark stroke for the hood's own edge against the face.
"""

p["black_warm"] = p.at_value(p.mix("burnt_umber", "ultramarine", 0.3), 0.14)
s.block_in(b_body, "flat", "black_warm", size=0.08, solid=True, edge="hard", direction=100)
s.block_in(b_hood, "flat", p.at_value(p.mix("black_warm", "mount", 0.2), 0.16), size=0.032,
           solid=True, edge="hard", direction=95)
s.dry()
s.block_in(b_face, "flat", "face_mid", size=0.008, solid=True, edge="hard", direction=90)
s.stroke(px_pts([(388, 598), (396, 612), (392, 626)]), "round_hard", "face_lit", size=0.005,
         opacity=0.9, pressure=[0.3, 1.0, 0.4], clip=b_face)
s.stroke(px_pts([(378, 584), (376, 610), (378, 640)]), "round_hard", "black_warm", size=0.006,
         opacity=0.9, pressure=[0.5, 1.0, 0.6])
s.stroke(px_pts([(358, 546), (374, 560), (384, 584)]), "round_hard", "rim_light", size=0.005,
         opacity=0.75, pressure=[0.1, 1.0, 0.3])
s.stroke(px_pts([(392, 648), (440, 662), (480, 690), (502, 730)]), "round_hard", "rim_light",
         size=0.006, opacity=0.7, pressure=[0.2, 1.0, 0.6, 0.1])
