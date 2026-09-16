# Quiet lighthouse at dusk.
# Why this subject: the last warm light around a small lamp is enough to hold
# a whole dark coast together.

p = s.palette

# Values planned before the first mark: dark coast/tower 0.15-0.20,
# sea 0.22-0.30, upper sky 0.20-0.32, horizon gold 0.55-0.84.
p["sky_high"] = p.at_value(p.mix("ultramarine", "alizarin", 0.28), 0.20)
p["sky_mid"] = p.at_value(p.mix("cerulean", "alizarin", 0.32), 0.32)
p["horizon_gold"] = p.at_value(p.mix("yellow_ochre", "cadmium_red", 0.24), 0.58)
p["gold_core"] = p.at_value(p.mix("cadmium_yellow", "titanium_white", 0.72), 0.84)
p["sea"] = p.at_value(p.mix("cerulean", "ultramarine", 0.45), 0.30)
p["sea_deep"] = p.at_value(p.mix("ultramarine", "burnt_umber", 0.42), 0.21)
p["rock"] = p.at_value(p.mix("ultramarine", "burnt_umber", 0.56), 0.16)
p["rock_face"] = p.at_value(p.mix("burnt_umber", "cerulean", 0.28), 0.24)
p["rock_warm"] = p.at_value(p.mix("burnt_sienna", "yellow_ochre", 0.30), 0.30)
p["tower_dark"] = p.at_value(p.mix("ultramarine", "burnt_umber", 0.50), 0.17)
p["tower_rim"] = p.at_value(p.mix("yellow_ochre", "titanium_white", 0.58), 0.60)
p["lamp_glass"] = p.at_value(p.mix("cadmium_yellow", "titanium_white", 0.78), 0.88)
p["night"] = p.mix("ultramarine", "burnt_umber", 0.48)

# Landmarks: measured places, not guesses.
s.mark("lamp", 0.658, 0.281)
s.mark("tower_base_l", 0.612, 0.690)
s.mark("tower_base_r", 0.704, 0.690)
s.mark("tower_top_l", 0.628, 0.338)
s.mark("tower_top_r", 0.688, 0.338)
s.mark("rock_high", 0.650, 0.640)
s.mark("beam_far", -0.060, 0.390)


def sky_upper():
    return polygon([
        (-0.08, -0.08), (1.08, -0.08), (1.08, 0.30),
        (0.76, 0.255), (0.46, 0.285), (-0.08, 0.245),
    ])


def sky_low():
    return polygon([
        (-0.08, 0.225), (0.46, 0.265), (0.76, 0.235), (1.08, 0.280),
        (1.08, 0.535), (0.78, 0.505), (0.40, 0.525), (-0.08, 0.500),
    ])


def sea_far():
    return polygon([
        (-0.08, 0.495), (0.40, 0.520), (0.78, 0.500), (1.08, 0.530),
        (1.08, 0.760), (-0.08, 0.735),
    ])


def sea_near():
    return polygon([
        (-0.08, 0.705), (0.52, 0.735), (1.08, 0.700),
        (1.08, 1.08), (-0.08, 1.08),
    ])


def headland():
    return polygon([
        (-0.08, 0.505), (0.08, 0.482), (0.18, 0.492), (0.28, 0.470),
        (0.40, 0.505), (0.40, 0.540), (-0.08, 0.535),
    ])


def rock_point():
    return polygon([
        (0.455, 0.735), (0.555, 0.680), (0.650, 0.640), (0.760, 0.655),
        (0.900, 0.720), (1.08, 0.760), (1.08, 1.08), (0.410, 1.08),
    ])


def tower():
    return polygon([
        s.pt("tower_base_l"), s.pt("tower_base_r"),
        s.pt("tower_top_r"), s.pt("tower_top_l"),
    ])


def tower_lit_plane():
    return polygon([
        (0.678, 0.684), (0.704, 0.690), (0.688, 0.338), (0.677, 0.338),
    ])


def gallery():
    return polygon([
        (0.604, 0.338), (0.712, 0.338), (0.700, 0.302), (0.616, 0.302),
    ])


def lantern():
    return polygon([
        (0.628, 0.302), (0.688, 0.302), (0.682, 0.258), (0.634, 0.258),
    ])


def cap():
    return polygon([
        (0.620, 0.258), (0.696, 0.258), (0.668, 0.224),
    ])


def sky_mass():
    s.scumble(sky_upper(), "sky_high", "sky_mid", 7, direction=7,
              load=1.0, load_falloff=0.0, opacity=0.95)


def sky_glow_mass():
    s.scumble(sky_low(), "sky_mid", "horizon_gold", 8, direction=5,
              load=1.0, load_falloff=0.0, opacity=0.95)


def sea_mass():
    s.scumble(sea_far(), "sea", "sea_deep", 8, direction=3,
              load=1.0, load_falloff=0.0, opacity=0.95)
    s.scumble(sea_near(), "sea_deep", "sea", 6, direction=6,
              load=1.0, load_falloff=0.0, opacity=0.92)
