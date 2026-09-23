# The lamp's light in the air: a beam reaching back toward the glow -- three glazes along
# its axis, mixed close to the sky they cross -- whose heads make the halo round the
# lantern. Dry before and after; then the lantern glass and the lamp laid again, lighter,
# so the film does not dull the one thing that has to win.
s.dry()
field = s.sample(ribbon([(0.64, 0.195), (0.30, 0.29), (-0.02, 0.37)], 0.05))
v = p.value_of(field)
p["air_far"]  = p.at_value(p.mix(field, "lamp", 0.5), v + 0.06)
p["air_body"] = p.at_value(p.mix("lamp", field, 0.35), v + 0.10)
p["air_core"] = p.at_value(p.mix("lamp", field, 0.25), v + 0.14)
print("beam field value", round(v, 3))
src = (TX - 0.003, 0.178)
s.glaze([src, (0.30, 0.292), (-0.08, 0.388)], "air_far", opacity=0.09, size=0.20,
        pressure=[0.4, 0.8, 1.0], note="subject")
s.glaze([src, (0.30, 0.288), (-0.08, 0.380)], "air_body", opacity=0.15, size=0.11,
        pressure=[1.0, 0.8, 0.4], note="subject")
s.glaze([src, (0.42, 0.254), (0.18, 0.320)], "air_core", opacity=0.17, size=0.06,
        pressure=[1.0, 0.7, 0.12], note="subject")
s.dry()
p["lantern2"] = p.at_value(p.mix("titanium_white", "cadmium_yellow", 0.25), 0.90)
s.stroke([(TX, 0.1968), (TX, 0.1598)], "flat", "lantern2", size=0.019, clip=lantern,
         opacity=1.0, load=1.0, load_falloff=0.0, pressure="even", jitter=0.0,
         size_jitter=0.0, note="subject")
s.dab(TX, 0.178, "round_hard", "lamp", size=0.013, press=3, tip_wobble=0.35, note="subject")
s.dry()
