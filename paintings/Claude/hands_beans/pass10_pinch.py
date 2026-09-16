# The pinch: the thing the picture is about, so it gets the brightest light, the
# hardest edge, and a dark laid right beside the light to make it snap. Dark first.
s.dry()

# the dark that separates the pinching fingers from the cupped hand behind them
s.stroke([(0.464, 0.499), (0.487, 0.504), (0.507, 0.500)], "round_hard", "palm_dk",
         size=0.010, opacity=0.70, load=1.0, load_falloff=0.20, tip_wobble=0.50,
         pressure=[0.15, 1.0, 0.25], note="subject")

# the index fingertip: its shadowed side, then the highest light in the painting
s.stroke([(0.499, 0.456), (0.486, 0.470), (0.477, 0.482)], "round_hard", "fl_body3",
         size=0.025, opacity=0.95, load=1.0, tip_wobble=0.40,
         pressure=[0.6, 1.0, 0.7], note="subject")
s.stroke([(0.494, 0.454), (0.483, 0.466), (0.475, 0.476)], "round_hard", "fl_high",
         size=0.012, opacity=1.0, load=1.0, load_falloff=0.10, tip_wobble=0.35,
         pressure=[0.35, 1.0, 0.5], note="subject")

# the thumb tip closing on it from below
s.stroke([(0.514, 0.492), (0.497, 0.489), (0.484, 0.487)], "round_hard", "fl_lit",
         size=0.016, opacity=1.0, load=1.0, load_falloff=0.15, tip_wobble=0.50,
         pressure=[0.25, 1.0, 0.7], note="subject")

# the one bean between them
s.dab(0.4805, 0.4835, "round_hard", "bean_dk", size=0.0095, press=3,
      tip_wobble=0.70, opacity=1.0, note="subject")
print(s.look(region="D4:F5"))
