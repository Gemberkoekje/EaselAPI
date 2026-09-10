exec(open("_pal.py").read())
exec(open("_geom.py").read())
exec(open("_pot.py").read())
_t2 = p.mix(p.mix("burnt_sienna", "cadmium_red", 0.18), "yellow_ochre", 0.22)
p["pot_mid"]  = at(p.desaturate(_t2, 0.22), 0.395)
p["pot_lit"]  = at(p.desaturate(p.mix(_t2, "cadmium_yellow", 0.12), 0.20), 0.555)
p["pot_hi"]   = at(p.desaturate(p.mix(_t2, "cadmium_yellow", 0.22), 0.28), 0.660)
p["pot_shad"] = at(p.desaturate(p.mix(_t2, "ultramarine", 0.30), 0.22), 0.250)
p["pot_refl"] = at(p.desaturate(p.mix(_t2, "cerulean", 0.35), 0.30), 0.335)
p["pot_rim"]  = at(p.desaturate(p.mix(_t2, "cadmium_yellow", 0.25), 0.25), 0.640)
p["pot_dark"] = at(p.mix(_t2, "ultramarine", 0.50), 0.170)
p["contact"]  = at(p.desaturate(p.mix(_warmgrey, "ultramarine", 0.30), 0.20), 0.290)
for n in ("pot_dark","pot_shad","pot_refl","pot_mid","pot_lit","pot_rim","pot_hi"):
    print(f"{n:9s} {p.hex(p[n])} {p.value_of(p[n]):.2f}")
s.dry()

# --- clear the old pot's spill, and lay the contact shadow on the sill ------
s.block_in(polygon([(0.492,0.462),(0.516,0.462),(0.516,0.552),(0.492,0.552)]),
           "flat", "glass", direction=(92,), density=1.0, size=0.016,
           pressure="even", load=1.0, overhang=0)
s.block_in(polygon([(0.732,0.462),(0.752,0.462),(0.752,0.552),(0.732,0.552)]),
           "flat", "wall", direction=(92,), density=1.0, size=0.014,
           pressure="even", load=1.0, overhang=0)
s.block_in(polygon([(0.500,0.744),(0.760,0.750),(0.760,0.784),(0.500,0.778)]),
           "flat", "sill_hot", direction=(3,), density=1.0, size=0.020,
           pressure="even", load=1.0, overhang=0)
s.dry()
s.block_in(ellipse((0.606, 0.756), 0.098, 0.019).inset(0.006), "round_hard", "contact",
           direction=(2,), density=1.0, size=0.012, pressure="even", load=1.0)
s.smudge([(0.520, 0.762), (0.430, 0.756)], size=0.026)
s.smudge([(0.560, 0.770), (0.470, 0.766)], size=0.022)
s.dry()

# --- the pot -----------------------------------------------------------------
s.block_in(SIL.inset(0.015), "flat", "pot_mid", direction=(94,), density=1.0,
           size=0.030, pressure="even", load=1.0)
s.block_in(band(0.34, 1.02).inset(0.010), "flat", "pot_lit", direction=(93,),
           density=1.0, size=0.020, pressure="even", load=1.0)
s.block_in(band(0.78, 1.02).inset(0.005), "flat", "pot_hi", direction=(92,),
           density=1.0, size=0.011, pressure="even", load=1.0)
s.block_in(band(-1.02, -0.28).inset(0.009), "flat", "pot_shad", direction=(97,),
           density=1.0, size=0.018, pressure="even", load=1.0)
s.block_in(band(-1.02, -0.80).inset(0.004), "flat", "pot_refl", direction=(96,),
           density=1.0, size=0.010, pressure="even", load=1.0)
for a, b, sz in [((0.5560,0.575),(0.5590,0.665),0.019),((0.5600,0.655),(0.5640,0.740),0.017),
                 ((0.6560,0.572),(0.6570,0.668),0.019),((0.6590,0.658),(0.6600,0.740),0.017),
                 ((0.7020,0.580),(0.7010,0.680),0.012)]:
    s.smudge([a, b], size=sz)

# --- arcs that run round the form, not down it ------------------------------
s.stroke(ring(0.5720, 0.011, -0.97, 0.97), "bristle", "pot_shad", size=0.013,
         pressure=[0.9, 1.0, 0.8, 0.45], load=0.95, note="collar's shadow")
s.stroke(ring(0.6250, 0.014, -0.92, 0.55), "bristle", "pot_mid", size=0.014,
         pressure="taper", load=0.7)
s.stroke(ring(0.6800, 0.017, 0.75, -0.88), "bristle", "pot_lit", size=0.012,
         pressure="lift_off", load=0.65)
s.stroke(ring(0.7300, 0.020, -0.86, 0.86), "bristle", "pot_shad", size=0.014,
         pressure=[0.5, 1.0, 0.9, 0.4], load=0.85)
s.stroke(ring(0.6480, 0.015, 0.30, 0.92), "bristle", "pot_hi", size=0.009,
         pressure="taper", load=0.6)

# --- the inside: far lip, the dark, what is in it, near lip -----------------
s.block_in(COLLAR.inset(0.008), "flat", "pot_rim", direction=(4,), density=1.0,
           size=0.016, pressure="even", load=1.0)
s.block_in(INSIDE.inset(0.005), "flat", "pot_dark", direction=(3,), density=1.0,
           size=0.011, pressure="even", load=1.0)
s.block_in(ellipse((CX, 0.4980), 0.082, 0.014).inset(0.003), "flat", "soil",
           direction=(2,), density=1.0, size=0.009, pressure="even", load=1.0)
for x, y, sz in [(0.556,0.4965),(0.590,0.4930),(0.628,0.4950),(0.664,0.4915),
                 (0.694,0.4975),(0.610,0.5005),(0.650,0.4890)]:
    s.dab(x, y, "round_hard", "leaf_dk", size=0.013, press=2)
s.block_in(NEARLIP.inset(0.006), "flat", "pot_lit", direction=(2,), density=1.0,
           size=0.013, pressure="even", load=1.0)
print(s.stroke_count)
print(s.look(region="E4:G7"))
