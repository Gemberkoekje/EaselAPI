# Pass 3: graded sky, flattened water, afterglow in the air, headland.
sky_mass()
sky_low_mass()
water_mass()
water_near_mass()

s.dry()
field = s.sample(span("B4", "D5"))
v = p.value_of(field)
p["sheet_far"] = p.at_value(p.mix(field, "glow", 0.35), min(v + 0.05, 0.50))
s.glaze([(-0.04, 0.42), (0.28, 0.405), (0.62, 0.43)], "sheet_far",
        opacity=0.08, size=0.14, pressure=[0.35, 0.75, 0.40])

sky_field = s.sample(span("B3", "D4"))
sv = p.value_of(sky_field)
p["air_far"] = p.at_value(p.mix(sky_field, "glow", 0.5), sv + 0.06)
p["air_body"] = p.at_value(p.mix("glow", sky_field, 0.35), sv + 0.10)
p["air_core"] = p.at_value(p.mix("glow_core", sky_field, 0.25), sv + 0.14)
source, far = (0.28, 0.38), (0.08, 0.22)
s.dry()
s.glaze([source, (0.20, 0.30), far], "air_far", opacity=0.09, size=0.20,
        pressure=[0.4, 0.8, 1.0])
s.glaze([source, (0.22, 0.32), (0.10, 0.24)], "air_body", opacity=0.15, size=0.11,
        pressure=[1.0, 0.8, 0.4])
s.glaze([source, (0.26, 0.36), (0.20, 0.32)], "air_core", opacity=0.17, size=0.06,
        pressure=[1.0, 0.7, 0.12])

right = s.sample(span("F2", "H3"))
p["far_light"] = p.at_value(p.mix(right, "glow", 0.35), p.value_of(right) + 0.05)
s.glaze([(0.70, 0.22), (0.88, 0.24), (1.08, 0.28)], "far_light", opacity=0.08,
        size=0.14, pressure=[0.4, 0.8, 1.0])

s.stroke([(-0.06, 0.18), (0.40, 0.22), (1.06, 0.16)], "bristle", "dusk_mid",
         size=0.07, load=0.40, opacity=0.40, pressure="swell")
s.stroke([(1.06, 0.62), (0.50, 0.58), (-0.06, 0.64)], "bristle", "water_near",
         size=0.06, load=0.35, opacity=0.38, pressure="swell")

land_mass()
s.look(values=True, path="pass3_values.png")
s.look(path="pass3_colour.png")
