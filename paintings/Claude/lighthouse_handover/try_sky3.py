import sys, os, random; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import run_variants
from easel import polygon, Region

top = polygon([(-0.06, -0.06), (1.06, -0.06), (1.06, 0.27), (-0.06, 0.29)])
mid = polygon([(-0.06, 0.17), (1.06, 0.15), (1.06, 0.45), (-0.06, 0.47)])
low = polygon([(-0.06, 0.35), (1.06, 0.33), (1.06, 0.62), (-0.06, 0.62)])
KW = dict(opacity=0.95, jitter=0.01, size_jitter=0.03)

def ramps(c, p, bottom):
    c.scumble(top, "zenith", "high", 8, direction=3, **KW)
    c.scumble(mid, "high", "pale", 8, direction=-2, **KW)
    c.scumble(low, "pale", bottom, 8, direction=2, **KW)

def warm_left(c, p, seed=3):
    rng = random.Random(seed)
    ys = [0.468, 0.487, 0.509, 0.528, 0.551, 0.572]
    for i, y in enumerate(ys):
        t = i / (len(ys) - 1)
        x_end = 0.50 + 0.2 * t + rng.uniform(-0.05, 0.05)
        c.stroke([(-0.06, y + rng.uniform(-0.004, 0.004)), (0.28, y - 0.003), (x_end, y + 0.004)],
                 "flat", p.mix("low2", "glow", 0.25 + 0.75 * t), size=0.058 + rng.uniform(-0.006, 0.006),
                 opacity=0.5, load=1.0, load_falloff=0.0, pressure=[1.0, 0.6, 0.0],
                 jitter=0.01, size_jitter=0.03)

def afterglow(c, p, k=1.0):
    c.dry()
    field = c.sample(Region(0.05, 0.53, 0.35, 0.58)); v = p.value_of(field)
    p["air_far"]  = p.at_value(p.mix(field, "glow", 0.5), min(v + 0.05, 0.9))
    p["air_body"] = p.at_value(p.mix("core", field, 0.35), min(v + 0.09, 0.9))
    p["air_core"] = p.at_value(p.mix("core", field, 0.25), min(v + 0.13, 0.9))
    c.glaze([(-0.08, 0.560), (0.19, 0.550), (0.66, 0.566)], "air_far", opacity=0.10 * k, size=0.26,
            pressure=[0.6, 1.0, 0.3])
    c.glaze([(-0.08, 0.572), (0.19, 0.566), (0.50, 0.576)], "air_body", opacity=0.15 * k, size=0.12,
            pressure=[0.5, 1.0, 0.25])
    c.glaze([(0.03, 0.580), (0.19, 0.577), (0.34, 0.581)], "air_core", opacity=0.18 * k, size=0.05,
            pressure=[0.3, 1.0, 0.2])
    c.dry()
    print("  glow field", round(v, 3), "-> core", round(p.value_of(c.sample(Region(0.12, 0.55, 0.26, 0.58))), 3),
          "| right horizon", round(p.value_of(c.sample(Region(0.80, 0.45, 0.95, 0.50))), 3))

def colours(p):
    p["low2"] = p.at_value(p.mix("cadmium_red", "yellow_ochre", 0.6), 0.66)
    p["low_cool"] = p.at_value(p.mix("alizarin", "yellow_ochre", 0.6), 0.64)

def vB(c, p, ns):   # cool rose horizon everywhere, warmth laid in from the left, then glazes
    colours(p); ramps(c, p, "low_cool"); warm_left(c, p); afterglow(c, p)
def vC(c, p, ns):   # peach horizon everywhere, glazes only
    colours(p); ramps(c, p, "low2"); afterglow(c, p, k=1.3)
paths = run_variants("sky3", [("B", vB), ("C", vC)])
