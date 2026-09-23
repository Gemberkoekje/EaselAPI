import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import run_variants, load
from easel import polygon, ellipse, Region

s, ns = load(); p = s.palette
for label, c in {"low_tan": p.at_value(p.mix("yellow_ochre", "alizarin", 0.15), 0.66),
                 "salmon": p.at_value(p.mix("titanium_white", "cadmium_red", 0.3), 0.66),
                 "peach": p.at_value(p.mix("cadmium_red", "yellow_ochre", 0.6), 0.66),
                 "rose_ochre": p.at_value(p.mix("alizarin", "yellow_ochre", 0.6), 0.66),
                 "pale_blue": p.at_value(p.mix("cerulean", "ultramarine", 0.3), 0.58)}.items():
    print(f"{label:11s} {p.hex(c)} value {p.value_of(c):.2f} chroma {p.chroma_of(c):.3f}")

top = polygon([(-0.06, -0.06), (1.06, -0.06), (1.06, 0.27), (-0.06, 0.29)])
mid = polygon([(-0.06, 0.17), (1.06, 0.15), (1.06, 0.45), (-0.06, 0.47)])
low = polygon([(-0.06, 0.35), (1.06, 0.33), (1.06, 0.62), (-0.06, 0.62)])
flat_glow = ellipse((0.20, 0.594), 0.40, 0.10)
glow_core = ellipse((0.19, 0.590), 0.17, 0.035)

def glow(c, p, ns, n=12):
    p["glow_rim"] = c.sample(Region(0.10, 0.49, 0.30, 0.51))
    c.scumble(flat_glow, "glow_rim", "glow", n, direction="inward")
    c.scumble(glow_core, "glow", "core", 6, direction="inward")

def v_three_bristle(c, p, ns):
    p["low2"] = p.at_value(p.mix("cadmium_red", "yellow_ochre", 0.6), 0.66)
    kw = dict(opacity=0.95, jitter=0.01, size_jitter=0.03)
    c.scumble(top, "zenith", "high", 8, direction=3, **kw)
    c.scumble(mid, "high", "pale", 8, direction=-2, **kw)
    c.scumble(low, "pale", "low2", 8, direction=2, **kw)
    glow(c, p, ns)

def v_three_flat(c, p, ns):
    p["low2"] = p.at_value(p.mix("cadmium_red", "yellow_ochre", 0.6), 0.66)
    kw = dict(brush="flat", opacity=0.95, jitter=0.01, size_jitter=0.03)
    c.scumble(top, "zenith", "high", 8, direction=3, **kw)
    c.scumble(mid, "high", "pale", 8, direction=-2, **kw)
    c.scumble(low, "pale", "low2", 8, direction=2, **kw)
    glow(c, p, ns)

run_variants("sky", [("three_bristle", v_three_bristle), ("three_flat", v_three_flat)])
