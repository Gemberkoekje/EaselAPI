# Pass 5: take the drawing out, quiet the joins, lose one edge, last light, sign.
s.unguide("horizon")
s.unguide("beam")
s.erase()
s.dry()

# Quiet films close to what is already there; no new masses.
sky = s.sample(sky_low())
sv = p.value_of(sky)
p["quiet_sky"] = p.at_value(p.mix(sky, "sky_mid", 0.45), sv)
s.glaze([(-0.06, 0.255), (0.42, 0.285), (1.08, 0.260)], "quiet_sky",
        opacity=0.11, size=0.11, pressure=[0.4, 0.8, 0.5])
s.glaze([(1.08, 0.390), (0.55, 0.365), (-0.06, 0.395)], "quiet_sky",
        opacity=0.09, size=0.10, pressure=[0.5, 0.75, 0.4])

water = s.sample(sea_far())
wv = p.value_of(water)
p["quiet_sea"] = p.at_value(p.mix(water, "sea", 0.50), wv)
s.glaze([(-0.06, 0.600), (0.42, 0.585), (1.08, 0.620)], "quiet_sea",
        opacity=0.10, size=0.10, pressure=[0.4, 0.75, 0.45])

# Two crossers keep the sea a field rather than bars.
s.stroke([(-0.05, 0.665), (0.34, 0.640), (0.74, 0.670), (1.05, 0.650)],
         "bristle", "quiet_sea", size=0.026, load=0.32, opacity=0.30,
         pressure="swell")
s.stroke([(1.05, 0.880), (0.55, 0.905), (0.12, 0.875), (-0.05, 0.895)],
         "bristle", "sea_deep", size=0.024, load=0.30, opacity=0.28,
         pressure="swell")

# Lose a stretch of the horizon right of the tower with paint, not a thumbprint.
s.stroke([(0.720, 0.505), (0.790, 0.510), (0.860, 0.520)], "bristle",
         "quiet_sky", size=0.030, load=0.55, opacity=0.45, pressure="taper")

# Final small lights: lamp core, one rail catch, two water sparks.
s.dab(*s.pt("lamp"), "round_hard", "lamp_glass", size=0.012, press=3,
      tip_wobble=0.35, note="subject")
s.stroke([(0.612, 0.335), (0.636, 0.312)], "liner", "gold_core", size=0.003,
         opacity=0.75, load=0.8, pressure="taper", note="subject")
s.stroke([(0.610, 0.552), (0.675, 0.548)], "flat", "gold_core", size=0.006,
         opacity=0.55, load=1.0, load_falloff=0.0, pressure="even", note="subject")
s.dab(0.725, 0.610, "round_hard", "horizon_gold", size=0.006, press=2,
      tip_wobble=0.7, note="subject")

# Signature: two small tide-lines, close in value to the near sea.
s.stroke([(0.070, 0.945), (0.118, 0.952)], "liner", "sea_deep", size=0.004,
         note="signature")
s.stroke([(0.078, 0.960), (0.124, 0.950)], "liner", "sea", size=0.0035,
         note="signature")

print(s.report())
s.look(path="pass5_colour.png")
s.look(values=True, path="pass5_values.png")
s.export("lighthouse-dusk-kimi.png")
