from easel import Session, Region
s = Session(1400, 200, texture="rough", ground="umber_wash", seed=11)
p = s.palette
plan = {
 "sky":      p.at_value(p.desaturate(p.mix("cerulean","titanium_white",0.72), 0.45), 0.68),
 "lip":      p.at_value(p.desaturate(p.mix("cerulean","titanium_white",0.85), 0.30), 0.84),
 "fogcool":  p.at_value(p.desaturate(p.mix("cerulean","titanium_white",0.72), 0.30), 0.60),
 "fog":      p.at_value(p.desaturate(p.mix(p.mix("yellow_ochre","cerulean",0.42),"titanium_white",0.70), 0.35), 0.55),
 "fogwarm":  p.at_value(p.desaturate(p.mix(p.mix("yellow_ochre","titanium_white",0.62),"burnt_sienna",0.14), 0.52), 0.52),
 "leafhaze": p.at_value(p.desaturate(p.mix(p.mix("viridian","yellow_ochre",0.45),"burnt_umber",0.20), 0.55), 0.44),
 "leaf":     p.at_value(p.mix(p.mix("viridian","yellow_ochre",0.28),"burnt_umber",0.12), 0.26),
 "bar":      p.at_value(p.mix("burnt_umber","ultramarine",0.32), 0.36),
 "brick":    p.at_value(p.mix(p.mix("burnt_sienna","burnt_umber",0.45),"ultramarine",0.18), 0.30),
 "trees":    p.at_value(p.desaturate(p.mix("burnt_umber","ultramarine",0.45), 0.25), 0.50),
 "yard":     p.at_value(p.desaturate(p.mix("yellow_ochre","ultramarine",0.34), 0.40), 0.42),
 "warm":     p.at_value(p.mix(p.mix("burnt_sienna","cadmium_red",0.42),"burnt_umber",0.12), 0.38),
 "dark":     p.at_value(p.mix("ultramarine","burnt_umber",0.48), 0.20),
}
n = len(plan)
for i, (name, c) in enumerate(plan.items()):
    band = Region(i/n + 0.004, 0.10, (i+1)/n - 0.004, 0.90)
    s.block_in(band, "flat", c, size=0.05, solid=True)
    print(f"{name:9s} v={p.value_of(c):.3f}  c={p.chroma_of(c):.3f}  {p.hex(c)}")
print(s.look())
