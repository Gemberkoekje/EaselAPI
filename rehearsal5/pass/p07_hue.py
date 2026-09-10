p = s.palette

def tv(base, target):
    lo, hi = 0.0, 1.0
    for _ in range(24):
        mid = (lo + hi) / 2
        if p.value_of(p.mix(base, "titanium_white", mid)) < target:
            lo = mid
        else:
            hi = mid
    return p.mix(base, "titanium_white", (lo + hi) / 2)

print("reference wood: dark #6F583D  mid #8C765D  light #9F8D79  upper-right #7D6B53")
print()
for d in (0.30, 0.45, 0.60, 0.75):
    base = p.desaturate(p.mix("yellow_ochre", "burnt_sienna", 0.30), d)
    row = [f"desat {d:.2f}:"]
    for t in (0.37, 0.46, 0.53, 0.60):
        row.append(f"{t}->{p.hex(tv(base, t))}")
    print("  ".join(row))
print()
print("earth+white (calibration's warm grey route):")
for r in (0.35, 0.5, 0.65, 0.8):
    print(f"  umber+white {r}: {p.hex(p.mix('burnt_umber', 'titanium_white', r))}"
          f" v={p.value_of(p.mix('burnt_umber', 'titanium_white', r)):.2f}")
print()
print("ochre/umber/white blends:")
for oc in (0.25, 0.4, 0.55):
    base = p.mix("burnt_umber", "yellow_ochre", oc)
    for d in (0.0, 0.3):
        b2 = p.desaturate(base, d) if d else base
        row = [f"  umber+ochre {oc} desat {d}:"]
        for t in (0.37, 0.46, 0.53, 0.60):
            row.append(f"{t}->{p.hex(tv(b2, t))}")
        print("  ".join(row))
