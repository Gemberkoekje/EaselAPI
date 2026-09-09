"""Composition helpers: named regions, a labelled grid, and relative placement.

This module exists because of a specific weakness. A language model reasons well
about *where things are in relation to each other* and badly about absolute
coordinates. So the painter should never be doing arithmetic on 0.63 and 0.29 --
it should be saying ``region("upper-left")``, ``cell("D6")``, ``below(horizon)``.

Every region is a normalised rectangle ``(x0, y0, x1, y1)`` with the origin at the
top-left, and every helper returns one, so they compose.
"""

from __future__ import annotations

from dataclasses import dataclass

__all__ = ["Region", "region", "cell", "thirds", "golden", "horizon", "below", "above",
           "left_of", "right_of", "between", "REGION_NAMES", "GRID_COLS", "GRID_ROWS"]

#: Columns of the ``look(grid=True)`` overlay, left to right.
GRID_COLS = "ABCDEFGH"
#: Rows of the grid overlay, top to bottom.
GRID_ROWS = "12345678"


@dataclass(frozen=True)
class Region:
    """A normalised rectangle on the canvas.

    Regions are the painter's unit of place. They can be shrunk, nudged, split and
    sampled, and any of them can be handed to ``look(region=...)`` or to a block-in.
    """

    x0: float
    y0: float
    x1: float
    y1: float
    name: str = ""

    def __post_init__(self) -> None:
        if self.x1 <= self.x0 or self.y1 <= self.y0:
            raise ValueError(
                f"Region must have positive extent, got ({self.x0}, {self.y0}, {self.x1}, {self.y1})"
            )

    # -- geometry ----------------------------------------------------------------
    @property
    def bounds(self) -> tuple[float, float, float, float]:
        return (self.x0, self.y0, self.x1, self.y1)

    @property
    def width(self) -> float:
        return self.x1 - self.x0

    @property
    def height(self) -> float:
        return self.y1 - self.y0

    @property
    def center(self) -> tuple[float, float]:
        return ((self.x0 + self.x1) * 0.5, (self.y0 + self.y1) * 0.5)

    def point(self, u: float, v: float) -> tuple[float, float]:
        """A point inside the region in its own 0..1 coordinates.

        ``point(0, 0)`` is the top-left corner, ``point(0.5, 0.5)`` the centre.
        """
        return (self.x0 + u * self.width, self.y0 + v * self.height)

    #: Smallest extent an inset or scaled region is allowed to collapse to.
    MIN_EXTENT = 0.005

    def inset(self, amount: float) -> Region:
        """Shrink by ``amount`` (a fraction of the canvas) on every side.

        Insetting further than the region is wide leaves a sliver at the centre
        rather than raising. A painter mid-painting should not get an exception for
        asking for too much margin.
        """
        a = float(amount)
        cx, cy = self.center
        half_w = max(self.width * 0.5 - a, Region.MIN_EXTENT * 0.5)
        half_h = max(self.height * 0.5 - a, Region.MIN_EXTENT * 0.5)
        return Region(_c(cx - half_w), _c(cy - half_h), _c(cx + half_w), _c(cy + half_h),
                      self.name)

    def scaled(self, factor: float) -> Region:
        """Grow or shrink about the centre. ``scaled(0.5)`` is half the size."""
        cx, cy = self.center
        hw = max(self.width * factor * 0.5, Region.MIN_EXTENT * 0.5)
        hh = max(self.height * factor * 0.5, Region.MIN_EXTENT * 0.5)
        return Region(_c(cx - hw), _c(cy - hh), _c(cx + hw), _c(cy + hh), self.name)

    def shifted(self, dx: float = 0.0, dy: float = 0.0) -> Region:
        """Move the region without changing its size."""
        return Region(_c(self.x0 + dx), _c(self.y0 + dy), _c(self.x1 + dx), _c(self.y1 + dy),
                      self.name)

    def split_h(self, n: int = 2) -> list[Region]:
        """Split into ``n`` columns, left to right."""
        w = self.width / n
        return [Region(_c(self.x0 + i * w), self.y0, _c(self.x0 + (i + 1) * w), self.y1)
                for i in range(n)]

    def split_v(self, n: int = 2) -> list[Region]:
        """Split into ``n`` rows, top to bottom."""
        h = self.height / n
        return [Region(self.x0, _c(self.y0 + i * h), self.x1, _c(self.y0 + (i + 1) * h))
                for i in range(n)]

    def __repr__(self) -> str:
        tag = f" {self.name!r}" if self.name else ""
        return f"Region({self.x0:.3f}, {self.y0:.3f}, {self.x1:.3f}, {self.y1:.3f}{tag})"


def _c(v: float) -> float:
    return float(min(max(v, 0.0), 1.0))


# --------------------------------------------------------------------------------------
# Named regions
# --------------------------------------------------------------------------------------
_THIRD = 1.0 / 3.0
_NAMED: dict[str, tuple[float, float, float, float]] = {
    "all": (0.0, 0.0, 1.0, 1.0),
    "canvas": (0.0, 0.0, 1.0, 1.0),
    # thirds
    "top-left": (0.0, 0.0, _THIRD, _THIRD),
    "top": (_THIRD, 0.0, 2 * _THIRD, _THIRD),
    "top-right": (2 * _THIRD, 0.0, 1.0, _THIRD),
    "left": (0.0, _THIRD, _THIRD, 2 * _THIRD),
    "center": (_THIRD, _THIRD, 2 * _THIRD, 2 * _THIRD),
    "right": (2 * _THIRD, _THIRD, 1.0, 2 * _THIRD),
    "bottom-left": (0.0, 2 * _THIRD, _THIRD, 1.0),
    "bottom": (_THIRD, 2 * _THIRD, 2 * _THIRD, 1.0),
    "bottom-right": (2 * _THIRD, 2 * _THIRD, 1.0, 1.0),
    # halves and bands
    "upper-half": (0.0, 0.0, 1.0, 0.5),
    "lower-half": (0.0, 0.5, 1.0, 1.0),
    "left-half": (0.0, 0.0, 0.5, 1.0),
    "right-half": (0.5, 0.0, 1.0, 1.0),
    "upper-left": (0.0, 0.0, 0.5, 0.5),
    "upper-right": (0.5, 0.0, 1.0, 0.5),
    "lower-left": (0.0, 0.5, 0.5, 1.0),
    "lower-right": (0.5, 0.5, 1.0, 1.0),
    "middle-band": (0.0, _THIRD, 1.0, 2 * _THIRD),
    # Deliberately neutral names. An engine that ships regions called "sky" and
    # "ground" is quietly suggesting what to paint, and the point of this one is
    # that the painter chooses.
    "upper-band": (0.0, 0.0, 1.0, 0.4),
    "lower-band": (0.0, 0.6, 1.0, 1.0),
    # a comfortable working area inside the edges
    "inner": (0.12, 0.12, 0.88, 0.88),
}

#: Every name :func:`region` accepts.
REGION_NAMES = tuple(sorted(_NAMED))


def region(name: str) -> Region:
    """Look up a named region.

    Accepts hyphens or underscores: ``region("top-left")`` and ``region("top_left")``
    are the same. See :data:`REGION_NAMES` for the full list.
    """
    key = str(name).strip().lower().replace("_", "-").replace(" ", "-")
    if key not in _NAMED:
        raise KeyError(
            f"Unknown region {name!r}. Available: {', '.join(REGION_NAMES)}. "
            f"You can also build one directly: Region(x0, y0, x1, y1)."
        )
    return Region(*_NAMED[key], name=key)


def cell(label: str) -> Region:
    """One cell of the ``look(grid=True)`` overlay, e.g. ``cell("D6")``.

    Columns run A-H left to right, rows 1-8 top to bottom. This is the intended way
    to turn something seen in a grid overlay into somewhere to paint.
    """
    text = str(label).strip().upper()
    if len(text) < 2 or text[0] not in GRID_COLS or text[1:] not in GRID_ROWS:
        raise ValueError(
            f"Bad cell {label!r}. Use a column {GRID_COLS[0]}-{GRID_COLS[-1]} followed by a "
            f"row {GRID_ROWS[0]}-{GRID_ROWS[-1]}, for example 'D6'."
        )
    col = GRID_COLS.index(text[0])
    row = GRID_ROWS.index(text[1:])
    cw, ch = 1.0 / len(GRID_COLS), 1.0 / len(GRID_ROWS)
    return Region(col * cw, row * ch, (col + 1) * cw, (row + 1) * ch, name=text)


def span(first: str, last: str) -> Region:
    """The rectangle covering a run of grid cells, e.g. ``span("E5", "H8")``.

    A mass seen on a gridded reference is rarely one cell -- it "fills E5 to H8" --
    and this is how to say so to :meth:`Session.block_in` or ``look(region=...)``.
    Both corner cells are included, and may be given in either order.
    """
    a, b = cell(first), cell(last)
    return Region(
        min(a.x0, b.x0), min(a.y0, b.y0), max(a.x1, b.x1), max(a.y1, b.y1),
        name=f"{a.name}:{b.name}",
    )


def thirds() -> tuple[list[float], list[float]]:
    """The rule-of-thirds lines as ``(vertical_xs, horizontal_ys)``."""
    return ([_THIRD, 2 * _THIRD], [_THIRD, 2 * _THIRD])


def golden() -> tuple[list[float], list[float]]:
    """The golden-section lines as ``(vertical_xs, horizontal_ys)``."""
    phi = 0.6180339887
    return ([1 - phi, phi], [1 - phi, phi])


def horizon(y: float = 0.4) -> Region:
    """A thin band at height ``y`` -- somewhere to sit a horizon or a table edge."""
    yy = _c(y)
    return Region(0.0, _c(yy - 0.012), 1.0, _c(yy + 0.012), name=f"horizon@{yy:.2f}")


# --------------------------------------------------------------------------------------
# Relative placement
# --------------------------------------------------------------------------------------
def below(target: Region, amount: float = 0.15) -> Region:
    """A band of height ``amount`` immediately below ``target``."""
    return Region(target.x0, _c(target.y1), target.x1, _c(target.y1 + amount))


def above(target: Region, amount: float = 0.15) -> Region:
    """A band of height ``amount`` immediately above ``target``."""
    return Region(target.x0, _c(target.y0 - amount), target.x1, _c(target.y0))


def left_of(target: Region, amount: float = 0.15) -> Region:
    """A band of width ``amount`` immediately left of ``target``."""
    return Region(_c(target.x0 - amount), target.y0, _c(target.x0), target.y1)


def right_of(target: Region, amount: float = 0.15) -> Region:
    """A band of width ``amount`` immediately right of ``target``."""
    return Region(_c(target.x1), target.y0, _c(target.x1 + amount), target.y1)


def between(a: Region, b: Region) -> Region:
    """The region spanning from the centre of ``a`` to the centre of ``b``."""
    ax, ay = a.center
    bx, by = b.center
    x0, x1 = min(ax, bx), max(ax, bx)
    y0, y1 = min(ay, by), max(ay, by)
    # Give it some body if the two centres line up on an axis.
    if x1 - x0 < 1e-3:
        x0, x1 = _c(x0 - 0.02), _c(x1 + 0.02)
    if y1 - y0 < 1e-3:
        y0, y1 = _c(y0 - 0.02), _c(y1 + 0.02)
    return Region(x0, y0, x1, y1)


def as_region(value) -> Region:
    """Coerce a name, a 4-tuple or a :class:`Region` into a :class:`Region`."""
    if isinstance(value, Region):
        return value
    if isinstance(value, str):
        return region(value)
    x0, y0, x1, y1 = (float(v) for v in value)
    return Region(x0, y0, x1, y1)
