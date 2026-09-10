import math

p = s.palette
WHITE = "titanium_white"


def to_value(base, target):
    a, b = 0.0, 1.0
    for _ in range(24):
        m = (a + b) / 2
        a, b = (m, b) if p.value_of(p.mix(base, WHITE, m)) < target else (a, m)
    return p.mix(base, WHITE, (a + b) / 2)


p["focal"] = p.desaturate(to_value(p.mix("burnt_umber", "alizarin", 0.30), 0.235), 0.30)
p["focal_lt"] = p.desaturate(to_value(p.mix("burnt_sienna", "yellow_ochre", 0.35), 0.50), 0.28)
p["focal_sh"] = to_value(p.mix("burnt_umber", "ultramarine", 0.45), 0.125)


def leaf(cx, cy, ln, ang, sz, col, label):
    a = math.radians(ang)
    dx, dy = ln / 2 * math.cos(a), ln / 2 * math.sin(a)
    return dict(points=[(cx - dx, cy - dy), (cx + dx, cy + dy)], brush="round_hard",
                color=col, size=sz, pressure="swell", label=label)


# A: one big dark blade lying across the centre of the chain
a_plan = [
    dict(points=[(0.436, 0.352), (0.520, 0.300), (0.606, 0.272)], brush="bristle",
         color="focal_sh", size=0.030, load=0.85, pressure="swell", label="A shadow"),
    dict(points=[(0.428, 0.344), (0.514, 0.292), (0.600, 0.262)], brush="round_hard",
         color="focal", size=0.026, pressure="swell", label="A blade"),
    dict(points=[(0.446, 0.330), (0.520, 0.288), (0.588, 0.266)], brush="liner",
         color="focal_lt", size=0.004, pressure=[0.9, 0.5, 0.2], label="A vein"),
]

# B: two smaller blades crossing each other over the same pool
b_plan = [
    dict(points=[(0.470, 0.330), (0.552, 0.286), (0.622, 0.276)], brush="bristle",
         color="focal_sh", size=0.022, load=0.85, pressure="swell", label="B shadow 1"),
    dict(points=[(0.464, 0.322), (0.546, 0.278), (0.616, 0.268)], brush="round_hard",
         color="focal", size=0.019, pressure="swell", label="B blade 1"),
    leaf(0.512, 0.238, 0.086, 62, 0.014, "focal_lt", "B blade 2"),
    dict(points=[(0.492, 0.216), (0.534, 0.264)], brush="liner", color="focal_sh",
         size=0.004, pressure=[0.8, 0.3], label="B vein 2"),
]

print(s.rehearse(a_plan, region=span("C2", "G5")))
print(s.rehearse(b_plan, region=span("C2", "G5")))
print(s.rehearse(a_plan))
print(s.rehearse(b_plan))
