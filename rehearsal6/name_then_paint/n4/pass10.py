exec(open("_pal.py").read())
exec(open("_geom.py").read())
exec(open("_plant.py").read())
rng = random.Random(17)
s.dry()

# --- the body of the bush: a dark mass, well inside its final silhouette ----
BODY_M = hull([(0.470,0.470),(0.500,0.270),(0.610,0.190),(0.760,0.215),
               (0.830,0.330),(0.775,0.455),(0.630,0.500)])
s.block_in(BODY_M.inset(0.026), "round_hard", "leaf_dk", direction="axis",
           density=1.0, size=0.048, pressure="even", load=1.0)
s.block_in(BODY_M.inset(0.055), "round_hard", "leaf_dk", direction=(112,),
           density=0.9, size=0.038, pressure="even", load=1.0)

# --- the silhouette is built out of sprigs, not drawn -----------------------
ORIGINS = [(0.560,0.500),(0.596,0.492),(0.626,0.486),(0.660,0.490),(0.694,0.498),
           (0.580,0.430),(0.672,0.428),(0.626,0.400),(0.540,0.462),(0.712,0.462)]
SPEC = [ (168, 0.255), (159, 0.300), (150, 0.215), (176, 0.180), (143, 0.265),
         (134, 0.320), (126, 0.245), (117, 0.330), (108, 0.295), ( 99, 0.350),
         ( 92, 0.270), ( 84, 0.335), ( 76, 0.300), ( 67, 0.355), ( 59, 0.290),
         ( 51, 0.330), ( 43, 0.265), ( 34, 0.310), ( 26, 0.250), ( 17, 0.285),
         (  9, 0.225), (  1, 0.245), ( -7, 0.190), (188, 0.155), (196, 0.130),
         (204, 0.115), (154, 0.135), (122, 0.165), ( 70, 0.180), ( 30, 0.160),
         (140, 0.190), ( 88, 0.205), ( 46, 0.215), (  6, 0.150), (170, 0.115)]
for i, (ang, ln) in enumerate(SPEC):
    o = ORIGINS[i % len(ORIGINS)]
    ln *= rng.uniform(0.85, 1.12)
    path = stem(ang + rng.uniform(-6, 6), ln, origin=o,
                bow=rng.uniform(-0.30, 0.30), rng=rng)
    s.stroke(path, "bristle", "leaf_dk", size=rng.uniform(0.013, 0.026),
             pressure=rng.choice(["taper", "lift_off", [1.0, 0.9, 0.25]]),
             load=rng.uniform(0.7, 1.0))
print(s.stroke_count)
print(s.look())
