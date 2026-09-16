# Pass 11: the last marks, about the picture. Three soft strokes of fog lying
# on the far water, which is what a fog does and what softens the rows of
# swell, all of them stopping short of the tower, which is nearer than the
# fog; then the lamp's brightest point, once, at the centre of the glass, so
# the lightest mark in the picture is the light it is about.
# The first version of this pass ran two of these strokes straight across the
# tower and the stair's third turn. Nothing stood on them yet, so the pass was
# undone -- the one scrape of the canvas in this painting -- and laid again.
s.stroke([(-0.02, 0.665), (0.28, 0.672), (0.56, 0.664)], "round_soft", "fog_low", size=0.04,
         opacity=0.30, load=1.0, load_falloff=0.0, pressure=[0.6, 1.0, 0.2], note="fog on the water")
s.stroke([(0.16, 0.705), (0.38, 0.712), (0.57, 0.704)], "round_soft", "fog_low", size=0.035,
         opacity=0.25, load=1.0, load_falloff=0.0, pressure=[0.2, 1.0, 0.25], note="fog on the water, lower")
s.stroke([(0.77, 0.70), (0.90, 0.706), (1.03, 0.70)], "round_soft", "fog_low", size=0.03,
         opacity=0.22, load=1.0, load_falloff=0.0, pressure=[0.2, 1.0, 0.5], note="fog on the water, right")
s.dab(0.661, 0.219, "round_hard", p.mix("glow", "titanium_white", 0.6), size=0.009, press=3,
      note="subject the lamp, brightest")
print(s.look(values=True))
print(s.look())
print(s.compare(PLAN))
