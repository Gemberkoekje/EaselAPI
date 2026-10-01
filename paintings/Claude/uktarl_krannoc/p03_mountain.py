"""The mountain, carved in front of the rays: a dark craggy mass against the gold.

The sun rises behind a dark mountain, which is the picture everyone already knows: the
mountain is quieter than the rays, so the figures in front of it can be found by their
lit faces. The stone first, then a dry brush along its slopes for the strata, the ridges
nearest the lamp catching its light, the cave mouths, and a few crevices.
"""

s.block_in(mountain, "flat", "mount_deep", size=0.10, solid=True, edge="hard",
           direction=10)

# Strata: a starved bristle down each slope, the lighter stone breaking on the tooth.
for path in ([(-10, 560), (120, 520), (250, 470), (380, 420)],
             [(20, 600), (160, 560), (300, 520)],
             [(1034, 560), (920, 520), (800, 470)],
             [(1034, 600), (900, 575), (840, 560)]):
    s.stroke(px_pts(path), "bristle", "mount", size=0.05, load=0.6, opacity=0.6,
             pressure="swell", clip=mountain)

# The ridges that turn toward the lamp, warm: the central crags' inner slopes.
for path, mix in (([(368, 381), (390, 384), (410, 387), (430, 371), (448, 353)], "mount_lit"),
                  ([(288, 409), (308, 411), (328, 415), (348, 397), (366, 382)], "mount_mid"),
                  ([(812, 407), (830, 422), (850, 441)], "mount_mid"),
                  ([(205, 441), (226, 444), (246, 449)], "mount_mid")):
    s.stroke(px_pts(path), "round_hard", mix, size=0.009, opacity=0.9,
             pressure=[0.2, 1.0, 0.9, 0.3], clip=mountain)

for cave in caves:
    s.block_in(cave, "flat", "cavern", size=0.02, solid=True, edge="hard",
               direction="axis")

for pk in (MT_L_PEAKS[1], MT_L_PEAKS[3], MT_R_PEAKS[2], MT_R_PEAKS[4]):
    side = -1 if pk[0] < 512 else 1
    s.stroke(px_pts([(pk[0] - 3 * side, pk[1] + 10), (pk[0] - 9 * side, pk[1] + 36),
                     (pk[0] - 4 * side, pk[1] + 64)]),
             "round_hard", "crevice", size=0.007, opacity=0.8, pressure="taper")
