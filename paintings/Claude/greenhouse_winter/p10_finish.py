# Pass 10: edges and incident. Lose three edges: the dark under each bench into
# the aisle floor, along its own line, and the far floor into the plinth. Then
# legs under the staging, barely lighter than the dark they stand in, and two
# dead leaves on the lit bench by the big pot.
s.dry()
s.smudge([P(BF, 0, 4.1), P(BF, 0, 3.4), P(BF, 0, 2.8), P(BF, 0, 2.35)])
s.smudge([P(-BF, 0, 4.1), P(-BF, 0, 3.4), P(-BF, 0, 2.8), P(-BF, 0, 2.35)])
s.smudge([P(-0.6, 0, FAR), P(0.0, 0, FAR), P(0.6, 0, FAR)])
p["leg"] = p.at_value("wood", 0.30)
for side, d in ((+1, 2.3), (+1, 3.4), (-1, 3.0)):
    a, b = P(side * BF, BENCH - 0.1, d), P(side * BF, 0, d)
    s.stroke([a, b], "round_hard", "leg", size=0.007, opacity=0.8, pressure=[0.9, 1.0, 0.6], note="leg")
s.dab(0.62, 0.86, "round_hard", "terra_dk", size=0.012, press=2, tip_wobble=0.7, note="leaf")
s.stroke([(0.70, 0.905), (0.715, 0.90), (0.725, 0.91)], "round_hard", p.at_value("stalk", 0.50),
         size=0.006, opacity=0.85, pressure="swell", tip_wobble=0.6, note="leaf")
print(s.budget_line())
print(s.look(grid=True))
print(s.look(values=True))
print(s.compare(PLAN))
