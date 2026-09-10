import math, random
rng = random.Random(97)
p = s.palette
def at_value(base, target):
    lo, hi = 0.0, 1.0
    for _ in range(24):
        mid = (lo+hi)/2
        if p.value_of(p.tint(base, mid)) < target: lo = mid
        else: hi = mid
    return p.tint(base, (lo+hi)/2)

neutral = p.desaturate(p.mix("ultramarine", "burnt_sienna", 0.44), 0.55)
earthy  = p.desaturate(p.mix("burnt_umber", "ultramarine", 0.42), 0.45)
brew    = p.mix(p.mix("burnt_umber", "burnt_sienna", 0.28), "ultramarine", 0.12)

p["cup_in"]  = at_value(neutral, 0.330)
p["shad"]    = at_value(earthy, 0.375)
p["shad_f"]  = at_value(p.desaturate(earthy, 0.3), 0.432)
p["contact"] = at_value(p.mix(earthy, "burnt_umber", 0.55), 0.208)
p["tea"]     = at_value(brew, 0.172)
for n in ("tea", "contact", "cup_in", "shad", "shad_f"):
    print(f"{n:8s} {p.hex(p[n])}  v={p.value_of(p[n]):.3f}")

CX, RIM_Y, RX, RY = 0.393, 0.630, 0.142, 0.074
BX, BASE_Y, BRX, BRY = 0.398, 0.796, 0.084, 0.044
TX, TEA_Y, TRX, TRY = 0.395, 0.700, 0.1176, 0.0611
def arc(cx, cy, rx, ry, a0, a1, n=36):
    return [(cx+rx*math.cos(a0+(a1-a0)*i/(n-1.0)),
             cy+ry*math.sin(a0+(a1-a0)*i/(n-1.0))) for i in range(n)]
def bez(p0, c, p1, n=18):
    return [((1-t)**2*p0[0]+2*(1-t)*t*c[0]+t*t*p1[0],
             (1-t)**2*p0[1]+2*(1-t)*t*c[1]+t*t*p1[1])
            for t in [i/(n-1.0) for i in range(n)]]
L, R = (CX-RX, RIM_Y), (CX+RX, RIM_Y)
BL, BR = (BX-BRX, BASE_Y), (BX+BRX, BASE_Y)
right_side = bez(R, (0.522, 0.716), BR)
left_side  = bez(BL, (0.266, 0.716), L)
front = polygon(arc(CX, RIM_Y, RX, RY, 0, math.pi) + right_side
                + arc(BX, BASE_Y, BRX, BRY, 0, math.pi) + left_side)
inner = polygon(arc(CX, RIM_Y, RX-0.014, RY-0.010, 0, 2*math.pi))
tea   = polygon(arc(TX, TEA_Y, TRX, TRY, 0, 2*math.pi))

s.dry()
# the sill's shadow again: broken edges, close in value to the board
cast = polygon([(0.42, 0.788), (0.60, 0.802), (0.80, 0.818), (1.06, 0.828),
                (1.06, 0.878), (0.82, 0.872), (0.58, 0.856), (0.40, 0.840)])
s.block_in(cast.inset(0.014), "bristle", "shad_f", direction=(6, -14),
           density=1.0, size=0.030, load=0.9)
s.block_in(polygon([(0.42, 0.796), (0.58, 0.810), (0.74, 0.822), (0.74, 0.856),
                    (0.56, 0.848), (0.41, 0.834)]).inset(0.010), "bristle", "shad",
           direction=(5, -12), density=1.0, size=0.022, load=0.95)
for a, b in [((0.86, 0.826), (0.92, 0.838)), ((0.70, 0.864), (0.76, 0.856)),
             ((0.53, 0.792), (0.60, 0.802))]:
    s.smudge([a, b], size=0.038)

# the inside, then the tea, then the near wall over both
s.block_in(inner.inset(0.011), "flat", "cup_in", direction=4, density=1.0, size=0.022, load=1.0)
s.block_in(tea.inset(0.010), "flat", "tea", direction=3, density=1.0, size=0.020, load=1.0)
s.block_in(front.inset(0.013), "flat", "cup", direction=(84, 22), density=1.0, size=0.026, load=1.0)

print("strokes:", s.stroke_count)
print(s.look(region="B4:G8"))
