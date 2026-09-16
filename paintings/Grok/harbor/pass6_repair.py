# Pass 6: bury the hole in the near water, then stop.
s.dry()
s.stroke([(0.72, 0.92), (0.88, 0.935), (1.05, 0.92)], "flat", "water_near",
         size=0.04, opacity=1.0, load=1.0, load_falloff=0.0, pressure="even")
s.look(path="pass6_colour.png")
s.export("harbor.png")
