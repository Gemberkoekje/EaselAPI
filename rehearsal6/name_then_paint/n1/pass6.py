# Pass 6 - the drawing. Pencil only; no paint, no strokes spent.
s.erase()

s.mark("rim_l",  0.318, 0.664)
s.mark("rim_r",  0.516, 0.672)
s.mark("rim_f",  0.417, 0.700)     # front of the rim ellipse, dipping toward us
s.mark("base_l", 0.352, 0.860)
s.mark("base_r", 0.482, 0.866)
s.mark("bl_a",   0.443, 0.452)     # main bloom
s.mark("bl_b",   0.634, 0.527)     # the heavy one leaning right
s.mark("bl_c",   0.404, 0.598)     # low bloom over the rim
s.mark("bud",    0.556, 0.392)     # small half-open head at the back
s.mark("pet1",   0.612, 0.838)
s.mark("pet2",   0.702, 0.892)
s.mark("pet3",   0.793, 0.806)

# --- the pot ------------------------------------------------------------------
s.pencil([s.pt("rim_l"), (0.360, 0.652), (0.420, 0.650), (0.478, 0.658), s.pt("rim_r")])
s.pencil([s.pt("rim_l"), (0.360, 0.688), s.pt("rim_f"), (0.478, 0.690), s.pt("rim_r")])
s.pencil([(0.324, 0.694), (0.366, 0.716), s.pt("rim_f"), (0.472, 0.718), (0.512, 0.700)])
s.pencil([(0.324, 0.694), (0.336, 0.780), s.pt("base_l")])
s.pencil([(0.512, 0.700), (0.498, 0.782), s.pt("base_r")])
s.pencil([s.pt("base_l"), (0.400, 0.878), (0.446, 0.877), s.pt("base_r")])
# the crack
s.pencil([(0.372, 0.708), (0.384, 0.752), (0.374, 0.790), (0.390, 0.834), (0.386, 0.862)],
         pressure=0.75)

# --- the flower mass ----------------------------------------------------------
s.pencil([(0.352, 0.500), (0.372, 0.418), (0.446, 0.378), (0.520, 0.398),
          (0.548, 0.352), (0.616, 0.372), (0.672, 0.424), (0.726, 0.470),
          (0.746, 0.540), (0.706, 0.604), (0.630, 0.632), (0.548, 0.616),
          (0.470, 0.646), (0.392, 0.648), (0.340, 0.594), (0.336, 0.536),
          (0.352, 0.500)])
for c, rx, ry in ((s.pt("bl_a"), 0.086, 0.079), (s.pt("bl_b"), 0.098, 0.086),
                  (s.pt("bl_c"), 0.062, 0.052), (s.pt("bud"), 0.044, 0.038)):
    s.pencil(ellipse(Region(c[0]-rx, c[1]-ry, c[0]+rx, c[1]+ry)).closed)

# --- stems and a few leaves ---------------------------------------------------
s.pencil([(0.418, 0.640), (0.428, 0.672), (0.424, 0.700)])
s.pencil([(0.520, 0.612), (0.486, 0.660), (0.452, 0.694)])
s.pencil([(0.300, 0.556), (0.256, 0.590), (0.238, 0.634)])
s.pencil([(0.716, 0.586), (0.772, 0.622), (0.804, 0.672)])
s.pencil([(0.560, 0.640), (0.596, 0.678), (0.588, 0.706)])

# --- the three fallen petals --------------------------------------------------
s.pencil(ellipse(Region(0.578, 0.820, 0.648, 0.856), rotate=-14).closed)
s.pencil(ellipse(Region(0.664, 0.874, 0.742, 0.910), rotate=8).closed)
s.pencil(ellipse(Region(0.756, 0.788, 0.830, 0.824), rotate=-26).closed)

print("strokes:", s.stroke_count)
print(s.look())
