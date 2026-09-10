import math
p = s.palette
def at_value(base, target):
    lo, hi = 0.0, 1.0
    for _ in range(24):
        m=(lo+hi)/2
        if p.value_of(p.tint(base, m)) < target: lo=m
        else: hi=m
    return p.tint(base, (lo+hi)/2)
G = p.desaturate(p.mix("ultramarine", "burnt_sienna", 0.48), 0.28)
p["hi"]   = at_value(G, 0.940)
p["hi2"]  = at_value(G, 0.900)
p["sig"]  = at_value(p.mix("burnt_umber", "ultramarine", 0.35), 0.330)
CX, RIM_Y = 0.393, 0.630
MRX, MRY = 0.130, 0.065
def marc(a0, a1, n=10):
    return [(CX + MRX*math.cos(a0+(a1-a0)*i/(n-1.0)),
             RIM_Y + MRY*math.sin(a0+(a1-a0)*i/(n-1.0))) for i in range(n)]

s.dry()
# last of the light in the glass, tapering away before it reaches the cup
for i, y in enumerate([0.424, 0.451, 0.478, 0.506]):
    s.stroke([(-0.20, y + 0.010), (0.24, y), (0.68, y - 0.008)], "round_hard",
             "hi2" if i % 2 else "burn", size=[0.040, 0.026, 0.048, 0.030][i],
             pressure=[1.0, 0.95, 0.05], load=1.0)

# --- highlights: three, and no more ---------------------------------------
s.stroke(marc(1.13*math.pi, 1.34*math.pi), "round_hard", "hi", size=0.0075,
         pressure=[0.2, 1.0, 0.35], load=1.0)
s.stroke(marc(0.80*math.pi, 0.95*math.pi, 6), "round_hard", "hi2", size=0.0055,
         pressure=[0.15, 0.9, 0.2], load=1.0)
s.dab(0.5565, 0.6535, "round_hard", "hi2", size=0.0055, press=2)

s.unmark("rim_l"); s.unmark("rim_r"); s.unmark("rim_t"); s.unmark("rim_f")
s.unmark("tea_t"); s.unmark("base_l"); s.unmark("base_r"); s.unmark("base_f")
print("strokes:", s.stroke_count)
print(s.look(sketch=False))
print(s.look(region="C4:F7", sketch=False))
