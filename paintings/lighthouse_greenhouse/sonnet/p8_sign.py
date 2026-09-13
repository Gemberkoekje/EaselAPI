# The signature: one mark, lower right, in the mist over the water. A small
# curl that thins to nothing at both ends -- the shape this session kept
# coming back to for anything growing (the tendrils, the trailing plant on
# each pot) -- given the faintest breath of the same green the beam picked
# up from the leaves. It is not a name and it repairs nothing.
before = s.stroke_count
s.stroke([(0.905, 0.845), (0.925, 0.828), (0.945, 0.838), (0.958, 0.822)],
         "round_hard", p.at_value(p.mix("sea_near", "leaf_mid", 0.2), 0.40),
         size=0.007, opacity=0.85, load=1.0, load_falloff=0.0,
         pressure=[0.05, 1.0, 0.6, 0.05], note="signature")
print("stroke_count", before, "->", s.stroke_count, "(the signature is not charged)")
print(s.look())
