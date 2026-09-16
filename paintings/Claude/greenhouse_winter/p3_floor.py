# Pass 3: the ground. The aisle floor, lit a little at the far end by what comes
# through the end wall; the brick plinth under the glass; and the dark under both
# benches, which is the deepest value in the picture and goes down solid because
# things will stand in front of it.
s.dry()
s.block_in(aisle(), "flat", "floor", size=0.15, density=0.9, direction=(93, 8), note="floor")
far_floor = polygon([(0.20, 0.77), (0.44, 0.77), (0.50, 0.90), (0.15, 0.90)])
s.scumble(far_floor, "floor_far", "floor", 5, brush="flat", direction=3, overhang=0.2,
          load=1.0, load_falloff=0.0, opacity=0.8, jitter=0.01, size_jitter=0.03, note="floor far")

# the plinth: a plane, solid, along its own length; its top course a shade lighter
s.block_in(base_wall(), "flat", "brick", size=0.05, density=1.0, solid=True, direction="axis",
           opacity=1.0, pressure="even", note="plinth")
# under the staging: a clean contour, so the dark stops at the bench's far edge
# instead of spilling up onto the end wall behind it
for side in (+1, -1):
    shape = under_bench(side)
    print("under", side, "cost", s.cost({"shape": shape, "brush": "flat", "size": 0.035,
                                          "direction": "axis", "solid": True, "edge": "clean"}))
    s.block_in(shape, "flat", "under", size=0.035, density=1.0, solid=True, direction="axis",
               edge="clean", opacity=1.0, pressure="even", note="under bench")
print(s.budget_line())
print(s.look(grid=True))
print(s.look(values=True))
