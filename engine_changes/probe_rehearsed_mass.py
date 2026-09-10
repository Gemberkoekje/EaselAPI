"""A rehearsed mass is now the mass that lands. Item 2 of `ENGINE_CHANGES.md`.

`rehearse()` paints a plan on a copy of the canvas and shows the result. Two things
were missing for the calls that lay a *mass*, which is where the money goes -- one
call, ten to thirty strokes:

1. **`sweep` could not be described at all.** `block_in` could (M8 added `shape=`);
   `sweep` raised "A stroke spec needs 'points'".
2. **What was rehearsed was not what landed.** A block-in's pass wander comes from
   the session's running generator, and the trial deliberately had a *different*
   one, so the rehearsal showed the same mass with a different hand. `NOTES.md`
   note 23 recorded that and told you not to test for equality.

The trial now holds a *copy* of the session's stream state. A copy draws exactly
what the real call would draw next, and spending it costs the real session nothing --
which is the whole reason the trial had its own stream in the first place.

This measures both halves::

    python engine_changes/probe_rehearsed_mass.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO / "src") not in sys.path:
    sys.path.insert(0, str(_REPO / "src"))

from easel import Session, blob, span  # noqa: E402

MASS = blob(span("D4", "F6"), wobble=0.3, seed=2, name="mass")
EDGE = [(0.06, 0.68), (0.31, 0.48), (0.56, 0.63), (0.84, 0.45)]
MASS_ARGS = dict(brush="bristle", color="dark", size=0.09, direction="axis")
SWEEP_ARGS = dict(brush="bristle", color="dark", size=0.12, into="down", depth=0.30,
                  cross=25)


def session() -> Session:
    """A painting already under way, so the trial has a stream state to copy."""
    s = Session(560, 420, ground="toned_grey", seed=3, timelapse=False,
                out_dir=_REPO / "out")
    s.palette["dark"] = s.palette.mix("ultramarine", "burnt_umber", 0.45)
    s.block_in("upper-half", "bristle", "burnt_umber", density=0.5, size=0.14)
    return s


def pair(what: str) -> tuple[Session, Session]:
    """The same mass twice: once on the scrap of canvas, once for real."""
    a, b = session(), session()
    trial = a._trial_session()
    if what == "mass":
        trial.block_in(MASS, **MASS_ARGS)
        b.block_in(MASS, **MASS_ARGS)
    else:
        trial.sweep(EDGE, **SWEEP_ARGS)
        b.sweep(EDGE, **SWEEP_ARGS)
    return trial, b


def measure() -> list[tuple[str, Image.Image]]:
    made: list[tuple[str, Image.Image]] = []
    for what in ("mass", "sweep"):
        trial, real = pair(what)
        rehearsed = trial.canvas.to_srgb8().astype(np.int16)
        landed = real.canvas.to_srgb8().astype(np.int16)
        delta = np.abs(rehearsed - landed).max(axis=2)
        print(f"{what:>6}: {len(real.history.records) - 1:2d} strokes,  "
              f"pixels that differ {int((delta > 0).sum()):6d},  max delta {int(delta.max())}")
        made.append((f"{what}: rehearsed", Image.fromarray(rehearsed.astype(np.uint8))))
        made.append((f"{what}: painted for real", Image.fromarray(landed.astype(np.uint8))))
    return made


def costs_nothing() -> None:
    """The other promise: rehearsing writes nothing and changes nothing after it."""
    a = session()
    a.rehearse([dict(MASS_ARGS, shape=MASS)], path=_REPO / "out" / "_rh_mass.png")
    a.rehearse(dict(SWEEP_ARGS, edge=EDGE), path=_REPO / "out" / "_rh_sweep.png")
    a.sweep(EDGE, **SWEEP_ARGS)

    b = session()
    b.sweep(EDGE, **SWEEP_ARGS)
    print()
    print(f"after two rehearsals, the painting that follows is identical: "
          f"{np.array_equal(a.canvas.rgb, b.canvas.rgb)}")
    print(f"the rehearsals cost {a.stroke_count - b.stroke_count} marks and "
          f"{len(a.history.records) - len(b.history.records)} log records")


def build(made) -> Image.Image:
    label_h, gap = 20, 3
    cols, rows = 2, len(made) // 2
    w, h = made[0][1].size
    sheet = Image.new("RGB", (cols * w + gap, rows * (h + label_h)), (18, 18, 20))
    draw = ImageDraw.Draw(sheet)
    for i, (title, img) in enumerate(made):
        x = (i % cols) * (w + gap)
        y = (i // cols) * (h + label_h)
        draw.text((x + 6, y + 5), title, fill=(250, 238, 200))
        sheet.paste(img, (x, y + label_h))
    return sheet


def main(argv: list[str]) -> int:
    made = measure()
    costs_nothing()
    out = Path(argv[0]) if argv else Path(__file__).parent / "rehearsed_mass.png"
    sheet = build(made)
    sheet.save(out)
    print(f"\nWrote {out} ({sheet.size[0]}x{sheet.size[1]})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
