"""Landmarks, first guess. Verify each at feature scale."""
p = s.palette

# --- can I supply a colour darker than the box floor? -------------------
for probe in ("#0d0c10", (0.05, 0.05, 0.07), [13, 12, 16]):
    try:
        p["probe"] = probe
        print("accepted", repr(probe), "->", p.hex(p["probe"]),
              round(p.value_of(p["probe"]), 3))
    except Exception as e:
        print("rejected", repr(probe), type(e).__name__, e)

# --- landmark first guesses, read off the C2:F6 crop --------------------
s.mark("rim_l",   0.307, 0.251)     # leftmost point of the rim
s.mark("rim_r",   0.629, 0.263)     # rightmost point of the rim
s.mark("rim_top", 0.437, 0.121)     # top (far side) of the rim ellipse
s.mark("lip_f",   0.471, 0.364)     # front lip, lowest point of the rim
s.mark("base_c",  0.468, 0.696)     # lowest point of the mug's base
s.mark("hand_o",  0.728, 0.394)     # outer extremity of the handle
s.mark("tag_c",   0.868, 0.584)     # centre of the teabag tag

print(s.look(reference="ref.jpg", grid=True))
for c in ("C3", "F3", "D1", "D3", "D6", "F4", "G5"):
    print(c, s.look(region=cell(c), reference="ref.jpg", grid="fine"))
