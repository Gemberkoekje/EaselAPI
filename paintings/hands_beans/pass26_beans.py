# Three of the four fingertips are deliberately lost into the table. One is found,
# because a viewer needs a single unmistakable fingertip to read the rest as
# fingers -- three lost and one found is the varied edge the checklist asks for,
# where four lost is just a soft passage.
s.dry()
s.stroke([(0.346, 0.492), (0.322, 0.496), (0.306, 0.488)], "round_hard", "fl_core",
         size=0.011, opacity=0.82, load=1.0, load_falloff=0.25, tip_wobble=0.45,
         pressure=[0.3, 1.0, 0.5], note="subject")
s.stroke([(0.352, 0.470), (0.330, 0.466), (0.316, 0.472)], "round_hard", "fl_lit",
         size=0.013, opacity=0.92, load=1.0, load_falloff=0.20, tip_wobble=0.40,
         pressure=[0.4, 1.0, 0.45], note="subject")
s.dab(0.3245, 0.4735, "round_hard", "fl_high", size=0.0062, press=3,
      tip_wobble=0.70, opacity=0.85, note="subject")

# beans on the table. Sorting means some are put down, and four of them say what
# the picture is about more plainly than anything else could at this cost. No two
# are laid the same way, and one sits well apart so they are not a handful.
s.stroke([(0.312, 0.700), (0.332, 0.708)], "round_hard", "bean_warm", size=0.0125,
         opacity=0.92, load=1.0, tip_wobble=0.60, pressure=[0.85, 0.30],
         note="table")
s.dab(0.3630, 0.7480, "round_hard", "bean_lit", size=0.0105, press=3,
      tip_wobble=0.75, opacity=0.88, note="table")
s.stroke([(0.286, 0.772), (0.302, 0.780)], "round_hard", "bean", size=0.0095,
         opacity=0.70, load=1.0, tip_wobble=0.70, pressure=[0.35, 0.9],
         note="table")
s.dab(0.1985, 0.6485, "round_hard", "bean_warm", size=0.0085, press=3,
      tip_wobble=0.65, opacity=0.62, note="table")
# two of them cast a shadow, which is what sets them on the table rather than in it
s.stroke([(0.330, 0.710), (0.346, 0.716)], "round_hard", "tbl_deep", size=0.0075,
         opacity=0.55, load=1.0, tip_wobble=0.55, pressure=[0.8, 0.15], note="table")
s.stroke([(0.372, 0.756), (0.388, 0.762)], "round_hard", "tbl_deep", size=0.0070,
         opacity=0.48, load=1.0, tip_wobble=0.60, pressure=[0.8, 0.15], note="table")
print(s.look(region="B5:E7"))
print(s.look())
