# the drawing -- graphite is free; nothing here counts against the budget
s.pencil(scr.closed, pressure=0.6, smooth=False)          # the glass
s.pencil(bezel.closed, pressure=0.45, smooth=False)       # the bezel
s.pencil([(0.478, 0.583), (0.532, 0.583), (0.528, 0.648), (0.482, 0.648)], pressure=0.5, smooth=False)   # stand neck
s.pencil([(0.428, 0.648), (0.590, 0.655)], pressure=0.5)  # stand base
s.pencil([(0.0, 0.645), (1.0, 0.645)], pressure=0.4)      # desk back edge
s.pencil([(0.0, 0.865), (1.0, 0.865)], pressure=0.5)      # desk front edge
s.pencil(kb.closed, pressure=0.55, smooth=False)          # keyboard
s.pencil(s.circle(cell("G6"), 0.032).closed, pressure=0.55)  # mug body
s.pencil(pool.closed, pressure=0.3, smooth=False)         # the light pool, barely
s.look(grid=True)
