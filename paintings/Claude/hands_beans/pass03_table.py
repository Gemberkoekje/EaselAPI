# The table: a graded field that is most of the picture. Light from the upper left,
# dying into the lower right. Two overlapping ramps, and things crossing it.
LIT  = polygon([(-0.06, -0.06), (1.06, -0.06), (1.06, 0.22), (0.50, 0.46), (-0.06, 0.74)])
DARK = polygon([(-0.06, 0.64), (0.50, 0.38), (1.06, 0.14), (1.06, 1.06), (-0.06, 1.06)])
AXIS = ((-0.06, 0.70), (1.06, 0.18))

s.scumble(LIT,  "tbl_lit", "table",    7, direction=AXIS,
          load=1.0, load_falloff=0.0, opacity=0.95)
s.scumble(DARK, "table",   "tbl_deep", 8, direction=AXIS,
          load=1.0, load_falloff=0.0, opacity=0.95)
# something has to cross it: three starved passes, none parallel, ends off the canvas
s.stroke([(-0.06, 0.20), (0.44, 0.30), (1.06, 0.33)], "bristle", "table",
         size=0.085, load=0.42, opacity=0.45, pressure="swell")
s.stroke([(1.06, 0.62), (0.52, 0.72), (-0.06, 0.70)], "bristle", "tbl_deep",
         size=0.070, load=0.38, opacity=0.40, pressure="swell")
s.stroke([(0.16, -0.06), (0.30, 0.46), (0.36, 1.06)], "bristle", "tbl_lit",
         size=0.060, load=0.35, opacity=0.30, pressure="swell")
print(s.cost_line([]))
