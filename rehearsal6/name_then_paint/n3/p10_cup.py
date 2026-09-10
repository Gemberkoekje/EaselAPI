import math, random
rng = random.Random(83)
p = s.palette
def at_value(base, target):
    lo, hi = 0.0, 1.0
    for _ in range(24):
        mid = (lo + hi)/2
        if p.value_of(p.tint(base, mid)) < target: lo = mid
        else: hi = mid
    return p.tint(base, (lo+hi)/2)

cool  = p.desaturate(p.mix("burnt_umber", "ultramarine", 0.40), 0.25)
china = p.desaturate(p.mix("ultramarine", "burnt_sienna", 0.46), 0.30)
brew  = p.mix(p.mix("burnt_umber", "burnt_sienna", 0.30), "ultramarine", 0.14)

p["shad"]    = at_value(p.mix(cool, "ultramarine", 0.25), 0.345)
p["shad_f"]  = at_value(p.mix(cool, "ultramarine", 0.18), 0.415)
p["contact"] = at_value(p.mix(cool, "burnt_umber", 0.5), 0.205)
p["cup"]     = at_value(china, 0.575)
p["cup_in"]  = at_value(p.mix(china, "ultramarine", 0.30), 0.325)
p["tea"]     = at_value(brew, 0.170)
for n in ("tea", "contact", "cup_in", "shad", "shad_f", "cup"):
    print(f"{n:8s} {p.hex(p[n])}  v={p.value_of(p[n]):.3f}")

CX, RIM_Y, RX, RY = 0.393, 0.630, 0.142, 0.074
BX, BASE_Y, BRX, BRY = 0.398, 0.796, 0.084, 0.044
TX, TEA_Y, TRX, TRY = 0.395, 0.700, 0.1176, 0.0611

def arc(cx, cy, rx, ry, a0, a1, n=30):
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
whole = polygon(arc(CX, RIM_Y, RX, RY, math.pi, 2*math.pi) + right_side
                + arc(BX, BASE_Y, BRX, BRY, 0, math.pi) + left_side)
front = polygon(arc(CX, RIM_Y, RX, RY, 0, math.pi) + right_side
                + arc(BX, BASE_Y, BRX, BRY, 0, math.pi) + left_side)

s.dry()
# --- on the sill, behind the cup: the cast shadow, soft and not very dark ---
sh = ribbon([(0.40, 0.798), (0.58, 0.820), (0.78, 0.840), (1.06, 0.856)], 0.115, 0.055)
s.block_in(sh, "flat", "shad_f", direction=("axis", 22), density=0.9, size=0.040, load=1.0)
s.block_in(ribbon([(0.42, 0.800), (0.60, 0.822), (0.76, 0.838)], 0.075, 0.040),
           "flat", "shad", direction=("axis", 18), density=0.95, size=0.030, load=1.0)

# --- the cup: far edge, then the inside, then the near edge ---
s.block_in(whole.inset(0.026), "flat", "cup", direction=(82, 16), density=1.0,
           size=0.045, load=1.0)
s.block_in(ellipse((CX, RIM_Y), RX-0.013, RY-0.009).inset(0.012), "flat", "cup_in",
           direction=(6, 74), density=1.0, size=0.024, load=1.0)
s.block_in(ellipse((TX, TEA_Y), TRX, TRY).inset(0.011), "flat", "tea",
           direction=(4, 70), density=1.0, size=0.022, load=1.0)
s.block_in(front.inset(0.013), "flat", "cup", direction=(84, 20), density=1.0,
           size=0.026, load=1.0)

print("strokes:", s.stroke_count)
print(s.look())
print(s.look(region="B4:G8"))
