# Pass 12. Thirty-two strokes were left and two passages are still ones I would
# apologise for: the stall riser under the window, which is a uniform dark band
# sitting directly beneath the subject, and the wall at the right edge, where the
# facade's vertical combing was never crossed.
#
# Deliberately no new objects. There are already nine small incidents in this
# picture -- two flyers, two pipes, a stain, a roof stack, a drain, a puddle, a wet
# patch -- and a tenth would be clutter. What these passages want is surface.
s.dry()

# The stall riser: a plinth line along its foot catching what comes back off the
# pavement, and two panel joints, unevenly placed and barely there.
s.stroke([(0.196, 0.6985), (0.430, 0.7025), (0.688, 0.6985)], "bristle",
         p.at_value("facade_lt", 0.268), size=0.011, load=0.85, load_falloff=0.15,
         opacity=0.60, pressure=[0.2, 1.0, 0.45], note="riser")
s.stroke([(0.3125, 0.6225), (0.3105, 0.6640), (0.3140, 0.7010)], "bristle",
         p.at_value("facade_dk", 0.150), size=0.009, load=0.85, opacity=0.55,
         pressure="swell", note="riser")
s.stroke([(0.5760, 0.6215), (0.5785, 0.6620), (0.5750, 0.7005)], "bristle",
         p.at_value("facade_dk", 0.152), size=0.008, load=0.80, opacity=0.45,
         pressure="swell", note="riser")
# and two marks across it, because a band with only horizontal and vertical marks
# in it is a band whatever is drawn on it
s.stroke([(0.218, 0.6980), (0.284, 0.6560), (0.336, 0.6265)], "bristle",
         p.at_value("facade_lt", 0.225), size=0.020, load=0.80, opacity=0.40,
         pressure="swell", note="riser")
s.stroke([(0.672, 0.6270), (0.606, 0.6580), (0.548, 0.6960)], "bristle",
         p.at_value("facade_lt", 0.205), size=0.024, load=0.85, opacity=0.35,
         pressure="swell", note="riser")

# The wall at the right edge: four marks crossing the combing at four angles, in and
# out of the sodium light, none of them parallel to another or to the canvas.
for pts, sz, val, ld, op in (
        ([(1.055, 0.268), (0.958, 0.306), (0.902, 0.292)], 0.030, 0.290, 0.85, 0.45),
        ([(0.912, 0.392), (0.982, 0.362), (1.055, 0.372)], 0.024, 0.230, 0.80, 0.40),
        ([(1.055, 0.512), (0.960, 0.482), (0.908, 0.502)], 0.028, 0.275, 0.85, 0.40),
        ([(0.922, 0.618), (1.000, 0.646), (1.055, 0.630)], 0.022, 0.245, 0.75, 0.35)):
    s.stroke(pts, "bristle", p.at_value("facade_lt", val), size=sz, load=ld,
             opacity=op, pressure="swell", note="right wall")

# The strip of wall between the roofline and the fascia, crossed twice.
s.stroke([(0.238, 0.2400), (0.340, 0.2285), (0.448, 0.2360)], "bristle",
         p.at_value("facade_lt", 0.205), size=0.018, load=0.80, opacity=0.40,
         pressure="swell", note="upper wall")
s.stroke([(0.782, 0.2360), (0.688, 0.2465), (0.598, 0.2395)], "bristle",
         p.at_value("facade_lt", 0.185), size=0.016, load=0.75, opacity=0.35,
         pressure="swell", note="upper wall")

# And one mark along the fascia, which has been one even value its whole length.
s.stroke([(0.828, 0.2890), (0.664, 0.2955), (0.508, 0.2905)], "bristle",
         p.at_value("facade_lt", 0.232), size=0.022, load=0.70, opacity=0.35,
         pressure="swell", note="fascia")
print(s.budget_line())
