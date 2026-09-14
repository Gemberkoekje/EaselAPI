# Pass 9: the condensation. Drips on the near panes of the right wall, each
# running down from a bead and none of them straight, a few beads low on the
# same panes, and two paler runs on the dirty lower panes of the end wall.
s.dry()
p["drip"] = p.at_value(p.mix("glass_right", "titanium_white", 0.3), 0.68)
p["drip_far"] = p.at_value("glass_far", 0.83)
p["bead"] = p.at_value(p.mix("glass_right", "titanium_white", 0.5), 0.74)
drips = [((0.79, 0.53), (0.793, 0.62), (0.787, 0.70)),
         ((0.703, 0.505), (0.706, 0.57), (0.701, 0.63)),
         ((0.93, 0.53), (0.927, 0.62), (0.934, 0.74))]
for a, b, c in drips:
    s.stroke([a, b, c], "liner", "drip", size=0.0035, opacity=0.8, pressure=[1.0, 0.7, 0.4], note="drip")
    s.dab(c[0], c[1] + 0.006, "round_hard", "bead", size=0.006, press=2, tip_wobble=0.6, note="bead")
for x, y in ((0.762, 0.66), (0.872, 0.69), (0.735, 0.60)):
    s.dab(x, y, "round_hard", "bead", size=0.0045, press=2, tip_wobble=0.7, note="bead")
for a, b in (((0.27, 0.49), (0.272, 0.60)), ((0.383, 0.475), (0.386, 0.585))):
    s.stroke([a, b], "liner", "drip_far", size=0.0035, opacity=0.8, pressure=[1.0, 0.5], note="drip")
print(s.budget_line())
print(s.look(region="E4:H7"))
print(s.look(grid=True))
