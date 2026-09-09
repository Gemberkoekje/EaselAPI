# c13 - last marks.
#  * the tea tag came out cornflower blue: desaturate(mix(ultramarine,
#    burnt_umber, 0.30), 0.15) is only 15% knocked back, so it is the most
#    saturated thing in a warm painting. Right value, wrong chroma (look_026
#    greyscale shows the value is fine).
#  * the string reads as a drawn wire - lose it in two places.
#  * the lower-right still bands; break it and leave it alone.
REF = r"C:\temp\Level1.jpg"
p = s.palette


def at_value(base, target):
    lo, hi = 0.0, 1.0
    if p.value_of(base) > target:
        for _ in range(26):
            mid = (lo + hi) / 2
            if p.value_of(p.shade(base, mid)) > target:
                lo = mid
            else:
                hi = mid
        return p.shade(base, (lo + hi) / 2)
    for _ in range(26):
        mid = (lo + hi) / 2
        if p.value_of(p.tint(base, mid)) < target:
            lo = mid
        else:
            hi = mid
    return p.tint(base, (lo + hi) / 2)


wood = p.desaturate(p.mix("yellow_ochre", "burnt_umber", 0.42), 0.30)
p["tag2"] = at_value(p.desaturate(p.mix("ultramarine", "burnt_umber", 0.45), 0.72), 0.245)
p["t48"] = at_value(wood, 0.480)
p["t52"] = at_value(wood, 0.520)
p["shdeep"] = at_value(p.desaturate(p.mix("burnt_umber", "ultramarine", 0.25), 0.35), 0.235)
p["cer"] = at_value(p.desaturate(p.mix("cerulean", "burnt_sienna", 0.22), 0.62), 0.535)
print("tag2", p.hex(p["tag2"]), round(p.value_of(p["tag2"]), 3))

n0 = s.stroke_count
s.dry()

# 1. the tag, neutral this time
s.stroke([(0.810, 0.562), (0.878, 0.592)], "flat", "tag2", size=0.046,
         load=1.0, pressure="even")
s.stroke([(0.824, 0.606), (0.874, 0.628)], "flat", "tag2", size=0.030,
         load=1.0, pressure="swell")
s.dab(0.836, 0.586, "round_hard", at_value(p.desaturate("cerulean", 0.4), 0.80),
      size=0.009)

# 2. lose the string in two places instead of drawing it end to end
s.stroke([(0.706, 0.300), (0.724, 0.352)], "flat", "t52", size=0.026,
         load=1.0, pressure="swell", opacity=0.9)
s.stroke([(0.772, 0.508), (0.788, 0.534)], "flat", "t52", size=0.022,
         load=1.0, pressure="swell", opacity=0.8)

# 3. break the banding in the lower right
for a, b_, sz, col, op in [((0.520, 0.930), (0.800, 0.836), 0.070, "t52", 0.55),
                           ((0.640, 0.760), (0.860, 0.700), 0.055, "t48", 0.5),
                           ((0.470, 0.870), (0.640, 0.812), 0.048, "t48", 0.45),
                           ((0.700, 0.960), (0.960, 0.876), 0.060, "t52", 0.4)]:
    s.stroke([a, b_], "flat", col, size=sz, load=1.0, pressure="swell",
             opacity=op, load_falloff=0.2)
s.smudge([(0.520, 0.850), (0.680, 0.786), (0.820, 0.740)], size=0.075)
s.smudge([(0.740, 0.660), (0.860, 0.632)], size=0.055)

# 4. the mug's left stripe, and the deepest shadow under the foot
s.stroke([(0.328, 0.320), (0.336, 0.470), (0.348, 0.600)], "flat", "cer",
         size=0.030, load=1.0, pressure="swell", opacity=0.9)
s.smudge([(0.316, 0.300), (0.322, 0.460)], size=0.028)
s.stroke([(0.560, 0.686), (0.400, 0.700)], "flat", "shdeep", size=0.040,
         load=1.0, pressure="swell", opacity=0.9)
s.stroke([(0.370, 0.716), (0.520, 0.706)], "flat", "shdeep", size=0.034,
         load=1.0, pressure="swell", opacity=0.75)
s.smudge([(0.400, 0.740), (0.520, 0.744)], size=0.05)

print("strokes:", s.stroke_count)
print(s.look(reference=REF))
