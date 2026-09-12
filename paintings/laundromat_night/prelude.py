# Shared across every pass: the palette as planned values, every mass as a shape
# function, and each depth layer named so the whole stack can be re-run for a repair.
#
# Subject: a laundromat at night, seen from the sidewalk across the street.
# One light story - cold fluorescent out of the window, warm sodium off-canvas
# right catching the facade and the wet road.
p = s.palette


def V(base, target, name=None):
    c = p.at_value(base, target)
    if name:
        print(f"  {name:10s} {p.hex(c)}  v={p.value_of(c):.2f}  (asked {target:.2f})")
    return c


# ---------------------------------------------------------------- the palette
def mixtures(verbose=False):
    n = (lambda k: k) if verbose else (lambda k: None)
    cool_black = p.mix("ultramarine", "burnt_umber", 0.35)
    warm_black = p.mix("ultramarine", "burnt_umber", 0.62)
    night_blue = p.mix("ultramarine", "burnt_umber", 0.22)
    fluoro = p.desaturate(p.mix(p.mix("lemon_yellow", "viridian", 0.16),
                                "titanium_white", 0.70), 0.22)
    sodium = p.mix("yellow_ochre", "cadmium_red", 0.18)
    asphalt = p.desaturate(p.mix("ultramarine", "burnt_umber", 0.45), 0.35)

    p["sky"] = V(night_blue, 0.27, n("sky"))                     # city haze overhead
    p["sky_lo"] = V(p.mix(night_blue, sodium, 0.22), 0.38, n("sky_lo"))
    p["facade"] = V(warm_black, 0.17, n("facade"))               # the anchoring dark
    p["facade_lt"] = V(p.mix(warm_black, sodium, 0.30), 0.26, n("facade_lt"))
    p["facade_dk"] = V(p.mix(warm_black, cool_black, 0.5), 0.145, n("facade_dk"))
    p["frame"] = V(p.mix(warm_black, cool_black, 0.5), 0.155, n("frame"))
    p["asphalt"] = V(asphalt, 0.23, n("asphalt"))
    p["kerb"] = V(p.mix(asphalt, sodium, 0.22), 0.33, n("kerb"))
    p["wet_lo"] = V(p.mix(asphalt, sodium, 0.30), 0.36, n("wet_lo"))
    p["wet_mid"] = V(p.mix(asphalt, sodium, 0.35), 0.46, n("wet_mid"))
    p["wet_hi"] = V(p.mix(asphalt, sodium, 0.55), 0.58, n("wet_hi"))
    p["wall_lo"] = V(p.desaturate(fluoro, 0.18), 0.74, n("wall_lo"))
    p["interior"] = V(fluoro, 0.88, n("interior"))               # the lightest mass
    p["hot"] = V(p.mix(fluoro, "titanium_white", 0.55), 0.95, n("hot"))
    p["machine"] = V(p.desaturate(p.mix(fluoro, cool_black, 0.42), 0.25), 0.52, n("machine"))
    p["mach_hi"] = V(p.desaturate(p.mix(fluoro, cool_black, 0.22), 0.20), 0.67, n("mach_hi"))
    p["mach_dk"] = V(p.mix(cool_black, fluoro, 0.18), 0.33, n("mach_dk"))
    p["figure"] = V(p.mix(cool_black, "burnt_sienna", 0.28), 0.24, n("figure"))
    p["spill"] = V(p.mix(sodium, fluoro, 0.45), 0.66, n("spill"))
    # The two lights have to stay separate or the picture has one. The window is
    # cold fluorescent, so what it throws on the pavement is cold; only the lamp
    # off-canvas right is warm. Mixed at 0.45 the pool came back amber, which read
    # as sodium coming out of a laundromat.
    p["spill_cool"] = V(p.mix(sodium, fluoro, 0.82), 0.66, n("spill_cool"))
    p["refl_hi"] = V(p.mix(asphalt, fluoro, 0.62), 0.56, n("refl_hi"))
    p["refl_lo"] = V(p.mix(asphalt, fluoro, 0.30), 0.325, n("refl_lo"))


mixtures()

# ---------------------------------------------------------------- the geometry
# Nothing here is a rectangle. The roofline steps, the shopfront is out of true,
# the kerb and the sidewalk converge a little to the right.
# Bolder than it wants to be: a step small enough to look right on paper is
# smaller than any brush that can lay a mass this size, and gets overhung away.
ROOF = [(-0.05, 0.238), (0.12, 0.230), (0.213, 0.223),
        (0.222, 0.118), (0.470, 0.110), (0.480, 0.206),
        (0.660, 0.212), (0.790, 0.202),
        (0.905, 0.220), (1.05, 0.213)]
VENT = [(0.806, 0.216), (0.810, 0.121), (0.856, 0.118), (0.861, 0.216)]
BASE = [(1.05, 0.733), (0.62, 0.722), (0.30, 0.714), (-0.05, 0.705)]
KERB = [(-0.05, 0.792), (0.35, 0.781), (0.70, 0.770), (1.05, 0.756)]

# the shopfront window: wide, low, and a little out of square
WIN = [(0.172, 0.340), (0.452, 0.333), (0.719, 0.337),
       (0.716, 0.607), (0.448, 0.611), (0.175, 0.604)]
# the glass door beside it: narrower, dimmer, and it reaches the ground
DOOR = [(0.778, 0.328), (0.892, 0.331), (0.897, 0.700), (0.780, 0.697)]
MULLION_X = (0.336, 0.548)           # unevenly spaced on purpose


def sky():
    return polygon([(-0.05, -0.06), (1.05, -0.06), (1.05, 0.32), (-0.05, 0.30)])


def vent():
    return polygon(VENT)


def facade():
    return polygon(ROOF + BASE)


def sidewalk():
    return polygon(BASE[::-1] + KERB[::-1])


def road():
    return polygon(KERB + [(1.05, 1.05), (-0.05, 1.05)])


def window_open():
    return polygon(WIN)


def door_open():
    return polygon(DOOR)


def fascia():
    # the shop's sign board: spans the window and the door, tilts a little, and its
    # underside is what the window lights from below
    return polygon([(0.155, 0.258), (0.500, 0.250), (0.912, 0.256),
                    (0.909, 0.323), (0.499, 0.329), (0.158, 0.325)])


def base_course():
    return polygon([(-0.05, 0.668), (0.35, 0.673), (0.72, 0.680), (1.05, 0.688),
                    (1.05, 0.735), (0.62, 0.724), (0.30, 0.716), (-0.05, 0.707)])


def machine_band():
    return polygon([(0.182, 0.520), (0.400, 0.514), (0.578, 0.523),
                    (0.575, 0.606), (0.398, 0.610), (0.180, 0.603)])


def figure():
    # Seated, backlit, facing left. Three shapes unioned rather than one outline:
    # union keeps a waist where a hull would fill it in. Two things are deliberate.
    # The knee overlaps the torso by 0.026 and the neck rises as a column *into* the
    # head circle, so inset() cannot pinch either join off -- the first preview had
    # the knee as a floating blob. And smooth(1), not the default two passes, which
    # cut the neck notch away and handed back a lump with no shoulders.
    head = s.circle((0.629, 0.486), 0.0160)
    torso = polygon([(0.618, 0.487), (0.641, 0.487), (0.646, 0.505),
                     (0.657, 0.520), (0.662, 0.558), (0.657, 0.601),
                     (0.597, 0.601), (0.593, 0.548), (0.600, 0.518),
                     (0.612, 0.504)])
    knee = polygon([(0.620, 0.548), (0.618, 0.601), (0.564, 0.601),
                    (0.561, 0.575), (0.584, 0.551)])
    return union(head, torso, knee).smooth(1)


def reflection():
    # the window's smear on the wet road: wider at the bottom, and it leans
    return polygon([(0.206, 0.756), (0.712, 0.752), (0.760, 1.05), (0.152, 1.05)])


def door_reflection():
    return polygon([(0.784, 0.742), (0.896, 0.740), (0.940, 1.05), (0.822, 1.05)])


# ---------------------------------------------------------------- value plan
# Each place sits well inside one mass, so a moved silhouette does not strand it.
PLAN = {
    span("A1", "H1"): 0.29,      # sky, clear of the roofline
    span("A4", "A5"): 0.18,      # facade, left of the window
    span("D4", "D4"): 0.86,      # the lit interior, above the machines
    # Re-read twice, and this is the considered number rather than the first guess.
    # 0.40 was planned for a reflection conceived as a lit patch. Laid as streaks
    # over dark asphalt -- which is what a wet road is -- the place reads 0.22, and
    # hitting 0.40 would mean flooding the near foreground to satisfy a number I had
    # written before the reflection existed. The road directly under the viewer, out
    # of the light, should be close to the darkest thing in the picture: it anchors
    # the bottom edge and keeps the eye up at the window. 0.25 is what that is.
    span("C8", "F8"): 0.25,      # the reflection as it dies, foreground
    span("A8", "A8"): 0.26,      # road, out of the reflection
}
