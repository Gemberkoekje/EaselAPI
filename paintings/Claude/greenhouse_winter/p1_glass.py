# Pass 1: the furthest masses, which are all glass. The side walls and the roof
# wedges go down first and spill inward; the end wall goes on last with a clean
# contour, so its gable and its sides are the drawn line and not a staircase of
# chisel ends. Density under 1 so the ground breathes through: the fog and the
# dirt on the panes are in it already.

# The right wall: strokes fanning out from behind the end wall's edge along the
# wall's own lines, sky-light at the top and the fogged garden at the bottom.
# Each one sits at a different height on the wall, so no two are parallel.
rows = [(2.25, 0.65, 0.17), (1.95, 0.64, 0.18), (1.65, 0.62, 0.19), (1.35, 0.60, 0.19),
        (1.05, 0.57, 0.19), (0.75, 0.54, 0.19), (0.45, 0.51, 0.18)]
for hm, v, size in rows:
    a, b = P(HALF, hm, 5.0), P(HALF, hm, 1.2)
    s.stroke([a, b], "flat", p.at_value("glass_right", v), size=size, opacity=0.9,
             load=1.0, load_falloff=0.15, pressure="even", note="glass right")
# the near half of the wall, where the fan opens wider than the brush; these
# land light at their far end so they have no visible start
for hm, v in ((1.8, 0.63), (1.2, 0.585), (0.6, 0.525)):
    a, b = P(HALF, hm, 3.2), P(HALF, hm, 1.2)
    s.stroke([a, b], "flat", p.at_value("glass_right", v), size=0.16, opacity=0.85,
             load=1.0, load_falloff=0.15, pressure="press_in", note="glass right")

# the left wall: passes along the eaves line, which is the edge that shows
s.block_in(left_wall(), "flat", "glass_left", size=0.10, density=0.9, direction=22,
           note="glass left")
# the roof wedges: passes parallel to the gable slope each one ends on; a flat,
# because a comb here would run the same way as the rafters that go on later
s.block_in(right_roof(), "flat", "roof", size=0.12, density=0.9, direction=41, note="roof")
s.block_in(left_roof(), "flat", "roof", size=0.10, density=0.9, direction=140, note="roof")

# the end wall, last, its outline drawn by the contour pass
plan = {"shape": far_glass(), "brush": "flat", "color": "glass_far", "size": 0.115,
        "density": 0.85, "direction": 88, "edge": "clean"}
print(s.cost_line(plan))
s.block_in(far_glass(), "flat", "glass_far", size=0.115, density=0.85, direction=88,
           edge="clean", load_falloff=0.3, note="glass far")
print(s.budget_line())
print(s.look(grid=True))
print(s.look(values=True))
