# Pass 1: value plan + first look at the reference with the grid on.
# Run with:  python -m easel run painting.easel c1_setup.py

REF = "C:/temp/Level3.jpg"

p = s.palette

# --- the value plan, as numbers, before anything is mixed onto the canvas ---
p["coat"]      = p.shade(p.mix("ultramarine", "burnt_umber", 0.62), 0.55)
p["coat_lit"]  = p.mix(p["coat"], "titanium_white", 0.18)
p["bg_dark"]   = p.mix("burnt_umber", "ultramarine", 0.22)
p["bg_mid"]    = p.tint(p.mix("burnt_umber", "yellow_ochre", 0.55), 0.30)
p["bg_lit"]    = p.tint(p.mix("yellow_ochre", "burnt_sienna", 0.30), 0.62)
p["hair_dk"]   = p.mix("burnt_umber", "ultramarine", 0.18)
p["hair_mid"]  = p.mix("burnt_umber", "yellow_ochre", 0.45)
p["hair_lit"]  = p.tint(p.mix("yellow_ochre", "burnt_umber", 0.30), 0.42)
p["skin_shad"] = p.desaturate(p.mix("burnt_sienna", "burnt_umber", 0.45), 0.25)
p["skin_mid"]  = p.tint(p.mix("burnt_sienna", "yellow_ochre", 0.45), 0.45)
p["skin_lit"]  = p.tint(p.mix("yellow_ochre", "cadmium_red", 0.22), 0.66)
p["skin_hi"]   = p.tint(p.mix("yellow_ochre", "cadmium_red", 0.18), 0.82)
p["carton"]    = p.mix("cadmium_red", "cadmium_yellow", 0.62)
p["white_hi"]  = p.tint("yellow_ochre", 0.90)

for name in ("coat", "coat_lit", "bg_dark", "bg_mid", "bg_lit", "hair_dk",
             "hair_mid", "hair_lit", "skin_shad", "skin_mid", "skin_lit",
             "skin_hi", "carton", "white_hi"):
    print("%-10s %-8s %.2f" % (name, p.hex(p[name]), p.value_of(p[name])))

print("ground umber_wash value ->", round(p.value_of(p.mix("burnt_umber", "titanium_white", 0.40)), 2))
print()
print("LOOK grid:", s.look(reference=REF, grid=True))
print("LOOK values:", s.look(reference=REF, grid=True, values=True))
print("strokes:", s.stroke_count)
