# Shared across every pass: the palette mixed to planned values, every mass as a
# named function so the stack can be re-run in depth order, the value plan as
# numbers, and the budget split written down before the first stroke.
p = s.palette

# ---------------------------------------------------------------- the palette
# A lighthouse mid-conversion into a greenhouse, on a foggy day with no visible
# horizon. Cool, desaturated fog and sea carry the picture; the only strong
# chroma is what belongs to the conversion itself -- terracotta, tomato red,
# leaf green -- and the beam, which has picked up green from the leaves it
# shines through. Three carrying values: rock 0.19 / fog 0.57 / horizon glow 0.67.
def V(base, target, name=None):
    c = p.at_value(base, target)
    if name:
        print(f"  {name:14s} {p.hex(c)}  v={p.value_of(c):.2f}  (asked {target:.2f})")
    return c

def mixtures(verbose=False):
    n = (lambda k: k) if verbose else (lambda k: None)
    fogmix    = p.desaturate(p.mix("ultramarine", "burnt_umber", 0.3), 0.25)
    glowmix   = p.desaturate(p.mix("yellow_ochre", "ultramarine", 0.6), 0.55)
    seafarmix = p.desaturate(p.mix("ultramarine", "viridian", 0.25), 0.3)
    seanearmx = p.desaturate(p.mix("ultramarine", "burnt_umber", 0.35), 0.25)
    rockmix   = p.mix("ultramarine", "burnt_umber", 0.5)
    rockmid   = p.mix("burnt_umber", "ultramarine", 0.35)
    rockcoolm = p.desaturate(p.mix("burnt_umber", "ultramarine", 0.6), 0.35)
    rockwarm  = p.desaturate(p.mix("burnt_umber", "burnt_sienna", 0.35), 0.65)
    towershmx = p.desaturate(p.mix("ultramarine", "burnt_umber", 0.25), 0.45)
    towerlitm = p.mix("titanium_white", "yellow_ochre", 0.12)
    ironmix   = p.mix("ultramarine", "burnt_umber", 0.5)
    terramix  = p.mix("burnt_sienna", "cadmium_red", 0.25)
    terralit  = p.mix("burnt_sienna", "yellow_ochre", 0.3)
    leafdrkmx = p.mix("viridian", "burnt_umber", 0.3)
    leafmidmx = p.mix("viridian", "yellow_ochre", 0.35)
    leaflitmx = p.mix("cadmium_yellow", "viridian", 0.35)
    leafbeammx= p.mix("cadmium_yellow", "viridian", 0.2)
    tomatomix = p.mix("cadmium_red", "cadmium_yellow", 0.15)
    beammix   = p.desaturate(p.mix("cadmium_yellow", "viridian", 0.3), 0.5)
    mossmix   = p.mix("viridian", "burnt_umber", 0.45)
    rustmix   = p.mix("burnt_sienna", "alizarin", 0.3)

    p["fog"]         = V(fogmix,     0.57, n("fog"))         # the atmosphere, everywhere
    p["fog_deep"]    = V(fogmix,     0.50, n("fog_deep"))    # upper fog, a touch darker
    p["glow"]        = V(glowmix,    0.67, n("glow"))        # diffused light low in the fog
    p["sea_far"]     = V(seafarmix,  0.54, n("sea_far"))
    p["sea_near"]    = V(seanearmx,  0.45, n("sea_near"))
    p["rock"]        = V(rockmix,    0.19, n("rock"))        # the anchoring dark
    p["rock_mid"]    = V(rockmid,    0.24, n("rock_mid"))
    p["rock_cool"]   = V(rockcoolm,  0.26, n("rock_cool"))    # ridge, facing the fog
    p["rock_warm"]   = V(rockwarm,   0.25, n("rock_warm"))    # face turned to the glow, muted
    p["rock_deep"]   = V(rockmix,    0.14, n("rock_deep"))
    p["tower_sh"]    = V(towershmx,  0.45, n("tower_sh"))    # the tower's cool side
    p["tower_lit"]   = V(towerlitm,  0.72, n("tower_lit"))   # the side facing the glow
    p["tower_deep"]  = V(towershmx,  0.34, n("tower_deep"))
    p["iron"]        = V(ironmix,    0.17, n("iron"))        # stair, frame, mullions
    p["terracotta"]  = V(terramix,   0.40, n("terracotta"))
    p["terra_lit"]   = V(terralit,   0.53, n("terra_lit"))
    p["terra_deep"]  = V(terramix,   0.27, n("terra_deep"))
    p["leaf_dark"]   = V(leafdrkmx,  0.24, n("leaf_dark"))
    p["leaf_mid"]    = V(leafmidmx,  0.40, n("leaf_mid"))
    p["leaf_lit"]    = V(leaflitmx,  0.58, n("leaf_lit"))
    p["leaf_beam"]   = V(leafbeammx, 0.68, n("leaf_beam"))   # foliage backlit by the lamp
    p["tomato"]      = V(tomatomix,  0.46, n("tomato"))
    p["beam"]        = V(beammix,    0.70, n("beam"))        # the lightest mass: lamplight through leaves
    p["beam_far"]    = V(p.desaturate(p.mix(glowmix, beammix, 0.35), 0.4), 0.60, n("beam_far"))
    p["moss"]        = V(mossmix,    0.22, n("moss"))
    p["rust"]        = V(rustmix,    0.30, n("rust"))
    p["mist"]        = V(p.mix("sea_far", "titanium_white", 0.6), 0.74, n("mist"))

mixtures()

# ---------------------------------------------------------------- the masses
def fog():           # the whole atmosphere -- no horizon; sky and sea share one field
    return Region(-0.04, -0.06, 1.04, 0.84)

def fog_upper_grad():   # darker air overhead, brightening down toward the glow
    return Region(-0.04, -0.06, 1.04, 0.40)

def fog_mid_grad():     # the diffused light, low and wide -- not a sun, not an outline
    return Region(-0.04, 0.28, 1.04, 0.60)

def fog_lower_grad():   # the glow giving back onto the water, darkening toward the foreground
    return Region(-0.04, 0.48, 1.04, 0.84)

def sea():           # loosely: where ripples belong. There is no separate sea mass or
                     # horizon -- the fog gradient above already carries this region.
    return Region(-0.04, 0.56, 1.04, 0.86)

TOWER_BASE_Y, TOWER_TOP_Y = 0.735, 0.115
TOWER_BL, TOWER_BR = 0.335, 0.535
TOWER_TL, TOWER_TR = 0.400, 0.470

def tower_edges(y):
    t = (TOWER_BASE_Y - y) / (TOWER_BASE_Y - TOWER_TOP_Y)
    left = TOWER_BL + (TOWER_TL - TOWER_BL) * t
    right = TOWER_BR + (TOWER_TR - TOWER_BR) * t
    return left, right

def rock():          # the outcrop the tower stands on -- rises a little in the middle
    return polygon([(-0.06, 0.815), (0.07, 0.784), (0.15, 0.795), (0.21, 0.766),
                    (0.29, 0.758), (0.345, 0.708), (0.40, 0.690), (0.465, 0.700),
                    (0.52, 0.688), (0.565, 0.706), (0.615, 0.752), (0.685, 0.765),
                    (0.765, 0.793), (0.86, 0.784), (1.06, 0.815), (1.06, 1.06),
                    (-0.06, 1.06)])

def tower():         # tapered; the base sits into the rock
    return polygon([(TOWER_BL, TOWER_BASE_Y), (TOWER_BR, TOWER_BASE_Y),
                    (TOWER_TR, TOWER_TOP_Y), (TOWER_TL, TOWER_TOP_Y)])

def lit_face():      # the right-hand side, facing the glow
    return polygon([(0.462, TOWER_BASE_Y), (TOWER_BR, TOWER_BASE_Y),
                    (TOWER_TR, TOWER_TOP_Y), (0.452, TOWER_TOP_Y)])

def boulders():      # near rocks, in front of the tower's base
    return blob((0.475, 0.718), 0.05, wobble=0.45, points=9, seed=6, aspect=s.aspect)

def boulders2():
    return blob((0.30, 0.735), 0.034, wobble=0.4, points=8, seed=2, aspect=s.aspect)

def gallery():       # the walkway under the lantern
    return [(0.383, 0.119), (0.487, 0.119)]

def lantern():       # the glass -- now packed with vines
    return polygon([(0.398, 0.118), (0.472, 0.118), (0.468, 0.078), (0.402, 0.078)])

def roof():          # the cap over the lantern
    return polygon([(0.392, 0.080), (0.478, 0.080), (0.455, 0.048), (0.415, 0.048)])

def halo():          # what light escapes the packed glass, on the fog behind it
    return s.circle((0.435, 0.098), 0.042, wobble=0.3, seed=11)

# The switchback stair bolted to the tower's outside: six landings, five
# straight flights between them. A single bent ribbon through all six priced
# out at 141 strokes -- 41% of the budget -- because a bend prices on the box
# it sweeps, cut into pieces by the outline (PAINTING.md, "Masses that are not
# rectangles"). Five straight flights, each a stroke rather than a mass, cost
# five.
STAIR_PTS = [(0.553, 0.715), (0.327, 0.620), (0.533, 0.530),
             (0.346, 0.440), (0.514, 0.350), (0.364, 0.270)]
FLIGHTS = list(zip(STAIR_PTS[:-1], STAIR_PTS[1:]))
LANDINGS = STAIR_PTS[1:-1]   # the interior turns, where a platform sits

POTS = [  # (x, y, radius) -- landings first, then a few mid-flight, largest low
    (0.553, 0.715, 0.020), (0.327, 0.620, 0.017), (0.533, 0.530, 0.0145),
    (0.346, 0.440, 0.012), (0.514, 0.350, 0.0105), (0.364, 0.270, 0.0088),
    (0.44, 0.667, 0.012), (0.44, 0.485, 0.0095), (0.44, 0.310, 0.0078),
]

def beam():          # the wedge of lit fog swept out from the lamp, down onto the sea
    return polygon([(0.478, 0.155), (1.06, 0.30), (1.06, 0.72), (0.478, 0.20)])

# ---------------------------------------------------------------- value plan
PLAN = {
    span("F1", "H2"):                    0.57,   # upper fog, clear of the tower
    span("F4", "H5"):                    0.66,   # the diffused glow, low and wide
    span("F7", "H8"):                    0.47,   # near sea, clear of the rock
    span("A6", "B7"):                    0.20,   # rock, left of the tower
    Region(0.345, 0.30, 0.395, 0.55):    0.45,   # tower, shadow side
    Region(0.475, 0.30, 0.525, 0.55):    0.72,   # tower, lit side
}

# ---------------------------------------------------------------- the split
# Written before the first stroke. The picture is the lamp room and the stairs --
# the two places the conversion actually shows.
SPLIT = {"fog and sea": 45, "rock": 30, "beam": 20, "tower": 45,
         "stairs and pots": 55, "lamp room and vines": 60,
         "edges and finish": 35, "reserve": 50}
