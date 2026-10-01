"""Free: the arrangement flat, at the values planned."""
places = {wall: 0.27}
for i, r in enumerate(rays):
    places[r] = 0.42
places[mountain] = 0.32
places[floor] = 0.18
places[ell_px(530, 450, 230, 200)] = (0.55, [wall])      # the lamplight on the relief
places[tub] = 0.10
places[uk_wing] = 0.22
for shape in (uk_body, uk_collar, uk_arm, uk_hand):
    places[shape] = 0.13
places[uk_head] = 0.55
places[d_body] = 0.14
for shape in (d_head, *d_ears):
    places[shape] = 0.15
places[table_top] = 0.42
places[a_body] = 0.13
places[a_hair] = 0.12
places[a_head] = 0.50
places[b_body] = 0.11
places[b_hood] = 0.12
print(s.thumbnail(places, size=384, path="out/notan_01.png"))
