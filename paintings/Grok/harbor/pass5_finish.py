# Pass 5: take the drawing out, quiet the fields, last light, sign.
s.unguide("horizon")
s.erase()
s.dry()

sky = s.sample(sky_low())
sv = p.value_of(sky)
p["quiet_sky"] = p.at_value(p.mix(sky, "dusk_mid", 0.4), sv)
s.glaze([(-0.06, 0.26), (0.40, 0.29), (1.08, 0.24)], "quiet_sky",
        opacity=0.12, size=0.11, pressure=[0.4, 0.8, 0.5])
s.glaze([(1.08, 0.33), (0.50, 0.31), (-0.06, 0.35)], "quiet_sky",
        opacity=0.11, size=0.10, pressure=[0.5, 0.8, 0.4])
s.glaze([(-0.06, 0.16), (0.55, 0.14), (1.08, 0.18)], "dusk_high",
        opacity=0.10, size=0.12, pressure=[0.4, 0.7, 0.5])

water = s.sample(water_far())
wv = p.value_of(water)
p["quiet_water"] = p.at_value(p.mix(water, "water", 0.5), wv)
s.glaze([(-0.06, 0.57), (0.45, 0.55), (1.08, 0.59)], "quiet_water",
        opacity=0.10, size=0.10, pressure=[0.4, 0.75, 0.45])
s.glaze([(1.08, 0.73), (0.48, 0.71), (-0.06, 0.75)], "water_near",
        opacity=0.09, size=0.09, pressure=[0.45, 0.7, 0.4])

s.stroke([(-0.05, 0.64), (0.36, 0.60), (0.78, 0.65), (1.05, 0.61)],
         "bristle", "quiet_water", size=0.028, load=0.35, opacity=0.30,
         pressure="swell")
s.stroke([(1.05, 0.84), (0.52, 0.86), (0.12, 0.83), (-0.05, 0.85)],
         "bristle", "water_near", size=0.026, load=0.32, opacity=0.28,
         pressure="swell")

s.stroke([P(-5.2, 0.45, 23.4), P(-3.4, 0.42, 24.5)], "round_hard", "glow_band",
         size=0.004, opacity=0.55, load=0.6, pressure=[0.1, 0.6, 0.1],
         note="subject")

s.stroke([(0.07, 0.945), (0.115, 0.952)], "liner", "water_near",
         size=0.004, note="signature")
s.stroke([(0.078, 0.958), (0.122, 0.948)], "liner", "water_near",
         size=0.0035, note="signature")

print(s.report())
s.look(path="pass5_colour.png")
s.look(values=True, path="pass5_values.png")
s.export("harbor.png")
