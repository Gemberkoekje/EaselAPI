# The cupped hand. Three fingers described, the fourth lost. No two get the same
# brush, the same body value, or the light in the same place across their width;
# the tips of the far ones are let go into the table.
s.dry()

s.stroke(CUP_ARM_LIT[0], "bristle", "fl_arm", size=0.058, opacity=0.85,
         load=1.0, load_falloff=0.40, pressure=[1.0, 0.8, 0.5, 0.15], note="subject")

for pts, sz in ([(0.512, 0.462), (0.430, 0.430), (0.340, 0.428), (0.290, 0.446)], 0.016), \
               ([(0.506, 0.506), (0.424, 0.482), (0.336, 0.486), (0.284, 0.512)], 0.018), \
               ([(0.500, 0.550), (0.420, 0.536), (0.348, 0.548), (0.300, 0.574)], 0.015):
    s.stroke(pts, "bristle", "fl_deep", size=sz, opacity=0.90,
             load=1.0, load_falloff=0.30, pressure="swell", note="subject")

s.paint([{"shape": CUP_HOLLOW, "brush": "bristle", "color": "palm_dk", "size": 0.040,
          "density": 1.0, "direction": ("axis", 66), "solid": True, "edge": "hard",
          "note": "subject"}])

# body: brush, size, colour, pressure | light: pts, size, opacity, cross-offset
FINGERS = [
    ("bristle", 0.044, "fl_body2", [0.95, 1.0, 0.7, 0.25],
     [(0.500, 0.428), (0.452, 0.407), (0.420, 0.400)], 0.019, 0.88, 0.40),
    ("bristle", 0.049, "fl_body",  [1.0, 0.95, 0.85, 0.55],
     [(0.492, 0.472), (0.432, 0.450), (0.376, 0.447), (0.336, 0.457)], 0.022, 1.00, 0.34),
    ("bristle", 0.042, "fl_body3", [0.85, 0.9, 0.5, 0.15],
     [(0.484, 0.516), (0.436, 0.502)], 0.014, 0.60, 0.50),
    ("bristle", 0.034, "fl_shad",  [0.7, 0.6, 0.3, 0.0],
     None, None, None, None),
]
for (pts, w, e), (br, bsz, bcol, bpr, lpts, lsz, lop, off) in zip(CUP_FING, FINGERS):
    s.stroke(pts, br, bcol, size=bsz, opacity=0.95, load=1.0,
             load_falloff=0.30, pressure=bpr, note="subject")
    if lpts:
        s.stroke([(x, y - bsz * off) for x, y in pts[:len(pts)]], "bristle",
                 "fl_mid", size=bsz * 0.54, opacity=0.80, load=0.55,
                 load_falloff=0.45, pressure="swell", note="subject")
        s.stroke(lpts, "round_hard", "fl_lit", size=lsz, opacity=lop, load=1.0,
                 load_falloff=0.20, tip_wobble=0.50,
                 pressure=[0.25, 1.0, 0.7, 0.2][:len(lpts)], note="subject")

for x, y, sz, pr in [(0.500, 0.444, 0.023, 3), (0.496, 0.487, 0.027, 3),
                     (0.490, 0.528, 0.019, 2)]:
    s.dab(x, y, "round_hard", "fl_warm", size=sz, press=pr, tip_wobble=0.75,
          opacity=0.82, note="subject")
print(s.look(region="C3:F6"))
