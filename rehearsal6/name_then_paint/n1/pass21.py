# Pass 21 - bloom B again: mass, dome, a real shadow flank. Nothing else.
exec(open("lib.py").read())
pc, warm, cool, arc, at, dome, finish = make(s)
p = s.palette
s.dry()

CX, CY, RX, RY = 0.640, 0.520, 0.112, 0.100
e = ellipse(Region(CX-RX, CY-RY, CX+RX, CY+RY))
s.block_in(e.inset(0.012), "flat", pc(0.62), direction=("axis", 74), density=1.0,
           size=0.022, load=1.0, pressure="even")
s.sweep(e, "flat", pc(0.64), depth=0.10, size=0.020, load=1.0, pressure="even")
dome(CX, CY, RX, RY, 5, 0.645, 0.215, 0.022)

# a shadow flank that actually turns the form
for k, (t0, span_, f, v) in enumerate([(-16, 74, 0.66, 0.50), (2, 82, 0.86, 0.455),
                                       (24, 66, 1.00, 0.425), (44, 54, 0.50, 0.53)]):
    s.stroke(arc(CX, CY, RX, RY, f, t0, t0+span_, 8), "flat", cool(pc(v), 0.16),
             size=0.020 + 0.004*(k % 2), pressure="even", load=1.0)
# the hollow at the heart, small and off-centre
s.stroke(arc(CX+0.004, CY+0.004, RX, RY, 0.17, 30, 320, 6), "round_hard",
         cool(pc(0.47), 0.14), size=0.013, pressure="even")
s.stroke([(0.630,0.510),(0.646,0.505),(0.660,0.514)], "round_hard",
         p.mix(pc(0.58), p["pet_heart"], 0.40), size=0.008, pressure=[0.4,1.0,0.35])

print("strokes:", s.stroke_count)
print(s.look(region=span("E4","G6"), sketch=False))
