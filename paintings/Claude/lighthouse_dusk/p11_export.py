# Export. Paints nothing.
print(s.budget_line())
print(s.export("paintings/Claude/lighthouse_dusk/painting.png"))
print(s.timelapse_gif("paintings/Claude/lighthouse_dusk/painting.gif", fps=6.0, every=2, scale=512))
