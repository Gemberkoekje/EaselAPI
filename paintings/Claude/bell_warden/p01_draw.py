"""Pass 1: the drawing. Guides only -- free, shown by look(), never exported."""
import os

os.makedirs("looks", exist_ok=True)
s.erase()

for shp, note in ((plinth_top, "plinth top"), (plinth_front, "plinth front"),
                  (plinth_side, "plinth side"), (wing, "wing"), (body, "gargoyle"), (tail, "tail"),
                  (head_top, "head top"), (cheek, "cheek"), (chest_lit, "chest"),
                  (shoulder_lit, "shoulder"), (back_lit, "back"), (haunch_lit, "haunch"),
                  (wing_lit, "wing lit")):
    s.guide(shp.closed, note=note)
for i, tip in enumerate(finger_tips):
    s.guide([wrist, tip], note=f"finger {i + 1}")

print(s.look(grid=True, path="looks/01c-drawing.png"))
