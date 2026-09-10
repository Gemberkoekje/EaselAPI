"""How far does one dab get towards its colour, and how many does a catchlight need?

The brief's reason for giving `dab()` a `press` argument: "a single dab lands at
about a third of its colour's strength, and a highlight the size of a catchlight
needs three". This measures it -- on the ground the highlight is actually being put
on, since how far a dab gets depends on what is under it.

    python m7/probe_dab.py                                  # this engine
    PYTHONPATH=/path/to/pre-m7/src python m7/probe_dab.py   # the M6 engine

On the M6 engine `press` does not exist, so the same mark costs one stroke per
stamp; the probe falls back to that and reports what it spent.
"""

from __future__ import annotations

import inspect

import numpy as np

from easel.session import Session

STAMPS = (1, 2, 3, 4, 5)
SUPPORTED = "press" in inspect.signature(Session.dab).parameters


def reach(ground: str, size: float = 0.06) -> None:
    print(f"\n  {ground:12s}  stamps   value at the centre   of the way to white   strokes")
    for stamps in STAMPS:
        s = Session(400, 300, texture="smooth", ground=ground, seed=4, timelapse=False)
        target = np.asarray(s.palette["titanium_white"], dtype=np.float32)
        before = s.canvas.rgb[150, 200].copy()
        if SUPPORTED:
            s.dab(0.5, 0.5, color="titanium_white", size=size, press=stamps)
        else:
            for _ in range(stamps):
                s.dab(0.5, 0.5, color="titanium_white", size=size)
        after = s.canvas.rgb[150, 200]
        got = float(np.mean((after - before) / np.maximum(target - before, 1e-6)))
        value = float(np.mean(after))
        print(f"  {'':12s}  {stamps:6d}   {value:19.3f}   {got:19.2f}   "
              f"{s.stroke_count:7d}")


def width_of_a_dab() -> None:
    """A round tip's width follows its pressure, and a lone dab is a light touch."""
    print("\nHow wide the mark is, at size 0.06 on a 400 px canvas (24 px nominal):\n")
    print("  stamps   width")
    for stamps in STAMPS:
        s = Session(400, 300, texture="smooth", ground="toned_grey", seed=4,
                    timelapse=False)
        before = s.canvas.rgb.copy()
        if SUPPORTED:
            s.dab(0.5, 0.5, color="titanium_white", size=0.06, press=stamps)
        else:
            for _ in range(stamps):
                s.dab(0.5, 0.5, color="titanium_white", size=0.06)
        d = np.abs(s.canvas.rgb - before).max(axis=2)
        rows = np.nonzero(d.max(axis=1) > 0.004)[0]
        print(f"  {stamps:6d}   {int(rows[-1] - rows[0] + 1):3d} px")


if __name__ == "__main__":
    print("A white dab, stamped on the same spot." if SUPPORTED else
          "A white dab, repeated -- this engine has no `press`, so each stamp is a stroke.")
    for ground in ("toned_grey", "umber_wash", "warm_white"):
        reach(ground)
    width_of_a_dab()
