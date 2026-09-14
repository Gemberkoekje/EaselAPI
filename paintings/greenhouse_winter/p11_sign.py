# The signature: two short lines meeting at a point, low in the dark under the
# left staging, a step lighter than what they sit on. A vanishing point in
# miniature, because every line in this picture was placed by one.
p["sig"] = p.at_value("under", 0.27)
s.stroke([(0.035, 0.945), (0.078, 0.963)], "liner", "sig", size=0.0045, opacity=0.9,
         pressure=[0.9, 0.4], note="signature")
s.stroke([(0.035, 0.981), (0.078, 0.963)], "liner", "sig", size=0.0045, opacity=0.9,
         pressure=[0.9, 0.4], note="signature")
print(s.budget_line())
print(s.look(region="A7:B8"))
