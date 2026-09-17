# Pass 3: the graded fields (the picture is most of these), the sun and its halo,
# the clouds, and the sun's reflection running down the water.
sky_mass()
sky_low_mass()
water_mass()
water_near_mass()

# clouds: two or three starved marks high in the sky, no two alike
s.stroke([(0.14, 0.12), (0.30, 0.16), (0.47, 0.13)], "bristle", "cloud_pale",
         size=0.030, load=0.35, opacity=0.40, pressure="swell")
s.stroke([(0.55, 0.20), (0.72, 0.17), (0.88, 0.21)], "bristle", "cloud_pale",
         size=0.022, load=0.30, opacity=0.35, pressure="swell")
s.stroke([(0.05, 0.24), (0.20, 0.22)], "bristle", "cloud_pale",
         size=0.016, load=0.30, opacity=0.30, pressure="taper")

# the halo: three glazes of lit air along the sun's axis, mixed close to the field
field = s.sample(span("B3", "D4"))
v = p.value_of(field)
p["air_far"]  = p.at_value(p.mix(field, "gold", 0.5), v + 0.05)
p["air_body"] = p.at_value(p.mix("gold", field, 0.35), v + 0.09)
p["air_core"] = p.at_value(p.mix("gold", field, 0.25), v + 0.13)
s.dry()
s.glaze([s.pt("sun"), (0.28, 0.30), (0.22, 0.16)], "air_far", opacity=0.09, size=0.20,
        pressure=[0.4, 0.8, 1.0])
s.glaze([s.pt("sun"), (0.295, 0.30), (0.26, 0.17)], "air_body", opacity=0.15, size=0.11,
        pressure=[1.0, 0.8, 0.4])
s.glaze([s.pt("sun"), (0.30, 0.36), (0.28, 0.24)], "air_core", opacity=0.17, size=0.06,
        pressure=[1.0, 0.7, 0.12])
# and one soft glaze carrying the light down across the horizon into the water
s.glaze([s.pt("sun"), (0.30, 0.50), (0.305, 0.56)], "gold", opacity=0.12, size=0.08,
        pressure=[1.0, 0.8, 0.5])

# the sun itself: a disc, and the one place a disc is the thing
s.dry()
s.dab(*s.pt("sun"), "round_hard", "gold", size=0.09, press=3, tip_wobble=0.25)

# its reflection: the glitter path -- broken horizontal flashes, shorter and fainter
# as they come toward the viewer
for y, w, op, dx in [
    (0.555, 0.022, 0.75, 0.000),
    (0.578, 0.018, 0.65, 0.008),
    (0.602, 0.015, 0.55, -0.006),
    (0.630, 0.012, 0.45, 0.005),
    (0.665, 0.010, 0.38, -0.008),
    (0.705, 0.008, 0.30, 0.004),
    (0.750, 0.007, 0.22, -0.003),
    (0.790, 0.006, 0.15, 0.000),
]:
    s.stroke([(0.30 + dx - 0.055, y), (0.30 + dx + 0.045, y)], "flat", "gold",
             size=w, opacity=op, load=1.0, load_falloff=0.0, pressure="even")
s.look(values=True, path="pass3_values.png")
s.look(path="pass3_colour.png")
