exec(open("_pal.py").read())
exec(open("_geom.py").read())
exec(open("_plant.py").read())
rng = random.Random(937)
p["halo"]    = at(p.desaturate(p.mix(_neutral, "cadmium_yellow", 0.25), 0.30), 0.845)
p["arris2"]  = at(p.desaturate(p.mix(_warmgrey, "cadmium_yellow", 0.34), 0.34), 0.790)
p["face_lo"] = at(p.desaturate(p.mix(_warmgrey, "ultramarine", 0.34), 0.30), 0.255)
p["face_hi"] = at(p.desaturate(p.mix(_warmgrey, "yellow_ochre", 0.30), 0.45), 0.360)
p["glow2"]   = at(p.mix("burnt_umber", "burnt_sienna", 0.40), 0.230)
s.dry()

# --- the light eats into the leaves where they meet the pane -------------
HALO = [(0.4120,0.2560),(0.3640,0.2960),(0.3200,0.3320),(0.2880,0.3720),(0.2560,0.3160),
        (0.4480,0.2200),(0.4900,0.1880),(0.3960,0.4560),(0.3400,0.4760),(0.4620,0.4900),
        (0.5040,0.4360),(0.2960,0.4400),(0.5200,0.1720),(0.4300,0.5000)]
for x, y in HALO:
    a = rng.uniform(150, 215)
    s.stroke(stem(a, rng.uniform(0.014, 0.038), origin=(x, y),
                  bow=rng.uniform(-0.4, 0.4), sag=0.0, rng=rng), "bristle", "halo",
             size=rng.uniform(0.006, 0.016), pressure="taper", load=rng.uniform(0.35, 0.70))
for _ in range(6):
    s.dab(rng.uniform(0.27, 0.50), rng.uniform(0.24, 0.48), "round_hard", "halo",
          size=rng.uniform(0.004, 0.008), press=1)

# --- more body on the right-hand sprigs so they are not debris -----------
for _ in range(22):
    x = rng.uniform(0.800, 0.995); y = rng.uniform(0.230, 0.450)
    a = math.degrees(math.atan2(0.340 - y, x - 0.760)) + rng.uniform(-45, 45)
    s.stroke(stem(a, rng.uniform(0.022, 0.060), origin=(x, y), bow=rng.uniform(-0.4,0.4),
                  sag=0.0, rng=rng), "bristle",
             rng.choice(["leaf_mid","leaf_mid","leaf_dk","leaf_lit"]),
             size=rng.uniform(0.009, 0.024), pressure="taper", load=rng.uniform(0.55,0.95))

# --- the sill's front edge, where the light rakes it ---------------------
for a, b, sz, pr in [((0.735,0.7815),(0.868,0.7870),0.005,[0.3,1.0,0.45,0.9,0.2]),
                     ((0.885,0.7878),(0.995,0.7918),0.005,[0.55,0.9,0.2]),
                     ((0.108,0.7560),(0.226,0.7608),0.004,[0.15,0.7,0.25]),
                     ((0.300,0.7655),(0.392,0.7690),0.004,[0.25,0.6,0.15])]:
    s.stroke([a, b], "liner", "arris2", size=sz, pressure=pr, load=1.0)
s.dab(0.7620, 0.7830, "round_hard", "arris2", size=0.006, press=2)

# --- the front face of the sill, and the dark below it -------------------
for i in range(6):
    t = i / 5.0
    y0 = 0.800 + 0.040 * t
    s.stroke([(0.02, y0 + 0.004), (0.44, y0 + 0.018), (0.99, y0 + 0.036)],
             "flat", at(p.desaturate(p.mix(_warmgrey, "ultramarine", 0.30), 0.32),
                        0.268 + 0.062 * (1.0 - t)),
             size=rng.uniform(0.016, 0.024), pressure="even", load=1.0)
s.stroke([(0.02,0.8180),(0.40,0.8320)], "bristle", "face_lo", size=0.020,
         pressure="taper", load=0.55)
s.stroke([(0.99,0.8480),(0.62,0.8380)], "bristle", "face_hi", size=0.014,
         pressure="taper", load=0.45)
for a, b, o in [((0.06,0.888),(0.44,0.882),0.09),((0.40,0.896),(0.78,0.906),0.08),
                ((0.74,0.900),(0.99,0.912),0.07),((0.10,0.935),(0.52,0.944),0.05)]:
    s.glaze([a, b], "glow2", opacity=o)
print(s.stroke_count)
print(s.look())
