from easel import Session

s = Session(600, 400, ground="toned_grey", seed=3)
p = s.palette

# -- the value-planning snippet from step 2
p["dark"] = p.mix("ultramarine", "burnt_umber", 0.55)
p["mid"]  = p.tint(p.mix("yellow_ochre", "burnt_sienna", 0.35), 0.40)
p["lit"]  = p.tint(p.mix("yellow_ochre", "burnt_sienna", 0.40), 0.74)
for name in ("dark", "mid", "lit"):
    print(name, p.hex(p[name]), round(p.value_of(p[name]), 2))

# -- the silhouette snippet from "a region is a rectangle"
def edge(knots):
    def at(x):
        for (x0, y0), (x1, y1) in zip(knots, knots[1:]):
            if x0 <= x <= x1:
                return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
        return knots[-1][1]
    return at

top = edge([(0.33, 1.02), (0.46, 0.66), (0.58, 0.43), (0.74, 0.50), (1.02, 0.68)])
x = 0.345
while x < 1.0:
    s.stroke([(x, top(x)), (x, 1.02)], "bristle", "dark", size=0.13, load=0.9)
    x += 0.033
print("silhouette strokes:", s.stroke_count)
print(s.look())
