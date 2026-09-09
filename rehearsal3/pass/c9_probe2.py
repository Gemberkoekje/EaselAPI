import math
REF = r"C:\temp\Level1.jpg"
p = s.palette
p["ck"] = p.desaturate(p.mix("burnt_umber","ultramarine",0.35), 0.35)
print("target value", round(p.value_of(p["ck"]),3))
plan = [{"points": [(0.36,0.20),(0.60,0.21)], "brush":"flat", "size":0.05,
         "color":"ck", "pressure":"even", "load":1.0}]
print("WET rehearse :", s.rehearse(plan, region=span("C2","F4")))
s.dry()
print("DRY rehearse :", s.rehearse(plan, region=span("C2","F4")))
print("strokes:", s.stroke_count)
