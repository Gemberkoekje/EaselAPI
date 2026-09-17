# The lantern: the thing the picture is about. It is a hollow thing, so it is
# three depths and they go on in this order -- what is behind the inside, the
# inside, then what is in front of it. Painted the other way round the vine runs
# out over its own frame and no later mark puts it back.
s.dry()

# 1. Behind the inside: the far panes, and the fog through them. A shade darker
#    and cooler than the open fog, which is what glass with a garden behind it
#    does to a grey day.
s.block_in(lantern(), "flat", "glass", size=0.045, density=0.9, solid=True,
           direction=90, edge="clean", note="subject lantern")

# 2. The inside. Crossed, because a tangle is the one mass in this picture that
#    genuinely has no direction.
s.block_in(vines(), "bristle", "leaf_dark", size=0.030, density=1.0, solid=True,
           direction=(28, 112), note="subject lantern")

s.dry()

# Leaves flattened on the panes, which is what makes it *pressing* rather than
# merely full: four of them, all different sizes, none of them a disc, and the
# lightest one is a leaf with the fog coming through it.
for pts, colour, size, load, op, press in (
        ([(0.180, 0.148), (0.199, 0.141), (0.213, 0.150)], "leaf_mid",
         0.020, 0.75, 0.9, "swell"),
        ([(0.232, 0.206), (0.252, 0.213), (0.268, 0.205)], "leaf_lit",
         0.016, 0.8, 0.85, [0.2, 1.0, 0.3]),
        ([(0.286, 0.128), (0.306, 0.134)], "leaf_mid",
         0.013, 0.6, 0.8, "lift_off"),
        ([(0.198, 0.186), (0.216, 0.196), (0.234, 0.190)], "leaf_lit",
         0.011, 0.85, 0.9, [0.3, 1.0, 0.15])):
    s.stroke(pts, "bristle", colour, size=size, load=load, opacity=op,
             pressure=press, note="subject lantern")

# Two clumps at a middle value, so the tangle is a tangle and not a lump.
s.stroke([(0.206, 0.166), (0.228, 0.178), (0.246, 0.170)], "bristle",
         p.at_value("leaf_mid", 0.27), size=0.026, load=0.8, opacity=0.85,
         pressure="swell", note="subject lantern")
s.stroke([(0.300, 0.196), (0.322, 0.204)], "bristle",
         p.at_value("leaf_mid", 0.30), size=0.020, load=0.7, opacity=0.8,
         pressure=[0.4, 1.0, 0.2], note="subject lantern")

# The lamp, still turning, seen through all of that. The lightest thing in the
# picture and about forty pixels of it. press=3 because press=1 is a whisper.
s.stroke([(0.288, 0.162), (0.308, 0.170)], "bristle",
         p.mix("lamp", "leaf_lit", 0.35), size=0.026, load=1.0, opacity=0.8,
         pressure="swell", note="subject lantern")
s.dab(0.299, 0.166, "round_hard", "lamp", size=0.013, press=3, tip_wobble=0.35,
      note="subject lantern")

# Two slivers where the foliage has not reached the glass, worked in from the
# frame rather than dabbed into the middle: a hole in a mass opens at its edge,
# and a pale dot in the interior is a floating disc whatever it is meant to be.
s.stroke([(0.1690, 0.214), (0.1840, 0.206), (0.1960, 0.211)], "bristle",
         p.at_value("glass", 0.64), size=0.013, load=0.35, opacity=0.75,
         pressure=[1.0, 0.55, 0.0], note="subject lantern")
s.stroke([(0.3420, 0.124), (0.3270, 0.119)], "bristle",
         p.at_value("glass", 0.61), size=0.010, load=0.28, opacity=0.65,
         pressure=[1.0, 0.0], note="subject lantern")

# 3. In front of the inside: the frame. Two astragals and the corner posts, and
#    no more -- with three, thicker, the lantern came back as a cage and the
#    thing inside it stopped being the point. What varies between them is their
#    weight and how much vine has got in front of each, not where they are.
for x0, x1, size, op, press in ((0.2055, 0.2030, 0.0026, 0.80, [1.0, 0.25, 0.9]),
                                (0.3015, 0.3000, 0.0030, 0.70, [0.9, 0.15, 1.0])):
    s.stroke([(x0, 0.112), (x1, 0.232)], "liner", "iron", size=size, opacity=op,
             pressure=press, note="subject lantern")
s.stroke([(0.1635, 0.110), (0.1680, 0.233)], "liner", "iron", size=0.0040,
         opacity=1.0, pressure="even", note="subject lantern")
s.stroke([(0.3465, 0.110), (0.3425, 0.233)], "liner", "iron", size=0.0040,
         opacity=1.0, pressure="even", note="subject lantern")

# 4. The cap, and the vent somebody has propped open.
s.block_in(roof(), "flat", p.at_value("iron", 0.235), size=0.016, density=1.0,
           solid=True, direction=0, edge="clean", note="subject lantern")
s.stroke([(0.206, 0.0795), (0.256, 0.0775), (0.304, 0.0795)], "round_hard",
         p.at_value("iron", 0.52), size=0.006, opacity=0.95,
         pressure=[0.3, 1.0, 0.25], note="subject lantern")
s.stroke([(0.2555, 0.078), (0.2565, 0.056)], "liner", p.at_value("iron", 0.30),
         size=0.005, opacity=0.95, pressure=[1.0, 0.5], note="subject lantern")
s.stroke([(0.246, 0.066), (0.232, 0.040), (0.252, 0.024)], "bristle", "leaf_mid",
         size=0.011, load=0.7, opacity=0.85, pressure=[1.0, 0.7, 0.0],
         note="subject lantern")

# And one shoot that has found its way out through a pane, on the side away from
# the beam so the two do not have to share the same corner.
s.stroke([(0.166, 0.196), (0.144, 0.212), (0.128, 0.238)], "bristle", "leaf_mid",
         size=0.010, load=0.65, opacity=0.8, pressure=[1.0, 0.6, 0.0],
         note="subject lantern")

# 5. The gallery rail, in front of everything the lantern is made of, and the
#    brackets under the walkway -- which are there to stop the plate reading as
#    the rectangle it was blocked in as.
s.stroke([(0.134, 0.2215), (0.256, 0.2245), (0.376, 0.2205)], "liner", "iron",
         size=0.0045, opacity=0.8, pressure=[0.3, 1.0, 0.45],
         note="subject lantern")
for bx, by0, by1, sz in ((0.152, 0.221, 0.238, 0.004),
                         (0.236, 0.223, 0.239, 0.0035),
                         (0.358, 0.221, 0.238, 0.004)):
    s.stroke([(bx, by0), (bx, by1)], "liner", "iron", size=sz, opacity=0.75,
             pressure="even", note="subject lantern")
for path in ([(0.176, 0.266), (0.186, 0.284)], [(0.330, 0.266), (0.318, 0.286)],
             [(0.252, 0.267), (0.254, 0.281)]):
    s.stroke(path, "round_hard", p.at_value("iron", 0.22), size=0.007,
             opacity=0.9, pressure=[1.0, 0.2], note="subject lantern")

print(s.look(region="A1:F4"))
print(s.look(grid=True))
