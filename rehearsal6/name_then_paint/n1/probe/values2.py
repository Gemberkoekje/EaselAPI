from easel import Session
s = Session(200,200,seed=1)
p = s.palette
def show(name, c):
    print(f"{name:26s} {p.hex(c)}  v={p.value_of(c):.3f}")

grey = p.mix("ultramarine","burnt_sienna",0.50)
for t in (0.62,0.70,0.78,0.84,0.88,0.92):
    show(f"cool_grey tint {t}", p.tint(grey,t))
print()
warm = p.mix("burnt_umber","yellow_ochre",0.55)
for t in (0.55,0.65,0.72,0.80,0.86):
    show(f"warm_grey tint {t}", p.tint(warm,t))
print()
gg = p.mix(p.mix("viridian","burnt_umber",0.5),"yellow_ochre",0.35)
for t in (0.55,0.68,0.78,0.86):
    show(f"greengrey tint {t}", p.tint(gg,t))
print()
for t in (0.25,0.35,0.45,0.55):
    show(f"bg lift {t}", p.tint(p.mix("ultramarine","burnt_umber",0.62),t))
print()
show("bg deep",  p.mix("ultramarine","burnt_umber",0.62))
show("bg deepest", p.mix("ultramarine","burnt_umber",0.50))
show("shadow_on_table", p.mix(p.mix("burnt_umber","burnt_sienna",0.4),"ultramarine",0.45))
show("terra deep",  p.mix(p.mix("burnt_sienna","cadmium_red",0.3),"burnt_umber",0.55))
show("terra rim lit", p.tint(p.mix(p.mix("burnt_sienna","cadmium_red",0.25),"yellow_ochre",0.35),0.50))
show("pot inside", p.mix(p.mix("burnt_umber","ultramarine",0.35),"burnt_sienna",0.15))
show("stem", p.mix(p.mix("viridian","yellow_ochre",0.45),"burnt_umber",0.40))
show("leaf lit warm", p.tint(p.mix(p.mix("viridian","yellow_ochre",0.55),"burnt_umber",0.2),0.22))
