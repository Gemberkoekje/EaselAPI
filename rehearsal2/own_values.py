from easel import Session
p = Session(1200, 800, texture="rough", ground="toned_warm_grey", seed=23).palette
p["sky"]      = p.tint(p.mix("burnt_sienna", "cerulean", 0.55), 0.78)
p["sky_warm"] = p.tint(p.mix("yellow_ochre", "cadmium_red", 0.15), 0.72)
p["glow"]     = p.tint("lemon_yellow", 0.6)
p["far"]      = p.tint(p.mix("ultramarine", "burnt_umber", 0.5), 0.30)
p["head"]     = p.tint(p.mix("ultramarine", "burnt_umber", 0.6), 0.12)
p["water"]    = p.desaturate(p.tint(p.mix("cerulean", "burnt_umber", 0.3), 0.45), 0.3)
p["water_lt"] = p.tint(p.mix("cerulean", "yellow_ochre", 0.4), 0.7)
p["mud"]      = p.mix("burnt_umber", "yellow_ochre", 0.4)
p["mud_lt"]   = p.tint(p.mix("burnt_umber", "yellow_ochre", 0.6), 0.35)
p["mud_dk"]   = p.mix("burnt_umber", "ultramarine", 0.3)
p["post"]     = p.mix("ultramarine", "burnt_umber", 0.5)
for n in ("sky", "sky_warm", "glow", "far", "head", "water", "water_lt", "mud", "mud_lt", "mud_dk", "post"):
    print(f"{n:9s} {p.hex(p[n])} {p.value_of(p[n]):.2f}")
