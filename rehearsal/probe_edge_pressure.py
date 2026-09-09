from easel import Session
s = Session(700, 300, ground="toned_grey", seed=3)
def edge(knots):
    def at(x):
        for (x0, y0), (x1, y1) in zip(knots, knots[1:]):
            if x0 <= x <= x1:
                return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
        return knots[-1][1]
    return at
top = edge([(0.02, 0.90), (0.25, 0.30), (0.48, 0.55)])
for i, pr in enumerate(["taper", "lift_off"]):
    off = i * 0.50
    x = 0.03
    while x < 0.47:
        s.stroke([(x + off, top(x)), (x + off, 1.02)], "bristle", "burnt_umber",
                 size=0.10, load=0.9, pressure=pr)
        x += 0.026
print(s.look())
