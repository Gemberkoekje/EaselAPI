paid = [r for r in s.history.records
        if r.kind not in ("dry", "look", "pencil", "erase")]
on_it = [r for r in paid if "subject" in r.note]
print(f"{len(on_it)} of {len(paid)} marks -- {len(on_it) / max(len(paid), 1):.0%} on the subject")
from collections import Counter
c = Counter(r.note.split()[0] if r.note else "(none)" for r in paid)
for k, v in c.most_common():
    print(f"  {v:4d}  {k}")
print(s.look(values=True))
