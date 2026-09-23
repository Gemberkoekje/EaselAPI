"""Try variants of a pass on throwaway copies; write one look per variant + a sheet."""
import os, sys, importlib.util
import easel
from easel import Session
P = os.path.dirname(os.path.abspath(__file__)); os.chdir(P)

def load():
    s = Session.load(os.path.join(P, "lighthouse.easel"))
    ns = {k: getattr(easel, k) for k in dir(easel) if not k.startswith("_")}
    ns["s"] = s
    exec(open(os.path.join(P, "prelude.py")).read(), ns)
    return s, ns

def run_variants(tag, variants, values=False, region=None):
    s, ns = load()
    paths = []
    for name, fn in variants:
        c = s.scratch()
        ns["s"] = c; ns["p"] = c.palette
        fn(c, c.palette, ns)
        path = os.path.join(P, "out", f"var_{tag}_{name}.png")
        c.look(path=path, values=values, region=region, marks=False, sketch=False)
        paths.append(path)
        print(name, "->", c.stroke_count - s.stroke_count, "strokes")
    return paths
