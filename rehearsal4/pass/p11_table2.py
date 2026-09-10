"""Pass A2 - the table again. The jagged polygon band was a mistake: paint over it.
Soft round masses this time, and a value gradient instead of a cut-out."""
p = s.palette

p["table_base"] = p.desaturate(p.mix(p.mix("cadmium_yellow", "burnt_umber", 0.65),
                                     "titanium_white", 0.42), 0.30)
p["table_lit"] = p.desaturate(p.mix(p.mix("cadmium_yellow", "burnt_umber", 0.6),
                                    "titanium_white", 0.58), 0.25)
p["table_glow"] = p.desaturate(p.mix(p.mix("lemon_yellow", "burnt_umber", 0.7),
                                     "titanium_white", 0.66), 0.20)
p["table_dark"] = p.desaturate(p.mix(p.mix("cadmium_yellow", "burnt_umber", 0.6),
                                     "titanium_white", 0.26), 0.40)
for n in ("table_base", "table_lit", "table_glow", "table_dark"):
    print(f"{n:11s} {p.hex(p[n])}  v={p.value_of(p[n]):.2f}")

s.dry()
s.block_in("all", "flat", "table_base", direction=(8, 98), density=1.0,
           size=0.24, load=1.0, load_falloff=0.2)
print("after base:", s.stroke_count)

# the light comes across the table from the right - one broad soft mass,
# not a band with corners in it
s.block_in(ellipse(Region(0.55, 0.02, 0.95, 0.86), rotate=-12), "flat",
           "table_lit", direction=(-72,), density=0.95, size=0.19, load=1.0)
s.block_in(ellipse(Region(0.30, 0.72, 0.82, 1.06)), "flat", "table_lit",
           direction=(-8,), density=0.95, size=0.17, load=1.0)
print("after lit:", s.stroke_count)

# the hot core of it, around F4-F6
s.block_in(ellipse(Region(0.60, 0.26, 0.84, 0.78), rotate=-10), "flat",
           "table_glow", direction=(-78,), density=0.9, size=0.15, load=1.0)
s.block_in(ellipse(Region(0.36, 0.84, 0.70, 1.06)), "flat", "table_glow",
           direction=(-6,), density=0.9, size=0.13, load=1.0)
print("after glow:", s.stroke_count)

# the shadowed left of the table, and the dark far edge top right
s.block_in(ellipse(Region(-0.22, -0.10, 0.17, 1.10)), "flat", "table_dark",
           direction=(84,), density=0.9, size=0.16, load=1.0)
s.block_in(polygon([(0.855, -0.02), (1.02, -0.02), (1.02, 0.06), (0.88, 0.018)]),
           "flat", p.mix("ultramarine", "burnt_umber", 0.55), direction="axis",
           density=1.0, size=0.05, load=1.0)

print("strokes:", s.stroke_count)
print(s.look())
