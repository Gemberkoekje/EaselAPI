# Pass 16 - the four flower heads as masses, at half-tone. No lights yet.
p = s.palette
grey = p.mix("ultramarine", "burnt_sienna", 0.50)
p["pet_sh"]   = p.tint(grey, 0.58)
p["pet_sh2"]  = p.tint(p.mix("ultramarine","burnt_umber",0.55), 0.66)
p["pet_halfc"]= p.tint(grey, 0.80)
p["pet_halfw"]= p.tint(p.mix(p.mix("burnt_umber","yellow_ochre",0.55),"viridian",0.10), 0.78)
p["pet_lit"]  = p.mix("titanium_white", "yellow_ochre", 0.10)
p["pet_hi"]   = "titanium_white"
p["pet_heart"]= p.mix(p.mix("yellow_ochre","viridian",0.35), "titanium_white", 0.62)
p["pet_warm"] = p.mix("titanium_white", p.mix("yellow_ochre","cadmium_red",0.25), 0.16)
for k in ("pet_sh","pet_sh2","pet_halfc","pet_halfw","pet_lit","pet_hi","pet_heart","pet_warm"):
    print(f"{k:10s} {p.hex(p[k])}  v={p.value_of(p[k]):.3f}")
s.dry()

blooms = [
    ("bud", Region(0.508,0.327,0.604,0.409), 0.34, 31, "pet_sh2",   0.018),
    ("A",   Region(0.342,0.344,0.530,0.516), 0.30, 17, "pet_halfw", 0.030),
    ("B",   Region(0.540,0.418,0.752,0.606), 0.32, 23, "pet_halfc", 0.032),
    ("C",   Region(0.330,0.530,0.466,0.646), 0.36, 41, "pet_halfc", 0.024),
]
for name, box, wob, sd, col, sz in blooms:
    shp = blob(box, wobble=wob, seed=sd)
    s.block_in(shp.inset(sz * 0.55), "flat", col, direction=("axis", 68), density=1.0,
               size=sz, load=1.0, pressure="even")
    print(name, "done", s.stroke_count)

print("strokes:", s.stroke_count)
print(s.look(sketch=False))
print(s.look(values=True, sketch=False))
