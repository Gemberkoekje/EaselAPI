# Pass 10. The highlights: smallest brushes, fewest marks. Eight of them, and every
# one is press=3 or a full-load stroke -- press=1 and press=2 are whispers, and a
# mark laid as a whisper because one is being careful simply does not register.
import math
s.dry()

# 1. The figure's rim. It is backlit, so light wraps the head and the near shoulder
# and nothing else. A tapered arc: the pressure list is the recipe, because a round
# tip's width follows pressure, so the horns thin to points and only the middle is
# the width asked for. s.aspect in the y term keeps the arc circular.
# Rehearsed once over the crown of the head at 0.470 and size 0.0055, and it read
# as a white hat -- a bright cap on the one shape the whole picture is aimed at. So
# it runs down the right side only, at a third of the contrast and two-thirds the
# width: on a backlit head the light wraps the edge, it does not sit on top.
cx, cy, r = 0.629, 0.486, 0.0170
arc = [(cx + r * math.cos(math.radians(a)),
        cy + r * s.aspect * math.sin(math.radians(a)))
       for a in (-58, -20, 18, 52)]
s.stroke(arc, "round_hard", p.at_value("figure", 0.330), size=0.0035, opacity=0.65,
         load=1.0, load_falloff=0.0, pressure=[0.05, 0.9, 0.8, 0.05],
         note="subject accent")

# 2. The hottest core of the tubes -- a smear with a bend, not a dot.
s.stroke([(0.372, 0.3695), (0.424, 0.3665), (0.468, 0.3690)], "bristle", "hot",
         size=0.016, load=0.85, opacity=0.70, pressure="swell", note="subject accent")

# 3. The brightest catch on the sill, where the light is squarest on. Given a
# length rather than laid as a dab: on its own in the middle of a long member, a
# dot reads as a speck of dirt rather than as a catch of light.
s.stroke([(0.3745, 0.6068), (0.4020, 0.6072)], "round_hard",
         p.at_value("hot", 0.690), size=0.0050, opacity=0.85, load=1.0,
         load_falloff=0.0, pressure=[0.15, 1.0, 0.2], note="subject accent")

# 4. Where the left mullion lands on the sill: the one junction in the frame that
# gets a highlight, so the frame is not uniformly black everywhere.
s.dab(0.3375, 0.6035, "round_hard", p.at_value("spill_cool", 0.520), size=0.0055,
      press=3, tip_wobble=0.30, note="subject accent")

# 5. The door's handle. One small vertical mark, and it is the thing that says a
# person comes out of here.
s.stroke([(0.8835, 0.4525), (0.8842, 0.4885)], "round_hard",
         p.at_value("mach_hi", 0.720), size=0.005, opacity=0.9, load=1.0,
         load_falloff=0.0, pressure=[0.35, 1.0, 0.4], note="subject accent")

# 6. The brightest note in the reflection, just under the kerb where it is freshest.
s.stroke([(0.4055, 0.7705), (0.4010, 0.7960), (0.3985, 0.8180)], "bristle",
         p.at_value("refl_hi", 0.640), size=0.010, load=1.0, load_falloff=0.20,
         opacity=0.70, pressure=[1.0, 0.5, 0.0], note="subject accent")

# 7. The wettest stretch of kerb.
s.stroke([(0.592, 0.7742), (0.634, 0.7722)], "round_hard",
         p.at_value("spill_cool", 0.600), size=0.0040, opacity=0.85, load=1.0,
         load_falloff=0.0, pressure=[0.2, 1.0, 0.2], note="subject accent")

# 8. The fascia's right end, where the sodium lamp reaches it. The picture's one
# warm highlight, and it is the furthest thing from the window on purpose.
s.stroke([(0.8985, 0.2705), (0.8845, 0.2790)], "round_hard",
         p.at_value("spill", 0.420), size=0.0045, opacity=0.8, load=1.0,
         load_falloff=0.0, pressure=[0.3, 1.0, 0.2], note="accent lamp")
print(s.budget_line())
