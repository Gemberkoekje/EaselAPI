exec(open("_pal.py").read())
exec(open("_geom.py").read())
exec(open("_pot.py").read())
p["pot_lit"]  = at(p.desaturate(_terra, 0.28), 0.560)
p["pot_mid"]  = at(p.desaturate(_terra, 0.32), 0.395)
p["pot_shad"] = at(p.desaturate(p.mix(_terra, "ultramarine", 0.32), 0.25), 0.245)
p["pot_refl"] = at(p.desaturate(p.mix(_terra, "cerulean", 0.30), 0.35), 0.330)
p["pot_rim"]  = at(p.desaturate(p.mix(_terra, "cadmium_yellow", 0.28), 0.30), 0.650)
p["pot_dark"] = at(p.mix(_terra, "ultramarine", 0.50), 0.175)
s.dry()

# --- the body first: the rim sits on top of it -----------------------------
s.block_in(BODY.inset(0.014), "flat", "pot_mid", direction=(96,), density=1.0,
           size=0.028, pressure="even", load=1.0)
s.block_in(band(0.646, 0.730).inset(0.008), "flat", "pot_lit", direction=(94,),
           density=1.0, size=0.017, pressure="even", load=1.0)
s.block_in(band(0.514, 0.578).inset(0.008), "flat", "pot_shad", direction=(98,),
           density=1.0, size=0.017, pressure="even", load=1.0)
s.block_in(band(0.512, 0.532).inset(0.004), "flat", "pot_refl", direction=(97,),
           density=1.0, size=0.010, pressure="even", load=1.0)
for a, b, sz in [((0.5790,0.560),(0.5810,0.660),0.020),((0.5820,0.650),(0.5860,0.735),0.018),
                 ((0.6460,0.560),(0.6480,0.665),0.020),((0.6490,0.655),(0.6520,0.735),0.018),
                 ((0.5325,0.565),(0.5345,0.670),0.013)]:
    s.smudge([a, b], size=sz)

# --- anything with an inside: far lip, inside, what is in it, near lip -----
s.block_in(COLLAR.inset(0.009), "flat", "pot_rim", direction=(4,), density=1.0,
           size=0.017, pressure="even", load=1.0)                    # the far lip
s.block_in(INSIDE.inset(0.006), "round_hard", "pot_dark", direction=(6,),
           density=1.0, size=0.013, pressure="even", load=1.0)       # the inside
s.block_in(ellipse((0.624, 0.505), 0.082, 0.016).inset(0.004), "round_hard", "soil",
           direction=(3,), density=1.0, size=0.010, pressure="even", load=1.0)
for x, y, sz in [(0.560,0.503,0.011),(0.596,0.499,0.013),(0.640,0.501,0.012),
                 (0.676,0.505,0.010),(0.612,0.508,0.009),(0.658,0.497,0.009)]:
    s.dab(x, y, "round_hard", "leaf_dk", size=sz, press=2)           # foliage in it
s.block_in(NEARLIP.inset(0.007), "flat", "pot_lit", direction=(2,), density=1.0,
           size=0.014, pressure="even", load=1.0)                    # the near lip
print(s.stroke_count)
print(s.look(region="D4:H7"))
