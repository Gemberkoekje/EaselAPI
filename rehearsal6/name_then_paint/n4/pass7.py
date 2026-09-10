exec(open("_pal.py").read())
exec(open("_geom.py").read())
p["sill_lit"]  = at(p.desaturate(p.mix(_warmgrey, "yellow_ochre", 0.40), 0.55), 0.620)
p["sill_hot"]  = at(p.desaturate(p.mix(_warmgrey, "cadmium_yellow", 0.30), 0.42), 0.735)
p["sill_mid"]  = at(p.desaturate(p.mix(_warmgrey, "yellow_ochre", 0.35), 0.60), 0.500)
p["sill_shad"] = at(p.desaturate(p.mix(_warmgrey, "ultramarine", 0.28), 0.30), 0.440)
p["sill_face"] = at(p.desaturate(p.mix(_warmgrey, "ultramarine", 0.30), 0.35), 0.300)
p["under"]     = at(p.desaturate(p.mix("burnt_umber", "ultramarine", 0.22), 0.18), 0.175)
p["under_wm"]  = at(p.mix("burnt_umber", "burnt_sienna", 0.30), 0.230)
for n in ("sill_mid","sill_shad","sill_lit","sill_hot","sill_face","under","under_wm"):
    print(f"{n:10s} {p.hex(p[n])} {p.value_of(p[n]):.2f}")
s.dry()

s.block_in(SILL, "flat", "sill_lit", direction=(3, 169), density=0.95,
           size=0.048, pressure="even", load=1.0, load_falloff=0.25)
s.block_in(polygon([(0.40,0.626),(1.0,0.650),(1.0,0.768),(0.43,0.736)]).inset(0.018),
           "flat", "sill_hot", direction=(4, 172), density=0.9, size=0.038,
           pressure="even", load=1.0)
s.block_in(polygon([(0.0,0.610),(0.215,0.616),(0.195,0.754),(0.0,0.750)]).inset(0.016),
           "flat", "sill_mid", direction=(2, 174), density=0.9, size=0.036,
           pressure="even", load=1.0)
for a, b, sz in [((0.208,0.632),(0.216,0.700),0.040), ((0.214,0.688),(0.204,0.748),0.034),
                 ((0.418,0.640),(0.428,0.706),0.038), ((0.424,0.700),(0.414,0.744),0.032)]:
    s.smudge([a, b], size=sz)

s.block_in(FACE, "flat", "sill_face", direction=(3, 165), density=1.0,
           size=0.036, pressure="even", load=1.0, load_falloff=0.25)
s.block_in(UNDER, "flat", "under", direction=(4, 98), density=1.0,
           size=0.055, pressure="even", load=1.0, load_falloff=0.25)
s.stroke([(0.02, 0.905), (0.47, 0.918)], "flat", "under_wm", size=0.055,
         pressure="even", load=0.75)
s.stroke([(0.98, 0.960), (0.55, 0.948)], "flat", "under_wm", size=0.048,
         pressure="even", load=0.7)
print(s.stroke_count)
print(s.look())
