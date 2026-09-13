# The near coping is hard and should be. The far one is the furthest edge in the
# picture and was as crisp as the nearest -- so the light strip is killed over one
# short stretch and the boundary smudged along its own curve, once.
s.dry()
s.glaze([(0.205, 0.630), (0.300, 0.564), (0.390, 0.502)], p.at_value("deck", 0.29),
        opacity=0.40, size=0.045, pressure="swell")
s.smudge([(-0.020, 0.828), (0.130, 0.730), (0.270, 0.636), (0.410, 0.544), (0.520, 0.468)])
print(s.look(region="A4:E7"))
