# Paints nothing. The finished picture and the time-lapse.
print(s.export("painting.png"))
print(s.timelapse_gif("painting.gif", fps=8.0, every=3, scale=320))
print(s.budget_line())
share()
print(s.compare(PLAN))
