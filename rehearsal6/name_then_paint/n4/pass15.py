exec(open("_pal.py").read())
exec(open("_geom.py").read())
exec(open("_pot.py").read())
_t2 = p.mix(p.mix("burnt_sienna", "cadmium_red", 0.18), "yellow_ochre", 0.22)
p["pot_mid"]  = at(p.desaturate(_t2, 0.22), 0.395)
p["pot_lit"]  = at(p.desaturate(p.mix(_t2, "cadmium_yellow", 0.12), 0.20), 0.555)
p["pot_hi"]   = at(p.desaturate(p.mix(_t2, "cadmium_yellow", 0.22), 0.28), 0.660)
p["pot_shad"] = at(p.desaturate(p.mix(_t2, "ultramarine", 0.22), 0.14), 0.285)
p["pot_refl"] = at(p.desaturate(p.mix(_t2, "cerulean", 0.28), 0.22), 0.370)
p["pot_dark"] = at(p.mix(_t2, "ultramarine", 0.55), 0.165)
p["lip_lit"]  = at(p.desaturate(p.mix(_t2, "cadmium_yellow", 0.30), 0.22), 0.700)
p["lip_shad"] = at(p.desaturate(p.mix(_t2, "ultramarine", 0.25), 0.18), 0.330)
s.dry()

# warm the shadow side back into terracotta
s.block_in(band(-1.02, -0.30).inset(0.009), "flat", "pot_shad", direction=(97,),
           density=1.0, size=0.018, pressure="even", load=1.0)
s.block_in(band(-1.02, -0.82).inset(0.004), "flat", "pot_refl", direction=(96,),
           density=1.0, size=0.010, pressure="even", load=1.0)
s.smudge([(0.5570, 0.578), (0.5600, 0.680)], size=0.019)
s.smudge([(0.5610, 0.665), (0.5650, 0.742)], size=0.017)
s.stroke(ring(0.5720, 0.011, -0.97, 0.20), "bristle", "pot_shad", size=0.012,
         pressure=[0.9, 1.0, 0.6], load=0.95)
s.stroke(ring(0.7300, 0.020, -0.86, 0.10), "bristle", "pot_shad", size=0.013,
         pressure=[0.5, 1.0, 0.7], load=0.85)
s.dry()

# --- the collar, modelled with marks rather than bands ---------------------
def cstroke(x):
    u = max(-0.999, min(0.999, (x - CX) / 0.115))
    k = (1.0 - u * u) ** 0.5
    return [(x, 0.5075 + 0.024 * k), (x - 0.001, 0.546 + 0.0325 * k)]
for x in [0.5165, 0.5290, 0.5420, 0.5550, 0.5680]:
    s.stroke(cstroke(x), "flat", "lip_shad", size=0.0135, pressure="even", load=1.0)
for x in [0.5805, 0.5930, 0.6055]:
    s.stroke(cstroke(x), "flat", "pot_mid", size=0.0135, pressure="even", load=1.0)
for x in [0.6180, 0.6305, 0.6430, 0.6555]:
    s.stroke(cstroke(x), "flat", "pot_lit", size=0.0135, pressure="even", load=1.0)
for x in [0.6680, 0.6805, 0.6930, 0.7040, 0.7130]:
    s.stroke(cstroke(x), "flat", "pot_hi", size=0.0130, pressure="even", load=1.0)
for a, b in [((0.5720,0.520),(0.5745,0.566)), ((0.6120,0.512),(0.6140,0.572)),
             ((0.6620,0.514),(0.6640,0.570)), ((0.7000,0.522),(0.7010,0.560))]:
    s.smudge([a, b], size=0.013)

# --- far lip, the dark inside, what is in it, near lip ---------------------
s.stroke(arc(CX, 0.4985, 0.1010, 0.0255, 182, 358, 22), "flat", "lip_lit",
         size=0.010, pressure="even", load=1.0, note="far lip, top surface")
s.block_in(ellipse((CX, 0.5015), 0.0925, 0.0215).inset(0.004), "flat", "pot_dark",
           direction=(3,), density=1.0, size=0.009, pressure="even", load=1.0)
s.block_in(ellipse((CX, 0.4975), 0.0800, 0.0130).inset(0.003), "flat", "soil",
           direction=(2,), density=1.0, size=0.007, pressure="even", load=1.0)
for x, y in [(0.556,0.4955),(0.586,0.4920),(0.618,0.4945),(0.650,0.4905),
             (0.680,0.4960),(0.604,0.4995),(0.666,0.4880),(0.634,0.5010)]:
    s.dab(x, y, "round_hard", "leaf_dk", size=0.012, press=2)
s.stroke(arc(CX, 0.5085, 0.1055, 0.0270, 168, 12, 22), "flat", "pot_lit",
         size=0.009, pressure="even", load=1.0, note="near lip")
s.stroke(arc(CX, 0.5100, 0.0700, 0.0245, 150, 42, 14), "liner", "lip_lit",
         size=0.005, pressure=[0.3, 1.0, 0.7, 0.9, 0.25], load=1.0)

# --- give the right-hand silhouette a real edge: paint the wall up to it ---
s.block_in(polygon([(0.7415,0.462),(0.7900,0.462),(0.7900,0.618),(0.7415,0.618)]),
           "flat", "wall", direction=(91,), density=1.0, size=0.012,
           pressure="even", load=1.0, overhang=0)
print(s.stroke_count)
print(s.look(region="E4:G7"))
