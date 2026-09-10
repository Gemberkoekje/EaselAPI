import math

p = s.palette
WHITE = "titanium_white"


def to_value(base, target):
    a, b = 0.0, 1.0
    for _ in range(24):
        m = (a + b) / 2
        a, b = (m, b) if p.value_of(p.mix(base, WHITE, m)) < target else (a, m)
    return p.mix(base, WHITE, (a + b) / 2)


p["blade"] = p.desaturate(to_value(p.mix("burnt_umber", "viridian", 0.35), 0.215), 0.45)
p["blade2"] = p.desaturate(to_value(p.mix("burnt_umber", "alizarin", 0.25), 0.185), 0.45)
p["blade_sh"] = to_value(p.mix("burnt_umber", "ultramarine", 0.45), 0.125)
p["blade_lt"] = p.desaturate(to_value(p.mix("yellow_ochre", "burnt_sienna", 0.30), 0.44), 0.35)
p["quiet"] = p.desaturate(to_value(p.mix("burnt_umber", "viridian", 0.35), 0.235), 0.55)
p["film"] = p.mix("ultramarine", "burnt_umber", 0.50)

s.dry()

# two blades lying across the water: found on the light, lost on the dark
s.stroke([(0.352, 0.442), (0.436, 0.372), (0.528, 0.302), (0.622, 0.256),
          (0.706, 0.234)], "round_hard", "blade_sh", size=0.015,
         pressure=[0.15, 0.8, 1.0, 0.7, 0.1])
s.stroke([(0.346, 0.436), (0.430, 0.364), (0.522, 0.294), (0.616, 0.248),
          (0.702, 0.226)], "round_hard", "blade", size=0.012,
         pressure=[0.2, 1.0, 0.9, 0.7, 0.15])
s.stroke([(0.624, 0.128), (0.578, 0.226), (0.536, 0.330), (0.506, 0.442)],
         "round_hard", "blade2", size=0.010, pressure=[0.1, 0.9, 1.0, 0.2])
s.stroke([(0.452, 0.356), (0.520, 0.302), (0.586, 0.268)], "liner", "blade_lt",
         size=0.0035, pressure=[0.2, 0.9, 0.3])

# sink the pale hook in the near corner - it was pulling the eye out of the picture
s.glaze([(0.052, 0.880), (0.128, 0.850), (0.204, 0.858)], "film", opacity=0.34,
        size=0.048)
s.stroke([(0.086, 0.866), (0.140, 0.852)], "bristle", "film", size=0.020, load=0.9,
         pressure="swell")

# two quiet leaves in the empty middle-right, barely above the field
for cx, cy, ln, ang, sz in ((0.664, 0.518, 0.052, -40, 0.013),
                            (0.556, 0.626, 0.040, 24, 0.010)):
    a = math.radians(ang)
    dx, dy = ln / 2 * math.cos(a), ln / 2 * math.sin(a)
    s.stroke([(cx - dx, cy - dy), (cx + dx, cy + dy)], "round_hard", "quiet",
             size=sz, pressure="swell")

print("strokes", s.stroke_count)
print(s.look())
