R = "/home/user/refs/Level1.jpg"
# option A: dry-brush bristle crossing the swathe at ~34 deg
A = [dict(points=[(0.55,0.86),(0.78,0.72),(0.98,0.60)], brush="bristle", color="wood_hi",
          size=0.10, load=0.5, pressure="even"),
     dict(points=[(0.52,0.63),(0.75,0.50),(1.0,0.40)], brush="bristle", color="wood_hi",
          size=0.10, load=0.5, pressure="even"),
     dict(points=[(0.56,0.36),(0.80,0.24),(1.0,0.16)], brush="bristle", color="wood_hi",
          size=0.10, load=0.5, pressure="even")]
# option B: broad flat, even, full load, same angle
B = [dict(p, brush="flat", size=0.13, load=1.0, opacity=0.35) for p in A]
# option C: round_hard (no axis), big and soft-loaded
C = [dict(p, brush="round_hard", size=0.11, load=0.7, pressure="even") for p in A]
print(s.rehearse(A, region=span("E4","H8")))
print(s.rehearse(B, region=span("E4","H8")))
print(s.rehearse(C, region=span("E4","H8")))
