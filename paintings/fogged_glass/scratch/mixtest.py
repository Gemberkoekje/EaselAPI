from easel import Session
s = Session(1200, 800, texture="rough", ground="umber_wash", seed=11)
p = s.palette

# sky / cold light
sky      = p.at_value(p.desaturate(p.mix("cerulean", "titanium_white", 0.72), 0.45), 0.68)
lip      = p.at_value(p.desaturate(p.mix("cerulean", "titanium_white", 0.85), 0.30), 0.84)
# the fog film
fog      = p.at_value(p.desaturate(p.mix(p.mix("yellow_ochre","cerulean",0.42), "titanium_white", 0.70), 0.35), 0.55)
fogwarm  = p.at_value(p.mix(p.mix("yellow_ochre","titanium_white",0.62), "burnt_sienna", 0.14), 0.52)
fogcool  = p.at_value(p.desaturate(p.mix("cerulean","titanium_white",0.72), 0.30), 0.60)
# the green behind
leaf     = p.at_value(p.mix(p.mix("viridian","yellow_ochre",0.40), "burnt_umber", 0.22), 0.26)
leafhaze = p.at_value(p.desaturate(p.mix(p.mix("viridian","yellow_ochre",0.45),"burnt_umber",0.20), 0.55), 0.44)
# structure
bar      = p.at_value(p.mix("burnt_umber", "ultramarine", 0.32), 0.36)
barlit   = p.at_value(p.mix("burnt_umber", "ultramarine", 0.22), 0.56)
brick    = p.at_value(p.mix(p.mix("burnt_sienna","burnt_umber",0.45), "ultramarine", 0.18), 0.30)
# distance
trees    = p.at_value(p.desaturate(p.mix("burnt_umber","ultramarine",0.45), 0.25), 0.50)
yard     = p.at_value(p.desaturate(p.mix("yellow_ochre","ultramarine",0.34), 0.40), 0.42)
warm     = p.at_value(p.mix(p.mix("burnt_sienna","cadmium_red",0.35),"burnt_umber",0.20), 0.38)
dark     = p.at_value(p.mix("ultramarine","burnt_umber",0.48), 0.20)

names = dict(sky=sky, lip=lip, fog=fog, fogwarm=fogwarm, fogcool=fogcool, leaf=leaf,
             leafhaze=leafhaze, bar=bar, barlit=barlit, brick=brick, trees=trees,
             yard=yard, warm=warm, dark=dark)
for n, c in names.items():
    print(f"{n:9s} v={p.value_of(c):.3f}  c={p.chroma_of(c):.3f}  {p.hex(c)}")
