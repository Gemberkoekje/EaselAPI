exec(open("_pal.py").read())
order = ["under","crack","leaf_dk","ink","soil","pot_shad","leaf_mid","sill_face","wall_dk",
         "pot_mid","bar","wall","sill_shad","leaf_lit","wall_lit","pot_lit","bar_lit",
         "leaf_hot","sill_lit","pot_rim","glass_low","sill_hot","glass","glass_hot"]
for n in order:
    print(f"{n:10s} {p.hex(p[n])}  {p.value_of(p[n]):.2f}")
print("strokes:", s.stroke_count)
print(s.look(grid=True))
