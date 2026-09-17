# Pass 8. Edges.
#
# The first version of this pass was five smudges, and four of them failed in the
# way the guide says they will. At size 0.024-0.032 on a boundary between a glow and
# a 0.17 wall, smudge does not blur the join -- it walks the light mass into the
# dark side and leaves a pale finger-shaped lobe, which it duly did on both piers,
# on the roofline, and worst of all as a blob sitting on the open road. So almost
# all of it is paint now, and the one smudge left is a third of the size.
s.dry()

# The piers. What was reading as a hard bright strip is the interior's own overhang
# past the jamb, so it gets broken up with a starved brush in a value between the
# glow and the wall -- three marks down each side, no two alike, which reads as
# light falling off rather than as a strip with an edge.
for y0, y1, sz, val, ld in ((0.352, 0.446, 0.024, 0.255, 0.55),
                            (0.430, 0.520, 0.018, 0.290, 0.40),
                            (0.508, 0.598, 0.022, 0.240, 0.60)):
    s.stroke([(0.1520, y0), (0.1480, 0.5 * (y0 + y1)), (0.1545, y1)], "bristle",
             p.at_value("facade_lt", val), size=sz, load=ld, opacity=0.55,
             pressure="swell", note="edge soft")
for y0, y1, sz, val, ld in ((0.356, 0.462, 0.020, 0.235, 0.50),
                            (0.448, 0.594, 0.016, 0.265, 0.45)):
    s.stroke([(0.7420, y0), (0.7455, 0.5 * (y0 + y1)), (0.7405, y1)], "bristle",
             p.at_value("facade_lt", val), size=sz, load=ld, opacity=0.50,
             pressure="swell", note="edge soft")

# The one surviving smudge, at a third of the size it failed at: the fascia's lower
# edge, lost for one stretch in the middle so the board is not outlined all the way
# across. Along the boundary, handed its own curve, one pass.
s.smudge([(0.352, 0.3260), (0.418, 0.3272), (0.484, 0.3278), (0.548, 0.3270)],
         size=0.011, note="edge lost")

# The far-right roofline, thrown away into the sky with the sky's own colour rather
# than by dragging the building into it. The parapet keeps its edge; this end does
# not, so the eye has somewhere to leave the picture.
s.stroke([(0.906, 0.2165), (0.958, 0.2135), (1.058, 0.2110)], "bristle", "sky_lo",
         size=0.026, load=0.55, opacity=0.40, pressure="swell", note="edge lost")

# The figure's base, into the sill's shadow: a starved brush at half opacity in a
# value between the two, laid ACROSS where they meet. This is the mark that a smudge
# run across a boundary is trying to be and cannot.
s.stroke([(0.578, 0.5985), (0.614, 0.6035), (0.650, 0.5975)], "bristle",
         p.mix("figure", "machine", 0.35), size=0.020, load=0.60, opacity=0.45,
         pressure="swell", note="edge lost")
s.stroke([(0.596, 0.5945), (0.640, 0.5995)], "bristle",
         p.mix("figure", "frame", 0.4), size=0.014, load=0.70, opacity=0.40,
         pressure="taper", note="edge lost")

# ...and one edge deliberately FOUND, because an image where everything is soft is
# as flat as one where everything is sharp. The kerb, in the stretch where the pool
# crosses it: the road's own colour laid up to where the sidewalk stops, brush
# centre on the road side, which is the only way an edge should be sharpened.
s.stroke([(0.436, 0.7885), (0.560, 0.7825), (0.684, 0.7765)], "flat",
         p.at_value("asphalt", 0.255), size=0.013, load=1.0, load_falloff=0.0,
         opacity=0.95, pressure="even", jitter=0.004, note="edge found")
s.stroke([(0.448, 0.7805), (0.566, 0.7745), (0.672, 0.7690)], "round_hard",
         p.at_value("spill_cool", 0.545), size=0.0045, opacity=0.85, load=1.0,
         load_falloff=0.0, pressure=[0.2, 1.0, 0.25], note="edge found")
print(s.budget_line())
