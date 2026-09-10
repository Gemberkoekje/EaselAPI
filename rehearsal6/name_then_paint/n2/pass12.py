import random, math
p = s.palette; rnd = random.Random(101)
def leaf(x, y, w, col, tilt, ln=0.55, brush="round_hard", pr="even", ld=1.0):
    dx = math.cos(math.radians(tilt))*w*ln/2; dy = math.sin(math.radians(tilt))*w*ln/2
    s.stroke([(x-dx,y-dy),(x+dx,y+dy)], brush, col, size=w, pressure=pr, load=ld)

s.dry()
# --- cut the background back into the silhouette: gaps are what make foliage read ---
for x, y, w, col, tilt in [(0.4255,0.4720,0.040,"glow_c",-28),(0.4430,0.4180,0.032,"glow_c",44),
                           (0.4680,0.5620,0.028,"glow_c",-52),(0.4400,0.5180,0.026,"haze",18),
                           (0.8050,0.4520,0.044,"wall",62),(0.7620,0.3960,0.036,"wall",-34),
                           (0.6400,0.3140,0.040,"wall",22),(0.5620,0.3300,0.034,"wall",-60),
                           (0.7010,0.5560,0.032,"wall",40),(0.7580,0.5580,0.036,"wall",-16),
                           (0.6640,0.4620,0.019,"wall",70),(0.6060,0.4080,0.017,"wall",-40),
                           (0.5300,0.3760,0.020,"wall",8),(0.7860,0.5000,0.024,"wall",-70)]:
    leaf(x, y, w, col, tilt, ln=0.5)

# --- the leaves themselves: dark against the light, lit against the dark ---
leaves = [(0.700,0.396,0.052,"lf_mid",-24),(0.744,0.432,0.046,"lf_lit", 38),
          (0.716,0.472,0.050,"lf_mid", 66),(0.762,0.492,0.040,"lf_mid",-12),
          (0.688,0.444,0.056,"lf_sh",  14),(0.734,0.540,0.038,"lf_dk", -48),
          (0.784,0.468,0.034,"lf_sh", -66),(0.660,0.494,0.052,"lf_mid", 28),
          (0.640,0.434,0.048,"lf_lit",-40),(0.604,0.386,0.046,"lf_mid", 52),
          (0.586,0.430,0.052,"lf_sh", -18),(0.628,0.350,0.040,"lf_mid",  8),
          (0.576,0.346,0.036,"lf_sh",  74),(0.612,0.470,0.054,"lf_sh", -34),
          (0.650,0.532,0.042,"lf_dk",  22),(0.548,0.418,0.048,"lf_dk", -56),
          (0.512,0.452,0.054,"lf_dk",  30),(0.480,0.494,0.044,"lf_dk", -20),
          (0.456,0.544,0.040,"lf_dk",  60),(0.524,0.514,0.046,"lf_dk", -70),
          (0.500,0.558,0.036,"lf_dk",  16),(0.678,0.352,0.036,"lf_sh", -50),
          (0.752,0.408,0.032,"lf_mid", 44),(0.596,0.512,0.044,"lf_dk",  -8)]
for x, y, w, c, t in leaves:
    leaf(x, y, w, c, t, ln=rnd.uniform(0.45,0.75))
# two leaves with the light coming through them
leaf(0.5340,0.4640,0.032,"lf_hot",-36, ln=0.6)
leaf(0.4930,0.5220,0.028,"lf_lit", 24, ln=0.6)
leaf(0.5560,0.4880,0.024,"lf_mid",-62, ln=0.6)
# the dark between the leaves
for x, y, w, t in [(0.672,0.418,0.020,-30),(0.622,0.412,0.018,50),(0.706,0.510,0.022,10),
                   (0.562,0.396,0.017,-64),(0.744,0.462,0.016,36),(0.630,0.500,0.020,-14)]:
    leaf(x, y, w, "lf_dk", t, ln=0.7)
print("strokes:", s.stroke_count)
