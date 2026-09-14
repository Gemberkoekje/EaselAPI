# Pass 4: the staging. Each bench top is one solid plane with a clean contour, so
# its far edge and its back edge against the wall are the drawn line. The sun
# rakes across the right bench from behind, so it is the lit wood; the left bench
# sits lower in value against the pale left wall. Then the pots throw long
# shadows toward the viewer, one tapering stroke each, and the near things are
# drawn again in pencil on top of the paint, because the first drawing is under
# it now.
s.dry()
right = {"shape": bench_top(+1), "brush": "flat", "color": "wood_lit", "size": 0.06,
         "density": 1.0, "solid": True, "direction": 48, "edge": "clean"}
left = {"shape": left_top(), "brush": "flat", "color": "wood", "size": 0.045,
        "density": 1.0, "solid": True, "direction": 133, "edge": "clean"}
print(s.cost_line(right))
print(s.cost_line(left))
s.block_in(bench_top(+1), "flat", "wood_lit", size=0.06, density=1.0, solid=True,
           direction=48, edge="clean", opacity=1.0, pressure="even", note="bench")
s.block_in(left_top(), "flat", "wood", size=0.045, density=1.0, solid=True,
           direction=133, edge="clean", opacity=1.0, pressure="even", note="bench")
# the lit front edge of the left bench, and two board joints on the right
a, b = P(-BF, BENCH, FARB), P(-BF, BENCH, 1.15)
s.stroke([a, b], "flat", "wood_lit", size=0.022, opacity=0.85, load=1.0, load_falloff=0.1,
         pressure=[0.6, 1.0, 1.0], note="bench")
for xm in (0.78, 1.06):
    s.stroke([P(xm, BENCH, 4.1), P(xm, BENCH, 1.15)], "liner", "wood", size=0.004,
             opacity=0.55, pressure=[0.4, 0.8, 1.0], note="bench")

# the shadows the pots throw: a step or two below the lit wood, losing their far end
p["shadow"] = p.at_value("wood", 0.45)
for xm, dm, w, h in ((XR, 2.0, 0.16, 0.15), (XR, 2.55, 0.15, 0.14), (XR, 3.7, 0.13, 0.12),
                     (XR, 4.15, 0.16, 0.15), (XRB, 2.6, 0.16, 0.15), (XL, 2.9, 0.18, 0.17)):
    bx, by = P(xm, BENCH, dm)
    dx, dy = shadow_dir((bx, by))
    L = 0.30 * (h / 0.15) * (2.2 / dm) ** 0.5
    pts = [(bx, by), (bx + dx * L * 0.5 + 0.004, by + dy * L * 0.5), (bx + dx * L, by + dy * L)]
    s.stroke(pts, "round_hard", "shadow", size=w * F / dm * 0.9, opacity=0.7, load=1.0,
             load_falloff=0.0, pressure=[1.0, 0.85, 0.2], note="shadow")

# redraw the near things on the fresh paint
for xm, row in ((XR, RIGHT_FRONT), (XRB, RIGHT_BACK), (XL, LEFT_FRONT)):
    for dm, w, h, kind in row:
        if kind == "tipped":
            g = tipped_geo(xm, dm, w, h)
            s.pencil(g["body"].closed, pressure=0.5, smooth=False)
            s.pencil(g["mouth"].closed, pressure=0.5)
            continue
        g = pot_geo(xm, dm, w, h)
        s.pencil(g["body"].closed, pressure=0.5, smooth=False)
        s.pencil(g["rim"].closed, pressure=0.5)
body, top, hw, sy = can_geo()
s.pencil(body.closed, pressure=0.5, smooth=False)
print(s.budget_line())
print(s.look(grid=True))
print(s.look(values=True))
print(s.look(region="C5:F7"))
print(s.compare(PLAN))
