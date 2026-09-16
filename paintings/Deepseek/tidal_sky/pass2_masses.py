# Pass 2: big masses first, biggest brush, back to front. Sky first, then water.
s.block_in(region("upper-half"), "bristle", "coral", density=0.8, size=0.18, direction="axis")
s.block_in(region("lower-half"), "bristle", "teal", density=0.8, size=0.18, direction="axis")
s.look(values=True, path="pass2_values.png")
