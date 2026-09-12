# Shared across every pass: the palette mixed to planned values, every mass as a
# named function so the stack can be re-run in depth order, the value plan as
# numbers, and the budget split written down before the first stroke.
import math
p = s.palette

# ---------------------------------------------------------------- the palette
# A lighthouse half-way to becoming a greenhouse, in sea fog. The tower stands on
# the right third; its lamp room is full of tomato vines pressed against the
# glass, and the lamp behind them throws a beam to the left across the fog,
# tinted green by the leaves. Terracotta pots spiral down the outside stair.
# Three carrying values: rock 0.17 / sea and tower 0.34-0.56 / fog and beam
# 0.66-0.80, with the light in the lamp room the lightest thing at 0.90.
def V(base, target, name=None):
    c = p.at_value(base, target)
    if name:
        print(f"  {name:11s} {p.hex(c)}  v={p.value_of(c):.2f}  (asked {target:.2f})")
    return c

def mixtures(verbose=False):
    n = (lambda k: k) if verbose else (lambda k: None)
    fogbase  = p.desaturate(p.mix("ultramarine", "yellow_ochre", 0.50), 0.30)   # a neutral grey, faintly warm
    beambase = p.mix("lemon_yellow", "viridian", 0.30)
    seabase  = p.desaturate(p.mix(p.mix("cerulean", "viridian", 0.45), "burnt_umber", 0.15), 0.40)
    deepsea  = p.desaturate(p.mix("ultramarine", "viridian", 0.45), 0.35)
    dark     = p.mix("ultramarine", "burnt_umber", 0.55)
    warmrock = p.mix("burnt_umber", "burnt_sienna", 0.30)
    stone    = p.desaturate(p.mix("ultramarine", "burnt_umber", 0.40), 0.25)
    cream    = p.desaturate(p.mix("yellow_ochre", "titanium_white", 0.50), 0.35)
    terra    = p.mix("burnt_sienna", "cadmium_red", 0.35)
    leaf     = p.mix("viridian", "cadmium_yellow", 0.40)

    p["fog"]        = V(fogbase, 0.66, n("fog"))          # the big light mass
    p["fog_top"]    = V(p.desaturate(p.mix("ultramarine", "yellow_ochre", 0.40), 0.25), 0.58, n("fog_top"))
    p["fog_low"]    = V(p.desaturate(p.mix("ultramarine", "yellow_ochre", 0.58), 0.30), 0.70, n("fog_low"))
    p["beam"]       = V(beambase, 0.78, n("beam"))        # light in the fog
    p["beam_core"]  = V(p.mix("lemon_yellow", "viridian", 0.14), 0.84, n("beam_core"))
    p["halo"]       = V(p.desaturate(p.mix("cadmium_yellow", "viridian", 0.30), 0.25), 0.76, n("halo"))
    p["sea_far"]    = V(seabase, 0.61, n("sea_far"))     # nearly lost in the fog
    p["sea_near"]   = V(deepsea, 0.40, n("sea_near"))
    p["sea_deep"]   = V(deepsea, 0.33, n("sea_deep"))
    p["rock"]       = V(dark, 0.17, n("rock"))            # the anchoring dark
    p["rock_lit"]   = V(warmrock, 0.27, n("rock_lit"))
    p["rock_cool"]  = V(p.mix(dark, fogbase, 0.40), 0.24, n("rock_cool"))
    p["tower_sh"]   = V(stone, 0.34, n("tower_sh"))       # the cool side
    p["tower_lit"]  = V(cream, 0.52, n("tower_lit"))      # the side facing the sea
    p["iron"]       = V(dark, 0.19, n("iron"))            # gallery, mullions, stair
    p["terra"]      = V(terra, 0.38, n("terra"))          # the pots
    p["terra_lit"]  = V(p.mix(terra, "yellow_ochre", 0.40), 0.52, n("terra_lit"))
    p["leaf"]       = V(leaf, 0.42, n("leaf"))            # vines against the glass
    p["leaf_dark"]  = V(p.mix("viridian", "burnt_umber", 0.30), 0.24, n("leaf_dark"))
    p["leaf_lit"]   = V(p.mix("lemon_yellow", "viridian", 0.30), 0.70, n("leaf_lit"))
    p["glow"]       = V(p.mix("titanium_white", "lemon_yellow", 0.35), 0.90, n("glow"))
    p["tomato"]     = V(p.mix("cadmium_red", "alizarin", 0.20), 0.36, n("tomato"))
    p["tomato_lit"] = V(p.mix("cadmium_red", "cadmium_yellow", 0.25), 0.50, n("tomato_lit"))

mixtures()

# ---------------------------------------------------------------- the masses
TX = 0.66                       # the tower's centre line
def r_at(y):                    # the tower's half-width at a height: tapered
    return 0.048 + 0.027 * (y - 0.31) / 0.59

def fog():          return Region(-0.05, -0.05, 1.05, 0.66)
def fog_upper():    return Region(-0.05, -0.05, 1.05, 0.40)
def fog_lower():    return Region(-0.05, 0.34, 1.05, 0.66)
def horizon_band(): return Region(-0.05, 0.55, 1.05, 0.68)
def sea():          return Region(-0.05, 0.60, 1.05, 1.05)

def beam():         # the wedge of lit fog, from the lamp room off the left edge
    return polygon([(0.63, 0.205), (-0.06, 0.29), (-0.06, 0.54), (0.63, 0.275)])

def rocks():        # the tower's footing, lower right, meeting the frame: a spur
                    # running out to the left, a hump to the right, a dip between.
                    # Few corners, and bold ones: rock is faceted, not wavy.
    return polygon([(0.38, 1.06), (0.44, 0.965), (0.50, 0.912), (0.56, 0.886),
                    (0.63, 0.878), (0.70, 0.858), (0.77, 0.866), (0.81, 0.842),
                    (0.86, 0.806), (0.93, 0.796), (0.99, 0.818), (1.06, 0.806),
                    (1.06, 1.06)])

def subdivide(points, n=6):     # extra points along each side, so the clean
                                # contour's spline hugs a straight edge instead
                                # of overshooting a four-cornered mass
    out = []
    for (x0, y0), (x1, y1) in zip(points, points[1:] + points[:1]):
        for i in range(n):
            t = i / n
            out.append((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t))
    return out

def tower():        # tapered; the base sits into the rock
    return polygon(subdivide([(TX - 0.076, 0.93), (TX + 0.076, 0.93),
                              (TX + 0.048, 0.31), (TX - 0.048, 0.31)]))

def lit_face():     # the side that looks left, toward the open sea
    return polygon(subdivide([(TX - 0.066, 0.93), (TX - 0.016, 0.93),
                              (TX - 0.006, 0.31), (TX - 0.038, 0.31)]))   # its outer edge half a brush inside the silhouette

def gallery():      # the walkway plate under the lamp room, wider than the tower
    return [(TX - 0.068, 0.303), (TX + 0.068, 0.303)]

def lantern():      # the glass drum
    return polygon([(TX - 0.045, 0.172), (TX + 0.045, 0.172), (TX + 0.045, 0.298), (TX - 0.045, 0.298)])

def roof():         # a low dome over the glass
    pts = [(TX - 0.054, 0.178)]
    for i in range(1, 8):
        a = math.pi * i / 8
        pts.append((TX - 0.054 * math.cos(a), 0.178 - 0.052 * math.sin(a)))
    pts.append((TX + 0.054, 0.178))
    return polygon(pts)

def halo():         # the lamp's light in the air, on the fog behind the lamp room
    return s.circle((TX, 0.235), 0.10, wobble=0.3, seed=4)

STAIR_TOP, PITCH, TREAD = 0.325, 0.18, 0.02
def stair_point(k, th):         # the k-th turn of the helix at angle th (0 = right side)
    y = STAIR_TOP + k * PITCH + PITCH * th / (2 * math.pi)
    R = r_at(y) + TREAD
    return (TX + R * math.cos(th), y)

def stair_arc(k, th0=-0.55, th1=math.pi + 0.55, n=14):
    # the near-side half of one turn, run a little past both silhouette edges,
    # which is where the far side of the stair peeks out beyond the tower
    return [stair_point(k, th0 + (th1 - th0) * i / n) for i in range(n + 1)]

def pot(x, y, w, h, kind="sprig"):
    # A terracotta pot standing on a tread with its base at (x, y): a short
    # vertical flat stroke for the body (a pot is very nearly a rectangle), a
    # thin flat bar for the rim, the lit side as a narrower stroke laid on the
    # body, and whatever grows in it. Pots on the shadow side of the tower are
    # the same marks a step darker. Vary one thing per pot: `kind`, and the size.
    lit_side = x < TX
    body = "terra" if lit_side else p.at_value("terra", 0.30)
    rim  = "terra_lit" if lit_side else p.at_value("terra", 0.40)
    lit  = "terra_lit" if lit_side else p.at_value("terra", 0.36)
    green = "leaf" if lit_side else p.mix("leaf", "leaf_dark", 0.45)
    if kind == "tipped":            # lying on its side, mouth to the left
        s.stroke([(x - w * 0.7, y - h * 0.5), (x + w * 0.7, y - h * 0.5)], "flat", body, size=h * 0.8,
                 opacity=1.0, load=1.0, load_falloff=0.0, pressure="even", note="subject pot, tipped")
        s.stroke([(x - w * 0.75, y - h * 0.95), (x - w * 0.75, y - h * 0.08)], "flat", rim, size=0.005,
                 opacity=0.95, load=1.0, load_falloff=0.0, pressure="even", note="subject pot rim")
        return
    s.stroke([(x, y - h), (x, y)], "flat", body, size=w, opacity=1.0, load=1.0,
             load_falloff=0.0, pressure="even", jitter=0.01, note="subject pot")
    s.stroke([(x - w * 0.62, y - h), (x + w * 0.62, y - h)], "flat", rim, size=0.005,
             opacity=0.95, load=1.0, load_falloff=0.0, pressure="even", note="subject pot rim")
    s.stroke([(x - w * 0.28, y - h + 0.006), (x - w * 0.28, y - 0.003)], "flat", lit, size=w * 0.36,
             opacity=0.7, load=1.0, load_falloff=0.0, pressure="even", note="subject pot, lit side")
    top = y - h - 0.003
    if kind == "sprig":
        s.stroke([(x - 0.004, top), (x + 0.002, top - 0.011), (x + 0.008, top - 0.007)], "round_hard",
                 green, size=0.006, opacity=0.9, pressure="swell", tip_wobble=0.5, note="subject sprig")
    elif kind == "tall":
        s.stroke([(x + 0.002, top), (x - 0.001, top - 0.018), (x + 0.003, top - 0.034)], "liner",
                 green, size=0.003, opacity=0.9, pressure="even", note="subject stem")
        s.stroke([(x - 0.006, top - 0.026), (x + 0.001, top - 0.032), (x + 0.007, top - 0.024)],
                 "round_hard", green, size=0.007, opacity=0.9, pressure="swell", tip_wobble=0.5,
                 note="subject leaf")
    elif kind == "bushy":
        s.dab(x + 0.001, top - 0.007, "round_hard", green, size=0.017, press=3, tip_wobble=0.7,
              note="subject bush")

# ---------------------------------------------------------------- value plan
PLAN = {
    span("A1", "D2"):                  0.62,   # fog, upper left
    span("G1", "H3"):                  0.64,   # fog, right
    Region(0.02, 0.32, 0.28, 0.50):    0.76,   # the beam, far end
    Region(0.40, 0.215, 0.58, 0.27):   0.79,   # the beam, near the lamp
    span("A5", "C5"):                  0.60,   # far sea, lost in fog
    span("A7", "C8"):                  0.40,   # near sea
    span("F8", "H8"):                  0.18,   # rock, the anchoring dark
    Region(0.618, 0.45, 0.648, 0.80):  0.52,   # tower, lit face
    Region(0.675, 0.45, 0.705, 0.80):  0.34,   # tower, shadow side
}

# ---------------------------------------------------------------- the split
# Written before the first stroke. The picture is the conversion: the lamp room
# full of vines, the green beam, the pots on the stair.
SPLIT = {"fog": 30, "beam": 20, "sea": 25, "rocks": 20, "tower and gallery": 25,
         "lamp room, roof, halo": 40, "stair and pots": 40, "vines and base": 15,
         "edges and finish": 35, "reserve": 50}
