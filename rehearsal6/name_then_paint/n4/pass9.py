exec(open("_pal.py").read())
exec(open("_geom.py").read())
p["sill_lit"]  = at(p.desaturate(p.mix(_warmgrey, "yellow_ochre", 0.40), 0.55), 0.620)
p["sill_hot"]  = at(p.desaturate(p.mix(_warmgrey, "cadmium_yellow", 0.30), 0.42), 0.735)
p["sill_mid"]  = at(p.desaturate(p.mix(_warmgrey, "yellow_ochre", 0.35), 0.60), 0.500)
p["sill_shad"] = at(p.desaturate(p.mix(_warmgrey, "ultramarine", 0.22), 0.30), 0.450)
p["arris"]     = at(p.desaturate(p.mix(_warmgrey, "cadmium_yellow", 0.32), 0.38), 0.715)
s.dry()

s.block_in(SILL, "flat", "sill_lit", direction=(3, 169), density=0.95,
           size=0.048, pressure="even", load=1.0, load_falloff=0.25)
s.block_in(polygon([(0.40,0.626),(1.0,0.650),(1.0,0.768),(0.43,0.736)]).inset(0.018),
           "flat", "sill_hot", direction=(4, 172), density=0.9, size=0.038,
           pressure="even", load=1.0)
s.block_in(polygon([(0.0,0.612),(0.215,0.618),(0.195,0.754),(0.0,0.750)]).inset(0.016),
           "flat", "sill_mid", direction=(2, 174), density=0.9, size=0.036,
           pressure="even", load=1.0)
for a, b, sz in [((0.208,0.634),(0.216,0.700),0.038), ((0.214,0.690),(0.203,0.748),0.032),
                 ((0.418,0.642),(0.428,0.706),0.036), ((0.424,0.700),(0.414,0.744),0.030)]:
    s.smudge([a, b], size=sz)
s.dry()

# --- the cast shadow: lower, shallower, and lost at its far end ------------
CAST = polygon([(0.600,0.700),(0.652,0.738),(0.578,0.758),(0.330,0.750),
                (0.190,0.722),(0.268,0.696),(0.440,0.690)])
s.block_in(CAST.inset(0.014), "round_hard", "sill_shad", direction="axis",
           density=1.0, size=0.028, pressure="even", load=1.0)
for x, y, sz, n in [(0.512,0.690,0.017,2),(0.462,0.684,0.012,1),(0.408,0.694,0.015,2),
                    (0.346,0.686,0.010,1),(0.308,0.698,0.013,1),(0.256,0.708,0.010,1)]:
    s.dab(x, y, "round_hard", "sill_shad", size=sz, press=n)
for a, b, sz in [((0.560,0.744),(0.400,0.742),0.030), ((0.380,0.746),(0.250,0.730),0.028),
                 ((0.250,0.716),(0.170,0.722),0.030), ((0.430,0.694),(0.300,0.698),0.026)]:
    s.smudge([a, b], size=sz)

# --- the arris, broken, brightest where the light rakes it -----------------
for a, b, sz, pr in [
    ((0.030,0.7527),(0.185,0.7590),0.004,[0.15,0.6,0.25]),
    ((0.240,0.7612),(0.395,0.7675),0.004,[0.3,0.75,0.2,0.5]),
    ((0.700,0.7799),(0.860,0.7864),0.005,[0.35,0.9,0.45]),
    ((0.895,0.7878),(0.990,0.7916),0.004,[0.5,0.7,0.2])]:
    s.stroke([a, b], "liner", "arris", size=sz, pressure=pr, load=1.0)
print(s.stroke_count)
print(s.look())
