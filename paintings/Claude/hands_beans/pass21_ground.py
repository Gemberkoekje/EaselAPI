# The last third, on what surrounds the subject. The upper right was a flat dead
# field. It does not get a THING put in it -- that is the wrong repair for an empty
# half -- it gets incident: broad soft passes at close values crossing each other,
# grain that breaks, and a warmer pool of table where the light reaches the hands.
s.dry()

# incident across the dead quadrant: close values, ends off the canvas, crossing
for pts, sz, col, op in [
    ([(0.24, -0.06), (0.58, 0.10), (1.06, 0.16)], 0.115, "glow_mid", 0.22),
    ([(1.06, -0.04), (0.72, 0.16), (0.40, 0.30)], 0.100, "table",    0.26),
    ([(0.34, 0.06), (0.62, 0.22), (0.96, 0.30)], 0.085, "grain",    0.20),
    ([(1.06, 0.34), (0.80, 0.24), (0.58, 0.10)], 0.070, "tbl_lit",  0.16),
]:
    s.stroke(pts, "bristle", col, size=sz, opacity=op, load=1.0,
             load_falloff=0.30, pressure="swell", note="table")

# the pool of table the light actually reaches, kept off the hands
for pts, sz, op in [([(0.06, 0.30), (0.26, 0.36), (0.40, 0.34)], 0.090, 0.20),
                    ([(0.14, 0.62), (0.26, 0.60), (0.36, 0.62)], 0.070, 0.16),
                    ([(0.52, 0.16), (0.62, 0.22), (0.70, 0.24)], 0.060, 0.14)]:
    s.stroke(pts, "bristle", "glow_mid", size=sz, opacity=op, load=1.0,
             load_falloff=0.40, pressure="swell", note="table")

# grain in the quiet lower right, none of it parallel to the rest
s.stroke([(1.06, 0.72), (0.90, 0.80), (0.78, 0.92)], "bristle", "grain",
         size=0.032, load=0.42, load_falloff=0.55, opacity=0.24,
         pressure="swell", note="table")
s.stroke([(0.62, 1.06), (0.70, 0.90), (0.74, 0.76)], "bristle", "tbl_lit",
         size=0.026, load=0.38, load_falloff=0.60, opacity=0.18,
         pressure="swell", note="table")
s.stroke([(0.30, 0.78), (0.24, 0.90), (0.22, 1.02)], "bristle", "grain",
         size=0.024, load=0.40, load_falloff=0.55, opacity=0.20,
         pressure="swell", note="table")

# deepen the very top and the far right, so nothing at the frame competes
s.glaze([(0.10, -0.03), (0.42, 0.01), (0.72, -0.01)], "corner", opacity=0.22,
        size=0.14, note="table")
s.glaze([(1.04, 0.62), (1.02, 0.80), (1.03, 0.98)], "corner", opacity=0.24,
        size=0.13, note="table")
print(s.look())
