# Pass 24: scene fixes only — break up the blocky lights, pull the coat's right
# edge off the table, put the table edge back. Then look hard at the head.
REF = "C:/temp/Level3.jpg"
p = s.palette
p["bg_lit"]  = p.mix(p.mix("yellow_ochre", "burnt_sienna", 0.30), "titanium_white", 0.46)
p["bg_mid"]  = p.mix(p.mix("burnt_umber", "yellow_ochre", 0.42), "titanium_white", 0.20)
p["bg_hi"]   = p.mix(p.mix("yellow_ochre", "burnt_sienna", 0.20), "titanium_white", 0.62)
p["bgfig"]   = p.mix(p.mix("burnt_umber", "ultramarine", 0.30), "titanium_white", 0.07)
s.dry()

n0 = s.stroke_count
# the two light slabs top-left were pasted on; break them with the dark between
s.stroke([(0.055, 0.075), (0.150, 0.068), (0.250, 0.082)], "bristle", "bg_mid",
         size=0.030, load=0.85, pressure="swell")
s.stroke([(0.180, 0.020), (0.280, 0.030)], "bristle", "bg_mid",
         size=0.026, load=0.7, pressure="taper")
# the table to the right of his shoulder is light in the reference, dark in mine
s.stroke([(0.905, 0.470), (0.955, 0.520), (0.995, 0.585)], "flat", "bg_hi",
         size=0.052, load=1.0, load_falloff=0.0, pressure="even")
s.stroke([(0.880, 0.615), (0.940, 0.640), (0.998, 0.665)], "flat", "bg_lit",
         size=0.042, load=1.0, load_falloff=0.0, pressure="even")
# the man in the background at G4, and the dark bag bottom right
s.stroke([(0.790, 0.330), (0.830, 0.360), (0.850, 0.400)], "bristle", "bgfig",
         size=0.030, load=0.9, pressure="taper")
s.stroke([(0.920, 0.880), (0.960, 0.930), (0.985, 0.990)], "flat", "bgfig",
         size=0.044, load=1.0, pressure="even")
print("scene:", s.stroke_count - n0)

print("head :", s.look(region=span("D2", "F5"), reference=REF))
print("whole:", s.look(reference=REF))
print("TOTAL strokes:", s.stroke_count)
