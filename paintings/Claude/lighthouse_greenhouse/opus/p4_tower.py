# The tower, over the beam so that the lantern will cut the beam's root. Not a
# mass with marks on it: the planes it is made of, tiling it, with the block-in's
# dark left showing along the shadow edge as the silhouette.
s.dry()

# The whole thing goes down in the shadow colour, vertically, contour drawn --
# the silhouette here *is* the drawing, and a bristle would leave it stringy.
s.block_in(tower(), "flat", "tower_sh", size=0.035, density=1.0, solid=True,
           direction=90, edge="clean", note="subject tower")

# Two planes on it, each a shape laid over the mass rather than a value change
# inside it, and each a different tip because they are different kinds of
# surface: the body combed, the lit band solid. direction=90 on both -- left off,
# these cost 44 and 57 instead of 9, because the default sweeps horizontally and
# steps down the whole height of the tower.
s.block_in(tower_mid_face(), "bristle", "tower_mid", size=0.027, density=1.0,
           solid=True, opacity=1.0, pressure="even", direction=90,
           note="subject tower")
# The lit band is combed too, not chiselled: laid with a `flat`, every vertical
# pass ended in a hard horizontal edge and the sloping boundary came back as a
# staircase down the right of the tower. One solid stroke down its middle
# afterwards gives it back the core a comb will not lay.
s.block_in(tower_lit_face(), "bristle", "tower_lit", size=0.022, density=1.0,
           solid=True, opacity=1.0, pressure="even", direction=90,
           note="subject tower")
s.stroke([(0.325, 0.272), (0.332, 0.540), (0.350, 0.886)], "flat", "tower_lit",
         size=0.019, opacity=1.0, load=1.0, load_falloff=0.0, pressure="even",
         note="subject tower")

# The joins. Four marks, two to a join, straddling it with a starved comb at an
# intermediate value: without them the planes meet at a step and the tower is
# three stripes rather than a cylinder. They follow the taper, so they are three
# points each and not two.
for path, colour, size, op, load in (
        ([(0.2235, 0.276), (0.2100, 0.540), (0.1815, 0.880)],
         p.mix("tower_sh", "tower_mid", 0.55), 0.034, 0.70, 0.55),
        ([(0.2170, 0.300), (0.2040, 0.560), (0.1770, 0.860)],
         p.mix("tower_sh", "tower_mid", 0.35), 0.021, 0.55, 0.40),
        ([(0.3035, 0.278), (0.3110, 0.540), (0.3290, 0.880)],
         p.mix("tower_mid", "tower_lit", 0.5), 0.026, 0.65, 0.50),
        ([(0.3090, 0.330), (0.3175, 0.600), (0.3360, 0.850)],
         p.mix("tower_mid", "tower_lit", 0.75), 0.015, 0.50, 0.35)):
    s.stroke(path, "bristle", colour, size=size, opacity=op, load=load,
             load_falloff=0.15, pressure="even", note="subject tower")

# The gallery plate the stair arrives at. The lantern goes on top of it next
# pass; its front rail goes on over the lantern, because that is in front.
s.block_in(gallery(), "flat", "iron", size=0.014, density=1.0, solid=True,
           direction="axis", note="subject tower")

s.dry()      # or the three runs below mix away into paint that is still wet

# What the damp has done to the whitewash. Three runs, none straight, none the
# same length, and one of them barely there -- a surface's grain varies, or it is
# a stack of stripes with a different name.
s.stroke([(0.246, 0.288), (0.238, 0.404), (0.249, 0.512)], "bristle", "stain",
         size=0.017, load=0.55, opacity=0.8, pressure=[0.9, 0.5, 0.0],
         note="subject tower")
s.stroke([(0.326, 0.500), (0.332, 0.614), (0.324, 0.688)], "bristle", "stain",
         size=0.011, load=0.45, opacity=0.6, pressure="lift_off",
         note="subject tower")
s.stroke([(0.197, 0.664), (0.189, 0.748)], "bristle",
         p.mix("stain", "tower_mid", 0.45), size=0.024, load=0.30, opacity=0.5,
         pressure="swell", note="subject tower")

print(s.look(grid=True))
print(s.look(region="B2:D8"))
