# Pass 5: the finish. Break the comb, lose one edge, add the last light, sign.
s.dry()

# two starved swell lines at an angle -- the marks that break the stack of bars
s.stroke([(-0.05, 0.66), (0.35, 0.645), (0.80, 0.66), (1.05, 0.645)], "bristle", "cloud_pale",
         size=0.020, load=0.35, opacity=0.30, pressure="swell")
s.stroke([(1.05, 0.88), (0.60, 0.895), (0.15, 0.885), (-0.05, 0.90)], "bristle", "cloud_pale",
         size=0.016, load=0.30, opacity=0.25, pressure="swell")

# lose the right half of the horizon completely: one smudge, then paint across it
s.smudge([(0.68, 0.518), (0.84, 0.512), (1.06, 0.508)])
s.stroke([(0.68, 0.516), (0.86, 0.510), (1.06, 0.506)], "bristle",
         p.mix("amber", "water_coral", 0.5), size=0.030, load=0.55,
         opacity=0.50, pressure="swell")

# the boat's waterline: half lost into the water toward the stern
s.smudge([(0.70, 0.578), (0.76, 0.565)])

# one quiet ripple near the viewer, then the two last sparks
s.stroke([(0.40, 0.84), (0.62, 0.855), (0.90, 0.845)], "bristle", "teal_deep",
         size=0.018, load=0.6, opacity=0.6, pressure="swell")
s.dab(0.335, 0.700, "round_hard", "gold", size=0.010, press=3, tip_wobble=0.7)
s.dab(0.272, 0.635, "round_hard", "gold", size=0.008, press=3, tip_wobble=0.7)

# the signature: a small mark in the corner, out of the picture's way
s.stroke([(0.86, 0.94), (0.90, 0.92)], "liner", "boat_dark", size=0.006,
         note="signature")

s.report()
s.look(path="pass5_finish.png")
s.look(values=True, path="pass5_values.png")
s.export("tidal_sky.png")
