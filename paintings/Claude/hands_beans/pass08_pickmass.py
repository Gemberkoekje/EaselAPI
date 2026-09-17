# The picking hand, in front of everything. Palm down, so its back faces the light
# and is the second-lightest mass in the picture. Its two fingers come down at
# 40-55 degrees across the cupped hand's near-horizontal run -- that crossing is
# the whole reason the left half stops reading as bands.
s.paint([{"shape": PICK, "brush": "bristle", "color": "fl_shad", "size": 0.086,
          "density": 1.0, "direction": ("axis", 34), "solid": True, "note": "subject"}])
s.dry()

# the forearm's lit edge, receding as it goes up out of frame
s.stroke(PICK_ARM_LIT[0][:3], "bristle", "fl_arm", size=0.050, opacity=0.70,
         load=0.85, load_falloff=0.80, pressure="lift_off", note="subject")

# the back of the hand: the plane that faces the light
s.paint([{"shape": PICK_BACK_LIT, "brush": "bristle", "color": "fl_plane",
          "size": 0.030, "density": 0.85, "direction": (58, 116), "load": 0.72,
          "load_falloff": 0.40, "opacity": 0.85, "note": "subject"}])
s.stroke([(0.648, 0.246), (0.700, 0.214), (0.756, 0.212)], "bristle", "fl_lit",
         size=0.030, opacity=0.78, load=0.60, load_falloff=0.45,
         pressure="swell", note="subject")

# the curled fingers, kept dark: one mark, no description
s.stroke([(0.700, 0.352), (0.752, 0.368), (0.782, 0.404)], "bristle", "fl_body3",
         size=0.048, opacity=0.85, load=0.70, load_falloff=0.40,
         pressure="swell", note="subject")

# the index: the finger doing the work, so it gets the firmest edge in the hand
s.stroke(PICK_INDEX[0], "bristle", "fl_body2", size=0.052, opacity=0.95,
         load=1.0, load_falloff=0.25, pressure="lift_off", note="subject")
s.stroke([(0.596, 0.302), (0.566, 0.348), (0.548, 0.382)], "round_hard", "fl_lit",
         size=0.015, opacity=0.88, load=1.0, load_falloff=0.20, tip_wobble=0.40,
         pressure=[0.35, 1.0, 0.55], note="subject")
s.stroke([(0.524, 0.416), (0.500, 0.450)], "round_hard", "fl_lit",
         size=0.012, opacity=0.80, load=1.0, tip_wobble=0.55,
         pressure=[0.5, 0.9], note="subject")

# the thumb: softer, and its lower edge is let go
s.stroke(PICK_THUMB[0], "bristle", "fl_body", size=0.056, opacity=0.90,
         load=0.85, load_falloff=0.40, pressure="lift_off", note="subject")
s.stroke([(0.626, 0.346), (0.572, 0.398), (0.528, 0.442)], "bristle", "fl_mid",
         size=0.024, opacity=0.70, load=0.55, load_falloff=0.45,
         pressure="swell", note="subject")

for x, y, sz, pr in [(0.628, 0.292, 0.026, 3), (0.668, 0.268, 0.024, 2),
                     (0.706, 0.258, 0.021, 2)]:
    s.dab(x, y, "round_hard", "fl_warm", size=sz, press=pr, tip_wobble=0.75,
          opacity=0.78, note="subject")
print(s.look())
