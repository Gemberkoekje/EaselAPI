from easel import Session, region

s = Session(900, 300, ground="toned_grey", seed=5)
left, mid, right = region("all").split_h(3)
for r in (left, mid, right):
    s.block_in(r, "bristle", "burnt_umber", density=1.0, size=0.1)
s.dry()
s.block_in(left,  "bristle", s.palette.tint("burnt_umber", 0.6), density=1.0, size=0.1)
s.stroke([(0.02, 0.5), (0.31, 0.5)], "round_hard",
         s.palette.tint("burnt_umber", 0.6), size=0.03)      # hard
s.smudge([(0.35, 0.3), (0.35, 0.7)], size=0.09)              # soft
print(s.look())
