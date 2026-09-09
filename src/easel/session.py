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
from easel.regions import Region, as_region
from easel.stroke import draw_pencil, paint_stroke

__all__ = ["Session"]

#: Bumped to 2 by M6: sessions now carry a graphite channel and named landmarks.
#: Format 1 files still load -- they simply have neither.
_EASEL_FORMAT = 2
_READABLE_FORMATS = (1, 2)
#: Stream label for a rehearsal's generator, so it cannot collide with the real one.
_REHEARSAL_STREAM = 918273645


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
            note: a line recorded in the log, for the painter's own benefit.
            **brush_overrides: any other :class:`~easel.brush.Brush` field.

        Returns:
            The :class:`~easel.history.StrokeRecord` that was logged.
        """
        b = self._resolve_brush(brush, size, opacity, brush_overrides)
        col = self._resolve_color(color)

        # Snapshot before the mark, so undo lands on the state before this stroke.
        self.history.push_snapshot(self.canvas.snapshot())

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
                params=_brush_params(b, col, glaze=glaze, smooth=smooth),
            )
        )
        if self.timelapse:
            self.history.add_frame(self.canvas.thumbnail_srgb8())
        return record

    def dab(self, x: float, y: float, brush="round_hard", color="burnt_umber", **kw):
        """A single mark at one point. Convenience for accents and highlights."""
        return self.stroke([(x, y)], brush=brush, color=color, **kw)

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
        overhang: float = 0.35,
        note: str = "",
        **brush_overrides,
    ) -> list[StrokeRecord]:
        """Fill a region with overlapping strokes, the way a painter blocks in a mass.

        This emits real strokes, not a fill: the brushwork stays visible, the edges
        stay ragged, and the paint runs out along each pass. That is the point --
        a flat fill is the single clearest tell that an image was not painted.

        Args:
            region: a name, a :class:`~easel.regions.Region`, or a 4-tuple.
            brush: preset name or brush.
            color: the colour to lay in.
            direction: ``"horizontal"``, ``"vertical"``, ``"diagonal"`` or
                ``"cross"``; a number of degrees, clockwise from the horizontal, to
                sweep the mass along its own form rather than along the canvas; or a
                sequence of any of those for one pass each. Vary this between passes
                so the marks are not parallel -- and prefer the angle the *subject*
                runs at. A hillside swept at its own angle stops being a stack of
                horizontal bars, which is the single loudest tell that nobody chose
                the direction.
            density: 1.0 covers the region; below 1 leaves the ground showing
                through, which is usually what you want for a first pass.
            pressure: pressure profile for each pass.
            size: brush size override.
            overhang: how far each pass runs past the region edge, as a fraction of
                the brush width. Some overhang keeps the block from looking cropped.
            note: recorded in the log.

        Returns:
            The records for every stroke laid down.
        """
        r = as_region(region)
        b = self._resolve_brush(brush, size, None, brush_overrides)

        band = max(b.size * (1.0 - 0.45 * float(np.clip(density, 0.05, 2.0))), 0.004)
        records: list[StrokeRecord] = []

        for pass_dir in _pass_directions(direction):
            for path in self._block_paths(r, pass_dir, band, b.size * overhang):
                records.append(
                    self.stroke(
                        path,
                        brush=b,
                        color=color,
                        pressure=pressure,
                        note=note or f"block-in {r.name or 'region'} {pass_dir}",
                    )
                )
        return records

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
        if self.timelapse:
            self.history.add_frame(self.canvas.thumbnail_srgb8())
        return record

    def erase(self, region=None, note: str = "") -> StrokeRecord:
        """Rub out the drawing, all of it or inside one region.

        Erase before painting rather than arguing with a line while painting. A line
        the painter has decided is wrong costs nothing to remove and costs a great
        deal to paint around.
        """
        r = as_region(region) if region is not None else None
        self.history.push_snapshot(self.canvas.snapshot())
        self.canvas.erase_sketch(r)
        return self.history.add(
            StrokeRecord(
                index=self._index_base + len(self.history.records),
                kind="erase",
                note=note or ("erase" + (f" {r}" if r is not None else " all")),
                params={"region": list(r.bounds) if r is not None else None},
            )
        )

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
                bounds = r.params.get("region")
                lines = [] if bounds is None else _erase_from_lines(lines, bounds)
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
        """Dry the canvas so the next paint covers instead of mixing."""
        r = as_region(region) if region is not None else None
        # Snapshot before the mark, like every other canvas-mutating call: without
        # this, undo() after a dry() pops the *previous* paint action's snapshot
        # while only dropping the dry record, desyncing the canvas from the log.
        self.history.push_snapshot(self.canvas.snapshot())
        self.canvas.dry(amount, r)
        return self.history.add(
            StrokeRecord(
                index=self._index_base + len(self.history.records),
                kind="dry",
                note=f"dry {amount:.2f}" + (f" in {r}" if r is not None else ""),
                params={"amount": float(amount),
                        "region": list(r.bounds) if r is not None else None},
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
            snap = self.history.pop_snapshots(n)
            if snap is not None:
                self.canvas.restore(snap)
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

        current = self.canvas.to_srgb8(impasto=impasto)
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
        self._last_look = self.canvas.to_srgb8(impasto=kwargs.get("impasto", True))
        return img

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
                ``brush``, ``size``, ``note``...). A single path is also accepted.
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
        """
        specs = self._stroke_specs(strokes)
        ref_img = None if reference is None else load_reference(reference)
        img = render_look(
            self.canvas,
            scale=scale,
            grid=grid,
            values=values,
            region=region,
            reference=ref_img,
            marks=self.marks or None,
            strokes=[self._preview_shape(spec, i) for i, spec in enumerate(specs)],
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

        The trial strokes are seeded as if they were the next strokes of the real
        painting, so what is rehearsed is what lands when it is painted for real.

        Args:
            strokes: as :meth:`preview`.
            reference: shown alongside, cropped to the same place.
            region: crop both panels, enlarged. Use one -- the point is feature scale.
            grid: as :meth:`look`.
            values: greyscale.
            path: where to write. Defaults to ``out_dir/rehearse_NNN.png``.
            scale: long-side pixel limit.
        """
        trial = self._trial_session()
        for spec in self._stroke_specs(strokes):
            kwargs = {k: v for k, v in spec.items() if k != "label"}
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

    def _trial_session(self) -> Session:
        """A throwaway session sharing this one's surface, palette and seeding.

        The canvas channels are copied and the tooth is shared, so a rehearsal costs
        a few small arrays rather than a whole canvas. It gets its *own* generator,
        seeded from this session's current state, because a rehearsal that consumed
        the real session's random stream would change the painting that follows it.
        """
        trial = Session.__new__(Session)
        trial.seed = self.seed
        # Its own stream, derived from the seed and how far along the painting is.
        # Only block_in draws from this one, and a rehearsal that consumed the real
        # session's stream would quietly change every stroke painted after it.
        trial.rng = np.random.default_rng([self.seed, _REHEARSAL_STREAM,
                                           len(self.history.records)])
        trial.canvas = self.canvas.trial_copy()
        trial.palette = self.palette
        trial.history = History()
        trial.out_dir = self.out_dir
        trial.timelapse = False
        trial._look_counter = 0
        trial._last_look = None
        trial.marks = self.marks
        trial._preparation = self._preparation
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

    def _preview_shape(self, spec: dict, index: int) -> dict:
        """What the overlay needs: the path, the brush's width, and a label."""
        b = self._resolve_brush(
            spec.get("brush", "bristle"), spec.get("size"), spec.get("opacity"),
            {k: v for k, v in spec.items()
             if k not in ("points", "brush", "size", "opacity", "color", "pressure",
                          "glaze", "smooth", "note", "label")},
        )
        return {"points": spec["points"], "width": b.size,
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
        as ``unreachable`` rather than as work: the box has no black in it, and a
        lamp-lit photograph has cells no mixture here can reach. Read ``fixable``
        for the list worth strokes.
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

    def log(self, last: int = 10) -> str:
        """A short text summary of recent marks."""
        return self.history.summary(last)

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
        except (zipfile.BadZipFile, KeyError, TypeError, EOFError) as exc:
            # A missing array, an unreadable zip, or a log entry with a field this
            # build's StrokeRecord does not know about (a newer Easel wrote it, or
            # the file is simply damaged) -- all of these are "not a valid session
            # file", not a bug in this code, and the CLI already knows how to
            # report that cleanly.
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

        for record in records:
            if record.kind == "dry":
                fresh.dry(record.params.get("amount", 1.0), record.params.get("region"))
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
                fresh.erase(record.params.get("region"), note=record.note)
                continue
            params = dict(record.params)
            color = params.pop("color", record.color_hex or "#000000")
            glaze = bool(params.pop("glaze", False))
            smooth = bool(params.pop("smooth", True))
            fresh.stroke(
                record.points,
                brush=_brush_from_params(params),
                color=np.asarray(color, dtype=np.float32) if isinstance(color, list) else color,
                pressure=record.pressure,
                glaze=glaze,
                smooth=smooth,
                note=record.note,
            )
        return fresh

    def _adopt(self, other: Session) -> None:
        """Take on another session's canvas and history, keeping our own identity."""
        self.canvas = other.canvas
        self.history = other.history

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


def _canvas_point(x: float, y: float) -> tuple[float, float]:
    """A point clamped to the canvas, the way the named block-in branches clamp."""
    return (float(np.clip(x, 0.0, 1.0)), float(np.clip(y, 0.0, 1.0)))


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


def _erase_from_lines(lines, bounds) -> list[list[tuple[float, float]]]:
    """Every part of every line that is *outside* ``bounds``.

    A line wholly inside disappears, a line wholly outside is untouched, and a line
    that crosses comes back as the one or two pieces left over. Anything reduced to
    a single point is dropped: a stroke cannot be aimed along it.
    """
    kept: list[list[tuple[float, float]]] = []
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
    gen = np.random.default_rng()
    try:
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
    except Exception:  # pragma: no cover - defensive, keeps a load from failing hard
        pass
    return gen
