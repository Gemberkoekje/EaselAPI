from easel import Session, polygon
import collections, math
s = Session(640, 480, ground="toned_warm_grey", seed=3, out_dir="pr")
s.palette["d"] = s.palette.mix("ultramarine", "burnt_umber", 0.45)
sh = polygon([(0.20, 0.42), (0.80, 0.40), (0.80, 0.52), (0.20, 0.54)])

for d in (0, 90, [0, 90], [0, 30, 60, 90]):
    t = s.scratch()
    n0 = len(t.history.records)
    t.block_in(sh, "bristle", "d", size=0.036, density=1.0, solid=True, direction=d)
    recs = t.history.records[n0:]
    angs = collections.Counter()
    for r in recs:
        p = r.points
        if len(p) >= 2:
            a = math.degrees(math.atan2(p[-1][1] - p[0][1], p[-1][0] - p[0][0])) % 180
            angs[round(a / 15) * 15 % 180] += 1
    print(f"direction={str(d):18s} records {len(recs):3d}  pass angles {dict(sorted(angs.items()))}")
