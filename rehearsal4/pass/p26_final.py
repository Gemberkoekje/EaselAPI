"""Pass K - fourteen last marks. Every one is a single stroke, counted.
The dark ones inside the rim do two jobs: they fix E2/E3 and they narrow the
rim, which had grown into a fat white horseshoe."""
p = s.palette
s.dry()
start = s.stroke_count

s.stroke([(0.560, 0.178), (0.584, 0.222), (0.578, 0.264)], "flat", "tea",
         size=0.040, pressure="even", load=1.0, note="inner right wall")
s.stroke([(0.380, 0.166), (0.470, 0.150), (0.548, 0.170)], "flat", "tea",
         size=0.038, pressure="even", load=1.0, note="inner back wall")
s.stroke([(0.352, 0.210), (0.347, 0.258), (0.374, 0.290)], "flat", "tea",
         size=0.034, pressure="even", load=1.0, note="inner left wall")
s.stroke([(0.600, 0.268), (0.607, 0.330), (0.604, 0.374)], "flat",
         p.mix(p["mug_face"], p["mug_shade"], 0.55), size=0.036,
         pressure="even", load=1.0, note="mug upper right, darker")
s.stroke([(0.392, 0.418), (0.450, 0.407), (0.496, 0.421)], "flat", "crew",
         size=0.030, pressure="even", load=1.0, note="head, top")
s.stroke([(0.500, 0.430), (0.508, 0.482)], "flat", "crew", size=0.028,
         pressure="even", load=1.0, note="his right shoulder")
s.stroke([(0.876, 0.636), (0.985, 0.692)], "flat",
         p.mix(p["table_lit"], p["table_base"], 0.72), size=0.095,
         pressure="even", load=1.0, note="H6 down")

# highlights: few, deliberate, smallest brush, last
s.stroke([(0.316, 0.240), (0.333, 0.184), (0.372, 0.146), (0.426, 0.126)],
         "round_hard", "mug_hi", size=0.009, pressure=[0.4, 1.0, 0.9, 0.5],
         note="rim light, front left")
s.stroke([(0.520, 0.127), (0.566, 0.153), (0.598, 0.192)], "round_hard",
         "mug_hi", size=0.008, pressure=[0.8, 0.6, 0.2], note="rim light, right")
s.stroke([(0.398, 0.694), (0.470, 0.707), (0.532, 0.695)], "flat", "mug_rim",
         size=0.015, pressure="even", load=1.0, note="reflected light, base")
s.stroke([(0.640, 0.310), (0.674, 0.342)], "flat", "mug_rim", size=0.013,
         pressure="even", load=1.0, note="light on the handle")
s.dab(0.545, 0.262, "round_hard", "mug_hi", size=0.010, press=3)

# two edges lost on purpose
s.smudge([(0.352, 0.330), (0.357, 0.470)], size=0.035)
s.smudge([(0.556, 0.762), (0.470, 0.802)], size=0.045)

print("this pass:", s.stroke_count - start, " total:", s.stroke_count)
print(s.look())
print(s.look(values=True, reference="ref.jpg"))
