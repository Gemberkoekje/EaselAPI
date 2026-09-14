s.dry()
# The nearest water had no surface at all: every ripple in the picture was laid in
# the middle distance. Foreground marks are the biggest ones, so these are wider
# than anything out by the lamps, and the light on them comes from up-left, where
# the near lamp is.
near = [([(0.200, 0.845), (0.340, 0.895), (0.480, 0.935)], 0.090, 0.55, 0.70, 0.43, "swell"),
        ([(0.460, 0.880), (0.600, 0.905), (0.700, 0.872)], 0.070, 0.48, 0.60, 0.46, "taper"),
        ([(0.240, 0.800), (0.380, 0.838), (0.500, 0.862)], 0.055, 0.40, 0.80, 0.70, "lift_off"),
        ([(0.420, 0.955), (0.560, 0.976)],                 0.065, 0.32, 0.65, 0.66, "swell"),
        ([(0.580, 0.828), (0.700, 0.846)],                 0.045, 0.36, 0.70, 0.68, "taper"),
        ([(0.160, 0.812), (0.262, 0.849)],                 0.038, 0.30, 0.60, 0.64, "taper"),
        ([(0.330, 0.871), (0.412, 0.885)],                 0.026, 0.30, 0.85, 0.76, "lift_off"),
        ([(0.520, 0.920), (0.616, 0.938)],                 0.032, 0.44, 0.55, 0.49, "swell")]
for pts, size, load, op, val, press in near:
    s.stroke(pts, "bristle", p.at_value("water", val), size=size, load=load,
             opacity=op, load_falloff=0.40, pressure=press, note="subject")
print(s.look(region="B6:G8"))
