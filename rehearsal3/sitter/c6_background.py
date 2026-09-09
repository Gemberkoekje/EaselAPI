# Pass 6: the background masses. Big flat brush, largest decisions first.
REF = "C:/temp/Level3.jpg"
p = s.palette

p["coat"]      = p.shade(p.mix("ultramarine", "burnt_umber", 0.62), 0.55)
p["bg_dark"]   = p.mix(p.mix("burnt_umber", "ultramarine", 0.25), "titanium_white", 0.12)
p["bg_mid"]    = p.mix(p.mix("burnt_umber", "yellow_ochre", 0.45), "titanium_white", 0.22)
p["bg_lit"]    = p.mix(p.mix("yellow_ochre", "burnt_sienna", 0.30), "titanium_white", 0.48)
p["bg_hi"]     = p.mix(p.mix("yellow_ochre", "burnt_sienna", 0.20), "titanium_white", 0.68)
p["bg_cool"]   = p.mix(p.mix("ultramarine", "burnt_umber", 0.45), "titanium_white", 0.20)

n0 = s.stroke_count
# one warm wall across the whole upper band, then modulate it
s.block_in(span("A1", "H4"), "flat", "bg_mid", density=1.0, size=0.17,
           direction="horizontal")
print("upper band:", s.stroke_count - n0)

n0 = s.stroke_count
s.block_in(span("F1", "H3"), "flat", "bg_lit", density=0.95, size=0.15,
           direction="vertical")
s.block_in(span("G1", "H2"), "flat", "bg_hi", density=0.8, size=0.12,
           direction="diagonal")
print("lit wall:", s.stroke_count - n0)

n0 = s.stroke_count
s.block_in(span("A1", "B2"), "flat", "bg_dark", density=0.9, size=0.14,
           direction="diagonal")
s.block_in(span("E1", "F2"), "flat", "bg_cool", density=0.85, size=0.13,
           direction="horizontal")
print("darks top:", s.stroke_count - n0)

n0 = s.stroke_count
s.block_in(span("A3", "B6"), "flat", "bg_dark", density=0.9, size=0.14,
           direction="vertical")
s.block_in(span("A3", "A6"), "flat", "bg_lit", density=0.7, size=0.10,
           direction="vertical")
print("left bg:", s.stroke_count - n0)

n0 = s.stroke_count
s.block_in(span("G5", "H8"), "flat", "bg_mid", density=0.85, size=0.14,
           direction="diagonal")
s.block_in(span("G6", "H7"), "flat", "bg_lit", density=0.75, size=0.11,
           direction="horizontal")
print("table:", s.stroke_count - n0)

s.dry()
print("look:", s.look(reference=REF, grid=True))
print("vals:", s.look(reference=REF, values=True))
print("TOTAL strokes:", s.stroke_count)
