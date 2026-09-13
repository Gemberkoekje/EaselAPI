from easel import Session

p = Session(600, 200, seed=6, timelapse=False).palette
for a, b in [("cadmium_yellow", "ultramarine"), ("cadmium_red", "ultramarine"),
             ("cadmium_yellow", "cadmium_red"), ("cerulean", "titanium_white"),
             ("viridian", "cerulean"), ("viridian", "titanium_white"),
             ("cerulean", "burnt_umber"), ("ultramarine", "burnt_umber")]:
    m = p.mix(a, b, 0.5)
    print(f"{a:15s} + {b:15s} -> {p.hex(m)}  value {p.value_of(m):.2f}  chroma {p.chroma_of(m):.2f}")
