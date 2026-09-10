REF = "C:/temp/Level1.jpg"

# the reference puts a shadow band under the front lip - I had painted light there
s.stroke([(0.370, 0.356), (0.440, 0.368), (0.502, 0.364)], "flat", "tea_lit",
         size=0.026, pressure="even", load=1.0, note="shadow under the lip")
# and the crewmate's head starts higher than I drew it
s.stroke([(0.376, 0.388), (0.440, 0.394), (0.498, 0.392)], "flat", "fig_dark",
         size=0.024, pressure="even", load=1.0, note="head top")
for y, size in [(0.432, 0.048), (0.520, 0.050)]:
    s.stroke([(0.374, y), (0.500, y + 0.003)], "flat", "fig_dark", size=size,
             pressure="even", load=1.0, note="solid crewmate")
print("D3/D4", s.stroke_count)

# the opening at the top right
s.stroke([(0.516, 0.162), (0.572, 0.186), (0.598, 0.220)], "flat", "tea",
         size=0.040, pressure="even", load=1.0, note="opening top right")
s.stroke([(0.530, 0.142), (0.580, 0.166)], "flat", "tea",
         size=0.028, pressure="even", load=1.0, note="opening top right")
print("E2", s.stroke_count)

# the legs, and the mug meeting its shadow
s.stroke([(0.392, 0.640), (0.462, 0.652), (0.502, 0.644)], "flat", "fig_dark",
         size=0.024, pressure="even", load=1.0, note="legs on the base")
print("D6", s.stroke_count)

print(s.compare(REF))
print(s.look(reference=REF))
