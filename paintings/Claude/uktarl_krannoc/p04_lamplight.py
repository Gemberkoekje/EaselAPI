"""The lantern's light on the relief, behind Uktarl.

A light's pool on a dark surface: soft strokes of paint, each smaller and lighter, mixed
from the surface they land on and aimed at a value. The pool lays its paint over rays and
gaps alike, which is not what light does (light multiplies), so the rays nearest the lamp
are struck again afterwards in the gilding's lit colour, inside their own wedges. Then
the corners of the wall go down toward dark: the carved sun is lit from its middle.
"""

gx, gy = glow_at
field = s.sample(ell_px(gx, gy, 200, 160))
v = p.value_of(field)
s.dry()
for size, lift, opacity, t, dy in ((0.62, 0.07, 0.30, 0.55, 0), (0.42, 0.14, 0.36, 0.65, -6),
                                   (0.27, 0.22, 0.42, 0.78, -12), (0.15, 0.31, 0.48, 0.9, -14)):
    colour = p.at_value(p.mix("glow", field, 1 - t), min(v + lift, 0.66))
    s.stroke(px_pts([(gx - 40, gy + dy + 10), (gx, gy + dy), (gx + 40, gy + dy + 8)]),
             "round_soft", colour, size=size, opacity=opacity, pressure="swell",
             clip=wall, note="lamplight")

# The gilding the lamp finds: the inner part of every ray above his head, re-struck.
s.dry()
for (ang, half), shape in zip(RAYS, rays):
    if not 20 <= ang <= 160:
        continue
    a = math.radians(ang)
    reach = 330 if 45 <= ang <= 135 else 270
    pts = [(SUN[0] + r * math.cos(a), SUN[1] - r * math.sin(a)) for r in (40, reach * 0.55, reach)]
    width = 2 * reach * math.tan(math.radians(half)) / CW + 0.012
    s.stroke(px_pts(pts), "flat", "ray_lit", size=width, clip=shape, solid=True,
             pressure=[1.0, 0.7, 0.0], note="ray lit")

# The corners going down toward dark: two soft films each side, wide and faint.
s.dry()
for path in ([(-60, 120), (120, 30), (300, -40)], [(-60, 330), (60, 200), (160, 60)],
             [(1084, 120), (904, 30), (724, -40)], [(1084, 330), (964, 200), (864, 60)]):
    s.glaze(px_pts(path), "wall_far", opacity=0.30, size=0.26, pressure=[0.6, 1.0, 0.6],
            clip=wall)
