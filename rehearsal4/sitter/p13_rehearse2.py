p = s.palette

lit_shell = ribbon([(0.470, 0.180), (0.505, 0.128), (0.560, 0.108), (0.615, 0.150),
                    (0.660, 0.225), (0.684, 0.310)], 0.070)
crown     = ribbon([(0.520, 0.118), (0.575, 0.122), (0.622, 0.170), (0.652, 0.228)], 0.034)

strands = [
    dict(points=[(0.512, 0.118), (0.556, 0.160), (0.586, 0.222)], brush="bristle",
         color="hair_l", size=0.007),
    dict(points=[(0.560, 0.112), (0.612, 0.170), (0.646, 0.246)], brush="bristle",
         color="hair_l", size=0.006),
    dict(points=[(0.596, 0.140), (0.646, 0.216), (0.668, 0.300)], brush="bristle",
         color="hair_d", size=0.008),
    dict(points=[(0.630, 0.196), (0.668, 0.278), (0.674, 0.360)], brush="bristle",
         color="hair_l", size=0.006),
    dict(points=[(0.484, 0.150), (0.520, 0.196), (0.540, 0.258)], brush="bristle",
         color="hair_d", size=0.009),
    dict(points=[(0.652, 0.270), (0.672, 0.352), (0.656, 0.428)], brush="bristle",
         color="hair_d", size=0.010),
    dict(points=[(0.500, 0.104), (0.528, 0.076)], brush="liner",
         color="hair_d", size=0.004, pressure=[0.9, 0.1]),
    dict(points=[(0.556, 0.096), (0.586, 0.070)], brush="liner",
         color="hair_d", size=0.004, pressure=[0.8, 0.1]),
    dict(points=[(0.700, 0.330), (0.724, 0.362)], brush="liner",
         color="hair_m", size=0.004, pressure=[0.9, 0.2]),
]

beard = [
    dict(points=[(0.412, 0.404), (0.440, 0.396), (0.466, 0.402)], brush="bristle",
         color="beard", size=0.014),
    dict(points=[(0.450, 0.400), (0.482, 0.414)], brush="bristle",
         color="beard", size=0.012),
    dict(points=[(0.424, 0.452), (0.430, 0.492), (0.448, 0.524)], brush="bristle",
         color="beard", size=0.018),
    dict(points=[(0.442, 0.512), (0.472, 0.544), (0.498, 0.534)], brush="bristle",
         color="beard", size=0.020),
    dict(points=[(0.486, 0.524), (0.510, 0.498), (0.522, 0.466)], brush="bristle",
         color="beard", size=0.018),
    dict(points=[(0.468, 0.440), (0.496, 0.458), (0.514, 0.482)], brush="bristle",
         color="hair_d", size=0.015, load=0.45),
    dict(points=[(0.546, 0.362), (0.552, 0.402), (0.542, 0.436)], brush="bristle",
         color="hair_d", size=0.011, load=0.5),
]

planes = [
    dict(points=[(0.424, 0.272), (0.452, 0.250), (0.482, 0.240)], brush="bristle",
         color="skin_l", size=0.020, opacity=0.7),
    dict(points=[(0.464, 0.336), (0.492, 0.386), (0.508, 0.430)], brush="bristle",
         color="skin_l", size=0.022, opacity=0.7),
    dict(points=[(0.426, 0.296), (0.460, 0.293)], brush="bristle",
         color="skin_d", size=0.013, opacity=0.6),
    dict(points=[(0.524, 0.286), (0.548, 0.344), (0.550, 0.398)], brush="bristle",
         color="skin_d", size=0.020, opacity=0.40),
    dict(points=[(0.414, 0.320), (0.402, 0.352)], brush="round_hard",
         color="skin_v", size=0.009),
    dict(points=[(0.413, 0.340), (0.415, 0.370)], brush="round_hard",
         color="skin_d", size=0.007, opacity=0.6),
]

feats = [
    dict(points=[(0.414, 0.271), (0.440, 0.266), (0.464, 0.272)], brush="liner",
         color="hair_d", size=0.007, pressure=[1, 0.4]),
    dict(points=[(0.450, 0.298), (0.474, 0.301)], brush="liner",
         color="hair_d", size=0.004),
    dict(points=[(0.439, 0.452), (0.459, 0.456)], brush="round_hard",
         color="iris", size=0.010),
    dict(points=[(0.442, 0.466), (0.460, 0.468)], brush="round_hard",
         color="lip", size=0.007),
]

print(s.rehearse(strands, reference="ref.jpg", region=span("D1", "F4")))
print(s.rehearse(beard + planes + feats, reference="ref.jpg", region=span("D3", "E5")))
