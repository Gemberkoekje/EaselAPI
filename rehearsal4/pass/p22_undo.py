"""Scrape the mug pass. A shaped block_in spills ~3/4 of a brush past its own
silhouette, so a 0.12 brush on a mass 0.32 wide loses the shape entirely."""
print("before:", s.stroke_count)
s.undo(72)
print("after:", s.stroke_count)
print(s.look())
