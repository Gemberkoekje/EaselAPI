from easel import Session
for hexc in ("#4a443c","#544b40","#463f3a","#5a5045","#3f3a34"):
    t = Session(320,240, ground=hexc, seed=1)
    print(f"  ground {hexc}  v={t.palette.value_of(t.sample()):.3f}")

s = Session(1024,768, ground="#544b40", seed=11)
p = s.palette
def V(base,target): return p.at_value(base,target)
cool_black = p.mix("ultramarine","burnt_umber",0.35)
warm_black = p.mix("ultramarine","burnt_umber",0.62)
night_blue = p.mix("ultramarine","burnt_umber",0.22)
fluoro     = p.desaturate(p.mix(p.mix("lemon_yellow","viridian",0.16),"titanium_white",0.70),0.22)
sodium     = p.mix("yellow_ochre","cadmium_red",0.18)
asphalt    = p.desaturate(p.mix("ultramarine","burnt_umber",0.45),0.35)

plan = [("facade",   warm_black, 0.17),
        ("facade_lt",p.mix(warm_black,sodium,0.30), 0.26),
        ("sky",      night_blue, 0.30),
        ("asphalt",  asphalt, 0.23),
        ("wet_mid",  p.mix(asphalt,sodium,0.35), 0.42),
        ("wet_hi",   p.mix(asphalt,sodium,0.55), 0.55),
        ("interior", fluoro, 0.88),
        ("wall_lo",  p.desaturate(fluoro,0.18), 0.74),
        ("machine",  p.desaturate(p.mix(fluoro,cool_black,0.42),0.25), 0.52),
        ("mach_dk",  p.mix(cool_black,fluoro,0.18), 0.33),
        ("figure",   p.mix(cool_black,"burnt_sienna",0.28), 0.24),
        ("frame",    p.mix(warm_black,cool_black,0.5), 0.155),
        ("spill",    p.mix(sodium,fluoro,0.45), 0.66),
        ("hot",      p.mix(fluoro,"titanium_white",0.55), 0.95)]
print()
for name, base, tgt in plan:
    c = V(base,tgt)
    print(f"  {name:10s} {p.hex(c)}  v={p.value_of(c):.3f}  (asked {tgt:.2f})")
