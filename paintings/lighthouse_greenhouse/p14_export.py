# Export. Paints nothing.
print(s.budget_line())
paid = [r for r in s.history.records if r.kind not in ("dry", "look", "pencil", "erase")]
on_it = [r for r in paid if "subject" in r.note]
print(f"subject: {len(on_it)} of {len(paid)} marks -- {len(on_it) / max(len(paid), 1):.0%}")
print(s.export("paintings/lighthouse_greenhouse/painting.png"))
print(s.timelapse_gif("paintings/lighthouse_greenhouse/painting.gif", fps=6.0, every=2, scale=512))
