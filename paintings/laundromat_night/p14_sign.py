# Signing it. Two marks, in the bottom-right corner, close in value to the wet road
# they sit on, and free because each carries note="signature".
#
# What I chose and why: the picture is one lit thing in a great deal of dark, so the
# mark is the smallest deliberate thing I could set down -- one short stroke and a
# shorter one under it. It is not a name, because I do not have one, and it is not a
# monogram standing in for one. It is two strokes in a corner, the second saying
# only that the first was meant. I put them on the dark side of the road where the
# reflection has already died, so they cost the picture nothing: not over a passage
# I was unhappy with, which would be a correction wearing a hat.
s.stroke([(0.9285, 0.9612), (0.9455, 0.9598), (0.9608, 0.9585)], "liner",
         p.at_value("kerb", 0.305), size=0.0050, opacity=0.85, load=1.0,
         load_falloff=0.0, pressure=[0.35, 1.0, 0.30], note="signature")
s.stroke([(0.9315, 0.9728), (0.9485, 0.9712)], "liner",
         p.at_value("kerb", 0.270), size=0.0040, opacity=0.75, load=1.0,
         load_falloff=0.0, pressure=[0.4, 1.0, 0.35], note="signature")
print(s.budget_line())
