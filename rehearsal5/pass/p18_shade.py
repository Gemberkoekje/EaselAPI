REF = "C:/temp/Level1.jpg"

# the wall turning away toward the handle
s.stroke([(0.556, 0.322), (0.568, 0.470), (0.552, 0.618)], "flat", "mug_dark",
         size=0.050, pressure="even", load=1.0, note="wall turning")
s.stroke([(0.598, 0.334), (0.602, 0.462), (0.578, 0.596)], "flat", "mug_dark",
         size=0.044, pressure="even", load=1.0, note="wall turning")
# the lit left edge
s.stroke([(0.330, 0.252), (0.338, 0.432), (0.362, 0.608)], "flat", "mug_lit",
         size=0.044, pressure="even", load=1.0, note="lit edge")
# the band of light under the front lip
s.stroke([(0.358, 0.320), (0.430, 0.354), (0.502, 0.358), (0.562, 0.338)],
         "flat", "mug_hi", size=0.030, pressure="swell", load=1.0, note="under lip")
# the tea has to fill the opening
s.stroke([(0.350, 0.214), (0.374, 0.182), (0.414, 0.168)], "flat", "tea",
         size=0.030, pressure="even", load=1.0, note="tea")
s.stroke([(0.512, 0.302), (0.562, 0.292), (0.588, 0.262)], "flat", "tea",
         size=0.030, pressure="even", load=1.0, note="tea")
# the base
s.stroke([(0.374, 0.630), (0.432, 0.654), (0.492, 0.652), (0.542, 0.632)],
         "flat", "mug_lit", size=0.022, pressure="even", load=1.0, note="base band")
print("shading", s.stroke_count)

# the handle: a round tip has no axis to print into a curve
mid = [(0.641, 0.276), (0.678, 0.296), (0.700, 0.345), (0.702, 0.405),
       (0.680, 0.458), (0.638, 0.492), (0.600, 0.505)]
out = [(0.646, 0.262), (0.690, 0.285), (0.716, 0.344), (0.718, 0.410),
       (0.694, 0.470), (0.646, 0.508), (0.600, 0.521)]
inn = [(0.636, 0.292), (0.666, 0.310), (0.684, 0.350), (0.686, 0.402),
       (0.666, 0.444), (0.630, 0.474), (0.600, 0.488)]
s.stroke(mid, "round_hard", "mug_mid", size=0.034, pressure="even", load=1.0,
         note="handle")
s.stroke(mid, "round_hard", "mug_lit", size=0.022, pressure="swell", load=1.0,
         note="handle lit")
s.stroke(out, "round_hard", "mug_hi", size=0.011, pressure="swell", load=1.0,
         note="handle outer light")
s.stroke(inn, "round_hard", "mug_dark", size=0.010, pressure="swell", load=1.0,
         note="handle inner shade")
print("handle", s.stroke_count)

print(s.look(reference=REF))
print(s.look(region=span("C2", "G5"), reference=REF))
