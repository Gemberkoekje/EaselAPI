# Pass 4: silhouettes — the edges the picture is about. Back to front.
# Dinghy dropped: three treatments failed; the fault was the drawing.
s.erase(span("D6", "F7"))

s.block_in(far_boat(), "flat", "ink", size=0.008, density=1.0, solid=True,
           direction="axis", edge="hard", opacity=1.0, pressure="even",
           note="subject")
ff, ft = s.pt("far_mast_foot"), s.pt("far_mast_top")
s.stroke([ff, (ff[0] + 0.004, (ff[1] + ft[1]) / 2), ft], "round_hard", "mast",
         size=0.004, opacity=0.70, load=0.55, load_falloff=0.4,
         pressure=[0.7, 0.45, 0.08], note="subject")

s.block_in(mid_boat(), "flat", "ink", size=0.012, density=1.0, solid=True,
           direction="axis", edge="hard", opacity=1.0, pressure="even",
           note="subject")
mf, mt = s.pt("mid_mast_foot"), s.pt("mid_mast_top")
s.stroke([mf, (mf[0] - 0.006, (mf[1] + mt[1]) / 2), mt], "round_hard", "mast",
         size=0.005, opacity=0.80, load=0.60, load_falloff=0.35,
         pressure=[0.85, 0.5, 0.10], note="subject")
s.stroke([P(0.20, 0.50, 11.1), P(1.35, 0.48, 12.4)], "round_hard", "glow_band",
         size=0.007, opacity=0.70, load=0.85, load_falloff=0.2,
         pressure=[0.15, 0.8, 0.2], note="subject")

s.look(region=span("A4", "D6"), path="pass4_far_boats.png")

along = (P(2.80, 0.42, 4.3), P(2.80, 0.42, 17.0))
s.block_in(pier_deck(), "flat", "pier", size=0.016, density=1.0,
           solid=True, direction=along, edge="hard", opacity=1.0,
           pressure="even")
s.stroke([P(2.25, 0.44, 4.5), P(2.30, 0.44, 16.0)], "bristle", "warm_dark",
         size=0.012, load=0.40, opacity=0.35, pressure="swell")
s.stroke([P(3.20, 0.44, 4.6), P(3.15, 0.44, 15.0)], "bristle", "ink",
         size=0.010, load=0.35, opacity=0.30, pressure="swell")

s.stroke([P(2.20, 0.02, 5.4), P(2.22, 1.05, 5.4)], "round_hard", "ink",
         size=0.006, opacity=0.88, load=1.0, load_falloff=0.0,
         pressure=[0.2, 0.9, 0.25], note="subject")
s.stroke([P(2.18, 0.02, 7.6), P(2.21, 0.95, 7.6)], "round_hard", "ink",
         size=0.005, opacity=0.80, load=1.0, load_falloff=0.0,
         pressure=[0.2, 0.85, 0.2], note="subject")
s.stroke([P(2.19, 0.02, 10.8), P(2.20, 0.80, 10.8)], "round_hard", "warm_dark",
         size=0.004, opacity=0.70, load=0.85, load_falloff=0.2,
         pressure=[0.2, 0.7, 0.15], note="subject")

s.stroke([P(-5.0, 0.02, 23.2), P(-3.4, 0.02, 24.5)], "bristle", "ink",
         size=0.008, load=0.40, opacity=0.30, pressure="swell")
s.stroke([P(-0.5, 0.02, 10.3), P(1.5, 0.02, 12.4)], "bristle", "ink",
         size=0.012, load=0.45, opacity=0.35, pressure="swell")

s.look(path="pass4_colour.png")
s.look(values=True, path="pass4_values.png")
