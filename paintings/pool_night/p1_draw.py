# Bands counted before the first mass: ceiling / wall / far deck / water / near deck
# = five. Two things cross them: the pool diamond (the subject) and the roof trusses.
# The wall base is a slope and is meant to be lost mid-way; the near end of the pool
# runs off the bottom of the canvas so the pool is not a contained lozenge.
s.pencil(WALLBASE, pressure=0.5)
s.pencil([pa, pb, pc, pd, pa], pressure=0.7)

# roof trusses, on the diagonal, lit only from the water below
s.pencil([(-0.05, 0.02), (0.42, 0.135), (1.05, 0.20)], pressure=0.5)
s.pencil([(-0.05, 0.155), (0.40, 0.045), (1.05, -0.03)], pressure=0.5)
s.pencil([(0.22, -0.05), (0.30, 0.30)], pressure=0.4)          # a hanger coming down

# a board, cantilevered over the far end, crossing the pool's far edge
s.pencil([(0.845, 0.415), (0.62, 0.475), (0.615, 0.492), (0.845, 0.432)], pressure=0.6)

# the ladder, on the near coping
s.pencil([(0.735, 0.735), (0.742, 0.700), (0.775, 0.690), (0.800, 0.707)], pressure=0.5)

s.mark("lamp_a", 0.285, 0.600)      # the big lamp, in the far wall of the pool
s.mark("lamp_b", 0.625, 0.520)      # the small one, further off
s.mark("exit",   0.105, 0.222)      # the one warm thing in the picture
print(s.look(grid=True))
