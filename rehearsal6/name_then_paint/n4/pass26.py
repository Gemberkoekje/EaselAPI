exec(open("_pal.py").read())
exec(open("_geom.py").read())
import random
rng = random.Random(1049)
p["arris2"] = at(p.desaturate(p.mix(_warmgrey, "cadmium_yellow", 0.34), 0.34), 0.790)
s.dry()

s.block_in(FACE, "flat", "sill_face", direction=(3, 168), density=1.0, size=0.030,
           pressure="even", load=1.0, load_falloff=0.0, overhang=0)
# raking light along the face: short overlapping passes, none the full width
for x0, x1, y, v, sz in [(0.60,0.99,0.812,0.348,0.024),(0.66,0.99,0.838,0.330,0.022),
                         (0.72,0.99,0.860,0.312,0.020),(0.38,0.72,0.806,0.318,0.022),
                         (0.44,0.78,0.834,0.306,0.020),(0.02,0.34,0.788,0.288,0.022),
                         (0.02,0.40,0.816,0.272,0.024),(0.06,0.38,0.846,0.262,0.020),
                         (0.30,0.62,0.856,0.282,0.018)]:
    col = at(p.desaturate(p.mix(_warmgrey, "ultramarine", 0.30), 0.32), v)
    s.stroke([(x0, y + 0.040*x0), (x1, y + 0.040*x1)], "flat", col,
             size=sz, pressure="even", load=1.0, load_falloff=0.0)
s.dry()
for a, b, sz, pr in [((0.010,0.7520),(0.185,0.7592),0.004,[0.15,0.65,0.25]),
                     ((0.238,0.7612),(0.396,0.7676),0.004,[0.3,0.8,0.2,0.5]),
                     ((0.735,0.7815),(0.868,0.7870),0.005,[0.3,1.0,0.45,0.9,0.2]),
                     ((0.885,0.7878),(0.995,0.7918),0.005,[0.55,0.9,0.2])]:
    s.stroke([a, b], "liner", "arris2", size=sz, pressure=pr, load=1.0)
s.dab(0.7620, 0.7830, "round_hard", "arris2", size=0.006, press=2)
print(s.stroke_count)
print(s.look(region="A6:H8"))
