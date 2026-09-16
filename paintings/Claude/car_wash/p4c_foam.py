# Soap on the glass. First attempt was five dabs and they came back as a row of
# floating discs -- the brush's own shape announcing itself. Foam on a windscreen is
# dragged, so these are five smears with some length and a curve in them, and the two
# catch-lights are short strokes rather than dabs, long enough not to read as capsules.
s.stroke([(0.192, 0.262), (0.268, 0.313), (0.339, 0.297)], "bristle", "foam",
         size=0.048, load=0.75, opacity=0.75, pressure="swell")
s.stroke([(0.398, 0.178), (0.433, 0.242), (0.483, 0.255)], "bristle", "foam",
         size=0.034, load=0.65, opacity=0.70, pressure="taper")
s.stroke([(0.498, 0.470), (0.553, 0.503), (0.599, 0.493)], "bristle", "foam",
         size=0.030, load=0.70, opacity=0.80, pressure="lift_off")
s.stroke([(0.186, 0.672), (0.252, 0.701), (0.303, 0.685)], "bristle", "haze",
         size=0.038, load=0.60, opacity=0.55, pressure="taper")
s.stroke([(0.268, 0.369), (0.313, 0.351)], "bristle", "foam_hi",
         size=0.026, load=0.80, opacity=0.90, pressure="swell")

s.stroke([(0.262, 0.361), (0.326, 0.346)], "round_hard", "foam_hi",
         size=0.009, opacity=0.85, pressure=[0.3, 1.0, 0.2])
s.stroke([(0.512, 0.484), (0.567, 0.475)], "round_hard", "foam_hi",
         size=0.008, opacity=0.75, pressure=[1.0, 0.25])
print(s.look())
