# Pass 8: the hair mass, walked as strands, not blocked in as a box.
REF = "C:/temp/Level3.jpg"
p = s.palette
p["hair_dk"]  = p.mix(p.mix("burnt_umber", "ultramarine", 0.14), "titanium_white", 0.08)
p["hair_mid"] = p.mix(p.mix("burnt_umber", "yellow_ochre", 0.42), "titanium_white", 0.14)
p["hair_lit"] = p.mix(p.mix("yellow_ochre", "burnt_umber", 0.40), "titanium_white", 0.30)
p["hair_hi"]  = p.mix(p.mix("yellow_ochre", "burnt_umber", 0.20), "titanium_white", 0.52)
s.dry()

STRANDS = [
    # (points, colour, size)
    ([(0.500, 0.090), (0.455, 0.140), (0.428, 0.200), (0.424, 0.250)], "hair_mid", 0.055),
    ([(0.522, 0.082), (0.472, 0.132), (0.442, 0.198), (0.438, 0.258)], "hair_lit", 0.045),
    ([(0.536, 0.080), (0.502, 0.128), (0.472, 0.198), (0.466, 0.268)], "hair_mid", 0.060),
    ([(0.550, 0.086), (0.532, 0.140), (0.512, 0.212), (0.508, 0.284)], "hair_dk",  0.055),
    ([(0.562, 0.092), (0.562, 0.152), (0.552, 0.232), (0.548, 0.304)], "hair_mid", 0.065),
    ([(0.576, 0.102), (0.596, 0.162), (0.602, 0.242), (0.598, 0.318)], "hair_lit", 0.050),
    ([(0.590, 0.112), (0.626, 0.176), (0.641, 0.256), (0.641, 0.332)], "hair_mid", 0.065),
    ([(0.600, 0.126), (0.649, 0.196), (0.666, 0.276), (0.664, 0.362)], "hair_dk",  0.070),
    ([(0.604, 0.148), (0.660, 0.226), (0.673, 0.312), (0.660, 0.402)], "hair_mid", 0.070),
    ([(0.598, 0.172), (0.650, 0.256), (0.665, 0.352), (0.650, 0.442)], "hair_dk",  0.075),
    ([(0.582, 0.202), (0.630, 0.292), (0.645, 0.382), (0.628, 0.462)], "hair_dk",  0.070),
    ([(0.558, 0.232), (0.604, 0.322), (0.620, 0.402), (0.608, 0.468)], "hair_dk",  0.060),
]
n0 = s.stroke_count
for pts, col, sz in STRANDS:
    s.stroke(pts, "bristle", col, size=sz, load=1.0, pressure="taper")
print("strands:", s.stroke_count - n0)

# cross-pass so the mass closes up instead of combing into threads
n0 = s.stroke_count
CROSS = [
    ([(0.440, 0.160), (0.520, 0.115), (0.600, 0.135)], "hair_mid", 0.055),
    ([(0.455, 0.225), (0.545, 0.190), (0.630, 0.215)], "hair_dk",  0.050),
    ([(0.520, 0.300), (0.600, 0.290), (0.665, 0.320)], "hair_dk",  0.055),
    ([(0.560, 0.395), (0.625, 0.390), (0.668, 0.400)], "hair_dk",  0.055),
    ([(0.575, 0.455), (0.630, 0.450), (0.655, 0.440)], "hair_dk",  0.050),
]
for pts, col, sz in CROSS:
    s.stroke(pts, "bristle", col, size=sz, load=0.9, pressure="swell")
print("cross:", s.stroke_count - n0)

# the lit strands along the top and right — few, small, deliberate
n0 = s.stroke_count
LIT = [
    ([(0.505, 0.098), (0.545, 0.088), (0.585, 0.108)], "hair_hi", 0.014),
    ([(0.562, 0.120), (0.606, 0.168), (0.630, 0.226)], "hair_hi", 0.012),
    ([(0.600, 0.200), (0.640, 0.262), (0.655, 0.322)], "hair_lit", 0.018),
    ([(0.470, 0.120), (0.442, 0.170), (0.432, 0.215)], "hair_lit", 0.013),
    ([(0.620, 0.310), (0.648, 0.372), (0.646, 0.428)], "hair_lit", 0.015),
]
for pts, col, sz in LIT:
    s.stroke(pts, "bristle", col, size=sz, load=1.0, pressure="taper")
print("lit strands:", s.stroke_count - n0)

print("head:", s.look(region=span("D1", "G5"), reference=REF))
print("whole:", s.look(reference=REF))
print("TOTAL strokes:", s.stroke_count)
