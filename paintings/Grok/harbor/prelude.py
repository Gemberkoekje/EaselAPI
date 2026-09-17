# Quiet harbour at dusk.
# Why this subject: dusk flattens the water into one colour, so the painting
# is mostly edges and light, not detail.

p = s.palette

p["dusk_high"] = p.at_value(p.mix("ultramarine", "alizarin", 0.32), 0.28)
p["dusk_mid"] = p.at_value(p.mix("cerulean", "alizarin", 0.38), 0.38)
p["glow"] = p.at_value(p.mix("yellow_ochre", "cadmium_red", 0.22), 0.70)
p["glow_band"] = p.at_value(p.mix("yellow_ochre", "cadmium_red", 0.18), 0.55)
p["glow_core"] = p.at_value(p.mix("cadmium_yellow", "cadmium_red", 0.16), 0.78)
p["water"] = p.at_value(p.mix("cerulean", "burnt_umber", 0.42), 0.40)
p["sheet"] = p.at_value(p.mix("cerulean", "yellow_ochre", 0.22), 0.48)
p["water_near"] = p.at_value(p.mix("cerulean", "burnt_umber", 0.58), 0.34)
p["ink"] = p.mix("ultramarine", "burnt_umber", 0.45)
p["pier"] = p.at_value(p.mix("burnt_umber", "ultramarine", 0.32), 0.20)
p["land"] = p.at_value(p.mix("burnt_umber", "ultramarine", 0.55), 0.22)
p["warm_dark"] = p.at_value(p.mix("burnt_umber", "alizarin", 0.28), 0.18)
p["mast"] = p.at_value(p.mix("ultramarine", "burnt_umber", 0.40), 0.17)

VX, VY, F, E = 0.28, 0.38, 0.90, 1.80


def P(xm, hm, dm):
    return (VX + xm * F / dm, VY - (hm - E) * F * s.aspect / dm)


s.mark("glow", *P(0.0, 0.0, 80.0))
s.mark("vp", VX, VY)
s.mark("pier_near_l", *P(2.15, 0.42, 4.3))
s.mark("pier_near_r", *P(3.45, 0.42, 4.3))
s.mark("pier_far_l", *P(2.15, 0.42, 17.0))
s.mark("pier_far_r", *P(3.45, 0.42, 17.0))
s.mark("dinghy_bow", *P(1.35, 0.22, 6.5))
s.mark("mid_mast_top", *P(0.35, 4.4, 11.5))
s.mark("mid_mast_foot", *P(0.35, 0.0, 11.5))
s.mark("far_mast_top", *P(-4.2, 4.2, 24.0))
s.mark("far_mast_foot", *P(-4.2, 0.0, 24.0))


def sky_whole():
    return polygon([
        (-0.08, -0.08), (1.08, -0.08), (1.08, 0.42),
        (0.84, 0.36), (0.70, 0.40), (0.28, 0.385), (-0.08, 0.40),
    ])


def sky_upper():
    return polygon([
        (-0.08, -0.08), (1.08, -0.08), (1.08, 0.26),
        (0.62, 0.22), (0.28, 0.24), (-0.08, 0.20),
    ])


def sky_low():
    return polygon([
        (-0.08, 0.16), (0.28, 0.20), (0.62, 0.18), (1.08, 0.22),
        (1.08, 0.42), (0.70, 0.40), (0.28, 0.385), (-0.08, 0.40),
    ])


def water_far():
    return polygon([
        (-0.08, 0.36), (0.28, 0.375), (0.70, 0.39), (1.08, 0.41),
        (1.08, 0.78), (-0.08, 0.80),
    ])


def water_near_shape():
    return polygon([
        (-0.08, 0.72), (0.55, 0.76), (1.08, 0.70),
        (1.08, 1.08), (-0.08, 1.08),
    ])


def sheet_shape():
    return polygon([
        (0.02, 0.385), (0.22, 0.375), (0.38, 0.39),
        (0.42, 0.62), (0.28, 0.78), (0.08, 0.64),
    ])


def headland():
    return polygon([
        (0.58, 0.392), (0.67, 0.372), (0.74, 0.380),
        (0.81, 0.350), (0.88, 0.358), (0.95, 0.318),
        (1.02, 0.295), (1.08, 0.268),
        (1.08, 0.462), (0.97, 0.440), (0.90, 0.452),
        (0.83, 0.428), (0.74, 0.438), (0.66, 0.418),
        (0.59, 0.408),
    ])


def pier_deck():
    return polygon([
        P(2.15, 0.42, 4.3), P(3.45, 0.42, 4.3),
        P(3.45, 0.42, 17.0), P(2.15, 0.42, 17.0),
    ])


def pier_face():
    return polygon([
        P(2.15, 0.42, 4.3), P(2.15, 0.00, 4.3),
        P(2.15, 0.00, 17.0), P(2.15, 0.42, 17.0),
    ])


def far_boat():
    return polygon([
        P(-5.4, 0.04, 23.0), P(-3.0, 0.04, 24.8),
        P(-3.2, 0.55, 24.6), P(-4.2, 0.62, 23.6),
        P(-5.3, 0.28, 23.0),
    ])


def mid_boat():
    return polygon([
        P(-0.75, 0.04, 10.1), P(1.95, 0.04, 12.9),
        P(1.70, 0.48, 12.7), P(0.70, 0.78, 11.6),
        P(-0.15, 0.62, 10.7), P(-0.70, 0.22, 10.1),
    ])


def dinghy_hull():
    return polygon([
        P(0.70, 0.12, 5.15), P(1.70, 0.12, 5.20),
        P(1.45, 0.22, 6.55), P(1.05, 0.22, 6.50),
    ])


def dinghy_inside():
    return polygon([
        P(0.88, 0.10, 5.32), P(1.52, 0.10, 5.36),
        P(1.35, 0.10, 6.25), P(1.12, 0.10, 6.20),
    ])


def dinghy_far_rim():
    return polygon([
        P(0.95, 0.36, 5.20), P(1.85, 0.36, 5.22),
        P(1.48, 0.36, 6.70), P(1.22, 0.36, 6.65),
    ])


def dinghy_near_rim():
    return polygon([
        P(0.88, 0.40, 5.08), P(1.95, 0.40, 5.12),
        P(1.78, 0.26, 5.30), P(1.02, 0.26, 5.26),
    ])


def sky_mass():
    s.scumble(sky_upper(), "dusk_high", "dusk_mid", 7, direction=6,
              load=1.0, load_falloff=0.0, opacity=0.95)


def sky_low_mass():
    s.scumble(sky_low(), "dusk_mid", "glow_band", 8, direction=4,
              load=1.0, load_falloff=0.0, opacity=0.95)


def water_mass():
    s.scumble(water_far(), "water", "water", 8, direction=3,
              load=1.0, load_falloff=0.0, opacity=0.95)


def water_near_mid():
    return polygon([
        (-0.08, 0.68), (1.08, 0.66), (1.08, 0.86), (-0.08, 0.88),
    ])


def water_near_foot():
    return polygon([
        (-0.08, 0.82), (1.08, 0.80), (1.08, 1.08), (-0.08, 1.08),
    ])


def water_near_mass():
    s.scumble(water_near_mid(), "water", "water_near", 6, direction=5,
              load=1.0, load_falloff=0.0, opacity=0.95)
    s.scumble(water_near_foot(), "water_near", "water_near", 5, direction=7,
              load=1.0, load_falloff=0.0, opacity=0.95)


def sheet_mass():
    s.scumble(sheet_shape(), "water", "sheet", 6, direction=8,
              load=1.0, load_falloff=0.0, opacity=0.85)


def land_mass():
    s.block_in(headland(), "flat", "land", size=0.016, density=1.0,
               solid=True, direction=((1.08, 0.27), (0.58, 0.39)),
               edge="hard", opacity=1.0, pressure="even")


def pier_fascia():
    return polygon([
        P(2.15, 0.42, 4.3), P(3.45, 0.42, 4.3),
        P(3.45, 0.00, 4.3), P(2.15, 0.00, 4.3),
    ])


def pier_mass():
    along = (P(2.80, 0.42, 4.3), P(2.80, 0.42, 17.0))
    s.block_in(pier_deck(), "flat", "pier", size=0.016, density=1.0,
               solid=True, direction=along, edge="hard", opacity=1.0,
               pressure="even")
    s.block_in(pier_fascia(), "flat", "ink", size=0.012, density=1.0,
               solid=True, direction="axis", edge="hard", opacity=1.0,
               pressure="even")


def boats_mass():
    s.block_in(far_boat(), "flat", "ink", size=0.012, density=1.0,
               solid=True, direction="axis", edge="clean", note="subject")
    s.block_in(mid_boat(), "flat", "ink", size=0.018, density=1.0,
               solid=True, direction="axis", edge="clean", note="subject")
