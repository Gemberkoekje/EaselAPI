from easel import Region
for nm, r in [("left of leaf", Region(0.855, 0.385, 0.895, 0.470)),
              ("above leaf",   Region(0.905, 0.320, 0.985, 0.372)),
              ("right of leaf",Region(0.986, 0.390, 0.999, 0.470)),
              ("below leaf",   Region(0.905, 0.487, 0.985, 0.540))]:
    c = s.sample(r)
    print(f"{nm:14s} v={p.value_of(c):.3f} c={p.chroma_of(c):.3f} {p.hex(c)}")
