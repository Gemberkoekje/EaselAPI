from easel import Session, Region

s = Session(1400, 260, ground="umber_wash", seed=9, out_dir="out_ex9")
p = s.palette

wood   = p.mix("burnt_umber", "burnt_sienna", 0.30)
wood   = p.mix(wood, "ultramarine", 0.12)
flesh  = p.mix("yellow_ochre", "burnt_sienna", 0.40)
cool   = p.mix(flesh, "ultramarine", 0.22)
warm   = p.mix("burnt_sienna", "cadmium_red", 0.35)
crock  = p.desaturate(p.mix("cerulean", "burnt_umber", 0.42), 0.35)
bean   = p.mix("burnt_sienna", "burnt_umber", 0.45)

plan = {
 "tbl_deep": p.at_value(wood, 0.16),
 "table":    p.at_value(wood, 0.22),
 "tbl_lit":  p.at_value(p.mix(wood, "yellow_ochre", 0.22), 0.34),
 "bean_dk":  p.at_value(bean, 0.24),
 "bean":     p.at_value(bean, 0.34),
 "bean_lit": p.at_value(p.mix(bean, "yellow_ochre", 0.35), 0.52),
 "fl_shad":  p.at_value(cool, 0.36),
 "crock":    p.at_value(crock, 0.47),
 "fl_mid":   p.at_value(flesh, 0.52),
 "fl_warm":  p.at_value(warm, 0.58),
 "crock_lit":p.at_value(p.mix(crock, "titanium_white", 0.3), 0.66),
 "fl_lit":   p.at_value(p.mix(flesh, "titanium_white", 0.45), 0.72),
 "fl_high":  p.at_value(p.mix(flesh, "titanium_white", 0.7), 0.84),
}
n = len(plan)
for i, (name, colour) in enumerate(plan.items()):
    band = Region(i / n + 0.004, 0.10, (i + 1) / n - 0.004, 0.90)
    s.block_in(band, "flat", colour, size=0.05, solid=True)
    print(f"{name:10s} {p.hex(colour)}  v={p.value_of(colour):.2f}  c={p.chroma_of(colour):.2f}")
print(s.look())
print(s.look(values=True))
