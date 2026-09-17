# Shared across every pass: the palette mixed to planned values, every mass as a
# named function so the stack can be re-run in depth order, the value plan as
# numbers, and the budget split written down before the first stroke.
p = s.palette

# ---------------------------------------------------------------- the palette
# A lighthouse half way through becoming a greenhouse. Thick fog, so the light is
# flat and everything far away dissolves; the tower is near and keeps its dark.
# Its whitewash has gone green with damp. The lamp still turns, and its beam
# comes out through a lantern packed with tomato vine, so what crosses the fog is
# green. Three carrying values: the darks 0.20 / the tower and sea 0.44 / the fog
# 0.63, with the beam above all of them at 0.75.
def V(base, target, name=None):
    c = p.at_value(base, target)
    if name:
        print(f"  {name:12s} {p.hex(c)}  v={p.value_of(c):.2f}  (asked {target:.2f})")
    return c


def mixtures(verbose=False):
    n = (lambda k: k) if verbose else (lambda k: None)
    fog      = p.desaturate(p.mix("ultramarine", "burnt_umber", 0.30), 0.45)
    seawater = p.desaturate(p.mix("ultramarine", "viridian", 0.40), 0.40)
    green    = p.mix(p.mix("lemon_yellow", "viridian", 0.28), "titanium_white", 0.35)
    # The beam is fog with a green cast, not green paint. Rehearsed once at the
    # raw mixture and it came back a chartreuse searchlight that owned the
    # picture; what carries "tinted through leaves" is the hue being *just*
    # off-neutral against a grey fog, and the value doing the rest.
    lit      = p.desaturate(green, 0.58)
    wash     = p.desaturate(p.mix("yellow_ochre", "viridian", 0.30), 0.55)
    iron     = p.mix("ultramarine", "burnt_umber", 0.55)
    stone    = p.mix("burnt_umber", "ultramarine", 0.35)
    leaf     = p.mix("viridian", "cadmium_yellow", 0.30)
    leaf_up  = p.mix("cadmium_yellow", "viridian", 0.35)
    clay     = p.desaturate(p.mix("burnt_sienna", "cadmium_red", 0.22), 0.30)
    fruit    = p.mix("cadmium_red", "alizarin", 0.20)
    filament = p.mix("lemon_yellow", "titanium_white", 0.30)

    p["fog_high"]  = V(fog,      0.58, n("fog_high"))   # the top of the canvas
    p["fog_low"]   = V(fog,      0.68, n("fog_low"))    # thickening to the horizon
    p["fog_warm"]  = V(p.desaturate(p.mix("yellow_ochre", "cerulean", 0.45), 0.60),
                                 0.71, n("fog_warm"))   # the day somewhere behind it
    p["sea_far"]   = V(seawater, 0.54, n("sea_far"))    # barely under the fog
    p["sea_near"]  = V(seawater, 0.40, n("sea_near"))
    p["beam"]      = V(lit,      0.75, n("beam"))       # the lightest mass
    p["beam_core"] = V(p.desaturate(green, 0.40), 0.82, n("beam_core"))
    p["glow"]      = V(lit,      0.635, n("glow"))      # light in the air, on fog
    # The cylinder turns in temperature as well as in value: the shadow side
    # takes the cool of the sky, the lit side the warmth of the diffuse light off
    # the water. Value alone gave three flat slabs in rehearsal.
    p["tower_sh"]  = V(p.mix(wash, "ultramarine", 0.14), 0.30, n("tower_sh"))
    p["tower_mid"] = V(wash,     0.40, n("tower_mid"))
    p["tower_lit"] = V(p.desaturate(p.mix(wash, "yellow_ochre", 0.16), 0.35),
                                 0.48, n("tower_lit"))
    # 0.28/0.40/0.50 and no wider: a mass shaded past about 0.15 across itself
    # buys form by spending the separation that made it a mass. At 0.60 the lit
    # band sat on the fog's own value and the silhouette went with it.
    p["stain"]     = V(p.mix("viridian", "burnt_umber", 0.45), 0.24, n("stain"))
    p["iron"]      = V(iron,     0.17, n("iron"))       # gallery, stair, mullions
    p["rock"]      = V(stone,    0.21, n("rock"))       # the anchoring dark
    p["rock_lit"]  = V(stone,    0.29, n("rock_lit"))   # and no lighter: at 0.33
                                                        # it sat 0.07 off the near
                                                        # sea and stopped being a dark
    p["leaf_dark"] = V(leaf,     0.20, n("leaf_dark"))  # the vine mass in the glass
    p["leaf_mid"]  = V(leaf,     0.34, n("leaf_mid"))
    p["leaf_lit"]  = V(leaf_up,  0.54, n("leaf_lit"))   # a leaf with the fog through it
    p["pot"]       = V(clay,     0.36, n("pot"))        # the one warm note, and
    p["pot_lit"]   = V(clay,     0.50, n("pot_lit"))    # knocked back: at full
                                                        # chroma ten of them read
                                                        # as plastic bricks
    p["tomato"]    = V(fruit,    0.36, n("tomato"))
    p["glass"]     = V(p.desaturate(p.mix("cerulean", "yellow_ochre", 0.35), 0.45),
                                 0.56, n("glass"))      # what is left showing of it
    p["lamp"]      = V(filament, 0.90, n("lamp"))       # the lightest thing, tiny


mixtures()

# ---------------------------------------------------------------- the masses
HORIZON = 0.600
LAMP = (0.310, 0.168)          # where the beam leaves the lantern


def fog_field():               # everything above the rock, run off every edge
    return Region(-0.05, -0.05, 1.05, 0.90)


def fog_upper():
    return Region(-0.05, -0.05, 1.05, 0.44)


def fog_lower():               # the scumble that thickens toward the horizon
    return Region(-0.05, 0.16, 1.05, 0.63)


def sea():
    return Region(-0.05, HORIZON - 0.004, 1.05, 1.05)


def sea_near_band():
    return Region(-0.05, 0.72, 1.05, 1.05)


def rock():                    # near, in front of the tower's foot; rises to the
                               # left and falls away right, so the sea is a wedge
                               # rather than a band. Unsmoothed and serrated: laid
                               # as a smooth line it came back a ramp, and rock
                               # has corners.
    return polygon([(-0.06, 0.762), (0.04, 0.794), (0.09, 0.779), (0.14, 0.813),
                    (0.20, 0.805), (0.26, 0.837), (0.33, 0.828), (0.38, 0.859),
                    (0.44, 0.847), (0.49, 0.885), (0.55, 0.871), (0.60, 0.909),
                    (0.67, 0.897), (0.72, 0.937), (0.79, 0.927), (0.85, 0.965),
                    (0.92, 0.957), (1.06, 1.012), (1.06, 1.062), (-0.06, 1.062)])


def tower():                   # tapered, flaring at the foot, buried in the rock
    return polygon([(0.170, 0.258), (0.163, 0.400), (0.154, 0.540), (0.142, 0.680),
                    (0.128, 0.820), (0.118, 0.940), (0.398, 0.940), (0.384, 0.820),
                    (0.368, 0.680), (0.357, 0.540), (0.348, 0.400), (0.340, 0.258)])


def tower_mid_face():          # the middle plane: off the shadow side, and it
                               # runs under the lit one rather than butting it. Smoothed: unsmoothed, the
                               # chain of straight segments came back as a staircase down the edge
    return polygon([(0.222, 0.266), (0.216, 0.400), (0.208, 0.540), (0.198, 0.680),
                    (0.186, 0.820), (0.176, 0.905), (0.354, 0.905), (0.340, 0.820),
                    (0.328, 0.680), (0.321, 0.540), (0.317, 0.400), (0.313, 0.268)]
                   ).smooth(3)


def tower_lit_face():          # the plane facing the sea. It runs *to* the
                               # silhouette, not inside it: held short, the dark
                               # left over between them read as a drawn outline
                               # down the right of the tower
    return polygon([(0.303, 0.268), (0.307, 0.400), (0.311, 0.540), (0.318, 0.680),
                    (0.330, 0.820), (0.344, 0.905), (0.398, 0.940), (0.384, 0.820),
                    (0.368, 0.680), (0.357, 0.540), (0.348, 0.400), (0.340, 0.258)]
                   ).smooth(3)


def gallery():                 # the walkway plate under the lantern: wider than
                               # the shaft, and the thing the stair arrives at
    return polygon([(0.136, 0.236), (0.374, 0.236), (0.366, 0.266), (0.144, 0.266)])


def lantern():                 # the glass house at the top
    return polygon([(0.160, 0.108), (0.350, 0.108), (0.344, 0.234), (0.166, 0.234)])


def roof():                    # the cap, with its vent propped open
    return polygon([(0.150, 0.112), (0.360, 0.112), (0.300, 0.062), (0.212, 0.062)])


def vines():                   # the mass inside the glass, pressing on it. Sized
                               # so the brush's own spill reaches the frame: what
                               # goes past it is leaves against the panes, and the
                               # near mullions go on over it anyway.
    return blob((0.254, 0.173), 0.066, wobble=0.42, points=13, seed=4, aspect=0.72)


def halo():                    # the lamp's light in the fog, round the lantern
    return s.circle((0.262, 0.158), 0.118, wobble=0.30)


def beam():                    # a wedge of lit fog, widening away from the lamp
                               # and reaching the water at the far right
    return polygon([(0.300, 0.146), (1.06, 0.238), (1.06, 0.560), (0.302, 0.194)])


# Four turns of the outside stair. Seen from a little below, the front of each
# turn sags; it descends to the right, goes round the back, and comes out one
# turn lower on the left. Each arc is given as its own curve so no two are the
# same sag or the same length.
# The turns get further apart as they come down, because the eye is below them.
STAIRS = [
    ([(0.166, 0.322), (0.216, 0.345), (0.268, 0.353), (0.318, 0.340),
      (0.347, 0.322)], 0.011),
    ([(0.159, 0.455), (0.213, 0.483), (0.267, 0.492), (0.322, 0.476),
      (0.352, 0.457)], 0.012),
    ([(0.149, 0.600), (0.207, 0.632), (0.265, 0.643), (0.323, 0.625),
      (0.362, 0.601)], 0.013),
    ([(0.135, 0.760), (0.200, 0.797), (0.262, 0.808), (0.329, 0.789),
      (0.376, 0.762)], 0.015),
]

# The pots, on the arcs and on the gallery -- the planting list, and what must
# not repeat across it is everything except the fact of being a pot: size, tilt,
# how dark the clay is, whether the rim catches anything, which way the growth
# goes, and whether there is any. Each sits a little *into* its stair: the arcs
# are splines and sag below the straight line between their points, so pots
# placed off a linear reading of them floated above the tread.
#   x, y, r, tilt, body value, rim value or None, (dx, dy, colour, size, load)
POTS = [
    (0.206, 0.333, 0.0175, -7, 0.38, 0.52, (+0.012, -0.032, "leaf_mid", 0.018, 0.75)),
    (0.298, 0.343, 0.0125, +5, 0.31, None, (-0.009, -0.022, "leaf_dark", 0.012, 0.55)),
    (0.232, 0.482, 0.0150, +9, 0.36, 0.49, (+0.016, +0.028, "leaf_mid", 0.015, 0.65)),
    (0.316, 0.470, 0.0180, -4, 0.40, 0.54, (-0.007, -0.036, "leaf_lit", 0.017, 0.85)),
    (0.184, 0.617, 0.0130, +12, 0.29, None, None),
    (0.272, 0.630, 0.0205, -6, 0.38, 0.51, (+0.020, +0.032, "leaf_mid", 0.020, 0.60)),
    (0.216, 0.794, 0.0165, +6, 0.34, None, (-0.014, -0.028, "leaf_dark", 0.016, 0.70)),
    (0.318, 0.779, 0.0230, -9, 0.41, 0.56, (+0.009, -0.044, "leaf_lit", 0.023, 0.80)),
    (0.177, 0.233, 0.0115, +8, 0.32, None, (+0.007, -0.019, "leaf_mid", 0.011, 0.55)),
    (0.342, 0.231, 0.0135, -5, 0.39, 0.53, (-0.011, +0.024, "leaf_dark", 0.014, 0.65)),
]

# ---------------------------------------------------------------- value plan
# Written before the first stroke, checked after every mass by check.py. Each
# place is chosen to sit on one mass only -- and re-read whenever a silhouette
# moves, because a place is a rectangle and a mass is not.
PLAN = {
    Region(0.42, 0.02, 0.98, 0.11):  0.58,   # fog, above the beam
    Region(0.44, 0.49, 0.72, 0.57):  0.68,   # fog, thickened toward the horizon
    Region(0.38, 0.20, 0.60, 0.26):  0.75,   # the beam, the lightest mass
    Region(0.50, 0.63, 0.95, 0.71):  0.54,   # far sea
    Region(0.55, 0.79, 1.00, 0.87):  0.40,   # near sea
    Region(0.52, 0.94, 0.86, 1.00):  0.21,   # rock, the anchoring dark
    Region(0.19, 0.52, 0.31, 0.59):  0.40,   # the tower's body, between two arcs
    Region(0.19, 0.14, 0.33, 0.21):  0.26,   # the vines behind the glass
}

# ---------------------------------------------------------------- the split
# The picture is the conversion: the lantern full of vine, the pots coming down
# the stair, and the green beam that says why. That is 164 of 300 -- 55%.
SPLIT = {"fog": 40, "sea": 22, "rock": 28,
         "beam and halo": 26, "tower": 40, "stair and pots": 46, "lantern": 52,
         "edges and finish": 26, "reserve": 20}

SUBJECT = ("beam and halo", "tower", "stair and pots", "lantern")


def share():
    """What went on the subject, against the plan. note='subject' as you paint."""
    paid = [r for r in s.history.records
            if r.kind not in ("dry", "look", "pencil", "erase")]
    on_it = [r for r in paid if "subject" in (r.note or "")]
    planned = sum(SPLIT[k] for k in SUBJECT) / sum(SPLIT.values())
    print(f"subject: {len(on_it)} of {len(paid)} marks -- "
          f"{len(on_it) / max(len(paid), 1):.0%} against a planned {planned:.0%}")
