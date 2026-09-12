"""The measurements behind the fourth session's list in SUGGESTIONS.md.

Five probes on stated canvases, each printing the numbers quoted in
``CALIBRATION.md`` and in the docstrings the fourth round changed: how far the
rendered view moves a mass off the paint it is made of, what a smudge's ``size``
buys and costs on a steep join, how a banded scumble bands when its brush is
narrower than its own pass step, whether opacity makes a passage quieter, and which
edges ``overhang`` actually lengthens.

**Two of the six requests did not survive being measured**, and this script is where
that is visible rather than asserted: the relief cancels over a mass (probe one), and
a shape blocked in at ``overhang=0`` is not left bare at its ends by anything but the
comb's own texture (probe five). Both answers are in ``SUGGESTIONS.md`` beside the
request, which is `LESSONS.md`'s *check the painters' numbers* applied to a list that
had already priced them.

    python scripts/probe_fourth_session.py          # writes out/probe_fourth_*.png
"""

from __future__ import annotations

import warnings
from pathlib import Path

import numpy as np

from easel import Region, Session, polygon
from easel.color import linear_to_srgb, luminance

OUT = Path("out")


def new(width: int = 512, height: int = 384, seed: int = 5) -> Session:
    return Session(width, height, texture="linen", ground="toned_grey", seed=seed,
                   timelapse=False, out_dir=OUT)


def value_of(rgb: np.ndarray) -> np.ndarray:
    """The value ``look(values=True)`` shows, per pixel, of a linear-light array."""
    return linear_to_srgb(luminance(np.asarray(rgb, dtype=np.float32)))


# -- 1. the paint, and the view of it --------------------------------------------------
def probe_relief() -> None:
    """Does the rendered relief lift a solid mass off the value it was mixed at?

    The request says it does, and prices it as the most expensive item on the list.
    It does not: the relief is a gradient of the paint height, so it brightens one
    side of every ridge and darkens the other by as much, and that cancels over any
    area bigger than a ridge.
    """
    print("\n== the paint and the view of it ==")
    print("  512x384 linen, a mass 0.60x0.20 over a solid wall, flat at size=0.030.")
    print(f"  {'mixed':>7} {'solid':>6} {'paint':>7} {'view':>7} {'gap':>7} {'worst px':>9}")
    for target in (0.215, 0.26, 0.33, 0.50):
        for solid in (False, True):
            s = new()
            s.palette["wall"] = s.palette.at_value("burnt_umber", 0.17)
            s.palette["mass"] = s.palette.at_value("burnt_umber", target)
            s.block_in((0.0, 0.0, 1.0, 1.0), "flat", "wall", size=0.05, solid=True)
            s.dry()
            s.block_in(Region(0.20, 0.35, 0.80, 0.55), "flat", "mass", size=0.030,
                       solid=solid)
            inner = Region(0.22, 0.37, 0.78, 0.53)
            x0, y0, x1, y1 = s.canvas.region_px(inner)
            paint = value_of(s.canvas.composite(impasto=False, sketch=False))[y0:y1, x0:x1]
            view = value_of(s.canvas.composite(impasto=True, sketch=False))[y0:y1, x0:x1]
            print(f"  {target:7.3f} {str(solid):>6} {paint.mean():7.3f} {view.mean():7.3f} "
                  f"{view.mean() - paint.mean():+7.3f} {np.abs(view - paint).max():+9.3f}")
    print("  So `solid=True` costs nothing in the view, and the row the request asked")
    print("  CALIBRATION.md for is a row of zeroes.")


# -- 2. what a smudge's size buys, and what it costs -----------------------------------
def _steep_join(seed: int = 7) -> tuple[Session, int, slice]:
    """Light over dark, both solid, plus where the boundary really ended up.

    Blocked in at ``size=0.030`` rather than a wide brush on purpose: a pass is wider
    than the step between passes, so a 0.10 brush lays the dark mass's own paint 30px
    above the outline it was given and the join is nowhere near where it was drawn.
    """
    s = new(640, 480, seed=seed)
    s.palette["lit"] = s.palette.at_value("titanium_white", 0.78)
    s.palette["wall"] = s.palette.at_value("burnt_umber", 0.17)
    s.block_in(polygon([(-0.05, 0.02), (1.05, 0.02), (1.05, 0.50), (-0.05, 0.50)]),
               "flat", "lit", size=0.030, solid=True)
    s.block_in(polygon([(-0.05, 0.50), (1.05, 0.50), (1.05, 0.98), (-0.05, 0.98)]),
               "flat", "wall", size=0.030, solid=True)
    s.dry()
    h, w = s.canvas.height, s.canvas.width
    columns = slice(int(0.42 * w), int(0.58 * w))
    profile = (s.canvas.values() / 255.0)[:, columns].mean(axis=1)
    edge = int(np.argmax(np.abs(np.diff(profile))[int(0.35 * h):int(0.65 * h)]))
    return s, edge + int(0.35 * h), columns


def probe_smudge_window() -> None:
    print("\n== what a smudge's size buys, and what it costs ==")
    print("  640x480 linen, a step from 0.78 to 0.17, one pass along the boundary.")
    base, edge, columns = _steep_join()
    h = base.canvas.height
    before = (base.canvas.values() / 255.0)[:, columns].mean(axis=1)
    bare = float(np.abs(np.diff(before[edge - 40:edge + 40])).max() * (h / 100.0))
    print(f"  bare join: {bare:.3f} of value per 1% of canvas height")
    print(f"  {'size':>6} {'sharpness':>10} {'softened':>9} {'carried into the dark':>22}")
    for size in (0.008, 0.011, 0.016, 0.020, 0.024, 0.028, 0.032, 0.040, 0.070):
        s, _, _ = _steep_join()
        with warnings.catch_warnings():     # the point of the probe is the wide end
            warnings.simplefilter("ignore", UserWarning)
            s.smudge([(0.30, (edge + 0.5) / h), (0.70, (edge + 0.5) / h)], size=size)
        after = (s.canvas.values() / 255.0)[:, columns].mean(axis=1)
        sharp = float(np.abs(np.diff(after[edge - 40:edge + 40])).max() * (h / 100.0))
        lifted = np.flatnonzero((after - before)[edge:] > 0.03)
        reach = (int(lifted.max()) + 1) / h * 100 if len(lifted) else 0.0
        print(f"  {size:6.3f} {sharp:10.3f} {sharp / bare - 1:+8.0%} {reach:21.2f}%")
    print("  The softening arrives at 0.016 and stops improving; the reach does not.")


# -- 3. a band, and the brush that closes its joins ------------------------------------
def probe_scumble_step() -> None:
    print("\n== a banded scumble's brush, in pass steps ==")
    band = Region(0.10, 0.30, 0.90, 0.70, name="band")
    n, step = 8, (0.70 - 0.30) / 8
    print(f"  640x480 linen, ground 0.53, a band 0.80x0.40 in {n} passes from 0.20 to")
    print(f"  0.70, bristle at opacity 0.5. The step across the band is {step:.3f}.")
    print(f"  {'brush':>7} {'steps':>6} {'ripple':>8} {'delivered':>14}")
    for k in (0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0):
        s = new(640, 480, seed=7)
        s.palette["a"] = s.palette.at_value("burnt_umber", 0.20)
        s.palette["b"] = s.palette.at_value("titanium_white", 0.70)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            s.scumble(band, "a", "b", n, size=max(k * step, 0.004))
        v = s.canvas.values() / 255.0
        x0, y0, x1, y1 = s.canvas.region_px(band)
        inset = int(0.12 * (x1 - x0))
        profile = v[y0:y1, x0 + inset:x1 - inset].mean(axis=1)
        win = max(3, int(round(step * s.canvas.height)))
        smooth = np.convolve(profile, np.ones(win) / win, mode="same")
        core = slice(win, len(profile) - win)
        print(f"  {k * step:7.4f} {k:5.2f}x {np.abs(profile - smooth)[core].std():8.4f} "
              f"   {profile[core].min():.2f}..{profile[core].max():.2f}")
    print("  Worst at one to one and a half steps, which is where a preset's default")
    print("  lands; the ramp starts collapsing past about five. Three is the middle.")


# -- 4. opacity does not make a passage quieter ----------------------------------------
def probe_scumble_opacity() -> None:
    print("\n== opacity on a passage that overlaps itself ==")
    band = Region(0.10, 0.35, 0.90, 0.65, name="band")
    print("  640x480 linen, 8 passes from 0.30 to 0.62 over a solid 0.22 ground,")
    print("  brush picked from the step.")
    print(f"  {'opacity':>8} {'mean':>6} {'span':>13}")
    for opacity in (0.15, 0.25, 0.40, 0.60, 0.80, 1.00):
        s = new(640, 480, seed=7)
        s.palette["road"] = s.palette.at_value("burnt_umber", 0.22)
        s.palette["a"] = s.palette.at_value("burnt_umber", 0.30)
        s.palette["b"] = s.palette.at_value("titanium_white", 0.62)
        s.block_in((0.0, 0.0, 1.0, 1.0), "flat", "road", size=0.05, solid=True)
        s.dry()
        s.scumble(band, "a", "b", 8, opacity=opacity)
        v = s.canvas.values() / 255.0
        h, w = v.shape
        m = v[int(0.40 * h):int(0.60 * h), int(0.2 * w):int(0.8 * w)]
        print(f"  {opacity:8.2f} {m.mean():6.2f}   {m.min():.2f}..{m.max():.2f}")
    print("  Below 0.4 it thins a little; above it, nothing. The passes accumulate.")


# -- 5. which edges overhang lengthens -------------------------------------------------
def probe_overhang() -> None:
    print("\n== overhang, and which edges it moves ==")
    shape = polygon([(0.30, 0.30), (0.70, 0.30), (0.70, 0.60), (0.30, 0.60)], name="lit")
    print("  640x480 linen, a shape 0.40x0.30 blocked in solid, bristle at size=0.030")
    print("  (19px). Reach past each edge, in pixels, and the share of the half-brush")
    print("  strip inside the pass ends still within 0.02 of the ground -- against the")
    print("  same strip inside the sides, which is the comb's own texture.")
    for direction, solid in (("horizontal", True), ("horizontal", False),
                             ("vertical", True)):
        print(f"  passes {direction}, "
              f"{'solid' if solid else 'at the default load'}:")
        print(f"    {'overhang':>9} {'left':>6} {'right':>6} {'top':>6} {'bottom':>7} "
              f"{'bare ends':>10} {'bare sides':>11}")
        for over in (0.0, 0.35, 1.0):
            s = new(640, 480, seed=7)
            before = s.canvas.values() / 255.0
            s.block_in(shape, "bristle", "titanium_white", size=0.030, solid=solid,
                       direction=direction, overhang=over)
            after = s.canvas.values() / 255.0
            painted = np.abs(after - before) >= 0.02
            h, w = painted.shape
            sideways = np.flatnonzero(painted[int(0.35 * h):int(0.55 * h), :].any(axis=0))
            updown = np.flatnonzero(painted[:, int(0.35 * w):int(0.65 * w)].any(axis=1))
            ends = painted[int(0.32 * h):int(0.58 * h), int(0.30 * w):int(0.315 * w)]
            sides = painted[int(0.30 * h):int(0.315 * h), int(0.32 * w):int(0.68 * w)]
            print(f"    {over:9.2f} {0.30 * w - sideways.min():5.0f}px "
                  f"{sideways.max() - 0.70 * w:4.0f}px {0.30 * h - updown.min():4.0f}px "
                  f"{updown.max() - 0.60 * h:5.0f}px {(~ends).sum() / ends.size:9.1%} "
                  f"{(~sides).sum() / sides.size:10.1%}")
    print("  The two edges it lengthens turn with the pass direction; the other two")
    print("  keep their half-brush whatever it is set to. The ends do run barer at")
    print("  overhang=0 -- but only at the default load, and a comb leaves as much of")
    print("  the ground showing along the *sides*, where overhang does nothing at all.")
    print("  So what that measures is the brush running dry and the comb's own")
    print("  texture, not a boundary left unpainted: solid=True leaves neither. That")
    print("  is why the warning the request asked for is not built -- its condition is")
    print("  block_in's own defaults, and what it would be pointing at is the load.")


def main() -> None:
    OUT.mkdir(exist_ok=True)
    probe_relief()
    probe_smudge_window()
    probe_scumble_step()
    probe_scumble_opacity()
    probe_overhang()


if __name__ == "__main__":
    main()
