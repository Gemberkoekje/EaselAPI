import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from easel import Session
P = os.path.dirname(os.path.abspath(__file__))
s = Session.load(os.path.join(P, "lighthouse.easel"))
tag = sys.argv[1] if len(sys.argv) > 1 else "clean"
region = sys.argv[2] if len(sys.argv) > 2 else None
s.look(path=os.path.join(P, "out", f"{tag}.png"), marks=False, sketch=False, region=region)
s.look(path=os.path.join(P, "out", f"{tag}_values.png"), marks=False, sketch=False, values=True, region=region)
print("ok")
