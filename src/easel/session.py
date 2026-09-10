"""The painting session: the one object a painter holds.

A session ties together a canvas, a palette, a seed and a history. Everything the
painter does goes through it, so every mark is logged and the whole painting stays
reproducible from the seed.

The session owns the random generator. That is what makes the determinism promise
real: the same script with the same seed produces the same PNG, because every
jittered dab in every stroke is drawn from this one stream in the same order.
"""

from __future__ import annotations

import json
import math
import os
import tempfile
import zipfile
from dataclasses import asdict
from dataclasses import fields as dataclass_fields
from pathlib import Path

import numpy as np
from PIL import Image

from easel.brush import Brush
from easel.brush import brush as get_brush
from easel.canvas import Canvas, build_surface, tooth_ceiling
from easel.color import parse_color
from easel.history import History, StrokeRecord
from easel.look import DEFAULT_LOOK_SIZE, load_reference, render_look, save_look
from easel.measure import Comparison, compare_images, heat_sheet
from easel.palette import Palette
from easel.prepare import Preparation, prepare_reference
from easel.regions import Polygon, Region, as_place, as_region
from easel.stroke import catmull_rom, draw_pencil, paint_stroke, press_width

__all__ = ["Session"]

#: Bumped to 2 by M6: sessions now carry a graphite channel and named landmarks.
#: Bumped to 3 by M8: and a note of which assisted modes the painting has used.
#: Format 1 and 2 files still load -- they simply have less in them.
_EASEL_FORMAT = 3
_READABLE_FORMATS = (1, 2, 3)


class Session:
    """A painting in progress.

    Args:
        width: canvas width in pixels.
        height: canvas height in pixels.
        texture: ``"smooth"``, ``"linen"`` or ``"rough"``.
        ground: a named ground, a hex colour, or an (r, g, b) tuple.
        seed: the determinism seed. The same seed and the same calls give the same
            painting, down to the pixel.
        timelapse: record a frame after every mark. Cheap, and the human watching
            gets to see the painting happen.
        out_dir: where ``look()`` writes its PNGs.

    Example::

        s = Session(1024, 768, texture="linen", ground="toned_grey", seed=7)
        s.stroke([(0.1, 0.6), (0.5, 0.55), (0.9, 0.62)], "bristle", "burnt_umber")
        s.look(grid=True)
        s.export("painting.png")
    """

    def __init__(
        self,
        width: int = 1024,
        height: int = 768,
        texture: str = "linen",
        ground: str = "white",
        seed: int = 0,
        timelapse: bool = True,
        out_dir: str | Path = "out",
        texture_strength: float = 1.0,
    ) -> None:
        self.seed = int(seed)
        self.rng = np.random.default_rng(self.seed)
        self.canvas = Canvas(width, height, texture, ground, seed, texture_strength)
        self.palette = Palette()
        self.history = History()
        self.out_dir = Path(out_dir)
        self.timelapse = bool(timelapse)
        self._look_counter = 0
        self._last_look: np.ndarray | None = None
        #: Named landmarks: ``{name: (x, y)}``. Six or seven verified points are a
        #: drawing, and the masses get hung on them. See :meth:`mark`.
        self.marks: dict[str, tuple[float, float]] = {}
        self._preparation: Preparation | None = None
        #: Assisted modes this painting has used: a machine-laid sketch, or a mass
        #: blocked in on an outline traced from the reference. The brief reserves
        #: the traced-copy question for the human, and a run that answers it one way
        #: has to say so -- so the painting keeps the record instead of the write-up
        #: having to remember. See :meth:`ref_shape` and :meth:`sketch`.
        self.assisted: list[str] = []
        # Where this session's per-stroke seeds start. Zero for a real painting; a
        # rehearsal continues from the real session's count, so what is tried on the
        # scrap of canvas is the mark that lands when it is painted for real.
        self._index_base = 0
        if self.timelapse:
            self.history.add_frame(self.canvas.thumbnail_srgb8())

    # -- properties -------------------------------------------------------------
    @property
    def stroke_count(self) -> int:
        """How many marks have been made so far."""
        return self.history.stroke_count

    @property
    def size(self) -> tuple[int, int]:
        return (self.canvas.width, self.canvas.height)

    # -- painting ---------------------------------------------------------------
    def stroke(
        self,
        points,
        brush: str | Brush = "bristle",
        color="burnt_umber",
        pressure="taper",
        size: float | None = None,
        opacity: float | None = None,
        glaze: bool = False,
        smooth: bool = True,
        press: int = 1,
        note: str = "",
        **brush_overrides,
    ) -> StrokeRecord:
        """Paint one stroke and log it.

        Args:
            points: normalised (x, y) points, origin top-left. A single point makes
                one dab.
            brush: a preset name or a :class:`~easel.brush.Brush`.
            color: a pigment name, a mixed palette slot, a hex string, or an (r, g, b).
            pressure: ``"taper"``, ``"press_in"``, ``"lift_off"``, ``"even"``,
                ``"swell"``, ``"dab"``, a number, or a list along the stroke.
            size: override the brush size (fraction of the canvas long side).
            opacity: override the brush opacity.
            glaze: lay colour without building paint height.
            smooth: fit a spline through the points. Off gives hard corners.
            press: for a one-point mark, how many times to stamp the same spot.
                See :meth:`dab`. One mark either way, in the log and in the budget.
            note: a line recorded in the log, for the painter's own benefit.
            **brush_overrides: any other :class:`~easel.brush.Brush` field.

        Returns:
            The :class:`~easel.history.StrokeRecord` that was logged.
        """
        b = self._resolve_brush(brush, size, opacity, brush_overrides)
        col = self._resolve_color(color)
        stamps = int(press)
        if stamps < 1:
            raise ValueError(f"press must be at least 1, got {press}.")

        # Snapshot before the mark, so undo lands on the state before this stroke.
        self.history.push_snapshot(self.canvas.snapshot())
        try:
            index = self._index_base + len(self.history.records)
            pts = np.atleast_2d(np.asarray(points, dtype=np.float32))
            result = paint_stroke(
                self.canvas,
                pts,
                b,
                col,
                pressure=pressure,
                rng=self._stroke_rng(index),
                glaze=glaze,
                smooth=smooth,
                press=stamps,
            )

            record = self.history.add(
                StrokeRecord(
                    index=index,
                    kind="glaze" if glaze else ("smudge" if b.smudge >= 1.0 else "stroke"),
                    brush=b.name,
                    color_hex=self.palette.hex(col),
                    points=[[float(x), float(y)] for x, y in pts],
                    pressure=pressure if isinstance(pressure, str) else _plain(pressure),
                    dabs=result.dabs,
                    paint=result.paint,
                    note=note,
                    params=_brush_params(b, col, glaze=glaze, smooth=smooth, press=stamps),
                )
            )
        except Exception:
            # A bad path (wrong shape, a NaN/Infinity point) is caught inside
            # paint_stroke *after* the snapshot above was pushed. Left in place,
            # that snapshot has no record to match it, and the next undo() would
            # silently delete an unrelated, successful earlier stroke instead of
            # undoing nothing. See REVIEW.md.
            self.history.discard_snapshot()
            raise
        if self.timelapse:
            self.history.add_frame(self.canvas.thumbnail_srgb8())
        return record

    def dab(self, x: float, y: float, brush="round_hard", color="burnt_umber",
            press: int = 1, **kw):
        """A single mark at one point. Convenience for accents and highlights.

        ``press`` is how many times the brush is set down on the same spot, in one
        mark: one stroke in the log, one against the budget. One touch is a light
        one -- it lands about a quarter of the way to its colour, at about half the
        brush's width, because a lone dab is the *start* of the default ``taper``
        and a round tip's width follows its pressure. Three stamps press through
        full pressure in the middle one, so a catchlight lands at the size asked
        for and reads as light rather than as a smudge of it.

        Example::

            s.dab(*s.pt("catchlight"), brush="round_hard", color="white",
                  size=0.006, press=3)
        """
        return self.stroke([(x, y)], brush=brush, color=color, press=press, **kw)

    def smudge(self, points, size: float = 0.07, pressure="even", **kw):
        """Drag what is already on the canvas, rather than adding paint."""
        return self.stroke(points, brush="smudge", color="titanium_white",
                           pressure=pressure, size=size, **kw)

    def glaze(self, points, color, brush="round_soft", opacity: float = 0.18, **kw):
        """A thin transparent film over dry paint. Does not build height."""
        return self.stroke(points, brush=brush, color=color, opacity=opacity, glaze=True, **kw)

    def block_in(
        self,
        region,
        brush: str | Brush = "bristle",
        color="burnt_umber",
        direction: str = "horizontal",
        density: float = 1.0,
        pressure="taper",
        size: float | None = None,
        overhang: float | None = None,
        note: str = "",
        **brush_overrides,
    ) -> list[StrokeRecord]:
        """Fill a place with overlapping strokes, the way a painter blocks in a mass.

        This emits real strokes, not a fill: the brushwork stays visible, the edges
        stay ragged, and the paint runs out along each pass. That is the point --
        a flat fill is the single clearest tell that an image was not painted.

        The place can be a rectangle or a **shape**. Given a shape, each pass is cut
        against the outline and stops there, so a mass keeps its silhouette instead
        of arriving as a box that later strokes have to carve back:

            s.block_in(blob(cell("D5"), wobble=0.3), "bristle", "dark", direction="axis")

        Args:
            region: a name, a :class:`~easel.regions.Region`, a 4-tuple, or a
                :class:`~easel.regions.Polygon` from ``polygon``, ``ellipse``,
                ``blob``, ``hull`` or ``ribbon``.
            brush: preset name or brush.
            color: the colour to lay in.
            direction: ``"horizontal"``, ``"vertical"``, ``"diagonal"``, ``"cross"``
                or ``"axis"`` (the place's own long axis); a number of degrees,
                clockwise from the horizontal, to sweep the mass along its own form
                rather than along the canvas; or a sequence of any of those for one
                pass each. Vary this between passes so the marks are not parallel --
                and prefer the angle the *subject* runs at. A hillside swept at its
                own angle stops being a stack of horizontal bars, which is the single
                loudest tell that nobody chose the direction.
            density: 1.0 covers the place; below 1 leaves the ground showing
                through, which is usually what you want for a first pass.
            pressure: pressure profile for each pass.
            size: brush size override.
            overhang: how far each pass runs past the edge, as a fraction of the
                brush width. Defaults to ``0.35`` for a rectangle, where some
                overhang keeps the block from looking cropped, and to ``0`` for a
                shape, where the edge is the drawing. (Either way the brush is wider
                than the step between passes, so paint still breaks past the
                boundary; it is the pass *centres* that stop.)
            note: recorded in the log.

        Returns:
            The records for every stroke laid down.
        """
        place = as_place(region)
        b = self._resolve_brush(brush, size, None, brush_overrides)
        shaped = isinstance(place, Polygon)

        records: list[StrokeRecord] = []
        traced = ""
        if getattr(place, "traced", False):
            # An outline lifted off the reference, not drawn by the painter. The
            # brief reserves that question for the human; the least this can do is
            # be impossible to leave out of the write-up by accident.
            traced = " (traced)"
            self._note_assisted(f"traced outline blocked in: {place.name or 'shape'}")

        for pass_dir, path in self._block_in_paths(place, b, direction, density, overhang):
            records.append(
                self.stroke(
                    path,
                    brush=b,
                    color=color,
                    pressure=pressure,
                    note=note or (f"block-in {place.name or ('shape' if shaped else 'region')} "
                                  f"{pass_dir}{traced}"),
                )
            )
        return records

    def _block_in_paths(self, place, b: Brush, direction, density: float, overhang):
        """Every pass ``block_in`` would lay, as geometry, before any of it is paint.

        Split out so :meth:`cost` and :meth:`preview` can say what a mass charges
        without laying it: walking the passes is about a three-hundredth of the time
        painting them takes, and the count does not depend on the wander drawn per
        pass. It stays a generator, and stays consumed one path at a time by the
        loop above, because the pass wander is drawn from ``self.rng`` *between* the
        ``stroke()`` calls -- collecting the paths up front would reorder the stream
        and move every shaped painting ever made.

        One place, so the price quoted and the price paid cannot drift apart;
        ``test_cost_is_what_block_in_actually_charges`` holds them together.
        """
        shaped = isinstance(place, Polygon)
        over = (0.0 if shaped else 0.35) if overhang is None else float(overhang)
        band = _pass_step(b.size, density)
        for pass_dir in _pass_directions(direction):
            angle = place.axis if pass_dir == "axis" else pass_dir
            paths = (self._shape_paths(place, angle, band, b.size * over) if shaped
                     else self._block_paths(place, angle, band, b.size * over))
            for path in paths:
                yield pass_dir, path

    def _shape_paths(self, poly: Polygon, degrees, band: float, over: float):
        """Sweep a shape at an angle, every pass cut against its own outline.

        The same sweep as :meth:`_angled_paths`, clipped to the boundary instead of
        to four sides. A pass that crosses a concave shape comes back as the two or
        three pieces that are really inside it, so a mass with a bite out of it keeps
        the bite instead of being painted across.
        """
        rng = self.rng
        theta = math.radians(_angle_of(degrees))
        dx, dy = math.cos(theta), math.sin(theta)
        nx, ny = -dy, dx
        pts = np.asarray(poly.points, dtype=np.float64)
        cx, cy = poly.box.center
        offs = (pts[:, 0] - cx) * nx + (pts[:, 1] - cy) * ny
        lo_n, hi_n = float(offs.min()), float(offs.max())
        n_passes = max(1, int(round((hi_n - lo_n) / band)))

        for i in range(n_passes):
            off = lo_n + (i + 0.5) * (hi_n - lo_n) / n_passes
            ox, oy = cx + nx * off, cy + ny * off
            for t0, t1 in _spans_inside(poly, (ox, oy), (dx, dy)):
                if t1 - t0 < band * 0.35:
                    continue        # a sliver at the tip of the shape, not a stroke
                a, z = t0 - over, t1 + over
                wob = rng.normal(0.0, band * 0.3, size=3)
                path = [
                    _canvas_point(ox + dx * a + nx * wob[0], oy + dy * a + ny * wob[0]),
                    _canvas_point(ox + dx * (a + z) * 0.5 + nx * wob[1],
                                  oy + dy * (a + z) * 0.5 + ny * wob[1]),
                    _canvas_point(ox + dx * z + nx * wob[2], oy + dy * z + ny * wob[2]),
                ]
                yield path if i % 2 == 0 else path[::-1]

    def _angled_paths(self, r: Region, degrees: float, band: float, over: float):
        """Sweep a region at an arbitrary angle, stepping along the sweep's normal.

        The four named directions each have their own branch below, kept exactly as
        they were so that every painting made before angles existed still replays
        byte-for-byte. This is the general case: the pass runs along ``d``, the
        passes are stacked along ``n``, and each one is clipped to the region the
        same way the diagonal branch clips to it -- without the clip a pass keeps
        running to the full extent of its line and smears the mass across the canvas.
        """
        rng = self.rng
        theta = math.radians(float(degrees))
        dx, dy = math.cos(theta), math.sin(theta)
        nx, ny = -dy, dx
        cx, cy = (r.x0 + r.x1) * 0.5, (r.y0 + r.y1) * 0.5

        corners = [(r.x0, r.y0), (r.x0, r.y1), (r.x1, r.y0), (r.x1, r.y1)]
        offs = [(x - cx) * nx + (y - cy) * ny for x, y in corners]
        lo_n, hi_n = min(offs), max(offs)
        n_passes = max(1, int(round((hi_n - lo_n) / band)))

        for i in range(n_passes):
            off = lo_n + (i + 0.5) * (hi_n - lo_n) / n_passes
            ox, oy = cx + nx * off, cy + ny * off
            # How far along d the line stays inside the region, as a parameter
            # interval; the region is a rectangle, so clip against its two slabs.
            span = _segment_inside(
                (ox - dx * 2.0, oy - dy * 2.0), (ox + dx * 2.0, oy + dy * 2.0),
                r.bounds,
            )
            if span is None:
                continue
            t0, t1 = (s * 4.0 - 2.0 for s in span)     # back to distance along d
            if t1 - t0 <= 1e-6:
                continue                                # this line only clips a corner
            t0, t1 = t0 - over, t1 + over
            wob = rng.normal(0.0, band * 0.3, size=3)
            path = [
                _canvas_point(ox + dx * t0 + nx * wob[0], oy + dy * t0 + ny * wob[0]),
                _canvas_point(
                    ox + dx * (t0 + t1) * 0.5 + nx * wob[1],
                    oy + dy * (t0 + t1) * 0.5 + ny * wob[1],
                ),
                _canvas_point(ox + dx * t1 + nx * wob[2], oy + dy * t1 + ny * wob[2]),
            ]
            yield path if i % 2 == 0 else path[::-1]

    def _block_paths(self, r: Region, direction, band: float, over: float):
        if not isinstance(direction, str):
            yield from self._angled_paths(r, float(direction), band, over)
            return
        """Stroke paths that sweep a region, with a little wander so they are not rules.

        Consecutive passes run in opposite directions, the way a hand comes back
        across the canvas. Paint runs out along a stroke, so passes that all start
        at the same edge stack their run-out on top of each other and leave the
        whole mass a full value lighter on the side they end at. See REVIEW.md
        finding 12.
        """
        rng = self.rng
        if direction == "horizontal":
            n = max(1, int(round(r.height / band)))
            for i in range(n):
                y = r.y0 + (i + 0.5) * r.height / n
                wob = rng.normal(0.0, band * 0.3, size=3)
                path = [
                    (max(r.x0 - over, 0.0), float(np.clip(y + wob[0], 0.0, 1.0))),
                    ((r.x0 + r.x1) * 0.5, float(np.clip(y + wob[1], 0.0, 1.0))),
                    (min(r.x1 + over, 1.0), float(np.clip(y + wob[2], 0.0, 1.0))),
                ]
                yield path if i % 2 == 0 else path[::-1]
        elif direction == "vertical":
            n = max(1, int(round(r.width / band)))
            for i in range(n):
                x = r.x0 + (i + 0.5) * r.width / n
                wob = rng.normal(0.0, band * 0.3, size=3)
                path = [
                    (float(np.clip(x + wob[0], 0.0, 1.0)), max(r.y0 - over, 0.0)),
                    (float(np.clip(x + wob[1], 0.0, 1.0)), (r.y0 + r.y1) * 0.5),
                    (float(np.clip(x + wob[2], 0.0, 1.0)), min(r.y1 + over, 1.0)),
                ]
                yield path if i % 2 == 0 else path[::-1]
        elif direction == "diagonal":
            h = r.height
            span = r.width + h
            n = max(1, int(round(span / (band * 1.42))))
            for i in range(n):
                t = (i + 0.5) / n
                sx = r.x0 + t * span - h
                # The pass is the 45-degree line from (sx, y1) up to (sx + h, y0),
                # clipped to the region. Without the clip each pass keeps running to
                # the full extent of that line, which puts paint a whole region-height
                # to either side of the mass -- a block-in that smears off across the
                # canvas. The horizontal and vertical branches have always clamped to
                # the region edges; this is the same clamp, along the line instead.
                lo, hi = 0.0, 1.0
                if h > 1e-9:
                    lo = max(lo, (r.x0 - sx) / h)
                    hi = min(hi, (r.x1 - sx) / h)
                if hi - lo <= 1e-6:
                    continue                       # this line only clips the corner
                over_u = over / (h * 1.42) if h > 1e-9 else 0.0
                lo, hi = lo - over_u, hi + over_u
                wob = rng.normal(0.0, band * 0.3, size=3)
                path = [
                    (
                        float(np.clip(sx + u * h + w, 0.0, 1.0)),
                        float(np.clip(r.y1 - u * h, 0.0, 1.0)),
                    )
                    for u, w in zip((lo, (lo + hi) * 0.5, hi), wob, strict=True)
                ]
                yield path if i % 2 == 0 else path[::-1]
        else:
            raise ValueError(
                f"Unknown direction {direction!r}. "
                f"Use 'horizontal', 'vertical', 'diagonal' or 'cross'."
            )

    def sweep(
        self,
        edge,
        brush: str | Brush = "bristle",
        color="burnt_umber",
        into=None,
        depth: float = 0.2,
        size: float | None = None,
        passes: int | None = None,
        cross: float | None = None,
        closed: bool | None = None,
        density: float = 1.0,
        pressure="taper",
        note: str = "",
        **brush_overrides,
    ) -> list[StrokeRecord]:
        """Lay a mass that has a silhouette: passes swept along its edge, stepped inward.

        ``block_in`` fills a place: a rectangle, or a shape whose silhouette the
        painter can name, with the passes cut against it. This is the other way of
        laying a mass that has a shape, and it answers a different question -- here
        the boundary is the thing in hand and the passes follow it:
        the boundary is given, the first pass runs along it, and every pass after
        that is the same curve offset one part-brush further into the mass. Passes
        that run *along* the edge describe the form; columns that hang *down* from
        it comb the mass into strands and print the canvas's axis over the whole
        thing.

        It emits ordinary strokes, so the log, ``undo`` and ``replay`` are the same
        as for anything else painted by hand.

        The edge is meant to be the painter's own -- seen, marked and read off the
        grid. Feeding ``ref_outline(n)`` straight in is an assisted mode, the same
        as :meth:`sketch`: worth running, and any write-up has to say it was used.

        Args:
            edge: normalised (x, y) points along the boundary, in order. It may run
                off the canvas -- a mass that meets the frame should. A
                :class:`~easel.regions.Polygon` is such a boundary and is accepted
                as one: it closes on itself, so ``into`` and ``closed`` are not
                needed, and a traced one carries its own mark into the log.
            brush: preset name or brush.
            color: the colour to lay in.
            into: which side of the edge the mass is on. ``"down"``, ``"up"``,
                ``"left"``, ``"right"`` or a number of degrees clockwise from the
                horizontal step every pass along that one direction, the way a hand
                works down a near-horizontal edge. An (x, y) point *inside* the mass
                steps along the boundary's own normal instead, so the passes stay
                parallel to a curved edge. A closed edge needs neither: the mass is
                what the edge encloses.
            depth: how far into the mass to sweep, in normalised canvas units. The
                passes cover it a part-brush at a time.
            size: brush size override.
            passes: how many passes, if you would rather say than let the brush
                decide. Given, it pins the spacing at ``depth / passes``.
            cross: lay a second set of passes leaning this many degrees off the
                boundary, over the same ground. One sweep leaves the edge stringy,
                because a bristle brush covers about three-quarters of its width;
                crossing it closes the mass up. Twenty to thirty is usually enough.
            closed: treat the edge as a loop. Inferred when the last point is the
                first; pass ``True`` for a boundary that comes back on itself
                without repeating its first point, as ``ref_outline`` returns.
            density: as ``block_in``: 1.0 covers, below 1 spaces the passes out and
                leaves what is underneath showing through.
            pressure: pressure profile for each pass.
            note: recorded in the log.

        Returns:
            The records for every stroke laid down.
        """
        if isinstance(edge, Polygon):
            # A shape *is* a boundary that comes back on itself, which is what a
            # closed sweep wants. Its outline repeats the first point, so `closed`
            # infers itself, and the traced-copy question follows the shape here the
            # same way it follows it into block_in.
            if edge.traced:
                self._note_assisted(f"traced outline swept: {edge.name or 'shape'}")
            edge = edge.closed

        b = self._resolve_brush(brush, size, None, brush_overrides)
        depth, step, n_passes, cross = self._sweep_passes(b, depth, passes, cross, density)

        records: list[StrokeRecord] = []
        for kind, path in self._sweep_paths(edge, step, n_passes, depth, cross,
                                            into, closed):
            records.append(
                self.stroke(
                    path,
                    brush=b, color=color, pressure=pressure,
                    note=note or kind,
                )
            )
        return records

    def _sweep_passes(self, b: Brush, depth, passes, cross, density: float):
        """How many passes a sweep lays, how far apart -- and what it refuses to lay.

        Shared by :meth:`sweep` and :meth:`cost`, so that a sweep which is quoted a
        price and then painted agrees with itself on the count, and one that cannot
        be painted raises the same complaint when it is priced instead.

        Returns ``(depth, step, n_passes, cross)``, each validated.
        """
        depth = float(depth)
        if not math.isfinite(depth) or depth <= 0.0:
            raise ValueError(
                f"sweep(depth={depth!r}) is how far into the mass to sweep, and has "
                f"to be a positive distance."
            )
        if depth > _MAX_SWEEP_DEPTH:
            # A pass per part-brush, and nothing bounds the count the way a region
            # bounds block_in's. Almost always a depth given in pixels.
            raise ValueError(
                f"sweep(depth={depth!r}) is deeper than the canvas. Coordinates here "
                f"are normalised 0..1, so a mass the height of the canvas is "
                f"depth=1.0."
            )

        # One part-brush, the same rule block_in spaces its passes by.
        step = _pass_step(b.size, density)
        if passes is None:
            n_passes = max(1, int(round(depth / step)))
        else:
            n_passes = int(passes)
            if n_passes < 1:
                raise ValueError(f"sweep(passes={passes!r}) needs at least one pass.")
            step = depth / n_passes

        if cross is not None:
            cross = float(cross)
            if not math.isfinite(cross) or not 0.0 < abs(cross) < 90.0:
                raise ValueError(
                    f"sweep(cross={cross!r}) is how far the second set of passes "
                    f"leans off the boundary, in degrees: not zero, and under 90. "
                    f"At 90 they are columns hanging off the edge, which is the "
                    f"thing sweeping exists to avoid."
                )
        return depth, step, n_passes, cross

    def _sweep_paths(self, edge, step: float, n_passes: int, depth: float,
                     cross, into, closed):
        """Every pass ``sweep`` would lay, as geometry, before any of it is paint.

        :meth:`_block_in_paths`' counterpart, and split out for the same reason: a
        sweep is one call and ten to thirty strokes, so :meth:`cost` has to be able
        to price one without painting it. A generator for the same reason too --
        the wander comes off ``self.rng`` between the ``stroke()`` calls above.

        Yields the log note for each pass beside its path, because the two sets of
        passes are named differently in the log and a caller that only counts them
        does not care which is which.
        """
        spacing = max(step * 0.6, 0.008)
        spine, ring = _sweep_spine(edge, closed, spacing)
        normals = _sweep_normals(spine, into, ring)
        cum = _arc_length(spine)
        length = float(cum[-1])

        for k in range(n_passes):
            off = k * step + self._sweep_wobble(cum, length, step, ring)
            path = _drop_folds(spine + normals * off[:, None], spine, step)
            if path is None:
                continue                      # this pass folded in on itself: past the middle
            yield "sweep", (path if k % 2 == 0 else path[::-1])

        if cross is None:
            return

        for i, (us, vs) in enumerate(_cross_lines(length, depth, step, cross, spacing)):
            base = _band_points(spine, normals, cum, us, np.zeros_like(vs))
            wob = self._sweep_wobble(us, length, step, False)
            path = _drop_folds(_band_points(spine, normals, cum, us, vs + wob), base, step)
            if path is None:
                continue
            yield "sweep cross", (path if i % 2 == 0 else path[::-1])

    def _sweep_wobble(self, at, length: float, step: float, ring: bool) -> np.ndarray:
        """A smooth wander along a pass, so a sweep is not a set of parallel rules.

        Three draws interpolated along the pass, not noise per point: independent
        per-point noise clumps and gaps, which reads as an artefact rather than as a
        hand (REVIEW.md finding 4). A closed edge gets the same value at both ends
        so the seam does not step.
        """
        wob = self.rng.normal(0.0, step * 0.3, size=3)
        if ring:
            wob[-1] = wob[0]
        return np.interp(at, [0.0, length * 0.5, length], wob)

    # -- drawing ----------------------------------------------------------------
    def pencil(
        self,
        points,
        pressure: float = 0.55,
        width: float = 0.0026,
        smooth: bool = True,
        note: str = "",
    ) -> StrokeRecord:
        """Draw a graphite line under the paint. Not a stroke, and not counted as one.

        A painter does not start on a blank canvas. The sketch is the first pass and
        making it disappear is the painting, so this puts a line into the canvas's
        ``sketch`` channel: no paint, no wetness, no paint height, broken by the
        canvas tooth the way a real pencil is. Paint covers it in proportion to how
        much actually lands, so it survives under thin paint and in the ground and
        goes under an opaque mass.

        Draw *through* the shapes, not around them. Lines drawn as outlines get
        painted up to instead of through, and a painting made of filled outlines is
        the single clearest tell that nobody was looking at masses.

        Args:
            points: normalised (x, y) points. One point makes a tick.
            pressure: 0..1. Darkens the line and pushes it further into the tooth.
            width: line width as a fraction of the canvas long side.
            smooth: fit a spline through the points.
            note: recorded in the log.

        Example::

            s.pencil([s.pt("chin"), s.pt("jaw"), s.pt("ear")])
            s.look()                       # is the drawing right before any paint?
        """
        self.history.push_snapshot(self.canvas.snapshot())
        try:
            index = self._index_base + len(self.history.records)
            pts = np.atleast_2d(np.asarray(points, dtype=np.float32))
            result = draw_pencil(
                self.canvas, pts, width=width, pressure=pressure,
                rng=self._stroke_rng(index), smooth=smooth,
            )
            record = self.history.add(
                StrokeRecord(
                    index=index,
                    kind="pencil",
                    brush="pencil",
                    points=[[float(x), float(y)] for x, y in pts],
                    pressure=float(pressure),
                    dabs=result.dabs,
                    paint=result.paint,
                    note=note,
                    params={"width": float(width), "smooth": bool(smooth)},
                )
            )
        except Exception:
            # Same reasoning as stroke(): a failure after the snapshot above must
            # not leave it orphaned against the wrong record.
            self.history.discard_snapshot()
            raise
        if self.timelapse:
            self.history.add_frame(self.canvas.thumbnail_srgb8())
        return record

    def erase(self, region=None, note: str = "") -> StrokeRecord:
        """Rub out the drawing, all of it or inside one region or shape.

        Erase before painting rather than arguing with a line while painting. A line
        the painter has decided is wrong costs nothing to remove and costs a great
        deal to paint around.
        """
        place = as_place(region) if region is not None else None
        self.history.push_snapshot(self.canvas.snapshot())
        self.canvas.erase_sketch(place)
        record = self.history.add(
            StrokeRecord(
                index=self._index_base + len(self.history.records),
                kind="erase",
                note=note or ("erase" + (f" {place}" if place is not None else " all")),
                params=_place_params(place),
            )
        )
        if self.timelapse:
            # erase() visibly changes the rendered canvas (it clears the sketch
            # channel, which the thumbnail includes) the same way stroke() and
            # pencil() do, so it belongs in the time-lapse the same way they are.
            self.history.add_frame(self.canvas.thumbnail_srgb8())
        return record

    def sketch_lines(self) -> list[list[tuple[float, float]]]:
        """Every pencil line still drawn, as normalised points.

        So a stroke can be aimed at a line, swept along it, or ignore it::

            for line in s.sketch_lines():
                s.stroke(line, "bristle", "shadow", size=0.05)

        What :meth:`erase` rubbed out is gone from here too, cut at the region's
        edge, so a line that only crosses the erased area comes back as the pieces
        outside it. This is derived from the log rather than stored, which is what
        keeps it right through undo and replay.
        """
        lines: list[list[tuple[float, float]]] = []
        for r in self.history.records:
            if r.kind == "pencil":
                lines.append([(float(x), float(y)) for x, y in r.points])
            elif r.kind == "erase":
                place = _place_from_params(r.params)
                lines = [] if place is None else _erase_from_lines(lines, place)
        return lines

    # -- landmarks --------------------------------------------------------------
    def mark(self, name: str, x: float, y: float) -> tuple[float, float]:
        """Record a named point, and show it on every look from now on.

        This is the unit of a drawing. Six or seven verified points -- where a
        silhouette turns, where two masses meet, the top and base of a shape -- and
        the masses get hung on them. Verify each one against the reference at
        feature scale before trusting it::

            s.mark("top_l", *cell("D4").point(0.3, 0.6))
            s.look(region=cell("D4"), reference=ref, grid="fine")

        Args:
            name: what to call it. Re-using a name moves the mark.
            x, y: normalised position.

        Returns:
            The point, so it can be used inline.
        """
        key = str(name).strip()
        if not key:
            raise ValueError("A landmark needs a name: mark('top_l', 0.42, 0.31)")
        if not (math.isfinite(x) and math.isfinite(y)):
            raise ValueError(f"A landmark needs a real position, got ({x!r}, {y!r}).")
        pt = (float(np.clip(x, 0.0, 1.0)), float(np.clip(y, 0.0, 1.0)))
        self.marks[key] = pt
        return pt

    def pt(self, name: str) -> tuple[float, float]:
        """A landmark, for use in a path: ``s.stroke([s.pt("top_l"), s.pt("base")])``."""
        key = str(name).strip()
        if key not in self.marks:
            known = ", ".join(sorted(self.marks)) or "(none yet)"
            raise KeyError(f"No landmark {name!r}. Marked so far: {known}.")
        return self.marks[key]

    def unmark(self, name: str) -> None:
        """Forget a landmark. Marking over it with the same name also moves it."""
        self.marks.pop(str(name).strip(), None)

    # -- canvas state -----------------------------------------------------------
    def dry(self, amount: float = 1.0, region=None) -> StrokeRecord:
        """Dry the canvas so the next paint covers instead of mixing.

        All of it, or inside one region or shape -- a shaped mass can be dried and
        painted over without drying the wet neighbour it has to blend into.
        """
        place = as_place(region) if region is not None else None
        # Snapshot before the mark, like every other canvas-mutating call: without
        # this, undo() after a dry() pops the *previous* paint action's snapshot
        # while only dropping the dry record, desyncing the canvas from the log.
        self.history.push_snapshot(self.canvas.snapshot())
        self.canvas.dry(amount, place)
        return self.history.add(
            StrokeRecord(
                index=self._index_base + len(self.history.records),
                kind="dry",
                note=f"dry {amount:.2f}" + (f" in {place}" if place is not None else ""),
                params={"amount": float(amount), **_place_params(place)},
            )
        )

    def undo(self, n: int = 1) -> int:
        """Scrape back ``n`` strokes. Returns how many were actually undone.

        This is not free and it is not the usual repair. Painting over a mistake is
        almost always the better move, and it is what a painter does.
        """
        if n <= 0 or not self.history.records:
            return 0
        depth = self.history.undo_depth
        if depth >= n:
            undone = self.history.records[-n:]
            snap = self.history.pop_snapshots(n)
            if snap is not None:
                self.canvas.restore(snap)
                if self.timelapse:
                    # Every record kind that pushes a snapshot except "dry" also
                    # adds a time-lapse frame (dry() only touches wetness, which
                    # a plain render never shows); drop exactly as many frames as
                    # undone records actually added, so the time-lapse does not
                    # keep frames for strokes that are no longer on the canvas.
                    self.history.drop_last_frames(
                        sum(1 for r in undone if r.kind != "dry")
                    )
                return n
        # Too few snapshots for the full request (older ones are dropped past
        # MAX_SNAPSHOTS), or none at all because this session came off disk.
        # Rebuild the whole way from the log instead -- costs a full repaint, but
        # it is exact, and it is what keeps undo(n) answering the same question
        # the same way regardless of how many snapshots this process happens to
        # have cached.
        keep = max(0, len(self.history.records) - n)
        undone = len(self.history.records) - keep
        self._adopt(self.replay(upto=keep))
        return undone

    # -- looking ----------------------------------------------------------------
    def look(
        self,
        scale: int | None = DEFAULT_LOOK_SIZE,
        grid: bool | str = False,
        values: bool = False,
        region=None,
        reference: str | Path | Image.Image | None = None,
        diff: bool = False,
        path: str | Path | None = None,
        impasto: bool = True,
        sketch: bool = True,
        marks: bool = True,
    ) -> Path:
        """Look at the canvas. Returns the path to a PNG.

        Look every five to fifteen strokes. A stroke you did not look at was a guess.

        Args:
            scale: long-side pixel limit; ``None`` for full resolution.
            grid: ``True`` overlays the labelled A-H by 1-8 grid; ``"fine"`` divides
                what is on screen into labelled tenths instead, which is how a place
                *inside* a cell gets named.
            values: greyscale, for judging the value structure.
            region: crop to a region, enlarged so a small crop is readable. With
                ``reference``, **both** panels are cropped to the same place.
            reference: place a reference image alongside for comparison.
            diff: tint what changed since the previous ``look()``.
            path: where to write. Defaults to ``out_dir/look_NNN.png``.
            impasto: shade paint height as relief.
            sketch: show the pencil underdrawing the paint has not covered.
            marks: draw the landmarks, on both panels.

        Example::

            s.look(region=cell("D4"), reference=ref, grid="fine")
        """
        ref_img = None if reference is None else load_reference(reference)

        current = self._look_array(values, impasto, sketch)
        img = render_look(
            self.canvas,
            scale=scale,
            grid=grid,
            values=values,
            region=region,
            reference=ref_img,
            diff_against=self._last_look if diff else None,
            impasto=impasto,
            sketch=sketch,
            marks=self.marks if marks else None,
        )
        self._last_look = current
        return save_look(img, self._look_path(path))

    def look_image(self, **kwargs) -> Image.Image:
        """The same view as :meth:`look`, returned as a PIL image instead of a path."""
        ref = kwargs.pop("reference", None)
        ref_img = None if ref is None else load_reference(ref)
        diff = kwargs.pop("diff", False)
        show_marks = kwargs.pop("marks", True)
        img = render_look(
            self.canvas, reference=ref_img,
            diff_against=self._last_look if diff else None,
            marks=self.marks if show_marks else None, **kwargs
        )
        self._last_look = self._look_array(
            kwargs.get("values", False), kwargs.get("impasto", True), kwargs.get("sketch", True)
        )
        return img

    def _look_array(self, values: bool, impasto: bool, sketch: bool) -> np.ndarray:
        """The array :func:`render_look` actually draws, before any grid or diff tint.

        Stored as ``_last_look`` so the next ``diff=True`` call compares like
        with like. Storing the plain colour render regardless of ``values``
        (the bug this replaced) meant a ``look(values=True, diff=True)`` always
        compared a greyscale render against a stored colour one -- which differ
        almost everywhere by construction -- and tinted the whole canvas as
        "changed" even when nothing had been painted since the last look.
        """
        if values:
            grey = self.canvas.values(sketch=sketch)
            return np.repeat(grey[:, :, None], 3, axis=2)
        return self.canvas.to_srgb8(impasto=impasto, sketch=sketch)

    def _look_path(self, path: str | Path | None, prefix: str = "look") -> Path:
        if path is not None:
            return Path(path)
        self._look_counter += 1
        return self.out_dir / f"{prefix}_{self._look_counter:03d}.png"

    # -- planning ---------------------------------------------------------------
    def preview(
        self,
        strokes,
        reference: str | Path | Image.Image | None = None,
        region=None,
        grid: bool | str = False,
        values: bool = False,
        path: str | Path | None = None,
        scale: int | None = DEFAULT_LOOK_SIZE,
    ) -> Path:
        """Draw intended strokes over the canvas -- and the reference -- without painting.

        Nothing is painted and nothing is logged. The points and the brush's width
        are drawn as an overlay on both panels, so a guess about where a mark goes
        is checked against the photograph *before* it is paid for in paint. The loop
        stops being paint-look-repair and becomes plan-check-paint.

        Args:
            strokes: what to preview. Each entry is either a list of points or a
                dict of arguments for :meth:`stroke` (``points`` plus any of
                ``brush``, ``size``, ``note``...), or a **mass**, drawn as the area
                it would cover: a shape, a region, or a dict with ``shape=`` and any
                :meth:`block_in` argument; or a dict with ``edge=`` and any
                :meth:`sweep` argument, drawn as the ground that sweep would cover.
                A single path or shape is also accepted.
            reference: shown alongside, with the same overlay.
            region: crop both panels to a place, enlarged.
            grid: as :meth:`look`. ``"fine"`` for tenths.
            values: greyscale.
            path: where to write. Defaults to ``out_dir/preview_NNN.png``.
            scale: long-side pixel limit.

        Example::

            plan = [{"points": [s.pt("top_l"), (0.44, 0.30)], "brush": "liner",
                     "size": 0.004, "label": "edge"}]
            s.preview(plan, reference=ref, region=cell("D4"), grid="fine")
            s.preview(blob(cell("D5")), reference=ref)      # a mass, before filling it
            s.preview({"edge": edge, "into": "down", "depth": 0.3})   # and a sweep
        """
        specs = self._plan_specs(strokes)
        ref_img = None if reference is None else load_reference(reference)
        img = render_look(
            self.canvas,
            scale=scale,
            grid=grid,
            values=values,
            region=region,
            reference=ref_img,
            marks=self.marks or None,
            strokes=[self._preview_entry(kind, spec, i)
                     for i, (kind, spec) in enumerate(specs)],
        )
        return save_look(img, self._look_path(path, "preview"))

    def rehearse(
        self,
        strokes,
        reference: str | Path | Image.Image | None = None,
        region=None,
        grid: bool | str = False,
        values: bool = False,
        path: str | Path | None = None,
        scale: int | None = DEFAULT_LOOK_SIZE,
    ) -> Path:
        """Paint the strokes on a *copy* of the canvas and look at the result.

        Nothing is committed and nothing is logged. The preview shows where a mark
        will go; the rehearsal shows what it will look like -- the brush's tooth
        breakup, how it mixes with what is already wet, whether it reads at all at
        this size. A feature the size of an eye can be tried three ways and judged
        before a stroke is spent, which is what a painter's scrap of canvas is for.

        The trial marks are seeded as if they were the next marks of the real
        painting, so what is rehearsed is what lands when it is painted for real --
        pixel for pixel, masses included, as long as the plan is painted before
        anything else is.

        **A mass is the thing worth rehearsing.** ``block_in`` and ``sweep`` are one
        call each and ten to thirty strokes each, which makes them the most
        expensive mark a painter can get wrong, and :meth:`preview` only shows the
        silhouette. Describe one instead of calling it and it is painted on the
        copy, looked at, and costs nothing::

            plan = [{"shape": blob(span("D4", "F6"), wobble=0.3, seed=2),
                     "brush": "bristle", "color": "dark", "size": 0.09,
                     "direction": "axis"}]
            s.rehearse(plan, region=span("D4", "F6"))     # what would that look like?
            s.rehearse([dict(plan[0], size=0.05)], region=span("D4", "F6"))  # or this?
            s.block_in(plan[0]["shape"], "bristle", "dark", size=0.09,
                       direction="axis")                  # the one you chose

        A sweep is described the same way, with the boundary under ``edge=`` and any
        other :meth:`sweep` argument beside it::

            s.rehearse({"edge": edge, "into": "down", "depth": 0.30, "cross": 25,
                        "brush": "bristle", "color": "dark", "size": 0.12})

        Args:
            strokes: as :meth:`preview`, marks and masses alike -- a shaped mass is
                twenty passes, and worth trying on the scrap of canvas first.
            reference: shown alongside, cropped to the same place.
            region: crop both panels, enlarged. Use one -- the point is feature scale.
            grid: as :meth:`look`.
            values: greyscale.
            path: where to write. Defaults to ``out_dir/rehearse_NNN.png``.
            scale: long-side pixel limit.
        """
        trial = self._trial_session()
        for kind, spec in self._plan_specs(strokes):
            kwargs = {k: v for k, v in spec.items()
                      if k not in ("label", "place", "edge")}
            if kind == "mass":
                trial.block_in(spec["place"], **kwargs)
            elif kind == "sweep":
                trial.sweep(spec["edge"], **kwargs)
            else:
                trial.stroke(**kwargs)

        ref_img = None if reference is None else load_reference(reference)
        img = render_look(
            trial.canvas,
            scale=scale,
            grid=grid,
            values=values,
            region=region,
            reference=ref_img,
            marks=self.marks or None,
        )
        return save_look(img, self._look_path(path, "rehearse"))

    def cost(self, strokes) -> int:
        """What a plan would charge against the stroke budget, without painting it.

        A mark costs one. A **mass** costs what its passes come to, and that is the
        number no painter can work out by hand: a mass is priced on the extent of
        its bounding box along the sweep's normal *and* on how many times a pass
        line crosses it, so anything curved or concave costs more than the box it
        sits in. A ribbon `0.029` wide at brush `0.015` is 4 passes straight and 75
        round a bend -- and the bend is not a defect to route around, it is what the
        band costs when its box is ten times its width.

        Same plan as :meth:`preview` and :meth:`rehearse`, so the three answer the
        three questions about a mark in the same words: where it goes, what it looks
        like, and what it costs. Nothing is painted, nothing is logged, and the
        stroke stream is not spent, so this can be called as often as it is useful::

            plan = {"shape": mass, "brush": "bristle", "color": "dark", "size": 0.05}
            s.cost(plan)                      # 31 -- a tenth of the budget
            s.cost(dict(plan, size=0.09))     # 12 -- the same mass, a wider brush
            s.preview(plan)                   # the count is on the overlay too

        Args:
            strokes: as :meth:`preview` -- marks, masses and sweeps, one or a list.

        Returns:
            The number of strokes painting the plan would charge.
        """
        return sum(self._plan_cost(kind, spec)
                   for kind, spec in self._plan_specs(strokes))

    def _plan_cost(self, kind: str, spec: dict) -> int:
        """Price one plan entry by walking its passes, not by laying them.

        On a trial session, whose generator holds a *copy* of the real stream: the
        pass wander is drawn while counting and would otherwise be spent, changing
        the painting that followed. The count itself does not depend on it.
        """
        if kind == "stroke":
            return 1
        trial = self._trial_session()
        b = trial._resolve_brush(spec.get("brush", "bristle"), spec.get("size"),
                                 spec.get("opacity"), {})
        if kind == "mass":
            return sum(1 for _ in trial._block_in_paths(
                spec["place"], b, spec.get("direction", "horizontal"),
                float(spec.get("density", 1.0)), spec.get("overhang")))

        # A sweep works its pass count out from the depth before any geometry is
        # walked, so the quote goes through the same arithmetic the painted one does
        # -- including its refusals, so a plan that cannot be swept says so when it
        # is priced rather than when it is paid for.
        edge = spec["edge"]
        depth, step, n_passes, cross = trial._sweep_passes(
            b, spec.get("depth", 0.2), spec.get("passes"), spec.get("cross"),
            float(spec.get("density", 1.0)))
        return sum(1 for _ in trial._sweep_paths(
            edge.closed if isinstance(edge, Polygon) else edge,
            step, n_passes, depth, cross, spec.get("into"), spec.get("closed")))

    def _trial_session(self) -> Session:
        """A throwaway session sharing this one's surface, palette and seeding.

        The canvas channels are copied and the tooth is shared, so a rehearsal costs
        a few small arrays rather than a whole canvas. It gets its own generator
        *object* holding a copy of this session's stream state, so what is tried on
        the scrap of canvas is what lands -- masses included -- without the trial
        consuming the real stream and changing the painting that follows it.
        """
        trial = Session.__new__(Session)
        trial.seed = self.seed
        # A separate generator holding this one's current state. `block_in` and
        # `sweep` draw their pass wander from here, so a copy of the state is what
        # makes a rehearsed mass the same mass, pixel for pixel, when it is painted
        # for real -- and because it is a copy, spending it costs the real session
        # nothing. Strokes need no help: they are seeded per index below.
        trial.rng = np.random.default_rng(self.seed)
        trial.rng.bit_generator.state = self.rng.bit_generator.state
        trial.canvas = self.canvas.trial_copy()
        trial.palette = self.palette
        trial.history = History()
        trial.out_dir = self.out_dir
        trial.timelapse = False
        trial._look_counter = 0
        trial._last_look = None
        trial.marks = self.marks
        trial._preparation = self._preparation
        trial.assisted = []
        trial._index_base = self._index_base + len(self.history.records)
        return trial

    def _stroke_specs(self, strokes) -> list[dict]:
        """Normalise what ``preview`` and ``rehearse`` accept into stroke kwargs.

        One place, so that a plan handed to ``preview`` can be handed unchanged to
        ``rehearse`` and then to ``stroke``. A plan that has to be rewritten between
        checking it and painting it is a plan that will drift.
        """
        if isinstance(strokes, dict):
            strokes = [strokes]
        elif _is_path(strokes):
            strokes = [strokes]
        out: list[dict] = []
        for entry in strokes:
            if isinstance(entry, dict):
                spec = dict(entry)
                if "points" not in spec:
                    raise ValueError(
                        f"A stroke spec needs 'points': {spec!r}. Give a list of "
                        f"(x, y) points, or a dict like "
                        f"{{'points': [...], 'brush': 'liner', 'size': 0.004}}."
                    )
            else:
                spec = {"points": entry}
            pts = np.atleast_2d(np.asarray(spec["points"], dtype=np.float32))
            if pts.ndim != 2 or pts.shape[1] != 2:
                raise ValueError(
                    f"Stroke points must be (x, y) pairs, got shape {pts.shape}."
                )
            spec["points"] = [(float(x), float(y)) for x, y in pts]
            out.append(spec)
        return out

    def _plan_specs(self, entries) -> list[tuple[str, dict]]:
        """Split what ``preview`` and ``rehearse`` accept into marks and masses.

        A plan entry is a mark -- a path, or a dict of :meth:`stroke` arguments -- or
        a mass. A mass is described the way the call that lays it is: a shape or
        region, or a dict with ``shape=`` and any :meth:`block_in` argument, is a
        block-in; a dict with ``edge=`` and any :meth:`sweep` argument is a sweep.
        One list holds all three, so a plan is previewed, rehearsed and painted
        without being rewritten in between, which is when a plan drifts.
        """
        if isinstance(entries, (dict, Polygon, Region)) or _is_path(entries):
            entries = [entries]
        out: list[tuple[str, dict]] = []
        for entry in entries:
            if isinstance(entry, (Polygon, Region)):
                out.append(("mass", {"place": as_place(entry)}))
            elif isinstance(entry, dict) and "points" not in entry and "edge" in entry:
                out.append(("sweep", dict(entry)))
            elif isinstance(entry, dict) and "points" not in entry and (
                    "shape" in entry or "region" in entry):
                spec = dict(entry)
                place = spec.pop("shape", None)
                fallback = spec.pop("region", None)
                spec["place"] = as_place(place if place is not None else fallback)
                out.append(("mass", spec))
            else:
                out.append(("stroke", self._stroke_specs([entry])[0]))
        return out

    def _preview_entry(self, kind: str, spec: dict, index: int) -> dict:
        """What the overlay needs, whichever of the three kinds this entry is."""
        if kind == "mass":
            return self._preview_mass(spec, index)
        if kind == "sweep":
            return self._preview_sweep(spec, index)
        return self._preview_shape(spec, index)

    def _priced(self, kind: str, spec: dict, label: str) -> str:
        """A mass's label with what it charges, so the price is on the picture.

        Only for the two kinds that cost more than the painter can count: a mark is
        one stroke and saying so would be noise on every overlay. Walking the passes
        costs a few milliseconds against the preview's own render, which is why this
        can be unconditional rather than something to remember to ask for.
        """
        return f"{label}  {self._plan_cost(kind, spec)} strokes"

    def _preview_sweep(self, spec: dict, index: int) -> dict:
        """What the overlay needs for a sweep: the ground it covers, and the brush."""
        b = self._resolve_brush(spec.get("brush", "bristle"), spec.get("size"),
                                spec.get("opacity"), {})
        edge = spec["edge"]
        points = _sweep_cover(edge.closed if isinstance(edge, Polygon) else edge,
                              b.size, float(spec.get("density", 1.0)),
                              float(spec.get("depth", 0.2)), spec.get("into"),
                              spec.get("closed"))
        label = str(spec.get("label", spec.get("note") or f"sweep {index + 1}"))
        return {"points": points, "width": b.size, "fill": True,
                "label": self._priced("sweep", spec, label)}

    def _preview_mass(self, spec: dict, index: int) -> dict:
        """What the overlay needs for a mass: its outline and the brush filling it."""
        place = spec["place"]
        b = self._resolve_brush(spec.get("brush", "bristle"), spec.get("size"),
                                spec.get("opacity"), {})
        points = (place.closed if isinstance(place, Polygon)
                  else [(place.x0, place.y0), (place.x1, place.y0),
                        (place.x1, place.y1), (place.x0, place.y1), (place.x0, place.y0)])
        label = str(spec.get("label", spec.get("note") or place.name
                              or f"mass {index + 1}"))
        return {"points": points, "width": b.size, "fill": True,
                "label": self._priced("mass", spec, label)}

    def _preview_shape(self, spec: dict, index: int) -> dict:
        """What the overlay needs: the path, the brush's width, and a label."""
        b = self._resolve_brush(
            spec.get("brush", "bristle"), spec.get("size"), spec.get("opacity"),
            {k: v for k, v in spec.items()
             if k not in ("points", "brush", "size", "opacity", "color", "pressure",
                          "glaze", "smooth", "press", "note", "label")},
        )
        # The band stands for how wide the mark will be, and on a round tip that now
        # depends on the pressure it is planned with -- a lone stamp most of all.
        dabs = int(spec.get("press", 1)) if len(spec["points"]) == 1 else 32
        width = b.size * press_width(b, spec.get("pressure", "taper"), dabs)
        return {"points": spec["points"], "width": width,
                "label": str(spec.get("label", spec.get("note", "") or index + 1))}

    # -- measuring --------------------------------------------------------------
    def compare(
        self,
        reference: str | Path | Image.Image,
        region=None,
        path: str | Path | None = None,
        threshold: float = 0.10,
    ) -> Comparison:
        """Per-cell value of the reference, of the canvas, and the difference.

        Squinting says something is off; this says which mass and by how much. The
        threshold that matters is ``0.10`` -- two masses closer than that read as
        one, so a cell further out than that is a separation the painting has lost.

        Args:
            reference: the image to measure against.
            region: measure inside a region, in its own tenths, instead of over the
                whole canvas in A-H by 1-8 cells. The labels are the ones
                ``look(grid="fine")`` shows, so a cell that is out names the place
                to fix: ``region.point(0.3, 0.6)``.
            path: where to write the heat map. Defaults to ``out_dir/compare_NNN.png``.
            threshold: what counts as out.

        Returns:
            A :class:`~easel.measure.Comparison`. Print it.

        Example::

            print(s.compare("mug.jpg"))
            for c in s.compare("mug.jpg").fixable:   # off, minus what cannot be painted
                print(c.label, c.delta)

        Cells whose reference is darker than the palette's own floor are reported
        as ``unreachable`` rather than as work. Since the masstones were darkened
        that floor is close to the engine's own, so expect the list to be empty:
        every cell on the object is normally the painter's to fix, and ``fixable``
        is then just ``off``.
        """
        ref_img = load_reference(reference)
        r = as_region(region) if region is not None else None

        canvas_rgb = self.canvas.to_srgb8(impasto=False)
        if r is not None:
            x0, y0, x1, y1 = self.canvas.region_px(r)
            canvas_rgb = canvas_rgb[y0:y1, x0:x1]
            rw, rh = ref_img.size
            # x0/y0 clipped first so a crop touching or past the far edge still
            # leaves room for x1/y1 to land strictly past it: rounding two
            # independently-clamped endpoints does not by itself guarantee
            # x1 > x0, and a zero-width PIL crop does not raise -- it silently
            # feeds an empty array into the value comparison below, as NaNs.
            ref_x0 = int(np.clip(round(r.x0 * rw), 0, max(rw - 1, 0)))
            ref_y0 = int(np.clip(round(r.y0 * rh), 0, max(rh - 1, 0)))
            ref_x1 = int(np.clip(max(round(r.x1 * rw), ref_x0 + 1), 1, rw))
            ref_y1 = int(np.clip(max(round(r.y1 * rh), ref_y0 + 1), 1, rh))
            ref_img = ref_img.crop((ref_x0, ref_y0, ref_x1, ref_y1))
        ref_rgb = np.asarray(ref_img, dtype=np.uint8)

        result = compare_images(canvas_rgb, ref_rgb, region=r, threshold=threshold,
                                floor=self.palette.darkest_value)
        sheet = heat_sheet(
            result,
            canvas_grey=_grey(canvas_rgb),
            reference_grey=_grey(ref_rgb),
        )
        result.path = save_look(sheet, self._look_path(path, "compare"))
        return result

    # -- reading the reference --------------------------------------------------
    def prepare(
        self,
        reference: str | Path | Image.Image,
        level: str = "coarse",
        path: str | Path | None = None,
        min_share: float = 0.004,
    ) -> Preparation:
        """Cut the reference into numbered masses, and write the overlay to look at.

        No model and no learned segmentation: the photograph is quantised in a
        perceptual colour space and its connected areas are labelled and numbered.
        The map will be wrong in places -- it joins two things of the same colour
        and cuts one thing along its shading -- so read it, then correct it with
        ``prep.merge(...)`` and ``prep.split(...)``. The useful sentence is "area 5
        is one thing, less the strip that belongs to its neighbour".

        Args:
            reference: a path or a PIL image.
            level: ``"coarse"`` (five to eight masses -- start here), ``"medium"``
                (about twenty), or ``"fine"``.
            path: where to write the overlay. Defaults to ``out_dir/prepare_NNN.png``.
            min_share: fragments smaller than this share of the picture are merged.

        Returns:
            A :class:`~easel.prepare.Preparation`. Print it for the table.

        Example::

            prep = s.prepare("mug.jpg")
            print(prep)
            prep.merge(3, 7)                      # both halves are one mug
            s.look(region=prep.region(3), reference="mug.jpg", grid="fine")
        """
        ref_img = load_reference(reference)
        prep = prepare_reference(ref_img, level=level, min_share=min_share, seed=self.seed)
        if isinstance(reference, (str, Path)):
            prep.source = Path(reference)
        self._preparation = prep
        self.look_areas(ref_img, path=path)
        return prep

    def look_areas(
        self,
        reference: str | Path | Image.Image | None = None,
        path: str | Path | None = None,
    ) -> Path:
        """Re-draw the prepared outlines and numbers over both panels.

        Call this after correcting the map. ``prep.merge(3, 7)`` changes the areas
        and their numbers, and reading a table without seeing the new outlines is
        how the painter ends up blocking in an area that no longer means what the
        note about it said.

        Args:
            reference: the photograph to draw on. Defaults to the one prepared.
            path: where to write. Defaults to ``out_dir/prepare_NNN.png``.
        """
        prep = self.preparation
        source = reference if reference is not None else prep.source
        if source is None:
            raise ValueError(
                "This preparation did not come from a file, so it does not know "
                "which image to draw on. Pass reference=..."
            )
        ref_img = load_reference(source)
        sheet = prep.overlay(ref_img, Image.fromarray(self.canvas.to_srgb8(), mode="RGB"))
        prep.overlay_path = save_look(sheet, self._look_path(path, "prepare"))
        return prep.overlay_path

    @property
    def preparation(self) -> Preparation:
        """The most recent :meth:`prepare`. Raises if there has not been one."""
        if self._preparation is None:
            raise RuntimeError(
                "No prepared reference yet. Call s.prepare('reference.jpg') first."
            )
        return self._preparation

    def ref_region(self, number: int) -> Region:
        """The bounds of one prepared area, for ``look(region=...)`` or a block-in."""
        return self.preparation.region(number)

    def ref_outline(self, number: int) -> list[tuple[float, float]]:
        """One prepared area's boundary as normalised points."""
        return self.preparation.outline(number)

    def ref_shape(self, number: int) -> Polygon:
        """One prepared area as a shape, ready to block in. **An assisted mode.**

        The outline came off the photograph, not out of the painter, so a mass
        blocked in on one is partly traced -- the question the brief reserves for the
        human, the same one :meth:`sketch` raises. Using it is a choice, not a
        default: it is recorded in :attr:`assisted` and in the log, and a run that
        uses it says so in the write-up.

        The unassisted way is to read the map, look at the shape, and lay the
        outline yourself: three or four landmarks and ``hull(...)``, or ``blob``,
        ``ellipse`` or ``ribbon`` sized to a cell.
        """
        return Polygon(tuple(self.preparation.outline(number)),
                       name=f"area {int(number)}", traced=True)

    def sketch(
        self,
        reference: str | Path | Image.Image | None = None,
        level: str = "coarse",
        pressure: float = 0.5,
        areas: list[int] | None = None,
    ) -> list[StrokeRecord]:
        """Lay the prepared outlines as pencil, in one call. **An assisted mode.**

        This is not the headline way to work and the definition of done says so: a
        run that starts from a machine-laid sketch measures the segmenter, not the
        painter. Use it deliberately, report it separately, and never for the
        unprompted stage -- there the pencil is the painter's own.

        The painter's own way is :meth:`pencil`: sketch the masses, look, adjust,
        then block in.

        Args:
            reference: what to prepare. Omit to use the most recent :meth:`prepare`.
            level: granularity, when preparing here.
            pressure: how dark the laid lines are.
            areas: only these area numbers. Default is all of them.

        Returns:
            One record per line drawn.
        """
        prep = self.preparation if reference is None else self.prepare(reference, level=level)
        wanted = prep.numbers if areas is None else [int(a) for a in areas]
        records = []
        for number in wanted:
            outline = prep.outline(number)
            if len(outline) < 2:
                continue
            records.append(
                self.pencil(outline + outline[:1], pressure=pressure, smooth=False,
                            note=f"sketch area {number}")
            )
        if records:
            self._note_assisted(f"machine sketch: {len(records)} outlines laid as pencil")
        return records

    # -- output -----------------------------------------------------------------
    def export(self, path: str | Path, impasto: bool = True, sketch: bool = True) -> Path:
        """Write the finished painting as a PNG at full resolution.

        Args:
            path: where to write.
            impasto: shade paint height as relief.
            sketch: keep whatever graphite the paint has not covered. This is on by
                default because it is what is on the canvas -- an underdrawing that
                still shows is a fact about the painting, not a rendering option.
                ``sketch=False`` shows the paint alone.
        """
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        Image.fromarray(self.canvas.to_srgb8(impasto=impasto, sketch=sketch),
                        mode="RGB").save(p)
        return p

    def timelapse_gif(self, path: str | Path, fps: float = 8.0) -> Path:
        """Write the time-lapse as an animated GIF."""
        return self.history.save_gif(path, fps=fps)

    def contact_sheet(self, path: str | Path, columns: int = 6) -> Path:
        """Write the time-lapse as a grid of thumbnails."""
        return self.history.save_contact_sheet(path, columns=columns)

    def capture_frame(self) -> None:
        """Record a time-lapse frame by hand, when ``timelapse`` is off."""
        self.history.add_frame(self.canvas.thumbnail_srgb8())

    def _note_assisted(self, what: str) -> None:
        """Record an assisted mode, once. See :attr:`assisted`."""
        if what not in self.assisted:
            self.assisted.append(what)

    def log(self, last: int = 10) -> str:
        """A short text summary of recent marks, and any assisted mode used."""
        text = self.history.summary(last)
        if self.assisted:
            text += "\nAssisted: " + "; ".join(self.assisted)
        return text

    # -- persistence ------------------------------------------------------------
    def save(self, path: str | Path) -> Path:
        """Save the whole session to a single ``.easel`` file (compressed npz).

        The CLI uses this so a painter can work in small increments from a shell
        without holding a Python process open.
        """
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        meta = {
            "format": _EASEL_FORMAT,
            "width": self.canvas.width,
            "height": self.canvas.height,
            "texture": self.canvas.texture_name,
            "ground": self.canvas.ground_name,
            "ground_spec": self.canvas.ground_spec,
            "seed": self.seed,
            "timelapse": self.timelapse,
            "out_dir": str(self.out_dir),
            "look_counter": self._look_counter,
            "stroke_count": self.canvas.stroke_count,
            "texture_strength": self.canvas.texture_strength,
            "rng_state": _encode_rng(self.rng),
            "palette_slots": {k: [float(c) for c in v] for k, v in self.palette.slots.items()},
            "marks": {k: [float(v[0]), float(v[1])] for k, v in self.marks.items()},
            "has_sketch": bool(self.canvas.has_sketch),
            "assisted": list(self.assisted),
        }
        frames = self.history._frames
        # Written through an open handle: np.savez_compressed appends ".npz" to a
        # path that lacks it, which would make `easel new p.easel` write p.easel.npz
        # and every later command fail to find its own session.
        #
        # The canvas tooth and grain are a pure function of (texture, size, seed,
        # strength), so they are rebuilt on load rather than stored.
        #
        # Written to a temp file and swapped into place with os.replace: the
        # `.easel` file is the only copy of the painting, and a crash or a full
        # disk partway through an in-place write would leave a truncated file with
        # no way back. os.replace is atomic on both POSIX and Windows for a
        # destination on the same filesystem, which the temp file always is.
        fd, tmp_name = tempfile.mkstemp(dir=p.parent, prefix=f".{p.name}.", suffix=".tmp")
        try:
            with os.fdopen(fd, "wb") as fh:
                np.savez_compressed(
                    fh,
                    meta=np.array(json.dumps(meta)),
                    log=np.array(self.history.to_json()),
                    rgb=self.canvas.rgb,
                    wetness=self.canvas.wetness,
                    thickness=self.canvas.thickness,
                    # Only when there is one: a graphite channel is the same size
                    # as a colour plane and a painting that never drew should not
                    # carry it.
                    sketch=(self.canvas.sketch if self.canvas.has_sketch
                            else np.zeros((0, 0), dtype=np.float32)),
                    frames=(np.stack(frames) if frames
                            else np.zeros((0, 1, 1, 3), dtype=np.uint8)),
                    last_look=(self._last_look if self._last_look is not None
                               else np.zeros((0, 0, 3), dtype=np.uint8)),
                )
        except BaseException:
            Path(tmp_name).unlink(missing_ok=True)
            raise
        os.replace(tmp_name, p)
        return p

    @classmethod
    def load(cls, path: str | Path) -> Session:
        """Reload a session saved by :meth:`save`."""
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(
                f"No session at {p}. Create one with `easel new` before painting."
            )
        try:
            with np.load(p, allow_pickle=False) as data:
                meta = json.loads(str(data["meta"]))
                if meta.get("format") not in _READABLE_FORMATS:
                    raise ValueError(
                        f"Session file {p} has format {meta.get('format')}, "
                        f"this build of Easel reads {_READABLE_FORMATS} and writes "
                        f"format {_EASEL_FORMAT}."
                    )
                s = cls.__new__(cls)
                s.seed = int(meta["seed"])
                s.rng = _decode_rng(meta["rng_state"])
                s.out_dir = Path(meta["out_dir"])
                s.timelapse = bool(meta["timelapse"])
                s._look_counter = int(meta["look_counter"])
                s.marks = {
                    k: (float(v[0]), float(v[1])) for k, v in meta.get("marks", {}).items()
                }
                s._preparation = None
                s.assisted = [str(a) for a in meta.get("assisted", [])]
                s._index_base = 0

                canvas = Canvas.__new__(Canvas)
                canvas.width = int(meta["width"])
                canvas.height = int(meta["height"])
                canvas.seed = s.seed
                canvas.texture_name = meta["texture"]
                canvas.ground_name = meta["ground"]
                canvas.ground_spec = meta.get("ground_spec", meta["ground"])
                canvas.rgb = data["rgb"].astype(np.float32)
                canvas.wetness = data["wetness"].astype(np.float32)
                canvas.thickness = data["thickness"].astype(np.float32)
                # meta's width/height drive every pixel-coordinate computation from
                # here on (to_px, region_px, stamp's clipping...); if they disagree
                # with what was actually stored -- a hand-edited or corrupted file --
                # trusting meta alone silently paints at the wrong scale or crashes
                # deep inside a stamp() far from this clear a place to say why.
                if canvas.rgb.shape[:2] != (canvas.height, canvas.width):
                    raise ValueError(
                        f"meta says {canvas.width}x{canvas.height}, but the stored "
                        f"canvas array is {canvas.rgb.shape[1]}x{canvas.rgb.shape[0]}."
                    )
                canvas.texture_strength = float(meta.get("texture_strength", 1.0))
                canvas.height_map, canvas.grain = build_surface(
                    canvas.texture_name,
                    canvas.height,
                    canvas.width,
                    s.seed,
                    canvas.texture_strength,
                )
                canvas.tooth_ceiling = tooth_ceiling(canvas.height_map, canvas.grain)
                canvas.stroke_count = int(meta["stroke_count"])
                # Format 1 has no sketch array at all; format 2 stores one only when
                # something was drawn.
                stored = data["sketch"] if "sketch" in data.files else None
                if stored is not None and stored.size:
                    canvas.sketch = stored.astype(np.float32)
                    canvas.has_sketch = True
                else:
                    canvas.sketch = np.zeros((canvas.height, canvas.width), dtype=np.float32)
                    canvas.has_sketch = False
                s.canvas = canvas

                s.palette = Palette()
                for name, rgb in meta.get("palette_slots", {}).items():
                    s.palette[name] = np.array(rgb, dtype=np.float32)

                s.history = History()
                s.history.records = History.records_from_json(str(data["log"]))
                frames = data["frames"]
                s.history._frames = [f for f in frames] if frames.size else []
                last = data["last_look"]
                s._last_look = last if last.size else None
        except (zipfile.BadZipFile, KeyError, TypeError, EOFError, ValueError) as exc:
            # A missing array, an unreadable zip, a log entry with a field this
            # build's StrokeRecord does not know about (a newer Easel wrote it, or
            # the file is simply damaged), a meta or log blob that is not valid
            # JSON, or an rng_state that does not decode -- all of these are "not
            # a valid session file", not a bug in this code, and the CLI already
            # knows how to report that cleanly. ``ValueError`` also covers the
            # deliberate format-mismatch raise just above: wrapping it repeats the
            # same information with one added sentence, not a different one.
            raise ValueError(f"{p} is not a valid Easel session file, or is corrupted: "
                             f"{exc}") from exc
        return s

    # -- replay -----------------------------------------------------------------
    def _stroke_rng(self, index: int) -> np.random.Generator:
        """A generator for one stroke, derived from the seed and the stroke index.

        Seeding per stroke rather than drawing from one running stream is what makes
        replay exact. A stroke's jitter then depends only on which stroke it is, not
        on how much randomness earlier calls happened to consume -- so rebuilding the
        painting from its log reproduces it pixel for pixel.
        """
        return np.random.default_rng([self.seed, index])

    def replay(self, upto: int | None = None) -> Session:
        """Rebuild this painting from its log, optionally stopping after ``upto`` records.

        Returns a **new** session. The whole painting is reproducible from the log
        plus the seed, so this is also how the CLI undoes strokes: session files do
        not carry snapshots, but they do carry the log.
        """
        records = self.history.records if upto is None else self.history.records[:upto]
        fresh = Session(
            self.canvas.width,
            self.canvas.height,
            texture=self.canvas.texture_name,
            ground=self.canvas.ground_spec,
            seed=self.seed,
            timelapse=self.timelapse,
            out_dir=self.out_dir,
            texture_strength=self.canvas.texture_strength,
        )
        for name, rgb in self.palette.slots.items():
            fresh.palette[name] = rgb
        fresh.marks = dict(self.marks)
        fresh.assisted = list(self.assisted)
        # The replayed session shares this one's out_dir, so without carrying
        # these across, its very next look()/preview()/rehearse()/compare() would
        # renumber from 1 and silently overwrite an earlier look_NNN.png this
        # session already wrote -- and ref_shape()/sketch() etc. would raise "No
        # prepared reference yet" even though this session has one.
        fresh._look_counter = self._look_counter
        fresh._last_look = self._last_look
        fresh._preparation = self._preparation

        for record in records:
            if record.kind == "dry":
                fresh.dry(record.params.get("amount", 1.0), _place_from_params(record.params))
                continue
            if record.kind == "pencil":
                fresh.pencil(
                    record.points,
                    pressure=float(record.pressure),
                    width=float(record.params.get("width", 0.0026)),
                    smooth=bool(record.params.get("smooth", True)),
                    note=record.note,
                )
                continue
            if record.kind == "erase":
                fresh.erase(_place_from_params(record.params), note=record.note)
                continue
            params = dict(record.params)
            color = params.pop("color", record.color_hex or "#000000")
            glaze = bool(params.pop("glaze", False))
            smooth = bool(params.pop("smooth", True))
            # Logs written before press existed have no key for it, and one stamp is
            # what they meant: they replay unchanged.
            press = int(params.pop("press", 1))
            fresh.stroke(
                record.points,
                brush=_brush_from_params(params),
                color=np.asarray(color, dtype=np.float32) if isinstance(color, list) else color,
                pressure=record.pressure,
                glaze=glaze,
                smooth=smooth,
                press=press,
                note=record.note,
            )
        return fresh

    def _adopt(self, other: Session) -> None:
        """Take on another session's canvas, history and rng, keeping our own identity."""
        self.canvas = other.canvas
        self.history = other.history
        # `other` is a fresh replay of exactly the kept records, so `other.rng`
        # is already in the state a plain seed + those records would produce --
        # not adopting it left self.rng wherever it happened to be before the
        # undo, so a block_in()/sweep() painted after this fallback path drew
        # its wobble from a stream a real replay would never have produced.
        self.rng = other.rng

    # -- internals --------------------------------------------------------------
    def _resolve_brush(self, brush, size, opacity, overrides: dict) -> Brush:
        b = brush if isinstance(brush, Brush) else get_brush(str(brush))
        changes = dict(overrides)
        if size is not None:
            changes["size"] = float(size)
        if opacity is not None:
            changes["opacity"] = float(opacity)
        return b.with_(**changes) if changes else b

    def _resolve_color(self, color) -> np.ndarray:
        if isinstance(color, str) and not color.startswith("#"):
            return self.palette[color]
        return parse_color(color)

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return (
            f"Session({self.canvas.width}x{self.canvas.height}, seed={self.seed}, "
            f"strokes={self.stroke_count})"
        )


# --------------------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------------------
def _pass_step(size: float, density: float) -> float:
    """One part-brush: how far apart ``block_in`` and ``sweep`` put their passes.

    The same number in both, and now in one place, because ``preview`` has to work
    out the ground a sweep would cover without laying it.
    """
    return max(size * (1.0 - 0.45 * float(np.clip(density, 0.05, 2.0))), 0.004)


def _sweep_cover(edge, size: float, density: float, depth: float, into,
                 closed) -> list[tuple[float, float]]:
    """The outline of the ground a sweep would cover: its edge, and the edge a depth in.

    What ``preview`` draws for a sweep, so the question it answers for a block-in --
    *where would this mass land* -- gets answered for the other way of laying one.
    """
    spine, ring = _sweep_spine(edge, closed, max(_pass_step(size, density) * 0.6, 0.008))
    far = spine + _sweep_normals(spine, into, ring) * float(depth)
    ring_points = np.vstack([spine, far[::-1], spine[:1]])
    return [(float(x), float(y)) for x, y in ring_points]


def _pass_directions(direction) -> list:
    """One entry per pass: the names as before, plus angles and sequences of either.

    ``"cross"`` stays two named passes. A number is one pass at that angle, and a
    sequence is one pass each -- so a cross at an angle is ``(30, 120)``, which is
    what a mass wants when its own axis is not the canvas's.
    """
    if isinstance(direction, str):
        return ["horizontal", "vertical"] if direction == "cross" else [direction]
    if isinstance(direction, (int, float)):
        return [float(direction)]
    passes: list = []
    for item in direction:
        passes.extend(_pass_directions(item))
    if not passes:
        raise ValueError("block_in(direction=...) was given an empty sequence")
    return passes


#: The named directions as angles, for the shaped sweep. The rectangle branches
#: keep their own hand-written geometry so that every painting made before shapes
#: existed replays byte for byte; these are the same lines, as numbers.
_NAMED_ANGLES = {"horizontal": 0.0, "vertical": 90.0, "diagonal": -45.0}


def _angle_of(direction) -> float:
    """A direction as degrees, whether it arrived as a name or a number."""
    if isinstance(direction, str):
        if direction not in _NAMED_ANGLES:
            raise ValueError(
                f"Unknown direction {direction!r}. Use 'horizontal', 'vertical', "
                f"'diagonal', 'cross', 'axis', or a number of degrees."
            )
        return _NAMED_ANGLES[direction]
    return float(direction)


def _spans_inside(poly: Polygon, origin, d) -> list[tuple[float, float]]:
    """Where the line through ``origin`` along ``d`` runs inside the shape.

    As parameter intervals along ``d``, in order. Even-odd: crossing an edge swaps
    inside for outside, so the sorted crossings pair up into spans. A vertex sitting
    exactly on the line counts once (the ``> 0`` test is half-open), which is what
    stops a pass through a corner from swallowing the rest of the shape.
    """
    ox, oy = origin
    dx, dy = d
    nx, ny = -dy, dx
    ts: list[float] = []
    pts = poly.points
    for (ax, ay), (bx, by) in zip(pts, [*pts[1:], pts[0]], strict=True):
        sa = (ax - ox) * nx + (ay - oy) * ny
        sb = (bx - ox) * nx + (by - oy) * ny
        if (sa > 0.0) == (sb > 0.0):
            continue
        u = sa / (sa - sb)
        px, py = ax + (bx - ax) * u, ay + (by - ay) * u
        ts.append((px - ox) * dx + (py - oy) * dy)
    ts.sort()
    return [(ts[i], ts[i + 1]) for i in range(0, len(ts) - 1, 2)]


def _place_params(place) -> dict:
    """A region or a shape as something the log can hold and :meth:`replay` rebuild."""
    if place is None:
        return {"region": None}
    if isinstance(place, Polygon):
        return {"region": None, "shape": [[float(x), float(y)] for x, y in place.points],
                "shape_name": place.name}
    return {"region": list(place.bounds)}


def _place_from_params(params: dict):
    """The other direction: what ``dry`` and ``erase`` were given, out of the log."""
    pts = params.get("shape")
    if pts:
        return Polygon(tuple((float(x), float(y)) for x, y in pts),
                       name=str(params.get("shape_name", "")))
    return params.get("region")


def _canvas_point(x: float, y: float) -> tuple[float, float]:
    """A point clamped to the canvas, the way the named block-in branches clamp."""
    return (float(np.clip(x, 0.0, 1.0)), float(np.clip(y, 0.0, 1.0)))


#: The deepest a sweep will go. The canvas is one unit across and an edge may run a
#: little off it, so anything past this is a depth given in pixels by mistake -- and
#: a sweep lays a pass per part-brush, with nothing else to bound the count.
_MAX_SWEEP_DEPTH = 2.0

#: What the words ``into=`` accepts mean, in degrees clockwise from the horizontal --
#: the same convention as ``block_in(direction=)``, and y runs down the canvas.
_INTO_WORDS = {"right": 0.0, "down": 90.0, "left": 180.0, "up": -90.0}


def _arc_length(points: np.ndarray) -> np.ndarray:
    """Cumulative distance along a polyline, one entry per point."""
    d = np.diff(points, axis=0)
    return np.concatenate([[0.0], np.cumsum(np.hypot(d[:, 0], d[:, 1]))])


def _sweep_spine(edge, closed, spacing: float) -> tuple[np.ndarray, bool]:
    """The boundary a sweep follows: smoothed, then resampled at even arc length.

    Smoothed first because that is the curve the strokes will actually paint -- a
    stroke fits a spline through its points, so offsetting the raw corners would
    step the passes off the painted edge. Even spacing is what lets the offset be
    measured in one part-brush and the cross passes be laid in the mass's own
    coordinates rather than the canvas's.

    Returns the spine and whether the edge is a loop. A loop's spine repeats its
    first point at the end, so interpolating along it wraps.
    """
    try:
        pts = np.asarray(edge, dtype=np.float64)
    except (TypeError, ValueError) as exc:
        raise ValueError(
            "sweep(edge=...) wants a list of (x, y) points along the boundary, "
            "like [(0.2, 0.7), (0.45, 0.52), (0.8, 0.6)]."
        ) from exc
    if pts.ndim != 2 or pts.shape[1] != 2 or len(pts) < 2:
        raise ValueError(
            f"sweep(edge=...) wants at least two (x, y) points along the boundary; "
            f"got an array of shape {pts.shape}."
        )
    if not np.isfinite(pts).all():
        raise ValueError("sweep(edge=...) has a point that is not a finite number.")
    if float(np.abs(pts - pts[0]).max()) < 1e-9:
        raise ValueError("sweep(edge=...) has no length: every point is the same place.")

    repeats_first = bool(np.allclose(pts[0], pts[-1], atol=1e-9))
    ring = repeats_first if closed is None else bool(closed)
    if ring:
        if repeats_first:
            pts = pts[:-1]
        if len(pts) < 3:
            raise ValueError(
                "A closed edge wants at least three points; two make a line, not a shape."
            )
        pts = np.vstack([pts, pts[:1]])

    dense = catmull_rom(pts.astype(np.float32), samples_per_segment=12).astype(np.float64)
    cum = _arc_length(dense)
    total = float(cum[-1])
    if total < 1e-9:
        raise ValueError("sweep(edge=...) has no length: every point is the same place.")

    # Enough points to follow the curve, few enough that a long edge stays quick.
    count = int(np.clip(round(total / max(spacing, 1e-4)) + 1, 4, 96))
    at = np.linspace(0.0, total, count)
    spine = np.stack(
        [np.interp(at, cum, dense[:, 0]), np.interp(at, cum, dense[:, 1])], axis=1
    )
    return spine, ring


def _sweep_normals(spine: np.ndarray, into, ring: bool) -> np.ndarray:
    """Unit vectors pointing into the mass, one per spine point.

    A fixed ``into`` gives every pass the same direction, which is the hand working
    down a near-horizontal edge and is what the recipe this replaces did. A point
    inside the mass, or a closed edge, gives each point the boundary's own inward
    normal instead, so the passes stay parallel to a curve rather than shearing off
    it. The side is chosen once for the whole edge, not per point: a normal that
    flips halfway along would fold the pass back on itself.
    """
    if ring:
        core = spine[:-1]
        tang = np.roll(core, -1, axis=0) - np.roll(core, 1, axis=0)
        tang = np.vstack([tang, tang[:1]])
    else:
        tang = np.gradient(spine, axis=0)
    mag = np.hypot(tang[:, 0], tang[:, 1])
    mag[mag < 1e-12] = 1.0
    tang = tang / mag[:, None]
    perp = np.stack([-tang[:, 1], tang[:, 0]], axis=1)

    if isinstance(into, str):
        try:
            degrees = _INTO_WORDS[into]
        except KeyError:
            raise ValueError(
                f"sweep(into={into!r}) is which side of the edge the mass is on. "
                f"Use {', '.join(sorted(_INTO_WORDS))}, a number of degrees "
                f"clockwise from the horizontal, or a point inside the mass."
            ) from None
        return _fixed_normals(len(spine), degrees)
    if isinstance(into, (int, float, np.floating, np.integer)) and not isinstance(into, bool):
        if not math.isfinite(float(into)):
            raise ValueError("sweep(into=...) is not a finite angle.")
        return _fixed_normals(len(spine), float(into))
    if into is None:
        if not ring:
            raise ValueError(
                "sweep() cannot tell which side of an open edge the mass is on. Say "
                "so: into='down' (or 'up', 'left', 'right', or a number of degrees "
                "clockwise from the horizontal), or into=(x, y) for a point inside "
                "the mass. A closed boundary needs neither -- pass closed=True."
            )
        # Shoelace: positive area means the interior lies to the left of travel.
        area = 0.5 * float(
            np.sum(spine[:-1, 0] * spine[1:, 1] - spine[1:, 0] * spine[:-1, 1])
        )
        return perp if area > 0.0 else -perp

    target = np.asarray(into, dtype=np.float64)
    if target.shape != (2,) or not np.isfinite(target).all():
        raise ValueError(
            f"sweep(into={into!r}) wants a compass word, a number of degrees, or one "
            f"(x, y) point inside the mass."
        )
    facing = float(np.sum((target - spine) * perp))
    return perp if facing >= 0.0 else -perp


def _fixed_normals(count: int, degrees: float) -> np.ndarray:
    theta = math.radians(degrees)
    return np.repeat(np.array([[math.cos(theta), math.sin(theta)]]), count, axis=0)


def _drop_folds(path: np.ndarray, spine: np.ndarray, step: float) -> np.ndarray | None:
    """Take the folds out of an offset pass, and drop it entirely if it collapsed.

    Offsetting a curve inward eventually runs it past its own centre, where the
    passes cross themselves and scribble. A point that travels *backwards* along
    the boundary relative to the last one kept is on the far side of such a fold,
    so it goes. Returns ``None`` when what is left is too short to be a mark, which
    is how a sweep deeper than its own mass stops instead of scribbling.
    """
    keep = [0]
    for i in range(1, len(path)):
        j = keep[-1]
        forward = float(np.dot(path[i] - path[j], spine[i] - spine[j]))
        if forward > 0.0:
            keep.append(i)
    if len(keep) < 2:
        return None
    out = path[keep]
    d = np.diff(out, axis=0)
    if float(np.hypot(d[:, 0], d[:, 1]).sum()) < step * 0.5:
        return None
    return out


def _band_points(spine, normals, cum, us: np.ndarray, vs: np.ndarray) -> np.ndarray:
    """Points given in the mass's own coordinates: ``us`` along the edge, ``vs`` into it."""
    x = np.interp(us, cum, spine[:, 0])
    y = np.interp(us, cum, spine[:, 1])
    nx = np.interp(us, cum, normals[:, 0])
    ny = np.interp(us, cum, normals[:, 1])
    mag = np.hypot(nx, ny)
    mag[mag < 1e-12] = 1.0
    return np.stack([x + vs * nx / mag, y + vs * ny / mag], axis=1)


def _cross_lines(length: float, depth: float, step: float, degrees: float, spacing: float):
    """The second set of passes, as (along, into) coordinates in the swept band.

    A straight line in the band's own coordinates is a pass that follows the form
    and still crosses the first set at ``degrees``, which is what closes up the
    stringing a single sweep leaves. Clipped to the band, so the silhouette the
    first pass laid stays where it is.
    """
    lean = math.tan(math.radians(degrees))
    apart = step / math.cos(math.radians(degrees))
    lo = min(0.0, -lean * length)
    hi = max(depth, depth - lean * length)
    count = max(1, int(round((hi - lo) / apart)))
    for i in range(count):
        start = lo + (i + 0.5) * (hi - lo) / count
        ends = ((0.0 - start) / lean, (depth - start) / lean)
        u0 = max(0.0, min(ends))
        u1 = min(length, max(ends))
        if u1 - u0 <= max(step, 1e-4) * 0.5:
            continue                      # this line only clips a corner of the band
        points = max(3, int(round((u1 - u0) / max(spacing, 1e-4))) + 1)
        us = np.linspace(u0, u1, points)
        yield us, np.clip(start + lean * us, 0.0, depth)

def _segment_inside(p, q, bounds) -> tuple[float, float] | None:
    """The stretch of the segment ``p``-``q`` that lies inside ``bounds``.

    Returned as the parameter interval ``(t0, t1)`` along the segment, or ``None``
    when no part of it is inside. Liang-Barsky, written out: the segment is clipped
    against each slab in turn and the surviving interval is their intersection.
    """
    x0, y0, x1, y1 = bounds
    t0, t1 = 0.0, 1.0
    for delta, lo, hi, start in (
        (q[0] - p[0], x0, x1, p[0]),
        (q[1] - p[1], y0, y1, p[1]),
    ):
        if abs(delta) < 1e-12:
            if start < lo or start > hi:
                return None                    # parallel to the slab and outside it
            continue
        a, b = (lo - start) / delta, (hi - start) / delta
        if a > b:
            a, b = b, a
        t0, t1 = max(t0, a), min(t1, b)
        if t0 > t1:
            return None
    return (t0, t1)


def _erase_from_lines(lines, place) -> list[list[tuple[float, float]]]:
    """Every part of every line that is *outside* the erased place.

    A line wholly inside disappears, a line wholly outside is untouched, and a line
    that crosses comes back as the one or two pieces left over. Anything reduced to
    a single point is dropped: a stroke cannot be aimed along it.
    """
    if isinstance(place, Polygon):
        return _erase_from_lines_shape(lines, place)
    kept: list[list[tuple[float, float]]] = []
    bounds = tuple(place.bounds if isinstance(place, Region) else place)
    x0, y0, x1, y1 = bounds
    for line in lines:
        if len(line) < 2:
            if line and not (x0 <= line[0][0] <= x1 and y0 <= line[0][1] <= y1):
                kept.append(list(line))
            continue
        run: list[tuple[float, float]] = []
        for p, q in zip(line, line[1:], strict=False):
            inside = _segment_inside(p, q, bounds)
            if inside is None:
                if not run:
                    run.append(p)
                run.append(q)
                continue
            t0, t1 = inside
            if t0 > 1e-9:                      # the piece before the region survives
                if not run:
                    run.append(p)
                run.append(_lerp(p, q, t0))
            if len(run) >= 2:
                kept.append(run)
            run = [_lerp(p, q, t1), q] if t1 < 1.0 - 1e-9 else []
        if len(run) >= 2:
            kept.append(run)
    return kept


def _erase_from_lines_shape(lines, poly: Polygon) -> list[list[tuple[float, float]]]:
    """The same, against a shape: cut each segment at every crossing of the outline.

    The rectangle above is clipped analytically against four sides. A shape has as
    many sides as it has points, so a segment is split at every crossing and the
    pieces whose middle is outside the shape are the ones that survive.
    """
    kept: list[list[tuple[float, float]]] = []
    for line in lines:
        if len(line) < 2:
            if line and not poly.contains(*line[0]):
                kept.append(list(line))
            continue
        run: list[tuple[float, float]] = []
        for p, q in zip(line, line[1:], strict=False):
            cuts = [0.0, *_crossings(p, q, poly), 1.0]
            for t0, t1 in zip(cuts, cuts[1:], strict=False):
                if t1 - t0 < 1e-9:
                    continue
                if poly.contains(*_lerp(p, q, (t0 + t1) * 0.5)):
                    if len(run) >= 2:
                        kept.append(run)
                    run = []
                    continue
                if not run:
                    run.append(_lerp(p, q, t0))
                run.append(_lerp(p, q, t1))
        if len(run) >= 2:
            kept.append(run)
    return kept


def _crossings(p, q, poly: Polygon) -> list[float]:
    """Where the segment ``p``-``q`` crosses the shape's outline, along the segment."""
    rx, ry = q[0] - p[0], q[1] - p[1]
    out: list[float] = []
    pts = poly.points
    for (ax, ay), (bx, by) in zip(pts, [*pts[1:], pts[0]], strict=True):
        sx, sy = bx - ax, by - ay
        denom = rx * sy - ry * sx
        if abs(denom) < 1e-15:
            continue                            # parallel: no single crossing point
        t = ((ax - p[0]) * sy - (ay - p[1]) * sx) / denom
        u = ((ax - p[0]) * ry - (ay - p[1]) * rx) / denom
        if 1e-9 < t < 1.0 - 1e-9 and -1e-9 <= u <= 1.0 + 1e-9:
            out.append(t)
    return sorted(out)


def _lerp(p, q, t: float) -> tuple[float, float]:
    return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)


def _is_path(value) -> bool:
    """True when ``value`` is a single list of points rather than a list of strokes.

    ``preview([(0.1, 0.2), (0.4, 0.5)])`` means one stroke, and
    ``preview([[(0.1, 0.2), (0.4, 0.5)]])`` means a list holding one. Both are
    natural to write, so both are accepted, and this is what tells them apart.
    """
    try:
        entries = list(value)
    except TypeError:
        return False
    if not entries or isinstance(entries[0], dict):
        return False
    for entry in entries:
        try:
            pair = list(entry)
        except TypeError:
            return False
        if len(pair) != 2 or not all(isinstance(v, (int, float, np.floating, np.integer))
                                     for v in pair):
            return False
    return True


def _grey(rgb8: np.ndarray) -> Image.Image:
    """An 8-bit RGB array as the greyscale the painter sees, for the comparison sheet."""
    from easel.color import linear_to_srgb, luminance, srgb_to_linear

    srgb = np.asarray(rgb8, dtype=np.float32) / 255.0
    lum = linear_to_srgb(luminance(srgb_to_linear(srgb)))
    grey = (lum * 255.0 + 0.5).astype(np.uint8)
    return Image.fromarray(np.repeat(grey[:, :, None], 3, axis=2), mode="RGB")


def _plain(value):
    if isinstance(value, np.ndarray):
        return [float(v) for v in value]
    if isinstance(value, (list, tuple)):
        return [float(v) for v in value]
    return float(value)


def _brush_params(b: Brush, color: np.ndarray, **extra) -> dict:
    """Everything needed to reproduce this mark: the whole brush and the exact colour.

    The colour is stored as linear floats rather than as the hex string, because hex
    is 8-bit sRGB and a replay built from it would not match the original pixel for
    pixel.
    """
    d = {k: v for k, v in asdict(b).items() if k != "meta"}
    d["color"] = [float(v) for v in color]
    d.update(extra)
    return d


def _brush_from_params(params: dict) -> Brush:
    fields = {f.name for f in dataclass_fields(Brush)} - {"meta"}
    return Brush(**{k: v for k, v in params.items() if k in fields})


def _encode_rng(rng: np.random.Generator) -> dict:
    state = rng.bit_generator.state
    return json.loads(json.dumps(state, default=str))


def _decode_rng(state: dict) -> np.random.Generator:
    # Deliberately not wrapped in a try/except: a malformed rng_state used to be
    # swallowed here and silently replaced with an OS-entropy-seeded generator, so
    # two loads of the same file painted differently from that point on with no
    # error at all. Letting KeyError/TypeError/ValueError propagate means
    # Session.load()'s own except clause turns this into the same clear
    # "is not a valid Easel session file" message every other corruption gets.
    gen = np.random.default_rng()
    s = dict(state)
    inner = dict(s.get("state", {}))
    for key in ("state", "inc"):
        if key in inner:
            inner[key] = int(inner[key])
    s["state"] = inner
    if "has_uint32" in s:
        s["has_uint32"] = int(s["has_uint32"])
    if "uinteger" in s:
        s["uinteger"] = int(s["uinteger"])
    gen.bit_generator.state = s
    return gen
