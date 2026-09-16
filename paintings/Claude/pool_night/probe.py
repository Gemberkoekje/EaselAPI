for name, pl in (("far deck L", span("C4","C5")), ("far deck M", span("D4","E4")),
                 ("far deck R", span("G4","G5")), ("deck left", span("A5","B5")),
                 ("streak col", span("C4","C4"))):
    print(f"{name:11s} {p.value_of(s.sample(pl)):.3f}")
