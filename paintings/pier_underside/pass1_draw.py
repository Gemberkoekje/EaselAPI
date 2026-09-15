s.erase()
s.guide([(0.0, 0.625), (1.0, 0.625)])
for b in beams():
    s.guide(b)

s.pencil(deck().closed, pressure=0.85)
s.pencil(slot().closed, pressure=0.8)
s.pencil(water().closed, pressure=0.7)
for q in piles():
    s.pencil(q.closed, pressure=0.8)

s.look(grid=True, path="out/03_drawing.png")
