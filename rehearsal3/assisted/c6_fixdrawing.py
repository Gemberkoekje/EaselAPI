# Pass 6 — argue with the machine's drawing.
#   ERASE : the wood-grain / lighting contours it cut across the whole table
#   KEEP  : the rim ellipse, the mug's upper silhouette, the handle, the figure,
#           the outer boundary of the cast shadow
#   ADD   : the spoon (missed entirely), the mug's base (swallowed by the shadow),
#           the tea's edge, the teabag tag (erased with the right-hand junk)
# Run: python -m easel run painting.easel c6_fixdrawing.py

REF = r"C:\temp\Level1.jpg"

# --- erase the junk -------------------------------------------------------
s.erase(span("A1", "B8"))     # left third: pure wood-grain zigzag
s.erase(span("G1", "H8"))     # right third: ditto (takes the tag with it)
s.erase(span("C8", "F8"))     # bottom band: ditto
s.erase(span("C1", "C2"))     # stray contour left of the rim

# --- landmarks ------------------------------------------------------------
s.mark("rim_l",  0.312, 0.192)
s.mark("rim_r",  0.636, 0.222)
s.mark("sp_top", 0.532, 0.006)
s.mark("sp_in",  0.505, 0.243)
s.mark("base_b", 0.465, 0.670)
s.mark("hand_o", 0.733, 0.372)
s.mark("tag_c",  0.865, 0.592)
s.mark("visor",  0.397, 0.465)

# --- draw what the machine did not ---------------------------------------
# the mug's base, from the left silhouette round to the right
s.pencil([(0.345, 0.550), (0.352, 0.615), (0.375, 0.648), (0.410, 0.665),
          (0.465, 0.670), (0.515, 0.663), (0.553, 0.648), (0.565, 0.610),
          (0.578, 0.550)])

# the spoon: two edges and a bowl
s.pencil([(0.509, 0.000), (0.4954, 0.068), (0.500, 0.150), (0.4985, 0.200),
          (0.497, 0.243)])
s.pencil([(0.5554, 0.009), (0.553, 0.059), (0.532, 0.140), (0.520, 0.195),
          (0.518, 0.243)])
s.pencil([(0.497, 0.243), (0.500, 0.272), (0.516, 0.294), (0.540, 0.297),
          (0.553, 0.278), (0.545, 0.256), (0.518, 0.243)])

# the tea's own edge, inside the rim
s.pencil([(0.352, 0.205), (0.383, 0.157), (0.440, 0.130), (0.505, 0.124),
          (0.562, 0.136), (0.598, 0.163), (0.610, 0.200), (0.594, 0.240),
          (0.548, 0.272), (0.480, 0.292), (0.420, 0.288), (0.376, 0.262),
          (0.356, 0.230), (0.352, 0.205)])

# the teabag tag
s.pencil([(0.815, 0.575), (0.840, 0.535), (0.900, 0.552), (0.918, 0.598),
          (0.893, 0.645), (0.833, 0.628), (0.815, 0.575)])

print(s.look(reference=REF, grid=True))
print("lines:", len(s.sketch_lines()), "strokes:", s.stroke_count)
