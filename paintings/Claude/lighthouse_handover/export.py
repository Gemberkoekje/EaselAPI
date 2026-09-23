import os
from easel import Session
P = os.path.dirname(os.path.abspath(__file__))
s = Session.load(os.path.join(P, "lighthouse.easel"))
s.export(os.path.join(P, "lighthouse_at_dusk.png"), sketch=False)
s.timelapse_gif(os.path.join(P, "lighthouse_at_dusk.gif"), fps=10.0, every=2)
print("exported")
