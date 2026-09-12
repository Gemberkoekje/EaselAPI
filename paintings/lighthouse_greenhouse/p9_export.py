# Export. Paints nothing.
print(s.budget_line())
print(s.export("painting.png"))
print(s.timelapse_gif("painting.gif", fps=6.0, every=2, scale=512))
