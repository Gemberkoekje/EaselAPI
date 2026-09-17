# The furthest thing: flat overcast winter light, darker at the zenith, hazy at the
# horizon. Two overlapping ramps off the frame, then crossers that are not parallel.
from easel import Region

s.scumble(Region(-0.04, -0.04, 1.04, 0.31), "sky", "skymid", 7, direction=3,
          load=1.0, load_falloff=0.0, opacity=0.95, note="sky")
s.scumble(Region(-0.04, 0.22, 1.04, 0.52), "skymid", "skylow", 8, direction=-4,
          load=1.0, load_falloff=0.0, opacity=0.95, note="sky")

s.stroke([(-0.06, 0.255), (0.44, 0.135), (1.06, 0.165)], "bristle", "skymid",
         size=0.085, load=0.40, opacity=0.42, pressure="swell", note="sky")
s.stroke([(1.06, 0.050), (0.52, 0.125), (-0.06, 0.075)], "bristle", "sky",
         size=0.070, load=0.35, opacity=0.38, pressure="swell", note="sky")
s.stroke([(-0.06, 0.435), (0.50, 0.375), (1.06, 0.415)], "bristle", "skylow",
         size=0.075, load=0.45, opacity=0.40, pressure="swell", note="sky")
