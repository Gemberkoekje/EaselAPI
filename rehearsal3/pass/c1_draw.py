# c1 - landmarks + my own pencil drawing. No paint.
# Masses named by cell from look_001:
#   mug body      C2 - F6      (pale mass, tallest thing)
#   coffee ellipse C3 - E4     (darkest thing in the picture)
#   spoon         E1 - E3      (dark spike out of the top)
#   among-us blob C4 - E6      (dark brown, on the mug's face)
#   cast shadow   C5 - G7      (soft dark, down-left of the base)
#   tea tag       G5 - H6      (small dark navy)
#   table         everything else; lightest F1-H3, darkest A6-C8
import math

REF = r"C:\temp\Level1.jpg"


def ellipse(cx, cy, a, b, shear=0.0, t0=0.0, t1=math.tau, n=48):
    pts = []
    for i in range(n + 1):
        t = t0 + (t1 - t0) * i / n
        dx = a * math.cos(t)
        dy = b * math.sin(t)
        pts.append((cx + dx, cy + dy + shear * dx))
    return pts


# ---- landmarks -------------------------------------------------------
s.mark("rim_l",      0.310, 0.197)
s.mark("rim_r",      0.638, 0.223)
s.mark("rim_top",    0.440, 0.112)
s.mark("rim_front",  0.470, 0.333)
s.mark("base_front", 0.465, 0.673)
s.mark("handle_out", 0.735, 0.363)
s.mark("spoon_top",  0.535, 0.008)
s.mark("visor",      0.398, 0.467)

# ---- the drawing -----------------------------------------------------
# outer rim
s.pencil(ellipse(0.474, 0.223, 0.164, 0.110, shear=0.159), pressure=0.7)
# inner rim / surface of the coffee
s.pencil(ellipse(0.480, 0.227, 0.135, 0.084, shear=0.13), pressure=0.6)
# left wall of the mug
s.pencil([(0.310, 0.200), (0.316, 0.330), (0.330, 0.480), (0.350, 0.628)])
# right wall
s.pencil([(0.638, 0.226), (0.632, 0.350), (0.612, 0.500), (0.578, 0.618)])
# base ellipse, front half only
s.pencil(ellipse(0.464, 0.632, 0.114, 0.041, t0=0.0, t1=math.pi, n=24))
# handle: outer arc, then the hole
s.pencil([(0.645, 0.218), (0.706, 0.250), (0.735, 0.330), (0.722, 0.430),
          (0.668, 0.487), (0.606, 0.498)])
s.pencil([(0.652, 0.268), (0.692, 0.300), (0.702, 0.368), (0.678, 0.432),
          (0.628, 0.452)])
# spoon: black handle then the metal into the cup
s.pencil([(0.498, 0.000), (0.572, 0.010), (0.540, 0.130), (0.512, 0.228),
          (0.478, 0.222), (0.487, 0.120), (0.498, 0.000)])
s.pencil([(0.482, 0.230), (0.512, 0.234), (0.548, 0.300), (0.512, 0.312),
          (0.482, 0.230)])
# among-us figure
s.pencil([(0.402, 0.402), (0.470, 0.396), (0.506, 0.424), (0.512, 0.470),
          (0.558, 0.478), (0.560, 0.552), (0.520, 0.560), (0.522, 0.652),
          (0.478, 0.655), (0.472, 0.610), (0.432, 0.612), (0.428, 0.658),
          (0.383, 0.655), (0.377, 0.480), (0.384, 0.424), (0.402, 0.402)])
s.pencil(ellipse(0.399, 0.470, 0.035, 0.023, shear=0.25))
# the cast shadow, as a boundary not an outline
s.pencil([(0.336, 0.616), (0.292, 0.700), (0.278, 0.760), (0.318, 0.818),
          (0.400, 0.848), (0.492, 0.845), (0.578, 0.800), (0.640, 0.730),
          (0.688, 0.648), (0.700, 0.598)])
# the handle's own shadow ring
s.pencil(ellipse(0.652, 0.560, 0.058, 0.030, shear=-0.2))
# tea tag + string
s.pencil([(0.811, 0.559), (0.850, 0.541), (0.928, 0.581), (0.920, 0.641),
          (0.878, 0.657), (0.820, 0.627), (0.811, 0.559)])
s.pencil([(0.645, 0.213), (0.700, 0.292), (0.731, 0.400), (0.762, 0.492),
          (0.812, 0.560)])
s.pencil([(0.606, 0.600), (0.668, 0.642), (0.726, 0.626), (0.800, 0.596)])
# dark corner, top right
s.pencil([(0.912, 0.000), (1.000, 0.000), (1.000, 0.056), (0.922, 0.018)])

print("strokes so far:", s.stroke_count)
print(s.look(reference=REF))
print(s.look(region=cell("C2"), reference=REF, grid="fine"))
print(s.look(region=span("D4", "E5"), reference=REF, grid="fine"))
