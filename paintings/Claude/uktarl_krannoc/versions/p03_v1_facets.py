"""The mountain, carved in front of the rays: the stone, its lit facets, its caverns.

A mass built of planes: the whole silhouette in the relief's stone, then the faces of the
crags that turn toward the middle of the wall (where the lamp is) laid on it as tiles,
the ones nearest the lamp lighter. Then the cave mouths, dark, and a few crevices.
"""

s.block_in(mountain, "flat", "mount", size=0.08, solid=True, edge="hard", direction="axis")

for i, plane in enumerate(mt_planes_l):
    near = i >= 3
    s.block_in(plane, "flat", "mount_lit" if near else "mount_mid", size=0.016,
               solid=True, edge="clean", direction=[MT_L_PEAKS[i], MT_L_DIPS[i]],
               opacity=1.0, pressure="even")
for i, plane in enumerate(mt_planes_r):
    near = i <= 1
    s.block_in(plane, "flat", "mount_lit" if near else "mount_mid", size=0.016,
               solid=True, edge="clean", direction=[MT_R_DIPS[i], MT_R_PEAKS[i]],
               opacity=1.0, pressure="even")

for cave in caves:
    s.block_in(cave, "flat", "cavern", size=0.012, solid=True, edge="hard",
               direction="axis")

# Crevices on the shade side of a few crags: punctuation, not outlines.
for pk in (MT_L_PEAKS[1], MT_L_PEAKS[3], MT_R_PEAKS[2], MT_R_PEAKS[4]):
    side = -1 if pk[0] < 512 else 1
    s.stroke(px_pts([(pk[0] - 4 * side, pk[1] + 8), (pk[0] - 10 * side, pk[1] + 34),
                     (pk[0] - 6 * side, pk[1] + 62)]),
             "round_hard", "mount_dark", size=0.007, opacity=0.85, pressure="taper")
