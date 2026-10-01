"""The lantern behind Uktarl, on the relief right round him.

The lamp stands behind his chest, so the stone nearest his silhouette is the most lit thing
on the wall, and that is what separates a black body and a crimson wing from a dark
mountain. Soft strokes along his edges, each held to the relief beside him: one wide and
faint, one narrow and brighter, strongest at the lamp's height. Above his head the same
light meets the gilding, a glare where the rays converge.
"""
glow_left = poly_px([(446, 330), (456, 352), (468, 370), (480, 386), (489, 398), (466, 398), (447, 410), (436, 432), (428, 470), (422, 520), (416, 575), (410, 640), (290, 640), (290, 320)], "the relief left of him"); glow_right = poly_px([(668, 322), (676, 330), (690, 352), (700, 396), (698, 440), (708, 482), (700, 528), (704, 570), (690, 606), (680, 640), (812, 640), (812, 300), (668, 300)], "the relief right of him")  # the prelude's, as they then stood
base = s.sample(ell_px(380, 500, 26, 40))
p["backglow"] = p.at_value(p.mix("glow", base, 0.55), 0.38)
p["backglow_hot"] = p.at_value(p.mix("glow", base, 0.35), 0.48)
s.dry()
p["backglow_wide"] = p.at_value(p.mix("glow", base, 0.75), 0.29)
for region, path in ((glow_left, [(420, 400), (380, 470), (360, 540), (370, 620)]),
                     (glow_right, [(730, 380), (760, 450), (770, 520), (750, 610)])):
    s.stroke(px_pts(path), "round_soft", "backglow_wide", size=0.24, opacity=0.40,
             pressure=[0.3, 1.0, 0.8, 0.3], clip=region)
for region, path in ((glow_left, [(446, 390), (424, 460), (414, 540), (404, 630)]),
                     (glow_right, [(694, 360), (712, 440), (716, 520), (706, 610)])):
    s.stroke(px_pts(path), "round_soft", "backglow", size=0.11, opacity=0.55,
             pressure=[0.5, 1.0, 0.9, 0.4], clip=region)
    s.stroke(px_pts(path), "round_soft", "backglow_hot", size=0.045, opacity=0.6,
             pressure=[0.6, 1.0, 0.8, 0.3], clip=region)
s.stroke(px_pts([(470, 316), (512, 300), (556, 312)]), "round_soft",
         p.at_value(p.mix("ray_lit", "glow", 0.5), 0.56), size=0.075, opacity=0.5,
         pressure="swell", clip=glow_above)
