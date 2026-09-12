# The signature: one mark, in the quiet near water at the bottom left, a step
# lighter than the sea it lies on. A tendril -- a curl that thins to nothing
# at both ends. It is that because the shape this session kept coming back
# to is the helix: the stair, the vine that got out over the rail, the stems
# climbing the glass. A curl is the smallest piece of one. It is not a name
# and it repairs nothing; it lies in the water like something reflected.
before = s.stroke_count
curl = [(0.045, 0.952), (0.062, 0.940), (0.078, 0.946), (0.074, 0.960), (0.060, 0.962)]
s.stroke(curl, "round_hard", p.at_value("sea_near", 0.50), size=0.007, opacity=0.9,
         load=1.0, load_falloff=0.0, pressure=[0.05, 0.6, 1.0, 0.6, 0.05], note="signature")
print("stroke_count", before, "->", s.stroke_count, "(the signature is not charged)")
print(s.look())
