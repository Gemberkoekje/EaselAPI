import math
s.erase()
CX, RIM_Y, RX, RY = 0.393, 0.630, 0.142, 0.074
BX, BASE_Y, BRX, BRY = 0.398, 0.796, 0.084, 0.044
TX, TEA_Y, TRX, TRY = 0.395, 0.700, 0.1176, 0.0611

def arc(cx, cy, rx, ry, a0, a1, n=30):
    return [(cx + rx*math.cos(a0+(a1-a0)*i/(n-1.0)),
             cy + ry*math.sin(a0+(a1-a0)*i/(n-1.0))) for i in range(n)]
def bez(p0, c, p1, n=18):
    return [((1-t)**2*p0[0] + 2*(1-t)*t*c[0] + t*t*p1[0],
             (1-t)**2*p0[1] + 2*(1-t)*t*c[1] + t*t*p1[1])
            for t in [i/(n-1.0) for i in range(n)]]

for nm, xy in [("rim_l",(CX-RX,RIM_Y)), ("rim_r",(CX+RX,RIM_Y)), ("rim_t",(CX,RIM_Y-RY)),
               ("rim_f",(CX,RIM_Y+RY)), ("tea_t",(TX,TEA_Y-TRY)),
               ("base_l",(BX-BRX,BASE_Y)), ("base_r",(BX+BRX,BASE_Y))]:
    s.mark(nm, *xy)

s.pencil(arc(CX, RIM_Y, RX, RY, 0, 2*math.pi), pressure=0.6)
s.pencil(arc(TX, TEA_Y, TRX, TRY, math.pi, 2*math.pi), pressure=0.5)
s.pencil(bez(s.pt("rim_l"), (0.266, 0.716), s.pt("base_l")), pressure=0.6)
s.pencil(bez(s.pt("rim_r"), (0.522, 0.716), s.pt("base_r")), pressure=0.6)
s.pencil(arc(BX, BASE_Y, BRX, BRY, 0, math.pi), pressure=0.55)
s.pencil(bez((0.528, 0.652), (0.646, 0.700), (0.498, 0.766)), pressure=0.5)
s.pencil(bez((0.519, 0.672), (0.601, 0.703), (0.495, 0.742)), pressure=0.5)
print(s.look(region="B4:G8"))
