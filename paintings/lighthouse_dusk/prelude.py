# Shared across every pass: the palette mixed to planned values, every mass as a
# named function so the stack can be re-run in depth order, the value plan as
# numbers, and the budget split written down before the first stroke.
p = s.palette

# ---------------------------------------------------------------- the palette
# A lighthouse on a rocky headland at dusk. The sun has just gone down off the
# right edge: the glow is at the right-hand horizon, the moon hangs over it, and
# the tower's right side catches the last warm light while its left side goes
# cool. Three carrying values: rock 0.16 / sea 0.44 / glow 0.74.
def V(base, target, name=None):
    c = p.at_value(base, target)
    if name:
        print(f"  {name:12s} {p.hex(c)}  v={p.value_of(c):.2f}  (asked {target:.2f})")
    return c

def mixtures(verbose=False):
    n = (lambda k: k) if verbose else (lambda k: None)
    indigo   = p.mix("ultramarine", "alizarin", 0.25)
    violet   = p.desaturate(p.mix("ultramarine", "alizarin", 0.50), 0.30)
    peach    = p.desaturate(p.mix("yellow_ochre", "cadmium_red", 0.30), 0.20)
    orange   = p.mix("cadmium_yellow", "cadmium_red", 0.30)
    teal     = p.desaturate(p.mix("ultramarine", "viridian", 0.30), 0.30)
    deep     = p.mix("ultramarine", "viridian", 0.35)
    umber_bl = p.mix("burnt_umber", "ultramarine", 0.35)
    warmrock = p.mix("burnt_sienna", "burnt_umber", 0.30)
    greyvio  = p.desaturate(p.mix("ultramarine", "alizarin", 0.40), 0.35)
    cream    = p.mix("titanium_white", p.mix("yellow_ochre", "cadmium_red", 0.25), 0.25)
    red      = p.mix("cadmium_red", "alizarin", 0.25)
    darkred  = p.mix("alizarin", "ultramarine", 0.20)
    iron     = p.mix("ultramarine", "burnt_umber", 0.50)
    lamp     = p.mix("titanium_white", "cadmium_yellow", 0.20)
    gold     = p.mix("cadmium_yellow", "yellow_ochre", 0.30)
    moon     = p.mix("titanium_white", "lemon_yellow", 0.08)

    p["sky_top"]   = V(indigo,   0.28, n("sky_top"))    # the dark of the sky
    p["sky_mid"]   = V(violet,   0.46, n("sky_mid"))
    p["sky_low"]   = V(peach,    0.60, n("sky_low"))    # the left horizon, fading
    p["glow"]      = V(orange,   0.74, n("glow"))       # the right horizon, lightest mass
    p["glow_core"] = V(p.mix("cadmium_yellow", "lemon_yellow", 0.4), 0.82, n("glow_core"))
    p["sea_far"]   = V(teal,     0.50, n("sea_far"))
    p["sea_near"]  = V(deep,     0.34, n("sea_near"))
    p["sea_lit"]   = V(p.mix("yellow_ochre", "cadmium_red", 0.20), 0.64, n("sea_lit"))
    p["rock"]      = V(umber_bl, 0.16, n("rock"))       # the anchoring dark
    p["rock_mid"]  = V(warmrock, 0.22, n("rock_mid"))
    p["rock_lit"]  = V(warmrock, 0.30, n("rock_lit"))
    p["tower_sh"]  = V(greyvio,  0.36, n("tower_sh"))   # the cool side
    p["tower_lit"] = V(cream,    0.72, n("tower_lit"))  # the side facing the glow
    p["band_lit"]  = V(red,      0.42, n("band_lit"))
    p["band_sh"]   = V(darkred,  0.24, n("band_sh"))
    p["iron"]      = V(iron,     0.18, n("iron"))       # gallery, mullions, roof
    p["lamp"]      = V(lamp,     0.92, n("lamp"))       # the lightest thing, tiny
    p["lamp_glow"] = V(gold,     0.64, n("lamp_glow"))  # halo centre, the beam
    p["moon"]      = V(moon,     0.94, n("moon"))

mixtures()

# ---------------------------------------------------------------- the masses
HORIZON = 0.58

def sky():          # runs off the top and under the sea
    return Region(-0.04, -0.05, 1.04, 0.61)

def sky_upper():    # indigo down to violet
    return Region(-0.04, -0.05, 1.04, 0.36)

def sky_lower():    # violet down to the peach at the horizon
    return Region(-0.04, 0.30, 1.04, 0.61)

def glow_patch():   # the afterglow, centred on the right-hand horizon; the sea
                    # covers its lower half and the reflection continues it
    return ellipse((0.76, HORIZON + 0.035), 0.36, 0.12)

def sea():
    return Region(-0.04, HORIZON - 0.005, 1.04, 1.05)

def headland():     # the rock mass, rising to the left, meeting the frame.
                    # Not smoothed: rock has corners, and a smoothed outline came
                    # back as a hull.
    return polygon([(-0.25, 0.53), (-0.05, 0.545), (0.03, 0.535), (0.08, 0.557),
                    (0.13, 0.552), (0.19, 0.586), (0.23, 0.592), (0.29, 0.607),
                    (0.34, 0.602), (0.40, 0.636), (0.45, 0.662), (0.49, 0.666),
                    (0.52, 0.702), (0.55, 0.746), (0.57, 0.792), (0.61, 0.872),
                    (0.63, 0.94), (0.64, 1.25), (-0.25, 1.25)])

def boulders():     # the near rocks, in front of the tower's base
    return blob((0.285, 0.658), 0.068, wobble=0.45, points=9, seed=5, aspect=s.aspect)

TOWER_X = 0.270
def tower():        # tapered; the base sits into the rock
    return polygon([(0.228, 0.630), (0.312, 0.630), (0.297, 0.165), (0.243, 0.165)])

def band():         # the red band, a little below the middle
    return polygon([(0.2365, 0.375), (0.3035, 0.375), (0.3010, 0.445), (0.2390, 0.445)])

def gallery():      # the walkway under the lantern: a dark plate wider than the tower
    return [(0.226, 0.160), (0.314, 0.160)]

def lantern():      # the glass
    return polygon([(0.250, 0.100), (0.290, 0.100), (0.290, 0.152), (0.250, 0.152)])

def roof():         # the cap over the lantern
    return polygon([(0.244, 0.102), (0.296, 0.102), (0.278, 0.072), (0.262, 0.072)])

def halo():         # the lamp's light in the air, on the sky behind the lantern
    return s.circle((0.270, 0.124), 0.085, wobble=0.3, seed=9)

MOON = (0.86, 0.10)

# ---------------------------------------------------------------- value plan
PLAN = {
    span("A1", "H1"):                    0.30,   # sky top, indigo
    span("A3", "H3"):                    0.46,   # sky mid
    Region(0.62, 0.48, 0.96, 0.575):     0.72,   # the glow, the lightest mass
    Region(0.00, 0.48, 0.20, 0.575):     0.60,   # left horizon, peach
    span("F6", "H6"):                    0.50,   # far sea
    span("E8", "H8"):                    0.34,   # near sea
    span("A7", "C8"):                    0.17,   # rock, the anchoring dark
}

# ---------------------------------------------------------------- the split
# Written before the first stroke. The picture is the tower and its light.
SPLIT = {"sky": 50, "sea": 35, "rocks": 35, "tower and lantern": 75,
         "halo, beam, moon": 20, "edges and finish": 25, "reserve": 60}
