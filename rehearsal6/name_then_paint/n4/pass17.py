exec(open("_pal.py").read())
exec(open("_geom.py").read())
exec(open("_pot.py").read())
exec(open("_plant.py").read())
rng = random.Random(91)
_t2 = p.mix(p.mix("burnt_sienna", "cadmium_red", 0.18), "yellow_ochre", 0.22)
p["pot_core"] = at(p.desaturate(p.mix(_t2, "ultramarine", 0.26), 0.16), 0.228)
p["pot_c2"]   = at(p.desaturate(p.mix(_t2, "ultramarine", 0.22), 0.16), 0.258)
p["pot_edge"] = at(p.desaturate(p.mix(_t2, "cerulean", 0.26), 0.24), 0.335)
p["pot_turn"] = at(p.desaturate(p.mix(_t2, "cadmium_yellow", 0.14), 0.24), 0.450)
p["contact2"] = at(p.desaturate(p.mix(_warmgrey, "ultramarine", 0.35), 0.15), 0.235)
p["bloom"]    = at(p.desaturate(p.mix(_t2, "cerulean", 0.30), 0.55), 0.560)
p["crackw"]   = at(p.mix(_t2, "burnt_umber", 0.55), 0.190)
p["woody"]    = at(p.desaturate(p.mix("burnt_umber", "viridian", 0.22), 0.30), 0.245)
p["woody_l"]  = at(p.desaturate(p.mix("burnt_umber", "yellow_ochre", 0.35), 0.35), 0.420)
s.dry()

def body_stroke(u, ya, yb, n=7):
    return [(CX + u * hw(max(0.5545, ya + (yb - ya) * i / (n - 1.0))),
             ya + (yb - ya) * i / (n - 1.0)) for i in range(n)]

# --- give the shadow side its core ----------------------------------------
for u, col in [(-1.00,"pot_edge"),(-0.90,"pot_c2"),(-0.79,"pot_core"),(-0.68,"pot_core"),
               (-0.57,"pot_c2"),(-0.46,"pot_c2"),(-0.35,"pot_shad"),(-0.25,"pot_shad")]:
    uu = u + rng.uniform(-0.02, 0.02)
    k = (1.0 - min(0.999, uu * uu)) ** 0.5
    ya = max(0.5555, 0.5460 + 0.0325 * k + 0.003) + rng.uniform(0.0, 0.008)
    yb = 0.7455 + 0.0140 * k - rng.uniform(0.0, 0.016)
    s.stroke(body_stroke(uu, ya, yb), "flat", col, size=rng.uniform(0.015, 0.020),
             pressure="even", load=1.0)
s.stroke(ring(0.6250, 0.014, -0.95, -0.30), "bristle", "pot_c2", size=0.012,
         pressure="taper", load=0.8)
s.stroke(ring(0.7000, 0.017, -0.90, -0.20), "bristle", "pot_core", size=0.011,
         pressure="lift_off", load=0.7)
s.stroke(ring(0.6600, 0.016, 1.00, 0.86), "bristle", "pot_turn", size=0.010,
         pressure="taper", load=0.8)
for a, b in [((0.5430,0.600),(0.5455,0.672)),((0.5760,0.612),(0.5790,0.688)),
             ((0.6060,0.640),(0.6080,0.700))]:
    s.smudge([a, b], size=0.011)
# chalky bloom, a few broken marks
for x0, y0, x1, y1, sz in [(0.5560,0.6300,0.5720,0.6180,0.007),
                           (0.6420,0.6900,0.6650,0.6820,0.006),
                           (0.6900,0.6050,0.7010,0.5950,0.005)]:
    s.stroke([(x0,y0),(x1,y1)], "bristle", "bloom", size=sz, pressure="taper", load=0.45)

# --- the pot meets the sill -----------------------------------------------
s.stroke(arc(CX, 0.7530, 0.0715, 0.0165, 168, 12, 20), "flat", "contact2",
         size=0.009, pressure="even", load=1.0, note="contact")
s.smudge([(0.5560, 0.7595), (0.4900, 0.7570)], size=0.020)
s.smudge([(0.6900, 0.7640), (0.7250, 0.7620)], size=0.016)

# --- soften the crack at its ends, warm its middle ------------------------
s.stroke([(0.5920,0.5960),(0.5955,0.6280),(0.5895,0.6560)], "liner", "crackw",
         size=0.0034, pressure=[0.5,1.0,0.6], load=1.0)
s.smudge([(0.5900, 0.5590), (0.5895, 0.5680)], size=0.008)
s.smudge([(0.5905, 0.7150), (0.5900, 0.7250)], size=0.008)

# --- woody stems rising out of the soil -----------------------------------
for a, ln, o, col in [(96,0.075,(0.598,0.4930),"woody"),(78,0.090,(0.618,0.4905),"woody"),
                      (110,0.070,(0.578,0.4955),"woody"),(66,0.078,(0.648,0.4895),"woody_l"),
                      (86,0.062,(0.664,0.4930),"woody"),(120,0.052,(0.556,0.4975),"woody")]:
    s.stroke(stem(a + rng.uniform(-6,6), ln, origin=o, bow=rng.uniform(-0.3,0.3),
                  sag=0.0, rng=rng), "bristle", col,
             size=rng.uniform(0.006, 0.010), pressure=[1.0, 0.85, 0.3], load=0.9)
print(s.stroke_count)
print(s.look(region="E4:G7"))
