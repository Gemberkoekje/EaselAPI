s.erase()                                     # the old drawing is buried; start clean
s.pencil([pa, pb, pc, pd, pa], pressure=0.6, smooth=False)

# a chair on the left deck: the one upright that crosses the wall base, and the only
# reason the empty half is not empty
CHAIR_L = [(0.105, 0.588), (0.128, 0.300)]
CHAIR_R = [(0.180, 0.602), (0.161, 0.307)]
CHAIR_BACK = [(0.124, 0.292), (0.119, 0.212), (0.157, 0.219), (0.163, 0.298)]
for line in (CHAIR_L, CHAIR_R, CHAIR_BACK):
    s.pencil(line, pressure=0.6, smooth=False)
s.pencil([(0.108, 0.560), (0.176, 0.335)], pressure=0.4, smooth=False)   # a brace

plan = [{"shape": POOL, "brush": "flat", "color": "water", "size": 0.13,
         "solid": True, "direction": "axis"}]
print(s.cost_line(plan))
water()
print(s.look(grid=True))
