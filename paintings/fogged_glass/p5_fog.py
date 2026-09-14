# The condensation. A film, not a mass: glazes that lift the glass a little and
# leave what is behind it showing. Only the far end, which goes to haze, and the
# grazing-angle band under the eave are laid as paint.
from easel import polygon

p["fogthin"] = p.at_value(p.mix(p["neutral"], "cerulean", 0.10), 0.68)
p["fogfar"]  = p.at_value(p.mix(p["neutral"], "cerulean", 0.07), 0.66)
p["fogsky"]  = p.at_value(p.mix(p["neutral"], "cerulean", 0.05), 0.70)

s.dry()

def along(hm, d0, d1, n=5):
    return [P(WALL, hm, d0 + (d1 - d0) * i / (n - 1.0)) for i in range(n)]

# the far end goes to haze. Strokes that lose their near end, not a filled shape:
# a shape came back as a lit panel with a hard edge down the middle of the glass.
for hm, sz, pr, ld in [(1.88, 0.130, [0.28, 0.75, 1.00, 0.40, 0.0], 0.85),
                       (1.42, 0.165, [0.24, 0.90, 0.85, 0.32, 0.0], 0.78),
                       (1.02, 0.120, [0.30, 0.60, 0.75, 0.22, 0.0], 0.68)]:
    s.stroke(along(hm, 19.0, 2.9), "round_hard", "fogfar", size=sz, pressure=pr,
             load=ld, load_falloff=0.10, opacity=0.62, note="fog")

# the film itself: four bands across the near two-thirds, each solved to a value
for hm, tv, sz in [(1.95, 0.48, 0.115), (1.62, 0.46, 0.130),
                   (1.30, 0.49, 0.140), (0.98, 0.46, 0.150)]:
    s.glaze(along(hm, 6.0, 1.28), "fogthin", to_value=tv, size=sz, note="fog")

# the glass just under the eave takes the sky at a grazing angle
s.stroke([(0.288, 0.452), (0.520, 0.352), (0.760, 0.249), (1.02, 0.138)],
         "bristle", "fogsky", size=0.030, load=0.7, load_falloff=0.15,
         opacity=0.50, pressure=[0.35, 0.8, 1.0, 0.9], note="fog")
s.stroke([(1.02, 0.186), (0.780, 0.289), (0.560, 0.381)],
         "bristle", "fogsky", size=0.022, load=0.45, load_falloff=0.25,
         opacity=0.40, pressure=[0.9, 1.0, 0.3], note="fog")
