# The signature: one mark, in the near water at the bottom right, a step lighter
# than the sea it sits on. A shallow arc that thins to nothing at both ends --
# the one shape this session came to trust, after the tool's own shapes (a disc,
# a slab, a comb, a ring) had each been thrown away in rehearsal at least once.
# It is not a name and it repairs nothing; it lies in the water like a ripple.
before = s.stroke_count
s.stroke([(0.915, 0.962), (0.945, 0.952), (0.975, 0.958)], "round_hard",
         p.at_value("sea_near", 0.42), size=0.008, opacity=0.9, load=1.0, load_falloff=0.0,
         pressure=[0.05, 1.0, 0.05], note="signature")
print("stroke_count", before, "->", s.stroke_count, "(the signature is not charged)")
print(s.look())
