# What is inside the cup, and the thumb that closes it. The thumb rises across the
# fingers' run on purpose -- it is the one thing in this hand that is not horizontal.
s.dry()

# the picking hand is above and right of the palm: its shadow falls across the
# knuckles and the far side of the hollow
s.stroke([(0.586, 0.474), (0.540, 0.526), (0.508, 0.590)], "bristle", "fl_deep",
         size=0.070, opacity=0.45, load=1.0, load_falloff=0.40,
         pressure="swell", note="subject")

# beans in the palm: a granular mass, then five of them described, no two alike
s.stroke([(0.392, 0.532), (0.448, 0.548), (0.500, 0.540)], "bristle", "bean_palm",
         size=0.052, opacity=0.70, load=0.50, load_falloff=0.30,
         pressure="swell", note="subject")
s.stroke([(0.386, 0.570), (0.442, 0.582), (0.492, 0.570)], "bristle", "bean_palm",
         size=0.040, opacity=0.60, load=0.42, load_falloff=0.35,
         pressure="swell", note="subject")
s.stroke([(0.402, 0.526), (0.424, 0.534)], "round_hard", "bean_lit",
         size=0.013, opacity=0.90, load=1.0, pressure=[0.8, 0.3],
         tip_wobble=0.55, note="subject")
s.stroke([(0.452, 0.556), (0.476, 0.550)], "round_hard", "bean_lit",
         size=0.011, opacity=0.80, load=1.0, pressure=[0.4, 0.9],
         tip_wobble=0.65, note="subject")
s.dab(0.428, 0.566, "round_hard", "bean_lit", size=0.010, press=3,
      tip_wobble=0.75, opacity=0.85, note="subject")
s.dab(0.492, 0.534, "round_hard", "bean_palm", size=0.012, press=2,
      tip_wobble=0.70, opacity=0.70, note="subject")

# the thumb: body, then its lit upper edge
s.stroke(CUP_THUMB[0], "bristle", "fl_body", size=0.060, opacity=0.95,
         load=1.0, load_falloff=0.30, pressure="lift_off", note="subject")
s.stroke(CUP_THUMB_LIT[0], "bristle", "fl_mid", size=0.028, opacity=0.82,
         load=0.58, load_falloff=0.40, pressure="swell", note="subject")
s.stroke([(0.572, 0.678), (0.516, 0.658), (0.470, 0.632)], "round_hard", "fl_lit",
         size=0.013, opacity=0.62, load=1.0, load_falloff=0.30,
         tip_wobble=0.45, pressure=[0.3, 1.0, 0.5], note="subject")
print(s.look(region="C3:F6"))
