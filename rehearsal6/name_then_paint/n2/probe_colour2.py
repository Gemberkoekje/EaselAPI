p = s.palette
def show(name, c):
    print(f"{name:26s} {p.hex(c):9s} {p.value_of(c):.2f}")

pale = p.mix("titanium_white", "yellow_ochre", 0.28)   # 0.85
dk   = p.mix("ultramarine", "burnt_umber", 0.55)
print("--- sill ramp: pale + umber ---")
for r in (0.08, 0.12, 0.18, 0.24, 0.32, 0.45):
    show(f"pale+umber {r}", p.mix(pale, "burnt_umber", r))
print("--- sill ramp: pale + dark mix ---")
for r in (0.15, 0.25, 0.35, 0.50, 0.68):
    show(f"pale+dk {r}", p.mix(pale, dk, r))
print("--- sill warm shadow (with sienna bounce) ---")
for r in (0.25, 0.40):
    show(f"pale+sienna {r}", p.mix(pale, "burnt_sienna", r))
show("sill shadow warm", p.mix(p.mix(pale,"burnt_sienna",0.35), dk, 0.45))

print("--- window ---")
show("glow cool", p.mix("titanium_white", "cerulean", 0.10))
show("glow core", p.mix("titanium_white", "yellow_ochre", 0.07))
show("glow far",  p.mix(p.mix("titanium_white","cerulean",0.14), "yellow_ochre", 0.06))
show("glow low",  p.mix(p.mix("titanium_white","cerulean",0.20), "burnt_umber", 0.05))
show("frame dark",p.mix(dk, "burnt_sienna", 0.22))
show("frame lit", p.mix(pale, "burnt_umber", 0.22))

print("--- pot ---")
tc = p.mix("burnt_sienna", "cadmium_red", 0.35)
show("pot lit",   p.tint(tc, 0.52))
show("pot half",  p.tint(tc, 0.26))
show("pot core",  p.mix(tc, dk, 0.35))
show("pot refl",  p.mix(p.mix(tc, dk, 0.35), "cadmium_red", 0.30))
show("pot rimlit",p.tint(tc, 0.70))
show("crack",     p.mix(dk, "burnt_sienna", 0.15))

print("--- leaves ---")
show("leaf silhouette", p.mix(p.mix("viridian","burnt_umber",0.5), "ultramarine", 0.3))
show("leaf shadow",     p.mix("viridian","burnt_umber",0.35))
show("leaf mid",        p.mix("viridian","yellow_ochre",0.42))
show("leaf lit",        p.tint(p.mix("viridian","cadmium_yellow",0.5), 0.22))
show("leaf hot",        p.tint(p.mix("viridian","cadmium_yellow",0.62), 0.35))
