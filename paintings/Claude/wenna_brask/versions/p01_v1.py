"""Pass 1: the drawing. Guides only -- free, shown by look(), never exported."""
import os

os.makedirs("looks", exist_ok=True)
s.erase()

for shp, note in ((mill, "mill"), (kerchief, "kerchief"), (knot, "knot"), (face, "face"),
                  (neck, "neck"), (shawl, "shawl"), (dress, "dress"), (upper_arm, "upper arm"),
                  (cuff, "cuff"), (forearm, "forearm"), (fist, "fist"), (cap, "cap"),
                  (lantern, "lantern"), (base, "base")):
    s.guide(shp.closed, note=note)
s.guide(ring, note="ring")
s.guide(rake, note="rake")
s.guide(mouth, note="mouth")
for (x, y), note in ((far_eye, "far eye"), (near_eye, "near eye"), (flame_at, "flame")):
    s.guide([(x - 0.012, y), (x + 0.012, y)], note=note)

print(s.look(grid=True, path=os.environ.get("LOOK", "looks/01-drawing.png")))
