exec(open("_pal.py").read())
for n in ("leaf_dk","leaf_mid","leaf_lit","leaf_hot","stem"):
    print(f"{n:9s} {p.hex(p[n])} {p.value_of(p[n]):.2f}")
