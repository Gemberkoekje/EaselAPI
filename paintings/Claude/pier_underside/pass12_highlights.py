p = s.palette
p["spark"] = p.at_value(p.mix("titanium_white", "lemon_yellow", 0.18), 0.935)

# ten marks, and they are the last ten. Every one added makes the others count less.
H = [(0.735, 0.7055, 0.030), (0.842, 0.7135, 0.022), (0.646, 0.6995, 0.018),
     (0.928, 0.7215, 0.017), (0.792, 0.6925, 0.014)]
plan = [{"points": [(x, y), (x + ln, y + 0.0015)], "brush": "liner", "color": "spark",
         "size": 0.0045, "pressure": [0.0, 1.0, 0.1], "load": 0.9,
         "load_falloff": 0.6, "opacity": 0.85} for x, y, ln in H]
# and three on the wood, where the water throws it hardest
for x, y, ln in [(0.815, 0.5585, 0.026), (0.896, 0.5205, 0.020), (0.706, 0.5885, 0.016)]:
    plan.append({"points": [(x, y), (x + ln * 0.6, y - 0.0035), (x + ln, y)],
                 "brush": "liner", "color": "spark", "size": 0.004,
                 "pressure": [0.0, 1.0, 0.0], "load": 0.85, "load_falloff": 0.7,
                 "opacity": 0.78, "note": "subject"})
print(s.cost_line(plan))
s.paint(plan)
s.look(path="out/15_highlights.png")
