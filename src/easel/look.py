"""``look()`` -- how the painter sees the canvas.

This is the most important function in the API. A painter who does not look is
guessing, and an agent that paints twenty strokes without looking has produced
twenty guesses. Everything here is in service of one question: *what is actually
on the canvas right now, and how does it differ from what I intended?*

The views are deliberately plain. A grid overlay so places can be named, a
greyscale view so values can be judged without hue confusing the issue, a
side-by-side against a reference, and a diff against the last look.

Two things here are about precision below the size of a grid cell, which is what
the second rehearsal ran out of. A crop with ``reference=`` crops **both** panels
to the same place and enlarges them, and ``grid="fine"`` divides that crop into
labelled tenths -- so a place inside a cell is *read off a label* rather than
estimated, and reading labels is something a language model does reliably. The
preview overlay draws intended strokes over both panels without painting them, so
a guess can be checked against the photograph before it is paid for in paint.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

from easel.canvas import Canvas
from easel.color import linear_to_srgb, luminance, srgb_to_linear
from easel.regions import GRID_COLS, GRID_ROWS, Region, as_region

__all__ = ["render_look", "save_look", "load_reference", "DEFAULT_LOOK_SIZE", "MIN_CROP_SIZE"]

#: Long-side pixel size a ``look()`` is downsampled to by default.
DEFAULT_LOOK_SIZE = 1024

_GRID_LINE = (255, 64, 64)
#: A region crop smaller than this on its long side is enlarged to it. One grid
#: cell of a 1200-wide canvas is 150 px, so this shows a cell at more than five
#: times, which is what judging a feature the size of an eye needs.
MIN_CROP_SIZE = 800

_GRID_LABEL = (255, 255, 255)
_GRID_LABEL_BG = (200, 32, 32)
_FINE_LINE = (90, 200, 255)
_FINE_LABEL_BG = (10, 90, 130)
_MARK_COLOR = (255, 210, 40)
_MARK_INK = (20, 16, 4)
_PREVIEW_BAND = (60, 220, 255)
_PREVIEW_LINE = (0, 40, 60)
#: Neutral on purpose. In a values view nothing on screen should carry hue --
#: the chrome included, or the painter is judging value against a tinted label.
_PANEL_LABEL_BG = (18, 18, 18)
_PANEL_LABEL_INK = (230, 230, 230)


class _Frame:
    """One panel, plus the mapping from normalised canvas coordinates into it.

    Both panels of a side-by-side carry the same normalised frame -- D4 is D4 in
    the reference and on the canvas -- so the same overlay code decorates both, and
    a landmark or a previewed stroke lands in the same place in each.
    """

    def __init__(self, img: Image.Image, crop: Region | None, aspect: float = 1.0) -> None:
        self.img = img
        self.crop = crop
        #: The *canvas* aspect (width / height), even for the reference panel: a
        #: brush size is a fraction of the canvas long side, and a previewed band
        #: has to be the same width in both panels or the comparison lies.
        self.aspect = float(aspect)

    def to_px(self, x: float, y: float) -> tuple[float, float]:
        w, h = self.img.size
        if self.crop is None:
            return x * w, y * h
        r = self.crop
        return (x - r.x0) / r.width * w, (y - r.y0) / r.height * h

    def scale_px(self) -> float:
        """Panel pixels for one unit of brush size (a fraction of the canvas long side).

        Measured down the vertical, because the two panels are matched in height:
        the same brush then draws the same band in each.
        """
        h = self.img.size[1]
        span_y = 1.0 if self.crop is None else self.crop.height
        return (h / max(span_y, 1e-6)) * max(self.aspect, 1.0)

    def contains(self, x: float, y: float) -> bool:
        if self.crop is None:
            return 0.0 <= x <= 1.0 and 0.0 <= y <= 1.0
        r = self.crop
        return r.x0 <= x <= r.x1 and r.y0 <= y <= r.y1


def render_look(
    canvas: Canvas,
    scale: int | None = DEFAULT_LOOK_SIZE,
    grid: bool | str = False,
    values: bool = False,
    region=None,
    reference: Image.Image | None = None,
    diff_against: np.ndarray | None = None,
    impasto: bool = True,
    sketch: bool = True,
    marks: dict | None = None,
    strokes: list | None = None,
) -> Image.Image:
    """Render a view of the canvas.

    Args:
        canvas: the canvas to look at.
        scale: downsample so the long side is at most this many pixels. ``None``
            renders at full resolution.
        grid: ``True`` overlays the labelled A-H by 1-8 grid, so places can be named
            and later targeted with :func:`easel.regions.cell`. ``"fine"`` divides
            whatever is on screen into labelled tenths instead, which is how a place
            *inside* a cell gets named.
        values: render greyscale, to judge the value structure without hue.
        region: crop to a region first, enlarged if small -- this is how to inspect
            a passage at the scale of the feature. With ``reference``, **both**
            panels are cropped to the same place.
        reference: if given, place the reference beside the canvas for comparison.
        diff_against: an earlier 8-bit RGB array; changed pixels are tinted.
        impasto: shade paint height as low relief.
        sketch: show the pencil underdrawing the paint has not covered.
        marks: named landmarks to draw on both panels, ``{name: (x, y)}``.
        strokes: previewed strokes to draw over both panels. Each is a dict with
            ``points`` and optionally ``width`` (normalised) and ``label``.

    Returns:
        A PIL image, ready to save or hand to a vision model.
    """
    arr = canvas.values(sketch=sketch) if values else canvas.to_srgb8(impasto=impasto,
                                                                     sketch=sketch)
    if values:
        arr = np.repeat(arr[:, :, None], 3, axis=2)

    if diff_against is not None:
        arr = _apply_diff(arr, diff_against)

    crop: Region | None = None
    if region is not None:
        crop = as_region(region)
        x0, y0, x1, y1 = canvas.region_px(crop)
        arr = arr[y0:y1, x0:x1]
        # A crop is for looking closely, so it is not downsampled below its own size.
        scale = None if scale is None else max(scale, max(arr.shape[0], arr.shape[1]))

    aspect = canvas.width / float(canvas.height)
    img = _fit(Image.fromarray(arr, mode="RGB"), crop is not None, scale)
    panels = [_Frame(img, crop, aspect)]

    if reference is not None:
        ref = reference.convert("RGB")
        if values:
            ref = _as_values(ref)
        if crop is not None:
            # The same normalised place in the reference's own frame. Cropping only
            # the canvas and showing the whole photograph beside it is the one thing
            # a close look must not do: the painter then compares a detail against a
            # thumbnail and reads the wrong value off it.
            ref = _crop_normalised(ref, crop)
        ref = _fit(ref, crop is not None, scale, match_height=img.size[1])
        panels.append(_Frame(ref, crop, aspect))

    for frame in panels:
        _decorate(frame, grid=grid, marks=marks, strokes=strokes)

    if len(panels) == 1:
        return panels[0].img
    return _side_by_side(panels[0].img, panels[1].img)


def _fit(
    img: Image.Image, cropped: bool, scale: int | None, match_height: int | None = None
) -> Image.Image:
    """Enlarge a small crop to a readable size, then apply the scale limit."""
    if match_height is not None:
        w = max(1, int(round(img.size[0] * match_height / img.size[1])))
        return img.resize((w, match_height), Image.LANCZOS)
    if cropped and max(img.size) < MIN_CROP_SIZE:
        # A single grid cell of a 1200-wide canvas is 150 px across, which is too
        # small to inspect anything in. Enlarge small crops; the pixels are the same.
        f = MIN_CROP_SIZE / max(img.size)
        img = img.resize(
            (max(1, round(img.width * f)), max(1, round(img.height * f))), Image.LANCZOS
        )
    if scale is not None:
        img = _downsample(img, scale)
    return img


def _crop_normalised(img: Image.Image, r: Region) -> Image.Image:
    """Crop an image by normalised bounds of its own frame."""
    w, h = img.size
    x0 = int(np.clip(round(r.x0 * w), 0, w - 1))
    y0 = int(np.clip(round(r.y0 * h), 0, h - 1))
    x1 = int(np.clip(round(r.x1 * w), x0 + 1, w))
    y1 = int(np.clip(round(r.y1 * h), y0 + 1, h))
    return img.crop((x0, y0, x1, y1))


def _decorate(frame: _Frame, grid, marks, strokes) -> None:
    """Draw everything that is annotation rather than paint, onto one panel."""
    if strokes:
        frame.img = _draw_strokes(frame, strokes)
    if grid == "fine":
        frame.img = _draw_fine_grid(frame.img, frame.crop)
    elif grid:
        frame.img = _draw_grid(frame.img)
    if marks:
        frame.img = _draw_marks(frame, marks)


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


def _draw_fine_grid(img: Image.Image, crop: Region | None) -> Image.Image:
    """Tenths of whatever is on screen, with the digit of each tenth on the edges.

    Read a place off this as two digits and hand them straight back as
    ``region.point(u, v)``: the label is the *near* edge of its tenth, so the label
    pair (3, 6) is ``point(0.3, 0.6)`` and the middle of that little square is
    ``point(0.35, 0.65)``. No fraction is ever estimated, which is the point --
    estimating fractions of a cell is what the second rehearsal could not do.
    """
    out = img.convert("RGB").copy()
    draw = ImageDraw.Draw(out)
    w, h = out.size

    for i in range(1, 10):
        x = int(round(w * i / 10))
        draw.line([(x, 0), (x, h)], fill=_FINE_LINE, width=1)
        y = int(round(h * i / 10))
        draw.line([(0, y), (w, y)], fill=_FINE_LINE, width=1)

    for i in range(10):
        x = int(round(w * i / 10))
        draw.rectangle([x + 1, 1, x + 11, 12], fill=_FINE_LABEL_BG)
        draw.text((x + 4, 2), str(i), fill=_GRID_LABEL)
        y = int(round(h * i / 10))
        draw.rectangle([1, y + 1, 11, y + 12], fill=_FINE_LABEL_BG)
        draw.text((4, y + 2), str(i), fill=_GRID_LABEL)

    # Bottom *right*: the bottom left belongs to the panel label, and two captions
    # printed over each other is worse than no caption at all.
    name = crop.name if crop is not None and crop.name else "canvas"
    caption = f"{name}  tenths -> point(u, v)"
    box_w = 8 + 6 * len(caption)
    draw.rectangle([w - box_w, h - 13, w, h], fill=_PANEL_LABEL_BG)
    draw.text((w - box_w + 4, h - 12), caption, fill=(210, 235, 255))
    return out


def _draw_marks(frame: _Frame, marks: dict) -> Image.Image:
    """Landmarks as a small cross and a name, on whichever panel this is."""
    out = frame.img.convert("RGB").copy()
    draw = ImageDraw.Draw(out)
    arm = 7
    for name, (x, y) in marks.items():
        if not frame.contains(x, y):
            continue
        px, py = frame.to_px(x, y)
        px, py = int(round(px)), int(round(py))
        for dx, dy in ((1, 1), (0, 0)):
            colour = _MARK_INK if dx else _MARK_COLOR
            draw.line([(px - arm + dx, py + dy), (px + arm + dx, py + dy)], fill=colour)
            draw.line([(px + dx, py - arm + dy), (px + dx, py + arm + dy)], fill=colour)
        label = str(name)
        tx, ty = px + arm + 2, py - 6
        draw.rectangle([tx, ty, tx + 6 * len(label) + 4, ty + 12], fill=_MARK_INK)
        draw.text((tx + 2, ty + 1), label, fill=_MARK_COLOR)
    return out


def _draw_strokes(frame: _Frame, strokes: list) -> Image.Image:
    """Intended strokes: the brush's width as a translucent band, the path over it.

    Nothing here touches the canvas. The whole value of a preview is that a mark can
    be wrong for free, so this draws on the *view* and the painting never hears
    about it.
    """
    base = frame.img.convert("RGBA")
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    ppu = frame.scale_px()

    for i, spec in enumerate(strokes):
        pts = [frame.to_px(float(x), float(y)) for x, y in spec.get("points", [])]
        if not pts:
            continue
        width = max(1, int(round(float(spec.get("width", 0.0)) * ppu)))
        if len(pts) > 1:
            draw.line(pts, fill=_PREVIEW_BAND + (90,), width=width, joint="curve")
            draw.line(pts, fill=_PREVIEW_LINE + (220,), width=1)
        else:
            x, y = pts[0]
            r = max(2, width // 2)
            draw.ellipse([x - r, y - r, x + r, y + r], fill=_PREVIEW_BAND + (90,),
                         outline=_PREVIEW_LINE + (220,))
        for x, y in pts:
            draw.ellipse([x - 2, y - 2, x + 2, y + 2], fill=_MARK_COLOR + (255,))
        label = str(spec.get("label", i + 1))
        lx, ly = pts[0]
        draw.rectangle([lx + 4, ly - 14, lx + 10 + 6 * len(label), ly - 2],
                       fill=_PANEL_LABEL_BG + (220,))
        draw.text((lx + 7, ly - 13), label, fill=_PREVIEW_BAND + (255,))

    return Image.alpha_composite(base, overlay).convert("RGB")


def _side_by_side(img: Image.Image, reference: Image.Image, gap: int = 12) -> Image.Image:
    """Reference on the left, painting on the right, matched in height."""
    target_h = max(img.size[1], reference.size[1])
    out = Image.new("RGB", (reference.size[0] + gap + img.size[0], target_h), (24, 24, 24))
    out.paste(reference, (0, 0))
    out.paste(img, (reference.size[0] + gap, 0))
    _label_panel(out, 0, reference.size[0], "reference")
    _label_panel(out, reference.size[0] + gap, img.size[0], "canvas")
    return out


def _label_panel(img: Image.Image, x: int, width: int, text: str) -> None:
    """Say which panel is which, bottom-left, out of the way of the grid labels."""
    draw = ImageDraw.Draw(img)
    y = img.size[1] - 13
    draw.rectangle([x, y, x + 8 + 6 * len(text), y + 13], fill=_PANEL_LABEL_BG)
    draw.text((x + 4, y + 1), text, fill=_PANEL_LABEL_INK)


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
    if isinstance(path, Image.Image):
        return path.convert("RGB")
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Reference image not found: {p}")
    return Image.open(p).convert("RGB")
