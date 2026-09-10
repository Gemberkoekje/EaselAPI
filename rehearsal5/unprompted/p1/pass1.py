p = s.palette

# --- the three values, planned as numbers before anything is mixed -------------
p["dark"]      = p.mix("ultramarine", "burnt_umber", 0.42)          # bottom of range
p["shore"]     = p.tint(p.mix("ultramarine", "burnt_umber", 0.55), 0.20)
p["mud"]       = p.tint(p.mix("burnt_umber", "yellow_ochre", 0.40), 0.30)
p["mud_lit"]   = p.tint(p.mix("burnt_umber", "yellow_ochre", 0.55), 0.52)
p["sheen"]     = p.tint(p.mix("cerulean", "burnt_sienna", 0.30), 0.62)
p["sky_high"]  = p.tint(p.mix("cerulean", "alizarin", 0.28), 0.58)
p["sky_low"]   = p.tint(p.mix("yellow_ochre", "cadmium_red", 0.28), 0.72)
p["glow"]      = p.tint(p.mix("cadmium_yellow", "cadmium_red", 0.22), 0.60)

for n in ("dark", "shore", "mud", "mud_lit", "sheen", "sky_high", "sky_low", "glow"):
    print(f"{n:9s} {p.hex(p[n])}  {p.value_of(p[n]):.2f}")

# --- furthest thing first: the sky --------------------------------------------
sky = span("A1", "H3")
s.block_in(sky, "flat", "sky_high", direction=(5, 95), density=0.9, size=0.20)

# a warm band of light low in it - a ribbon, not a rectangle
low = ribbon([(0.02, 0.315), (0.34, 0.295), (0.68, 0.305), (0.99, 0.285)], 0.15)
s.block_in(low, "flat", "sky_low", direction="axis", density=0.9, size=0.09)

print("strokes", s.stroke_count)
print(s.look(grid=True))
