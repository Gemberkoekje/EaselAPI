# Finishing, and most of it goes on the passage this painting would have to
# apologise for: the rock, which came back a stack of horizontal bands with the
# tower's foot ghosting through it where the block-in ran thin.
s.dry()

# 1. Bury the foot. Two long solid strokes along the rock's own grain, ends run
#    off past the area so no chisel stops inside the picture -- the burying
#    recipe, laid by hand because it wants a direction the region would not give.
for path, v, size in (([(0.150, 0.848), (0.300, 0.868), (0.450, 0.888)], 0.195, 0.058),
                      ([(0.200, 0.894), (0.340, 0.914), (0.470, 0.930)], 0.170, 0.050)):
    s.stroke(path, "flat", p.at_value("rock", v), size=size, opacity=1.0,
             load=1.0, load_falloff=0.0, pressure="even", note="rock")

# 2. Break the banding. Four passes across the rock at an angle it has nowhere
#    else, starved so they read as surface and not as more bands.
for path, v, size, load, op in (
        ([(-0.04, 0.930), (0.26, 0.868), (0.52, 0.906)], 0.265, 0.030, 0.30, 0.65),
        ([(0.12, 1.020), (0.44, 0.952), (0.74, 0.982)], 0.230, 0.024, 0.26, 0.55),
        ([(0.30, 0.996), (0.62, 0.940)], 0.300, 0.017, 0.35, 0.7),
        ([(0.04, 0.876), (0.22, 0.916), (0.34, 0.980)], 0.175, 0.021, 0.40, 0.6)):
    s.stroke(path, "bristle", p.at_value("rock", v), size=size, load=load,
             opacity=op, pressure="swell", note="rock")

# 3. A plane on the rock's shoulder left of the tower, and the shadow the tower
#    casts into the rock it is standing in -- darkest where the two things meet,
#    losing its far end, and a step below the surface rather than at the bottom
#    of the box.
s.block_in(polygon([(-0.05, 0.790), (0.08, 0.806), (0.13, 0.842), (0.05, 0.874),
                    (-0.05, 0.856)]), "flat", p.at_value("rock", 0.305),
           size=0.022, density=1.0, solid=True, direction="axis", note="rock")
s.stroke([(0.135, 0.846), (0.255, 0.872), (0.372, 0.876)], "flat",
         p.at_value("rock", 0.150), size=0.020, opacity=0.85, load=1.0,
         load_falloff=0.0, pressure=[0.9, 1.0, 0.0], note="rock")
s.stroke([(0.146, 0.838), (0.230, 0.856)], "round_hard",
         p.at_value("rock", 0.145), size=0.009, opacity=0.9,
         pressure=[1.0, 0.0], note="rock")

# 4. One crevice and one dry-brush pass, so the near dark has something in it.
s.stroke([(0.62, 0.952), (0.74, 1.004), (0.80, 1.062)], "round_hard",
         p.at_value("rock", 0.145), size=0.011, opacity=0.9,
         pressure=[0.25, 1.0, 0.0], note="rock")
s.stroke([(0.06, 0.958), (0.30, 0.986), (0.48, 1.026)], "bristle",
         p.at_value("rock", 0.290), size=0.020, load=0.22, opacity=0.55,
         pressure="lift_off", note="rock")

s.dry()

# 5. The edges. The tower's right side is hard from the gallery to the rock, and
#    an image where every edge is equally sharp looks like clip-art. One stretch
#    of it goes, along the boundary's own curve and in one pass -- a second pass
#    puts back 60% of what the first took and leaves a thumbprint besides.
s.smudge([(0.3495, 0.392), (0.3545, 0.470), (0.3605, 0.548), (0.3655, 0.612)])
s.stroke([(0.338, 0.428), (0.362, 0.446), (0.380, 0.436)], "bristle",
         p.mix("tower_lit", "fog_low", 0.5), size=0.020, load=0.45, opacity=0.5,
         pressure="swell", note="edges")

# The two stair turns that stop dead at the silhouette: a stair going round the
# back should arrive at nothing, not at a chisel end.
s.stroke([(0.330, 0.478), (0.352, 0.460)], "bristle",
         p.mix("iron", "tower_lit", 0.45), size=0.012, load=0.4, opacity=0.55,
         pressure=[0.8, 0.0], note="edges")
s.stroke([(0.146, 0.601), (0.162, 0.608)], "bristle",
         p.mix("iron", "tower_sh", 0.5), size=0.011, load=0.4, opacity=0.5,
         pressure=[0.0, 0.8], note="edges")

# 6. Out in the water: one small stack, fog-grey rather than rock-dark because it
#    is a long way off, and the light the beam is putting on the sea beyond it.
s.block_in(blob((0.848, 0.806), 0.030, wobble=0.5, points=7, seed=17, aspect=0.55),
           "bristle", p.at_value("rock", 0.315), size=0.016, density=1.0,
           solid=True, direction=("axis", 70), note="sea")
s.stroke([(0.820, 0.836), (0.868, 0.844), (0.906, 0.838)], "bristle",
         p.at_value("sea_near", 0.585), size=0.009, load=0.4, opacity=0.7,
         pressure="swell", note="sea")
s.stroke([(0.62, 0.634), (0.82, 0.646), (1.06, 0.640)], "bristle",
         p.at_value("beam", 0.625), size=0.026, load=0.35, opacity=0.45,
         pressure=[0.0, 0.9, 0.4], note="subject beam")

# 7. Last: the gallery plate is a black rectangle, and a lit top edge is what
#    stops it being one.
s.stroke([(0.140, 0.2385), (0.256, 0.2415), (0.370, 0.2375)], "liner",
         p.at_value("iron", 0.42), size=0.004, opacity=0.75,
         pressure=[0.25, 1.0, 0.35], note="subject lantern")

# 8. The tower's foot. The lit band ran all the way down to the waterline at very
#    nearly the near sea's own value and floated there as a pale wedge with no
#    bottom. Below the last turn of the stair the shaft goes dark -- splash, weed,
#    and the shade of the rock it is standing in. Both marks are kept clear of the
#    lowest pot and laid starved, because what is underneath them is the expensive
#    part of this picture and a repair that buries it is not a repair.
s.stroke([(0.3480, 0.700), (0.3580, 0.780), (0.3700, 0.852)], "bristle",
         p.at_value("tower_lit", 0.345), size=0.030, load=0.60, opacity=0.75,
         pressure=[0.15, 0.85, 1.0], note="subject tower")
s.stroke([(0.158, 0.822), (0.262, 0.842), (0.372, 0.850)], "bristle",
         p.at_value("tower_sh", 0.255), size=0.034, load=0.35, opacity=0.5,
         pressure="swell", note="subject tower")

# 9. Two more on the near dark, at angles it has nowhere else.
s.stroke([(0.02, 0.928), (0.18, 0.954), (0.30, 0.942)], "bristle",
         p.at_value("rock", 0.275), size=0.018, load=0.25, opacity=0.5,
         pressure="swell", note="rock")
s.stroke([(0.60, 1.022), (0.82, 0.970), (1.02, 0.996)], "bristle",
         p.at_value("rock", 0.255), size=0.022, load=0.30, opacity=0.55,
         pressure=[0.3, 1.0, 0.0], note="rock")

print(s.look(grid=True))
print(s.look(values=True))
print(s.look(region="A6:E8"))
