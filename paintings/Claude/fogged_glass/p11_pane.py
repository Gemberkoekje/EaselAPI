# Settling the subject. The near pane went washed out, and the glazing grid is
# mechanically regular -- so: knock the pane back, make the film uneven the way
# condensation actually is, and give one pane less of it than its neighbours.
from easel import polygon

p["cool"] = p.at_value(p.desaturate(p.mix(p["neutral"], "viridian", 0.12), 0.40), 0.24)
p["thick"] = p.at_value(p.mix(p["neutral"], "titanium_white", 0.50), 0.70)

def along(hm, d0, d1, n=6):
    return [P(WALL, hm, d0 + (d1 - d0) * i / (n - 1.0)) for i in range(n)]

# --- the whole near pane back a little: you are looking into a dark greenhouse
for hm, sz, op in [(1.88, 0.120, 0.10), (1.46, 0.135, 0.11), (1.04, 0.140, 0.09)]:
    s.glaze(along(hm, 4.6, 1.30), "cool", opacity=op, size=sz, note="subject")

# --- the film is not even: three places where it has gathered thick, and they are
#     not the same size or shape as each other
s.stroke([(0.822, 0.300), (0.892, 0.268), (0.958, 0.286)], "bristle", "thick",
         size=0.052, load=0.75, load_falloff=0.30, opacity=0.40,
         pressure="swell", note="subject")
s.stroke([(0.998, 0.608), (0.930, 0.640), (0.884, 0.618)], "bristle", "thick",
         size=0.038, load=0.60, load_falloff=0.35, opacity=0.34,
         pressure="swell", note="subject")
s.stroke([(0.700, 0.402), (0.752, 0.386), (0.786, 0.404)], "bristle", "thick",
         size=0.026, load=0.50, load_falloff=0.35, opacity=0.28,
         pressure="swell", note="subject")

# --- one pane with less film on it than its neighbours, so the grid is not a grid
pane = polygon([P(WALL, 2.00, 2.50), P(WALL, 2.00, 1.95),
                P(WALL, 1.56, 1.95), P(WALL, 1.56, 2.50)]).inset(0.009)
s.block_in(pane, "bristle", "cool", direction=-23, density=0.85, size=0.022,
           load=0.55, load_falloff=0.30, opacity=0.42, note="subject")
s.stroke([(0.684, 0.478), (0.726, 0.430), (0.742, 0.360)], "round_hard", "leafmid",
         size=0.011, pressure=[0.0, 1.0, 0.3], load=0.85, opacity=0.65,
         jitter=0.014, note="subject")
s.stroke([(0.776, 0.520), (0.756, 0.452), (0.772, 0.388)], "round_hard", "leaflit",
         size=0.008, pressure=[0.2, 0.9, 0.0], load=0.8, opacity=0.6,
         jitter=0.014, note="subject")
