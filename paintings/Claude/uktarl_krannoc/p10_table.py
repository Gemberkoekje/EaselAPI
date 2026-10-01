"""The table: round, wooden, decrepit, near the door, in front of Uktarl.

A plane that is a plane, laid dark, then the candle's pool on it: three soft strokes of
paint, each smaller and lighter, wider than tall because the top is seen at a slant, mixed
from the wood and aimed at a value. Two cracks along its planks. Its near edge, seen as
the top's thickness, goes down dark along the arc nearest us.
"""

s.block_in(table_top, "flat", "wood", size=0.05, solid=True, edge="hard", direction="axis")
s.stroke(px_pts([(x, y + 7) for x, y in table_near_arc]), "flat",
         p.at_value(p.mix("wood", "black", 0.5), 0.145), size=0.016, solid=True,
         pressure="even")
s.dry()
cx, cy = candle_base
field = s.sample(table_top)
v = p.value_of(field)
for size, lift, opacity, t, w in ((0.30, 0.09, 0.40, 0.55, 70), (0.19, 0.17, 0.45, 0.7, 46),
                                  (0.10, 0.27, 0.50, 0.85, 26)):
    s.stroke(px_pts([(cx - w, cy + 4), (cx, cy + 2), (cx + w, cy + 3)]), "round_soft",
             p.at_value(p.mix("wood_lit", field, 1 - t), v + lift), size=size,
             opacity=opacity, pressure="swell", clip=table_top)
crack = p.at_value(p.mix("wood", "black", 0.6), 0.15)
for path in ([(330, 650), (420, 648), (500, 652)], [(600, 690), (660, 684), (712, 672)]):
    s.stroke(px_pts(path), "round_hard", crack, size=0.004, opacity=0.7,
             pressure=[0.1, 1.0, 0.2], clip=table_top)
