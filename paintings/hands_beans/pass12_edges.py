# Edges: found where the picture is about something, lost where it is not.
s.unguide()
s.dry()

# FOUND -- the picking finger crosses in front of the cupped hand, and nothing
# says so yet. Sharpen it by painting the mass on the OTHER side of the edge:
# the cupped hand's dark laid up to where the finger stops.
s.stroke([(0.562, 0.378), (0.536, 0.414), (0.510, 0.450)], "round_hard", "palm_dk",
         size=0.011, opacity=0.62, load=1.0, load_falloff=0.30, tip_wobble=0.45,
         pressure=[0.2, 1.0, 0.35], note="subject")
s.stroke([(0.596, 0.318), (0.572, 0.350)], "round_hard", "palm_dk",
         size=0.012, opacity=0.70, load=1.0, tip_wobble=0.50,
         pressure=[0.8, 0.25], note="subject")

# LOST -- the cupped hand's far fingertips go into the table and do not come back
s.smudge([(0.300, 0.424), (0.284, 0.452), (0.278, 0.486), (0.288, 0.522)])
s.stroke([(0.322, 0.408), (0.286, 0.442), (0.272, 0.484)], "bristle", "fl_shad",
         size=0.030, opacity=0.42, load=0.48, load_falloff=0.50,
         pressure="swell", note="subject")
s.stroke([(0.258, 0.462), (0.296, 0.494), (0.330, 0.516)], "bristle", "tbl_lit",
         size=0.026, opacity=0.38, load=0.42, load_falloff=0.55,
         pressure="swell", note="subject")

# LOST -- the picking forearm's outer edge, high up, dissolves into the dark
s.smudge([(0.884, 0.052), (0.868, 0.108), (0.848, 0.168)])
s.stroke([(0.906, 0.070), (0.870, 0.128), (0.842, 0.192)], "bristle", "cast",
         size=0.034, opacity=0.40, load=0.45, load_falloff=0.50,
         pressure="swell", note="subject")

# LOST -- the bowl's right side goes under the cupped forearm and stays there
s.smudge([(0.360, 0.812), (0.396, 0.860), (0.412, 0.914)])
print(s.look())
