s.dry()
p["edge_lit"] = p.at_value(p.mix("deck", "watlit", 0.35), 0.46)
p["chair"]    = p.at_value(p.mix("ultramarine", "burnt_umber", 0.50), 0.155)
p["board"]    = p.at_value(p.mix("ultramarine", "burnt_umber", 0.45), 0.22)

# The deck glazes buried the chair. Re-laid at its own depth against the darker deck
# it now stands on, so it is a step further down than before.
for pts, size, op in [([(0.134, 0.524), (0.146, 0.390), (0.153, 0.272)], 0.0065, 0.95),
                      ([(0.192, 0.536), (0.184, 0.398), (0.177, 0.278)], 0.0060, 0.95),
                      ([(0.138, 0.498), (0.188, 0.320)],                 0.0035, 0.80),
                      ([(0.131, 0.272), (0.196, 0.281)],                 0.0130, 0.95),
                      ([(0.166, 0.268), (0.163, 0.243)],                 0.0230, 0.95)]:
    s.stroke(pts, "flat", "chair", size=size, opacity=op, load=1.0,
             load_falloff=0.0, pressure="even")
s.stroke([(0.178, 0.276), (0.176, 0.245)], "liner", "edge_lit",
         size=0.0035, opacity=0.85, load=0.6, load_falloff=0.75, pressure=[1.0, 0.3])
s.stroke([(0.187, 0.516), (0.181, 0.400)], "liner", "edge_lit",
         size=0.0028, opacity=0.55, load=0.45, load_falloff=0.85, pressure=[0.9, 0.1])

# the board came back a comb of streaks: a flat cannot lay a slab that narrow.
# The knife can -- it is the tool for a thick slab with a hard edge.
s.stroke([(1.04, 0.508), (0.900, 0.552), (0.768, 0.592)], "knife", "board",
         size=0.011, opacity=1.0, load=1.0, load_falloff=0.0, pressure="even",
         jitter=0.010, size_jitter=0.030)
s.stroke([(0.982, 0.534), (0.856, 0.575), (0.772, 0.601)], "liner", "edge_lit",
         size=0.0035, opacity=0.85, load=0.55, load_falloff=0.8, pressure=[0.2, 1.0, 0.55])

# and two quiet darks in the pale stretch between the lamps
s.glaze([(0.440, 0.610), (0.560, 0.630), (0.660, 0.612)], p.at_value("water", 0.52),
        opacity=0.30, size=0.075, pressure="swell", note="subject")
s.glaze([(0.498, 0.692), (0.622, 0.708)], p.at_value("water", 0.54),
        opacity=0.24, size=0.055, pressure="taper", note="subject")
print(s.look())
