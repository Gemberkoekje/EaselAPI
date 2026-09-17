print(s.budget_line())
paid = [r for r in s.history.records if r.kind not in ("dry", "look", "pencil", "erase")]
on_it = [r for r in paid if "subject" in r.note]
print(f"{len(on_it)} of {len(paid)} marks -- {len(on_it)/max(len(paid),1):.0%} on the subject")
print(s.compare(PLAN))
print("colour:", s.look())
print("values:", s.look(values=True))
