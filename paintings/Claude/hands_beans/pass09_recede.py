# The limbs were the two biggest, lightest masses in the picture and had become a
# bright X across it. They are not the subject: they are how the subject enters.
# Dark glazes walk each one down toward the table, hardest at the frame, so all
# the light is left where the hands meet. to_value solves the opacity, one stroke each.
s.dry()
for pts, size, target in [
    ([(0.660, 0.690), (0.740, 0.788), (0.816, 0.884)], 0.155, 0.320),
    ([(0.734, 0.782), (0.822, 0.890), (0.906, 0.996)], 0.150, 0.268),
    ([(0.826, 0.886), (0.912, 0.992), (0.975, 1.060)], 0.142, 0.222),
    ([(0.756, 0.246), (0.792, 0.170), (0.822, 0.098)], 0.130, 0.300),
    ([(0.796, 0.150), (0.838, 0.046), (0.868, -0.036)], 0.124, 0.242),
    ([(0.844, 0.030), (0.878, -0.060)], 0.118, 0.218),
]:
    s.glaze(pts, "tbl_deep", to_value=target, size=size, note="subject")
print(s.look())
print(s.look(values=True))
