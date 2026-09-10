exec(open("_pal.py").read())
exec(open("_geom.py").read())
import random, math
rng = random.Random(401)
p["dust_l"] = at(p.desaturate(p.mix(_neutral, "cadmium_yellow", 0.22), 0.35), 0.868)
s.dry()

# --- clean the speckled glass -------------------------------------------
s.block_in(polygon([(0.012,0.296),(0.272,0.296),(0.270,0.606),(0.014,0.602)]),
           "flat", "glass", direction=(97, 15), density=1.0, size=0.052,
           pressure="even", load=1.0, overhang=0)
s.block_in(polygon([(0.300,0.548),(0.548,0.545),(0.548,0.606),(0.300,0.604)]),
           "flat", "glass", direction=(4, 96), density=1.0, size=0.026,
           pressure="even", load=1.0, overhang=0)
s.stroke([(0.292,0.290),(0.286,0.612)], "flat", "bar", size=0.026,
         pressure="even", load=1.0)
s.stroke([(0.300,0.300),(0.295,0.600)], "liner", "bar_lit", size=0.006,
         pressure=[0.3,1.0,0.7,0.2], load=1.0)
s.dry()

# --- the wall's corner: graded, not slabs -------------------------------
s.block_in(polygon([(0.800,0.0),(1.0,0.0),(1.0,0.250),(0.812,0.222)]),
           "flat", "wall", direction=(106, 24), density=1.0, size=0.050,
           pressure="even", load=1.0, overhang=0)
s.dry()
for i in range(9):
    t = i / 8.0
    x = 0.845 + 0.165 * t
    v = 0.400 - 0.075 * t
    col = at(p.desaturate(p.mix(_warmgrey, "ultramarine", 0.22), 0.24), v)
    s.stroke([(x + rng.uniform(-0.008,0.008), -0.01),
              (x + rng.uniform(-0.010,0.010), 0.115),
              (x + 0.012 + rng.uniform(-0.010,0.010), 0.245 + rng.uniform(-0.03,0.05))],
             "flat", col, size=rng.uniform(0.028, 0.044), pressure="even", load=1.0)

# --- dust: a film and a few streaks, nothing more -----------------------
for a, b in [((0.500,0.055),(0.120,0.330)), ((0.470,0.300),(0.075,0.520)),
             ((0.290,0.040),(0.045,0.235)), ((0.545,0.400),(0.230,0.575))]:
    s.glaze([a, b], "dust_l", opacity=0.065)
for _ in range(7):
    x0 = rng.uniform(0.04, 0.50); y0 = rng.uniform(0.03, 0.50)
    ang = rng.uniform(-84, -52)
    ln = rng.uniform(0.06, 0.17)
    s.stroke([(x0, y0), (x0 + math.cos(math.radians(ang))*ln*0.5,
                         y0 - math.sin(math.radians(ang))*ln*0.5 + rng.uniform(-0.006,0.006)),
              (x0 + math.cos(math.radians(ang))*ln, y0 - math.sin(math.radians(ang))*ln)],
             "liner", "dust_l", size=rng.uniform(0.004, 0.008),
             pressure=[0.15, 0.6, 0.25, 0.5, 0.1], load=1.0)
print(s.stroke_count)
print(s.look())
