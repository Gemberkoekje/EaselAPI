import math, random
rng = random.Random(67)
p = s.palette
s.dry()

# cover the three pale rectangles with the board's own colour, marks at their own angles
for x, y in [(0.13, 0.652), (0.52, 0.646), (0.79, 0.640)]:
    for k in range(3):
        yy = y + (k - 1) * 0.011 + rng.uniform(-0.004, 0.004)
        s.stroke([(x - 0.085, yy + 0.012), (x + 0.085, yy - 0.010)], "bristle",
                 rng.choice(["sill", "sill_b", "sill_a"]), size=0.020,
                 pressure="even", load=1.0, load_falloff=0.2)

# ---- the cup, as geometry -------------------------------------------------
CX, RIM_Y, RX, RY = 0.393, 0.638, 0.145, 0.0725
BX, BASE_Y, BRX, BRY = 0.398, 0.790, 0.088, 0.044
TX, TEA_Y, TRX, TRY = 0.395, 0.714, 0.1165, 0.0583

def arc(cx, cy, rx, ry, a0, a1, n=26):
    return [(cx + rx * math.cos(a0 + (a1 - a0) * i / (n - 1.0)),
             cy + ry * math.sin(a0 + (a1 - a0) * i / (n - 1.0))) for i in range(n)]

def side(p0, p1, ctrl, n=16):
    return [((1-t)**2 * p0[0] + 2*(1-t)*t*ctrl[0] + t*t*p1[0],
             (1-t)**2 * p0[1] + 2*(1-t)*t*ctrl[1] + t*t*p1[1])
            for t in [i/(n-1.0) for i in range(n)]]

s.mark("rim_l", CX - RX, RIM_Y)
s.mark("rim_r", CX + RX, RIM_Y)
s.mark("rim_t", CX, RIM_Y - RY)
s.mark("rim_f", CX, RIM_Y + RY)
s.mark("base_l", BX - BRX, BASE_Y)
s.mark("base_r", BX + BRX, BASE_Y)
s.mark("base_f", BX, BASE_Y + BRY)

s.pencil(arc(CX, RIM_Y, RX, RY, 0, 2*math.pi), pressure=0.6)          # the rim
s.pencil(arc(TX, TEA_Y, TRX, TRY, math.pi, 2*math.pi), pressure=0.5)  # tea, far arc
s.pencil(side(s.pt("rim_l"), s.pt("base_l"), (0.268, 0.720)), pressure=0.6)
s.pencil(side(s.pt("rim_r"), s.pt("base_r"), (0.520, 0.720)), pressure=0.6)
s.pencil(arc(BX, BASE_Y, BRX, BRY, 0, math.pi), pressure=0.55)        # base, near arc
s.pencil(side((0.532, 0.664), (0.500, 0.752), (0.612, 0.706)), pressure=0.5)  # handle out
s.pencil(side((0.523, 0.672), (0.503, 0.736), (0.580, 0.704)), pressure=0.5)  # handle in

print("strokes:", s.stroke_count)
print(s.look())
print(s.look(region="B5:F8"))
