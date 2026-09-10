p = s.palette
s.dry()
n = s.stroke_count

# ---- the lit shell of the hair, as a mass ------------------------------
shell = ribbon([(0.474, 0.176), (0.508, 0.126), (0.560, 0.106), (0.615, 0.150),
                (0.660, 0.226), (0.682, 0.312)], 0.066)
s.block_in(shell, "bristle", "hair_m", direction="axis", density=1.0,
           size=0.030, load=1.0)
print("lit shell", s.stroke_count - n); n = s.stroke_count

for pts, col, sz in [
    ([(0.512, 0.118), (0.556, 0.160), (0.586, 0.222)], "hair_l", 0.007),
    ([(0.560, 0.112), (0.612, 0.170), (0.646, 0.246)], "hair_l", 0.006),
    ([(0.596, 0.140), (0.646, 0.216), (0.668, 0.300)], "hair_d", 0.008),
    ([(0.630, 0.196), (0.668, 0.278), (0.674, 0.360)], "hair_l", 0.006),
    ([(0.484, 0.150), (0.520, 0.196), (0.540, 0.258)], "hair_d", 0.009),
    ([(0.652, 0.270), (0.672, 0.352), (0.656, 0.428)], "hair_d", 0.010),
    ([(0.470, 0.196), (0.498, 0.148), (0.532, 0.120)], "hair_l", 0.006),
]:
    s.stroke(pts, "bristle", col, size=sz, pressure="taper")
# strands falling over the forehead, and wisps against the light
s.stroke([(0.492, 0.146), (0.454, 0.196), (0.430, 0.244)], "liner", "hair_d",
         size=0.005, pressure=[1, 0.3])
s.stroke([(0.476, 0.134), (0.446, 0.180)], "liner", "hair_d", size=0.004,
         pressure=[0.8, 0.2])
s.stroke([(0.500, 0.104), (0.528, 0.074)], "liner", "hair_d", size=0.004,
         pressure=[0.9, 0.1])
s.stroke([(0.556, 0.096), (0.588, 0.068)], "liner", "hair_d", size=0.004,
         pressure=[0.8, 0.1])
s.stroke([(0.700, 0.330), (0.726, 0.364)], "liner", "hair_m", size=0.004,
         pressure=[0.9, 0.2])
print("strands", s.stroke_count - n); n = s.stroke_count

# ---- the beard, as a mass ----------------------------------------------
beard_sh = polygon([
    (0.406, 0.402), (0.436, 0.392), (0.470, 0.402), (0.498, 0.424), (0.512, 0.462),
    (0.508, 0.500), (0.492, 0.530), (0.466, 0.550), (0.440, 0.534), (0.424, 0.498),
    (0.416, 0.456), (0.410, 0.424),
])
s.block_in(beard_sh, "bristle", "beard", direction=("axis", 78), density=1.0,
           size=0.040, load=1.0)
s.stroke([(0.468, 0.440), (0.496, 0.458), (0.514, 0.482)], "bristle", "hair_d",
         size=0.015, load=0.45)
s.stroke([(0.546, 0.362), (0.552, 0.402), (0.542, 0.436)], "bristle", "hair_d",
         size=0.011, load=0.5)
print("beard", s.stroke_count - n); n = s.stroke_count

# ---- the face, as planes ------------------------------------------------
s.stroke([(0.424, 0.272), (0.452, 0.250), (0.482, 0.240)], "bristle", "skin_l",
         size=0.020, opacity=0.7)
s.stroke([(0.464, 0.336), (0.492, 0.386), (0.508, 0.430)], "bristle", "skin_l",
         size=0.022, opacity=0.7)
s.stroke([(0.426, 0.296), (0.460, 0.293)], "bristle", "skin_d", size=0.013,
         opacity=0.6)
s.stroke([(0.524, 0.286), (0.548, 0.344), (0.550, 0.398)], "bristle", "skin_d",
         size=0.020, opacity=0.40)
s.stroke([(0.412, 0.322), (0.401, 0.350)], "round_hard", "skin_l", size=0.006)
s.stroke([(0.413, 0.340), (0.415, 0.370)], "round_hard", "skin_d", size=0.006,
         opacity=0.6)
s.stroke([(0.404, 0.390), (0.422, 0.400)], "round_hard", "skin_l", size=0.007,
         opacity=0.7)
print("planes", s.stroke_count - n); n = s.stroke_count

# ---- features ----------------------------------------------------------
s.stroke([(0.414, 0.271), (0.440, 0.266), (0.464, 0.272)], "liner", "hair_d",
         size=0.007, pressure=[1, 0.4])                       # brow
s.dab(0.458, 0.308, "round_hard", "skin_d", size=0.020)        # socket
s.dab(0.468, 0.310, "round_hard", "eyew", size=0.008, press=2) # white
s.dab(0.4598, 0.3095, "round_hard", "iris", size=0.009, press=2)
s.stroke([(0.449, 0.299), (0.474, 0.302)], "liner", "hair_d", size=0.004)  # lid
s.dab(0.407, 0.379, "round_hard", "beard", size=0.009)         # nostril
s.stroke([(0.439, 0.452), (0.459, 0.456)], "round_hard", "iris", size=0.010)
s.dab(0.4455, 0.4375, "round_hard", "teeth", size=0.008, press=2)
s.stroke([(0.442, 0.467), (0.460, 0.469)], "round_hard", "lip", size=0.006,
         opacity=0.8)
s.dab(0.5875, 0.344, "round_hard", "skin_m", size=0.024)       # ear
s.dab(0.590, 0.350, "round_hard", "skin_d", size=0.011, opacity=0.7)
s.dab(0.590, 0.441, "round_hard", "beard", size=0.005)         # the mole
print("features", s.stroke_count - n)

print("total:", s.stroke_count)
print(s.look(region=span("D1", "F5"), reference="ref.jpg"))
