# What stands inside. Muted, because this is foliage seen through a fogged pane --
# the real green is saved for the runnels, where the water has cleared the film.
# Every shape is built in metres and projected, so the foliage converges with the
# building it stands in.
from easel import polygon

p["leaflit"] = p.at_value(p.desaturate(p.mix(p.mix("viridian", "yellow_ochre", 0.40),
                                             "burnt_umber", 0.16), 0.52), 0.42)
p["leafmid"] = p.at_value(p.desaturate(p.mix(p.mix("viridian", "yellow_ochre", 0.34),
                                             "burnt_umber", 0.20), 0.50), 0.33)
p["leafdk"]  = p.at_value(p.desaturate(p.mix(p.mix("viridian", "yellow_ochre", 0.28),
                                             "burnt_umber", 0.26), 0.42), 0.26)
# kept back for the runnels and the pressed leaves: the only real green in the picture
p["leafclear"] = p.at_value(p.mix(p.mix("viridian", "yellow_ochre", 0.30),
                                  "burnt_umber", 0.10), 0.28)

def upright(d0, d1, h_lo, h_hi, jag):
    top = [P(WALL, h_hi + j, d0 + (d1 - d0) * i / (len(jag) - 1.0))
           for i, j in enumerate(jag)]
    return polygon(top + [P(WALL, h_lo, d1), P(WALL, h_lo, d0)])

BANK_D = [1.25, 1.70, 2.20, 2.90, 3.80, 5.00, 7.00, 9.50]
BANK_H = [1.05, 1.27, 1.02, 1.24, 1.06, 1.20, 1.09, 1.16]
bank = polygon([P(WALL, h, d) for d, h in zip(BANK_D, BANK_H)]      # top, near to far
                + [P(WALL, SILL, 9.50), P(WALL, SILL, 3.00),        # then the sill back
                   P(WALL, SILL, 2.20), (1.06, 1.06)])
tall = upright(1.56, 2.02, 1.05, 1.78, [0.00, 0.14, -0.10, 0.17, -0.04, 0.09])
mid  = upright(3.30, 3.95, 1.05, 1.62, [0.00, 0.11, -0.07, 0.09, 0.00])
low  = upright(2.30, 2.62, 1.02, 1.44, [0.00, 0.09, -0.05, 0.07])
hang = polygon([P(WALL, 2.06, 2.42), P(WALL, 2.06, 3.02), P(WALL, 1.63, 2.96),
                P(WALL, 1.44, 2.74), P(WALL, 1.58, 2.52)])

# one direction each, and a different one each: foliage is stringy, so a comb is
# the thing here -- but four parallel combs would be hatching, so no two agree
s.block_in(bank, "bristle", "leafmid", direction=58, density=0.85,
           size=0.065, load=0.85, note="glass")
s.block_in(mid,  "bristle", "leafmid", direction=80, density=0.85,
           size=0.030, load=0.8, note="glass")
s.block_in(hang, "bristle", "leafdk",  direction=88, density=0.85,
           size=0.030, load=0.8, note="glass")
s.block_in(low,  "bristle", "leaflit", direction=66, density=0.85,
           size=0.030, load=0.8, note="glass")
s.block_in(tall, "bristle", "leaflit", direction=72, density=0.85,
           size=0.046, load=0.9, note="glass")

# a few leaves crossing the combs, so the masses are not four grains
s.stroke([(0.905, 0.300), (0.948, 0.355), (0.962, 0.430)], "bristle", "leafdk",
         size=0.030, load=0.6, opacity=0.8, note="glass")
s.stroke([(0.828, 0.470), (0.886, 0.508), (0.948, 0.502)], "bristle", "leaflit",
         size=0.026, load=0.55, opacity=0.75, note="glass")
s.stroke([(0.700, 0.660), (0.780, 0.690), (0.856, 0.742)], "bristle", "leafdk",
         size=0.034, load=0.6, opacity=0.7, pressure="swell", note="glass")
s.stroke([(0.520, 0.616), (0.585, 0.634), (0.652, 0.618)], "bristle", "leaflit",
         size=0.022, load=0.5, opacity=0.7, note="glass")
s.stroke([(0.612, 0.352), (0.636, 0.420), (0.622, 0.486)], "round_hard", "leafdk",
         size=0.018, load=0.5, opacity=0.65, pressure="lift_off", note="glass")
