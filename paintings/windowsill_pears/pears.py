import math
ASPECT = 1024 / 768

def pear_outline(cx, cy, R, r, lean=0.0, angle=0.0, n=14, m=8):
    """Outline of a pear: a big lobe (radius R, centre cx,cy) and a small lobe (radius r)
    stacked above it, joined by a waist. Sizes in fractions of the width; y is scaled
    so the lobes are round. angle rotates the whole pear (clockwise degrees); -90 lays it
    on its side with the neck to the left."""
    pts = []
    for i in range(n):                      # the big lobe, sweeping through its bottom
        t = math.radians(-25 + 250 * i / (n - 1))
        pts.append((R * math.cos(t), R * math.sin(t)))
    cy_top = -(R + r * 1.15)
    for i in range(m):                      # the small lobe, sweeping over its top
        t = math.radians(200 + 140 * i / (m - 1))
        pts.append((lean + r * math.cos(t), cy_top + r * math.sin(t)))
    a = math.radians(angle)
    out = []
    for x, y in pts:
        xr = x * math.cos(a) - y * math.sin(a)
        yr = x * math.sin(a) + y * math.cos(a)
        out.append((cx + xr, cy + yr * ASPECT))
    return out

def pear_top(cx, cy, R, r, lean=0.0, angle=0.0):
    """Where the stem leaves the pear, in canvas coordinates."""
    x, y = lean, -(R + r * 1.15) - r
    a = math.radians(angle)
    xr = x * math.cos(a) - y * math.sin(a)
    yr = x * math.sin(a) + y * math.cos(a)
    return (cx + xr, cy + yr * ASPECT)

PEARS = {
    "pear1": dict(cx=0.33,  cy=0.565, R=0.068, r=0.031, lean=0.012, angle=4),
    "pear2": dict(cx=0.488, cy=0.60,  R=0.060, r=0.028, lean=-0.010, angle=-6),
    "pear3": dict(cx=0.44,  cy=0.70,  R=0.052, r=0.026, lean=0.0,   angle=-90),
}
SHAPES = {k: polygon(pear_outline(**v)) for k, v in PEARS.items()}
TOPS = {k: pear_top(**v) for k, v in PEARS.items()}

def pear_point(params, deg, frac, lobe="big"):
    """Canvas point at angle `deg` (y-down: 90 is the bottom, 270 the top) and `frac` of the
    lobe's radius from its centre, after the pear's own rotation."""
    R, r, lean, angle = params["R"], params["r"], params["lean"], params["angle"]
    t = math.radians(deg)
    if lobe == "big":
        x, y = frac * R * math.cos(t), frac * R * math.sin(t)
    else:
        x, y = lean + frac * r * math.cos(t), -(R + r * 1.15) + frac * r * math.sin(t)
    a = math.radians(angle)
    xr = x * math.cos(a) - y * math.sin(a)
    yr = x * math.sin(a) + y * math.cos(a)
    return (params["cx"] + xr, params["cy"] + yr * ASPECT)

def paint_pear(name, size=0.02):
    prm, shp = PEARS[name], SHAPES[name]
    pp = lambda deg, frac, lobe="big": pear_point(prm, deg, frac, lobe)
    s.block_in(shp, "round_hard", "pear_mid", density=1.0, size=size, direction="axis",
               pressure="even", load=1.0, note=f"{name} mass")
    # shadow side: away from the window, so the right and underneath
    s.stroke([pp(-20, 0.72), pp(20, 0.74), pp(60, 0.72), pp(100, 0.70)], "round_hard",
             "pear_shadow", size=0.034, pressure=[0.5, 1.0, 1.0, 0.7], load=1.0,
             note=f"{name} shadow, big lobe")
    s.stroke([pp(-40, 0.55, "small"), pp(0, 0.6, "small"), pp(40, 0.55, "small"), pp(-35, 0.85)],
             "round_hard", "pear_shadow", size=0.018, pressure=[0.4, 1.0, 0.9, 0.5], load=1.0,
             note=f"{name} shadow, neck")
    # lit side: the left shoulder up into the neck
    s.stroke([pp(160, 0.72), pp(200, 0.74), pp(240, 0.72), pp(200, 0.55, "small"), pp(240, 0.5, "small")],
             "round_hard", "pear_lit", size=0.022, pressure=[0.25, 0.9, 1.0, 0.7, 0.3], load=1.0,
             note=f"{name} light")

UPRIGHT = dict(rim_big=[165, 200, 235], rim_small=[205, 245, 275], reflect=[25, 60, 95, 125])
LYING   = dict(rim_big=[70, 40, 10, 340], rim_small=[20, -20, -60], reflect=[130, 170, 210])

def pear_plan(name, body="pear_body", size=0.02, angles=None):
    """The pear as a contre-jour form: a body in shadow with its outline smoothed by one
    sweep, warm reflected light on the side toward the sill (soft brush), and a narrow
    lit rim on the contour facing the window. Angles are in the pear's own frame."""
    prm, shp = PEARS[name], SHAPES[name]
    ang = angles or (LYING if prm["angle"] < -45 else UPRIGHT)
    pp = lambda deg, frac, lobe="big": pear_point(prm, deg, frac, lobe)
    rim = [pp(d, 0.95) for d in ang["rim_big"]] + [pp(d, 0.9 - 0.03 * i, "small")
                                                   for i, d in enumerate(ang["rim_small"])]
    n = len(rim)
    rim_pressure = [0.2] + [0.85] * (n - 3) + [0.6, 0.25] if n > 3 else [0.3, 1.0, 0.3]
    refl = [pp(d, 0.62) for d in ang["reflect"]]
    return [
        {"shape": shp, "brush": "round_hard", "color": body, "density": 1.0, "size": size,
         "direction": "axis", "pressure": "even", "load": 1.0, "jitter": 0.0,
         "label": f"{name} body"},
        {"edge": shp, "brush": "round_hard", "color": body, "depth": 0.012, "passes": 1,
         "size": 0.018, "pressure": "even", "load": 1.0, "jitter": 0.0,
         "label": f"{name} outline"},
        {"points": refl, "brush": "round_soft", "color": "pear_reflect", "size": 0.036,
         "pressure": [0.3] + [1.0] * (len(refl) - 2) + [0.4], "load": 1.0, "opacity": 0.55,
         "label": f"{name} reflected light"},
        {"points": rim, "brush": "round_hard", "color": "pear_rim", "size": 0.013,
         "pressure": rim_pressure, "load": 1.0, "label": f"{name} lit rim"},
    ]

def run_plan(plan):
    for spec in plan:
        spec = {k: v for k, v in spec.items() if k != "label"}
        if "shape" in spec:
            s.block_in(spec.pop("shape"), **spec)
        elif "edge" in spec:
            s.sweep(spec.pop("edge"), **spec)
        else:
            s.stroke(spec.pop("points"), **spec)

def stem_plan(name):
    top = TOPS[name]
    prm = PEARS[name]
    if prm["angle"] < -45:      # lying: the stem points left and a little up
        pts = [top, (top[0] - 0.02, top[1] - 0.006), (top[0] - 0.038, top[1] - 0.016)]
    else:
        pts = [top, (top[0] + 0.006, top[1] - 0.02), (top[0] + 0.004, top[1] - 0.04)]
    return {"points": pts, "brush": "liner", "color": "dark", "size": 0.006,
            "pressure": [1.0, 0.8, 0.5], "load": 1.0, "label": f"{name} stem"}
