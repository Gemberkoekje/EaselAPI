"""Which free verbs perturb the random stream?

A bristle stroke's comb is drawn from the RNG. Lay one, preceded by each free verb, and
compare the export. If the hash matches the baseline the verb left the stream untouched.

Result: look, values, preview, rehearse, cost, compare are all clean -- which is what
makes "rehearse everything" free of side effects. pencil is the exception: it advances
the stream, so adding or removing an underdrawing changes the texture of every later
stroke (deterministically, so reproduction still holds).

Run: .venv/bin/python probes/probe_rng.py
"""
import hashlib

from easel import Session


def build(pre):
    s = Session(400, 300, texture="linen", ground="toned_grey", seed=9)
    s.palette["c"] = s.palette.mix("ultramarine", "burnt_umber", 0.4)
    plan = [{"points": [(0.1, 0.5), (0.9, 0.5)], "brush": "bristle", "color": "c", "size": 0.08}]
    {
        "none": lambda: None,
        "look": lambda: s.look(),
        "values": lambda: s.look(values=True),
        "preview": lambda: s.preview(plan),
        "rehearse": lambda: s.rehearse(plan),
        "cost": lambda: s.cost(plan),
        "compare": lambda: s.compare({"all": 0.3}),
        "pencil": lambda: s.pencil([(0.1, 0.1), (0.9, 0.9)]),
    }[pre]()
    s.stroke([(0.1, 0.5), (0.9, 0.5)], "bristle", "c", size=0.08)
    s.export("_rng.png", impasto=True)
    return hashlib.sha256(open("_rng.png", "rb").read()).hexdigest()[:12]


if __name__ == "__main__":
    base = build("none")
    print(f"{'baseline':10s} {base}")
    for pre in ("look", "values", "preview", "rehearse", "cost", "compare", "pencil"):
        h = build(pre)
        print(f"{pre:10s} {h} {'== baseline (side-effect free)' if h == base else '!= baseline  <-- perturbs the stream'}")
