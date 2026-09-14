s.dry()
# The far deck was the flattest passage in the picture and a horizontal band across
# it besides. It gets the ground's own job: light falling off toward the wall, and
# wet streaks running back from the water that cross the band instead of lying in it.
s.glaze([(0.22, 0.300), (0.50, 0.330), (0.78, 0.352)], p.at_value("deck", 0.25),
        opacity=0.42, size=0.075, pressure="swell")
s.glaze([(0.62, 0.372), (0.85, 0.400), (1.05, 0.420)], p.at_value("deck", 0.27),
        opacity=0.32, size=0.060, pressure="taper")

streak = [([(0.245, 0.632), (0.236, 0.556), (0.231, 0.494)], 0.036, 0.62, 0.52, "lift_off"),
          ([(0.336, 0.562), (0.324, 0.442), (0.317, 0.352)], 0.030, 0.56, 0.54, "lift_off"),
          ([(0.431, 0.486), (0.422, 0.392), (0.419, 0.324)], 0.027, 0.50, 0.50, "lift_off"),
          ([(0.656, 0.506), (0.669, 0.424)],                 0.032, 0.46, 0.48, "lift_off"),
          ([(0.901, 0.586), (0.919, 0.502), (0.927, 0.436)], 0.028, 0.42, 0.47, "taper")]
for pts, size, load, val, press in streak:
    s.stroke(pts, "bristle", p.at_value("deck", val), size=size, load=load,
             opacity=0.80, load_falloff=0.45, pressure=press)

s.stroke([(0.498, 0.432), (0.578, 0.448)], "bristle", p.at_value("deck", 0.29),
         size=0.026, load=0.55, opacity=0.60, load_falloff=0.4, pressure="taper")
s.stroke([(0.826, 0.498), (0.904, 0.518)], "bristle", p.at_value("deck", 0.30),
         size=0.028, load=0.50, opacity=0.55, load_falloff=0.4, pressure="swell")
print(s.look(region="A3:H6"))
