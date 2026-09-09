"""``look()`` -- how the painter sees the canvas.

This is the most important function in the API. A painter who does not look is
guessing, and an agent that paints twenty strokes without looking has produced
twenty guesses. Everything here is in service of one question: *what is actually
on the canvas right now, and how does it differ from what I intended?*

The views are deliberately plain. A grid overlay so places can be named, a
greyscale view so values can be judged without hue confusing the issue, a
side-by-side against a reference, and a diff against the last look.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

from easel.canvas import Canvas
from easel.color import linear_to_srgb, luminance, srgb_to_linear
from easel.regions import GRID_COLS, GRID_ROWS, as_region

__all__ = ["render_look", "save_look", "load_reference", "DEFAULT_LOOK_SIZE"]

#: Long-side pixel size a ``look()`` is downsampled to by default.
DEFAULT_LOOK_SIZE = 1024

_GRID_LINE = (255, 64, 64)
_GRID_LABEL = (255, 255, 255)
_GRID_LABEL_BG = (200, 32, 32)


def render_look(
    canvas: Canvas,
    scale: int | None = DEFAULT_LOOK_SIZE,
    grid: bool = False,
    values: bool = False,
    region=None,
    reference: Image.Image | None = None,
    diff_against: np.ndarray | None = None,
    impasto: bool = True,
) -> Image.Image:
    """Render a view of the canvas.

    Args:
        canvas: the canvas to look at.
        scale: downsample so the long side is at most this many pixels. ``None``
            renders at full resolution.
        grid: overlay a labelled A-H by 1-8 grid, so places can be named and later
            targeted with :func:`easel.regions.cell`.
        values: render greyscale, to judge the value structure without hue.
        region: crop to a region first -- at full resolution, so this is how to
            inspect a small passage closely.
        reference: if given, place the reference beside the canvas for comparison.
        diff_against: an earlier 8-bit RGB array; changed pixels are tinted.
        impasto: shade paint height as low relief.

    Returns:
        A PIL image, ready to save or hand to a vision model.
    """
    arr = canvas.values() if values else canvas.to_srgb8(impasto=impasto)
    if values:
        arr = np.repeat(arr[:, :, None], 3, axis=2)

    if diff_against is not None:
        arr = _apply_diff(arr, diff_against)

    if region is not None:
        r = as_region(region)
        x0, y0, x1, y1 = canvas.region_px(r)
        arr = arr[y0:y1, x0:x1]
        # A crop is for looking closely, so it is not downsampled below its own size.
        scale = None if scale is None else max(scale, max(arr.shape[0], arr.shape[1]))

    img = Image.fromarray(arr, mode="RGB")

    if scale is not None:
        img = _downsample(img, scale)
    if grid:
        img = _draw_grid(img)
    if reference is not None:
        # The reference gets the same treatment as the canvas, or the comparison is
        # not a comparison: greyscale beside greyscale when values are being judged,
        # and the *same* grid over both, so a place named on one names it on the
        # other. A grid that stops at the edge of your own painting is no use for
        # the one job it has when there is a reference -- getting what you can see
        # over there into the right cell over here.
        ref = reference.convert("RGB")
        if values:
            ref = _as_values(ref)
        img = _side_by_side(img, ref, grid=grid)
    return img


def _as_values(img: Image.Image) -> Image.Image:
    """An image as the greyscale the canvas would show: luminance, sRGB-encoded.

    Not PIL's `grayscale`, which takes a weighted sum of the *encoded* channels.
    That is a different number, and the point of putting these two panels side by
    side is that the same value reads the same in both.
    """
    arr = np.asarray(img, dtype=np.float32) / 255.0
    lum = luminance(srgb_to_linear(arr))
    grey = (linear_to_srgb(lum) * 255.0 + 0.5).astype(np.uint8)
    return Image.fromarray(np.repeat(grey[:, :, None], 3, axis=2), mode="RGB")


def _downsample(img: Image.Image, long_side: int) -> Image.Image:
    w, h = img.size
    longest = max(w, h)
    if longest <= long_side:
        return img
    f = long_side / float(longest)
    return img.resize((max(1, int(round(w * f))), max(1, int(round(h * f)))), Image.LANCZOS)


def _draw_grid(img: Image.Image) -> Image.Image:
    """Overlay a labelled grid. Labels sit inside the cell they name."""
    out = img.convert("RGB").copy()
    draw = ImageDraw.Draw(out)
    w, h = out.size
    ncol, nrow = len(GRID_COLS), len(GRID_ROWS)

    for i in range(1, ncol):
        x = int(round(w * i / ncol))
        draw.line([(x, 0), (x, h)], fill=_GRID_LINE, width=1)
    for j in range(1, nrow):
        y = int(round(h * j / nrow))
        draw.line([(0, y), (w, y)], fill=_GRID_LINE, width=1)

    # Label every cell. Without labels the painter has to count squares, which is
    # exactly the kind of arithmetic this whole module exists to avoid.
    cw, ch = w / ncol, h / nrow
    for ci, col in enumerate(GRID_COLS):
        for ri, row in enumerate(GRID_ROWS):
            label = f"{col}{row}"
            x, y = int(ci * cw) + 2, int(ri * ch) + 2
            draw.rectangle([x, y, x + 17, y + 11], fill=_GRID_LABEL_BG)
            draw.text((x + 3, y + 1), label, fill=_GRID_LABEL)
    return out


def _side_by_side(
    img: Image.Image, reference: Image.Image, gap: int = 12, grid: bool = False
) -> Image.Image:
    """Reference on the left, painting on the right, matched in height."""
    ref = reference.convert("RGB")
    target_h = img.size[1]
    ref_w = max(1, int(round(ref.size[0] * target_h / ref.size[1])))
    ref = ref.resize((ref_w, target_h), Image.LANCZOS)
    if grid:
        # Drawn after the resize, so the cells divide the reference's own frame the
        # way they divide the canvas: D4 is D4 in both panels.
        ref = _draw_grid(ref)

    out = Image.new("RGB", (ref_w + gap + img.size[0], target_h), (24, 24, 24))
    out.paste(ref, (0, 0))
    out.paste(img, (ref_w + gap, 0))
    return out


def _apply_diff(arr: np.ndarray, previous: np.ndarray) -> np.ndarray:
    """Tint pixels that changed since ``previous``, leaving the rest legible."""
    if previous.shape != arr.shape:
        return arr
    delta = np.abs(arr.astype(np.int16) - previous.astype(np.int16)).max(axis=2)
    changed = delta > 6
    if not changed.any():
        return arr
    out = arr.copy()
    # Knock the unchanged areas back and tint what moved, so new work reads at a glance.
    out[~changed] = (out[~changed].astype(np.float32) * 0.55 + 96).astype(np.uint8)
    tint = np.array([255, 80, 80], dtype=np.float32)
    out[changed] = (out[changed].astype(np.float32) * 0.72 + tint * 0.28).astype(np.uint8)
    return out


def save_look(img: Image.Image, path: str | Path) -> Path:
    """Write a look to disk, creating the parent directory if needed."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    img.save(p)
    return p


def load_reference(path: str | Path) -> Image.Image:
    """Load a reference image for ``side_by_side``."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Reference image not found: {p}")
    return Image.open(p).convert("RGB")
