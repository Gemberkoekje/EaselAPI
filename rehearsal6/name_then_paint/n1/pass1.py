# Pass 1 - the far masses: background field, its warm glow, and the table plane.
p = s.palette

p["bg"]       = p.mix("ultramarine", "burnt_umber", 0.62)          # 0.134 deep warm dark
p["bg_cool"]  = p.mix("ultramarine", "burnt_umber", 0.42)          # 0.14 cooler dark
p["bg_lift"]  = p.tint(p.mix("ultramarine", "burnt_umber", 0.68), 0.24)
p["bg_glow"]  = p.tint(p.mix(p.mix("ultramarine","burnt_umber",0.72), "yellow_ochre", 0.22), 0.30)

p["wood_dk"]  = p.mix(p.mix("burnt_umber","burnt_sienna",0.40), "ultramarine", 0.30)   # 0.146
p["wood"]     = p.tint(p.mix("burnt_umber","burnt_sienna",0.45), 0.28)
p["wood_lit"] = p.tint(p.mix(p.mix("burnt_umber","burnt_sienna",0.5),"yellow_ochre",0.30), 0.40)

for k in ("bg","bg_cool","bg_lift","bg_glow","wood_dk","wood","wood_lit"):
    print(f"{k:9s} {p.hex(p[k])}  v={p.value_of(p[k]):.3f}")

# --- the dark field, in two overlapping wedges at unrelated angles -------------
left_dark  = polygon([(0.0, 0.0), (0.58, 0.0), (0.34, 0.82), (0.0, 0.80)])
right_dark = polygon([(0.44, 0.0), (1.0, 0.0), (1.0, 0.84), (0.50, 0.80)])

s.block_in(left_dark,  "bristle", "bg",      direction=(64, 118), density=1.0,
           size=0.16, load=1.0, load_falloff=0.18)
s.block_in(right_dark, "bristle", "bg_cool", direction=(72, 128), density=1.0,
           size=0.15, load=1.0, load_falloff=0.18)

# a second, warmer beat over the right so the two wedges are not two colours
s.block_in(polygon([(0.62,0.05),(1.0,0.0),(1.0,0.55),(0.68,0.62)]), "flat", "bg",
           direction=(38, 130), density=0.8, size=0.13, load=0.8)

# --- the glow behind where the flowers will be --------------------------------
glow = ellipse(Region(0.14, 0.10, 0.70, 0.60))
s.block_in(glow.inset(0.05), "bristle", "bg_lift", direction=(24, 96), density=0.6,
           size=0.12, load=0.75)
s.block_in(ellipse(Region(0.24, 0.17, 0.58, 0.47)), "bristle", "bg_glow",
           direction=(18, 104), density=0.45, size=0.10, load=0.6)

s.dry()

# --- the table: swept along its own (tilted) far edge --------------------------
table_edge = [(0.0, 0.706), (0.31, 0.712), (0.63, 0.719), (1.0, 0.729)]
s.sweep(table_edge, "bristle", "wood", into="down", depth=0.30, size=0.13,
        cross=17, load=1.0, load_falloff=0.20)
# warmer, lighter toward the near left where the light falls
s.sweep([(0.0, 0.80), (0.38, 0.83), (0.72, 0.88)], "flat", "wood_lit", into="down",
        depth=0.15, size=0.11, cross=14, load=0.85)
# the far right of the table sinks back into the dark
s.block_in(polygon([(0.72,0.74),(1.0,0.75),(1.0,0.97),(0.76,0.93)]), "flat", "wood_dk",
           direction=(9, 148), density=0.7, size=0.11, load=0.8)

print("strokes:", s.stroke_count)
print(s.look())
print(s.look(values=True))
