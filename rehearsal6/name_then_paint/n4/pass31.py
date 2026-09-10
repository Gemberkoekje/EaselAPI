exec(open("_pal.py").read())
exec(open("_geom.py").read())
import random
rng = random.Random(1597)
p["backline"] = at(p.desaturate(p.mix(_warmgrey, "ultramarine", 0.32), 0.28), 0.430)
p["grit"]     = at(p.desaturate(p.mix(_warmgrey, "ultramarine", 0.25), 0.25), 0.380)
s.dry()

# where the sill runs back under the window
for a, b, sz, pr in [((0.006,0.6135),(0.212,0.6215),0.0040,[0.15,0.8,0.35,0.6,0.2]),
                     ((0.238,0.6225),(0.404,0.6285),0.0035,[0.25,0.7,0.2]),
                     ((0.440,0.6300),(0.528,0.6335),0.0030,[0.3,0.6,0.15]),
                     ((0.616,0.6365),(0.804,0.6435),0.0038,[0.2,0.85,0.3,0.5]),
                     ((0.836,0.6448),(0.996,0.6508),0.0034,[0.4,0.7,0.15])]:
    s.stroke([a, b], "liner", "backline", size=sz, pressure=pr, load=1.0)
for _ in range(11):
    x = rng.uniform(0.02, 0.46); y = rng.uniform(0.640, 0.744)
    s.dab(x, y, "round_hard", "grit", size=rng.uniform(0.0030, 0.0065), press=1)
for x0,y0,x1,y1,sz in [(0.086,0.688,0.152,0.680,0.004),(0.262,0.712,0.322,0.718,0.0035),
                       (0.836,0.700,0.918,0.706,0.0035)]:
    s.stroke([(x0,y0),(x1,y1)], "liner", "grit", size=sz,
             pressure=[0.15,0.7,0.25], load=1.0)
print(s.stroke_count)
print(s.look())
