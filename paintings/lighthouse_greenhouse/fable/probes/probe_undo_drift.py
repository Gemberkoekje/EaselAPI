"""CLI `easel undo` is not reliably lossless.

Rebuilds this painting four ways and diffs each against the committed painting.png:

  clean   p1..p13 in one invocation                         -> byte-identical
  plan    p0_plan first, then p1..p13                        -> byte-identical
  split   same marks, split across invocations, no undo      -> byte-identical
  undo    p1..p10 | p11(v1) | easel undo 3 | p11(v2) p12 p13 -> ~1.06% drift

Only the undo path drifts, and only in the region painted after the undo. In-process
s.undo(), save/load alone, and simplified CLI-undo cases all restore byte for byte
(see the notes), so this is not a universal undo bug -- it resisted minimization, which
points at accumulated state (RNG cursor or wet layer) not surviving the CLI undo's
save->undo->load boundary under conditions a full painting sets up. Practice: for a
reproducible result, rebuild from edited scripts or undo in-process, not via CLI mid-run.

Slow: it repaints the picture four times (~4 minutes).
Run: .venv/bin/python probes/probe_undo_drift.py
"""
import os
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
FABLE = os.path.abspath(os.path.join(HERE, ".."))
EASEL = os.path.join(os.path.dirname(sys.executable), "easel")
COMMITTED = os.path.join(FABLE, "painting.png")

PRELUDE = os.path.join(FABLE, "prelude.py")
P0 = os.path.join(FABLE, "p0_plan.py")
EARLY = [f"p{n}" for n in ("1_fog", "2_beam", "3_sea", "4_rocks", "5_tower",
                           "6_lantern", "7_stairs", "8_base", "9_finish",
                           "9b_counterbeam", "10_rail")]
LATE = ["p11_last", "p12_rock_again", "p13_sign"]
EARLY = [os.path.join(FABLE, f + ".py") for f in EARLY]
LATE = [os.path.join(FABLE, f + ".py") for f in LATE]

# p11 v1: the version whose fog strokes crossed the tower (before it was stopped short)
P11_V1 = """
s.stroke([(-0.02, 0.665), (0.30, 0.672), (0.62, 0.664)], "round_soft", "fog_low", size=0.04,
         opacity=0.30, load=1.0, load_falloff=0.0, pressure=[0.6, 1.0, 0.3], note="fog on the water")
s.stroke([(0.20, 0.705), (0.48, 0.712), (0.80, 0.70), (1.03, 0.706)], "round_soft", "fog_low", size=0.035,
         opacity=0.25, load=1.0, load_falloff=0.0, pressure=[0.2, 0.9, 1.0, 0.4], note="fog on the water, lower")
s.dab(0.661, 0.219, "round_hard", p.mix("glow", "titanium_white", 0.6), size=0.009, press=3, note="lamp")
"""


def run(easel_file, scripts, cwd):
    subprocess.run([EASEL, "run", easel_file, "--prelude", PRELUDE, *scripts],
                   cwd=cwd, capture_output=True)


def build(name, cwd):
    ef = os.path.join(cwd, name + ".easel")
    subprocess.run([EASEL, "new", ef, "--size", "1024x768", "--texture", "linen",
                    "--ground", "toned_warm_grey", "--seed", "47", "--budget", "300"],
                   cwd=cwd, capture_output=True)
    out = os.path.join(cwd, name + ".png")
    exp = os.path.join(cwd, f"exp_{name}.py")
    open(exp, "w").write(f"print(s.export({out!r}))\n")
    if name == "clean":
        run(ef, EARLY + LATE, cwd)
    elif name == "plan":
        run(ef, [P0] + EARLY + LATE, cwd)
    elif name == "split":
        run(ef, EARLY, cwd)
        run(ef, LATE, cwd)
    elif name == "undo":
        run(ef, EARLY, cwd)
        v1 = os.path.join(cwd, "p11_v1.py")
        open(v1, "w").write(P11_V1)
        run(ef, [v1], cwd)
        subprocess.run([EASEL, "undo", ef, "3"], cwd=cwd, capture_output=True)
        run(ef, LATE, cwd)
    run(ef, [exp], cwd)
    return out


def diff(png):
    c = np.asarray(Image.open(COMMITTED).convert("RGB")).astype(int)
    a = np.asarray(Image.open(png).convert("RGB")).astype(int)
    d = np.abs(a - c).max(axis=2)
    reg = ""
    ys, xs = np.nonzero(d > 8)
    if len(ys):
        reg = f"  >8 span x{xs.min()/1024:.2f}-{xs.max()/1024:.2f} y{ys.min()/768:.2f}-{ys.max()/768:.2f}"
    return f"differ {(d>0).mean()*100:5.2f}%  >8/255 {(d>8).mean()*100:6.3f}%  max {int(d.max()):3d}{reg}"


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as cwd:
        for name in ("clean", "plan", "split", "undo"):
            png = build(name, cwd)
            print(f"{name:6s} {diff(png)}")
    print("\nExpected: clean/plan/split byte-identical (0.00%); undo ~1.06% in x0.50-0.90 y0.16-0.91.")
