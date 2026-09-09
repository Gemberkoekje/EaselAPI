# Pass 26: the last six strokes, then measure and export.
REF = "C:/temp/Level3.jpg"
p = s.palette
p["h_a"]  = p.mix(p.mix("burnt_umber", "yellow_ochre", 0.30), "titanium_white", 0.06)
p["h_c"]  = p.mix(p.mix("yellow_ochre", "burnt_umber", 0.55), "titanium_white", 0.12)
p["beard"] = p.mix(p.mix("burnt_umber", "burnt_sienna", 0.30), "titanium_white", 0.07)
p["sk_hi"] = p.mix(p.mix("burnt_sienna", "yellow_ochre", 0.38), "titanium_white", 0.76)
p["catch"] = p.mix("titanium_white", "yellow_ochre", 0.06)
s.dry()

n0 = s.stroke_count
# the opaque ear cover left a hard slab — comb hair down over it
s.stroke([(0.5760, 0.2820), (0.5920, 0.3180), (0.5980, 0.3620)], "bristle", "h_a",
         size=0.016, load=1.0, pressure="taper")
s.stroke([(0.5880, 0.2900), (0.6010, 0.3260), (0.6020, 0.3680)], "bristle", "h_c",
         size=0.008, load=1.0, pressure="lift_off")
# the pale patch behind the jaw belongs to the beard
s.stroke([(0.5520, 0.4220), (0.5720, 0.4520), (0.5760, 0.4860)], "bristle", "beard",
         size=0.022, load=1.0, pressure="swell")
s.stroke([(0.5300, 0.4720), (0.5540, 0.4980), (0.5560, 0.5240)], "bristle", "beard",
         size=0.016, load=0.9, pressure="taper")
# two last accents
s.dab(0.5020, 0.3380, "round_hard", "sk_hi", size=0.014)
s.dab(0.4548, 0.3058, "round_hard", "catch", size=0.0030)
print("last:", s.stroke_count - n0)

print("head :", s.look(region=span("D2", "F5"), reference=REF))
print("side :", s.look(reference=REF))
print("vals :", s.look(reference=REF, values=True))
print("alone:", s.look())
print(s.compare(REF))
print("TOTAL strokes:", s.stroke_count)
