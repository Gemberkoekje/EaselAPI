"""The floor, and the stone tub carved into it under the relief.

The floor is a plane that is a plane, each half laid along its own receding lines. The
tub is a hollow thing: its far inner wall first, dark, with the lamp catching only its
top; then the heaped blanket inside it, held to the opening so the near rim cuts it off,
and a corner of it hanging over the rim; then one broken catch-light along the near rim.
"""

vp = s.px(512, CAM_VY * CH)
s.block_in(floor_l, "flat", "floor", size=0.12, solid=True, opacity=1.0, pressure="even", edge="hard",
           direction=[vp, s.px(-300, 900)])
s.block_in(floor_r, "flat", "floor", size=0.12, solid=True, opacity=1.0, pressure="even", edge="hard",
           direction=[vp, s.px(1324, 900)])

s.block_in(tub_far_wall, "flat", "tub_wall", size=0.035, solid=True, edge="hard",
           direction="axis")
rim_far = [PXL(TUB_X0 + 0.3, 0, TUB_DF), PXL(1.7, 0, TUB_DF), PXL(TUB_X1, 0, TUB_DF)]
s.stroke(px_pts([(x, y + 9) for x, y in rim_far]), "flat", "rim", size=0.018,
         clip=tub_far_wall, solid=True, pressure=[1.0, 0.7, 0.3])
s.dry()
s.block_in(tub_heap, "flat", "bedroll", size=0.026, solid=True, edge="hard", direction=8,
           clip=tub_far_wall)
s.block_in(tub_flap, "flat", "bedroll", size=0.012, solid=True, edge="hard",
           direction="axis")
hx, hy = PXL(1.80, 0.02, 6.45)
s.stroke(px_pts([(hx - 30, hy - 6), (hx - 6, hy - 12), (hx + 22, hy - 9)]), "round_hard",
         "bedroll_lit", size=0.008, opacity=0.85, pressure=[0.2, 1.0, 0.3],
         clip=tub_far_wall)
x0, y0 = PXL(1.95, 0.0, TUB_DN)
x2, y2 = PXL(2.62, 0.0, TUB_DN)
s.stroke(px_pts([(x0, y0), ((x0 + x2) / 2, (y0 + y2) / 2 - 1), (x2, y2)]), "round_hard",
         "rim", size=0.006, opacity=0.9, pressure=[0.15, 1.0, 0.35])
