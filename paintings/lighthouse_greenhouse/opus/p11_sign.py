# Finished. One mark, in the darkest corner, a step above what it sits on.
#
# It is not a name and it is not a motif out of the picture -- a sprig would have
# been the third thing in this painting that was a growing shoot, and the mark is
# not part of the painting. It is a hook: one stroke that changes direction once,
# which is the least a mark can do and still be unmistakably somebody's decision
# rather than something that happened. Small, quiet, in a corner where it does
# the picture no harm.
s.stroke([(0.0300, 0.9600), (0.0300, 0.9885), (0.0530, 0.9885)], "liner",
         p.at_value("rock", 0.235), size=0.0045, opacity=0.85,
         pressure=[0.9, 1.0, 0.5], note="signature")
print("stroke_count", s.stroke_count, "-- the signature does not count:",
      s.spent, "of 300 spent,", s.remaining, "left")
print(s.look(region="A7:C8"))
