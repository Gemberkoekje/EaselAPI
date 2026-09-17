# Highlights: smallest brush, fewest marks. The first version put four discs in
# one small area, which is the tool printing itself. One spark at the pinch; the
# knuckles get a length instead, so they are marks and not dots.
s.dry()

# the single highest light in the painting
s.dab(0.4838, 0.4638, "round_hard", "fl_spark", size=0.0072, press=3,
      tip_wobble=0.65, opacity=1.0, note="subject")

# the knuckles: short marks along the ridge, not stamps on it
s.stroke([(0.4930, 0.4380), (0.5085, 0.4470)], "round_hard", "fl_high",
         size=0.0090, opacity=0.80, load=1.0, load_falloff=0.30,
         tip_wobble=0.55, pressure=[0.35, 0.95], note="subject")
s.stroke([(0.4880, 0.4830), (0.5040, 0.4925)], "round_hard", "fl_high",
         size=0.0105, opacity=0.88, load=1.0, load_falloff=0.30,
         tip_wobble=0.55, pressure=[0.9, 0.3], note="subject")

# one broken catch-light along the NEAR edge of the cup -- the mark that makes a
# hollow thing read as hollow, and the only mark on it
s.stroke([(0.470, 0.7255), (0.545, 0.7395), (0.610, 0.7235)], "round_hard",
         "fl_lit", size=0.0085, opacity=0.95, load=1.0, load_falloff=0.35,
         tip_wobble=0.35, pressure=[0.15, 1.0, 0.35], note="subject")

# the leading knuckle of the picking hand, kept a step below the cupped hand's
s.stroke([(0.6395, 0.2840), (0.6545, 0.2735)], "round_hard", "fl_high",
         size=0.0095, opacity=0.68, load=1.0, tip_wobble=0.60,
         pressure=[0.8, 0.25], note="subject")

# one bean in the palm catches the light, and only one
s.dab(0.4355, 0.5495, "round_hard", "bean_lit", size=0.0062, press=3,
      tip_wobble=0.75, opacity=0.82, note="subject")
print(s.look(region="D4:F5"))
print(s.look())
