# Highlights: smallest brush, fewest strokes. A droplet on a pane is two marks --
# the light caught on the top of its curve and the dark under it -- and there are
# only a handful, because every one added makes the others count for less.
p["wet"]    = p.at_value(p.mix(p["neutral"], "titanium_white", 0.62), 0.80)
p["wetdk"]  = p.at_value(p.desaturate(p.mix(p["neutral"], "viridian", 0.14), 0.40), 0.30)

for x, y, r in [(0.862, 0.672, 0.0075), (0.945, 0.744, 0.0055),
                (0.827, 0.514, 0.0048), (0.898, 0.830, 0.0090)]:
    s.dab(x + r * 0.30, y + r * 0.55, "round_hard", "wetdk", size=r * 1.5,
          press=2, tip_wobble=0.7, note="subject")
    s.dab(x - r * 0.25, y - r * 0.30, "round_hard", "wet", size=r,
          press=3, tip_wobble=0.5, note="subject")

# two that have started to run
for x, y0, y1, w in [(0.876, 0.556, 0.604, 0.0055), (0.958, 0.466, 0.498, 0.0042)]:
    s.stroke([(x, y0), (x + 0.0015, y1)], "liner", "wet", size=w,
             pressure=[0.35, 1.0], load=1.0, opacity=0.9, note="subject")
    s.dab(x + 0.0018, y1 + w, "round_hard", "wet", size=w * 1.25, press=3,
          tip_wobble=0.5, note="subject")

# the light along the meniscus of the three runnels that matter -- one side only,
# broken, and not the same side on each
s.stroke([(0.893, 0.300), (0.890, 0.415), (0.897, 0.470)], "liner", "wet",
         size=0.0032, pressure=[0.0, 0.85, 0.0], load=1.0, opacity=0.72, note="subject")
s.stroke([(0.983, 0.556), (0.979, 0.648)], "liner", "wet", size=0.0026,
         pressure=[0.7, 0.0], load=1.0, opacity=0.62, note="subject")
s.stroke([(0.839, 0.662), (0.843, 0.742)], "liner", "wet", size=0.0024,
         pressure=[0.0, 0.8], load=1.0, opacity=0.58, note="subject")

# the one warm thing in the picture, up a little: it is what the painting is about
s.dab(0.780, 0.884, "round_soft", "glow", size=0.026, press=2, note="subject")
s.dab(0.773, 0.877, "round_hard", p.at_value(p["glow"], 0.34), size=0.011,
      press=3, tip_wobble=0.7, note="subject")
