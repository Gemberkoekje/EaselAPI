"""``compare()`` -- the numbers behind a squint.

Looking at two panels side by side tells a painter that something is off. It does
not say *which* mass and by how much, and "a bit too light" is not actionable at
the point where the copy is nearly right and the last twenty strokes have to go in
the correct places. This module puts a number on it, per cell: the mean value of
the reference, the mean value of the canvas, and the difference.

The number that matters is ``0.10``. That is the guide's own threshold: two masses
closer than a tenth of the value range read as one mass, so a cell that far out is
a cell where the painting has lost a separation the photograph has.

Deliberately coarse. This is a measuring stick, not a colour picker -- a painter
who samples the reference pixel by pixel and matches it is tracing, and the mean
colour per cell is here to catch "that whole passage is too warm", nothing finer.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

from easel.color import linear_to_srgb, luminance, srgb_to_linear
from easel.regions import GRID_COLS, GRID_ROWS, Region

__all__ = ["CellCompare", "Comparison", "compare_images", "VALUE_THRESHOLD"]

#: Two masses closer than this in value read as one. PAINTER.md's own threshold,
#: and the definition of done for the M6 copy stage.
VALUE_THRESHOLD = 0.10

_HEAT_COOL = np.array([70, 120, 255], dtype=np.float32)    # canvas darker than reference
_HEAT_WARM = np.array([255, 90, 60], dtype=np.float32)     # canvas lighter
_HEAT_OK = np.array([32, 34, 38], dtype=np.float32)


@dataclass(frozen=True)
class CellCompare:
    """One cell of a comparison."""

    label: str
    #: Normalised centre of the cell, in the compared frame's own coordinates.
    u: float
    v: float
    ref: float
    canvas: float
    delta: float
    ref_hex: str
    canvas_hex: str
    #: What counts as out, for this cell. Sourced from the comparison it belongs
    #: to, so ``off`` agrees with a custom ``compare(threshold=...)`` instead of
    #: silently falling back to the module default regardless of what was asked.
    threshold: float = VALUE_THRESHOLD

    @property
    def off(self) -> bool:
        return abs(self.delta) > self.threshold

    def __str__(self) -> str:
        return (f"{self.label} ref {self.ref:.2f} canvas {self.canvas:.2f} "
                f"{self.delta:+.2f} ({self.ref_hex} vs {self.canvas_hex})")


@dataclass
class Comparison:
    """The result of :meth:`easel.session.Session.compare`.

    Print it. ``str(comparison)`` is the table, and the table is the point; the
    fields are there for a painter that wants to drive off the numbers::

        c = s.compare("reference.jpg")
        print(c)
        for cell in c.off:
            ...                     # every cell more than 0.10 out
    """

    cells: list[CellCompare]
    columns: list[str]
    rows: list[str]
    region: Region | None
    path: Path | None = None
    threshold: float = VALUE_THRESHOLD
    #: The darkest value the palette can reach. Cells whose *reference* is more than
    #: a threshold below it are out of reach of any stroke; zero disables the split.
    floor: float = 0.0

    def __post_init__(self) -> None:
        self._by_label = {c.label: c for c in self.cells}

    def __getitem__(self, label: str) -> CellCompare:
        key = str(label).strip().upper()
        if key not in self._by_label:
            raise KeyError(f"No cell {label!r} in this comparison. "
                           f"Cells run {self.cells[0].label} to {self.cells[-1].label}.")
        return self._by_label[key]

    @property
    def off(self) -> list[CellCompare]:
        """Every cell further than the threshold from the reference, worst first."""
        return sorted((c for c in self.cells if abs(c.delta) > self.threshold),
                      key=lambda c: -abs(c.delta))

    @property
    def unreachable(self) -> list[CellCompare]:
        """Cells asking for a value darker than any paint in the box, worst first.

        Not a failure of the painting. Chasing these spends strokes that cannot
        land, which is exactly what two rehearsals did before this existed.

        Expect it to be empty most of the time now. It was built when the palette
        floored at ``0.23`` and a lamp-lit photograph put eighteen of sixty-four
        cells below anything a stroke could reach; the masstones are darker since,
        the box bottoms out near ``0.13``, and an ordinary shadow is the painter's
        own work again. What is left here is the deepest few cells a photograph can
        hold, and a list this size is a fact about the reference, not a licence to
        stop early.
        """
        if self.floor <= 0.0:
            return []
        return [c for c in self.off if c.ref < self.floor - self.threshold]

    @property
    def fixable(self) -> list[CellCompare]:
        """The cells that are out *and* within reach, worst first. The work list."""
        out_of_reach = {id(c) for c in self.unreachable}
        return [c for c in self.off if id(c) not in out_of_reach]

    def worst(self, n: int = 6) -> list[CellCompare]:
        """The ``n`` cells furthest from the reference."""
        return sorted(self.cells, key=lambda c: -abs(c.delta))[:n]

    @property
    def max_delta(self) -> float:
        return max((abs(c.delta) for c in self.cells), default=0.0)

    def table(self) -> str:
        """The whole comparison as a grid of signed differences, plus the worst cells."""
        ncol = len(self.columns)
        head = "     " + "".join(f"{c:>7s}" for c in self.columns)
        lines = [
            f"compare: value 0..1, delta = canvas - reference, threshold {self.threshold:.2f}",
            head,
        ]
        out_of_reach = {id(c) for c in self.unreachable}
        for r, row in enumerate(self.rows):
            cells = self.cells[r * ncol:(r + 1) * ncol]
            marks = "".join(
                f"{c.delta:+7.2f}" if abs(c.delta) <= self.threshold
                else f"{c.delta:+6.2f}" + ("~" if id(c) in out_of_reach else "*")
                for c in cells
            )
            lines.append(f"{row:>4s} {marks}")

        bad, beyond = self.off, self.unreachable
        lines.append(
            f"{len(bad)} of {len(self.cells)} cells more than {self.threshold:.2f} out"
            f" (* above); largest {self.max_delta:.2f}."
        )
        if beyond:
            lines.append(
                f"{len(beyond)} of those (~) ask for a value below the palette's "
                f"{self.floor:.2f} floor and cannot be painted. "
                f"{len(self.fixable)} are worth strokes."
            )
        for c in self.fixable[:6]:
            lines.append(f"    {c}")
        if self.path is not None:
            lines.append(f"    heat map: {self.path}")
        return "\n".join(lines)

    def __str__(self) -> str:
        return self.table()


def _means(arr: np.ndarray, cols: int, rows: int) -> tuple[np.ndarray, np.ndarray]:
    """Per-cell mean value and mean sRGB colour of an 8-bit RGB array.

    The value is sRGB-encoded luminance, which is what the greyscale view shows.
    Averaging in linear light and reporting that would be a number the painter
    cannot see -- and a tool that reports a value the painter cannot see is how two
    early findings happened. The measurement can be right and the instrument still
    wrong; see ``LESSONS.md``.
    """
    h, w = arr.shape[:2]
    srgb = np.asarray(arr, dtype=np.float32) / 255.0
    value = linear_to_srgb(luminance(srgb_to_linear(srgb)))

    values = np.zeros((rows, cols), dtype=np.float32)
    colours = np.zeros((rows, cols, 3), dtype=np.float32)
    for r in range(rows):
        # y0 clamped to a real row index first, then y1 given at least one row
        # past it and clamped to the array: rounding a region a few pixels tall
        # into ten row-tenths can otherwise push y0 to or past h, which slices
        # to an empty array regardless of y1 and means() it to NaN. A NaN delta
        # compares false against any threshold, so a cell like that silently
        # dropped out of `off`/`fixable` instead of being reported.
        y0 = min(int(round(r * h / rows)), h - 1)
        y1 = min(max(int(round((r + 1) * h / rows)), y0 + 1), h)
        for c in range(cols):
            x0 = min(int(round(c * w / cols)), w - 1)
            x1 = min(max(int(round((c + 1) * w / cols)), x0 + 1), w)
            values[r, c] = float(value[y0:y1, x0:x1].mean())
            colours[r, c] = srgb[y0:y1, x0:x1].reshape(-1, 3).mean(axis=0)
    return values, colours


def _hex(rgb: np.ndarray) -> str:
    v = np.clip(rgb * 255.0 + 0.5, 0, 255).astype(int)
    return "#{:02X}{:02X}{:02X}".format(*v)


def compare_images(
    canvas_rgb: np.ndarray,
    reference_rgb: np.ndarray,
    region: Region | None = None,
    threshold: float = VALUE_THRESHOLD,
    floor: float = 0.0,
) -> Comparison:
    """Compare two 8-bit RGB arrays cell by cell.

    Both arrays must already cover the same normalised frame; they need not be the
    same pixel size. Without a region the grid is the painter's own A-H by 1-8. With
    one it is the tenths of that region, labelled the way ``look(grid="fine")``
    labels them, so a cell that is out has a name that goes straight back into
    ``region.point(u, v)``.

    ``floor`` is the darkest value the palette can reach; pass it and the result
    separates the cells that are out because the painting is wrong from the ones
    that are out because no paint in the box goes that dark.
    """
    if region is None:
        cols, rows = list(GRID_COLS), list(GRID_ROWS)
    else:
        cols = rows = [str(i) for i in range(10)]

    cv, cc = _means(canvas_rgb, len(cols), len(rows))
    rv, rc = _means(reference_rgb, len(cols), len(rows))

    cells: list[CellCompare] = []
    for r, row in enumerate(rows):
        for c, col in enumerate(cols):
            label = f"{col}{row}" if region is None else f"{col},{row}"
            cells.append(
                CellCompare(
                    label=label,
                    u=(c + 0.5) / len(cols),
                    v=(r + 0.5) / len(rows),
                    ref=float(rv[r, c]),
                    canvas=float(cv[r, c]),
                    delta=float(cv[r, c] - rv[r, c]),
                    ref_hex=_hex(rc[r, c]),
                    canvas_hex=_hex(cc[r, c]),
                    threshold=threshold,
                )
            )
    return Comparison(cells=cells, columns=cols, rows=rows, region=region,
                      threshold=threshold, floor=floor)


def heat_sheet(
    comparison: Comparison,
    canvas_grey: Image.Image,
    reference_grey: Image.Image,
    cell_px: int = 64,
) -> Image.Image:
    """Reference, canvas and the difference, as three panels the same size.

    Greyscale for the first two on purpose: the question a comparison answers is
    about value, and hue beside it is a distraction the painter does not need while
    asking it.
    """
    ncol, nrow = len(comparison.columns), len(comparison.rows)
    # The panels keep the reference's aspect and the cells follow it, rather than the
    # cells being square and the picture being squashed to fit them. A grid cell on a
    # 4:3 canvas is not square either, and a comparison that distorts the thing being
    # compared is a comparison nobody should trust.
    src_w, src_h = reference_grey.size
    w = ncol * cell_px
    h = max(nrow, int(round(w * src_h / max(src_w, 1))))
    cell_w, cell_h = w / ncol, h / nrow

    heat = np.zeros((nrow, ncol, 3), dtype=np.float32)
    for i, c in enumerate(comparison.cells):
        r, col = divmod(i, ncol)
        t = min(abs(c.delta) / max(comparison.threshold * 3.0, 1e-6), 1.0)
        target = _HEAT_WARM if c.delta > 0 else _HEAT_COOL
        heat[r, col] = _HEAT_OK * (1.0 - t) + target * t
    heat_img = Image.fromarray(np.clip(heat, 0, 255).astype(np.uint8), mode="RGB").resize(
        (w, h), Image.NEAREST
    )

    panels = [reference_grey.convert("RGB").resize((w, h), Image.LANCZOS),
              canvas_grey.convert("RGB").resize((w, h), Image.LANCZOS),
              heat_img]

    gap, top = 10, 16
    sheet = Image.new("RGB", (w * 3 + gap * 4, h + top + gap), (22, 22, 24))
    draw = ImageDraw.Draw(sheet)
    for i, (panel, name) in enumerate(zip(panels, ("reference", "canvas", "difference"),
                                          strict=True)):
        x = gap + i * (w + gap)
        sheet.paste(panel, (x, top))
        draw.text((x + 2, 3), name, fill=(225, 225, 230))

    # The numbers, on the heat panel. A colour says "here"; a number says "by how
    # much", and the painter needs both in one glance.
    hx = gap + 2 * (w + gap)
    for i, c in enumerate(comparison.cells):
        r, col = divmod(i, ncol)
        if abs(c.delta) < 0.005:
            continue
        # The sign is the whole message -- too dark or too light are opposite repairs.
        draw.text((hx + col * cell_w + 6, top + r * cell_h + cell_h // 2 - 4),
                  f"{c.delta:+.2f}", fill=(240, 240, 245))
    for i in range(1, ncol):
        draw.line([(hx + i * cell_w, top), (hx + i * cell_w, top + h)], fill=(60, 60, 66))
    for j in range(1, nrow):
        draw.line([(hx, top + j * cell_h), (hx + w, top + j * cell_h)], fill=(60, 60, 66))

    # Cell names down the side and across the top of the difference panel.
    for c, name in enumerate(comparison.columns):
        draw.text((hx + c * cell_w + cell_w // 2 - 3, top + 2), name, fill=(150, 160, 175))
    for r, name in enumerate(comparison.rows):
        draw.text((hx + 2, top + r * cell_h + 2), name, fill=(150, 160, 175))
    return sheet
