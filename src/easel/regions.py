"""Composition helpers: named regions, a labelled grid, and relative placement.

This module exists because of a specific weakness. A language model reasons well
about *where things are in relation to each other* and badly about absolute
coordinates. So the painter should never be doing arithmetic on 0.63 and 0.29 --
it should be saying ``region("upper-left")``, ``cell("D6")``, ``below(horizon)``.

A :class:`Region` is a normalised rectangle ``(x0, y0, x1, y1)`` with the origin at
the top-left, and every helper here returns one, so they compose.

A rectangle is the shape of very little, though, and a vocabulary made only of
rectangles turns out to steer what gets painted: told what the engine was
mechanically good at, six fresh sessions in eight justified their subject by
horizontal bands in as many words. So a place can also
be a :class:`Polygon` -- a closed shape, built with :func:`polygon`, :func:`ellipse`,
:func:`blob`, :func:`hull` or :func:`ribbon` -- and a block-in fills one pass by
pass, stopping at its boundary. Anything that takes a region takes a shape.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

__all__ = ["Region", "region", "cell", "span", "thirds", "golden", "horizon", "below",
           "above", "left_of", "right_of", "between", "REGION_NAMES", "GRID_COLS",
           "GRID_ROWS", "as_region", "as_place",
           "Polygon", "polygon", "ellipse", "blob", "hull", "ribbon"]

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
        # NaN and Infinity both compare False against every ordering, so
        # `x1 <= x0` alone lets a NaN or Infinite bound straight through --
        # Polygon already guards its own points against exactly this
        # (`_clean_points`'s `math.isfinite` check); Region did not, and it
        # surfaced downstream instead as a raw, unexplained crash wherever a
        # bound was later multiplied by a canvas size and rounded to a pixel
        # index (:meth:`easel.canvas.Canvas.region_px`), or as corrupted state
        # if the NaN made it into the undo log first.
        if not all(math.isfinite(v) for v in (self.x0, self.y0, self.x1, self.y1)):
            raise ValueError(
                f"Region needs finite bounds, got ({self.x0}, {self.y0}, {self.x1}, {self.y1})"
            )
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

    @property
    def axis(self) -> float:
        """The angle its long side runs at, for ``block_in(direction="axis")``."""
        return 0.0 if self.width >= self.height else 90.0

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
    # Both checks below are single-character membership, not "in", deliberately:
    # "12" in "12345678" is True (a substring match), which let a two-digit typo
    # like "A12" silently resolve to row "1" instead of being rejected.
    if len(text) != 2 or text[0] not in GRID_COLS or text[1] not in GRID_ROWS:
        raise ValueError(
            f"Bad cell {label!r}. Use a column {GRID_COLS[0]}-{GRID_COLS[-1]} followed by a "
            f"row {GRID_ROWS[0]}-{GRID_ROWS[-1]}, for example 'D6'."
        )
    col = GRID_COLS.index(text[0])
    row = GRID_ROWS.index(text[1])
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
    """Coerce a name, a cell, a span, a 4-tuple or a :class:`Region` into a Region.

    Strings are tried as a named region, then as a grid cell, then as a span::

        as_region("upper-band")     # a named region
        as_region("D4")             # one grid cell
        as_region("C3:F6")          # a run of cells

    So anything that takes a region -- ``look``, ``block_in``, ``compare`` -- takes
    a cell label straight off a gridded look, which is where the painter read it.
    """
    if isinstance(value, Region):
        return value
    if isinstance(value, Polygon):
        # A shape crops, measures and dries as the rectangle around it wherever the
        # caller only knows about rectangles. Use :func:`as_place` to keep the shape.
        return value.box
    if isinstance(value, str):
        text = value.strip()
        if ":" in text:
            first, last = text.split(":", 1)
            return span(first.strip(), last.strip())
        key = text.lower().replace("_", "-").replace(" ", "-")
        if key in _NAMED:
            return region(key)
        try:
            return cell(text)
        except ValueError:
            pass
        raise KeyError(
            f"Unknown region {value!r}. Use a name ({', '.join(REGION_NAMES)}), "
            f"a grid cell like 'D4', a span like 'C3:F6', or Region(x0, y0, x1, y1)."
        )
    x0, y0, x1, y1 = (float(v) for v in value)
    return Region(x0, y0, x1, y1)


def as_place(value):
    """Coerce to a :class:`Polygon` if it is one, otherwise to a :class:`Region`.

    What :meth:`~easel.session.Session.block_in` uses: a shape stays a shape, and
    everything else is a rectangle, so one call fills either.
    """
    if isinstance(value, Polygon):
        return value
    return as_region(value)


# --------------------------------------------------------------------------------------
# Shaped masses
# --------------------------------------------------------------------------------------
@dataclass(frozen=True)
class Polygon:
    """A closed shape on the canvas, as normalised points: a mass with a silhouette.

    A rectangle is the shape of very little. Everything above takes one, so before
    this existed the only mass the engine filled honestly was a band -- and painters
    reasoned their way to band-shaped pictures because that was what the tool could
    carry. A shape goes anywhere a region goes:
    :meth:`~easel.session.Session.block_in` fills it pass by pass and stops at the
    boundary, ``look(region=...)`` and ``compare(region=...)`` crop to the rectangle
    around it, and :meth:`~easel.session.Session.dry` and
    :meth:`~easel.session.Session.erase` act inside the shape itself.

    Build one with :func:`polygon`, :func:`ellipse`, :func:`blob`, :func:`hull` or
    :func:`ribbon` rather than by typing coordinates: naming a place you can see and
    letting the helper do the arithmetic is the whole point of this module.

    The points are the outline in order, open (the last does not repeat the first).
    ``traced`` marks a shape that came from the *reference* rather than from the
    painter -- see :meth:`~easel.session.Session.ref_shape`.
    """

    points: tuple[tuple[float, float], ...]
    name: str = ""
    traced: bool = False

    def __post_init__(self) -> None:
        pts = _clean_points(self.points)
        if len(pts) < 3:
            raise ValueError(
                f"A shape needs at least three distinct points, got {len(pts)}. "
                f"Two points are a line: paint it with s.stroke(), or give it a "
                f"width with ribbon(points, width)."
            )
        if abs(_signed_area(pts)) < 1e-7:
            raise ValueError(
                "A shape needs some area, and these points are on one line. "
                "ribbon(points, width) turns a line into a mass."
            )
        object.__setattr__(self, "points", pts)
        object.__setattr__(self, "name", str(self.name))
        object.__setattr__(self, "traced", bool(self.traced))

    # -- geometry ----------------------------------------------------------------
    @property
    def bounds(self) -> tuple[float, float, float, float]:
        """The rectangle around the shape, so anything taking a region takes this."""
        xs = [p[0] for p in self.points]
        ys = [p[1] for p in self.points]
        return (min(xs), min(ys), max(xs), max(ys))

    @property
    def box(self) -> Region:
        """The bounding :class:`Region`. What ``look(region=shape)`` crops to."""
        return Region(*self.bounds, name=self.name)

    @property
    def width(self) -> float:
        x0, _, x1, _ = self.bounds
        return x1 - x0

    @property
    def height(self) -> float:
        _, y0, _, y1 = self.bounds
        return y1 - y0

    @property
    def area(self) -> float:
        """Share of the canvas the shape covers, 0..1."""
        return abs(_signed_area(self.points))

    @property
    def center(self) -> tuple[float, float]:
        """The centroid -- the balance point of the shape, not of its box."""
        return _centroid(self.points)

    @property
    def axis(self) -> float:
        """The angle the shape runs at, in degrees, for ``block_in(direction="axis")``.

        The long axis of the outline, weighted by edge length, so a mass gets swept
        along its own direction instead of along the canvas's.
        """
        return _principal_axis(self.points)

    @property
    def closed(self) -> list[tuple[float, float]]:
        """The outline with the first point repeated: a path that comes back round.

        This is what to hand :meth:`~easel.session.Session.pencil` to draw the
        silhouette, or :meth:`~easel.session.Session.preview` to look at it.
        """
        return [*self.points, self.points[0]]

    def point(self, u: float, v: float) -> tuple[float, float]:
        """A point in the shape's bounding box, in its own 0..1 coordinates.

        The same reading as :meth:`Region.point`, so a place inside a shape is named
        the way a place inside a region is. It is the *box* that is divided, so a
        point can land outside a concave shape -- :meth:`contains` says whether it did.
        """
        return self.box.point(u, v)

    def contains(self, x: float, y: float) -> bool:
        """Is this point inside the shape?"""
        return bool(self.inside(np.array([float(x)]), np.array([float(y)]))[0])

    def inside(self, xs, ys) -> np.ndarray:
        """Which of these points are inside the shape. Even-odd, vectorised."""
        x = np.asarray(xs, dtype=np.float64)
        y = np.asarray(ys, dtype=np.float64)
        result = np.zeros(np.broadcast(x, y).shape, dtype=bool)
        pts = self.points
        for (ax, ay), (bx, by) in zip(pts, [*pts[1:], pts[0]], strict=True):
            if ay == by:
                continue                      # horizontal edge: no crossing to count
            crosses = (ay > y) != (by > y)
            cut = (bx - ax) * (y - ay) / (by - ay) + ax
            result ^= crosses & (x < cut)
        return result

    def mask(self, width: int, height: int) -> np.ndarray:
        """A boolean mask of the shape at a pixel size, for the canvas to act on."""
        w, h = int(width), int(height)
        out = np.zeros((h, w), dtype=bool)
        x0, y0, x1, y1 = self.bounds
        cx0 = max(0, int(np.floor(x0 * w)))
        cy0 = max(0, int(np.floor(y0 * h)))
        cx1 = min(w, int(np.ceil(x1 * w)) + 1)
        cy1 = min(h, int(np.ceil(y1 * h)) + 1)
        if cx1 <= cx0 or cy1 <= cy0:
            return out
        xs = (np.arange(cx0, cx1, dtype=np.float64) + 0.5) / w
        ys = (np.arange(cy0, cy1, dtype=np.float64) + 0.5) / h
        out[cy0:cy1, cx0:cx1] = self.inside(xs[None, :], ys[:, None])
        return out

    # -- reshaping ---------------------------------------------------------------
    def inset(self, amount: float) -> Polygon:
        """Shrink the silhouette by ``amount`` all the way round; negative grows it.

        The same move as :meth:`Region.inset`, and wanted for the same reason: two
        masses that meet at the same depth want the near one held back off the seam
        by half a brush. A shape shrunk past its own width collapses to a sliver at
        the centre rather than raising -- a painter mid-painting should not get an
        exception for asking for too much margin.

        Every *edge* moves in by ``amount``; a *tip* moves further, because that is
        where a brush of that reach has to stop. On a lobed or spiky outline the
        lobes therefore retreat by up to about three times what was asked, and the
        bounding box shrinks with them: ``inset(0.045)`` on a five-pointed star
        takes 0.24 off its width, not 0.09. That is the offset doing its job -- it
        is what keeps a brush half its width inside the silhouette -- and it is not
        the same move as :meth:`scaled`, which is the one to reach for when what is
        wanted is a smaller mass rather than a margin.
        """
        a = float(amount)
        if abs(a) < 1e-9:
            return self
        pts = np.asarray(self.points, dtype=np.float64)
        smaller = a > 0
        best: Polygon | None = None
        # Which way along the bisectors is *in* depends on the winding, so offset
        # both ways and keep whichever moved the area the way the caller asked.
        for cand in (_offset_ring(pts, a), _offset_ring(pts, -a)):
            made = _try_polygon(cand, self.name, self.traced)
            if made is None or (made.area < self.area) != smaller:
                continue
            if best is None or (made.area < best.area) == smaller:
                best = made
        # A mitre join on a spiky or very thin outline can fold the shape through
        # itself; a fold shows up as a shape that lost most of its area, or as
        # points that came out the wrong side of the outline they were offset
        # from. Growing needs the same check mirrored, because growing a spiky
        # concave outline can fold it just as easily -- the reflex vertices are
        # exactly where a mitre offset overshoots.
        #
        # The test is containment of the *points*, not of the centre. A concave
        # shape need not contain its own centroid -- a C or a horseshoe does not,
        # and neither does a deeply lobed blob -- so testing the centre threw the
        # offset away on exactly the shapes an offset is hardest on, and fell back
        # to a scale about a centroid that is nowhere near the middle of the mass.
        # That returned an inset shape with half its points *outside* the shape it
        # had been asked to shrink.
        if best is not None:
            mine = np.asarray(self.points, dtype=np.float64)
            theirs = np.asarray(best.points, dtype=np.float64)
            if smaller:
                sane = (best.area >= 0.05 * self.area
                        and bool(self.inside(theirs[:, 0], theirs[:, 1]).all()))
            else:
                sane = (best.area >= 0.95 * self.area
                        and bool(best.inside(mine[:, 0], mine[:, 1]).all()))
            if sane:
                return best
        # The offset ate the shape (a thin or spiky outline will do that). Fall back
        # to pulling every point toward the centre by the same amount.
        return self._toward_centre(a)

    def smooth(self, iterations: int = 2) -> Polygon:
        """A rounder version of this outline: the corners cut, the silhouette kept.

        A polygon drawn through a dozen points has a dozen corners, and a round tip
        laid along it leaves a scalloped edge that reads as faceting rather than as
        form. This cuts the corners off -- Chaikin's corner cutting, run on the
        closed ring -- so a shape built from a few named points can still have a
        silhouette a brush can follow::

            pear = union(circle_top, circle_body).smooth()

        Each pass replaces every corner with two points a quarter of the way along
        each of its edges, so the outline doubles in length per iteration and pulls
        very slightly inside the original -- a corner is cut, not rounded outward.
        Two passes is usually enough; beyond about four a shape starts heading for
        its own ellipse.

        Args:
            iterations: how many passes of corner cutting. ``0`` returns the shape
                unchanged.

        Returns:
            A new :class:`Polygon`. The name and the traced mark carry over.
        """
        pts = np.asarray(self.points, dtype=np.float64)
        for _ in range(max(0, int(iterations))):
            nxt = np.roll(pts, -1, axis=0)
            out = np.empty((len(pts) * 2, 2), dtype=np.float64)
            out[0::2] = pts * 0.75 + nxt * 0.25
            out[1::2] = pts * 0.25 + nxt * 0.75
            pts = out
        return Polygon(tuple((float(x), float(y)) for x, y in pts),
                       name=self.name, traced=self.traced)

    def scaled(self, factor: float) -> Polygon:
        """Grow or shrink about the centroid. ``scaled(0.5)`` is half the size."""
        f = max(float(factor), 1e-4)
        cx, cy = self.center
        pts = [(cx + (x - cx) * f, cy + (y - cy) * f) for x, y in self.points]
        made = _try_polygon(np.asarray(pts, dtype=np.float64), self.name, self.traced)
        return made if made is not None else self._sliver()

    def shifted(self, dx: float = 0.0, dy: float = 0.0) -> Polygon:
        """Move the shape without changing it."""
        pts = [(x + float(dx), y + float(dy)) for x, y in self.points]
        made = _try_polygon(np.asarray(pts, dtype=np.float64), self.name, self.traced)
        return made if made is not None else self._sliver()

    def renamed(self, name: str) -> Polygon:
        """The same shape under another name. Names show up in the log."""
        return Polygon(self.points, name=str(name), traced=self.traced)

    def _toward_centre(self, amount: float) -> Polygon:
        cx, cy = self.center
        radii = [math.hypot(x - cx, y - cy) for x, y in self.points]
        mean_r = sum(radii) / len(radii)
        f = 1.0 - amount / mean_r if mean_r > 1e-9 else 0.0
        if f <= 1e-3:
            return self._sliver()
        return self.scaled(f)

    def _sliver(self) -> Polygon:
        cx, cy = self.center
        d = Region.MIN_EXTENT * 0.5
        return Polygon(((cx - d, cy - d), (cx + d, cy - d), (cx + d, cy + d),
                        (cx - d, cy + d)), name=self.name, traced=self.traced)

    def __repr__(self) -> str:
        x0, y0, x1, y1 = self.bounds
        tag = f" {self.name!r}" if self.name else ""
        traced = " traced" if self.traced else ""
        return (f"Polygon({len(self.points)} points, "
                f"{x0:.3f}, {y0:.3f}, {x1:.3f}, {y1:.3f}{tag}{traced})")


# -- building shapes ---------------------------------------------------------------
def polygon(points, name: str = "") -> Polygon:
    """A shape from an outline you already have: a list of normalised points.

    Landmarks are the natural source -- the corners of a mass are exactly what
    :meth:`~easel.session.Session.mark` is for::

        s.polygon([s.pt("top"), s.pt("right"), s.pt("foot"), s.pt("left")])

    A region, or the name of one, becomes its own four corners, which is how a
    rectangle gets treated as one shape among others.
    """
    if isinstance(points, Polygon):
        return points if not name else points.renamed(name)
    if isinstance(points, (Region, str)) or _looks_like_bounds(points):
        r = as_region(points)
        return Polygon(((r.x0, r.y0), (r.x1, r.y0), (r.x1, r.y1), (r.x0, r.y1)),
                       name=name or r.name)
    return Polygon(tuple((float(x), float(y)) for x, y in points), name=name)


def ellipse(place, rx: float | None = None, ry: float | None = None,
            rotate: float = 0.0, steps: int = 48, name: str = "",
            aspect: float | None = None) -> Polygon:
    """A round mass. Give it a centre and two radii, or a place to sit inside.

    ``ellipse(cell("D5"))`` fills that cell; ``ellipse((0.4, 0.6), 0.2, 0.12, 30)``
    is an ellipse a fifth of the canvas wide, tilted thirty degrees.

    Args:
        place: a point ``(x, y)``, or any region -- the ellipse is inscribed in it.
        rx, ry: radii. One on its own sets both, so a single radius is a circle on
            a square canvas wherever the shape is placed; give neither and they
            default to half the place's width and height.
        rotate: degrees, clockwise.
        steps: how many points the outline gets.
        name: shows up in the log.
        aspect: the canvas's width over its height. Given, one radius is a shape
            that is actually **round in pixels** rather than round in coordinates --
            on a 4:3 canvas those are not the same thing, and ``rx == ry`` is an
            oval. :meth:`~easel.session.Session.circle` passes this for you.
    """
    cx, cy, dx, dy = _centre_and_radii(place, rx, ry, aspect)
    theta = np.linspace(0.0, 2.0 * np.pi, max(8, int(steps)), endpoint=False)
    return _ring(cx, cy, dx, dy, np.ones_like(theta), theta, rotate,
                 name or _place_name(place))


def blob(place, radius: float | None = None, ry: float | None = None,
         wobble: float = 0.22, points: int = 15, seed: int = 0,
         rotate: float = 0.0, name: str = "", aspect: float | None = None) -> Polygon:
    """An irregular closed shape -- a mass with a silhouette nobody drew by hand.

    The same arguments as :func:`ellipse` plus ``wobble`` (how far the outline
    wanders from the ellipse, as a fraction of its radius) and ``seed``. One radius
    is round and two are oval, the same on a point as inside a region; leave both
    out and the blob fills the place it was given. The seed is the shape's own, not
    the session's: the same seed is the same silhouette, so a blob you liked comes
    back.

    Reach for this when a mass wants a shape and the shape is nobody's business but
    the painting's -- and then *look* at it, with ``s.preview(shape)``, before
    spending twenty passes filling it.

    ``aspect`` is the canvas's width over its height, as on :func:`ellipse`: given,
    one radius is round in pixels rather than round in coordinates.
    ``s.blob(...)`` passes it for you.
    """
    cx, cy, dx, dy = _centre_and_radii(place, radius, ry, aspect)
    n = max(6, int(points))
    theta = np.linspace(0.0, 2.0 * np.pi, n, endpoint=False)
    rng = np.random.default_rng(int(seed))
    ks = np.array([2.0, 3.0, 5.0])
    amps = rng.uniform(0.5, 1.0, 3) * np.array([0.55, 0.30, 0.15])
    amps *= float(wobble) / max(float(amps.sum()), 1e-9)
    phases = rng.uniform(0.0, 2.0 * np.pi, 3)
    radii = 1.0 + sum(a * np.sin(k * theta + p) for a, k, p in zip(amps, ks, phases,
                                                                  strict=True))
    return _ring(cx, cy, dx, dy, np.clip(radii, 0.15, 2.0), theta, rotate,
                 name or _place_name(place))


def hull(places, name: str = "") -> Polygon:
    """The smallest shape containing everything given: points, shapes or regions.

    Three or four landmarks are a mass::

        s.block_in(hull([s.pt("top"), s.pt("right"), s.pt("foot")]), "bristle", "dark")

    Mixed input is allowed, so ``hull([shape_a, shape_b])`` is the mass covering
    both -- which is how two shapes get joined without any boolean geometry.
    """
    pts: list[tuple[float, float]] = []
    for item in places:
        if isinstance(item, Polygon):
            pts.extend(item.points)
        elif isinstance(item, (Region, str)):
            r = as_region(item)
            pts.extend([(r.x0, r.y0), (r.x1, r.y0), (r.x1, r.y1), (r.x0, r.y1)])
        else:
            x, y = item
            pts.append((float(x), float(y)))
    if len(pts) < 3:
        raise ValueError(
            f"A hull needs at least three points, got {len(pts)}. Mark the corners "
            f"of the mass first: s.mark('top', ...), then hull([s.pt('top'), ...])."
        )
    return Polygon(tuple(_convex_hull(pts)), name=name)


def union(*shapes, resolution: int = 1024, name: str = "") -> Polygon:
    """One shape round the outside of several overlapping ones.

    :func:`hull` covers everything given but only convexly: two circles become a
    lozenge, and the waist between them -- which is the whole reason for drawing two
    circles -- is filled in. This keeps the waist::

        pear = union(circle(top, 0.06), circle(body, 0.09)).smooth()

    The shapes must overlap or touch, because what comes back is one silhouette. Two
    masses that do not meet are two masses: block them in separately, or use
    :func:`hull` if the thing you meant was the area covering both.

    Holes are not kept. A painter blocking in a mass paints its silhouette, which is
    what ``block_in`` and ``sweep`` both take; a shape with a hole in it is two
    decisions, and the second one is a mass of its own in the colour behind.

    Args:
        *shapes: two or more shapes, regions, region names or 4-tuples. A single
            sequence of them is accepted too.
        resolution: the grid the outline is traced on. The default resolves a
            feature about a thousandth of the canvas; raise it for a silhouette with
            very fine detail, at the cost of a slower trace.
        name: shows up in the log.

    Returns:
        A :class:`Polygon` outlining the lot.
    """
    if len(shapes) == 1 and not isinstance(shapes[0], (Polygon, Region, str)) \
            and not _looks_like_bounds(shapes[0]):
        shapes = tuple(shapes[0])
    polys = [polygon(item) for item in shapes]
    if len(polys) < 2:
        raise ValueError(
            f"union() needs at least two shapes, got {len(polys)}. One shape is "
            f"already its own union."
        )

    n = max(64, int(resolution))
    mask = np.zeros((n, n), dtype=bool)
    for poly in polys:
        mask |= poly.mask(n, n)
    if not mask.any():
        raise ValueError(
            "union() was given shapes that cover no pixels at this resolution. "
            "Raise resolution=, or check the shapes are on the canvas at all."
        )

    biggest = _largest_component(mask)
    if int(biggest.sum()) < int(mask.sum()):
        raise ValueError(
            "union() was given shapes that do not all touch, so there is no single "
            "silhouette round them. Block the separate masses in one at a time, or "
            "use hull(...) for the one area that covers them all."
        )

    points = _trace_outline(mask)
    if len(points) < 3:
        raise ValueError(
            "union() could not trace an outline round these shapes -- the result is "
            "thinner than the grid it was traced on. Raise resolution=."
        )
    return Polygon(tuple(points), name=name or "+".join(p.name for p in polys if p.name))


def ribbon(places, width: float, end_width: float | None = None,
           smooth: bool = True, name: str = "") -> Polygon:
    """A mass of the given width running along a path: a shape that is not a box.

    ``ribbon([(0.2, 0.8), (0.45, 0.5), (0.8, 0.42)], 0.18)`` is a band a fifth of
    the canvas wide that follows those three points and bends where they bend. Pass
    ``end_width`` for one that narrows along its length.

    Args:
        places: the centre line, as points or landmarks. Two or more.
        width: how wide the mass is across the line, at its start.
        end_width: width at the far end. Defaults to ``width``.
        smooth: curve the centre line the way :meth:`~easel.session.Session.stroke`
            curves a path, so the silhouette bends instead of turning corners.
        name: shows up in the log.
    """
    pts = np.asarray([(float(x), float(y)) for x, y in places], dtype=np.float64)
    if len(pts) < 2:
        raise ValueError("A ribbon needs at least two points to run along.")
    if smooth and len(pts) > 2:
        # Lazily imported: the smoothing a stroke gets, so a ribbon's silhouette and
        # a stroke along the same points bend the same way.
        from easel.stroke import catmull_rom
        pts = np.asarray(catmull_rom(pts.astype(np.float32), 8), dtype=np.float64)
    w0 = abs(float(width)) * 0.5
    w1 = w0 if end_width is None else abs(float(end_width)) * 0.5
    if max(w0, w1) < 1e-6:
        raise ValueError("A ribbon needs a width.")

    d = np.gradient(pts, axis=0)
    length = np.hypot(d[:, 0], d[:, 1])
    length[length < 1e-12] = 1.0
    normals = np.stack([-d[:, 1] / length, d[:, 0] / length], axis=1)
    t = np.linspace(0.0, 1.0, len(pts))[:, None]
    half = w0 + (w1 - w0) * t
    left = pts + normals * half
    right = pts - normals * half
    return Polygon(tuple((float(x), float(y))
                         for x, y in np.vstack([left, right[::-1]])), name=name)


# -- shape internals ---------------------------------------------------------------
def _clean_points(points) -> tuple[tuple[float, float], ...]:
    """Normalised, finite, on the canvas, with no repeated neighbours."""
    out: list[tuple[float, float]] = []
    for pair in points:
        x, y = (float(v) for v in pair)
        if not (math.isfinite(x) and math.isfinite(y)):
            raise ValueError(f"A shape needs real points, got ({x!r}, {y!r}).")
        p = (_c(x), _c(y))
        if out and abs(p[0] - out[-1][0]) < 1e-9 and abs(p[1] - out[-1][1]) < 1e-9:
            continue
        out.append(p)
    while len(out) > 1 and abs(out[0][0] - out[-1][0]) < 1e-9 \
            and abs(out[0][1] - out[-1][1]) < 1e-9:
        out.pop()                              # an outline given closed, or clamped shut
    return tuple(out)


def _signed_area(points) -> float:
    total = 0.0
    for (ax, ay), (bx, by) in zip(points, [*points[1:], points[0]], strict=True):
        total += ax * by - bx * ay
    return total * 0.5


def _centroid(points) -> tuple[float, float]:
    a = _signed_area(points)
    if abs(a) < 1e-12:                         # degenerate: fall back to the mean
        return (sum(p[0] for p in points) / len(points),
                sum(p[1] for p in points) / len(points))
    cx = cy = 0.0
    for (ax, ay), (bx, by) in zip(points, [*points[1:], points[0]], strict=True):
        cross = ax * by - bx * ay
        cx += (ax + bx) * cross
        cy += (ay + by) * cross
    return (cx / (6.0 * a), cy / (6.0 * a))


def _principal_axis(points) -> float:
    """The long axis of an outline, in degrees clockwise from the horizontal.

    Each point is weighted by half the length of the two edges meeting at it, so a
    long straight side counts for its length and a cluster of points on a corner
    does not outvote it.
    """
    pts = np.asarray(points, dtype=np.float64)
    nxt = np.roll(pts, -1, axis=0)
    prv = np.roll(pts, 1, axis=0)
    w = 0.5 * (np.hypot(*(nxt - pts).T) + np.hypot(*(pts - prv).T))
    total = float(w.sum())
    if total < 1e-12:                          # pragma: no cover - degenerate
        return 0.0
    cx, cy = float((pts[:, 0] * w).sum() / total), float((pts[:, 1] * w).sum() / total)
    dx, dy = pts[:, 0] - cx, pts[:, 1] - cy
    sxx = float((w * dx * dx).sum())
    syy = float((w * dy * dy).sum())
    sxy = float((w * dx * dy).sum())
    if abs(sxy) < 1e-15 and abs(sxx - syy) < 1e-15:
        return 0.0
    return float(np.degrees(0.5 * np.arctan2(2.0 * sxy, sxx - syy)))


def _offset_ring(pts: np.ndarray, distance: float) -> np.ndarray:
    """Every vertex moved ``distance`` along the bisector of its two edges.

    A mitre join, clamped: at a sharp corner the exact mitre runs away to infinity,
    and a corner three times the offset out is close enough for paint.
    """
    prv = np.roll(pts, 1, axis=0)
    nxt = np.roll(pts, -1, axis=0)
    n1 = _unit_normals(pts - prv)
    n2 = _unit_normals(nxt - pts)
    bis = n1 + n2
    norm = np.hypot(bis[:, 0], bis[:, 1])[:, None]
    norm[norm < 1e-9] = 1.0
    bis = bis / norm
    cos_half = np.clip((bis * n1).sum(axis=1), 0.34, 1.0)[:, None]
    return pts + bis * (distance / cos_half)


def _unit_normals(edges: np.ndarray) -> np.ndarray:
    length = np.hypot(edges[:, 0], edges[:, 1])
    length[length < 1e-12] = 1.0
    return np.stack([-edges[:, 1] / length, edges[:, 0] / length], axis=1)


def _try_polygon(pts: np.ndarray, name: str, traced: bool) -> Polygon | None:
    """A polygon from these points, or ``None`` if they no longer make one."""
    try:
        return Polygon(tuple((float(x), float(y)) for x, y in pts), name=name,
                       traced=traced)
    except ValueError:
        return None


def _centre_and_radii(place, rx, ry, aspect=None) -> tuple[float, float, float, float]:
    """A centre and two radii from either a point or a region.

    One radius is a circle and two are an ellipse, wherever the shape is put; give
    neither and it takes the place's own half-extents. The region branch used to let
    ``ry`` fall back to the region's half-height instead of to ``rx``, so
    ``blob(cell("D5"), 0.26)`` came back a sausage nearly five times wider than it
    was tall while the same radius on a point gave a circle.

    ``aspect`` is the canvas's width over its height, and it is what makes "one
    radius is a circle" true on a canvas that is not square. Coordinates are
    normalised on both axes, so ``0.1`` across is 102 pixels on a 1024-wide canvas
    and ``0.1`` down is 77 on a 768-high one: equal radii are an oval. Given the
    aspect, a radius meant for x is scaled by it on the way into y. A radius the
    caller gave explicitly is never scaled -- two radii are an ellipse on purpose.
    """
    if _looks_like_point(place):
        cx, cy = (float(place[0]), float(place[1]))
        dx = dy = 0.15
        if aspect is not None:
            dy = dx * float(aspect)
    else:
        r = as_region(place)
        cx, cy = r.center
        dx, dy = r.width * 0.5, r.height * 0.5
        if aspect is not None:
            # The biggest round shape that still fits the place, rather than the
            # oval that fills it.
            dx = min(dx, dy / max(float(aspect), 1e-9))
            dy = dx * float(aspect)
    if rx is not None or ry is not None:
        dx = abs(float(rx if rx is not None else ry))
        if ry is not None:
            dy = abs(float(ry))
        else:
            dy = dx * (1.0 if aspect is None else float(aspect))
    return cx, cy, max(dx, 1e-4), max(dy, 1e-4)


def _ring(cx, cy, rx, ry, radii, theta, rotate, name) -> Polygon:
    """Points on a rotated ellipse, each pushed out by its own radius multiplier."""
    ux, uy = np.cos(theta) * radii * rx, np.sin(theta) * radii * ry
    a = math.radians(float(rotate))
    ca, sa = math.cos(a), math.sin(a)
    xs, ys = cx + ux * ca - uy * sa, cy + ux * sa + uy * ca
    return Polygon(tuple((float(x), float(y)) for x, y in zip(xs, ys, strict=True)),
                   name=name)


def _convex_hull(points) -> list[tuple[float, float]]:
    """Andrew's monotone chain. Returns the hull in order."""
    pts = sorted(set((float(x), float(y)) for x, y in points))
    if len(pts) < 3:
        return pts

    def half(seq):
        out: list[tuple[float, float]] = []
        for p in seq:
            while len(out) >= 2 and _cross(out[-2], out[-1], p) <= 0:
                out.pop()
            out.append(p)
        return out[:-1]

    return half(pts) + half(reversed(pts))


def _cross(o, a, b) -> float:
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def _looks_like_point(value) -> bool:
    return (isinstance(value, (tuple, list, np.ndarray)) and len(value) == 2
            and all(isinstance(v, (int, float, np.floating, np.integer)) for v in value))


def _looks_like_bounds(value) -> bool:
    return (isinstance(value, (tuple, list, np.ndarray)) and len(value) == 4
            and all(isinstance(v, (int, float, np.floating, np.integer)) for v in value))


def _place_name(place) -> str:
    if isinstance(place, (Region, Polygon)):
        return place.name
    if isinstance(place, str):
        return as_region(place).name
    return ""


_MOORE = ((-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1))


def _largest_component(mask: np.ndarray) -> np.ndarray:
    """The mask's largest 8-connected run of ``True`` pixels, alone.

    An area fresh out of :func:`prepare_reference` is always one connected run,
    but :meth:`Preparation.merge` can join two that do not touch at all (its own
    docstring's example is one thing cut in two by another), and :meth:`Preparation.split`
    partitions by colour with no regard for where the pieces sit. A Moore-neighbour
    trace only ever follows one run's boundary, so it needs to be handed the one
    the caller means -- the biggest -- rather than whichever run happens to
    contain the mask's topmost-then-leftmost pixel.
    """
    h, w = mask.shape
    visited = np.zeros_like(mask, dtype=bool)
    best: list[tuple[int, int]] = []
    ys_all, xs_all = np.nonzero(mask)
    for sy, sx in zip(ys_all.tolist(), xs_all.tolist(), strict=True):
        if visited[sy, sx]:
            continue
        stack = [(sy, sx)]
        visited[sy, sx] = True
        component = [(sy, sx)]
        while stack:
            y, x = stack.pop()
            for dy, dx in _MOORE:
                ny, nx = y + dy, x + dx
                if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not visited[ny, nx]:
                    visited[ny, nx] = True
                    stack.append((ny, nx))
                    component.append((ny, nx))
        if len(component) > len(best):
            best = component

    out = np.zeros_like(mask)
    if best:
        rows, cols = zip(*best, strict=True)
        out[rows, cols] = True
    return out


def _trace_outline(mask: np.ndarray, tolerance: float = 0.9) -> list[tuple[float, float]]:
    """The area's boundary as normalised points, by Moore-neighbour tracing.

    Only the outer boundary of the largest run: an area with holes in it is still
    one shape to draw, and a painter drawing a mass draws its silhouette.
    """
    h, w = mask.shape
    if not np.any(mask):
        return []
    mask = _largest_component(mask)
    ys, xs = np.nonzero(mask)

    # Start at the topmost-leftmost pixel: the boundary is guaranteed to pass through
    # it, and its left neighbour is guaranteed to be outside.
    start_y = int(ys.min())
    start_x = int(xs[ys == start_y].min())

    def inside(y: int, x: int) -> bool:
        return 0 <= y < h and 0 <= x < w and bool(mask[y, x])

    contour = [(start_y, start_x)]
    cy, cx = start_y, start_x
    back = 6                                   # came from the left
    for _ in range(8 * mask.size):
        found = False
        for step in range(1, 9):
            d = (back + step) % 8
            ny, nx = cy + _MOORE[d][0], cx + _MOORE[d][1]
            if inside(ny, nx):
                back = (d + 5) % 8             # the direction we arrived from
                cy, cx = ny, nx
                contour.append((cy, cx))
                found = True
                break
        if not found or (cy, cx) == (start_y, start_x) and len(contour) > 2:
            break

    pts = [(x / w, y / h) for y, x in contour]
    return _simplify(pts, tolerance / max(w, h))


def _simplify(points: list[tuple[float, float]], epsilon: float) -> list[tuple[float, float]]:
    """Douglas-Peucker. A traced boundary is one point per pixel; a drawing is not."""
    if len(points) < 3:
        return points
    pts = np.asarray(points, dtype=np.float64)
    keep = np.zeros(len(pts), dtype=bool)
    keep[0] = keep[-1] = True
    stack = [(0, len(pts) - 1)]
    while stack:
        i, j = stack.pop()
        if j <= i + 1:
            continue
        a, b = pts[i], pts[j]
        ab = b - a
        length = float(np.hypot(*ab))
        seg = pts[i + 1:j]
        if length < 1e-12:
            dist = np.hypot(*(seg - a).T)
        else:
            # The 2-D cross product, written out: numpy 2 dropped it from np.cross.
            rel = seg - a
            dist = np.abs(ab[0] * rel[:, 1] - ab[1] * rel[:, 0]) / length
        k = int(dist.argmax())
        if float(dist[k]) > epsilon:
            keep[i + 1 + k] = True
            stack.append((i, i + 1 + k))
            stack.append((i + 1 + k, j))
    return [(float(x), float(y)) for x, y in pts[keep]]
