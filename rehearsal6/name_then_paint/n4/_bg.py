def rebuild_background():
    s.dry()
    s.block_in(GLASS, "flat", "glass", direction=(98, 14), density=1.0,
               size=0.15, pressure="even", load=1.0, load_falloff=0.0)
    s.block_in(WALL, "flat", "wall", direction=(104, 20), density=1.0,
               size=0.135, pressure="even", load=1.0, load_falloff=0.0)
    hot = polygon([(0.020,0.0),(0.566,0.0),(0.556,0.230),(0.290,0.200),(0.028,0.275)])
    s.block_in(hot.inset(0.028), "flat", "glass_hot", direction=(8, 96), density=1.0,
               size=0.055, pressure="even", load=1.0)
    s.smudge([(0.035,0.272),(0.180,0.246)], size=0.040)
    s.smudge([(0.160,0.243),(0.330,0.212)], size=0.036)
    s.smudge([(0.310,0.208),(0.470,0.222)], size=0.042)
    s.smudge([(0.450,0.226),(0.560,0.238)], size=0.034)
    corner = polygon([(0.860,0.0),(1.0,0.0),(1.0,0.320),(0.905,0.240)])
    s.block_in(corner.inset(0.026), "flat", "wall_dk", direction=(118, 32),
               density=1.0, size=0.050, pressure="even", load=1.0)
    s.smudge([(0.872,0.030),(0.930,0.150)], size=0.044)
    s.smudge([(0.918,0.140),(0.985,0.270)], size=0.044)
    s.dry()
    s.stroke([(0.292,-0.02),(0.286,0.615)], "flat", "bar", size=0.026,
             pressure="even", load=1.0)
    s.stroke([(0.018,0.298),(0.566,0.281)], "flat", "bar", size=0.022,
             pressure="even", load=1.0)
    s.stroke([(0.300,0.02),(0.295,0.60)], "liner", "bar_lit", size=0.006,
             pressure=[0.3,1.0,0.7,0.2], load=1.0)
    s.stroke([(0.030,0.290),(0.560,0.273)], "liner", "bar_lit", size=0.005,
             pressure=[0.2,0.9,0.5,0.9,0.3], load=1.0)
    s.block_in(JAMB, "flat", "bar", direction=(90,), density=1.0, size=0.030,
               pressure="even", load=1.0)
    s.stroke([(0.556,0.0),(0.549,0.618)], "liner", "bar_lit", size=0.007,
             pressure=[0.9,0.5,1.0,0.6], load=1.0)
    s.stroke([(0.604,0.02),(0.598,0.628)], "liner", "wall_dk", size=0.005,
             pressure=[0.4,1.0,0.6], load=1.0)
    s.dry()

def rebuild_sill():
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
    for a, b, sz, pr in [
        ((0.030,0.7527),(0.185,0.7590),0.004,[0.15,0.6,0.25]),
        ((0.240,0.7612),(0.395,0.7675),0.004,[0.3,0.75,0.2,0.5]),
        ((0.700,0.7799),(0.860,0.7864),0.005,[0.35,0.9,0.45]),
        ((0.895,0.7878),(0.990,0.7916),0.004,[0.5,0.7,0.2])]:
        s.stroke([a, b], "liner", "arris", size=sz, pressure=pr, load=1.0)
    s.dry()
