REF = "C:/temp/Level1.jpg"

rim  = ellipse((0.474, 0.226), 0.167, 0.110, rotate=5)
tea  = ellipse((0.470, 0.244), 0.132, 0.077, rotate=5)
body = polygon([(0.307, 0.224), (0.352, 0.292), (0.412, 0.327), (0.474, 0.337),
                (0.545, 0.324), (0.605, 0.289), (0.641, 0.230),
                (0.596, 0.440), (0.548, 0.630), (0.510, 0.652), (0.456, 0.663),
                (0.400, 0.652), (0.364, 0.624), (0.334, 0.425)])
handle = ribbon([(0.636, 0.262), (0.688, 0.288), (0.716, 0.348),
                 (0.706, 0.430), (0.660, 0.492), (0.596, 0.518)], 0.040)
fig = hull([(0.362, 0.415), (0.430, 0.392), (0.500, 0.400), (0.505, 0.600),
            (0.430, 0.628), (0.368, 0.600)])
pack = polygon([(0.497, 0.452), (0.552, 0.462), (0.558, 0.560), (0.500, 0.572)])

# the drawing, free, over the far masses and under everything to come
s.pencil(rim.closed, pressure=0.7)
s.pencil(tea.closed, pressure=0.5)
s.pencil(body.closed, pressure=0.7)
s.pencil(handle.closed, pressure=0.6)
s.pencil(fig.closed, pressure=0.5)
s.pencil(pack.closed, pressure=0.5)
s.pencil([(0.505, 0.000), (0.497, 0.120), (0.488, 0.196)], pressure=0.7)
s.pencil([(0.540, 0.002), (0.524, 0.130), (0.512, 0.200)], pressure=0.7)

print(s.look(reference=REF))
print(s.look(region=span("C1", "G6"), reference=REF))
print("strokes", s.stroke_count)
