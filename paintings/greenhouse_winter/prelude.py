# Shared by every pass: the geometry of the greenhouse in metres through one
# perspective helper, the palette mixed to planned values, every mass as a
# function so the stack can be re-run in depth order, and the split.
import math
p = s.palette

# ---------------------------------------------------------------- perspective
# Camera on the centre line of the aisle, low: eye 1.0 m, at the height of the
# pot rims, so the pots stand against the glass instead of against the staging.
VX, VY, F = 0.36, 0.42, 0.8         # vanishing point; 1 m = F/depth of the width
A = s.aspect                        # y is normalised over the short side
E = 1.55                            # eye height, metres above the floor: standing
XC = 0.15                           # the camera stands this far right of the centre line

def P(xm, hm, dm):
    """Screen point for a place xm metres right of the centre line, hm above the
    floor, dm metres away."""
    return (VX + (xm - XC) * F / dm, VY - (hm - E) * F * A / dm)

HALF, BASE, EAVES, RIDGE = 1.4, 0.6, 2.1, 3.3      # the house: half-width, brick plinth, eaves, ridge
BENCH, BF, BB = 0.85, 0.5, 1.35                    # staging: height, front edge, back edge (xm)
NEAR, FARB, FAR = 1.2, 4.2, 4.6                    # the staging runs NEAR..FARB; the end wall at FAR

# ---------------------------------------------------------------- the masses
def far_glass():      # the end wall glass, gable included
    return polygon([P(-HALF, BASE, FAR), P(-HALF, EAVES, FAR), P(0, RIDGE, FAR),
                    P(HALF, EAVES, FAR), P(HALF, BASE, FAR)])
def base_wall():      # the brick plinth under it
    return polygon([P(-HALF, 0, FAR), P(-HALF, BASE, FAR), P(HALF, BASE, FAR), P(HALF, 0, FAR)])
# The side walls, roof and floor are clipped near the frame: a pass laid off the
# canvas still costs a stroke.
def right_wall():
    return polygon([P(HALF, BASE, FAR), P(HALF, EAVES, FAR), P(HALF, EAVES, 1.35), P(HALF, BASE, 1.35)])
def left_wall():
    return polygon([P(-HALF, BASE, FAR), P(-HALF, EAVES, FAR), P(-HALF, EAVES, 2.8), P(-HALF, BASE, 2.8)])
def right_roof():      # the wedge between the right eaves line and the top of the frame
    return polygon([P(0, RIDGE, FAR), P(HALF, EAVES, FAR), P(HALF, EAVES, 1.5), (1.06, -0.06), (P(0, RIDGE, FAR)[0], -0.06)])
def left_roof():
    return polygon([P(0, RIDGE, FAR), P(-HALF, EAVES, FAR), P(-HALF, EAVES, 2.7), (-0.06, -0.06), (P(0, RIDGE, FAR)[0], -0.06)])
def floor():
    return polygon([P(-HALF, 0, FAR), P(HALF, 0, FAR), (1.06, 1.06), (-0.06, 1.06)])
def bench_top(side):  # side = +1 right, -1 left
    return polygon([P(side * BF, BENCH, NEAR), P(side * BB, BENCH, NEAR),
                    P(side * BB, BENCH, FARB), P(side * BF, BENCH, FARB)])
def bench_front(side):   # the vertical plane under the front edge: shadow, legs, stores
    return polygon([P(side * BF, BENCH, NEAR), P(side * BF, BENCH, FARB),
                    P(side * BF, 0, FARB), P(side * BF, 0, NEAR)])
def bench_end(side):     # the far end face of the staging
    return polygon([P(side * BF, BENCH, FARB), P(side * BB, BENCH, FARB),
                    P(side * BB, 0, FARB), P(side * BF, 0, FARB)])

def clip_below(points, ymax=1.06):
    """Cut a polygon off at y = ymax, so passes are not laid below the frame."""
    out = []
    n = len(points)
    for i in range(n):
        (x0, y0), (x1, y1) = points[i], points[(i + 1) % n]
        in0, in1 = y0 <= ymax, y1 <= ymax
        if in0:
            out.append((x0, y0))
        if in0 != in1:
            t = (ymax - y0) / (y1 - y0)
            out.append((x0 + (x1 - x0) * t, ymax))
    return out

def under_bench(side):   # the dark under the staging: its far end face and the face under its front edge
    b = side * BF
    top = BENCH - 0.12   # a hair below the bench top, so the brush's overhang stays under it
    return polygon(clip_below([P(b, top, NEAR), P(b, top, FARB), P(side * BB, top, FARB),
                               P(side * BB, 0, FARB), P(b, 0, FARB), P(b, 0, NEAR)]))
def at_x(a, b, x):       # the point on segment a-b at that x
    t = (x - a[0]) / (b[0] - a[0])
    return (x, a[1] + (b[1] - a[1]) * t)

def left_top():          # the left bench top, cut at the left edge of the frame
    front_far, front_near = P(-BF, BENCH, FARB), P(-BF, BENCH, NEAR)
    back_far, back_near = P(-BB, BENCH, FARB), P(-BB, BENCH, NEAR)
    return polygon([front_far, at_x(front_far, front_near, -0.06),
                    at_x(back_far, back_near, -0.06), back_far])

def aisle():             # the floor between the two benches, widened under them
    return polygon([(0.18, 0.77), (0.47, 0.77), (0.64, 1.06), (0.02, 1.06)])

def shadow_dir(base):    # cast shadows on a plane run away from the sun's own place on the screen
    dx, dy = base[0] - SUN[0], base[1] - SUN[1]
    L = math.hypot(dx, dy)
    return dx / L, dy / L

SUN = (0.30, 0.33)       # where the sun sits behind the fogged end wall
def bloom(r=0.13):
    return s.circle(SUN, r, wobble=0.18, seed=5)

def pot_geo(xm, dm, w, h, lean=0.0):
    """A pot standing on the staging, seen from above its rim: the body trapezoid,
    the rim ellipse (its far arc is the top of the silhouette), the opening inside
    it, and the near arc of the rim, which is the edge that catches the light."""
    bx, by = P(xm, BENCH, dm)
    cx, cy = P(xm, BENCH + h, dm)
    sx = F / dm
    rx = w / 2 * sx * 1.06
    cx += lean * rx
    y_near = P(xm, BENCH + h, dm - w / 2)[1]
    y_far = P(xm, BENCH + h, dm + w / 2)[1]
    ry = (y_near - y_far) / 2
    bw = 0.7 * w / 2 * sx
    body = polygon([(bx - bw, by), (bx + bw, by), (cx + rx, cy), (cx - rx, cy)])
    rim = ellipse((cx, cy), rx, ry)
    opening = ellipse((cx, cy), rx * 0.86, ry * 0.72)
    arc = [(cx + rx * math.cos(math.radians(a)), cy + ry * math.sin(math.radians(a)))
           for a in (10, 40, 70, 90, 110, 140, 170)]     # the near, lower half of the rim
    return dict(body=body, rim=rim, opening=opening, arc=arc, top=(cx, cy),
                rx=rx, ry=ry, base=(bx, by))

def tipped_geo(xm, dm, w, h):
    """A pot lying on its side on the staging, mouth toward the aisle and the viewer."""
    R = w / 2
    base_c = P(xm + 0.09, BENCH + R * 0.9, dm + 0.12)
    mouth_c = P(xm - 0.05, BENCH + R, dm - 0.06)
    rb = 0.72 * R * F / (dm + 0.12)
    rm = R * F / (dm - 0.06)
    body = polygon([(mouth_c[0] - rm, mouth_c[1] - rm * A), (mouth_c[0] + rm, mouth_c[1] - rm * A),
                    (base_c[0] + rb, base_c[1] - rb * A), (base_c[0] + rb, base_c[1] + rb * A),
                    (mouth_c[0] + rm, mouth_c[1] + rm * A), (mouth_c[0] - rm, mouth_c[1] + rm * A)])
    mouth = ellipse(mouth_c, rm * 0.8, rm * A * 0.92)
    return dict(body=body, mouth=mouth, mouth_c=mouth_c, base_c=base_c, rm=rm)

def pot(xm, dm, w, h, kind="empty", lean=0.0, chip=False, note="subject pot"):
    """Paint one standing pot, backlit: the body dark, the rim's far arc closing
    the silhouette, the opening darker, then the near arc of the rim catching the
    light, hottest on the sun side. Small far pots get three marks; near ones
    get the lit sliver down the sun side and a bounce from the bench too."""
    g = pot_geo(xm, dm, w, h, lean)
    cx, cy = g["top"]
    rx, ry = g["rx"], g["ry"]
    bx, by = g["base"]
    sw = w * F / dm
    lit = -1 if cx > SUN[0] else 1            # the side the sun rakes
    big, mid = sw > 0.085, sw > 0.045
    bw = 0.66 * rx                            # the base's half-width
    top_y = cy + ry * 0.3
    # the body: one to three vertical chisel strokes that converge with the taper
    cols, size = ((-0.62, 0.0, 0.62), sw * 0.36) if big else ((-0.45, 0.45), sw * 0.55) if mid else ((0.0,), sw * 0.9)
    for c in cols:
        s.stroke([(cx + c * rx, top_y), (bx + c * bw, by - 0.002)], "flat", "terra", size=size,
                 opacity=1.0, load=1.0, load_falloff=0.0, pressure="even", jitter=0.01, note=note)
    # the rim: one capsule along the ellipse, closing the silhouette at the top
    ex = max(0.0, rx - 0.75 * ry)
    if mid:
        s.stroke([(cx - ex, cy), (cx + ex, cy)], "round_hard", "terra", size=1.5 * ry, opacity=1.0,
                 load=1.0, load_falloff=0.0, pressure="even", note=note)
    # the opening, darker
    s.stroke([(cx - rx * 0.62, cy), (cx + rx * 0.62, cy)], "round_hard", "terra_dk",
             size=max(0.004, 1.5 * ry * 0.7), opacity=0.95, load=1.0, load_falloff=0.0,
             pressure="even", note=note)
    # the near arc of the rim catching the light, one tapered stroke
    arc = g["arc"] if lit < 0 else g["arc"][::-1]
    prof = [0.15, 0.6, 1.0, 0.8, 0.5, 0.3, 0.1]
    if chip:                                  # a bite out of the near rim
        arc, prof = arc[:3] + arc[4:], prof[:3] + prof[4:]
    s.stroke(arc, "round_hard", "terra_lit", size=max(0.004, ry * 0.55), opacity=0.9,
             load=1.0, load_falloff=0.0, pressure=prof, note=note)
    if mid:
        s.stroke(arc[1:4], "round_hard", "terra_edge", size=max(0.004, ry * 0.4), opacity=0.9,
                 pressure=[0.3, 1.0, 0.2], note=note)
        s.stroke([(cx + lit * rx * 0.9, cy + ry * 0.8), (bx + lit * bw * 0.95, by - 0.004)],
                 "round_hard", "terra_lit", size=max(0.004, sw * 0.05), opacity=0.7,
                 pressure=[0.9, 0.45, 0.1], note=note)
    if big:
        s.stroke([(cx - lit * rx * 0.85, cy + ry * 1.5), (bx - lit * bw * 0.85, by - 0.006)],
                 "round_soft", p.at_value("terra", 0.43), size=sw * 0.1, opacity=0.4,
                 pressure=[0.2, 0.8, 0.4], note=note)
    return g

def foliage(g, dm, scale=1.0, note="subject leaves"):
    """What is still green in a pot: a dark mass over the rim, mid leaves, then a
    few lit through by the sun on its side."""
    cx, cy = g["top"]
    rx = g["rx"]
    lit = -1 if cx > SUN[0] else 1
    r = rx * 1.1 * scale
    top = cy - r * A * 0.85
    # the dark mass as two clots, so its silhouette is nobody's disc
    s.dab(cx + lit * r * 0.15, top, "round_hard", "leaf_dk", size=r * 1.9, press=3,
          tip_wobble=0.7, note=note)
    s.dab(cx - lit * r * 0.35, top + r * A * 0.35, "round_hard", "leaf_dk", size=r * 1.5, press=3,
          tip_wobble=0.7, note=note)
    s.stroke([(cx - r * 0.5, top + r * A * 0.4), (cx + r * 0.2, top - r * A * 0.3)], "round_hard",
             "leaf", size=max(0.005, r * 0.4), opacity=0.9, pressure="swell", tip_wobble=0.5, note=note)
    for ax, ay, bx_, by_ in ((lit * 0.85, 0.0, lit * 0.3, -0.55), (lit * 0.2, 0.6, lit * 0.75, 0.25)):
        s.stroke([(cx + ax * r, top + ay * r * A), (cx + bx_ * r, top + by_ * r * A)], "round_hard",
                 "leaf_lit", size=max(0.004, r * 0.3), opacity=0.9, pressure="swell",
                 tip_wobble=0.5, note=note)

def stalks(g, dm, n=3, note="subject stalks"):
    """Dry stalks left standing in a pot: a few pale lines, no two the same height."""
    cx, cy = g["top"]
    rx = g["rx"]
    for k in range(n):
        x0 = cx + rx * (-0.5 + k * 0.5)
        hh = rx * A * (1.6 + 0.7 * ((k * 7) % 3))
        bend = rx * 0.3 * (1 if k % 2 else -1)
        s.stroke([(x0, cy - 0.002), (x0 + bend * 0.4, cy - hh * 0.55), (x0 + bend, cy - hh)], "liner",
                 "stalk", size=0.0035, opacity=0.85, pressure="lift_off", note=note)
    s.dab(cx + rx * 0.5 + bend * 0.6, cy - hh * 0.98, "round_hard", "stalk", size=0.006, press=2,
          tip_wobble=0.7, note=note)

def tipped(xm, dm, w, h, note="subject pot tipped"):
    """A pot on its side: the body, the dark mouth, and the lit near rim of it."""
    g = tipped_geo(xm, dm, w, h)
    mx, my = g["mouth_c"]
    rm = g["rm"]
    s.stroke([g["base_c"], (mx, my)], "flat", "terra", size=rm * 1.9, opacity=1.0, load=1.0,
             load_falloff=0.0, pressure="even", note=note)
    s.dab(mx, my, "round_hard", "terra_dk", size=rm * 1.6, press=3, tip_wobble=0.2, note=note)
    arc = [(mx + rm * 0.8 * math.cos(math.radians(a)), my + rm * A * 0.92 * math.sin(math.radians(a)))
           for a in (150, 120, 90, 60, 30)]
    s.stroke(arc, "round_hard", "terra_lit", size=max(0.004, rm * 0.25), opacity=0.9,
             pressure=[0.1, 0.7, 1.0, 0.6, 0.1], note=note)
    return g

# front row on the right staging (xm 0.65), back row (xm 1.15); the left staging (xm -0.65)
XR, XRB, XL = 0.65, 1.15, -0.65
RIGHT_FRONT = [  # dm, width, height, kind
    (1.5, 0.26, 0.24, "empty"), (2.0, 0.16, 0.15, "green"), (2.55, 0.15, 0.14, "stalks"),
    (3.1, 0.19, 0.17, "tipped"), (3.7, 0.13, 0.12, "green"), (4.15, 0.16, 0.15, "empty")]
RIGHT_BACK = [(1.35, 0.22, 0.20, "empty"), (1.8, 0.20, 0.18, "empty"),
              (2.6, 0.16, 0.15, "stalks"), (3.5, 0.18, 0.17, "empty")]
LEFT_FRONT = [(2.2, 0.15, 0.14, "stalks"), (2.9, 0.18, 0.17, "green"), (3.8, 0.13, 0.12, "empty")]

CAN = dict(xm=-0.25, dm=3.3, w=0.24, h=0.36)     # the watering can, on the aisle floor
def can_geo():
    c = CAN
    bx, by = P(c["xm"], 0, c["dm"])
    sx, sy = F / c["dm"], F * A / c["dm"]
    hw = c["w"] * sx / 2
    top = by - c["h"] * sy
    body = polygon([(bx - hw, by), (bx + hw, by), (bx + hw * 0.92, top), (bx - hw * 0.92, top)])
    return body, (bx, top), hw, sy

# glazing bars, as point lists
PITCH = 0.6
def wall_verticals(side):
    out = []
    d = 1.4
    while d < FAR:
        out.append([P(side * HALF, BASE, d), P(side * HALF, EAVES, d)])
        d += PITCH
    return out
def wall_transom(side, h=1.35):
    return [P(side * HALF, h, 1.0), P(side * HALF, h, FAR)]
def far_verticals():
    out = []
    for xm in (-0.93, -0.47, 0.0, 0.47, 0.93):
        top = RIDGE - (RIDGE - EAVES) * abs(xm) / HALF     # up to the gable roof line
        out.append([P(xm, BASE, FAR), P(xm, top, FAR)])
    return out
def far_transoms():
    return [[P(-HALF, 1.35, FAR), P(HALF, 1.35, FAR)], [P(-HALF, EAVES, FAR), P(HALF, EAVES, FAR)]]
def gable():
    return [P(-HALF, EAVES, FAR), P(0, RIDGE, FAR), P(HALF, EAVES, FAR)]
def rafters(side):
    out = []
    d = 2.6
    while d < FAR:
        out.append([P(side * HALF, EAVES, d), P(0, RIDGE, d)])
        d += PITCH
    return out

# ---------------------------------------------------------------- the palette
def V(base, target, name=None):
    c = p.at_value(base, target)
    if name:
        print(f"  {name:10s} {p.hex(c)}  v={p.value_of(c):.2f}  chroma {p.chroma_of(c):.3f}  (asked {target:.2f})")
    return c

def mixtures(verbose=False):
    n = (lambda k: k) if verbose else (lambda k: None)
    dark   = p.mix("ultramarine", "burnt_umber", 0.5)
    warmgr = p.desaturate(p.mix("yellow_ochre", "cadmium_red", 0.12), 0.50)  # a warm buff grey
    coolgr = p.desaturate(p.mix("cerulean", "burnt_umber", 0.40), 0.30)    # grey-blue
    wood   = p.desaturate(p.mix("burnt_umber", "yellow_ochre", 0.45), 0.20)
    terra  = p.mix("burnt_sienna", "cadmium_red", 0.30)
    p["glass_far"]  = V(warmgr, 0.75, n("glass_far"))       # the lit end wall, fogged
    p["glass_low"]  = V(p.mix(warmgr, "viridian", 0.15), 0.64, n("glass_low"))   # its dirty bottom panes
    p["glass_left"] = V(p.mix(warmgr, coolgr, 0.5), 0.64, n("glass_left"))
    p["glass_right"]= V(coolgr, 0.58, n("glass_right"))
    p["roof"]       = V(coolgr, 0.62, n("roof"))
    p["bloom_mid"]  = V(p.mix("yellow_ochre", "titanium_white", 0.6), 0.85, n("bloom_mid"))
    p["bloom_core"] = V(p.mix(p.mix("cadmium_yellow", "yellow_ochre", 0.4), "titanium_white", 0.8), 0.93, n("bloom_core"))
    p["bar"]        = V(p.mix("burnt_umber", "ultramarine", 0.35), 0.28, n("bar"))
    p["bar_lit"]    = V(p.mix("burnt_umber", "yellow_ochre", 0.5), 0.52, n("bar_lit"))
    p["wood"]       = V(wood, 0.48, n("wood"))
    p["wood_lit"]   = V(p.mix(wood, "yellow_ochre", 0.3), 0.62, n("wood_lit"))
    p["under"]      = V(dark, 0.18, n("under"))
    p["floor"]      = V(p.mix(p.mix("burnt_umber", "ultramarine", 0.3), "burnt_sienna", 0.2), 0.31, n("floor"))
    p["floor_far"]  = V(p.mix("burnt_umber", "yellow_ochre", 0.4), 0.41, n("floor_far"))
    p["brick"]      = V(p.mix("burnt_sienna", "burnt_umber", 0.5), 0.34, n("brick"))
    p["terra"]      = V(terra, 0.36, n("terra"))
    p["terra_dk"]   = V(p.mix(terra, dark, 0.3), 0.27, n("terra_dk"))
    p["terra_lit"]  = V(p.mix(terra, "yellow_ochre", 0.4), 0.56, n("terra_lit"))
    p["terra_edge"] = V(p.mix(terra, "yellow_ochre", 0.6), 0.70, n("terra_edge"))
    p["leaf_dk"]    = V(p.mix("viridian", "burnt_umber", 0.4), 0.24, n("leaf_dk"))
    p["leaf"]       = V(p.mix("viridian", "cadmium_yellow", 0.35), 0.38, n("leaf"))
    p["leaf_lit"]   = V(p.mix(p.mix("lemon_yellow", "viridian", 0.30), warmgr, 0.35), 0.68, n("leaf_lit"))
    p["stalk"]      = V(p.mix("yellow_ochre", "burnt_umber", 0.25), 0.62, n("stalk"))
    p["zinc"]       = V(p.desaturate(p.mix("cerulean", "burnt_umber", 0.5), 0.2), 0.46, n("zinc"))
    p["zinc_dk"]    = V(p.mix(coolgr, dark, 0.4), 0.30, n("zinc_dk"))
    p["zinc_hi"]    = V(p.mix("titanium_white", "yellow_ochre", 0.08), 0.92, n("zinc_hi"))
    p["dark"]       = V(dark, 0.15, n("dark"))
mixtures()

# ---------------------------------------------------------------- value plan
PLAN = {
    Region(0.30, 0.28, 0.36, 0.36):            0.90,   # the core of the bloom
    Region(0.44, 0.16, 0.55, 0.40):            0.75,   # the end wall glass, right of the sun
    Region(0.72, 0.12, 0.96, 0.38):            0.58,   # the right wall glass
    Region(0.02, 0.14, 0.14, 0.38):            0.64,   # the left wall glass
    Region(0.45, 0.85, 0.53, 0.98):            0.18,   # under the right staging
    Region(0.22, 0.90, 0.42, 0.98):            0.31,   # the aisle floor, near
    Region(0.26, 0.78, 0.38, 0.84):            0.41,   # the aisle floor, far
    Region(0.24, 0.83, 0.285, 0.90):           0.46,   # the watering can
    Region(0.60, 0.72, 0.66, 0.78):            0.62,   # the lit bench top, right
}

# ---------------------------------------------------------------- the split
# The picture is the light through the glass and what it does to the pots.
SPLIT = {"glass masses": 45, "bloom and glazes": 18, "glazing bars": 28,
         "floor, plinth, under-bench": 30, "staging": 22, "pots right": 55,
         "pots left": 22, "watering can": 12, "drips, dirt on the glass": 15,
         "edges and finish": 25, "reserve": 28}
