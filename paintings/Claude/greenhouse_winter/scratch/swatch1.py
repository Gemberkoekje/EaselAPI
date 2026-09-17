from easel import Session, Region
s = Session(900, 300, ground="toned_warm_grey", seed=9, out_dir="out_swatch")
p = s.palette
cands = {
 "a_cur":  p.desaturate(p.mix("yellow_ochre", "cerulean", 0.45), 0.40),
 "b_red":  p.desaturate(p.mix("yellow_ochre", "cadmium_red", 0.12), 0.50),
 "c_aliz": p.desaturate(p.mix("yellow_ochre", "alizarin", 0.10), 0.45),
 "d_umb":  p.desaturate(p.mix("yellow_ochre", "burnt_umber", 0.20), 0.35),
 "e_sien": p.desaturate(p.mix("yellow_ochre", "burnt_sienna", 0.25), 0.45),
 "f_lem":  p.desaturate(p.mix("lemon_yellow", "burnt_sienna", 0.30), 0.50),
}
n = len(cands)
for i, (name, base) in enumerate(cands.items()):
    c = p.at_value(base, 0.75)
    band = Region(0.02 + i * 0.96 / n, 0.08, 0.02 + (i + 1) * 0.96 / n - 0.01, 0.55)
    s.block_in(band, "flat", c, size=0.06, solid=True)
    print(f"{name:7s} {p.hex(c)} v={p.value_of(c):.2f} chroma={p.chroma_of(c):.3f}")
# below each: the right-wall cool grey and a left-wall candidate, for the neighbours
cool = p.at_value(p.desaturate(p.mix("cerulean", "burnt_umber", 0.40), 0.30), 0.58)
left = p.at_value(p.desaturate(p.mix(p.mix("cerulean", "burnt_umber", 0.40), "yellow_ochre", 0.35), 0.35), 0.64)
s.block_in(Region(0.02, 0.60, 0.49, 0.95), "flat", cool, size=0.06, solid=True)
s.block_in(Region(0.51, 0.60, 0.98, 0.95), "flat", left, size=0.06, solid=True)
print("cool", p.hex(cool), "left", p.hex(left), p.chroma_of(left))
print(s.look())
