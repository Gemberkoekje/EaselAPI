# Probe, rehearsed only: what brush and step the inward scumble picks on the
# bloom, and what the check says about it.
s.dry()
p["bloom_edge"] = s.sample(bloom(0.15))
before = len(s.history.records)
s.scumble(bloom(), "bloom_edge", "bloom_core", 8, direction="inward", note="bloom")
recs = s.history.records[before:]
r = recs[0]
print("record fields:", [k for k in vars(r).keys()])
for r in recs:
    prm = getattr(r, "params", {}) or {}
    print(r.kind, "size", prm.get("size"), "brush", prm.get("brush"), "via", prm.get("via"))
print(s.report(since=before))
