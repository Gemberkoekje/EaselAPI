s.dry()
# The wet streaks on the far deck came out as columns of speckle -- scratches, not
# reflection. Buried under films that run ALONG the band at just under its measured
# value (0.36-0.41), so nothing new is introduced running across it. Two smooth
# marks are left in their place so the idea survives the repair.
for pts, size, op, val in [([(0.115, 0.592), (0.300, 0.470), (0.482, 0.390)], 0.160, 0.50, 0.345),
                           ([(0.455, 0.394), (0.700, 0.432), (1.035, 0.482)], 0.150, 0.45, 0.345),
                           ([(0.880, 0.560), (0.960, 0.612), (1.040, 0.668)], 0.090, 0.40, 0.320)]:
    s.glaze(pts, p.at_value("deck", val), opacity=op, size=size, pressure="swell")

s.stroke([(0.246, 0.628), (0.237, 0.542), (0.232, 0.482)], "bristle",
         p.at_value("deck", 0.45), size=0.022, load=0.90, opacity=0.50,
         load_falloff=0.55, pressure="lift_off")
s.stroke([(0.661, 0.508), (0.670, 0.438)], "bristle", p.at_value("deck", 0.43),
         size=0.018, load=0.85, opacity=0.45, load_falloff=0.6, pressure="lift_off")
print(s.look(region="B3:F6"))
