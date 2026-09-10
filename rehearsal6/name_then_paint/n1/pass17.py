# Pass 17 - flower heads swept round their own outlines, so passes follow petals.
p = s.palette
grey = p.mix("ultramarine", "burnt_sienna", 0.50)
p["pet_core"] = p.tint(grey, 0.48)
p["pet_sh"]   = p.tint(grey, 0.62)
p["pet_half"] = p.tint(grey, 0.745)
p["pet_halfw"]= p.tint(p.mix(p.mix("burnt_umber","yellow_ochre",0.55),"viridian",0.10), 0.70)
p["pet_lt"]   = p.mix("titanium_white", p.mix("yellow_ochre","cadmium_red",0.25), 0.16)
for k in ("pet_core","pet_sh","pet_half","pet_halfw","pet_lt"):
    print(f"{k:10s} {p.hex(p[k])}  v={p.value_of(p[k]):.3f}")
s.dry()

s.block_in(polygon([(0.305,0.305),(0.775,0.300),(0.775,0.565),(0.305,0.560)]), "flat",
           "bg", direction=(34, 124), density=1.0, size=0.048, load=1.0, pressure="even")

heads = [
    ("bud", (0.556,0.372), 0.050, 0.044, "pet_sh",    0.016, 0.055),
    ("A",   (0.442,0.436), 0.100, 0.092, "pet_halfw", 0.022, 0.105),
    ("B",   (0.640,0.520), 0.112, 0.100, "pet_half",  0.024, 0.115),
    ("C",   (0.398,0.586), 0.078, 0.066, "pet_half",  0.019, 0.080),
]
ells = {}
for name, (cx, cy), rx, ry, col, sz, dep in heads:
    e = ellipse(Region(cx-rx, cy-ry, cx+rx, cy+ry))
    ells[name] = (e, cx, cy, rx, ry)
    s.sweep(e, "flat", col, depth=dep, size=sz, load=1.0, pressure="even")
    print(name, s.stroke_count)

print("strokes:", s.stroke_count)
print(s.look(sketch=False))
