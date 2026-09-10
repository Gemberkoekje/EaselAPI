exec(open("_pal.py").read())
exec(open("_geom.py").read())
exec(open("_plant.py").read())
rng = random.Random(1151)
_t2 = p.mix(p.mix("burnt_sienna", "cadmium_red", 0.18), "yellow_ochre", 0.22)
p["arris2"]  = at(p.desaturate(p.mix(_warmgrey, "cadmium_yellow", 0.34), 0.34), 0.790)
p["needle"]  = at(p.desaturate(p.mix(_sage, "cadmium_yellow", 0.26), 0.50), 0.635)
p["potcatch"]= at(p.desaturate(p.mix(_t2, "cadmium_yellow", 0.36), 0.24), 0.775)
p["sig"]     = at(p.mix("burnt_umber", "burnt_sienna", 0.45), 0.275)
s.dry()

# --- quiet the face down to one plane, with a little variation -----------
s.block_in(FACE, "flat", "sill_face", direction=(3, 168), density=1.0, size=0.032,
           pressure="even", load=1.0, load_falloff=0.0, overhang=0)
for x0, x1, y, v, sz in [(0.66,0.99,0.822,0.335,0.026),(0.74,0.99,0.852,0.318,0.020),
                         (0.04,0.31,0.806,0.278,0.024),(0.10,0.36,0.842,0.286,0.018),
                         (0.42,0.68,0.828,0.296,0.016)]:
    s.stroke([(x0, y + 0.040*x0), (x1, y + 0.040*x1)], "flat",
             at(p.desaturate(p.mix(_warmgrey, "ultramarine", 0.30), 0.32), v),
             size=sz, pressure="even", load=1.0, load_falloff=0.0)
s.dry()
for a, b, sz, pr in [((0.030,0.7528),(0.176,0.7588),0.0035,[0.1,0.45,0.2]),
                     ((0.248,0.7616),(0.390,0.7674),0.0035,[0.2,0.6,0.15,0.35]),
                     ((0.735,0.7815),(0.868,0.7870),0.0050,[0.3,1.0,0.45,0.9,0.2]),
                     ((0.888,0.7880),(0.994,0.7918),0.0045,[0.5,0.85,0.2])]:
    s.stroke([a, b], "liner", "arris2", size=sz, pressure=pr, load=1.0)

# --- highlights: few, and last ------------------------------------------
s.dab(0.7055, 0.5060, "round_hard", "potcatch", size=0.010, press=3)      # 1 lip
s.stroke([(0.6820,0.4980),(0.7180,0.5115)], "liner", "potcatch", size=0.0045,
         pressure=[0.2,0.9,0.35], load=1.0)                               # 2 lip's turn
s.dab(0.7085, 0.5960, "round_hard", "potcatch", size=0.008, press=3)      # 3 belly
s.dab(0.7620, 0.7832, "round_hard", "arris2", size=0.0065, press=3)       # 4 sill's nose
for x, y, a, ln, sz in [(0.7480,0.2180,52,0.030,0.007),(0.8060,0.1880,40,0.026,0.006),
                        (0.8620,0.2640,26,0.028,0.007),(0.7820,0.3020,64,0.022,0.006),
                        (0.9080,0.3320,14,0.024,0.006)]:
    s.stroke(stem(a, ln, origin=(x, y), bow=rng.uniform(-0.3,0.3), sag=0.0, rng=rng),
             "bristle", "needle", size=sz, pressure="taper", load=0.85)   # 5-9 needles
s.dab(0.1720, 0.1540, "round_hard", "glass_hot", size=0.005, press=3)     # 10 a mote

# --- sign it ------------------------------------------------------------
s.stroke([(0.9280,0.9560),(0.9420,0.9480),(0.9520,0.9585),(0.9605,0.9490)],
         "liner", "sig", size=0.0040, pressure=[0.2,0.9,0.5,0.8,0.15], load=1.0,
         note="signature")
print(s.stroke_count)
print(s.look())
