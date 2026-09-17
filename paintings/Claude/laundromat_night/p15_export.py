print(s.budget_line())
paid = [r for r in s.history.records if r.kind not in ("dry", "look", "pencil", "erase")]
sig = [r for r in paid if "signature" in r.note]
on_it = [r for r in paid if "subject" in r.note and "signature" not in r.note]
body = [r for r in paid if "signature" not in r.note]
print(f"subject: {len(on_it)} of {len(body)} paid marks -- "
      f"{len(on_it)/max(len(body),1):.0%}  (planned 45%)")
print(f"signature marks (free): {len(sig)}")
print(s.compare(PLAN))
print("export:  ", s.export("painting.png"))
print("gif:     ", s.timelapse_gif("painting.gif", fps=9.0, every=2, scale=480))
print("sheet:   ", s.contact_sheet("contact_sheet.png", columns=6))
