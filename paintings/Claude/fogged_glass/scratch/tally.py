paid = [r for r in s.history.records if r.kind not in ("dry", "look", "pencil", "erase")]
buckets = {}
for r in paid:
    buckets[r.note or "(none)"] = buckets.get(r.note or "(none)", 0) + 1
for k, v in sorted(buckets.items(), key=lambda kv: -kv[1]):
    print(f"  {k:10s} {v:4d}  {v/len(paid):5.0%}")
on_it = [r for r in paid if "subject" in (r.note or "")]
print(f"subject: {len(on_it)} of {len(paid)} marks -- {len(on_it)/max(len(paid),1):.0%}")
