import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import run_variants
from easel import polygon, Region

top = polygon([(-0.06, -0.06), (1.06, -0.06), (1.06, 0.27), (-0.06, 0.29)])
mid = polygon([(-0.06, 0.17), (1.06, 0.15), (1.06, 0.45), (-0.06, 0.47)])
low = polygon([(-0.06, 0.35), (1.06, 0.33), (1.06, 0.62), (-0.06, 0.62)])
warm = polygon([(-0.06, 0.46), (1.06, 0.44), (1.06, 0.62), (-0.06, 0.62)])

def ramps(c, p):
    p["low2"] = p.at_value(p.mix("cadmium_red", "yellow_ochre", 0.6), 0.66)
    c.scumble(top, "zenith", "high", 8, direction=3, opacity=0.95)
    c.scumble(mid, "high", "pale", 8, direction=-2, opacity=0.95)
    c.scumble(low, "pale", "low2", 8, direction=2, opacity=0.95)

def afterglow(c, p, k=1.0):
    c.scumble(warm, "low2", "glow", 6, direction=1, opacity=0.9, pressure=[1.0, 0.75, 0.25, 0.0])
    c.dry()
    field = c.sample(Region(0.05, 0.53, 0.35, 0.58)); v = p.value_of(field)
    p["air_far"]  = p.at_value(p.mix(field, "glow", 0.5), min(v + 0.05, 0.9))
    p["air_body"] = p.at_value(p.mix("core", field, 0.35), min(v + 0.09, 0.9))
    p["air_core"] = p.at_value(p.mix("core", field, 0.25), min(v + 0.13, 0.9))
    c.glaze([(-0.08, 0.572), (0.19, 0.566), (0.62, 0.575)], "air_far", opacity=0.10 * k, size=0.22,
            pressure=[0.6, 1.0, 0.3])
    c.glaze([(-0.08, 0.578), (0.19, 0.572), (0.48, 0.579)], "air_body", opacity=0.15 * k, size=0.11,
            pressure=[0.5, 1.0, 0.25])
    c.glaze([(0.03, 0.580), (0.19, 0.577), (0.34, 0.581)], "air_core", opacity=0.18 * k, size=0.05,
            pressure=[0.3, 1.0, 0.2])
    c.dry()
    print("glow field value", round(v, 3), "->", round(p.value_of(c.sample(Region(0.12, 0.55, 0.26, 0.58))), 3))

def vA(c, p, ns): ramps(c, p); afterglow(c, p)
run_variants("sky2", [("A", vA)])
