from easel import Region
print("--- is any of the ground still showing? (umber_wash reads 0.425, warm) ---")
for nm, r in [("glass, near",  Region(0.86, 0.30, 0.94, 0.42)),
              ("glass, mid",   Region(0.62, 0.40, 0.72, 0.52)),
              ("foliage bank", Region(0.72, 0.68, 0.82, 0.80))]:
    c = s.sample(r); print(f"  {nm:14s} v={p.value_of(c):.3f} chroma={p.chroma_of(c):.3f}")
print("--- the three values, and the extremes ---")
for nm, r in [("roof lip",  Region(0.86, 0.075, 0.99, 0.105)),
              ("sky",       Region(0.30, 0.05, 0.55, 0.18)),
              ("near pane", Region(0.84, 0.42, 0.99, 0.72)),
              ("yard near", Region(0.02, 0.80, 0.24, 0.98)),
              ("eave",      Region(0.90, 0.145, 0.99, 0.175)),
              ("pot",       Region(0.688, 0.848, 0.724, 0.896))]:
    c = s.sample(r); print(f"  {nm:11s} v={p.value_of(c):.3f} chroma={p.chroma_of(c):.3f}")
paid = [r for r in s.history.records if r.kind not in ("dry", "look", "pencil", "erase")]
on_it = [r for r in paid if "subject" in (r.note or "")]
print(f"subject: {len(on_it)} of {len(paid)} -- {len(on_it)/len(paid):.0%}")
