"""The bristle comb: is it the same on every stroke, and how wide are its streaks?

Both questions come from REHEARSAL2.md's *Still open* and the brief's M7. Run it
against either engine -- the numbers below are what M7 changed:

    python m7/probe_comb.py                                  # this engine
    PYTHONPATH=/path/to/pre-m7/src python m7/probe_comb.py   # the M6 engine

Everything that could make two marks differ *other than* the comb is turned off:
no jitter, no size jitter, no tooth gating, no run-out, the same canvas, the same
path. What is left is the brush. On the M6 engine the four marks are identical to
the last bit; on this one they are four marks.
"""

from __future__ import annotations

import numpy as np

from easel.brush import brush
from easel.canvas import Canvas
from easel.stroke import paint_stroke

SIZE = (900, 600)


def bare(size: float):
    return brush("bristle", size=size, jitter=0.0, size_jitter=0.0,
                 texture_sensitivity=0.0, load_falloff=0.0)


def mark(b, index: int) -> np.ndarray:
    """One horizontal mark, painted as stroke number ``index`` of a painting."""
    c = Canvas(*SIZE, texture="smooth", ground="warm_white", seed=3)
    before = c.rgb.copy()
    paint_stroke(c, [(0.08, 0.5), (0.92, 0.5)], b, "#FFFFFF", "even",
                 np.random.default_rng([3, index]))
    return np.abs(c.rgb - before).max(axis=2)


def section(deposit: np.ndarray, x0: int = 380, x1: int = 520) -> np.ndarray:
    col = deposit[:, x0:x1].mean(axis=1)
    ink = np.nonzero(col > col.max() * 0.12)[0]
    return col[ink[0] : ink[-1] + 1]


def streaks(band: np.ndarray) -> int:
    """How many streaks lie across a mark: sign changes of the de-trended profile."""
    w = max(3, (len(band) // 2) | 1)
    residual = band - np.convolve(band, np.ones(w) / w, mode="same")
    sign = np.sign(residual)
    sign = sign[sign != 0]
    return max(1, int(np.sum(sign[1:] != sign[:-1])) // 2 + 1)


def same_comb_every_time() -> None:
    print("Four bristle marks, one brush, identical canvas and path.")
    print("Only which stroke of the painting it is differs.\n")
    b = bare(0.12)
    first = mark(b, 0)
    a = section(first)
    for index in (1, 2, 3):
        other = mark(b, index)
        band = section(other)
        n = min(len(a), len(band))
        print(f"  stroke 0 vs stroke {index}:  "
              f"identical pixels: {str(np.array_equal(first, other)):5s}   "
              f"comb correlation {np.corrcoef(a[:n], band[:n])[0, 1]:+.3f}")
    print("\n  (True / +1.000 is the brush printing one fixed comb over and over)")


def streaks_against_size() -> None:
    print("\nStreak width against brush size, on a 900 px canvas:\n")
    print("  size    tip width   bristles   streaks across the mark   streak width")
    for size in (0.02, 0.04, 0.08, 0.12, 0.18):
        b = bare(size)
        band = section(mark(b, 0))
        count = b.bristles(size * 900) if hasattr(b, "bristles") else b.bristle_count
        n = streaks(band)
        print(f"  {size:.3f}   {size * 900:6.1f} px   {count:6d}   "
              f"{n:14d}            {len(band) / n:5.1f} px")
    print("\n  A bristle has a width of its own, so the count should follow the brush")
    print("  and the width should not. Before M7 the count was 22 at every size.")


if __name__ == "__main__":
    same_comb_every_time()
    streaks_against_size()
