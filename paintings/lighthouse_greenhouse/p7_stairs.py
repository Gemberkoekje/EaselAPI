# Pass 7: the outside stair and the pots on it, in front of the tower. Each
# visible turn of the helix is one flat stroke of dark iron along the curve --
# vertical where it meets the silhouette, flattest across the middle, run a
# little past both edges where the far side of the stair peeks out beyond the
# tower -- and one thinner, lighter stroke along its top edge for the treads
# catching the fog's light. Then eleven terracotta pots standing on the
# treads, three or four to a turn, unevenly spaced, no two the same size, and
# each growing something different or nothing: one has tipped over.
p["tread"] = p.at_value("tower_sh", 0.50)
for k in range(3):
    arc = stair_arc(k)
    s.stroke(arc, "flat", "iron", size=0.012, opacity=0.95, load=1.0, load_falloff=0.0,
             pressure="even", note="subject stair")
    s.stroke([(x, y - 0.0065) for x, y in arc], "liner", "tread", size=0.0045, opacity=0.9,
             pressure="even", note="subject treads")
pots = [  # (turn, angle round the tower, width, height, what grows in it)
    (0, 0.45, 0.017, 0.024, "sprig"), (0, 1.35, 0.021, 0.028, "tall"),  (0, 2.45, 0.015, 0.020, "empty"),
    (1, 0.70, 0.019, 0.026, "sprig"), (1, 1.60, 0.016, 0.022, "sprig"), (1, 2.30, 0.022, 0.030, "bushy"),
    (1, 2.85, 0.014, 0.019, "tipped"),
    (2, 0.35, 0.020, 0.027, "sprig"), (2, 1.10, 0.017, 0.023, "empty"), (2, 1.95, 0.023, 0.030, "tall"),
    (2, 2.70, 0.016, 0.021, "sprig"),
]
for k, th, w, h, kind in pots:
    x, y = stair_point(k, th)
    pot(x, y - 0.004, w, h, kind)
print(s.look(values=True))
print(s.look())
print(s.look(region="E3:G7"))
