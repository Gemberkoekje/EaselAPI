exec(open("_pal.py").read())
exec(open("_geom.py").read())
p["sill_shad"] = at(p.desaturate(p.mix(_warmgrey, "ultramarine", 0.30), 0.28), 0.380)
p["sill_arris"]= at(p.desaturate(p.mix(_warmgrey, "cadmium_yellow", 0.32), 0.35), 0.800)
p["glow"]      = at(p.mix("burnt_umber", "burnt_sienna", 0.35), 0.245)
s.dry()

# repairs: the two brown bars, and a yellow remnant left over the sill's back edge
s.block_in(UNDER, "flat", "under", direction=(5, 96), density=1.0,
           size=0.055, pressure="even", load=1.0, load_falloff=0.25)
s.block_in(polygon([(0.0,0.500),(0.262,0.505),(0.258,0.616),(0.0,0.612)]),
           "flat", "glass", direction=(6, 100), density=1.0, size=0.045,
           pressure="even", load=1.0)
s.dry()
# a faint bounce off the sill's underside, nothing more
for a, b, o in [((0.06,0.900),(0.42,0.892),0.09), ((0.36,0.884),(0.74,0.898),0.08),
                ((0.70,0.905),(0.99,0.916),0.07)]:
    s.glaze([a, b], "glow", opacity=o)

# --- the cast shadow, running left and forward off the pot -----------------
CAST = polygon([(0.598,0.702),(0.664,0.752),(0.585,0.792),(0.300,0.788),
                (0.120,0.740),(0.205,0.694),(0.410,0.684)])
s.block_in(CAST.inset(0.017), "flat", "sill_shad", direction="axis", density=0.95,
           size=0.034, pressure="even", load=1.0)
# lacy foliage shadow scattered off its top edge - broken, not a line
for x, y, sz, pr in [(0.520,0.686,0.020,0.8),(0.470,0.678,0.014,0.6),(0.418,0.690,0.018,0.9),
                     (0.352,0.676,0.012,0.5),(0.318,0.694,0.016,0.7),(0.262,0.706,0.013,0.6),
                     (0.212,0.700,0.010,0.45),(0.166,0.716,0.014,0.55),(0.128,0.726,0.009,0.4)]:
    s.dab(x, y, "round_hard", "sill_shad", size=sz, press=2 if pr > 0.6 else 1)
# and lose the far end of it
s.smudge([(0.190, 0.724), (0.118, 0.742)], size=0.038)
s.smudge([(0.150, 0.704), (0.098, 0.730)], size=0.032)

# --- the sill's front arris, before the pot stands on it -------------------
s.stroke([(0.010,0.7515),(0.240,0.7615),(0.470,0.7710)], "liner", "sill_arris",
         size=0.005, pressure=[0.25,0.9,0.5,1.0,0.35], load=1.0)
s.stroke([(0.455,0.7705),(0.720,0.7815),(0.995,0.7920)], "liner", "sill_arris",
         size=0.006, pressure=[0.4,1.0,0.55,0.85,0.3], load=1.0)
print(s.stroke_count)
print(s.look())
