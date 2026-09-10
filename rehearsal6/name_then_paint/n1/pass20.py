exec(open("lib.py").read())
pc, warm, cool, arc, at, dome, finish = make(s)
s.dry()
finish(0.640, 0.520, 0.112, 0.100, 5, 0.64, 0.21, 0.022, bg="bg",
       notches=9, edges=8, out_petals=5, bites=5,
       droop=[(0.700, 0.598, 0.030, 0.020, 0.50), (0.664, 0.614, 0.026, 0.017, 0.46),
              (0.736, 0.556, 0.026, 0.018, 0.58)])
print("strokes:", s.stroke_count)
print(s.look(region=span("E4","G6"), sketch=False))
