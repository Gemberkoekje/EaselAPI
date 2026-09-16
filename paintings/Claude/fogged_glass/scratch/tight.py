from easel import Region
for nm, r in [("roof lip",   Region(0.930, 0.083, 0.990, 0.094)),
              ("eave member",Region(0.930, 0.118, 0.990, 0.133)),
              ("sky zenith", Region(0.40, 0.02, 0.60, 0.10)),
              ("near bar",   Region(0.797, 0.40, 0.810, 0.60)),
              ("brick base", Region(0.560, 0.930, 0.640, 0.985))]:
    c = s.sample(r); print(f"  {nm:12s} v={p.value_of(c):.3f} chroma={p.chroma_of(c):.3f}")
