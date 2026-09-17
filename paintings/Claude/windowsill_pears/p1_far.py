# Pass 1: the furthest masses. Window pane first, then the wall either side of it.
s.block_in(Region(0.13, -0.02, 0.73, 0.61), "flat", "window", density=0.9, size=0.16,
           direction=12, load=1.0, note="window pane")
s.block_in(Region(-0.02, -0.02, 0.15, 0.62), "flat", "wall", density=0.9, size=0.10,
           direction=84, load=1.0, overhang=0, note="wall left of window")
s.block_in(Region(0.71, -0.02, 1.02, 0.62), "flat", "wall", density=0.9, size=0.12,
           direction=84, load=1.0, overhang=0, note="wall right of window")
print("strokes:", s.stroke_count)
print(s.look(grid=True))
