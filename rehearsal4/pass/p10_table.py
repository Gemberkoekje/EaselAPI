"""Pass A - the furthest thing: the table top. Big brush, no detail."""
p = s.palette

# --- the mixtures, planned as values before anything is mixed ------------
p["table_base"] = p.desaturate(p.mix(p.mix("cadmium_yellow", "burnt_umber", 0.7),
                                     "titanium_white", 0.45), 0.30)
p["table_lit"] = p.desaturate(p.mix(p.mix("lemon_yellow", "burnt_umber", 0.7),
                                    "titanium_white", 0.65), 0.25)
p["table_dark"] = p.desaturate(p.mix(p.mix("cadmium_yellow", "burnt_umber", 0.6),
                                     "titanium_white", 0.30), 0.40)
p["edge_dark"] = p.mix("ultramarine", "burnt_umber", 0.55)

for n in ("table_base", "table_lit", "table_dark", "edge_dark"):
    print(f"{n:11s} {p.hex(p[n])}  v={p.value_of(p[n]):.2f}")

# --- the whole table, crossed, biggest brush in the painting ------------
s.block_in("all", "flat", "table_base", direction=(9, 99), density=1.0,
           size=0.20, load=1.0, load_falloff=0.2)
print("after base:", s.stroke_count)

# --- the lit band: upper right, down the right, sweeping along the bottom
lit = polygon([(0.62, 0.13), (0.80, 0.09), (0.90, 0.22), (0.90, 0.45),
               (0.86, 0.66), (0.80, 0.83), (0.72, 0.96), (0.55, 1.02),
               (0.40, 1.00), (0.33, 0.90), (0.41, 0.80), (0.56, 0.74),
               (0.63, 0.60), (0.63, 0.34)])
s.preview(lit)
s.block_in(lit, "flat", "table_lit", direction="axis", density=0.95,
           size=0.17, load=1.0, load_falloff=0.15)
print("after lit:", s.stroke_count)

# --- the shadowed left of the table -------------------------------------
darkside = polygon([(-0.02, -0.02), (0.30, -0.02), (0.24, 0.30), (0.20, 0.62),
                    (0.22, 1.02), (-0.02, 1.02)])
s.block_in(darkside, "flat", "table_dark", direction="axis", density=0.9,
           size=0.16, load=1.0, load_falloff=0.15)

# --- the dark far edge of the table, top right --------------------------
faredge = polygon([(0.855, -0.02), (1.02, -0.02), (1.02, 0.055), (0.88, 0.015)])
s.block_in(faredge, "flat", "edge_dark", direction="axis", density=1.0,
           size=0.05, load=1.0)

print("strokes:", s.stroke_count)
print(s.look())
print(s.look(values=True, reference="ref.jpg"))
