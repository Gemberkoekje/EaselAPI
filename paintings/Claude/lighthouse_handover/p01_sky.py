# The sky: a graded field that is most of the picture, laid as three overlapping ramps a
# few degrees off the frame (bristle, wander halved), the warmth brought in from the left
# with passes that fade to nothing toward the right, two crossers, then the afterglow
# itself as lit air: three glazes along the horizon, centred where the sun went down.
import random

p["low2"] = p.at_value(p.mix("cadmium_red", "yellow_ochre", 0.6), 0.66)
p["low_cool"] = p.at_value(p.mix("alizarin", "yellow_ochre", 0.6), 0.64)
KW = dict(opacity=0.95, jitter=0.01, size_jitter=0.03)

top = polygon([(-0.06, -0.06), (1.06, -0.06), (1.06, 0.27), (-0.06, 0.29)])
mid = polygon([(-0.06, 0.17), (1.06, 0.15), (1.06, 0.45), (-0.06, 0.47)])
low = polygon([(-0.06, 0.35), (1.06, 0.33), (1.06, 0.62), (-0.06, 0.62)])
s.scumble(top, "zenith", "high", 8, direction=3, **KW)
s.scumble(mid, "high", "pale", 8, direction=-2, **KW)
s.scumble(low, "pale", "low_cool", 8, direction=2, **KW)

# warmth from the left: each pass full on the left, nothing by its right end
rng = random.Random(3)
ys = [0.472, 0.489, 0.509, 0.528, 0.551, 0.572]
for i, y in enumerate(ys):
    t = i / (len(ys) - 1)
    x_end = 0.50 + 0.2 * t + rng.uniform(-0.05, 0.05)
    s.stroke([(-0.06, y + rng.uniform(-0.004, 0.004)), (0.28, y - 0.003), (x_end, y + 0.004)],
             "flat", p.mix("low2", "glow", 0.1 + 0.9 * t), size=0.058 + rng.uniform(-0.006, 0.006),
             opacity=0.35 + 0.15 * t, load=1.0, load_falloff=0.0, pressure=[1.0, 0.6, 0.0],
             jitter=0.01, size_jitter=0.03)

# two crossers, starved, at angles, not parallel to each other or to the bands
p["cloud_high"] = p.at_value(p.mix("zenith", "high", 0.4), 0.39)
p["cloud_lit"]  = p.at_value(p.mix("low2", "alizarin", 0.15), 0.64)
s.stroke([(-0.06, 0.105), (0.45, 0.205), (1.06, 0.330)], "bristle", "cloud_high",
         size=0.065, load=0.45, opacity=0.40, pressure="swell")      # rising to the left, ~8 deg
s.stroke([(-0.06, 0.482), (0.25, 0.452), (0.58, 0.402)], "bristle", "cloud_lit",
         size=0.05, load=0.40, opacity=0.45, pressure="swell")       # rising to the right, left half

# the afterglow: lit air, not light on a surface
s.dry()
field = s.sample(Region(0.05, 0.53, 0.35, 0.58)); v = p.value_of(field)
p["air_far"]  = p.at_value(p.mix(field, "glow", 0.5), min(v + 0.05, 0.9))
p["air_body"] = p.at_value(p.mix("core", field, 0.35), min(v + 0.09, 0.9))
p["air_core"] = p.at_value(p.mix("core", field, 0.25), min(v + 0.13, 0.9))
s.glaze([(-0.08, 0.560), (0.19, 0.550), (0.66, 0.566)], "air_far", opacity=0.10, size=0.26,
        pressure=[0.6, 1.0, 0.3])
s.glaze([(-0.08, 0.572), (0.19, 0.566), (0.50, 0.576)], "air_body", opacity=0.15, size=0.12,
        pressure=[0.5, 1.0, 0.25])
s.glaze([(0.03, 0.580), (0.19, 0.577), (0.34, 0.581)], "air_core", opacity=0.18, size=0.05,
        pressure=[0.3, 1.0, 0.2])
s.dry()
