# The last strokes go to the weakest passage: the two green pots, whose foliage
# is a smooth clot. Leaves poking out of the silhouette, dark and lit, break it.
s.dry()
leaves = [((0.53, 0.66), (0.505, 0.633), "leaf_dk"), ((0.58, 0.656), (0.607, 0.63), "leaf_dk"),
          ((0.548, 0.637), (0.538, 0.607), "leaf_lit"),
          ((0.12, 0.58), (0.099, 0.559), "leaf_dk"), ((0.165, 0.576), (0.186, 0.553), "leaf")]
for a, b, col in leaves:
    s.stroke([a, b], "round_hard", col, size=0.007, opacity=0.9, pressure="swell", tip_wobble=0.5,
             note="subject leaves")
print(s.budget_line())
print(s.look(region="D5:G7"))
print(s.look(region="A5:C7"))
