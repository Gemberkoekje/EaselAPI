# A correction of rank, not of drawing. The two lit fingers sit beside the pinch
# and belong to the same focal cluster, so they stay. What gets walked back is
# what had become bright far from the subject: the bowl's rim, in the corner, and
# the broad plane on the back of the picking hand.
s.dry()
for pts, size, target in [
    ([(-0.020, 0.784), (0.050, 0.756), (0.110, 0.742), (0.168, 0.746)], 0.017, 0.268),
    ([(0.640, 0.262), (0.706, 0.222), (0.782, 0.212)], 0.072, 0.436),
    ([(0.784, 0.230), (0.742, 0.268), (0.700, 0.288)], 0.055, 0.408),
]:
    s.glaze(pts, "corner", to_value=target, size=size, note="rank")
print(s.look(values=True))
print(s.look())
