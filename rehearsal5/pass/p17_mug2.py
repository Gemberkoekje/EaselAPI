REF = "C:/temp/Level1.jpg"

body = polygon([(0.307, 0.224), (0.352, 0.292), (0.412, 0.327), (0.474, 0.337),
                (0.545, 0.324), (0.605, 0.289), (0.641, 0.230),
                (0.596, 0.440), (0.548, 0.630), (0.510, 0.652), (0.456, 0.663),
                (0.400, 0.652), (0.364, 0.624), (0.334, 0.425)])

s.dry()
s.block_in(body, "flat", "mug_mid", direction=90, density=0.85,
           size=0.050, load=1.0, note="near wall 2")
print("body", s.stroke_count)

# the pale band of the rim, arc by arc, around the tea
for pts, size in [([(0.318, 0.194), (0.310, 0.226), (0.320, 0.260), (0.340, 0.288)], 0.038),
                  ([(0.328, 0.172), (0.372, 0.141), (0.428, 0.122)], 0.036),
                  ([(0.432, 0.121), (0.502, 0.122), (0.562, 0.142)], 0.036),
                  ([(0.572, 0.152), (0.618, 0.188), (0.638, 0.228), (0.632, 0.262)], 0.038),
                  ([(0.626, 0.272), (0.598, 0.302), (0.558, 0.322)], 0.034)]:
    s.stroke(pts, "flat", "mug_lit", size=size, pressure="even", load=1.0,
             load_falloff=0.0, note="rim band")
print("rim band", s.stroke_count)

# the tea did not reach the right side of the mug
s.stroke([(0.548, 0.212), (0.578, 0.248), (0.566, 0.290)], "flat", "tea",
         size=0.034, pressure="even", load=1.0, note="tea right")
print("tea", s.stroke_count)

print(s.look(reference=REF))
print(s.look(region=span("C2", "F5"), reference=REF))
