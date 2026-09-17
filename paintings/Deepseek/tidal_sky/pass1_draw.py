# Pass 1: the drawing, in graphite. Free, and nothing after this fixes it.
s.pencil([(0.0, HORIZON), (1.0, HORIZON)], pressure=0.5)
s.pencil([s.pt("bow"), (0.63, 0.567), s.pt("stern")], pressure=0.6)
s.pencil([s.pt("bow"), (0.535, 0.596), (0.63, 0.594), (0.745, 0.578), s.pt("stern")], pressure=0.6)
s.pencil(s.circle(s.pt("sun"), 0.05).closed, pressure=0.5)
s.look(grid=True, path="pass1_draw.png")
