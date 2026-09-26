"""Pass 1: the drawing. Guides only -- free, shown by look(), never exported."""
import os

os.makedirs("looks", exist_ok=True)

for shp, note in ((glow, "glow"), (pillar, "pillar"), (floor, "floor"), (pool, "pool"),
                  (plinth_top, "plinth top"), (plinth_front, "plinth front"),
                  (plinth_side, "plinth side"), (body, "gargoyle"), (tail, "tail")):
    s.guide(shp.closed, note=note)

for shp, note in ((face_lit, "face lit"), (chest_lit, "chest lit"),
                  (wing_edge_lit, "wing edge lit"), (arm_lit, "arm lit"), (haunch_lit, "haunch lit")):
    s.guide(shp.closed, note=note)

s.guide([(0.33, 0.30), (0.35, 0.25), (0.385, 0.235)], note="horn near")
s.guide([(0.35, 0.305), (0.38, 0.265), (0.415, 0.255)], note="horn far")
s.guide([(0.00, 0.00), (0.34, 0.60)], note="beam axis")

print(s.look(grid=True, path="looks/01-drawing.png"))
