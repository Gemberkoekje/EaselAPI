# The forearms are flat slabs. Both run almost exactly along the light, so neither
# has a lit SIDE -- a cylinder lit end-on is light down its middle and dark at both
# edges, and that is what makes a limb read as round. The middle light fades out
# toward the frame so the limbs still go away into the dark.
s.dry()

for dark_a, dark_b, core, sz in [
    ([(0.694, 0.668), (0.794, 0.786), (0.892, 0.908)],
     [(0.616, 0.736), (0.714, 0.860), (0.808, 0.992)],
     [(0.656, 0.702), (0.754, 0.822), (0.852, 0.952)], 0.040),
    ([(0.806, 0.216), (0.846, 0.102), (0.874, 0.006)],
     [(0.716, 0.250), (0.762, 0.128), (0.796, 0.022)],
     [(0.762, 0.236), (0.804, 0.118), (0.836, 0.018)], 0.034),
]:
    s.stroke(dark_a, "bristle", "fl_under", size=sz * 1.15, opacity=0.30, load=1.0,
             load_falloff=0.55, pressure="swell", note="subject")
    s.stroke(dark_b, "bristle", "fl_under", size=sz * 1.05, opacity=0.26, load=1.0,
             load_falloff=0.60, pressure="swell", note="subject")
    s.stroke(core, "bristle", "fl_arm", size=sz * 1.9, opacity=0.24, load=1.0,
             load_falloff=0.60, pressure=([1.0, 0.55, 0.08] if sz > 0.036 else "lift_off"), note="subject")

# one mark across each, so neither is a bare length: the crease at the wrist and
# a fold where the forearm turns
s.stroke([(0.640, 0.708), (0.690, 0.678), (0.722, 0.664)], "bristle", "fl_body3",
         size=0.024, opacity=0.38, load=0.55, load_falloff=0.50,
         pressure="swell", note="subject")
s.stroke([(0.742, 0.244), (0.786, 0.222), (0.818, 0.196)], "bristle", "fl_body3",
         size=0.020, opacity=0.32, load=0.52, load_falloff=0.50,
         pressure="swell", note="subject")
print(s.look())
