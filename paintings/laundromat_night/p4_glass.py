# Pass 4. The window is a hollow thing, so it is three masses at three depths and
# the order is the whole recipe: what is behind the inside, then the inside, then
# the near edge. This pass is the first of the three -- the lit back wall.
#
# dry() is not optional here. Exercise 4: cadmium yellow laid into wet ultramarine
# comes back olive. A 0.88 fluorescent laid into a wet 0.17 facade would do the same.
s.dry()

# The lit field, solid. Two rehearsals went on discovering that a scumble will not
# lay this: at size 0.050 on a 0.034 step its passes left dark gaps between them and
# the brightest mass in the picture came back a venetian blind, and at 0.095 the
# centre closed up but the first and last passes still wobbled off the boundary and
# left the facade showing along the top and bottom. So it is blocked in solid and
# graded with strokes afterwards. It fills the whole opening and is left to break
# past it -- the frame goes on top and that is what makes the opening's edge an edge.
# overhang defaults to 0 on a shape, so every pass stopped dead on the boundary and
# their wobble left dark bites out of the left edge. It is the ends of the passes it
# controls, which is exactly what was wrong.
s.block_in(window_open(), "flat", p.at_value("interior", 0.820), density=1.0,
           solid=True, size=0.055, direction=3, overhang=0.4, note="subject interior")

# The ceiling falls off downward: three passes the same way, one value step apart,
# each dying to nothing at one end so no pass has a visible termination.
for i in range(3):
    t = i / 2
    y = 0.404 + t * 0.048
    s.stroke([(0.176, y - 0.004), (0.450, y + 0.003), (0.724, y + 0.008)], "bristle",
             p.at_value("interior", 0.905 - 0.055 * t), size=0.042,
             load=1.0, load_falloff=0.0, opacity=0.55,
             pressure=[1.0, 0.7, 0.15], note="subject interior")

# The fluorescent tubes: the hottest thing inside, tilted off the horizontal, and
# with the overhang left to bloom past the strip because a light source should.
s.block_in(polygon([(0.196, 0.352), (0.470, 0.346), (0.710, 0.351),
                    (0.708, 0.388), (0.469, 0.384), (0.198, 0.391)]),
           "flat", p.at_value("interior", 0.945), density=1.0, solid=True,
           size=0.020, direction=2, note="subject tubes")
s.stroke([(0.192, 0.372), (0.290, 0.365)], "bristle", "wall_lo", size=0.030,
         load=0.80, opacity=0.55, pressure="lift_off", note="subject tubes lost")

# The glass door beside it. Varied on purpose rather than repeated: dimmer, because
# its light comes past the shelving, and its axis is vertical so its passes are too.
# No edge="clean" -- on a mass this narrow it insets half a brush from both sides and
# hands back a rounded lozenge, which is what one rehearsal made of this door. And
# barely any overhang: these passes run vertically, so overhang lengthens them
# downward -- at 0.6 the glass ran over its own kick panel and onto the sidewalk.
s.block_in(polygon([(0.782, 0.334), (0.893, 0.337), (0.895, 0.558), (0.783, 0.556)]),
           "flat", p.at_value("wall_lo", 0.690), density=1.0, solid=True,
           size=0.042, direction="axis", pressure="even", overhang=0.10,
           note="subject door glass")
# and a kick panel at its foot, which is not glass at all
s.block_in(polygon([(0.783, 0.560), (0.895, 0.562), (0.897, 0.699), (0.781, 0.696)]),
           "flat", p.at_value("machine", 0.300), density=1.0, solid=True,
           size=0.038, direction="axis", pressure="even", overhang=0.10,
           note="subject door panel")
print(s.budget_line())
