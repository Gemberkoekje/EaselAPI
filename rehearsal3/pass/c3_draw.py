# c3 - marks + corrected drawing on the new umber_wash ground, and two region
# compares against the still-empty canvas so I read the reference's LOCAL values
# instead of guessing them again.
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


s.mark("rim_l",      0.310, 0.197)
s.mark("rim_r",      0.638, 0.223)
s.mark("rim_top",    0.440, 0.112)
s.mark("rim_front",  0.470, 0.333)
s.mark("base_front", 0.465, 0.665)
s.mark("handle_out", 0.735, 0.363)
s.mark("spoon_top",  0.535, 0.008)
s.mark("visor",      0.398, 0.466)

s.pencil(ellipse(0.474, 0.223, 0.164, 0.110, shear=0.159), pressure=0.7)
s.pencil(ellipse(0.480, 0.227, 0.135, 0.084, shear=0.13), pressure=0.6)
s.pencil([(0.310, 0.200), (0.316, 0.330), (0.332, 0.500), (0.355, 0.651)])
s.pencil([(0.638, 0.226), (0.632, 0.350), (0.612, 0.500), (0.578, 0.622)])
s.pencil(ellipse(0.4665, 0.641, 0.112, 0.024, shear=-0.125,
                 t0=0.0, t1=math.pi, n=24))
s.pencil([(0.645, 0.218), (0.706, 0.250), (0.735, 0.330), (0.722, 0.430),
          (0.668, 0.487), (0.606, 0.498)])
s.pencil([(0.652, 0.268), (0.692, 0.300), (0.702, 0.368), (0.678, 0.432),
          (0.628, 0.452)])
s.pencil([(0.498, 0.000), (0.572, 0.010), (0.540, 0.130), (0.512, 0.228),
          (0.478, 0.222), (0.487, 0.120), (0.498, 0.000)])
s.pencil([(0.482, 0.230), (0.512, 0.234), (0.548, 0.300), (0.512, 0.312),
          (0.482, 0.230)])
s.pencil([(0.402, 0.402), (0.470, 0.396), (0.506, 0.424), (0.512, 0.470),
          (0.558, 0.478), (0.560, 0.552), (0.520, 0.560), (0.522, 0.652),
          (0.478, 0.655), (0.472, 0.610), (0.432, 0.612), (0.428, 0.658),
          (0.383, 0.655), (0.377, 0.480), (0.384, 0.424), (0.402, 0.402)])
s.pencil(ellipse(0.399, 0.466, 0.033, 0.020, shear=0.25))
s.pencil([(0.352, 0.560), (0.333, 0.610), (0.318, 0.655), (0.303, 0.700),
          (0.312, 0.755), (0.333, 0.791), (0.400, 0.828), (0.455, 0.845),
          (0.545, 0.831), (0.616, 0.764), (0.668, 0.690), (0.700, 0.612)])
s.pencil(ellipse(0.652, 0.560, 0.056, 0.028, shear=-0.2))
s.pencil([(0.810, 0.548), (0.830, 0.538), (0.875, 0.565), (0.883, 0.610),
          (0.865, 0.650), (0.818, 0.630), (0.798, 0.590), (0.810, 0.548)])
s.pencil([(0.645, 0.213), (0.700, 0.292), (0.731, 0.400), (0.766, 0.492),
          (0.806, 0.552)])
s.pencil([(0.912, 0.000), (1.000, 0.000), (1.000, 0.056), (0.922, 0.018)])

print("=== the mug, C2:F6 ===")
print(s.compare(REF, region=span("C2", "F6")))
print("=== shadow + table under it, C5:G8 ===")
print(s.compare(REF, region=span("C5", "G8")))
print("strokes:", s.stroke_count)
print(s.look(reference=REF))
