s.dry()
# The water measured 0.45-0.55 against a deck at 0.38 -- too close for the subject
# to own the top of the scale. Lifted with films over the lit passages only; the
# reflected darks and the near corner are left where they are.
lift = [([(0.22, 0.700), (0.42, 0.716), (0.62, 0.690), (0.80, 0.700)], 0.160, 0.42, 0.71),
        ([(0.30, 0.762), (0.44, 0.800), (0.58, 0.838)],                0.130, 0.34, 0.67),
        ([(0.52, 0.562), (0.68, 0.600), (0.86, 0.650)],                0.110, 0.26, 0.63),
        ([(0.596, 0.540), (0.700, 0.562)],                             0.070, 0.32, 0.69)]
for pts, size, op, val in lift:
    s.glaze(pts, p.at_value("water", val), opacity=op, size=size, pressure="swell",
            note="subject")
print(s.look())
