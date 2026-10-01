"""The two passages I would apologise for: the cards in Uktarl's hand, and the far crags.

The fan was three short chisel marks over an oval and read as a napkin. Cards are taller
than wide and spread from one point, each with a pip near its top, red or black, which is
what a playing card is at this size; the thumb lies across their base. The crags at the
far ends of the relief were one flat stone: each now has its face toward the lamp lit,
fainter the further from it.
"""

hx, hy = 486, 476
for i, (ang, mix) in enumerate(((-42, "card"), (-8, "card_b"), (26, "card"))):
    if mix == "card_b":
        p["card_b"] = p.at_value("card", 0.66)
    a = math.radians(ang - 90)
    tip = (hx + 34 * math.cos(a), hy + 34 * math.sin(a))
    s.stroke(px_pts([(hx, hy), tip]), "flat", mix, size=0.015, solid=True, pressure="even",
             note="subject")
    pip = (hx + 26 * math.cos(a), hy + 26 * math.sin(a))
    s.stroke(px_pts([(pip[0] - 1.5, pip[1] - 1), (pip[0] + 1.5, pip[1] + 1)]), "round_hard",
             "lining_lit" if i != 1 else "black", size=0.0045, opacity=1.0, pressure="even",
             note="subject")
s.stroke(px_pts([(hx - 12, hy + 6), (hx - 2, hy - 2), (hx + 6, hy - 6)]), "round_hard",
         "face_lit", size=0.0075, opacity=0.95, pressure=[0.6, 1.0, 0.4], note="subject")

for (top, foot), mix in ((((38, 499), (68, 542)), "mount_dark"),
                         (((205, 441), (238, 492)), "mount_mid"),
                         (((288, 409), (316, 458)), "mount_mid"),
                         (((890, 449), (862, 500)), "mount_mid"),
                         (((968, 471), (942, 520)), "mount_dark"),
                         (((1004, 501), (986, 548)), "mount_dark")):
    s.stroke(px_pts([top, ((top[0] + foot[0]) / 2, (top[1] + foot[1]) / 2 + 2), foot]),
             "flat", mix, size=0.02, opacity=0.8, pressure=[1.0, 0.7, 0.2], clip=mountain)
