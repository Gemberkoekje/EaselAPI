"""Does pressure change how wide a mark is, or only how much paint lands?

REVIEW.md's open finding, measured: a stroke at `pressure=0.1` and one at `1.0`
covered an identical bounding box, so the six named profiles were indistinguishable
once an opaque colour saturated, and a mark that tapers was two strokes of different
sizes. Run it against either engine:

    python m7/probe_pressure.py                                  # this engine
    PYTHONPATH=/path/to/pre-m7/src python m7/probe_pressure.py   # the M6 engine

The last block is the one the second rehearsal's eye test asked for: a single stroke
that starts at a lid's width and ends at a lash's.
"""

from __future__ import annotations

import numpy as np

from easel.brush import brush
from easel.canvas import Canvas
from easel.stroke import paint_stroke

W, H = 600, 400


def paint(b, pressure, color="#402010"):
    c = Canvas(W, H, texture="smooth", ground="warm_white", seed=3)
    before = c.rgb.copy()
    result = paint_stroke(c, [(0.1, 0.5), (0.9, 0.5)], b, color, pressure,
                          np.random.default_rng([3, 0]))
    return np.abs(c.rgb - before).max(axis=2), result


def height(deposit: np.ndarray) -> int:
    rows = np.nonzero(deposit.max(axis=1) > 0.004)[0]
    return int(rows[-1] - rows[0] + 1) if len(rows) else 0


def flat_pressures() -> None:
    print("round_hard, size 0.06 on a 600 px canvas, one pressure held all the way:\n")
    print("  pressure   width   paint landed")
    b = brush("round_hard", size=0.06, jitter=0.0, size_jitter=0.0)
    for p in (0.1, 0.25, 0.5, 0.75, 1.0):
        deposit, result = paint(b, p)
        print(f"  {p:8.2f}   {height(deposit):3d} px   {result.paint:8.0f}")
    print(f"\n  nominal width: {0.06 * 600:.0f} px")


def named_profiles() -> None:
    print("\nThe six named profiles, same brush, widest and narrowest point of each:\n")
    print("  profile      widest   narrowest")
    b = brush("round_hard", size=0.06, jitter=0.0, size_jitter=0.0)
    for name in ("even", "taper", "press_in", "lift_off", "swell", "dab"):
        deposit, _ = paint(b, name)
        widths = [height(deposit[:, x : x + 40]) for x in range(60, 540, 40)]
        print(f"  {name:10s}   {max(widths):4d} px   {min(widths):4d} px")


def the_eye_test() -> None:
    print("\nOne stroke, pressure [1, 0] -- a lid line that ends as a lash:\n")
    b = brush("liner", size=0.02)
    deposit, _ = paint(b, [1.0, 0.0])
    for x in (100, 220, 340, 460):
        print(f"  at x={x:3d}:  {height(deposit[:, x:x + 60]):3d} px")
    print(f"\n  nominal width: {0.02 * 600:.0f} px. Before M7 every reading was that "
          f"number.")


def the_oriented_tips() -> None:
    print("\nThe oriented tips keep their chisel -- width at pressure 0.2 and 1.0:\n")
    for name in ("flat", "bristle", "knife"):
        b = brush(name, size=0.1, jitter=0.0, size_jitter=0.0)
        light, _ = paint(b, 0.2)
        heavy, _ = paint(b, 1.0)
        print(f"  {name:8s}  {height(light):3d} px   {height(heavy):3d} px")


if __name__ == "__main__":
    flat_pressures()
    named_profiles()
    the_eye_test()
    the_oriented_tips()
