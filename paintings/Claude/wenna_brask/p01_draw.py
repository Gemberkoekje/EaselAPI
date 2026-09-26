"""Pass 1: the drawing. Guides only -- free, shown by look(), never exported."""
import os

os.makedirs("looks", exist_ok=True)
s.erase()

for shp, note in ((mill, "mill"), (kerchief, "kerchief"), (knot, "knot"), (face, "face"),
                  (neck, "neck"), (shawl, "shawl"), (fist, "fist"), (thumb, "thumb"),
                  (cap, "cap"), (lantern, "lantern"), (base, "base")):
    s.guide(shp.closed, note=note)
for path, note in ((ring, "ring"), (rake, "rake"), (mouth, "mouth"), (bracket, "bracket"),
                   (brace, "brace")):
    s.guide(path, note=note)
for i, path in enumerate(folds + tails):
    s.guide(path, note=f"fold {i + 1}" if i < len(folds) else "tail")
for (x, y), note in ((far_eye, "far eye"), (near_eye, "near eye"), (flame_at, "flame")):
    s.guide([(x - 0.012, y), (x + 0.012, y)], note=note)

print(s.look(grid=True, path=os.environ.get("LOOK", "looks/01-drawing.png")))
