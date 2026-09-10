p = s.palette; dk = p["dk"]
tc = p.mix("burnt_sienna", "cadmium_red", 0.30)
warm = p.mix("yellow_ochre", "titanium_white", 0.40)
print("tc", p.hex(tc), round(p.value_of(tc),2), " warm", p.hex(warm), round(p.value_of(warm),2))
for r in (0.15,0.3,0.45,0.6,0.75):
    c = p.mix(tc, warm, r); print(f"  tc+warm {r:.2f}", p.hex(c), round(p.value_of(c),2))
for r in (0.1,0.2,0.35,0.5):
    c = p.mix(tc, "yellow_ochre", r); print(f"  tc+ochre {r:.2f}", p.hex(c), round(p.value_of(c),2))
for r in (0.15,0.3,0.45,0.6):
    c = p.mix(tc, dk, r); print(f"  tc+dk {r:.2f}", p.hex(c), round(p.value_of(c),2))
for r in (0.2,0.35,0.5):
    c = p.mix(p.mix(tc,dk,0.45), "cadmium_red", r); print(f"  refl {r:.2f}", p.hex(c), round(p.value_of(c),2))
