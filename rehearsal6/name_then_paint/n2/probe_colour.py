p = s.palette

def show(name, c):
    print(f"{name:22s} {p.hex(c):9s} {p.value_of(c):.2f}")

print("--- ground / light through the window ---")
show("white",            "titanium_white")
show("wm_white .10",     p.mix("titanium_white", "yellow_ochre", 0.10))
show("wm_white .20",     p.mix("titanium_white", "yellow_ochre", 0.20))
show("cl_white .10",     p.mix("titanium_white", "cerulean", 0.10))
show("cl_white .18",     p.mix("titanium_white", "cerulean", 0.18))
show("hazy",             p.desaturate(p.mix("titanium_white", "cerulean", 0.16), 0.4))
show("sky-ish",          p.tint(p.mix("cerulean","yellow_ochre",0.25), 0.85))

print("--- interior darks ---")
for r in (0.35, 0.5, 0.65):
    show(f"ub mix {r}",  p.mix("ultramarine", "burnt_umber", r))
show("wall = ub.6 + w .12", p.mix(p.mix("ultramarine","burnt_umber",0.6), "titanium_white", 0.12))
show("wall = ub.6 + w .20", p.mix(p.mix("ultramarine","burnt_umber",0.6), "titanium_white", 0.20))
show("wall warm +sienna",   p.mix(p.mix("ultramarine","burnt_umber",0.6), "burnt_sienna", 0.30))

print("--- terracotta ---")
tc = p.mix("burnt_sienna", "cadmium_red", 0.35)
show("terracotta raw", tc)
for t in (0.20, 0.35, 0.50):
    show(f"terracotta tint {t}", p.tint(tc, t))
show("tc shadow", p.mix(tc, "ultramarine", 0.28))
show("tc shadow2", p.mix(p.mix(tc,"ultramarine",0.28), "burnt_umber", 0.3))

print("--- foliage ---")
show("leaf dark",  p.mix("viridian", "burnt_umber", 0.45))
show("leaf dark2", p.mix(p.mix("viridian","burnt_umber",0.45), "ultramarine", 0.25))
show("leaf mid",   p.mix("viridian", "yellow_ochre", 0.45))
show("leaf lit",   p.tint(p.mix("viridian", "cadmium_yellow", 0.45), 0.25))

print("--- blooms ---")
show("red",        "cadmium_red")
show("bloom lit",  p.tint(p.mix("cadmium_red","cadmium_yellow",0.15), 0.22))
show("bloom mid",  "cadmium_red")
show("bloom dark", p.mix("alizarin", "burnt_umber", 0.35))

print("--- sill (pale stone/paint) ---")
sl = p.mix("titanium_white", "yellow_ochre", 0.28)
show("sill lit", sl)
show("sill lit+",p.mix("titanium_white","yellow_ochre",0.16))
show("sill mid", p.mix(sl, "burnt_umber", 0.30))
show("sill shad",p.mix(sl, p.mix("ultramarine","burnt_umber",0.5), 0.62))
