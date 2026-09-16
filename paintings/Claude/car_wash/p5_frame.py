# The near dark. No header band: from the driver's seat the top of the screen is above
# the sight line, so the mirror hangs in from off-canvas. A band there made a letterbox.
# load=1.0 with no falloff because these have to read as solid -- the default runs dry.
SOLID = dict(density=1.0, load=1.0, load_falloff=0.0, edge="clean")
for name, item in [
    ("pillar L", {"shape": pillar_l(), "brush": "flat", "color": "frame",
                  "size": 0.030, "direction": "axis", **SOLID}),
    ("pillar R", {"shape": pillar_r(), "brush": "flat", "color": "frame",
                  "size": 0.024, "direction": "axis", **SOLID}),
    ("mirror",   {"shape": mirror(),   "brush": "flat", "color": "frame",
                  "size": 0.018, "direction": "axis", **SOLID}),
    ("dash",     {"shape": dash(),     "brush": "flat", "color": "frame",
                  "size": 0.060, "direction": "axis", **SOLID}),
    # the inside of the wheel, laid before its rim so the rim has something to stop against
    ("binnacle", {"shape": binnacle(), "brush": "flat", "color": "frame",
                  "size": 0.052, "direction": "axis", "density": 1.0,
                  "load": 1.0, "load_falloff": 0.0, "opacity": 0.90}),
]:
    print(f"  {name:9s} {s.cost(item):3d}")
    s.paint(item)

s.stroke([(0.552, -0.04), (0.566, 0.082)], "flat", "frame", size=0.013,
         load=1.0, load_falloff=0.0, pressure="even")
s.stroke(wheel(), "flat", "frame", size=0.026,
         load=1.0, load_falloff=0.0, pressure="even")
s.stroke([(0.108, 0.912), (0.190, 0.778), (0.304, 0.726)], "flat", "frame",
         size=0.019, load=1.0, load_falloff=0.0, pressure="taper")

# What makes the frame a car interior rather than a mask: three catch-lights, each
# broken and partial. The wheel's lower edge is lost into the dash on purpose; only
# its top is found, against the glass.
# The rim is glossy: one hard streak of the screen's light along its upper left is
# what makes the whole wheel read, and it is the only mark on it.
s.stroke([(0.158, 0.812), (0.252, 0.736), (0.378, 0.712)], "round_hard", "rim",
         size=0.0085, opacity=0.95, pressure=[0.15, 1.0, 0.35])
s.stroke([(0.446, 0.762), (0.498, 0.818)], "round_hard", "rim",
         size=0.0060, opacity=0.70, pressure=[0.9, 0.1])
s.stroke([(0.690, 0.876), (0.858, 0.826), (0.985, 0.782)], "bristle", "frame_lt",
         size=0.010, load=0.35, opacity=0.65, pressure="lift_off")
s.stroke([(0.072, 0.128), (0.060, 0.412)], "bristle", "mag_lo",
         size=0.009, load=0.30, opacity=0.55, pressure="taper")
print(s.look())
