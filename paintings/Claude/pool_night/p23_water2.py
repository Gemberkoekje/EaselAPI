s.dry()
# The far half of the water was still the palest flat area in the picture, and it is
# the subject. Darks first, then catches on them -- sparse, and with a stretch in the
# middle deliberately left with nothing.
for pts, size, op, val in [([(0.620, 0.600), (0.740, 0.626), (0.860, 0.642)], 0.070, 0.30, 0.54),
                           ([(0.700, 0.690), (0.820, 0.712)],                 0.055, 0.26, 0.55),
                           ([(0.560, 0.520), (0.660, 0.538)],                 0.045, 0.24, 0.56)]:
    s.glaze(pts, p.at_value("water", val), opacity=op, size=size, pressure="swell",
            note="subject")
for pts, size, load, op, val, press in [
        ([(0.640, 0.674), (0.726, 0.686)], 0.030, 0.34, 0.70, 0.74, "swell"),
        ([(0.782, 0.626), (0.848, 0.641)], 0.026, 0.30, 0.60, 0.72, "taper"),
        ([(0.512, 0.586), (0.586, 0.599)], 0.028, 0.32, 0.65, 0.76, "lift_off"),
        ([(0.686, 0.554), (0.734, 0.565)], 0.026, 0.26, 0.55, 0.78, "taper"),
        ([(0.856, 0.632), (0.902, 0.647)], 0.026, 0.24, 0.45, 0.70, "swell")]:
    s.stroke(pts, "bristle", p.at_value("water", val), size=size, load=load,
             opacity=op, load_falloff=0.40, pressure=press, note="subject")
print(s.look())
