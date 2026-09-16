# No paint: the pencil that still shows outside the pots and the can is rubbed
# out, then the export, the time-lapse, and the last looks.
s.erase(Region(0.44, 0.52, 1.0, 1.0))
s.erase(Region(0.0, 0.52, 0.34, 1.0))
print(s.export("painting.png"))
print(s.timelapse_gif("painting.gif", every=2, scale=320))
print(s.look())
print(s.look(values=True))
print(s.budget_line())
paid = [r for r in s.history.records if r.kind not in ("dry", "look", "pencil", "erase")]
on_it = [r for r in paid if "subject" in r.note]
print(f"subject: {len(on_it)} of {len(paid)} marks -- {len(on_it) / max(len(paid), 1):.0%}")
