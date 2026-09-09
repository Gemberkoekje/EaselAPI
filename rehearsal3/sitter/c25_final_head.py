# Pass 25: last work on the head. Kill the teal slug and the orange ear blob,
# blend the band across the cheek, two highlights, strands, one lost edge.
REF = "C:/temp/Level3.jpg"
p = s.palette
p["coat"]   = p.shade(p.mix("ultramarine", "burnt_umber", 0.62), 0.55)
p["h_d"]    = p.mix(p.mix("burnt_umber", "yellow_ochre", 0.18), "titanium_white", 0.04)
p["h_a"]    = p.mix(p.mix("burnt_umber", "yellow_ochre", 0.30), "titanium_white", 0.06)
p["h_c"]    = p.mix(p.mix("yellow_ochre", "burnt_umber", 0.55), "titanium_white", 0.12)
p["sk_lit"] = p.mix(p.mix("burnt_sienna", "yellow_ochre", 0.44), "titanium_white", 0.62)
p["sk_mid"] = p.mix(p.mix("burnt_sienna", "yellow_ochre", 0.40), "titanium_white", 0.46)
p["sk_hi"]  = p.mix(p.mix("burnt_sienna", "yellow_ochre", 0.38), "titanium_white", 0.76)
p["sk_shad"] = p.desaturate(
    p.mix(p.mix("burnt_sienna", "burnt_umber", 0.45), "titanium_white", 0.32), 0.22)
s.dry()

n0 = s.stroke_count
# the blue flash was a teal slug at head scale — bury it
s.stroke([(0.505, 0.542), (0.560, 0.550), (0.605, 0.552)], "flat", "coat",
         size=0.030, load=1.0, pressure="even")
# the ear: an opaque hair cover, then a small quiet ear inside it
s.stroke([(0.5760, 0.2880), (0.5980, 0.3080), (0.6020, 0.3420),
          (0.5900, 0.3720)], "flat", "h_d", size=0.030, load=1.0, pressure="even")
s.stroke([(0.5790, 0.3140), (0.5870, 0.3250), (0.5860, 0.3420)], "round_hard",
         "sk_shad", size=0.011, load=1.0, pressure="even")
s.stroke([(0.5800, 0.3200), (0.5840, 0.3320)], "liner", "sk_mid",
         size=0.0055, load=1.0, pressure="taper")
print("kills:", s.stroke_count - n0)

n0 = s.stroke_count
# blend the hard horizontal band across the cheek and the streaks on the forehead
s.smudge([(0.4180, 0.3760), (0.4700, 0.3810), (0.5300, 0.3860)], size=0.026)
s.stroke([(0.4200, 0.2500), (0.4520, 0.2680), (0.4820, 0.2860)], "flat", "sk_lit",
         size=0.024, load=1.0, pressure="even")
s.glaze([(0.4300, 0.3300), (0.4800, 0.3560), (0.5300, 0.3820)], "sk_mid", opacity=0.20)
print("blend:", s.stroke_count - n0)

n0 = s.stroke_count
# two highlights, no more
s.dab(0.4980, 0.3320, "round_hard", "sk_hi", size=0.016)
s.dab(0.4260, 0.2760, "round_hard", "sk_hi", size=0.013)
# the shadow under the nose has to read or the nose does not
s.stroke([(0.4090, 0.3936), (0.4230, 0.3956), (0.4360, 0.3934)], "liner", "sk_shad",
         size=0.0070, load=1.0, pressure="swell")
# under-jaw shadow so the head sits on the neck
s.stroke([(0.4880, 0.5480), (0.5320, 0.5620), (0.5740, 0.5580)], "bristle", "sk_shad",
         size=0.016, load=0.8, pressure="taper")
print("accents:", s.stroke_count - n0)

n0 = s.stroke_count
# strands over the temple, and one lost edge where the hair meets the coat
s.stroke([(0.4700, 0.1820), (0.4400, 0.2240), (0.4280, 0.2600)], "bristle", "h_a",
         size=0.010, load=1.0, pressure="lift_off")
s.stroke([(0.4980, 0.2060), (0.4700, 0.2480), (0.4560, 0.2820)], "bristle", "h_c",
         size=0.006, load=1.0, pressure="taper")
s.smudge([(0.6300, 0.4300), (0.6480, 0.4620), (0.6420, 0.4900)], size=0.034)
print("strands/edge:", s.stroke_count - n0)

print("head :", s.look(region=span("D2", "F5"), reference=REF))
print("TOTAL strokes:", s.stroke_count)
