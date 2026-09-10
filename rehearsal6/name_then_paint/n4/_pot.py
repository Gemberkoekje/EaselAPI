import math
CX = 0.6230
RY = 0.0300

def arc(cx, cy, rx, ry, a0, a1, n=28):
    return [(cx + rx * math.cos(math.radians(a)), cy + ry * math.sin(math.radians(a)))
            for a in [a0 + (a1 - a0) * i / (n - 1.0) for i in range(n)]]

# outer profile: (y, half-width) from the lip down to the foot
PROF = [(0.4990, 0.1125), (0.5240, 0.1140), (0.5470, 0.1150), (0.5545, 0.1010),
        (0.5850, 0.0985), (0.6200, 0.0950), (0.6560, 0.0895), (0.6950, 0.0830),
        (0.7220, 0.0770), (0.7380, 0.0725), (0.7480, 0.0680)]

def side(sign, squash=1.0, dy=0.0):
    return [(CX + sign * w * squash, y + dy) for y, w in PROF]

SIL = polygon(side(-1) + arc(CX, 0.7480, 0.0680, 0.0165, 180, 360)[::-1] + side(1)[::-1]
              + arc(CX, 0.4990, 0.1125, RY, 360, 180)[::-1])
RIM     = ellipse((CX, 0.4990), 0.1125, RY)
INSIDE  = ellipse((CX, 0.5015), 0.0985, 0.0245)
COLLAR  = polygon(arc(CX, 0.4990, 0.1125, RY, 180, 360)
                  + arc(CX, 0.5460, 0.1150, 0.0325, 0, 180))
NEARLIP = polygon(arc(CX, 0.4995, 0.0990, 0.0250, 12, 168)
                  + arc(CX, 0.5065, 0.1125, 0.0300, 168, 12))
BASE    = ellipse((CX, 0.7440), 0.0700, 0.0170)

def hw(y):
    for i in range(len(PROF) - 1):
        (y0, w0), (y1, w1) = PROF[i], PROF[i + 1]
        if y0 <= y <= y1:
            t = (y - y0) / (y1 - y0)
            return w0 + (w1 - w0) * t
    return PROF[-1][1]

def band(u0, u1, y0=0.5560, y1=0.7480):
    """a vertical slice of the body between fractions u0..u1 of its half-width"""
    ys = [y0 + (y1 - y0) * i / 7.0 for i in range(8)]
    left  = [(CX + u0 * hw(y), y) for y in ys]
    right = [(CX + u1 * hw(y), y) for y in ys]
    return polygon(left + right[::-1])

def ring(y, ry, u0=-1.0, u1=1.0, n=16):
    """a curved path running round the pot at height y - the marks that say cylinder"""
    a0 = math.degrees(math.acos(max(-1.0, min(1.0, u0))))
    a1 = math.degrees(math.acos(max(-1.0, min(1.0, u1))))
    return [(CX + hw(y) * math.cos(math.radians(a)), y + ry * math.sin(math.radians(a)))
            for a in [a0 + (a1 - a0) * i / (n - 1.0) for i in range(n)]]
