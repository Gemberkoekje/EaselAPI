# Pass 3: the sea, over the bottom of the fog. The horizon is lost: one soft
# passage from the fog's horizon value down into a far sea mixed only a step
# below it, then the sea's own passage in two bands, so the swell is fine far
# off and broad near the frame. Then the beam's light lying faintly on the
# water under where it passes, and a few swells a step below the water they
# lie in -- no two the same length, weight or angle, so they are water and not
# rows. The first version of this pass had a teal sea a fog would never show,
# a scalloped horizon, and swells at the bottom of the box that floated like logs.
s.scumble(Region(-0.05, 0.54, 1.05, 0.70), "fog_low", "sea_far", 8, brush="flat", size=0.07,
          opacity=0.55, load=1.0, load_falloff=0.0, note="horizon, lost")
p["sea_mid"]  = p.mix("sea_far", "sea_near", 0.5)
p["sea_low"]  = p.at_value("sea_near", 0.34)
s.scumble(Region(-0.05, 0.66, 1.05, 0.82), "sea_far", "sea_mid", 6, brush="flat", size=0.09,
          opacity=0.85, load=1.0, load_falloff=0.0, note="far sea")
s.scumble(Region(-0.05, 0.79, 1.05, 1.05), "sea_mid", "sea_near", 6, brush="flat", size=0.13,
          opacity=0.85, load=1.0, load_falloff=0.0, note="near sea")
s.stroke([(-0.02, 0.675), (0.15, 0.668), (0.32, 0.676)], "round_soft", p.mix("sea_far", "beam_body", 0.3),
         size=0.05, opacity=0.22, load=1.0, load_falloff=0.0, pressure=[0.8, 1.0, 0.1],
         note="subject beam on the water")
swells = [  # (points, size, colour, opacity): thin, a step below the water, no two alike
    ([(0.02, 0.864), (0.16, 0.857), (0.30, 0.861)], 0.006, "sea_low", 0.32),
    ([(0.21, 0.936), (0.37, 0.929)],                 0.007, "sea_low", 0.35),
    ([(0.36, 0.796), (0.47, 0.802), (0.55, 0.799)], 0.005, "sea_near", 0.35),
    ([(0.07, 0.760), (0.19, 0.756)],                 0.004, "sea_mid", 0.35),
    ([(0.04, 0.984), (0.22, 0.976), (0.40, 0.988)], 0.009, "sea_low", 0.32),
]
for pts, size, colour, op in swells:
    s.stroke(pts, "round_hard", colour, size=size, opacity=op, pressure="swell", note="swell")
print(s.look(values=True))
print(s.look())
