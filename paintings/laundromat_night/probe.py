from easel import Session
# what does each ground actually read at?
for g in ("white","warm_white","toned_grey","toned_warm_grey","cool_grey","umber_wash","burnt_sienna"):
    t = Session(320, 240, ground=g, seed=1)
    print(f"  ground {g:18s} v={t.palette.value_of(t.sample()):.3f}  {t.palette.hex(t.sample())}")

s = Session(1024, 768, ground="toned_grey", seed=11)
p = s.palette
print("\ndarkest_value", round(p.darkest_value,3), " aspect", round(s.aspect,4))

print("\ncandidate mixtures (hue check before value-forcing):")
cands = {
 "cool_black": p.mix("ultramarine","burnt_umber",0.35),
 "warm_black": p.mix("ultramarine","burnt_umber",0.62),
 "night_blue": p.mix("ultramarine","burnt_umber",0.22),
 "fluoro":     p.desaturate(p.mix("lemon_yellow","titanium_white",0.72),0.30),
 "fluoro_g":   p.desaturate(p.mix(p.mix("lemon_yellow","viridian",0.16),"titanium_white",0.70),0.22),
 "sodium":     p.mix("yellow_ochre","cadmium_red",0.18),
 "asphalt":    p.desaturate(p.mix("ultramarine","burnt_umber",0.45),0.35),
}
for k,v in cands.items():
    print(f"  {k:11s} {p.hex(v)}  v={p.value_of(v):.3f}")
