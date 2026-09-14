# Does a direction sequence price at the steepest angle in it, as the eighth
# session guessed? Measure the mechanism, not the failure.
from easel import Session, blob, polygon

s = Session(1024, 768, texture="rough", ground="toned_warm_grey", seed=17, out_dir="pr")
s.palette["d"] = s.palette.mix("ultramarine", "burnt_umber", 0.45)
A = s.aspect

wide = polygon([(0.20, 0.42), (0.80, 0.40), (0.80, 0.52), (0.20, 0.54)])   # wide, short
tall = polygon([(0.44, 0.18), (0.56, 0.18), (0.56, 0.78), (0.44, 0.78)])   # tall, narrow
lump = blob((0.5, 0.5), 0.18, wobble=0.40, points=15, seed=3, aspect=A)    # concave-ish

def c(shape, d, sz=0.036):
    return s.cost([{"shape": shape, "brush": "bristle", "color": "d", "size": sz,
                    "density": 1.0, "solid": True, "direction": d}])

for name, sh in (("wide", wide), ("tall", tall), ("lump", lump)):
    singles = {a: c(sh, a) for a in (0, 30, 60, 90, 120, 150)}
    worst = max(singles.values())
    print(f"\n{name}: singles {singles}")
    for seq in ([0, 90], [0, 30, 60, 90], [0, 30, 60, 90, 120, 150]):
        got = c(sh, seq)
        sum_of = sum(singles[a] for a in seq)
        print(f"  seq n={len(seq)}: cost {got:4d} | sum of its singles {sum_of:4d}"
              f" | n x worst-single {len(seq)*worst:4d}")
