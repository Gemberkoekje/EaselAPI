# The back of the picking hand, third try. Starved gave lichen; a hard-edged
# block-in gave a smooth egg. Solid paint, crossed, with the strokes running off
# the shape so the silhouette stays broken. It sits away from the focal point and
# is meant to be quiet, not blank.
s.dry()
s.stroke([(0.612, 0.286), (0.688, 0.234), (0.766, 0.208), (0.818, 0.222)],
         "bristle", "fl_plane", size=0.060, opacity=0.95, load=1.0,
         load_falloff=0.30, pressure="swell", note="subject")
s.stroke([(0.802, 0.188), (0.756, 0.248), (0.700, 0.300)], "bristle", "fl_mid",
         size=0.048, opacity=0.72, load=1.0, load_falloff=0.45,
         pressure="swell", note="subject")
s.stroke([(0.646, 0.306), (0.714, 0.276), (0.788, 0.264)], "bristle", "fl_plane",
         size=0.034, opacity=0.60, load=0.95, load_falloff=0.50,
         pressure="swell", note="subject")
s.stroke([(0.820, 0.244), (0.776, 0.298), (0.730, 0.336)], "bristle", "fl_under",
         size=0.030, opacity=0.62, load=0.90, load_falloff=0.45,
         pressure="swell", note="subject")
for x, y, sz, pr, op in [(0.648, 0.282, 0.025, 3, 0.88), (0.692, 0.256, 0.021, 2, 0.68)]:
    s.dab(x, y, "round_hard", "fl_lit", size=sz, press=pr, tip_wobble=0.75,
          opacity=op, note="subject")
print(s.look(region="E2:H4"))
