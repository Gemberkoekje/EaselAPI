"""Lighthouse at dusk -- run before every pass: palette, shapes, landmarks, plan."""

p = s.palette

# ---- palette (checked as a swatch strip first) --------------------------------
p["zenith"]   = p.at_value(p.mix("ultramarine", "alizarin", 0.25), 0.34)
p["high"]     = p.at_value(p.mix("ultramarine", "cerulean", 0.5), 0.45)
p["pale"]     = p.at_value(p.mix("cerulean", "titanium_white", 0.7), 0.58)
p["low"]      = p.at_value(p.mix("yellow_ochre", "alizarin", 0.15), 0.66)
p["glow"]     = p.at_value(p.mix("cadmium_yellow", "cadmium_red", 0.35), 0.72)
p["core"]     = p.at_value(p.mix("cadmium_yellow", "titanium_white", 0.7), 0.78)
p["sea_far"]  = p.at_value(p.mix("ultramarine", "burnt_umber", 0.3), 0.44)
p["sea_near"] = p.at_value(p.mix("ultramarine", "burnt_umber", 0.4), 0.26)
p["land"]     = p.at_value(p.mix("burnt_umber", "ultramarine", 0.5), 0.15)
p["grass"]    = p.at_value(p.mix("burnt_umber", "viridian", 0.3), 0.20)
p["lit"]      = p.at_value(p.mix("burnt_sienna", "yellow_ochre", 0.4), 0.30)
p["cliff"]    = p.at_value(p.mix("ultramarine", "burnt_umber", 0.55), 0.19)
p["tower"]    = p.at_value(p.mix("ultramarine", "burnt_umber", 0.4), 0.28)
p["tower_lit"] = p.at_value(p.mix("tower", "burnt_sienna", 0.35), 0.39)
p["rim"]      = p.at_value(p.mix("cadmium_red", "yellow_ochre", 0.5), 0.52)
p["lantern"]  = p.at_value(p.mix("titanium_white", "cadmium_yellow", 0.3), 0.86)
p["lamp"]     = p.at_value(p.mix("titanium_white", "cadmium_yellow", 0.12), 0.93)

# ---- the drawing, in canvas units ---------------------------------------------
HY = 0.585                       # the horizon: eye level, low-ish
TX = 0.700                       # the tower's axis, on the right third

import math, random

def roughen(pts, step=0.010, amp=0.006, seed=0, calm=None):
    """Subdivide an outline and walk it off the line: a silhouette nobody drew.
    calm(x) -> 0..1 scales the wander down (e.g. where something stands on it)."""
    rng = random.Random(seed); out = []; walk = 0.0
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        dx, dy = x1 - x0, y1 - y0
        n = max(1, int(math.hypot(dx / 0.75, dy) / step))
        nx, ny = -dy / 0.75, dx
        nl = math.hypot(nx, ny) or 1.0
        nx, ny = nx / nl, ny / nl
        for i in range(n):
            x, y = x0 + dx * i / n, y0 + dy * i / n
            walk = 0.72 * walk + rng.gauss(0, 1)
            k = amp * walk * (calm(x) if calm else 1.0)
            out.append((x + nx * k * 0.75, y + ny * k))
    out.append(pts[-1])
    return out

TOP = [(0.398, 0.632), (0.425, 0.612), (0.445, 0.598), (0.48, 0.580), (0.52, 0.564),
       (0.56, 0.550), (0.60, 0.540), (0.64, 0.533), (0.68, 0.531), (0.72, 0.531),
       (0.77, 0.528), (0.83, 0.523), (0.89, 0.518), (0.95, 0.513), (1.06, 0.506)]
WATER = [(0.86, 1.06), (0.82, 0.96), (0.77, 0.88), (0.71, 0.815), (0.65, 0.760),
         (0.58, 0.712), (0.52, 0.680), (0.47, 0.660), (0.43, 0.645), (0.398, 0.632)]
seat = lambda x: min(1.0, abs(x - TX) / 0.05)          # calm where the tower stands
headland = polygon(roughen(TOP, amp=0.0045, seed=4, calm=seat)[:-1]
                   + [(1.06, 0.506), (1.06, 1.06)]
                   + roughen(WATER, amp=0.008, seed=9)[:-1], name="headland")
stack_a = blob((0.377, 0.637), 0.012, 0.010, wobble=0.35, seed=5, name="stack_a")
stack_b = blob((0.352, 0.641), 0.006, 0.005, wobble=0.45, seed=11, name="stack_b")

tower = polygon([(TX - 0.020, 0.540), (TX + 0.020, 0.540),
                 (TX + 0.0135, 0.207), (TX - 0.0135, 0.207)], name="tower")
tower_lit_side = polygon([(TX - 0.018, 0.538), (TX - 0.006, 0.538),
                          (TX - 0.0035, 0.209), (TX - 0.0120, 0.209)], name="tower_lit")
lantern = polygon([(TX - 0.010, 0.198), (TX + 0.010, 0.198),
                   (TX + 0.010, 0.158), (TX - 0.010, 0.158)], name="lantern")
cap = polygon([(TX - 0.0135, 0.160), (TX + 0.0135, 0.160), (TX + 0.008, 0.147),
               (TX + 0.0025, 0.139), (TX - 0.0025, 0.139), (TX - 0.008, 0.147)], name="cap")
glow_patch = ellipse((0.19, 0.600), 0.32, 0.17, name="glow")      # centred just under the horizon

sky_upper = polygon([(-0.06, -0.06), (1.06, -0.06), (1.06, 0.44), (-0.06, 0.47)])
sky_lower = polygon([(-0.06, 0.34), (1.06, 0.31), (1.06, 0.62), (-0.06, 0.62)])
sea = polygon([(-0.06, HY), (1.06, HY), (1.06, 1.06), (-0.06, 1.06)], name="sea")

LAMP = (TX, 0.178)

for name, (x, y) in {"lamp": LAMP, "base": (TX, 0.536), "glow": (0.19, HY),
                     "tip": (0.398, 0.632)}.items():
    s.mark(name, x, y)

# ---- what this painting is for ------------------------------------------------
s.plan(
    why=("At dusk the sun's glow is going out low on the left while the lamp comes on "
         "at the right: two warm lights handing over, and the small made one has to win."),
    values={lantern: 0.86,
            ellipse((0.19, 0.555), 0.13, 0.028): 0.72,      # the glow's core, above the horizon
            Region(0.0, 0.0, 1.0, 0.16): 0.36,              # the top of the sky
            Region(0.80, 0.26, 1.0, 0.44): 0.50,            # the sky behind the tower's right
            Region(0.0, 0.74, 0.34, 1.0): 0.32,             # the near sea
            polygon([(0.62, 0.60), (0.95, 0.58), (0.98, 0.95), (0.80, 0.93), (0.66, 0.74)]): 0.16,
            tower: 0.29},
    lightest=lantern,
    subject_share=0.25,
    bands="subject",            # a dusk sea: the horizontals are the subject's own
    ground="buried",            # sky and sea are continuous fields; no ground between them
)

# ---- the headland's planes, drawn with its silhouette: tiles, not slabs ------------
TOP_EDGE = ((0.40, 0.632), (1.0, 0.510))           # the line the rock's strata run along
p["lit_dim"] = p.at_value(p.mix("land", "burnt_sienna", 0.5), 0.23)   # west face, glow-lit
p["cliff"]   = p.at_value(p.mix("ultramarine", "burnt_umber", 0.55), 0.18)
p["lit"]     = p.at_value(p.mix("lit_dim", "glow", 0.25), 0.30)
west_face = polygon([(0.414, 0.627), (0.447, 0.604), (0.49, 0.585), (0.54, 0.568),
                     (0.595, 0.552), (0.64, 0.541), (0.68, 0.537), (0.66, 0.557),
                     (0.62, 0.573), (0.56, 0.597), (0.50, 0.622), (0.45, 0.640),
                     (0.425, 0.640)], name="west_face")
front_face = polygon([(0.455, 0.648), (0.50, 0.630), (0.56, 0.605), (0.62, 0.580),
                      (0.665, 0.563), (0.72, 0.551), (0.80, 0.547), (0.90, 0.542),
                      (1.06, 0.537), (1.06, 0.66), (0.93, 0.71), (0.83, 0.765),
                      (0.76, 0.80), (0.70, 0.79), (0.64, 0.748), (0.58, 0.705),
                      (0.52, 0.674), (0.47, 0.657)], name="front_face")

def headland_mass():
    s.block_in(headland, "flat", "land", size=0.07, density=1.0, solid=True,
               direction=TOP_EDGE, edge="hard")

def headland_planes():
    s.block_in(front_face, "flat", "cliff", size=0.03, density=1.0, solid=True,
               direction=((0.47, 0.657), (0.76, 0.80)), edge="clean", opacity=1.0,
               pressure="even", clip=headland)                   # grain along the waterline
    s.block_in(west_face, "flat", "lit_dim", size=0.014, density=1.0, solid=True,
               direction=((0.414, 0.627), (0.68, 0.537)), edge="clean", opacity=1.0,
               pressure="even", clip=headland)
    s.stroke([(0.588, 0.551), (0.66, 0.539), (0.74, 0.537), (0.84, 0.530), (0.95, 0.522),
              (1.06, 0.515)], "flat", "grass", size=0.013, opacity=0.9, load=1.0,
             load_falloff=0.0, pressure="even", jitter=0.01, size_jitter=0.03,
             clip=headland)                                      # the grass, one stroke
