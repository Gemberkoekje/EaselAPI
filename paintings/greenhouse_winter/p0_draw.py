# Pass 0: no paint. The arrangement in graphite, looked at with the grid, before
# a mass is spent on it. Every line here is a mass boundary or a glazing bar.
print("ground:", round(p.value_of(s.sample()), 2))
mixtures(verbose=True)
print("split:", sum(SPLIT.values()), SPLIT)
s.erase()

for shape in (far_glass(), base_wall(), right_wall(), left_wall(), right_roof(), left_roof()):
    s.pencil(shape.closed, pressure=0.45, smooth=False)
for side in (+1, -1):
    for shape in (bench_top(side), bench_front(side), bench_end(side)):
        s.pencil(shape.closed, pressure=0.6, smooth=False)
s.pencil(floor().closed, pressure=0.35, smooth=False)
s.pencil(bloom().closed, pressure=0.4)
for line in (wall_verticals(+1) + wall_verticals(-1) + far_verticals() + far_transoms()
             + rafters(+1) + rafters(-1)):
    s.pencil(line, pressure=0.3, smooth=False)
s.pencil(wall_transom(+1), pressure=0.3, smooth=False)
s.pencil(wall_transom(-1), pressure=0.3, smooth=False)

for xm, row in ((XR, RIGHT_FRONT), (XRB, RIGHT_BACK), (XL, LEFT_FRONT)):
    for dm, w, h, kind in row:
        if kind == "tipped":
            g = tipped_geo(xm, dm, w, h)
            s.pencil(g["body"].closed, pressure=0.6, smooth=False)
            s.pencil(g["mouth"].closed, pressure=0.6)
            continue
        g = pot_geo(xm, dm, w, h)
        s.pencil(g["body"].closed, pressure=0.6, smooth=False)
        s.pencil(g["rim"].closed, pressure=0.6)
        s.pencil(g["opening"].closed, pressure=0.4)
body, top, hw, sy = can_geo()
s.pencil(body.closed, pressure=0.6, smooth=False)
print(s.compare(PLAN))
print(s.look(grid=True))
