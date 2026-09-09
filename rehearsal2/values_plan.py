from easel import Session
p = Session(1200, 800, texture="linen", ground="umber_wash", seed=11).palette
p["dark"]     = p.mix("ultramarine", "burnt_umber", 0.55)
p["coat_wm"]  = p.mix(p["dark"], "burnt_sienna", 0.12)
p["ceiling"]  = p.mix("burnt_umber", "yellow_ochre", 0.3)
p["wall_mid"] = p.tint(p.mix("yellow_ochre", "burnt_umber", 0.5), 0.3)
p["wall_lt"]  = p.tint(p.mix("yellow_ochre", "burnt_sienna", 0.2), 0.6)
p["wall_pale"]= p.tint(p.mix("yellow_ochre", "burnt_sienna", 0.2), 0.78)
p["hair"]     = p.mix("burnt_umber", "yellow_ochre", 0.45)
p["hair_lt"]  = p.tint(p["hair"], 0.35)
p["flesh"]    = p.tint(p.mix("burnt_sienna", "yellow_ochre", 0.5), 0.55)
p["flesh_sh"] = p.tint(p.mix("burnt_sienna", "burnt_umber", 0.4), 0.2)
p["flesh_lt"] = p.tint(p.mix("burnt_sienna", "yellow_ochre", 0.5), 0.75)
p["orange"]   = p.mix("cadmium_yellow", "cadmium_red", 0.35)
p["table"]    = p.tint("yellow_ochre", 0.55)
p["red"]      = p.mix("cadmium_red", "alizarin", 0.4)
p["glass"]    = p.desaturate(p.tint("cerulean", 0.6), 0.5)
for n in ["dark","coat_wm","ceiling","wall_mid","wall_lt","wall_pale","hair","hair_lt",
          "flesh","flesh_sh","flesh_lt","orange","table","red","glass"]:
    print(f"{n:10s} {p.hex(p[n])}  {p.value_of(p[n]):.2f}")
print("ground umber_wash value:", round(p.value_of(p.mix("burnt_umber","yellow_ochre",0.0)),2), "(dummy)")
