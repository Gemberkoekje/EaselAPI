exec(open("_pal.py").read())
exec(open("_geom.py").read())
import random, math
rng = random.Random(313)
p["dust_l"] = at(p.desaturate(p.mix(_neutral, "cadmium_yellow", 0.22), 0.35), 0.868)
p["dust_d"] = at(p.desaturate(p.mix(_neutral, "yellow_ochre", 0.20), 0.45), 0.772)
p["outside"]= at(p.desaturate(p.mix(_neutral, "viridian", 0.25), 0.62), 0.742)
p["sill_ck"]= at(p.desaturate(p.mix(_warmgrey, "ultramarine", 0.25), 0.25), 0.405)
p["greenref"]= at(p.desaturate(p.mix(_sage, "yellow_ochre", 0.30), 0.55), 0.585)
s.dry()

# --- the wall's top-right corner, ghosts and all --------------------------
s.block_in(polygon([(0.820,0.0),(1.0,0.0),(1.0,0.230),(0.828,0.205)]),
           "flat", "wall", direction=(106, 22), density=1.0, size=0.048,
           pressure="even", load=1.0, overhang=0)
s.block_in(polygon([(0.884,0.0),(1.0,0.0),(1.0,0.196),(0.918,0.150)]).inset(0.020),
           "flat", "wall_dk", direction=(122, 36), density=1.0, size=0.040,
           pressure="even", load=1.0)
for i in range(7):
    x0 = 0.845 + rng.uniform(-0.02, 0.05); y0 = rng.uniform(0.01, 0.20)
    s.stroke([(x0, y0), (x0 + rng.uniform(0.045, 0.11), y0 + rng.uniform(0.02, 0.09))],
             "flat", "wall_dk" if rng.random() < 0.5 else "wall",
             size=rng.uniform(0.020, 0.042), pressure="even", load=rng.uniform(0.7, 1.0))

# --- the left of the sill: graded, and marked with things, not stripes ----
for i in range(9):
    t = i / 8.0
    y = 0.6180 + 0.1300 * t + rng.uniform(-0.006, 0.006)
    v = 0.470 + 0.075 * t
    col = at(p.desaturate(p.mix(_warmgrey, "yellow_ochre", 0.36), 0.58), v)
    s.stroke([(0.0 - 0.01, y + rng.uniform(-0.004, 0.004)),
              (0.115, y + rng.uniform(-0.003, 0.005)),
              (0.235 + rng.uniform(-0.02, 0.02), y + 0.008)],
             "flat", col, size=rng.uniform(0.020, 0.030), pressure="even", load=1.0)
for x0, y0, x1, y1, sz, col in [
        (0.048,0.664,0.112,0.652,0.006,"sill_ck"), (0.112,0.652,0.146,0.668,0.005,"sill_ck"),
        (0.030,0.722,0.084,0.732,0.005,"sill_ck"), (0.168,0.640,0.196,0.634,0.004,"sill_ck"),
        (0.062,0.700,0.130,0.694,0.006,"sill_hot"), (0.140,0.716,0.192,0.722,0.005,"sill_hot")]:
    s.stroke([(x0,y0),(x1,y1)], "liner", col, size=sz,
             pressure=[0.2, 0.9, 0.4, 0.7, 0.15], load=1.0)
for _ in range(7):
    s.dab(rng.uniform(0.02, 0.24), rng.uniform(0.630, 0.744), "round_hard",
          rng.choice(["sill_ck", "sill_hot"]), size=rng.uniform(0.004, 0.008), press=1)

# --- a green bounce off the plant onto the sill --------------------------
for x0, y0, x1, y1, sz in [(0.300,0.660,0.470,0.668,0.020),(0.360,0.646,0.520,0.652,0.016),
                           (0.760,0.664,0.880,0.672,0.017)]:
    s.stroke([(x0,y0),(x1,y1)], "bristle", "greenref", size=sz,
             pressure="taper", load=0.35)

# --- dust on the glass ---------------------------------------------------
for i in range(15):
    x0 = rng.uniform(0.03, 0.52); y0 = rng.uniform(0.02, 0.55)
    ang = rng.choice([-72, -66, -78, -58, -84, 12, -40])
    ln = rng.uniform(0.05, 0.22)
    x1 = x0 + math.cos(math.radians(ang)) * ln
    y1 = y0 - math.sin(math.radians(ang)) * ln
    s.stroke([(x0, y0), ((x0+x1)/2 + rng.uniform(-0.012,0.012), (y0+y1)/2), (x1, y1)],
             "bristle", "dust_l" if rng.random() < 0.55 else "dust_d",
             size=rng.uniform(0.012, 0.040), pressure="taper", load=rng.uniform(0.28, 0.50))
s.stroke([(0.055,0.470),(0.180,0.462),(0.268,0.478)], "bristle", "outside",
         size=0.055, pressure="taper", load=0.40)
s.stroke([(0.040,0.520),(0.150,0.512)], "bristle", "outside",
         size=0.042, pressure="taper", load=0.34)
print(s.stroke_count)
print(s.look())
