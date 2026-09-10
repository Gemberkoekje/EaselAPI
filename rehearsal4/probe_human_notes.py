"""Numbers for the two things the human saw in `pass/out/look_046.png`.

Both notes arrived while the session was still painting, and neither was passed to
it -- a fresh session that gets coached is not measuring the guide any more. They are
measured here instead, so the write-up can say how big each one is rather than that
somebody minded.

Unlike `PREREGISTERED.md`, nothing here was written in advance: these probes were
built to put a number on a defect that had already been seen. That is what they are
good for and it is the only thing they are good for. Neither is a pass criterion.

**Note 1 -- "the tea kinda flows out of the mug".** The mug is a container, so its
depth order is far rim, then the liquid, then the near wall. Painted in the other
order the liquid has no edge to stop against and runs off the side. Measured as: dark
paint inside the mouth's bounding box that is nowhere near dark in the photograph.

**Note 2 -- "a table correction was done after the mug ear was drawn".** The guide's
own rule is that a mistake in the background stops being cheap the moment something
stands in front of it. Measured from the log, which is the only place the order of
events survives: how much broad mass paint landed on top of ground already carrying a
fine mark, and which marks did it.

Run from the repo root:  python rehearsal4/probe_human_notes.py [session.easel ...]
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

#: The mug's mouth in normalised coordinates, read off `_ref_grid_mug.png`: from
#: just above the far rim to just below the front lip, and the full width of the rim.
MOUTH = (0.28, 0.05, 0.68, 0.36)
#: What counts as "the dark in the cup" in either picture.
DARK = 0.22
#: How far off a photograph's dark a mark may land before it counts as escaped, as a
#: fraction of the picture's width. A brush edge is soft and a silhouette that
#: overlaps a little is the guide's own advice, so this is deliberately generous.
SLACK = 0.02

#: Brush sizes, in the guide's own terms: a detail mark against a mass.
FINE = 0.02
MASS = 0.05


# -- note 1: did the liquid stay in the cup? -------------------------------------

def _value(path: str, longest: int = 800) -> np.ndarray:
    im = Image.open(path).convert("L")
    im = im.resize((longest, round(longest * im.height / im.width)), Image.LANCZOS)
    return np.asarray(im, dtype=np.float64) / 255.0


def _crop(a: np.ndarray, box) -> np.ndarray:
    h, w = a.shape
    x0, y0, x1, y1 = box
    return a[round(y0 * h):round(y1 * h), round(x0 * w):round(x1 * w)]


def _dilate(mask: np.ndarray, radius: int) -> np.ndarray:
    """Square dilation by `radius`, written out rather than pulled from scipy."""
    out = mask.copy()
    for _ in range(radius):
        padded = np.pad(out, 1, mode="edge")
        out = (padded[:-2, 1:-1] | padded[2:, 1:-1] | padded[1:-1, :-2]
               | padded[1:-1, 2:] | padded[1:-1, 1:-1])
    return out


def containment(painting: str, reference: str, label: str) -> None:
    if not os.path.exists(painting):
        print(f"  {label:<34} (missing)")
        return
    canvas = _crop(_value(painting), MOUTH)
    ref = _crop(_value(reference), MOUTH)
    if canvas.shape != ref.shape:  # the two crops round independently
        ref = np.asarray(Image.fromarray((ref * 255).astype(np.uint8))
                         .resize((canvas.shape[1], canvas.shape[0]), Image.LANCZOS),
                         dtype=np.float64) / 255.0

    ref_dark = ref < DARK
    canvas_dark = canvas < DARK
    allowed = _dilate(ref_dark, max(1, round(SLACK * canvas.shape[1])))
    escaped = canvas_dark & ~allowed

    ref_area = int(ref_dark.sum())
    share = 100.0 * escaped.sum() / max(ref_area, 1)
    if escaped.any():
        cols = np.where(escaped.any(axis=0))[0]
        # How far past the allowed dark the worst column reaches, as a fraction of
        # the whole picture's width.
        span = (cols.max() - cols.min() + 1) / canvas.shape[1] * (MOUTH[2] - MOUTH[0])
    else:
        span = 0.0
    print(f"  {label:<34} {share:6.1f} %   over {span:.3f} of the picture's width")


# -- note 2: what got painted over, and when? ------------------------------------

def _footprint(record: dict, w: int, h: int) -> np.ndarray:
    """A mark's rough footprint: a disc of its brush size swept along its points."""
    mask = np.zeros((h, w), dtype=bool)
    pts = record.get("points") or []
    size = float(record.get("params", {}).get("size", 0.02) or 0.02)
    radius = max(1.0, size / 2.0 * w)
    ys, xs = np.mgrid[0:h, 0:w]
    for i in range(len(pts)):
        x0, y0 = pts[i]
        x1, y1 = pts[min(i + 1, len(pts) - 1)]
        # Distance from the pixel centre to this segment, in pixels.
        ax, ay = x0 * w, y0 * h
        bx, by = x1 * w, y1 * h
        dx, dy = bx - ax, by - ay
        length = dx * dx + dy * dy
        t = 0.0 if length == 0 else np.clip(((xs - ax) * dx + (ys - ay) * dy) / length,
                                            0.0, 1.0)
        mask |= np.hypot(xs - (ax + t * dx), ys - (ay + t * dy)) <= radius
    return mask


def overpainting(path: str, label: str, grid: int = 200) -> None:
    if not os.path.exists(path):
        print(f"\n  {label}: missing ({path})")
        return
    with np.load(path, allow_pickle=False) as z:
        log = json.loads(str(z["log"]))

    h = round(grid * 0.75)
    detail = np.zeros((h, grid), dtype=bool)
    detail_area = 0
    hits: list[tuple[float, int, str]] = []
    covered = 0

    for record in log:
        if record["kind"] not in ("stroke", "glaze", "smudge"):
            continue
        size = float(record.get("params", {}).get("size", 0.0) or 0.0)
        foot = _footprint(record, grid, h)
        if size >= MASS and detail.any():
            over = int((foot & detail).sum())
            if over:
                covered += over
                hits.append((100.0 * over / max(detail.sum(), 1), record["index"],
                             record.get("note", "")))
            # A mass that lands on a fine mark buries it; it is no longer detail.
            detail &= ~foot
        if size <= FINE:
            detail |= foot
            detail_area = max(detail_area, int(detail.sum()))

    print(f"\n  {label}")
    print(f"    broad marks landing on an earlier fine mark   {len(hits)}")
    print(f"    detail area they buried, as a share of the "
          f"most detail ever standing   {100.0 * covered / max(detail_area, 1):.1f} %")
    for share, index, note in sorted(hits, reverse=True)[:6]:
        print(f"      #{index:<4} buried {share:5.1f} % of the standing detail"
              f"   {note[:54]}")


if __name__ == "__main__":
    print("Note 1 - did the dark in the cup stay in the cup?")
    print("  (dark paint in the mouth's box that is nowhere near dark in the photo,")
    print(f"   with {SLACK:.0%} of the width of slack for a soft edge)\n")
    containment(f"{HERE}/pass/copy_final.png", "C:/temp/Level1.jpg",
                "REHEARSAL4 pass (mug)")
    containment(f"{ROOT}/rehearsal3/pass/copy_final.png", "C:/temp/Level1.jpg",
                "REHEARSAL3 pass (mug)")
    containment(f"{ROOT}/rehearsal3/assisted/copy_final.png", "C:/temp/Level1.jpg",
                "REHEARSAL3 assisted (mug)")

    print("\n\nNote 2 - what got painted over after it was drawn?")
    print(f"  (a 'fine' mark is size <= {FINE}, a 'mass' is size >= {MASS})")
    targets = sys.argv[1:] or [
        f"{HERE}/pass/copy.easel",
        f"{ROOT}/rehearsal3/pass/copy.easel",
    ]
    for target in targets:
        overpainting(target, os.path.relpath(target, ROOT).replace("\\", "/"))
