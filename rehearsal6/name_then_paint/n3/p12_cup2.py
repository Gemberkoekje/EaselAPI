import math
p = s.palette
CX, RIM_Y, RX, RY = 0.393, 0.630, 0.142, 0.074
IRX, IRY = 0.118, 0.056
BX, BASE_Y, BRX, BRY = 0.398, 0.796, 0.084, 0.044
TX, TEA_Y, TRX, TRY = 0.395, 0.700, 0.1176, 0.0611

def arc(cx, cy, rx, ry, a0, a1, n=40):
    return [(cx+rx*math.cos(a0+(a1-a0)*i/(n-1.0)),
             cy+ry*math.sin(a0+(a1-a0)*i/(n-1.0))) for i in range(n)]
def bez(p0, c, p1, n=20):
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
inner = polygon(arc(CX, RIM_Y, IRX, IRY, 0, 2*math.pi))

# the tea is the lens where its surface is still inside the near lip
top, bot = [], []
for i in range(60):
    x = CX - 0.104 + 0.208 * i / 59.0
    a = (x - TX) / TRX; b = (x - CX) / IRX
    if abs(a) >= 1 or abs(b) >= 1: continue
    yt = TEA_Y - TRY * math.sqrt(1 - a*a)
    yb = RIM_Y + IRY * math.sqrt(1 - b*b)
    if yt < yb - 0.004:
        top.append((x, yt)); bot.append((x, yb))
tea = polygon(top + bot[::-1])
print("tea lens box:", tea.box)

s.dry()
s.block_in(whole.inset(0.020), "flat", "cup", direction=(86, 32), density=1.0,
           size=0.036, load=1.0)
s.block_in(inner, "flat", "cup_in", direction=90, density=1.0, size=0.014, load=1.0)
s.block_in(tea, "flat", "tea", direction=90, density=1.0, size=0.012, load=1.0)
s.block_in(front.inset(0.010), "flat", "cup", direction=90, density=1.0, size=0.020, load=1.0)
print("strokes:", s.stroke_count)
print(s.look(region="C5:E6", sketch=False))
print(s.look(region="B4:G8"))
