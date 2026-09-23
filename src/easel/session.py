"""The painting session: the one object a painter holds.

A session ties together a canvas, a palette, a seed and a history. Everything the
painter does goes through it, so every mark is logged and the whole painting stays
reproducible from the seed.

The session owns the random generator. That is what makes the determinism promise
real: the same script with the same seed produces the same PNG, because every
jittered dab in every stroke is drawn from this one stream in the same order.
"""

from __future__ import annotations

import inspect
import json
import math
import os
import tempfile
import warnings
import zipfile
from contextlib import contextmanager
from dataclasses import asdict
from dataclasses import fields as dataclass_fields
from difflib import get_close_matches
from pathlib import Path
from typing import NamedTuple

import numpy as np
from PIL import Image

from easel import checklist
from easel.brush import Brush
from easel.brush import brush as get_brush
from easel.canvas import Canvas, build_surface, tooth_ceiling
from easel.color import (
    linear_to_oklab,
    linear_to_srgb,
    luminance,
    parse_color,
    srgb_to_linear,
)
from easel.history import DEFAULT_FRAME_PX, History, StrokeRecord
from easel.look import (
    DEFAULT_LOOK_SIZE,
    label_sheet,
    load_reference,
    render_look,
    save_look,
)
from easel.measure import (
    VALUE_THRESHOLD,
    Comparison,
    compare_images,
    compare_plan,
    heat_sheet,
    plan_sheet,
)
from easel.notices import NOTICES, EaselWarning, Notice, PassReport, rebuild_moves, version_key
from easel.notices import explain as notice_text
from easel.palette import Palette
from easel.plan import Plan
from easel.plan import build as build_plan
from easel.plan import planned as planned_place
from easel.prepare import Preparation, prepare_reference
from easel.regions import (
    Polygon,
    Region,
    _looks_like_bounds,
    _looks_like_point,
    as_place,
    as_region,
    blob,
    ellipse,
    polygon,
)
from easel.stroke import (
    catmull_rom,
    draw_pencil,
    paint_stroke,
    press_width,
    pressure_curve,
)

__all__ = ["Session"]

#: Bumped to 2 by M6: sessions now carry a graphite channel and named landmarks.
#: Bumped to 3 by M8: and a note of which assisted modes the painting has used.
#: Bumped to 4: and a stroke budget, so the split a painter writes down survives
#: being closed and reopened between ``easel run`` calls.
#: Format 1, 2 and 3 files still load -- they simply have less in them.
#: Since 0.2.0 every record also carries the generator's state at the start of the
#: call that made it (``params["rng"]``), which is what lets ``undo`` and ``replay``
#: put the stream back where the painting's was. Not a bump: an older build reads the
#: extra key without noticing it, and a log written without it still loads here --
#: it simply cannot have its stream restored, and ``undo`` says so.
_EASEL_FORMAT = 4
_READABLE_FORMATS = (1, 2, 3, 4)

#: The width of a smudge, as a fraction of the canvas long side, when the painter
#: does not name one. The knee of the measured curve in :meth:`Session.smudge`: the
#: softening a single pass buys has arrived by here and stops improving, while the
#: distance the pass carries the lighter mass into the darker goes on growing with
#: the brush. It was ``0.07`` through 0.1.x, which is four times this and off the
#: top of that table.
SMUDGE_SIZE = 0.020

#: Past this a smudge says what it will look like. ``0.03`` is where the reach of a
#: single pass passes ``1.8%`` of canvas height while the join is no softer than it
#: was at ``0.02`` -- a lobe bought for nothing.
SMUDGE_MAX = 0.030

#: A film's strength when the painter names neither an opacity nor a value to reach.
GLAZE_OPACITY = 0.18

#: How far off the target a solved film may land before the search stops looking.
#: A value plan is written to the hundredth and read against a ``0.10`` threshold,
#: so a fifth of a hundredth is already past the precision the number is used at;
#: what this really buys is an early exit, and the search usually takes it.
_GLAZE_VALUE_TOL = 0.002

#: How many films :meth:`Session._glaze_opacity` may lay on a trial canvas. Halving
#: the opacity bracket each time, twelve is a thousandth of the range; with the
#: tolerance above the search has normally stopped by seven or eight.
_GLAZE_SOLVE_STEPS = 12

#: How far a pixel's linear colour has to move before it counts as under the film.
#: Measured against a probe at full strength, so this is only separating paint from
#: arithmetic noise, not weak films from strong ones.
_GLAZE_FOOTPRINT = 1e-4

#: Under this, a solved film is a stroke that changes nothing and says so. From the
#: measured table, ``0.05`` moves a value ``0.028``, so this is about a hundredth --
#: the precision a value plan is written to, and the point below which a painter is
#: paying a mark for a film nobody can see.
_GLAZE_MIN_OPACITY = 0.02

#: The standard deviation of value inside a sampled place, above which its mean is
#: not a colour that is anywhere in it. Measured over 226 rectangles -- every cell and
#: every 2x2 span -- on two finished paintings rebuilt from their own passes: of the
#: rectangles whose mean misses the value of their own dominant mass by more than
#: ``0.03``, **every one** has a spread at or above this, and it fires on a quarter of
#: the rectangles that are within it. The span that raised the rule, ``span("C3","D4")``
#: across a hand on a table, measures ``0.110`` against ``0.011`` for a clear cell of
#: the same table. **It is deliberately not asked of a shape**: a mass with a turn in
#: it is spread by design -- the same painting's two hands measure ``0.093`` and
#: ``0.100`` handed whole -- and a shape is the remedy this warning names.
_SAMPLE_SPREAD = 0.06

#: Below this share of the place, the lighter or darker part of it is an incident --
#: a glint, a bean, a signature -- rather than a second mass, and it moves the mean by
#: less than the spread suggests.
_SAMPLE_MINOR_SHARE = 0.10

#: How close two planned places count as touching, as a fraction of the canvas long
#: side, when the painter names no number. Half the narrower brush is what the rule
#: wants and a value plan carries no brushes -- the keys are places and the values
#: are values -- so this stands in for one: ``0.01`` is half of a fine brush at
#: ``0.02``, and a painter who knows the two brushes passes ``near=`` instead.
_PLAN_TOUCH = 0.01


class Session:
    """A painting in progress.

    Args:
        width: canvas width in pixels.
        height: canvas height in pixels.
        texture: ``"smooth"``, ``"linen"`` or ``"rough"``.
        ground: a named ground, a hex colour, or an (r, g, b) tuple.
        seed: the determinism seed. The same seed and the same calls give the same
            painting, down to the pixel.
        timelapse: record a frame after every mark. The human watching gets to see
            the painting happen. **A number is the frame's long side in pixels**
            (the default is 360), which used to be unreachable: a 1440x960 painting
            had a 360x240 time-lapse and no argument anywhere could say otherwise. A
            frame is the dearest thing a mark does that is not paint -- 60 ms at
            1440x960 against 6 for the undo snapshot -- so the size is worth
            choosing, and ``timelapse_gif(from_log=True)`` rebuilds one at any size
            afterwards, from a painting that has no frames at all. **The frames are
            kept in memory, not in the** ``.easel`` **file**: a session loaded from
            one records none and rebuilds its film from the log at this size when
            it is asked for (:meth:`timelapse_gif`).
        out_dir: where ``look()`` writes its PNGs.
        budget: how many strokes this painting is allowed, if you want the engine to
            hold the number. A painter is told to write the split down before
            starting; this is where it gets written. Nothing is refused when it runs
            out -- the budget is a plan, not a lock -- but :meth:`cost` says when a
            call would eat a large share of what is left, and ``easel run`` prints
            spent and remaining after every pass.

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
        timelapse: bool | int = True,
        out_dir: str | Path = "out",
        texture_strength: float = 1.0,
        budget: int | None = None,
    ) -> None:
        self.seed = int(seed)
        self.rng = np.random.default_rng(self.seed)
        self.canvas = Canvas(width, height, texture, ground, seed, texture_strength)
        self.palette = Palette()
        self.history = History()
        self.out_dir = Path(out_dir)
        self.timelapse = _as_timelapse(timelapse)
        #: The stroke budget, or ``None``. See :meth:`budget_line` and :meth:`cost`.
        self.budget = None if budget is None else int(budget)
        self._last_look: np.ndarray | None = None
        # A scrap of canvas rather than the painting: set on the copies handed out by
        # scratch() and rehearse(), and read by _look_path so a rehearsal's looks are
        # numbered apart from the painting's. See :meth:`_next_rehearsal_path`.
        self._is_trial = False
        #: Named landmarks: ``{name: (x, y)}``. Six or seven verified points are a
        #: drawing, and the masses get hung on them. See :meth:`mark`.
        self.marks: dict[str, tuple[float, float]] = {}
        #: The overlay drawing: paths ``look()`` draws and paint never buries. See
        #: :meth:`guide`.
        self.guides: list[dict] = []
        # Where the stack-of-bars warning last fired: the painting's mark count at
        # the time, and how many long marks crossed the bars it was fired about.
        # See :meth:`_banding_wanted`.
        self._banding_told: tuple[int, int] | None = None
        self._preparation: Preparation | None = None
        #: Assisted modes this painting has used: a machine-laid sketch, or a mass
        #: blocked in on an outline traced from the reference. The protocol reserves
        #: the traced-copy question for the human, and a run that answers it one way
        #: has to say so -- so the painting keeps the record instead of the write-up
        #: having to remember. See :meth:`ref_shape` and :meth:`sketch`.
        self.assisted: list[str] = []
        # Where this session's per-stroke seeds start. Zero for a real painting; a
        # rehearsal continues from the real session's count, so what is tried on the
        # scrap of canvas is the mark that lands when it is painted for real.
        self._index_base = 0
        # The generator's state at the start of the painting call in progress, held
        # so that every record the call makes carries the same one -- see
        # :meth:`_one_call`. ``None`` between calls.
        self._stream_mark: dict | None = None
        self._call_verb = ""
        # Whether that call was handed a rectangle rather than a shape -- the
        # ``boxes:`` line's own input. See :meth:`_one_call`.
        self._call_boxed = False
        # Marks charged before this session's own log began: zero for a painting,
        # and the painting's own count on a rehearsal copy, so that ``spent`` and
        # ``remaining`` inside a rehearsed pass are the painting's numbers.
        self._spent_base = 0
        # The same marks as records rather than as a count. A rehearsal copy starts
        # with an empty log, so every rule in :meth:`report` that reads across passes
        # -- the first-sixty guard and the subject's share -- saw a painting that had
        # never been painted, and *on the rehearse path only*: the same pass run for
        # real read the whole log and stayed correctly silent. Since the guide has
        # every painter rehearse first and look, the wrong answer is the one they
        # always got. Shared, never written through: the copy is thrown away.
        self._prior: list[StrokeRecord] = []
        # A session that works out every stroke and lays none of it. Set on the copy
        # `scratch(count_only=True)` hands back; see :meth:`scratch`.
        self._counting = False
        # What such a copy has already said it cannot answer, so it says each thing
        # once however many times the pass asks.
        self._uncounted: list[str] = []
        # Everything this session has said at a call, in order. Beside the log and
        # never in it: a mark's texture is seeded from its place in
        # `history.records`, so a notice that took an index would move every painting
        # made before it. See :meth:`_notify`.
        self._notices: list[Notice] = []
        # What each pass run from the shell or the MCP server was told afterwards,
        # rehearsals included. Beside the log for the notices' reason. See
        # :meth:`reports`.
        self._reports: list[PassReport] = []
        # What the painter wrote down before painting: the values, the place meant to
        # be lightest, the subject's share, and the two standing warnings this picture
        # has declared its way out of. Beside the log for the same reason the notices
        # are. See :meth:`plan`.
        self._plan = Plan()
        # The last clip mask built, and the outline it came from.
        # See :meth:`_clip_cover`.
        self._clip_memo: tuple | None = None
        # How the film in progress was asked for: ``""`` for a mark laid by hand,
        # ``"glaze"`` when :meth:`glaze` is laying it, ``"aimed"`` when it was given
        # ``to_value=``. Read by :func:`_check_glaze_far`, which does not tell a film
        # aimed at a value that it moved the value -- the painter asked for that shift.
        self._film_call = ""
        # Set on the trial copies :meth:`_glaze_opacity` lays its search films on, so
        # the dozen films a search tries are not each told what a film does.
        self._solving = False
        # The canvas as the pass under way opened -- ``(log index, values view)`` --
        # for the one rule in :meth:`report` that needs to see what a pass covered.
        # Taken by :meth:`_open_pass`, and by :meth:`report` itself for the pass after
        # it. Beside the log, never saved: a pass is one process's business.
        self._opened: tuple[int, np.ndarray] | None = None
        # Whether this painting's time-lapse is rebuilt from the log rather than
        # recorded. Set on a session loaded from a file that kept no frames, which since
        # 0.7.0 is every file: a frame recorded after that load would begin a film in
        # the middle of the painting. See :meth:`timelapse_gif`.
        self._film_from_log = False
        # What opening the session file said -- an `out_dir` somewhere foreign, an
        # engine older than this one -- for the shell and the server to say before
        # anything else. Nothing for a session made here. See :meth:`load`.
        self._load_notices: list[Notice] = []
        if self.timelapse:
            self.capture_frame()

    # -- properties -------------------------------------------------------------
    @property
    def stroke_count(self) -> int:
        """How many marks have been made so far.

        On a rehearsal copy this continues the painting's own count rather than
        starting again from nought: a pass run with ``--rehearse`` sees the same
        ``stroke_count``, :attr:`spent` and :attr:`remaining` it will see when it is
        run for real, which is the number a painter inside the pass is asking for.
        What the copy itself laid is ``s.history.stroke_count``. (It read ``0`` and
        the whole budget until 0.2.0, while ``compare()`` and ``look()`` in the same
        script plainly saw the painted canvas.)
        """
        return self._spent_base + self.history.stroke_count

    @property
    def size(self) -> tuple[int, int]:
        return (self.canvas.width, self.canvas.height)

    @property
    def ground(self) -> np.ndarray:
        """The canvas's own ground, as a colour to mix with or to paint in.

        See :attr:`~easel.canvas.Canvas.ground_color`. Sampling an unpainted corner
        was the only route to it, which is a measurement of the tooth's shading as
        well as of the ground.
        """
        return self.canvas.ground_color

    @property
    def spent(self) -> int:
        """Strokes charged so far. The same number as :attr:`stroke_count`, named
        for the budget rather than for the log."""
        return self.stroke_count

    @property
    def remaining(self) -> int | None:
        """Strokes left of the budget, or ``None`` when no budget was set.

        Goes negative rather than clamping: a painting that has overrun by forty
        strokes should say so, not sit at zero looking finished.
        """
        return None if self.budget is None else self.budget - self.spent

    def budget_line(self) -> str:
        """One line of budget for a human or an agent to read after a pass.

        Printed by ``easel run``. Without a budget it still says what was spent,
        because the count is worth seeing either way::

            142 of 300 strokes spent, 158 left
            142 strokes spent (no budget set)
        """
        if self.budget is None:
            return f"{self.spent} strokes spent (no budget set)"
        left = self.remaining
        if left < 0:
            return f"{self.spent} of {self.budget} strokes spent, {-left} OVER budget"
        return f"{self.spent} of {self.budget} strokes spent, {left} left"

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
        clip=None,
        solid: bool = False,
        note: str = "",
        feather: float | None = None,
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
            clip: a place -- a shape, a region, a name, a run of points -- outside
                which none of this stroke's paint may land. What
                ``block_in(edge="hard")`` is made of, and available by hand for the
                same reason: it is the only way a mark ends on a line rather than on
                its own tip. It changes where the paint goes and nothing else, so a
                clipped stroke and its unclipped twin lay the same dabs from the same
                draws. **A list of places holds the paint inside all of them** -- it
                lands where they agree -- which is what a mass masked to its own
                outline and to a window besides is made of. Its edge is broken
                rather than cut: see ``feather``.
            solid: lay this mark as solid paint -- ``load=1.0`` and
                ``load_falloff=0.0``, so the brush does not run dry along the stroke.
                The same pair :meth:`block_in` has always taken under this name, and
                the clause painters type by hand most often. An explicit ``load=`` or
                ``load_falloff=`` beside it wins.
            note: a line recorded in the log, for the painter's own benefit.
            feather: how far inside ``clip``'s outline the edge breaks, as a fraction
                of the canvas's long side like ``size``. **Left off, 0.002** -- two
                pixels on a canvas 1024 wide -- and the edge is cut the way a loaded
                brush meets tooth: nothing on the drawn line, all of it that far in
                (or a quarter of the way across a shape narrower than four feathers,
                so a thin one keeps its body), and between the two the canvas's own
                weave decides, so the edge is crisp where the tooth is high and
                broken where it is low. Nothing lands past the line. ``feather=0`` cuts it on the line -- a ruled
                edge, which is what every clip was until 0.7.0, and what a ruled
                thing wants. A saved mark replays at the feather it was laid with.
                Only a held mark has an edge to break: given without ``clip=``, it
                is refused.
            **brush_overrides: any other :class:`~easel.brush.Brush` field.

        Returns:
            The :class:`~easel.history.StrokeRecord` that was logged.
        """
        if solid:
            brush_overrides = {"load": 1.0, "load_falloff": 0.0, **brush_overrides}
        b = self._resolve_brush(brush, size, opacity, brush_overrides)
        col = self._resolve_color(color)
        stamps = int(press)
        if stamps < 1:
            raise ValueError(f"press must be at least 1, got {press}.")
        holds = _as_outlines(clip)
        feather = _held_feather(feather, bool(holds), "stroke")
        cover = (None if not holds or self._counting
                 else self._clip_cover(holds, feather))

        # Snapshot before the mark, so undo lands on the state before this stroke.
        # A count-only copy has nothing to undo to and nothing to undo, and copying
        # three canvas-sized arrays per stroke is most of what it is trying not to
        # spend: without this the pot recipe above counted in 2.1s against 3.1s
        # painted, and with it in 0.06s.
        #
        # Of the box this mark can reach rather than of the whole canvas -- the
        # marks are what they were, and the undo stack is a few megabytes instead of
        # several hundred. See :func:`_stroke_box`.
        box = None if self._counting else _stroke_box(self.canvas, points, b, smooth)
        self._snapshot(box)
        # A film laid by hand -- not a pass of a mass, not a replay, not a search film
        # -- is measured once it has landed, so its box is kept as it was before it.
        # See :func:`_check_glaze_far`.
        film = (None if not glaze or box is None or self._stream_mark is not None
                or self._solving
                else self.canvas.rgb[box[1]:box[3], box[0]:box[2]].copy())
        try:
            index = self._index_base + len(self.history.records)
            pts = np.atleast_2d(np.asarray(points, dtype=np.float32))
            if self._stream_mark is None:
                # A mark the painter laid by hand rather than a pass of a mass: the
                # one place a pressure list is likely to be asking for a *width*.
                _check_pressure_on_tip(self, b, pressure, pts, self.canvas)
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
                clip=cover,
                dry_run=self._counting,
            )

            if box is not None and not _within(result.bounds, box, self.canvas):
                # Never seen, and the one way a boxed snapshot could be wrong: the
                # box is the path's own reach with the brush's jitter at six
                # standard deviations and a margin besides. Restoring it would leave
                # paint behind and say nothing, so the stack is dropped and undo()
                # rebuilds from the log, which is exact.
                self.history.invalidate_snapshots()
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
                    params=_brush_params(b, col, glaze=glaze, smooth=smooth, press=stamps,
                                         rng=self._stream_state(),
                                         **({"clip": _clip_params(holds)}
                                            if holds else {}),
                                         # Beside the clip, and only where the edge
                                         # was broken: a record without it replays
                                         # cut on the line, as every clip before
                                         # 0.7.0 was laid.
                                         **({"feather": feather}
                                            if holds and feather > 0.0 else {}),
                                         **({"via": self._call_verb} if self._call_verb
                                            else {}),
                                         **({"boxed": True} if self._call_boxed
                                            else {})),
                )
            )
        except Exception:
            # A bad path (wrong shape, a NaN/Infinity point) is caught inside
            # paint_stroke *after* the snapshot above was pushed. Left in place,
            # that snapshot has no record to match it, and the next undo() would
            # silently delete an unrelated, successful earlier stroke instead of
            # undoing nothing.
            self.history.discard_snapshot()
            raise
        self._auto_frame()
        if film is not None:
            # One frame deeper when it came through `glaze()`, so the warning points
            # at the painter's line either way.
            _check_glaze_far(self, box, film, col, aimed=self._film_call == "aimed",
                             stacklevel=4 if self._film_call else 3)
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

    def smudge(self, edge, size: float = SMUDGE_SIZE, pressure="even", **kw):
        """Drag what is already on the canvas, rather than adding paint.

        Run it **along** a boundary, never across one -- and *along* means along the
        boundary's own shape. Handed two points, a curved or sloping edge gets a pass
        that starts along it and ends across it, which is the same thumbprint
        arriving more slowly. Only a straight boundary is two points.

        So hand it the curve. A shape or a region is a boundary and is taken as one:
        it walks its own outline, which is otherwise the step where a painter samples
        coordinates off a curve by hand and skips it::

            s.smudge([(0.30, 0.40), (0.38, 0.41)], size=0.04)    # a straight edge is two points
            s.smudge([(0.30, 0.40), (0.45, 0.45), (0.60, 0.53),
                      (0.73, 0.63)], size=0.04)                  # a curved one is the curve
            s.smudge(mass, size=0.04)                            # a shape is already that curve

        Measured on a boundary that bends, one pass at ``size=0.040``: given the two
        ends it moved the boundary a mean of ``0.51%`` of canvas height and ``2.9%``
        at worst, where four points along the curve moved it ``0.01%`` and ``0.7%``.
        On a *straight* sloping edge the two are the same pass to the pixel, which is
        the whole of the rule: only a straight boundary is two points.

        **What ``size`` buys stops at about ``0.02``, and what it costs does not.**
        Measured on a step from ``0.78`` to ``0.17``, one pass along the boundary,
        640x480 linen -- the join's steepest value step, and how far the pass walked
        the light mass into the dark:

        ============  ==================  ============================
        ``size``      join softened by    light carried into the dark
        ============  ==================  ============================
        ``0.008``     nothing             ``0.4%`` of canvas height
        ``0.011``     nothing             ``0.6%``
        ``0.016``     ``-46%``            ``1.0%``
        ``0.020``     ``-52%``            ``1.3%``
        ``0.028``     ``-50%``            ``1.7%``
        ``0.040``     ``-69%``            ``2.3%``
        ``0.070``     ``-82%``            ``4.4%``
        ============  ==================  ============================

        Below about ``0.014`` the tip is too small to straddle the join and the pass
        does nothing at all. From ``0.016`` the softening arrives all at once and
        then flattens, while the reach goes on growing with the brush -- so past
        ``0.02`` you are paying in lobe for a join that is already as soft as one
        pass will make it. **The default is the knee of that curve**, and anything
        past ``0.03`` says so as it lays it. It was ``0.07`` until 0.2.0, which is
        off the end of the table: four of five smudges in one painting arrived as
        pale finger-shaped lobes, at sizes the guide's own examples used.

        And this is one pass. Repetition undoes it -- three passes at ``0.040``
        leave a join *sharper* than one does. When once is not enough the answer is
        paint, not another smudge.

        One mark either way, in the log and against the budget.

        Args:
            edge: the boundary to work along -- normalised (x, y) points, or a
                :class:`~easel.regions.Polygon` or region, whose own outline is
                walked. Points are used as given; an outline is resampled fine
                enough to follow itself.
            size: the width of the drag. See the table above before raising it.
            pressure: pressure profile along the pass.
            **kw: any other :meth:`stroke` argument.
        """
        _check_smudge_size(self, size)
        path = _smudge_path(edge, size)
        _check_smudge_path(self, path, size, smooth=bool(kw.get("smooth", True)))
        return self.stroke(path, brush="smudge", color="titanium_white",
                           pressure=pressure, size=size, **kw)

    def glaze(self, points, color, brush="round_soft", opacity: float | None = None,
              to_value: float | None = None, **kw):
        """A thin transparent film over dry paint. Does not build height.

        ``opacity`` is the only argument that does much, and it is the hard one:
        a film's strength is its **distance from what it lands on**, in hue as well
        as in value, so the usable window moves with every passage it is laid over.
        Measured on one mass, a warm light mixture over a cool dark: ``0.05`` has
        already killed the underlying hue and delivered a neutral grey, and ``0.14``
        has moved the value ``0.087`` -- within a hundredth of the ``0.10`` that
        makes a *new* mass rather than shifting an old one. Between those two is the
        whole of the window, and where it sits is different over every mass. The
        guide's answer is *mix the glaze close, then choose an opacity*, and that
        second half is a search a painter runs by rehearsal: one painting spent six
        rehearsals on it and dropped a glaze it had rehearsed three times.

        **So aim at the value instead.** ``to_value=`` is to a film what
        :meth:`~easel.palette.Palette.at_value` is to a mixture -- the same question,
        the other instrument -- and it is answered the same way, by searching rather
        than by arithmetic, because the film's delivery is no more linear in opacity
        than a mixture's value is in the ratio of white::

            s.glaze(band, "warm", opacity=0.18)        # a strength, and then look
            s.glaze(band, "warm", to_value=0.42)       # a value, and it lands there

        It lays films on a trial canvas until one delivers the value asked for,
        measured over the **film's own footprint** -- the pixels it actually
        changes, not a region named by hand -- and then lays that one for real. The
        trials come off a copy of the stroke stream, so the film that lands is the
        film that would have landed had its opacity been typed out: solving for it
        moves no paint. It costs the search about eight trial films, which is
        nothing on a halo and about a second on a band across the whole canvas, and
        it charges **one stroke**, like any other glaze.

        The opacity it chose is on the record it hands back, so a rehearsed film can
        be written out as a number for the real pass::

            print(s.glaze(band, "warm", to_value=0.42).params["opacity"])

        Args:
            points: the film's path, as any stroke's.
            color: the colour of the film. Mix it *close to what it lands on* --
                this solves for an opacity, and no opacity rescues a film that is
                far away: see the table under ``glaze`` in ``CALIBRATION.md``.
            brush: preset name or brush. The soft round by default, which is the one
                tip a film wants.
            opacity: how strong the film is, ``0.18`` by default. Hand this or
                ``to_value``, not both.
            to_value: the value the passage under the film should read at
                afterwards, as :meth:`~easel.palette.Palette.value_of` reports it.

        Returns:
            The one record for the film.

        Raises:
            ValueError: if both ``opacity`` and ``to_value`` are given, or if the
                target is not between the value already there and the one the film
                delivers at full strength. It raises rather than laying the nearest
                it managed, for :meth:`~easel.palette.Palette.at_value`'s reason: a
                film silently landing at the wrong value is the failure this exists
                to stop.
        """
        if to_value is not None:
            if opacity is not None:
                raise ValueError(
                    f"glaze(opacity={opacity!r}, to_value={to_value!r}) was given "
                    f"both: a strength and a value to reach are two ways of asking "
                    f"for the same film, and to_value= exists because the first is "
                    f"the hard one. Drop one of them."
                )
            if self._counting:
                # The search measures what is under the film, and a count-only copy
                # has laid none of its own pass on the canvas it borrowed -- so the
                # answer here would be measured against a canvas that does not
                # exist. It is skipped rather than guessed at, and said out loud
                # once, because an out-of-reach value raises when it is painted.
                self._say_uncounted(
                    "a film given to_value= was priced but not solved: what a film "
                    "delivers is measured off the paint under it, and a count-only "
                    "run has laid none of this pass. The stroke count is exact; "
                    "whether the value is in reach is a question for --rehearse."
                )
                opacity = None
            else:
                opacity = self._glaze_opacity(points, color, float(to_value),
                                              brush, kw)
        self._film_call = "aimed" if to_value is not None else "glaze"
        try:
            return self.stroke(points, brush=brush, color=color, glaze=True,
                               opacity=GLAZE_OPACITY if opacity is None else float(opacity),
                               **kw)
        finally:
            self._film_call = ""

    def _glaze_opacity(self, points, color, target: float, brush, kw: dict) -> float:
        """The opacity at which this film delivers ``target`` over its own footprint.

        Bisected on trial canvases rather than solved, for the reason
        :meth:`~easel.palette.Palette.at_value` bisects: what a film delivers is the
        pigment model, the tooth and whatever is already there, and none of that is
        available as a formula. Each probe is a real film on a copy of this canvas,
        so what is measured is what will happen.

        The footprint comes off a probe at full strength -- the pixels a film of this
        shape changes at all -- and every probe after it is measured over that one
        mask, so the search is comparing like with like and never widens as the film
        gets stronger. It is also the honest place to measure: a film laid along a
        path reaches where its brush reaches, and a region named by hand is a
        different area from the one the paint lands on.
        """
        before = self.canvas.rgb

        def film(opacity: float) -> np.ndarray:
            trial = self._trial_session()
            trial._solving = True
            trial.glaze(points, color, brush=brush, opacity=opacity, **kw)
            return trial.canvas.rgb

        full = film(1.0)
        under = np.abs(full - before).sum(axis=2) > _GLAZE_FOOTPRINT
        if not under.any():
            raise ValueError(
                "glaze(to_value=...) cannot solve a film that lands nowhere: at "
                "opacity=1.0 this one changes no pixel. Check the points are on "
                "the canvas and the colour is not what is already there."
            )
        field = self.palette.value_of(before[under].mean(axis=0))
        reach = self.palette.value_of(full[under].mean(axis=0))
        lowest, highest = min(field, reach), max(field, reach)
        if not lowest - _GLAZE_VALUE_TOL <= target <= highest + _GLAZE_VALUE_TOL:
            raise ValueError(
                f"glaze(to_value={target:.3f}) is out of reach: the paint under this "
                f"film reads {field:.3f}, and at opacity=1.0 -- the whole film, no "
                f"transparency left -- it reaches {reach:.3f}. A film can only travel "
                f"between those two. Mix the film further from what it lands on, or "
                f"lay the change as paint: a film asked to move a passage this far "
                f"has no usable opacity, which is the table under `glaze` in "
                f"CALIBRATION.md."
            )

        rising = reach > field
        lo, hi = 0.0, 1.0
        best, best_v = 1.0, reach
        for _ in range(_GLAZE_SOLVE_STEPS):
            mid = 0.5 * (lo + hi)
            value = self.palette.value_of(film(mid)[under].mean(axis=0))
            if abs(value - target) < abs(best_v - target):
                best, best_v = mid, value
            if abs(value - target) <= _GLAZE_VALUE_TOL:
                break
            if (value < target) == rising:
                lo = mid
            else:
                hi = mid
        if best < _GLAZE_MIN_OPACITY:
            self._notify(
                "glaze-nothing",
                f"glaze(to_value={target:.3f}) solved to opacity={best:.3g}, which is "
                f"a film that changes nothing: the paint under it already reads "
                f"{field:.3f}. It still costs a stroke. Ask for a value further from "
                f"what is there, or leave the passage alone.",
                stacklevel=4,
            )
        return best

    def block_in(
        self,
        region,
        brush: str | Brush = "bristle",
        color="burnt_umber",
        direction=None,
        density: float = 1.0,
        pressure="taper",
        size: float | None = None,
        overhang: float | None = None,
        edge: str = "ragged",
        solid: bool = False,
        clip=None,
        dry_first: bool = False,
        note: str = "",
        feather: float | None = None,
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
                rather than along the canvas; **a line of two points to run along**,
                ``direction=((0.33, 0.01), (0.58, 0.29))``; or a sequence of any of
                those for one pass each. The passes run *along* the angle and the
                stack steps *across* it, which is the same geometry ``cost_line``
                counts when it says how far a stack steps.

                Take the line rather than the angle wherever the angle came off the
                picture. Degrees here are measured in the ``0..1`` coordinates, not
                on the screen, so on a canvas that is not square they are not the
                angle you can see: measured on 1000x500, ``direction=-23`` lays its
                passes at **-12 degrees on screen**, and on 1024x768 ``45`` runs at
                **37**. Three painters wrote a metric projection, read the screen
                slope of an edge off it, typed that in, and got something else --
                one laid *passes along the sloped boundary*, the remedy for a gable
                whose screen slope was 41 degrees, at 33. A pair of points is a
                line; a pair of numbers is still two angles, so ``(28, 118)`` is a
                cross and not a point.

                Vary this between passes so the marks are not parallel -- and prefer
                the angle the *subject* runs at. A hillside swept at its
                own angle stops being a stack of horizontal bars, which is the single
                loudest tell that nobody chose the direction. **Left off, the passes
                run horizontally**, and on a shape that is not wider than it is tall
                that is the expensive way round: the passes step down its whole
                height. A painter costed two planes at 9 and 9 with ``direction=90``,
                wrote the calls without it, and the rehearsal charged 43 and 55. So a
                shape laid with this left off says so when it costs more than about
                2.5x what ``"axis"`` would, and names the number.

                **A sequence is one whole pass per angle and is charged the sum.**
                Not one stack sized for the steepest -- every angle is paid for in
                full, and a steep angle on a wide mass costs several times a
                shallow one. Measured on one painting's room mass, same brush, same
                density: ``"axis"`` 4 strokes, a single ``-17`` degrees 7,
                ``"cross"`` 15, and a ten-angle sequence **85**, which is the ten
                angles' own prices added up. Two directions are what breaks a comb
                and more do not break it further, so a list longer than a pair says
                so too, with every angle's price in the line.
            density: how close together the passes run. 1.0 steps them a part-brush
                apart, which covers the place; below 1 spaces them out and leaves
                the ground showing through, which is usually what you want for a
                first pass. It is the *spacing*, not the coverage -- a mass that
                has to be solid wants ``solid=True`` as well, because the passes
                run dry as they go whatever their spacing.
            pressure: pressure profile for each pass.
            size: brush size override.
            overhang: how far each pass runs past the **ends of the pass**, as a
                fraction of the brush width -- and **which two edges those are turns
                with** ``direction``. It lengthens each pass along its own line, so
                on a mass swept horizontally it reaches past the left and right
                edges, and on the same mass swept vertically -- which is what
                ``"axis"`` picks when the mass is taller than it is wide -- it
                reaches past the top and the bottom, and off the foot of the mass
                onto whatever the mass is standing on. Measured on a shape
                ``0.40x0.30``, bristle at ``size=0.030`` (19px), 640x480: swept
                horizontally the paint reaches 3px past the left edge at ``0`` and
                22px at ``1.0``, while top and bottom stay at 6px throughout; swept
                vertically the same numbers move on the top and bottom instead
                (4px to 18px) and the sides stay put. **The edges it does not
                lengthen still get half a brush**, because the brush is wider than
                the step between passes: it is the pass *centres* that stop at the
                boundary. So a mass never stops dead at its own outline, whatever
                this is set to.

                It defaults to ``0.35`` for a rectangle and to ``0`` for a shape.
                They differ because the two places mean different things: a
                rectangle is a *region of canvas* and a block that stops short of
                its own corners reads as cropped, while a shape's outline **is the
                drawing**, and paint run past it is the silhouette being spoiled by
                an argument. Raising it on a shape is worth doing deliberately and
                worth rehearsing.
            edge: ``"ragged"``, the default -- the passes stop at the boundary and
                the brush breaks past it, which is what a brush does, and what a mass
                sitting behind other things wants. ``"clean"`` gives the mass a drawn
                contour instead: the shape is inset by half the brush, filled, and
                then one pass is swept along that inset outline in the same colour,
                so the **outer half of the brush lands on the line you drew** --
                and that contour does not wander, because the line is the drawing.
                Reach for it on a small mass whose silhouette is the drawing -- a
                round tip lays its half-brush overhang as separate discs, and at that
                size they read as a fringe of dots around the shape rather than as a
                soft edge. Measured on a mass a third of the canvas across, round tip at
                ``size=0.05``:
                paint reaches 20px past the outline ragged and 13px clean, and the
                clean silhouette is the less ragged of the two. **Use a solid tip.**
                Clean pulls the paint in on a comb too, but one bristle pass along a
                contour is stringy -- it covers about three-quarters of its width --
                so it leaves a *rougher* outline than the ragged fill did, and says
                so when asked. Where the outline runs off the canvas the inset is
                dropped: there is no drawn line out there for the brush's outer
                half to land on, and a mass that meets the frame should run off it.

                ``"hard"`` masks **every dab to the outline** -- no inset, no contour
                pass, and no paint outside the shape at all. It is the only setting
                that ends a pass where the outline is rather than where the tip
                falls, which is what the chisel staircase and the half-brush spill
                both are: a mass laid ragged puts three to four times as many
                horizontal edges down a sloping boundary as the mass has of its own,
                and a dark under a bench spilled half a brush onto the wall behind
                it as a sawtooth. Measured on one painter's lit face with the same
                Sobel instrument the staircase table uses -- the share of strong
                edges within ten degrees of horizontal, on a mass that has no
                horizontal feature of its own, vertical passes, laid solid: a
                ``flat`` at ``size=0.020`` puts **13%** there ragged and **4%**
                hard, a ``knife`` **16%** and **4%**. The comb and the round tip
                were never the ones doing it (**4%** and **3%** ragged) and are not
                much helped. Furthest paint past the outline on that shape, which is
                the other half of the same measurement: **9.3px** ragged, **2.6px**
                clean, and **under one pixel on every side** hard, that pixel being
                the boundary's own feathering. Its cost is the thing ragged is for
                -- a mass
                *behind* other things wants the brush to break past its boundary --
                so ragged stays the default and this is opt-in. ``overhang``
                defaults to **two** brushes here, since nothing can land outside the
                outline and the only thing it still does is carry every pass end up
                to it. One was not enough: the default ``pressure="taper"`` reaches
                zero one brush out, so at one brush every pass met the outline at
                part pressure -- and a round tip, which loses *width* with pressure,
                met it at part width. Measured on the 3 px strip just inside a
                sloping outline, laid solid: a ``round_hard`` left ``0.85%`` to
                ``3.26%`` of it bare at one brush and ``0.055%`` to ``0.33%`` at
                two. The pass count does not move, so neither does what
                :meth:`cost` quotes. **The edge is broken, not cut** (0.7.0): just
                inside the outline -- ``0.002`` of the long side, two pixels at 1024
                -- the paint lands where the canvas's tooth is high and not where it
                is low (``feather``), because a mask cut on the line was one pixel of
                four values and then a step, which a painter who relied on it called
                the least paint-like thing in the engine.
            solid: lay the mass as solid paint -- ``load=1.0`` and
                ``load_falloff=0.0``, so no pass runs dry partway across. Density
                spaces the passes; this is what fills the gaps *along* them.
                Measured on 38 passes of a ``flat`` at ``size=0.030``,
                ``density=1.0`` -- which looks like a request for a solid mass and
                is not one: the interior comes out at **sd 0.063** with **4.4%** of
                its pixels still within ``0.05`` of bare ground, and at **sd 0.007**
                and **0.0%** with this -- nine times more even, for the same 38
                strokes and the same money. Off by default, because a first pass
                wants the ground showing through, and because every painting made
                before this existed replays as it was. An explicit ``load=`` or
                ``load_falloff=`` beside it wins: a painter asking for a starved
                brush means it.
            clip: a place -- or a list of places -- outside which none of this mass's
                paint may land, as on :meth:`stroke`. ``edge="hard"`` is this same
                clip pointed at the mass's **own** outline; this one points it
                somewhere else, which is how a mass is held inside a window, a pane,
                or a neighbour it must not cross. Given both, the paint lands where
                they agree.
            dry_first: dry the place before laying the mass, so this paint covers
                what is under it instead of mixing with it. Free, and off by
                default, because wet-into-wet is most of what makes a passage soft
                and a mass laid over a dried one is a decision. What it is for is the
                case that cost a painter their one ``undo``: a patch laid over a
                bezel still wet from the pass before it picked the bezel's value up
                and printed it -- a film at ``opacity=0.15`` leaves about ``0.13``
                behind, which is past the ``0.10`` that makes a new mass
                (``CALIBRATION.md``, *GLM's rings*). :meth:`cover` has had this
                since it was built, and has it on.
            note: recorded in the log.
            feather: how far inside the outline a held edge breaks -- under
                ``edge="hard"``, and on ``clip=`` -- as on :meth:`stroke`: **0.002**
                left off, ``0`` for an edge cut on the line. Only a held mass has an
                edge to break, so a ragged or clean one without ``clip=`` refuses it.

        Returns:
            The records for every stroke laid down.
        """
        place = as_place(region)
        # `solid` is a pair of defaults, not an override: a painter who says
        # `load=0.3` beside it is asking for a starved brush on purpose, and gets one.
        if solid:
            brush_overrides = {"load": 1.0, "load_falloff": 0.0, **brush_overrides}
        b = self._resolve_brush(brush, size, None, brush_overrides)
        shaped = isinstance(place, Polygon)
        if edge not in ("ragged", "clean", "hard"):
            raise ValueError(
                f"block_in(edge={edge!r}) is one of 'ragged' -- the brush breaks past "
                f"the boundary, the default -- 'clean', which insets the fill by half "
                f"the brush and lays one pass along the outline itself, or 'hard', "
                f"which masks every dab to the outline so no paint lands outside it."
            )
        overhang = _mass_overhang(edge, overhang)

        records: list[StrokeRecord] = []
        traced = ""
        if getattr(place, "traced", False):
            # An outline lifted off the reference, not drawn by the painter. The
            # protocol reserves that question for the human; the least this can do is
            # be impossible to leave out of the write-up by accident.
            traced = " (traced)"
            self._note_assisted(f"traced outline blocked in: {place.name or 'shape'}")

        # A clean edge fills the shape half a brush short of its own boundary. The
        # fill's own overhang then carries the paint back out to the true outline,
        # and the contour pass below draws it.
        fill = _clean_fill(place, b.size * 0.5) if edge == "clean" else place
        held = _mass_hold(place, edge, clip)
        feather = _held_feather(feather, bool(held),
                                "cover" if self._call_verb == "cover" else "block_in")
        _check_solid_comb(self, b, density, solid, stacklevel=3)
        if edge == "clean" and b.tip == "bristle":
            self._notify(
                "clean-comb",
                f"block_in(edge='clean') with a bristle brush ({b.name!r}) leaves a "
                f"stringier contour than the ragged fill it replaces: one comb pass "
                f"covers about three-quarters of its width. Use a solid tip "
                f"('flat', 'knife', 'round_hard') for a drawn edge.",
                stacklevel=2,
            )

        if shaped and direction is None:
            _check_default_direction(self, fill, b, density, overhang, stacklevel=3)
        if direction is not None:
            _check_direction_sequence(self, fill, b, direction, density, overhang,
                                      stacklevel=3)
        if edge == "clean":
            # Regions too: cover() is handed one far more often than a shape.
            _check_clean_size(self, place, b, self.canvas, stacklevel=3,
                              verb="cover" if self._call_verb == "cover" else "block_in")
        elif edge == "ragged" and shaped:
            _check_round_block(self, place, b, self.canvas, stacklevel=3)
        if edge == "ragged":
            # Regions too: a rectangle swept at an angle stairs down all four sides,
            # and `span(...)` is how most of the corpus's bands are written.
            _check_chisel_staircase(self, place, b, direction, density, self.canvas,
                                    stacklevel=3)
            if self._call_verb != "cover":
                # A burial's ends run outside the area on purpose: cover() says why.
                _check_mass_spill(self, place, fill, b, direction, density, overhang,
                                  held, stacklevel=3)

        with self._one_call("block_in", place):
            if dry_first:
                self.dry(1.0, place)
            for pass_dir, path, flipped in self._block_in_paths(fill, b, direction,
                                                                density, overhang):
                records.append(
                    self.stroke(
                        path,
                        brush=b,
                        color=color,
                        pressure=_canvas_order_pressure(pressure) if flipped else pressure,
                        clip=held,
                        feather=feather,
                        note=note or (f"block-in "
                                      f"{place.name or ('shape' if shaped else 'region')} "
                                      f"{pass_dir}{traced}"),
                    )
                )
            if edge == "clean":
                records.extend(self._clean_contour(
                    fill, b, color, pressure,
                    note or (f"clean edge {place.name or ('shape' if shaped else 'region')}"
                             f"{traced}"),
                    clip=held, feather=feather,
                ))
        # The same test `_check_solid_comb` asks, and for the same reason: what
        # matters is what the paint did, not which keyword was typed. `cover()` lays
        # `load=1.0, load_falloff=0.0` itself and refuses `solid=` as a duplicate of
        # its own recipe, so a burying pass would otherwise be the one solid mass
        # nobody measured -- and burying is exactly where a hole is worth knowing.
        if solid or (b.load >= 1.0 and b.load_falloff <= 0.0):
            _check_holes(self, place, b, color, stacklevel=3)
        return records

    def _clean_contour(self, fill, b: Brush, color, pressure, note: str,
                       clip=None, feather: float = 0.0) -> list[StrokeRecord]:
        """The one pass ``edge="clean"`` lays along the inset outline.

        Along the *inset* outline, not the drawn one, so that the outer half of the
        brush lands on the drawn line rather than half a brush past it. Measured on a
        mass a third of the canvas across, size 0.05: paint reaches 20px past the
        outline blocked in ragged, 38px with the contour laid along the drawn line,
        and 13px this way -- and this way also leaves the least ragged silhouette of
        the three.

        And along the outline's **own edges**, not a spline through its corners. A
        sweep smooths the boundary it is given before offsetting it, which is right
        for a boundary read off the grid and wrong for a drawn polygon: through two
        sparse corners the spline bows outward, and on a tall four-cornered tower the
        contour stood **65px** above the top edge the ragged fill stopped 3px short
        of -- a pointed arch nobody drew, found by three painters on three shapes.
        The fill is cut against the polygon's straight sides, so the contour now
        follows the same line the fill stops at. Same draw from the stream as the
        sweep it replaces, so nothing painted after a clean mass moves.
        """
        outline = fill.closed if isinstance(fill, Polygon) else polygon(fill).closed
        depth = max(b.size * 0.5, 1e-3)
        out: list[StrokeRecord] = []
        for _kind, path, flipped in self._sweep_paths(outline, depth, 1, depth, None,
                                                       None, None, wander=False,
                                                       smooth=False):
            out.append(self.stroke(
                path, brush=b, color=color,
                pressure=_canvas_order_pressure(pressure) if flipped else pressure,
                clip=clip, feather=feather if clip else None,
                note=note,
            ))
        return out

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
        for pass_dir in _pass_directions("horizontal" if direction is None else direction):
            angle = place.axis if pass_dir == "axis" else pass_dir
            paths = (self._shape_paths(place, angle, band, b.size * over) if shaped
                     else self._block_paths(place, angle, band, b.size * over))
            for path, flipped in paths:
                yield pass_dir, path, flipped

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
                yield (path, False) if i % 2 == 0 else (path[::-1], True)

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
            yield (path, False) if i % 2 == 0 else (path[::-1], True)

    def _block_paths(self, r: Region, direction, band: float, over: float):
        if not isinstance(direction, str):
            yield from self._angled_paths(r, float(direction), band, over)
            return
        """Stroke paths that sweep a region, with a little wander so they are not rules.

        Consecutive passes run in opposite directions, the way a hand comes back
        across the canvas. Paint runs out along a stroke, so passes that all start
        at the same edge stack their run-out on top of each other and leave the
        whole mass a full value lighter on the side they end at.
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
                yield (path, False) if i % 2 == 0 else (path[::-1], True)
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
                yield (path, False) if i % 2 == 0 else (path[::-1], True)
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
                yield (path, False) if i % 2 == 0 else (path[::-1], True)
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
        wander: bool = True,
        solid: bool = False,
        clip=None,
        note: str = "",
        feather: float | None = None,
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
            wander: whether each pass wanders a little off the offset curve, so that
                a stack of them is not a set of parallel rules. That is what it is
                for, and a stack is the usual case -- but a **single** pass has no
                parallel to break, and the wander then only moves the line off the
                one the painter drew. Three draws carry the whole pass, so what it
                moves is a whole section of it at once. Measured on an eleven-point
                ridge, ``flat`` at ``size=0.08``, over ten seeds: the contour sits
                a mean ``10.8px`` past the drawn line either way, but how far varies
                from seed to seed by **3.3px** with the wander and **1.1px** without
                it, and its departure along its own length falls from ``3.98px`` to
                ``3.30px``. (Setting the brush's ``jitter=0`` instead does nothing
                here: ``3.45px`` and ``3.89px``. It is this, not the tip.) Off for
                the contour of :meth:`block_in`'s ``edge="clean"``, whose whole
                bargain is landing on the line.
            solid: lay the passes as solid paint -- ``load=1.0`` and
                ``load_falloff=0.0``, so no pass runs dry partway along. The same
                pair :meth:`block_in` takes under this name; a long pass along an
                edge is where a brush runs out soonest.
            clip: a place, or a list of places, outside which none of this mass's
                paint may land, as on :meth:`stroke`. A sweep has no ``edge=``
                setting of its own -- its first argument *is* the boundary -- so
                this is how its passes are held to a silhouette instead of breaking
                past it.
            note: recorded in the log.
            feather: how far inside ``clip``'s outline its edge breaks, as on
                :meth:`stroke`: **0.002** left off, ``0`` for an edge cut on the line.

        Returns:
            The records for every stroke laid down.
        """
        feather = _held_feather(feather, bool(_as_outlines(clip)), "sweep")
        if isinstance(edge, Polygon):
            # A shape *is* a boundary that comes back on itself, which is what a
            # closed sweep wants. Its outline repeats the first point, so `closed`
            # infers itself, and the traced-copy question follows the shape here the
            # same way it follows it into block_in.
            if edge.traced:
                self._note_assisted(f"traced outline swept: {edge.name or 'shape'}")
            edge = edge.closed

        if solid:
            brush_overrides = {"load": 1.0, "load_falloff": 0.0, **brush_overrides}
        b = self._resolve_brush(brush, size, None, brush_overrides)
        depth, step, n_passes, cross = self._sweep_passes(b, depth, passes, cross, density)

        records: list[StrokeRecord] = []
        with self._one_call("sweep"):
            for kind, path, flipped in self._sweep_paths(edge, step, n_passes, depth,
                                                         cross, into, closed, wander):
                records.append(
                    self.stroke(
                        path,
                        brush=b, color=color,
                        pressure=_canvas_order_pressure(pressure) if flipped else pressure,
                        clip=clip,
                        feather=feather,
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
                     cross, into, closed, wander: bool = True, smooth: bool = True):
        """Every pass ``sweep`` would lay, as geometry, before any of it is paint.

        :meth:`_block_in_paths`' counterpart, and split out for the same reason: a
        sweep is one call and ten to thirty strokes, so :meth:`cost` has to be able
        to price one without painting it. A generator for the same reason too --
        the wander comes off ``self.rng`` between the ``stroke()`` calls above.

        Yields the log note for each pass beside its path, because the two sets of
        passes are named differently in the log and a caller that only counts them
        does not care which is which. ``smooth=False`` follows the edge's own
        corners instead of a spline through them -- what the contour of a clean
        block-in wants, and nothing else so far.
        """
        spacing = max(step * 0.6, 0.008)
        spine, ring = _sweep_spine(edge, closed, spacing, smooth)
        normals = _sweep_normals(spine, into, ring)
        cum = _arc_length(spine)
        length = float(cum[-1])

        for k in range(n_passes):
            off = k * step + self._sweep_wobble(cum, length, step, ring, wander)
            path = _drop_folds(spine + normals * off[:, None], spine, step)
            if path is None:
                continue                      # this pass folded in on itself: past the middle
            yield ("sweep", path, False) if k % 2 == 0 else ("sweep", path[::-1], True)

        if cross is None:
            return

        for i, (us, vs) in enumerate(_cross_lines(length, depth, step, cross, spacing)):
            base = _band_points(spine, normals, cum, us, np.zeros_like(vs))
            wob = self._sweep_wobble(us, length, step, False, wander)
            path = _drop_folds(_band_points(spine, normals, cum, us, vs + wob), base, step)
            if path is None:
                continue
            yield (("sweep cross", path, False) if i % 2 == 0
                   else ("sweep cross", path[::-1], True))

    def _sweep_wobble(self, at, length: float, step: float, ring: bool,
                      wander: bool = True) -> np.ndarray:
        """A smooth wander along a pass, so a sweep is not a set of parallel rules.

        Three draws interpolated along the pass, not noise per point: independent
        per-point noise clumps and gaps, which reads as an artefact rather than as a
        hand. A closed edge gets the same value at both ends
        so the seam does not step.

        ``wander=False`` returns no offset -- but *takes the draw anyway*, so that
        turning it off moves the pass it is turned off for and nothing else. Skipping
        the draw would shift the generator's stream under every mark laid after it,
        and a painting reruns from its own scripts.
        """
        wob = self.rng.normal(0.0, step * 0.3, size=3)
        if not wander:
            return np.zeros(np.shape(at))
        if ring:
            wob[-1] = wob[0]
        return np.interp(at, [0.0, length * 0.5, length], wob)

    # -- drawing ----------------------------------------------------------------
    def cover(
        self,
        place,
        color,
        brush: str | Brush = "flat",
        size: float | None = None,
        direction: str = "horizontal",
        density: float = 1.0,
        overhang: float | None = None,
        edge: str = "hard",
        dry_first: bool = True,
        clip=None,
        note: str = "",
        feather: float | None = None,
        **brush_overrides,
    ) -> list[StrokeRecord]:
        """Bury a mistake, with every clause of the burying recipe already set.

        Repairs happen with paint, not with :meth:`undo` -- and burying takes a
        particular kind of mark that the wrong brush makes worse. This is that mark:
        the area dried first so new paint covers instead of mixing, a **solid tip**
        because a comb leaves the old paint showing between its streaks however high
        the opacity goes, ``load=1.0`` and ``load_falloff=0.0`` because a brush that
        runs dry leaves a speckled film that everything after it has to sit on,
        ``opacity=1.0``, ``pressure="even"``, and passes that **run past the area and
        are held to it**, so no chisel end stops inside the mistake and no paint lands
        outside the place it was handed::

            s.cover(cell("D5"), "corrected_sky")     # that is the whole repair

        ``load_falloff=0.0`` is the clause that is easy to miss: a full-width
        correction stroke at ``load=1.0`` still runs dry and speckles at its far end
        without it, which is the failure that sends a painter back for a second
        correction over the first. Those two clauses are
        :meth:`block_in`'s ``solid=True``, which is the same pair of defaults for a
        mass that is not a repair.

        **Held to its place, by default** (0.6.0; the default was ``"ragged"``).
        Until then the passes ran a full brush past the area, which is invisible on a
        flat passage and the fault on any other: burying a mis-made leaf inside a
        finished pane of glass, ``cover(Region(0.905, 0.380, 0.985, 0.478))`` laid a
        flat pale panel across a visibly larger patch than the one it was given, and
        the repair was louder than the mistake. Measured on a place 108x60 px on a
        900x600 canvas, with the default brush, burying a light stroke in the
        passage's own colour: on a flat passage neither edge leaves anything to see;
        on a graded one ``"ragged"`` leaves **4.45x** the place visibly off the
        passage, nearly all of it outside the place, against **0.47x** held to it; on
        a worked one **4.14x**, the neighbouring marks buried with it, against
        **0.51x**. Holding it costs an outline: the place's rectangle stands in a
        worked passage as a value step of ``0.042`` against the passage's own
        ``0.010`` -- a crisp patch the size of the place, which does read as cut out,
        and is the smaller fault (``CALIBRATION.md``, *A burial and the place it was
        handed*). ``"ragged"`` is still one keyword away and says nothing about its
        overrun, which is what that form is for.

        Args:
            place: what to bury -- a region, a name, a 4-tuple or a shape.
            color: what to bury it under.
            brush: a solid tip. ``"flat"`` and ``"knife"`` leave a chisel end,
                ``"round_hard"`` a rounded one; both are outside the area anyway.
                A bristle is refused the recipe and says so.
            size: brush size override.
            direction: as :meth:`block_in`. Run it along the grain of what is
                already there.
            density: as :meth:`block_in`. Leave it at 1.0 -- a correction that lets
                the old paint through is not a correction.
            overhang: how far past the area each pass runs, in brush widths. The
                default follows ``edge``: **two** under ``"hard"``, which is
                :meth:`block_in`'s own rule -- nothing can cross the mask, so the only
                thing left for an overhang to do is carry every pass end up to the
                outline, and one brush left the boundary bitten between them; one full
                width under ``"ragged"``, which is what puts the ends outside; ``0``
                under ``"clean"``, which is what keeps them in.
            edge: ``"hard"``, the default -- every dab masked to the area, so nothing
                lands outside it at all. ``"ragged"`` runs the passes a full brush past
                the area, the recipe before 0.6.0: it melts into a flat passage and
                buries whatever stands beside the place on any other. ``"clean"`` is
                :meth:`block_in`'s clean edge, the fill inset by half the brush and the
                boundary drawn, and it wants a place four brushes across: under that
                the inset takes the place rather than a rim of it -- the place above,
                at the default brush, keeps ``8%`` to ``15%`` of its mistake showing
                -- and the call says so.
            dry_first: dry the area before covering it. Free, and part of the
                recipe; only the area, so a wet neighbour it must blend into stays
                wet.
            clip: a place, or a list of places, outside which none of the burial's
                paint may land, as on :meth:`stroke` and :meth:`block_in`. A burial is
                held to its own place already, so this is what to reach for when the
                repair has to stop at something else as well -- the pane it sits in,
                the form it is on.
            note: recorded in the log.
            feather: how far inside the place the burial's edge breaks, as on
                :meth:`stroke`: **0.002** left off, so the patch's border takes paint
                where the tooth is high and lets the passage show where it is low,
                rather than standing as a cut rectangle; ``0`` for an edge cut on
                the line, the burial before 0.7.0.

        Returns:
            The records for every stroke laid down, the ``dry`` not among them --
            drying is free and is not a mark.
        """
        target = as_place(place)
        # Asked before anything is laid: the dry below is a record too.
        _held_feather(feather, bool(_mass_hold(target, edge, clip)), "cover")
        reach = _cover_overhang(edge, overhang)
        b = self._resolve_brush(
            brush, size, None,
            {"load": 1.0, "load_falloff": 0.0, "opacity": 1.0, **brush_overrides},
        )
        if b.tip == "bristle":
            self._notify(
                "cover-comb",
                f"cover() was given a bristle brush ({b.name!r}), which does not "
                f"bury: its comb leaves the old paint showing between the streaks "
                f"at any opacity. Use 'flat', 'knife' or 'round_hard'.",
                stacklevel=2,
            )
        with self._one_call("cover", target):
            if dry_first:
                self.dry(1.0, target)
            return self.block_in(
                target, brush=b, color=color, direction=direction, density=density,
                pressure="even", overhang=reach, edge=edge, clip=clip, feather=feather,
                note=note or f"cover {target.name or 'area'}",
            )

    def scumble(
        self,
        band,
        color_a,
        color_b,
        n: int = 8,
        brush: str | Brush = "bristle",
        size: float | None = None,
        opacity: float = 0.5,
        direction="axis",
        overhang: float = 0.35,
        pressure="even",
        solid: bool = False,
        edge: str = "ragged",
        clip=None,
        note: str = "",
        feather: float | None = None,
        **brush_overrides,
    ) -> list[StrokeRecord]:
        """A soft passage: ``n`` overlapping passes stepping from one value to another.

        There is no gradient tool, and there should not be one -- but the thing a
        painter reaches for a gradient *for* is a wide quiet passage, and a wide
        quiet passage laid as three hard bars is the loudest tell in a picture. One
        smudge takes about 40% off a join, once; doing it again undoes most of the
        first pass. When once is not enough, the answer is paint: many overlapping
        strokes at closely spaced values, which is what this lays::

            s.scumble(span("A3", "H5"), "shadow", "light", 8)   # 8 strokes, no bars

        The passes run **along** the band and step **across** it, from ``color_a`` at
        one edge to ``color_b`` at the other, mixing one step per pass. They overlap:
        the brush is wider than the step between them, which is what closes the
        joins that stepping alone would leave. **The step is ``extent / n``, and with
        no ``size=`` the brush is picked from it** -- about three steps, the same
        mechanism the ``inward`` case uses, because the brush and the step are one
        thing and not two settings. A preset's own default is usually one to one and
        a half steps here, which is the worst place on the curve: the passes clear
        each other and the passage comes back a venetian blind. Hand it a narrower
        brush than that on purpose and it says so.

        **The passes are laid solid** -- ``load=1.0, load_falloff=0.0`` -- because a
        wide pass that runs dry along its own length prints a stripe down the passage
        that the passes after it do not close. Measured on a band eight passes wide:
        ``5.17%`` of it came back within a hair of bare ground on the brush's own
        load, ``0.01%`` on this pair. Both are defaults: ``load=`` or
        ``load_falloff=`` beside the call still wins, which is how a starved band is
        asked for on purpose.

        **Opacity does not make a passage quieter; it slows the passes down.** The
        passes overlap, so a low opacity accumulates back toward full colour rather
        than thinning what arrives. Measured on a band of 8 passes from ``0.30`` to
        ``0.62`` over a ``0.22`` ground, 640x480: the passage delivers a mean of
        ``0.45`` at ``opacity=1.0``, ``0.44`` at ``0.60`` and ``0.41`` at ``0.40``.
        Only below about ``0.4`` does it move at all, and at ``0.15`` it still
        arrives within ``0.12`` of full colour. **To make a passage quiet, mix the
        two colours closer together** -- that is what the two arguments are for.

        **That grades edge to edge, which is a band and not a glow.** A lit patch, a
        bloom, a light falling off a surface goes dark at *every* edge and bright in
        the middle, and ``direction="inward"`` lays that: the passes go round the
        place instead of across it, the first along its boundary and each one after it
        a part-brush further in, so ``color_a`` sits on the edge and ``color_b``
        arrives at the centre::

            s.scumble(patch, "shadow", "lit", 8, direction="inward")   # 8 strokes

        The rings step ``depth / n`` apart, where ``depth`` is half the patch's
        shorter extent, and each is laid over the ones before it -- so the brush and
        the step are one mechanism, not two settings. Leave ``size`` off and it is
        picked from the step (about three of them). Give a brush much wider than
        that and the last rings bury the first: the middle comes back one flat
        colour with a rim of ramp round it, which is a sun and not a glow, and it
        says so.

        **The patch bounds ``n`` from the other side, and this is the half that
        surprises people.** The brush is ``3 x depth / n``, so *more rings on a
        shallow patch buy a narrower brush, not finer banding* -- and past
        ``n = 120 x depth`` that brush is under ``0.025``, where a comb is four
        streaks with gaps. A patch ``0.0667`` deep carries the recipe's eight
        rings and nothing shallower does. It says so at the call, from both sides
        now: a painter who met this at ``n=12`` on a patch ``0.075`` deep read the
        post-pass check's bristle complaint as unrelated and spent two more
        rehearsals. **Where no ``n`` fits** -- under about ``0.042`` deep, where
        even five rings comb -- the patch is not asking for this verb at all: a
        glow that shallow is *a volume of lit air*, three glazes along the axis of
        the light, and the warning says so.

        Reach for it instead of strokes radiating out from a centre, which draw the
        petals of a daisy -- :meth:`report` says so when a pass lays one.

        The first ring lands **on** the boundary, so ``color_a`` is the value the
        patch meets what it sits in at: give it the surrounding value and the glow
        melts into the mass around it, give it something darker and the patch gets a
        rim drawn round it.

        Costs exactly ``n`` strokes on a band the painter can name, so it can be
        budgeted before it is laid. (On a concave shape a pass line is cut into the
        pieces really inside the shape, the same way :meth:`block_in` cuts one, so a
        shape with a bite out of it costs a little more than ``n``.)

        Args:
            band: where the passage goes -- a region, a name, a 4-tuple or a shape.
            color_a: the value at the first edge.
            color_b: the value at the far edge.
            n: how many passes. Below about five the steps start to read; the guide's
                own recipe uses eight. On ``direction="inward"`` it is also bounded
                from above by the patch -- ``n <= 120 x depth``, above which the
                brush derived from the ring step is under ``0.025`` and combs. Both
                walls say so at the call.
            brush: preset name or brush.
            size: brush size override. **Leave it off on either direction and the
                verb sizes its own brush from its own step.** On a band that is
                ``3 x extent / n``; measured on a band ``0.80x0.40`` at ``n=8``, a
                step of ``0.050``, the profile's one-step ripple runs ``0.014`` at
                one step and ``0.015`` at one and a half -- the bars -- against
                ``0.008`` at two steps and ``0.007`` at three, and past about five
                steps the last passes bury the first and the ramp stops reaching its
                own ends. On ``direction="inward"`` leave it off: the verb sizes
                the brush from its own ring step, because a preset's default is
                five steps wide on a patch a painter would call a glow and fills it
                flat. Measured on an ellipse ``0.72x0.24`` at ``n=7``, opacity
                ``0.5``, bristle -- the share of the patch within ``0.06`` of the
                centre value: **44%** at the preset's ``0.11``, **12%** at
                ``0.05``, **0.2%** at ``0.03``. Three ring steps is the usable
                middle and is what it picks.
            opacity: each pass is laid part-transparent so that the passes blend
                into each other rather than replacing one another. It is not a
                quietness dial -- see above; overlapping passes accumulate.
            direction: which way the passes run. ``"axis"``, the default, runs them
                along the band's own long axis so a wide low band is swept the wide
                way. ``"inward"`` runs them *round* the place, stepping toward its
                centre, which is the centred fall-off above -- a value falling off
                from a point rather than across an edge. Otherwise as
                :meth:`block_in`: a name or a number of degrees.
            overhang: how far past the band each pass runs, in brush widths -- past
                the **ends of the pass**, which turn with ``direction`` exactly as
                they do in :meth:`block_in`. A centred passage has no ends to run
                past, so ``"inward"`` ignores this.
            pressure: pressure profile for each pass. ``"even"`` by default: a taper
                at both ends of every pass would print the band's own edges back
                into the passage.
            solid: lay the passes as solid paint -- ``load=1.0`` and
                ``load_falloff=0.0`` -- the same pair :meth:`block_in` takes under
                this name. **A band lays its passes that way already**, and
                ``"inward"`` has defaulted ``load_falloff=0.0`` since it was written,
                so this argument now moves nothing on a band and only an inward
                pass's ``load`` -- the brush's own, `0.9` on the default `bristle`,
                worth `0.005%` of a patch against `0.012%`. It is kept because
                scripts type it. A passage is many wide passes, which is where a
                brush running dry shows as a stripe down one side of it, and that is
                now the default rather than the thing to remember. To starve a
                passage on purpose, name ``load=`` or ``load_falloff=`` beside the
                call: those still win.
            edge: ``"ragged"``, the default -- each pass breaks past the band the way
                a brush does. ``"hard"`` masks every dab to the band, so **no paint
                lands outside it**: this is :meth:`block_in`'s own setting, and it is
                the answer to a wide passage laid at an angle, whose auto brush is
                measured across the band's bounding box and can paint three times the
                band's area. (``"clean"`` is a :meth:`block_in` word: a passage has no
                contour to draw.)
            clip: a place, or a list of places, outside which none of the passage's
                paint may land, as on :meth:`stroke`. ``edge="hard"`` is this clip
                pointed at the band itself; this one points it somewhere else.
            note: recorded in the log.
            feather: how far inside a held band its edge breaks, as on
                :meth:`stroke`: **0.002** left off, ``0`` for an edge cut on the line
                -- a horizon ruled on purpose, say.

        Returns:
            The records for every pass laid down.
        """
        if int(n) < 2:
            raise ValueError(
                f"scumble(n={n!r}) needs at least two passes -- a passage from one "
                f"value to another is at least two. Eight is the usual number."
            )
        if edge not in ("ragged", "hard"):
            raise ValueError(
                f"scumble(edge={edge!r}) is 'ragged' -- the passes break past the "
                f"band, the default -- or 'hard', which masks every dab to the band "
                f"so no paint lands outside it. 'clean' is block_in's: it draws a "
                f"contour along the outline, and a passage has none to draw."
            )
        place = as_place(band)
        n = int(n)
        held = _mass_hold(place, edge, clip)
        feather = _held_feather(feather, bool(held), "scumble")
        if solid:
            brush_overrides = {"load": 1.0, "load_falloff": 0.0, **brush_overrides}
        b, inward, paths = self._scumble_paths(place, n, brush, size, opacity,
                                               direction, overhang, brush_overrides,
                                               held=held)
        if inward:
            return self._scumble_inward(place, color_a, color_b, n, b, pressure, note,
                                        paths, clip=held, feather=feather)

        records: list[StrokeRecord] = []
        laid = 0
        with self._one_call("scumble", place):
            for path, flipped in paths:
                t = laid / max(n - 1, 1)
                records.append(self.stroke(
                    path, brush=b, color=self.palette.mix(color_a, color_b, min(t, 1.0)),
                    pressure=_canvas_order_pressure(pressure) if flipped else pressure,
                    clip=held, feather=feather,
                    note=note or f"scumble {place.name or 'band'} {laid + 1}/{n}",
                ))
                laid += 1
        return records

    def _scumble_paths(self, place, n: int, brush, size, opacity: float, direction,
                       overhang: float, brush_overrides: dict, stacklevel: int = 3,
                       held=None):
        """The brush a scumble lays, and every pass it would lay -- before any is paint.

        Split out for the reason :meth:`_block_in_paths` is: :meth:`cost`,
        :meth:`preview` and :meth:`rehearse` have to be able to say what a passage
        charges without laying it, and a second copy of *which brush, how many
        passes* is a second answer waiting to disagree with the first. It stays a
        generator for the same reason too -- the pass wander is drawn from the stream
        between the ``stroke()`` calls, so collecting the paths up front would
        reorder it.

        ``held`` is every outline the passage is held inside (:func:`_mass_hold`), which
        the band's spill is measured through: a band laid ``edge="hard"`` lands nowhere
        but the band, and saying otherwise would be a rule firing on its own remedy.

        Returns the brush, whether this is the centred (``"inward"``) case, and the
        paths themselves.
        """
        if direction == "inward":
            # A ring is two or three times the length of a pass across the same patch,
            # and it has no far end to run dry at -- it comes back to where it started.
            # Left to the usual falloff the brush starves half way round and the glow
            # comes out bright on one side, which is not a fall-off from a centre. A
            # default, not an override: `load_falloff=` beside it still wins.
            # The brush comes from the ring step unless the painter named one. A
            # `Brush` handed in carries a size somebody chose, so it counts as named;
            # a preset's name does not, and a preset's default is what fills the patch.
            named = size is not None or isinstance(brush, Brush)
            if not named:
                size = _inward_size(place, n)
            b = self._resolve_brush(brush, size, opacity,
                                    {"load_falloff": 0.0, **brush_overrides})
            _check_inward_brush(self, place, b, n)
            _check_inward_comb(self, place, b, n, named)
            outline = place.closed if isinstance(place, Polygon) else polygon(place).closed
            # In to the middle: half the shorter extent, which is the radius of a round
            # patch and the half-width of a long one, where the ramp lands on its spine.
            depth = _inward_depth(place, b.size)
            return b, True, self._ring_paths(outline, depth / n, n)
        degrees = place.axis if direction == "axis" else _angle_of(direction)
        step = _normal_extent(place, degrees) / n
        # The same mechanism as the inward case, and for the same reason: the passes
        # step `extent / n` apart whatever brush is on them, so the brush and the step
        # are one thing. Left to a preset's default the bristle is whatever it is --
        # 1.5 steps on the band that came back a venetian blind -- and 1 to 1.5 steps
        # is the worst place on the curve. Named, either as `size=` or as a `Brush`
        # carrying one, it is the painter's and is left alone.
        picked = size is None and not isinstance(brush, Brush)
        if picked:
            size = _linear_size(step)
        # And the same pair the inward case takes, for the same reason one step down:
        # a band is many wide passes laid over each other, and a brush running dry
        # along one of them prints a stripe down the passage that the passes after it
        # do not close. The band's own default brush is the one preset that is not
        # already full -- `bristle` at `load=0.9, load_falloff=0.55` -- which is why
        # two committed banded scumbles in three type this clause by hand. Measured on
        # a band `0.10-0.90 x 0.40-0.60`, eight passes, burnt umber to titanium white
        # over `toned_grey`: bare `5.17%` without it and `0.01%` with, ripple `0.0110`
        # against `0.0031`. A default, not an override: `load=` or `load_falloff=`
        # beside the call still wins, which is how a starved band is still asked for.
        b = self._resolve_brush(brush, size, opacity,
                                {"load": 1.0, "load_falloff": 0.0, **brush_overrides})
        _check_linear_brush(self, b, step, n)
        if not _check_scumble_ends(self, place, degrees, b, n, stacklevel=stacklevel):
            # One notice per bloom: the ends check has already said this band paints
            # past itself whenever it fires, and said why.
            _check_band_spill(self, place, b, degrees, step, n, overhang, picked,
                              direction == "axis", held, stacklevel=stacklevel)
        shaped = isinstance(place, Polygon)
        paths = (self._shape_paths(place, degrees, step, b.size * overhang) if shaped
                 else self._angled_paths(place, degrees, step, b.size * overhang))
        return b, False, paths

    def _scumble_inward(self, place, color_a, color_b, n: int, b: Brush,
                        pressure, note: str, paths, clip=None,
                        feather: float = 0.0) -> list[StrokeRecord]:
        """A centred fall-off: ``n`` rings stepping in from the boundary.

        The band version grades edge to edge, which is what a band wants and is not a
        glow. Nine passes over the same round patch, measured in the values view: the
        band steps ``0.90, 0.56, 0.51, 0.23, 0.17`` across the patch and stands within
        ``0.01`` of flat down its middle; these rings step ``0.30, 0.42, 0.86, 0.91``
        from edge to centre and do the same thing whichever way you cut them. A lit
        patch falls off from the *middle* in every direction, and the obvious
        hand-rolled answer -- strokes radiating from a shared centre -- comes back as a
        daisy, because strokes that all start in one place draw the petals of one.

        So the passes go round rather than out: the first runs along the boundary, each
        one after it is the same curve a part-brush further in, and the colour steps one
        part per ring. That is :meth:`sweep`'s geometry, which is already the answer to
        *passes that follow the form rather than combing across it* -- with the colour
        moving as it goes inward.
        """
        records: list[StrokeRecord] = []
        with self._one_call("scumble", place):
            for k, path, flipped in paths:
                records.append(self.stroke(
                    path, brush=b,
                    color=self.palette.mix(color_a, color_b, k / max(n - 1, 1)),
                    pressure=_canvas_order_pressure(pressure) if flipped else pressure,
                    clip=clip, feather=feather if clip else None,
                    note=note or f"scumble inward {place.name or 'patch'} {k + 1}/{n}",
                ))
        return records

    def _ring_paths(self, outline, step: float, n: int):
        """Every ring a centred scumble lays: the same walk as a closed :meth:`sweep`.

        Beside that walk rather than through it, for one reason: the ring's own number
        comes out with it. A centred passage takes its colour from *which* ring it is,
        and a ring that folded in on itself past the middle is dropped rather than
        laid -- so numbering the ones that survive would quietly compress the ramp and
        land the middle colour short of the middle.
        """
        spacing = max(step * 0.6, 0.008)
        spine, ring = _sweep_spine(outline, True, spacing)
        normals = _sweep_normals(spine, None, ring)
        cum = _arc_length(spine)
        length = float(cum[-1])
        for k in range(n):
            off = k * step + self._sweep_wobble(cum, length, step, ring)
            path = _drop_folds(spine + normals * off[:, None], spine, step)
            if path is None:
                continue            # this ring folded in on itself: past the middle
            yield (k, path, False) if k % 2 == 0 else (k, path[::-1], True)

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
        self._snapshot()
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
                    params={"width": float(width), "smooth": bool(smooth),
                            "rng": self._stream_state()},
                )
            )
        except Exception:
            # Same reasoning as stroke(): a failure after the snapshot above must
            # not leave it orphaned against the wrong record.
            self.history.discard_snapshot()
            raise
        self._auto_frame()
        return record

    def erase(self, region=None, note: str = "") -> StrokeRecord:
        """Rub out the drawing, all of it or inside one region or shape.

        **Both drawings**: the graphite in the canvas and the overlay :meth:`guide`
        lays on the view. They are two mechanisms and one word -- a painter redrawing
        an arrangement reaches for ``erase()``, and a scaffolding fan left behind on
        the view puts two convergence points in one look, which is exactly the thing
        the drawing exists to judge. :meth:`unguide` takes the overlay on its own,
        and takes it by ``note``.

        Erase before painting rather than arguing with a line while painting. A line
        the painter has decided is wrong costs nothing to remove and costs a great
        deal to paint around.
        """
        place = as_place(region) if region is not None else None
        self._snapshot()
        self.canvas.erase_sketch(place)
        if place is None:
            self.guides.clear()
        elif self.guides:
            kept = []
            for g in self.guides:
                for piece in _erase_from_lines([g["points"]], place):
                    kept.append({"points": piece, "note": g.get("note", "")})
            self.guides[:] = kept
        record = self.history.add(
            StrokeRecord(
                index=self._index_base + len(self.history.records),
                kind="erase",
                note=note or ("erase" + (f" {place}" if place is not None else " all")),
                params={**_place_params(place), "rng": self._stream_state()},
            )
        )
        # erase() visibly changes the rendered canvas (it clears the sketch
        # channel, which the thumbnail includes) the same way stroke() and pencil()
        # do, so it belongs in the time-lapse the same way they are.
        self._auto_frame()
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

    def guide(self, points, note: str = "") -> list[tuple[float, float]]:
        """Draw a line on **the view** rather than on the canvas. Paint cannot bury it.

        :meth:`mark` is this for a point. A landmark survives the whole painting
        because it is a point held beside the canvas and drawn onto every look; a
        graphite line does not, because it is in the canvas and paint is allowed to
        cover it. So the method's own order costs a second drawing pass: landmarks
        first, pencil after the far masses, near masses on top -- and in one painting
        the bench tops buried the first drawing, so the pass before the pots redrew
        every pot and the can before painting them. Nine of eleven paintings never
        made that second pass, and the two passages one painter never drew were the
        two it named weakest.

        This is the same mechanism along a path. It touches no paint, no wetness and
        no graphite channel: :meth:`look` draws it over the render, ``look(sketch=False)``
        leaves it out with the drawing, and :meth:`export` never sees it, so the
        arrangement drawn at step 1 is still there at step 7 and out of the picture
        at the end. It is not a stroke and is not charged.

        Use :meth:`pencil` for a drawing that *should* go under the paint and show
        through it -- the underdrawing is part of the painting, and this is not.

        It comes off with :meth:`unguide`, which takes the whole overlay or one
        ``note`` of it, and with :meth:`erase`, which takes the graphite and the
        overlay together the way redrawing an arrangement wants.

        Args:
            points: normalised (x, y) points. One point is a dot.
            note: a short label drawn beside the line's first point.

        Returns:
            The path, so it can be used inline.

        Example::

            for shelf in (0.38, 0.55, 0.72):
                s.guide([(0.05, shelf), (0.95, shelf - 0.04)], note="bench")
            s.look()                        # still there after the masses go on
        """
        pts = np.atleast_2d(np.asarray(points, dtype=np.float64))
        if pts.size == 0 or pts.shape[1] != 2:
            raise ValueError(
                f"guide() needs at least one point, as (x, y) pairs -- "
                f"guide([(0.2, 0.4), (0.7, 0.45)]) -- and got shape {pts.shape}."
            )
        path = [(float(x), float(y)) for x, y in pts]
        if not all(math.isfinite(v) for xy in path for v in xy):
            raise ValueError(f"guide() was given a point that is not finite: {path}")
        self.guides.append({"points": path, "note": str(note)})
        return path

    def unguide(self, note: str | None = None) -> int:
        """Rub out the overlay drawing, or the parts of it carrying ``note``.

        Returns how many paths went. The whole of it is the usual thing to want, once
        the paint has taken over from the drawing. :meth:`erase` takes the overlay
        as well as the graphite, which is the call to reach for when the whole
        arrangement is being redrawn; this one is for taking back one labelled part
        of it and leaving the rest.
        """
        before = len(self.guides)
        if note is None:
            self.guides.clear()
        else:
            key = str(note)
            self.guides[:] = [g for g in self.guides if g.get("note") != key]
        return before - len(self.guides)

    # -- canvas state -----------------------------------------------------------
    # -- shapes, in this canvas's own units --------------------------------------
    @property
    def aspect(self) -> float:
        """The canvas's width over its height. ``1.333`` on a 1024x768.

        The number behind the one unit trap in the whole API. Coordinates are
        normalised on *both* axes, so ``0.1`` across is 102 pixels here and ``0.1``
        down is 77: a distance in x and the same distance in y are not the same
        distance. Brush sizes are a fraction of the canvas's **long side**, which is
        why a brush is round and an ``ellipse(p, 0.1, 0.1)`` is not.
        """
        return self.canvas.width / self.canvas.height

    def circle(self, place, r: float | None = None, wobble: float = 0.0,
               points: int = 15, seed: int = 0, rotate: float = 0.0,
               steps: int = 48, name: str = "") -> Polygon:
        """A mass that is round on *this* canvas, not merely round in coordinates.

        ``ellipse(p, 0.1, 0.1)`` is an oval on any canvas that is not square, because
        the two radii are in different units. This takes one radius, in x, and works
        the other out from :attr:`aspect` -- so what comes back is round in pixels,
        which is what "round" meant::

            s.circle((0.42, 0.55), 0.09)                 # a round lobe
            s.circle(cell("D5"))                         # the biggest circle that fits
            s.circle((0.42, 0.55), 0.09, wobble=0.25)    # round, but nobody drew it

        Args:
            place: a point ``(x, y)``, or a region to sit inside.
            r: the radius across, as a fraction of the canvas width. Leave it out to
                take the largest circle the place holds.
            wobble: above zero, the outline wanders by this fraction of the radius
                and what comes back is a :func:`~easel.regions.blob` -- a round mass
                with a silhouette nobody drew by hand.
            points: how many points a wobbled outline gets.
            seed: the shape's own seed, not the session's. The same seed is the same
                silhouette.
            rotate: degrees, clockwise. Only visible on a wobbled outline.
            steps: how many points an unwobbled outline gets.
            name: shows up in the log.

        Returns:
            A :class:`~easel.regions.Polygon`, as :func:`~easel.regions.ellipse` and
            :func:`~easel.regions.blob` return.
        """
        if wobble:
            return blob(place, r, wobble=wobble, points=points, seed=seed,
                        rotate=rotate, name=name, aspect=self.aspect)
        return ellipse(place, r, rotate=rotate, steps=steps, name=name,
                       aspect=self.aspect)

    def dry(self, amount: float = 1.0, region=None) -> StrokeRecord:
        """Dry the canvas so the next paint covers instead of mixing.

        All of it, or inside one region or shape -- a shaped mass can be dried and
        painted over without drying the wet neighbour it has to blend into.
        """
        place = as_place(region) if region is not None else None
        # Snapshot before the mark, like every other canvas-mutating call: without
        # this, undo() after a dry() pops the *previous* paint action's snapshot
        # while only dropping the dry record, desyncing the canvas from the log.
        self._snapshot()
        self.canvas.dry(amount, place)
        return self.history.add(
            StrokeRecord(
                index=self._index_base + len(self.history.records),
                kind="dry",
                note=f"dry {amount:.2f}" + (f" in {place}" if place is not None else ""),
                params={"amount": float(amount), **_place_params(place),
                        "rng": self._stream_state()},
            )
        )

    def undo(self, n: int = 1) -> int:
        """Scrape back ``n`` **log records**. Returns how many were actually undone.

        Records, not marks you paid for: a ``dry``, a ``pencil`` line and an
        ``erase`` are free against the budget and are entries in the log like any
        other, so ``undo(1)`` after a ``dry()`` takes back the drying and leaves the
        stroke before it alone. :meth:`replay` counts the same way, and so does
        :meth:`log`; what the budget counts is :attr:`stroke_count`. ``s.log()``
        prints the records in order, which is where to look before undoing several.

        This is not free and it is not the usual repair. Painting over a mistake is
        almost always the better move, and it is what a painter does.
        """
        if n <= 0 or not self.history.records:
            return 0
        depth = self.history.undo_depth
        if depth >= n:
            undone = self.history.records[-n:]
            unwind = self.history.pop_snapshots(n)
            if unwind is not None:
                # Newest first: a snapshot holds the state before its own mark, over
                # the box that mark could reach, so the marks after it have to be
                # put back before it is.
                for snap in unwind:
                    self.canvas.restore(snap)
                # And the generator, to where it stood before the first undone mark's
                # call began. The undone marks may have been the passes of a mass, and
                # a mass draws its wander from the stream: left where it was, the next
                # mass drew from a stream a clean rebuild never produces.
                self._restore_stream(undone[0])
                if self.timelapse and not self._film_from_log:
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
        # Without frames when this painting's film comes from the log anyway: a
        # frame is the dearest thing a mark does that is not paint, and every one the
        # rebuild made would be thrown away with the file's next save.
        self._adopt(self.replay(upto=keep, frames=False if self._film_from_log else None))
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
            sketch: show the drawing -- the pencil underdrawing the paint has not
                covered, and the overlay :meth:`guide` draws. ``False`` hides both.
            marks: draw the landmarks, on both panels. ``False`` hides them and their
                labels, which sit over the details they name. ``easel look
                --no-marks --no-sketch`` is the same clean view from a shell.

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
            guides=self.guides,
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
            marks=self.marks if show_marks else None, guides=self.guides, **kwargs
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
        return self._next_free_path("rehearse" if self._is_trial else prefix)

    def _next_free_path(self, prefix: str) -> Path:
        """The next free ``<prefix>_NNN.png`` under :attr:`out_dir`.

        Numbered from what is on disk rather than from a counter, because a counter
        only knows about the session holding it. A rehearsal has nowhere to keep one
        at all -- it runs on a copy of the session and the copy is thrown away, so
        ``easel run --rehearse`` restarted at ``001`` every time, over the painting's
        own ``look_001.png`` and then over the previous rehearsal. The same defect
        reaches further than rehearsals: **two sessions sharing an ``out_dir``
        overwrite each other**, each counting from 1 in ignorance of the other. One
        painter ran four of the nine exercises from one script, got one file written
        four times, and lost all four images in the one part of the method that is
        *only* looking. A directory is the thing both sessions can see, so the
        directory is what the number comes from.
        """
        return self.out_dir / f"{prefix}_{_highest_numbered(self.out_dir, prefix) + 1:03d}.png"

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
                :meth:`sweep` argument, drawn as the ground that sweep would cover;
                or a passage, ``band=`` with ``color_a=``, ``color_b=`` and any
                :meth:`scumble` argument; or a burial, ``cover=`` and any
                :meth:`cover` argument. A film is a mark with ``glaze=True`` and the
                verb's own defaults written out, since a mark's are a stroke's --
                ``{"points": band, "glaze": True, "brush": "round_soft", "color":
                "warm", "opacity": 0.18}`` is ``glaze(band, "warm")``. A single path
                or shape is also accepted.
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
        vary: dict | None = None,
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
                twenty passes, and worth trying on the scrap of canvas first. **A
                whole pass is a plan**: its masses, passages, marks and films, in the
                order they are laid, rehearsed here as one.
            reference: shown alongside, cropped to the same place.
            region: crop both panels, enlarged. Use one -- the point is feature scale.
            grid: as :meth:`look`.
            values: greyscale.
            path: where to write. Defaults to ``out_dir/rehearse_NNN.png``.
            scale: long-side pixel limit. With ``vary``, the whole sheet's.
            vary: settings to try the same marks at, ``{argument: [values]}`` --
                one panel per combination, in place, labelled with what it is::

                    s.rehearse(plan, region=span("D4", "F6"),
                               vary={"size": [0.02, 0.035, 0.05, 0.08]})

                Every entry of the plan takes the setting, which is what makes it a
                calibration rather than a plan: it is usually one mark. Four sizes
                used to be four rehearsals, each rendering the whole canvas and
                none of them next to the others -- and a question about size is a
                question only comparison answers. Free, like any rehearsal, and it
                spends no stream: each panel is its own copy, seeded as the next
                marks of the real painting, so whichever one is chosen lands as it
                was shown. Two arguments vary together as their combinations, which
                is why there is a ceiling on how many.
        """
        if vary:
            return self._rehearse_sheet(strokes, vary, reference=reference,
                                        region=region, grid=grid, values=values,
                                        path=path, scale=scale)
        trial = self._trial_session()
        for kind, spec in self._plan_specs(strokes):
            trial._lay(kind, spec)
        self._adopt_notices(trial)

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

    def _rehearse_sheet(self, strokes, vary: dict, reference=None, region=None,
                        grid: bool | str = False, values: bool = False,
                        path=None, scale: int | None = DEFAULT_LOOK_SIZE) -> Path:
        """:meth:`rehearse` with ``vary``: one panel per setting, in one image."""
        settings = _vary_settings(vary)
        ref_img = None if reference is None else load_reference(reference)
        columns = min(len(settings), 4)
        panel = None if scale is None else max(int(scale) // columns, 200)
        panels: list[tuple[str, Image.Image]] = []
        for setting in settings:
            trial = self._trial_session()
            for kind, spec in self._plan_specs(strokes):
                trial._lay(kind, dict(spec, **setting))
            # Every panel's notices, not the first panel's: which settings the engine
            # has something to say about is half of what the sheet is being asked.
            self._adopt_notices(trial)
            panels.append((
                " ".join(f"{k}={_setting_text(v)}" for k, v in setting.items()),
                render_look(trial.canvas, scale=panel, grid=grid, values=values,
                            region=region, reference=ref_img, marks=self.marks or None),
            ))
        return save_look(label_sheet(panels, columns=columns),
                         self._look_path(path, "rehearse"))

    def _lay(self, kind: str, spec: dict) -> list[StrokeRecord]:
        """Paint one plan entry on this session.

        The single dispatch from a plan entry to the call that lays it, so that what
        :meth:`rehearse` tries on the scrap of canvas and what :meth:`paint` commits
        cannot drift apart -- they are the same three lines, one on a trial session
        and one on the real one.
        """
        # ``edge`` is dropped for a sweep, whose edge is passed positionally, and
        # kept for the place-filling verbs, where it is the ragged-or-clean contour.
        drop = ("label", "place", "edge") if kind == "sweep" else ("label", "place")
        kwargs = {k: v for k, v in spec.items() if k not in drop}
        if kind == "mass":
            return self.block_in(spec["place"], **kwargs)
        if kind == "sweep":
            return self.sweep(spec["edge"], **kwargs)
        if kind == "scumble":
            return self.scumble(spec["place"], **kwargs)
        if kind == "cover":
            return self.cover(spec["place"], **kwargs)
        return [self.stroke(**kwargs)]

    def paint(self, plan, note: str = "") -> list[StrokeRecord]:
        """Paint a plan -- marks, masses and sweeps -- exactly as it was checked.

        :meth:`cost`, :meth:`preview` and :meth:`rehearse` all read the same plan.
        This paints it. Before, a mass or a sweep in a plan had to be dispatched to
        :meth:`block_in` or :meth:`sweep` by hand once it had been approved, which
        is the one place a plan can drift from the thing that was checked: the
        rehearsal is of the plan, the painting is of the retyping.

        The four together are the loop the guide asks for, and no line of the plan
        is written twice::

            plan = [{"shape": blob(cell("D5")), "brush": "bristle", "color": "dark"},
                    {"edge": ridge, "into": "down", "depth": 0.2, "color": "shadow"},
                    {"points": [(0.2, 0.6), (0.6, 0.55)], "brush": "liner"}]

            s.cost(plan)                    # 34 -- what it charges
            s.preview(plan, reference=ref)  # where it goes
            s.rehearse(plan, region=...)    # what it will look like
            s.paint(plan)                   # the same plan, now paid for

        Because a rehearsal is seeded as if it were the next marks of the real
        painting, rehearsing a plan and then painting it -- with nothing in between
        -- lands it pixel for pixel as it was rehearsed.

        Args:
            plan: as :meth:`preview`. One entry or a list; marks, masses and sweeps
                may be mixed, and are painted in the order given.
            note: recorded against every entry that does not carry a note of its own.

        Returns:
            The records for every stroke laid down, masses flattened in with marks.
        """
        records: list[StrokeRecord] = []
        for kind, spec in self._plan_specs(plan):
            if note and not spec.get("note"):
                spec = dict(spec, note=note)
            records.extend(self._lay(kind, spec))
        return records

    def cost(self, strokes, share: float = 0.25) -> int:
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

        When the session carries a ``budget``, a plan that would eat more than
        ``share`` of what is left says so as a warning. That is the number a painter
        cannot feel: twelve strokes sounds small until it is most of what remains.

        Args:
            strokes: as :meth:`preview` -- marks, masses and sweeps, one or a list.
            share: how much of the remaining budget one plan may take before it is
                flagged. ``0`` never flags. Ignored without a budget.

        Returns:
            The number of strokes painting the plan would charge.
        """
        priced = self.cost_of(strokes)
        total = sum(n for n, _ in priced)
        self._flag_budget(total, share, priced)
        return total

    def cost_of(self, strokes) -> list[tuple[int, str]]:
        """What each entry of a plan charges, and why: ``[(strokes, reason), ...]``.

        The breakdown :meth:`cost` adds up and :meth:`cost_line` prints, in the order
        the plan is written. A mark's reason is empty -- one stroke is one stroke.
        Nothing is painted and nothing is logged, the same as :meth:`cost`.
        """
        return [self._plan_price(kind, spec)
                for kind, spec in self._plan_specs(strokes)]

    def cost_line(self, strokes) -> str:
        """What a plan costs **and why**, as a line to print. Warns about nothing.

        :meth:`cost` hands back a number, and a number on its own sends a painter to
        redesign the shape when the fix is usually the call. The three ways a mass
        runs away are all visible from the geometry and all have a lever:

        - **crossing a direction** doubles it, and one mass rarely needs two;
        - **the passes step across the bounding box**, so a long curved shape pays
          for the box its curve sweeps out and a wider brush is the cheapest fix;
        - **a concave shape cuts every pass** into the pieces really inside it.

        ::

            print(s.cost_line(plan))
            # 74 strokes -- 31% of the 240 left of a 300-stroke budget
            #   68  2 directions, 34 passes each stepping across 1.10 of the canvas
            #    6  6 passes, 0.12 deep

        Args:
            strokes: as :meth:`cost` -- marks, masses and sweeps, one or a list.

        Returns:
            One line for the plan, and one more for every entry that costs more than
            a painter can count: a mass or a sweep.
        """
        priced = self.cost_of(strokes)
        total = sum(n for n, _ in priced)
        head = f"{total} strokes"
        left = self.remaining
        if left is not None and left > 0:
            head += (f" -- {total / left:.0%} of the {left} left of a "
                     f"{self.budget}-stroke budget")
        elif left is not None:
            head += f", and the {self.budget}-stroke budget is already spent"
        return "\n".join([head] + [f"  {n:3d}  {why}" for n, why in priced if why])

    def _flag_budget(self, total: int, share: float, priced=()) -> None:
        """Warn when a plan takes more than ``share`` of what the budget has left.

        A warning rather than a refusal: the budget is the painter's plan for the
        picture, and a painting that needs forty more strokes than it planned should
        get them and be told, not be stopped halfway with the masses unfinished.

        It says what the biggest entry is *doing* as well as what it costs. A number
        four to twelve times what a painter would have guessed is nearly always one
        of three things -- a crossed direction, passes stepping across a bounding box
        much bigger than the mass, a concave shape cutting every pass into pieces --
        and all three are cheap to fix once named. See :meth:`cost_line`.
        """
        left = self.remaining
        if left is None or share <= 0:
            return
        worst = max((p for p in priced if p[1]), key=lambda p: p[0], default=None)
        because = f" Its {worst[0]}-stroke entry: {worst[1]}." if worst else ""
        if left <= 0:
            self._notify(
                "budget-spent",
                f"This plan costs {total} strokes, and the {self.budget}-stroke "
                f"budget is already spent.{because}",
                stacklevel=3,
            )
        elif total > share * left:
            self._notify(
                "budget-share",
                f"This plan costs {total} strokes -- {total / left:.0%} of the "
                f"{left} left of a {self.budget}-stroke budget.{because}",
                stacklevel=3,
            )

    def _plan_cost(self, kind: str, spec: dict) -> int:
        """What one plan entry charges. :meth:`_plan_price` without the reason."""
        return self._plan_price(kind, spec)[0]

    def _plan_price(self, kind: str, spec: dict) -> tuple[int, str]:
        """Price one plan entry by walking its passes, not by laying them -- and say why.

        On a trial session, whose generator holds a *copy* of the real stream: the
        pass wander is drawn while counting and would otherwise be spent, changing
        the painting that followed. The count itself does not depend on it.

        The reason comes off the same walk rather than out of a second measurement,
        so what it describes is the passes that were actually counted. A mark has
        none: one stroke is one stroke, and saying so on every entry would be noise.
        """
        if kind == "stroke":
            return 1, ""
        if kind == "cover":
            # A burial is a block-in with the recipe already set, so it is priced as
            # the block-in it lays -- through the same arithmetic, not beside it.
            # The dry is free and is not a mark.
            return self._plan_price("mass", _cover_as_mass(spec))
        trial = self._trial_session()
        b = trial._resolve_brush(spec.get("brush", "bristle"), spec.get("size"),
                                 spec.get("opacity"), {})
        density = float(spec.get("density", 1.0))
        if kind == "mass":
            # A clean edge fills the shape inset by half a brush and then draws the
            # contour, so it is priced on the inset shape plus the one contour pass.
            edge = spec.get("edge", "ragged")
            place = spec["place"]
            fill = _clean_fill(place, b.size * 0.5) if edge == "clean" else place
            direction = spec.get("direction")
            over = _mass_overhang(edge, spec.get("overhang"))
            laid = sum(1 for _ in trial._block_in_paths(
                fill, b, direction, density, over))
            if direction is None:
                # The same line block_in gives, from the same walk: a rehearsal that
                # comes back charging 124 for a pass budgeted at 40 should say why.
                _check_default_direction(trial, fill, b, density, over,
                                         stacklevel=5)
            else:
                _check_direction_sequence(trial, fill, b, direction, density,
                                          spec.get("overhang"), stacklevel=5)
            self._adopt_notices(trial)
            return (laid + int(edge == "clean"),
                    _mass_reason(fill, b, direction, density, laid))

        if kind == "scumble":
            place = spec["place"]
            n = int(spec.get("n", 8))
            b, inward, paths = trial._scumble_paths(
                place, n, spec.get("brush", "bristle"), spec.get("size"),
                float(spec.get("opacity", 0.5)), spec.get("direction", "axis"),
                float(spec.get("overhang", 0.35)), _brush_overrides_of(spec),
                stacklevel=5,
                held=_mass_hold(place, spec.get("edge", "ragged"), spec.get("clip")))
            laid = sum(1 for _ in paths)
            self._adopt_notices(trial)
            if inward:
                why = f"{laid} rings stepping in from the boundary"
                if laid < n:
                    why += f", of the {n} asked for: the rest fold past the middle"
            else:
                why = f"{laid} passes stepping across {place.name or 'the band'}"
                if laid != n:
                    why += f", not the {n} asked for: the outline cuts them"
            return laid, why

        # A sweep works its pass count out from the depth before any geometry is
        # walked, so the quote goes through the same arithmetic the painted one does
        # -- including its refusals, so a plan that cannot be swept says so when it
        # is priced rather than when it is paid for.
        edge = spec["edge"]
        depth, step, n_passes, cross = trial._sweep_passes(
            b, spec.get("depth", 0.2), spec.get("passes"), spec.get("cross"), density)
        laid = sum(1 for _ in trial._sweep_paths(
            edge.closed if isinstance(edge, Polygon) else edge,
            step, n_passes, depth, cross, spec.get("into"), spec.get("closed")))
        why = f"{min(n_passes, laid)} passes, {depth:.2f} deep"
        if cross is not None and laid > n_passes:
            why += f", and {laid - n_passes} more crossing them at {abs(cross):.0f} degrees"
        self._adopt_notices(trial)
        return laid, why

    def scratch(self, count_only: bool = False) -> Session:
        """A throwaway copy of this session: the painter's scrap of canvas.

        Everything painted on it lands exactly where it would land on the real
        painting -- the strokes are seeded as if they were the next marks of this
        session -- but the canvas is a copy and the history starts empty, so nothing
        is committed and :attr:`stroke_count` counts only what the trial itself laid.

        :meth:`rehearse` is this for a plan. This is it for a whole pass: ``easel run
        --rehearse`` runs a script against one of these, looks at the result and
        prints what it would cost, and then throws it away.

        ``count_only=True`` is the same copy with **the pixel work skipped**: every
        pass is worked out, every stroke is logged, and not one dab is stamped. The
        price and the post-pass check come back in a second or two instead of three
        minutes, and there is nothing to look at.

        It exists because :meth:`cost` prices one ``block_in`` or one ``sweep``, and
        a painter's own helper that calls a dozen verbs had no price at all short of
        painting it. One budgeted a row of thirteen pots at about 100 strokes,
        rehearsed it at **220 against 142 left**, and rebuilt it from strokes at 108
        -- three renders of a pass that was never going to be laid. The count is
        exact rather than an estimate: pass geometry is settled before anything is
        stamped, so a counted pass and a painted one log the same number of strokes,
        the same paths and the same brushes. ``tests/test_paintings.py`` holds that
        against this repository's own painting scripts.

        What it does not have is paint -- graphite is not paint and is still drawn,
        being free against the budget and cheap to lay. :meth:`look`, :meth:`sample`
        and :meth:`compare` on a counted copy read the canvas it started from, every
        record's ``paint`` is nought, and :meth:`report` leaves out its ground line
        rather than reporting the canvas it borrowed. A film given ``to_value=`` is
        priced but not solved, and says so once: the search measures the paint under
        the film, a counted run has laid none of its own pass, and an out-of-reach
        value raises when it is painted. The count is still exact -- a film costs one
        stroke at any opacity -- and whether the value is in reach is a question for
        ``--rehearse``. Rehearse for real when the question is what it
        looks like; count when the question is what it costs::

            price = s.scratch(count_only=True)
            paint_the_pots(price)                       # the helper, whole
            print(price.spent, "strokes, of", s.remaining, "left")
            print(price.report(since=0))
        """
        trial = self._trial_session()
        trial._counting = bool(count_only)
        return trial

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
        # Copies, not the painting's own: a rehearsed pass runs the prelude and its own
        # mixtures, landmarks and guides, and while the three were shared every one of
        # them was left behind on the painting. Nothing saved the painting after a
        # rehearsal, so nothing showed it -- until a rehearsal had to save what its
        # check said (`reports`), and then a mixture tried on the scrap of canvas would
        # have gone into the file with it.
        trial.palette = self.palette._copy()
        trial.history = History()
        trial.out_dir = self.out_dir
        trial.budget = self.budget
        trial.timelapse = False
        trial._is_trial = True
        # The painting's own last look, so `look(diff=True)` inside a rehearsed pass
        # tints what the pass would change. A trial starting with none could only
        # diff a rehearsal against itself, which is to say against nothing -- and
        # what a pass would change is the one question a rehearsal exists to answer.
        # Shared rather than copied: `render_look` reads it and `look` replaces it,
        # neither writes into it, and the trial is thrown away regardless.
        trial._last_look = self._last_look
        trial.marks = dict(self.marks)
        trial.guides = [dict(g) for g in self.guides]
        # A tuple, so the trial deciding it has been told does not tell the painting:
        # a rehearsed pass gets the same answer the paid pass will get.
        trial._banding_told = self._banding_told
        trial._preparation = self._preparation
        trial.assisted = []
        trial._index_base = self._index_base + len(self.history.records)
        trial._stream_mark = None
        trial._call_verb = ""
        trial._call_boxed = False
        trial._spent_base = self.spent
        # The log behind that count, for the rules that read across passes. Same
        # marks, kept as records rather than as a number; concatenated rather than
        # taken from `self.history` alone so that a scratch of a scratch carries the
        # whole painting and not just the layer under it.
        trial._prior = self._prior + self.history.records
        trial._counting = self._counting
        trial._uncounted = []
        # Its own, empty: a rehearsal says what the paid pass will say, and it says
        # it about the copy. Carrying the painting's notices in would have `easel run
        # --rehearse` print every notice the painting has ever given.
        trial._notices = []
        # And no reports: what a rehearsal was told is kept on the painting, by the
        # shell or the server that ran it. See :meth:`_keep_report`.
        trial._reports = []
        # The plan itself is carried, because a rehearsal is meant to say what the paid
        # pass will say and every line the plan adds to the check is one of those. It
        # is immutable, so a trial that re-declares its own plan leaves the painting's
        # alone -- the same reason `_banding_told` is passed as a tuple.
        trial._plan = self._plan
        trial._clip_memo = self._clip_memo
        trial._film_call = ""
        trial._solving = False
        trial._opened = None
        # A rehearsal records no frames at all, and says so (`_no_frames_here`).
        trial._film_from_log = False
        trial._load_notices = []
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
                _check_plan_keys("stroke", spec)
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
        """Split what ``preview`` and ``rehearse`` accept into the calls that lay them.

        A plan entry is described the way the call that lays it is. A mark is a path,
        or a dict of :meth:`stroke` arguments. A dict with ``shape=`` (or ``region=``)
        and any :meth:`block_in` argument is a **mass**; with ``edge=`` and any
        :meth:`sweep` argument, a **sweep**; with ``band=`` -- or a place and the two
        colours a passage steps between -- a **scumble**; with ``cover=``, a burial.
        One list holds all five, so a plan is previewed, rehearsed and painted
        without being rewritten in between, which is when a plan drifts.

        Until this took the last two, a scumble could not be planned, priced,
        previewed or rehearsed at all -- and a scumble-shaped entry carrying
        ``shape=`` was **priced as a block-in**, quoting 5 where the call lays 8,
        raising only when ``paint()`` reached the keys block_in does not take.
        """
        if isinstance(entries, (dict, Polygon, Region)) or _is_path(entries):
            entries = [entries]
        out: list[tuple[str, dict]] = []
        for entry in entries:
            if isinstance(entry, (Polygon, Region)):
                out.append(("mass", {"place": as_place(entry)}))
                continue
            if not isinstance(entry, dict) or "points" in entry:
                out.append(("stroke", self._stroke_specs([entry])[0]))
                continue
            spec = dict(entry)
            if "cover" in spec:
                # The verb names itself, because cover's own first argument is the
                # generic `place` and a plan needs a word that says which call it is.
                kind, place = "cover", spec.pop("cover")
            elif "band" in spec or (("shape" in spec or "region" in spec)
                                    and ("color_a" in spec or "color_b" in spec)):
                kind = "scumble"
                place = spec.pop("band", None)
                if place is None:
                    place = spec.pop("shape", spec.pop("region", None))
            elif "shape" in spec or "region" in spec:
                # Tested before the sweep branch, because ``edge`` means two things:
                # the boundary a sweep follows, and the ragged-or-clean contour of a
                # place being filled. A ``shape``/``region`` key settles it -- an
                # entry that names the mass is a mass, and its ``edge`` is the
                # contour.
                kind = "mass"
                place = spec.pop("shape", None)
                if place is None:
                    place = spec.pop("region", None)
            elif "edge" in spec:
                kind, place = "sweep", None
            else:
                out.append(("stroke", self._stroke_specs([entry])[0]))
                continue
            _check_plan_keys(kind, entry)
            if place is not None:
                spec["place"] = as_place(place)
            out.append((kind, spec))
        return out

    def _preview_entry(self, kind: str, spec: dict, index: int) -> dict:
        """What the overlay needs, whichever of the five kinds this entry is."""
        if kind in ("mass", "scumble", "cover"):
            return self._preview_mass(spec, index, kind)
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

    def _preview_mass(self, spec: dict, index: int, kind: str = "mass") -> dict:
        """What the overlay needs for a mass: its outline and the brush filling it.

        A passage and a burial fill a place too, so they draw the same way -- with
        their own default brush and their own price, which is the half of this that
        matters: the overlay says what the entry charges, and a scumble charges its
        passes rather than a block-in's.
        """
        place = spec["place"]
        default = {"scumble": "bristle", "cover": "flat"}.get(kind, "bristle")
        b = self._resolve_brush(spec.get("brush", default), spec.get("size"),
                                spec.get("opacity"), {})
        points = (place.closed if isinstance(place, Polygon)
                  else [(place.x0, place.y0), (place.x1, place.y0),
                        (place.x1, place.y1), (place.x0, place.y1), (place.x0, place.y0)])
        label = str(spec.get("label", spec.get("note") or place.name
                              or f"{kind} {index + 1}"))
        if kind in ("mass", "cover"):
            # The same lines block_in gives, here too: the guide already says to
            # preview the inset shape, and these are those sentences with numbers on
            # them. A burial lays a block-in, so it is asked the same.
            edge = spec.get("edge", "hard" if kind == "cover" else "ragged")
            if edge == "clean":
                _check_clean_size(self, place, b, self.canvas, stacklevel=4,
                                  verb="cover" if kind == "cover" else "block_in")
            elif edge == "ragged" and kind == "mass" and isinstance(place, Polygon):
                _check_round_block(self, place, b, self.canvas, stacklevel=4)
        return {"points": points, "width": b.size, "fill": True,
                "label": self._priced(kind, spec, label)}

    def _preview_shape(self, spec: dict, index: int) -> dict:
        """What the overlay needs: the path, the brush's width, and a label."""
        b = self._resolve_brush(
            spec.get("brush", "bristle"), spec.get("size"), spec.get("opacity"),
            {k: v for k, v in spec.items()
             if k not in ("points", "brush", "size", "opacity", "color", "pressure",
                          "glaze", "smooth", "press", "clip", "feather", "solid",
                          "note", "label")},
        )
        # The band stands for how wide the mark will be, and on a round tip that now
        # depends on the pressure it is planned with -- a lone stamp most of all.
        dabs = int(spec.get("press", 1)) if len(spec["points"]) == 1 else 32
        width = b.size * press_width(b, spec.get("pressure", "taper"), dabs)
        return {"points": spec["points"], "width": width,
                "label": str(spec.get("label", spec.get("note", "") or index + 1))}

    # -- measuring --------------------------------------------------------------
    def sample(self, place=None, rendered: bool = False) -> np.ndarray:
        """The colour already on the canvas at a place, ready to paint with.

        Returns the engine's own linear ``float32`` array, which is what the palette
        and every colour argument take untouched::

            s.palette["sky_here"] = s.sample(halo_ring)      # matches what is there
            s.stroke(path, "round_soft", s.sample(cell("B2")))

        A halo's outer ring meant to be the sky's own colour, a moon's dark side, a
        repair that has to disappear into what it lands on: each needs the colour
        that is *there*, not the one that was mixed for it eight passes ago and has
        since been scumbled over.

        **It averages what is in the place, which is a trap when the place is a
        cell.** A cell is a rectangle of canvas and a mass rarely fills one, so
        sampling the cell hands back the mass averaged with everything around it --
        a number that reads exactly like a measurement and is not one. Measured on a
        bird planned at ``0.30`` standing in water at ``0.50``: its cell reads
        ``0.501``, its own shape ``0.327``, a region cut inside it ``0.318``. A
        painter checked two masses that way, concluded the engine was laying
        everything ``0.14`` light, and wrote a second probe to find out why; both
        were :meth:`~easel.palette.Palette.at_value` doing what it was asked. **To
        measure a mass, hand it the mass** -- a shape is averaged over itself, and
        the mass you blocked in is a shape you already have. A number that disagrees
        with ``at_value`` by more than a hundredth is almost always the place.

        **A rectangle that holds two masses says so**, because the sentence above was
        read by the painter it was written for and the failure still arrives as a
        number and goes straight into paint. Sampling a rectangle whose own values
        fall into two parts warns and names both -- *67% of it reads about 0.303 and
        33% about 0.564, so the 0.422 this returns is a measurement of neither*. A
        shape is never asked the question: handing one over is the remedy, and a mass
        with a turn in it is spread by design. See :meth:`_check_one_mass`.

        Reading it back by hand is where this goes wrong, and quietly. The canvas
        holds linear light; a plain ``(r, g, b)`` tuple handed to the palette is read
        as sRGB, the same as a hex string is -- so a mean sampled off ``s.canvas.rgb``
        and passed back as a tuple comes back a different colour. Measured on a
        ``toned_grey`` ground, which reads ``0.53``: its own mean, assigned as a
        tuple, reads **0.25**. This hands back the array, which passes through as
        itself.

        The paint is what is sampled, not the view of it: the relief shading that
        ``look`` draws is light on the surface, not pigment in it, and mixing it
        into a colour would bake a highlight into the mixture.

        ``rendered=True`` samples the view instead -- the relief and whatever
        graphite the paint has not buried, the surface ``look()`` and ``export()``
        draw. It is there so the question can be *asked*: a painter whose mass looks
        lighter than the number they mixed it at can put the two side by side in one
        line rather than believing one of them.

            s.palette.value_of(s.sample(mass))                   # the paint
            s.palette.value_of(s.sample(mass, rendered=True))    # the view of it

        **Measured, and the answer is that they agree**: over a mass the two are the
        same to within `0.001` at every combination of load, ground and passage tried
        -- the relief is a *gradient*, so it lifts one side of every ridge and drops
        the other by as much, and that cancels over any area larger than the ridge.
        The numbers and what they were measured on are in ``CALIBRATION.md`` under
        *The paint and the view of it*. Do not reach for this to explain a mass that
        came out wrong; reach for it once, to rule the view out.

        Args:
            place: a name, a region, a 4-tuple or a shape. A shape is averaged over
                the shape itself, not its bounding box. Omitted, the whole canvas.
            rendered: sample the surface as it is drawn -- relief and graphite --
                rather than the pigment. Never what you want for *mixing*.

        Returns:
            A linear ``float32`` array of shape ``(3,)``.
        """
        rgb = self.canvas.composite(impasto=True, sketch=True) if rendered else self.canvas.rgb
        if place is None:
            flat = rgb.reshape(-1, 3)
            mean = flat.mean(axis=0).astype(np.float32)
            self._check_one_mass(flat, mean, "the whole canvas")
            return mean

        spot = as_place(place)
        x0, y0, x1, y1 = self.canvas.region_px(spot)
        window = rgb[y0:y1, x0:x1]
        # Duck-typed on `mask`, the way the canvas itself decides whether a place is
        # a shape or a rectangle.
        maker = getattr(spot, "mask", None)
        if maker is not None:
            inside = maker(self.canvas.width, self.canvas.height)[y0:y1, x0:x1]
            if inside.any():
                # No spread check on a shape: the painter has handed it a mass, which
                # is the whole of what the check would ask them to do, and a mass with
                # a turn in it is spread by design. See `_check_one_mass`.
                return window[inside].mean(axis=0).astype(np.float32)
            # A shape thinner than a pixel, or one drawn entirely off the canvas:
            # its bounding box is the honest answer and is never empty. Still a shape,
            # so still not asked the question.
            return window.reshape(-1, 3).mean(axis=0).astype(np.float32)
        flat = window.reshape(-1, 3)
        mean = flat.mean(axis=0).astype(np.float32)
        named = getattr(spot, "name", "") or (
            "{:.3g},{:.3g} to {:.3g},{:.3g}".format(*spot.bounds))
        self._check_one_mass(flat, mean, named)
        return mean

    def _check_one_mass(self, pixels: np.ndarray, mean: np.ndarray, what: str) -> None:
        """Warn when a sampled rectangle holds two masses, so its mean is neither.

        :meth:`sample` hands back a number that reads exactly like a measurement.
        Over a place that straddles a boundary it is a measurement of nothing on the
        canvas, it arrives silently, and it goes straight into paint: one painter
        sampled a span across a hand for the table under it, got ``0.342`` where the
        table reads ``0.258``, and painted a pale halo above the hand with it.

        The documented remedy -- *to measure a mass, hand it the mass* -- is already
        in :meth:`sample`'s own docstring, and that painter had read it. What the
        engine can add is the thing a painter cannot ask about their own place: **is
        there more than one thing in here?** The place's own pixels answer it, so the
        rule costs one pass over a window that has already been cut.

        Asked of rectangles only, and the numbers behind ``_SAMPLE_SPREAD`` say why:
        a mass handed in whole is spread by its own turn from lit to shadow, and it is
        the answer this warning would give. So a painter who does what the sentence
        says never sees it, and one who samples a cell hears about it before the
        colour is mixed.
        """
        v = linear_to_srgb(luminance(pixels)).ravel()
        if v.size < 16 or float(v.std()) < _SAMPLE_SPREAD:
            return
        cut = _two_ways(v)
        dark, light = v[v <= cut], v[v > cut]
        minor = min(dark.size, light.size) / v.size
        if minor < _SAMPLE_MINOR_SHARE:
            # One thing with something small on it -- a glint, a bean, a signature.
            # It moves the mean by less than the spread suggests, and the mean is
            # still a measurement of the mass.
            return
        here = float(linear_to_srgb(luminance(mean)))
        self._notify(
            "sample-split",
            f"sample({what}) is averaging more than one mass: {dark.size / v.size:.0%} "
            f"of it reads about {dark.mean():.3f} and {light.size / v.size:.0%} about "
            f"{light.mean():.3f}, so the {here:.3f} this returns is a measurement of "
            f"neither. The place is a rectangle of canvas and a mass rarely fills one. "
            f"To measure a mass, hand it the mass -- the shape you blocked in, which "
            f"is a shape you already have.",
            stacklevel=3,
        )

    def compare(
        self,
        reference: str | Path | Image.Image,
        region=None,
        path: str | Path | None = None,
        threshold: float = 0.10,
        near: float = _PLAN_TOUCH,
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
            near: how close two planned places have to be, as a fraction of the
                canvas long side, before the sheet calls them touching. Only used by
                a value plan. Half the narrower brush is the number to want, and a
                plan carries no brushes, so it defaults to ``0.01`` -- about a fine
                brush -- and takes half of yours when you know it.

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

        **Without a photograph, compare against the plan instead.** Hand it a dict of
        ``{place: value}`` -- the value plan a painter writing from their head is
        told to put down in numbers -- and it measures each named place against the
        value it was promised, with the same table and the same sheet::

            s.compare({"upper-band": 0.72, lower: 0.38, near_mass: 0.30})

        The keys are places (a name, a region, a shape) and the values are what
        :meth:`~easel.palette.Palette.value_of` reports, so a plan can be written
        before a stroke is laid and checked after every mass.

        **Two planned values closer than the threshold only matter where the two
        places meet**, and the sheet says which of them do. It used to ask -- three
        of one painting's four close pairs were masses that never met -- and the two
        rounds that followed answered it wrong, the worse of them a pair planned
        ``0.00`` apart that met along its whole far edge. Every place in a plan is a
        rectangle or a shape, so whether two of them overlap or come within ``near``
        of each other is arithmetic, not a question for the painter.
        """
        if isinstance(reference, Plan):
            # The plan the session is already holding, handed straight back: `s.plan()`
            # returns one, so `s.compare(s.plan())` measures the canvas against what
            # was written down, sheet and all. A plan that has to be retyped to be
            # checked is a plan that drifts, and the drift arrives as paint.
            if not reference.values:
                raise ValueError(
                    "compare() was handed a plan with no values in it. Declare them "
                    "first -- s.plan(values={sky: 0.70, water: 0.39}) -- or hand "
                    "compare() the dict itself."
                )
            reference = reference.as_dict()
        if isinstance(reference, dict):
            return self._compare_plan(reference, path=path, threshold=threshold,
                                      near=near)
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

    def _compare_plan(self, plan: dict, path=None, threshold: float = 0.10,
                      near: float = _PLAN_TOUCH) -> Comparison:
        """Measure the canvas against a written value plan. See :meth:`compare`."""
        if not plan:
            raise ValueError(
                "compare({}) was given an empty plan. A value plan is at least one "
                "place and the value you mean to paint it: "
                "s.compare({'upper-band': 0.72, 'D5': 0.38})."
            )
        w, h = self.canvas.width, self.canvas.height
        places: list[tuple[str, np.ndarray, float]] = []
        outlines: list[tuple[str, list[tuple[float, float]]]] = []
        planned = np.zeros((h, w), dtype=np.float32)

        for i, (where, target) in enumerate(plan.items()):
            # The same entry `s.plan(values=)` builds, from the same place: a value plan
            # is written once and read by both, so a mass called `near_mass` in one table
            # is not `place 3` in the other, and a value out of range is refused in one
            # sentence rather than two copies of one.
            entry = planned_place(where, target, i)
            name, poly, value = entry.name, entry.outline, float(entry.value)
            mask = poly.mask(w, h)
            places.append((name, mask, value))
            outlines.append((name, list(poly.closed)))
            # Later places sit in front of earlier ones, as they would be painted.
            planned[mask] = value

        canvas_rgb = self.canvas.to_srgb8(impasto=False)
        result = compare_plan(canvas_rgb, places, threshold=threshold,
                              floor=self.palette.darkest_value)
        # The pairs the plan itself puts within a threshold of each other. Read off
        # the plan rather than the canvas, so the question is asked at plan time, on
        # the empty canvas, which is the one run the guide already tells a painter
        # to make and the moment it is free to answer.
        gap_px = max(float(near) * float(self.canvas.long_side), 0.0)
        result.pairs = sorted(
            ((a, b, abs(va - vb), _masks_meet(ma, mb, gap_px))
             for i, (a, ma, va) in enumerate(places)
             for (b, mb, vb) in places[i + 1:]
             if abs(va - vb) < threshold),
            key=lambda t: t[2],
        )
        plan_grey = Image.fromarray(
            np.clip(planned * 255.0 + 0.5, 0, 255).astype(np.uint8), mode="L")
        sheet = plan_sheet(result, canvas_grey=_grey(canvas_rgb),
                           plan_grey=plan_grey, outlines=outlines)
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
        blocked in on one is partly traced -- the question the protocol reserves for the
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

    def timelapse_gif(self, path: str | Path, fps: float = 8.0, every: int = 1,
                      scale: int | None = None, from_log: bool = False) -> Path:
        """Write the time-lapse as an animated GIF.

        **A session file keeps no frames**, since 0.7.0: they were more than half of a
        painting's file -- 8.8 of 16.1 MB after 171 marks -- for a film a painter makes
        once, at the end. So a session loaded from a file makes its film by
        replaying the log, at the frame size it was created with, which is the film it
        would have recorded: it costs a full repaint rather than a read, and the frames
        are built, written and dropped. A session painted in this process keeps its
        frames in memory and uses them, as it always has.

        Args:
            path: where to write.
            fps: frames per second.
            every: keep every nth frame. A painting of a couple of hundred marks
                makes a couple of megabytes at ``every=1``, and consecutive frames
                differ by one stroke; ``every=3`` is a third of the size and reads
                the same. The finished painting is always the last frame, whatever
                ``every`` would have landed on.
            scale: long side in pixels. On the painting's own frames -- recorded, or
                rebuilt for a session loaded from a file -- this only shrinks them,
                because they are made at :data:`~easel.history.DEFAULT_FRAME_PX`
                unless the session asked for another size. With ``from_log`` it is
                the size they are **built** at, and it defaults to the canvas's own.
            from_log: rebuild the frames by replaying the painting, at any size. The
                whole painting is in the log, so the film can be made at any
                resolution **afterwards** -- which is the answer to a 1440x960
                painting whose frames are 360 px wide, and to one that was painted
                with the time-lapse off altogether. It costs a full repaint, and it
                stores nothing.

        Example::

            s.timelapse_gif("painting.gif", every=3, scale=240)   # small enough to send
            s.timelapse_gif("big.gif", from_log=True, scale=960)  # rebuilt, full size
        """
        if from_log:
            px = max(self.canvas.width, self.canvas.height) if scale is None else int(scale)
            rebuilt = self.replay(frames=px)
            return rebuilt.history.save_gif(path, fps=fps, every=every)
        return self._film().save_gif(path, fps=fps, every=every, scale=scale)

    def contact_sheet(self, path: str | Path, columns: int = 6) -> Path:
        """Write the time-lapse as a grid of thumbnails.

        From the frames :meth:`timelapse_gif` would use: a session loaded from a file
        rebuilds them from the log first, which costs a full repaint.
        """
        return self._film().save_contact_sheet(path, columns=columns)

    def _film(self) -> History:
        """The history whose frames are this painting's time-lapse.

        This session's own, when it recorded them. A session loaded from a file that
        kept none has its film rebuilt: the log replayed onto a fresh canvas with a frame
        kept after each mark, at :attr:`frame_px`, exactly as the painting recorded them
        while it was being painted. Only when the time-lapse is on -- a painting made with
        it off asked for no film, and is told how to have one anyway.
        """
        self._no_frames_here()
        if self._film_from_log and self.timelapse:
            return self.replay(frames=self.frame_px).history
        return self.history

    def _no_frames_here(self) -> None:
        """Say what happened when a *rehearsal* is asked for a time-lapse.

        A rehearsal copy is created with the time-lapse off -- it is a scrap of
        canvas, and a film of a scrap is not what anybody wants -- so the frames a
        painter went looking for are on the painting this copy came from. The
        general message says to create the session with ``timelapse=True``, which is
        the one thing the painting already did.
        """
        if self._is_trial and not self.history.frame_count:
            raise ValueError(
                "This is a rehearsal copy, and a rehearsal records no frames: the "
                "painting it was copied from keeps its own. Run the pass for real, "
                "or ask the painting itself -- easel timelapse <session> <out.gif>."
            )

    def capture_frame(self) -> None:
        """Record a time-lapse frame by hand, when ``timelapse`` is off.

        Kept in this process only: a session file keeps no frames, so a film captured
        by hand has to be written before the session is.
        """
        px = self.frame_px
        self.history.add_frame(self.canvas.thumbnail_srgb8(px), max_side=px)

    def _auto_frame(self) -> None:
        """Record a frame after a mark, if the time-lapse is on and wants one.

        Past :data:`~easel.history.MAX_FRAMES` the sequence is thinned by halves, so
        most of the frames a long painting built used to be built and then dropped.
        :meth:`~easel.history.History.wants_frame` says which ones survive, and the
        rest are not built: the same film, for a fraction of the 42-60 ms a frame
        costs. Nothing here touches the log or the stream -- frames live beside
        both -- so no painting moves.

        **None at all on a session loaded from a file that kept none**, which is every
        file since 0.7.0 -- so every pass run from the shell or the server. The film of
        such a session is rebuilt from the log when it is asked for (:meth:`_film`), a
        frame recorded here would begin that film in the middle of the painting, and
        the file's next save would drop it anyway.
        """
        if self.timelapse and not self._film_from_log and self.history.wants_frame():
            self.capture_frame()

    @property
    def frame_px(self) -> int:
        """The long side this painting's time-lapse frames are made at: recorded, or
        rebuilt from the log for a session loaded from a file."""
        size = self.timelapse
        if size is True or size is False:
            return DEFAULT_FRAME_PX
        return max(int(size), 1)

    def report(self, since: int | None = None, subject_share: float | None = None) -> str:
        """The post-pass check: what the marks just laid would be warned about, off the log.

        ``easel run`` prints this beside the budget line after every pass, and
        ``--check`` widens it to the whole painting. It is the form the guide's
        standing warnings take once they can be checked rather than repeated --
        three painters made the same mistakes *after* reading the warnings about
        them, and what did catch a mistake was never a sentence but a line printed
        after a pass. Every rule's input but one is already in the log, which carries
        brush, size, path, pressure and note per mark; the one is the canvas as the
        pass opened. Ten rules, each of which a real pass
        of a real painting would have tripped, and under them the standing lines --
        measurements rather than findings: the subject's share, and four read off the
        canvas -- plus, for a painting that has declared a plan (:meth:`plan`), a line
        per declaration it can measure:

        - **one brush at one size** for a whole pass of two or more calls;
        - **a stack of passes at one angle** -- twelve or more long marks within six
          degrees of each other, from two or more calls, and most of the long marks
          in the pass, **a ``scumble`` counting as one**: its passes are one band,
          sized to overlap, and whether they show as bars is ``scumble-bars``'
          question at the call. **Said once**, and again only when the picture has acquired
          a long mark ``_REPORT_CROSSING_DEG`` off the bars it was said about. It is
          the one rule here that can be *right and useless*: its own text concedes
          *unless the subject runs that way*, it cannot tell whether the subject
          does, and on a subject that does -- joists, a waterline, a reflection -- it
          fired on five passes running until the painter stopped reading it, which
          means it was unread on the pass where it was right. Under
          ``plan(bands="subject")`` the painter has answered that, and the line stops
          warning and counts what crosses the bars instead;
        - **a graded passage laid too narrow** -- five or more long parallel marks at
          three or more colours, in one run with no gap wider than four brushes and
          with their colours turning at most once, stepped further apart than half
          the narrowest brush laying them. That is the same wall ``scumble`` warns
          on and the one a hand-laid band gets no protection from; the clauses around
          it are what keeps ten pots and two ramps laid end to end out of it, and a
          brush that lays no colour of its own is not counted at all;
        - **a loaded bristle under ``size=0.025``**, which is a comb of four streaks
          with gaps rather than a brush. Not a *starved* one: below ``load=0.6`` the
          gaps are the mark, and a painting made of broken glints tripped this
          twenty-eight times and was right to ignore it every time. **A pass's rule
          only**: it asks for a brush for the marks about to be laid, and over a whole
          painting it says nothing;
        - **small marks before the masses are down** -- eight or more under
          ``size=0.02`` inside the first sixty marks of the painting. *The
          painting's* first sixty, rehearsal copies included: this and the subject's
          share are the two rules that read across passes, and both counted a
          rehearsal's own log alone until 0.4.0, which on the path the guide tells
          every painter to use meant counting from a bare canvas;
        - **a pressure list on a chisel tip**, on a hand-laid mark short enough to
          have been asking for a taper;
        - **three or more small round-tip marks at ``tip_wobble=0``**, each short
          enough to be the tip's silhouette rather than a line. Both of a round tip's
          defaults are the bad one -- the disc is the default and the fix is opt-in --
          so *several small marks with ``round_hard`` or ``liner``* is the failure
          nobody has to ask for. The closing checklist's *is any small mark a disc, a
          capsule or a rectangle* is this rule's own question, and **over a whole
          painting it counts only the discs seen together** -- three or more, each
          within ``0.06`` of another -- leaves a signature out, and says where they
          are: a lamp, a moon and a glint laid in three passes are three marks, and
          were being counted as one disc printed three times;
        - **a daisy** -- five or more hand-laid marks, each at least twice as long as
          its brush is wide, leaving one point in every direction: no gap in the circle
          of their directions wider than ninety degrees. The point is where consecutive
          marks' lines meet, so rays laid from a disc's rim count as well as petals
          from its centre; a tree's fork, a tuft of grass and a fan of rays leave a
          wider gap, and a glow of films as wide as they are long is not lines at all;
        - **a loop's signature** -- six or more consecutive hand-laid marks of one
          brush at one length, or a strict ramp of lengths, evenly spaced along a line
          and further apart than their own width. A row placed by hand varies both,
          and a passage laid as overlapping passes sits closer than its width;
        - **details a layer buried** -- earlier small or ``subject`` marks that were
          showing as the pass opened, left at under half their contrast by a glaze or
          by the passes of a mass. It reads the canvas as the pass opened, which
          ``easel run`` keeps and so does the report before, for a script that reports
          after every pass; like the plan's lines, it is left off a counted copy;
        - **what the plan promised**, for a painting that declared one: how many of
          its places are painted within ``0.10`` of the value they were promised, and
          whether the place meant to be lightest is the lightest of them. Both read
          the canvas, so both are left off a counted copy;
        - **the subject's share** of the marks so far, whenever a mark is noted
          ``subject``, against ``subject_share`` -- the argument here, or the plan's
          own, the argument winning. The
          share to measure at the moment the subject is finished, and meant to fall
          afterwards. A measurement, not a rule: it is printed under the findings and
          not counted among them;
        - **how much ground is still showing**, once anything has been painted:
          :meth:`~easel.canvas.Canvas.ground_showing` against a bare canvas at this
          session's own ground, texture and seed. The closing checklist asks *is
          there anywhere the ground still shows through? There should be*, and until
          0.4.0 there was no way to answer it short of building that canvas and
          diffing it -- which one painter did after the painting was finished, having
          already spent the warm ground the whole picture had been planned around.
          It says so under ``_GROUND_FLOOR``, which is the line's one judgement --
          and under ``plan(ground="buried")`` it prints the number without asking,
          because whether this picture covers its ground on purpose is the painter's
          to say;
        - **the values, the edges and the pencil**, the other three lines only the
          canvas can answer: where the picture's values sit against what the palette
          reaches, how its edge length divides between hard and soft, and how much
          graphite still shows. Each is a number with its threshold said out loud,
          and :mod:`easel.checklist` holds each one's evidence. Printed after every
          pass like the ground line, and like it left off a counted copy. The noise
          budget counts findings and call-time notices, and these are neither: four
          lines that print on every pass are the design, and whether a longer block
          gets skimmed is for a painter's run to show.

        **What this cannot see is a composition**, and it says ``nothing to report`` to
        a dead one. Every rule here is about a mark, because a mark is what the log
        holds. One painting's largest mistake was its first arrangement -- it made the
        distant opening the hero and left the subject an empty band across the top of
        the frame -- and every pass the check approved was locally clean. That is a
        boundary rather than a fault: composition is carried by the drawing, which is
        free, and judged by looking at it. It is also the argument for putting *why
        did you choose this subject* on the closing checklist, where a painter answers
        it, rather than here, where nothing can.

        Two more need the shape and so fire at the call instead: a shaped
        ``block_in`` with ``direction`` left off costing over 2.5x its axis price (or
        a sequence of directions costing over 2.5x its own dearest angle), and a round
        tip blocking in a *feature* -- a shape under a tenth of the canvas across --
        less than four brushes wide. Each
        rule that lives here can leave the guide, which is the growth rule paying
        for itself, and one has: *you will under-vary your marks* is in
        ``PAINTING.md`` rather than on the front page since 0.3.0.

        Args:
            since: the log index the pass began at -- ``len(s.history.records)``
                before the pass -- so the check covers the pass alone. Omitted, the
                whole log, and the one rule that decays does not: an audit asked for
                says everything it has about the painting. The two rules about a pass
                are asked the painting's question instead -- the small comb says
                nothing, and the discs are counted where they sit together.
            subject_share: the share of the marks the plan gave the subject, ``0..1``.

        Returns:
            The lines to print. Never empty: a pass with nothing to report says so.

        Example::

            before = len(s.history.records)
            lay_the_rocks()
            print(s.budget_line())
            print(s.report(since=before, subject_share=0.32))

        Prints, on a pass that tripped nothing, for a painting that declared a plan::

            check over this pass, 9 marks: nothing to report
              plan: 5 of 6 places inside 0.10; halo +0.14
              lightest: lamp reads 0.78, the lightest of the 6 places planned
              subject: 41 of 128 marks so far (32%), against 32% planned
              values: 0.21-0.84 of a box that reaches 0.13-0.96, clusters at 0.27, 0.49, 0.78; a clear light, mid and dark
              edges: 41% of edges are under 2.5 px wide, median 2.9 px
              ground: 2.16% of the canvas is still bare ground
        """
        records = self.history.records
        start = 0 if since is None else max(0, min(int(since), len(records)))
        marks = [r for r in records[start:] if r.kind not in History.UNPAINTED_KINDS]
        # Every mark of the painting before this pass, the copy's inheritance
        # included. A rehearsal's own log starts empty -- see :attr:`_prior` -- and
        # without this the two rules that read across passes both answer as if the
        # canvas were bare.
        before = [r for r in self._prior if r.kind not in History.UNPAINTED_KINDS]
        earlier = len(before) + sum(
            1 for r in records[:start] if r.kind not in History.UNPAINTED_KINDS
        )
        # The marks this painting has been charged for -- the same set the budget
        # counts, signature allowance and all, rather than every mark of paint. The
        # subject line divided by the second and was compared against the first.
        paid = History.paid_marks(list(self._prior) + list(records))
        # The stack-of-bars line decays over a pass and not over the painting: what
        # makes a warning skimmable is being printed after every pass unasked, and
        # `--check` is asked for. An audit says everything it has about the painting --
        # which is why the two rules that were about a pass, the small comb and the
        # discs, are asked the painting's question instead (see `_pass_findings`).
        findings = _pass_findings(
            marks, earlier, self.canvas,
            banding=None if since is None else self._banding_wanted(paid),
            bands=self._plan.bands, whole=since is None,
        )
        # One reading of the canvas for everything below that looks at it. A counted
        # copy has laid no paint on the canvas it borrowed, so it takes none.
        without = self.canvas.values(sketch=False) if paid and not self._counting else None
        view = None if without is None else without.astype(np.float32) / 255.0
        opened = self._opened
        if (view is not None and since is not None and opened is not None
                and opened[0] == start and opened[1].shape == view.shape):
            found = _buried(opened[1], view, list(self._prior) + list(records[:start]),
                            records[start:], self.canvas)
            if found is not None:
                findings.append(_buried_line(*found))
        scope = "this pass" if since is not None else "the painting"
        head = f"check over {scope}, {len(marks)} mark{'s' if len(marks) != 1 else ''}: "
        if findings:
            head += f"{len(findings)} thing{'s' if len(findings) != 1 else ''} to look at"
        else:
            head += "nothing to report"
        lines = [head] + [f"  - {line}" for line in findings]
        # The lines the plan itself asked for, before the two standing ones: they are
        # measurements of what the painter said they would do, so they read first. Gated
        # exactly as the ground line below is -- they read the canvas, so a counted copy
        # has nothing of its own to read, and a painting with no paint on it yet would be
        # told how far its plan is from the bare ground.
        if paid and not self._counting and (self._plan.values
                                            or self._plan.lightest is not None):
            view = self._value_view()
            for line in (self._plan.value_line(view), self._plan.lightest_line(view)):
                if line:
                    lines.append(f"  {line}")
        subject = self._subject_line(paid, subject_share)
        if subject:
            lines.append(f"  {subject}")
        if without is not None:
            # A count-only copy has laid no paint on the canvas it borrowed, so the
            # honest answer is the one it started with and the useful one does not
            # exist. Every other line here comes off the log and is exact.
            lines += [f"  {one}" for one in self._canvas_lines(without)]
            # And the canvas as it stands is the one the next pass opens on, for a
            # painter who runs passes in one script and calls this after each.
            self._opened = (len(records), view)
        return "\n".join(lines)

    def _open_pass(self) -> int:
        """Keep the canvas as a pass opens, and return the log index the pass starts at.

        What :meth:`report` needs to say that a pass buried details under a film or a
        mass: the canvas before the pass, which the log cannot give back without
        replaying it. ``easel run`` and the MCP ``run`` tool take it where they already
        take the index; a painter calling :meth:`report` after each pass in one script
        gets it from the report before. Nothing is taken on a counted copy.
        """
        here = len(self.history.records)
        if not self._counting:
            self._opened = (here, self.canvas.values(sketch=False).astype(np.float32) / 255.0)
        return here

    def checklist(self, subject_share: float | None = None) -> str:
        """The closing checklist, answered: every measured line with its number.

        `PAINTER.md` has ended with a list of questions to ask a finished painting
        since the first version of it, and until 0.6.0 every one was answered by
        looking. The questions with a *number* behind them were the ones answered
        wrongly -- looking afresh is what a painter who has been at the canvas for
        four hours cannot do -- and each cohort produced the same evidence: a
        painting planned around a warm ground finished with ``0.07%`` of it left, and
        five of the next six budgeted paintings stopped with more than half the
        budget unspent. So the measured lines answer themselves here, and
        `PAINTER.md`'s list shrinks to the three that cannot be measured plus this
        call.

        Everything :meth:`report` prints over the whole painting, plus the three
        lines that only make sense at the end -- ``boxes:``, ``unspent:`` and the
        three questions. It is :meth:`report` with ``since=None`` and not a second
        instrument: a number that disagreed with the one printed after the last pass
        would make both useless.

        **And then the three it cannot answer**, printed as questions with the
        painter's own ``why`` quoted back. *Is the thing you measured most carefully
        still attached*, *which passage is the weakest*, and *is the reason you chose
        this subject still in the picture* are not withheld for tidiness -- nothing
        in this engine can ask them. The check reads marks and measures pixels, and a
        picture can pass every line above and have quietly become a different
        picture, competently painted. That boundary is `LESSONS.md`'s and it is kept
        here on purpose.

        Args:
            subject_share: the share of the marks the subject was to get, ``0..1``.
                The plan's own is used when this is left off.

        Returns:
            The lines to print.

        Example::

            print(s.checklist())

        Prints::

            checklist for this painting -- 128 of 300 marks spent
              subject: 41 of 128 marks so far (32%), against 32% planned
              values: 0.15-0.35 of a box that reaches 0.13-0.96, clusters at 0.17,
                0.25, 0.32; no clear light -- nothing above 0.35, ...
              edges: 27% of edges are under 2 px wide, median 3.4 px
              ground: 2.16% of the canvas is still bare ground
              boxes: 2 of 9 masses were laid in a rectangle (22%) -- check the
                background hardest
              unspent: 172 of 300 unspent (57%) -- name the weakest passage and
                spend them there

            three this cannot answer, and they are the ones to answer slowly:
              - Cover the thing you measured most carefully. Is it still attached to
                the picture -- and is the lightest mass the one you planned to be?
              - Which passage would you apologise for? That is the one the marks
                left are for, not the one you have most recently been enjoying.
              - You wrote: "a hot afternoon, and the light coming off the water".
                Is that reason still in the picture?
        """
        records = self.history.records
        marks = [r for r in records if r.kind not in History.UNPAINTED_KINDS]
        paid = History.paid_marks(list(self._prior) + list(records))
        head = (f"checklist for this painting -- {self.spent} of {self.budget} marks "
                f"spent" if self.budget is not None
                else f"checklist for this painting -- {self.spent} marks spent")
        lines = [head]
        # The audit's own findings, over the whole painting rather than a pass: the
        # discs seen together, the bars, the small marks before the masses. `since=None`
        # is what turns the one rule that decays back on -- a closing check asked for
        # says everything it has about the painting -- and `whole` is what keeps two
        # rules about a pass from adding the painting up (finding 12).
        findings = _pass_findings(marks, 0, self.canvas, banding=None,
                                  bands=self._plan.bands, whole=True)
        lines += [f"  - {line}" for line in findings]
        if paid and not self._counting and (self._plan.values
                                            or self._plan.lightest is not None):
            view = self._value_view()
            for line in (self._plan.value_line(view), self._plan.lightest_line(view)):
                if line:
                    lines.append(f"  {line}")
        subject = self._subject_line(paid, subject_share)
        if subject:
            lines.append(f"  {subject}")
        if paid and not self._counting:
            lines += [f"  {one}" for one in self._canvas_lines()]
        lines.append(f"  {checklist.boxes_line(*checklist.mass_counts(records))}")
        lines.append(f"  {checklist.unspent_line(self.spent, self.budget)}")
        lines.append("")
        lines.append("three this cannot answer, and they are the ones to answer slowly:")
        lines += [f"  - {one}" for one in self._questions()]
        return "\n".join(lines)

    def _questions(self) -> list[str]:
        """The three the check cannot answer, with ``why`` quoted back.

        Kept apart from the measured lines and printed as questions, because the
        difference between them is the whole boundary: every line above is a number
        about a mark or a pixel, and these three are about a picture. The wording is
        `PAINTER.md`'s own, so that a painter who read the file meets the same
        sentence here rather than a paraphrase of it.

        The third is the one nothing else can ask at all, and it is quoted rather
        than summarised: a reason read back in the painter's own words is the
        instrument, and a reason the engine reworded would be the engine's.
        """
        why = (self._plan.why or "").strip()
        return [
            "Cover the thing you measured most carefully. Is it still attached to "
            "the picture -- and is the lightest mass the one you planned to be?",
            "Which passage would you apologise for? That is the one the marks left "
            "are for, not the one you have most recently been enjoying.",
            (f"You wrote: {why!r}. Is that reason still in the picture?" if why else
             "You did not write down why you chose this subject, so nothing can read "
             "it back. s.plan(why=...) before the next painting: it is the one line "
             "here no measurement can replace."),
        ]

    def _subject_line(self, paid: list[StrokeRecord], subject_share=None) -> str:
        """The subject's share of the marks so far, against what was planned for it.

        Empty when no mark carries ``note="subject"``: there is nothing to divide,
        and a painting that never named its subject's marks is not being told it
        spent 0% on them.

        Args:
            paid: the marks charged against the budget, the painting's own included.
            subject_share: the share the caller declared, which wins over the plan's.
        """
        on_it = [r for r in paid if "subject" in str(r.note).lower()]
        if not on_it:
            return ""
        share = len(on_it) / max(len(paid), 1)
        line = f"subject: {len(on_it)} of {len(paid)} marks so far ({share:.0%})"
        # The argument wins over the plan: it is the more specific of the two, and
        # a pass measuring one passage against its own share should be able to say
        # so. Without either there is no comparison to print -- which is what
        # every painter working through `easel run` or the MCP server got, because
        # neither passed the argument and there was nowhere to declare it.
        declared = (subject_share if subject_share is not None
                    else self._plan.subject_share)
        if declared is not None:
            planned = float(declared)
            line += f", against {planned:.0%} planned"
            if share < planned - 0.005:
                line += " -- behind, if the subject is finished"
        return line

    def _ground_line(self) -> str:
        """How much ground is still showing, with the one judgement in it named.

        Split out of :meth:`report` when :meth:`checklist` came to need the same
        sentence: two places printing the same measurement in two wordings is how a
        document and a tool drift apart, which is the whole argument of
        :mod:`easel.notices` applied to a line that is not a notice.
        """
        bare = self.canvas.ground_showing()
        line = f"ground: {bare:.2%} of the canvas is still bare ground"
        if bare < _GROUND_FLOOR:
            if self._plan.ground == "buried":
                # Declared, so the number is the whole of what there is to say.
                # Five of seven painters in one cohort accepted this line by hand,
                # three of them naming the same cause: the graded field they were
                # told to lay buried the breather they were told to leave.
                line += " -- buried, as the plan says"
            else:
                line += f" -- under {_GROUND_FLOOR:.1%}, and the checklist asks for some"
        return line

    def _canvas_lines(self, without: np.ndarray | None = None) -> list[str]:
        """The standing measurements, off as few readings of the canvas as they need.

        `values:`, `edges:`, `ground:` and `pencil:` -- the four that can only be had
        by looking at the picture, as against the ones that come off the log and are
        exact. They print after every pass, beside the findings, because the fault
        each one names is one that three cohorts of painters did not see by looking:
        a picture with no clear light, boundaries that are all the same width, a
        warm ground spent without noticing, a drawing left showing.

        **Two composites at most.** The rise widths and the clusters both read the
        canvas without its graphite, so they share one array; ``pencil:`` is the
        difference between that and the canvas with it, and is skipped outright when
        there is no graphite to find -- which is the common case by the end of a
        painting and costs a composite to discover otherwise. The cost guard in the
        plan this came from is *one canvas pass per report()*, and the third reading
        here (:meth:`_value_view`, for a declared plan) was already being taken.

        Never called on a counted copy: it has laid no paint on the canvas it
        borrowed, so every number here would be the canvas's and not the pass's.
        ``without`` is the values view without graphite when the caller already has
        it -- :meth:`report` does, for the rule that reads what a pass covered.
        """
        if without is None:
            without = self.canvas.values(sketch=False)
        view = without.astype(np.float32) / 255.0
        reach = (self.palette.darkest_value, self.palette.lightest_value)
        lines = [checklist.values_line(view, reach=reach),
                 checklist.edges_line(view),
                 self._ground_line()]
        if self.canvas.has_sketch:
            lines.append(checklist.pencil_line(self.canvas.values(sketch=True), without))
        return lines

    def _value_view(self) -> np.ndarray:
        """The whole canvas as values, 0..1, the way :func:`compare_plan` reads it.

        One array per :meth:`report`, shared by every place the plan names: the same
        arithmetic per place would be the canvas converted five times over to answer
        five questions about it.
        """
        return _values_of(self.canvas.to_srgb8(impasto=False))

    def _banding_wanted(self, painting: list[StrokeRecord]):
        """Whether the stack-of-bars line is worth printing, as a test on its angle.

        Said once, and again only when the picture has acquired something that
        crosses the bars. A warning that concedes *unless the subject runs that way*
        cannot tell whether the subject does, and on a subject that does -- joists, a
        waterline, a reflection -- it fired on five passes running until the painter
        stopped reading it. By the fourth it was unread on the pass where it was
        right. That is the bristle floor's twenty-eight correctly-ignored warnings
        again, inside the engine rather than in a file, and teaching a painter to skim
        a line is worse than not printing it.

        Re-checking the same pass says the same thing: the pass is identified by the
        painting's mark count at its end, so ``report()`` called twice over one pass
        answers twice, and only a *later* pass is measured against what the picture
        has picked up since.

        Returns a callable that answers with **the crossing count, or ``None`` for do
        not print** -- rather than with a bool, because since 0.6.0 the count is not
        just the gate but the line: a painting that has declared ``bands="subject"``
        is not warned about its bars, it is told how much crosses them. ``None`` and
        not ``0``: nothing crossing is a number worth printing, and the two would be
        the same answer under a plain truth test.
        """
        here = len(painting)

        def wanted(centre: float) -> int | None:
            crossings = _crossing_marks(painting, centre, self.canvas)
            told = self._banding_told
            if told is None or told[0] == here or crossings > told[1]:
                self._banding_told = (here, crossings)
                return crossings
            return None

        return wanted

    # -- what the engine says at the call ---------------------------------------
    def _notify(self, code: str, text: str, stacklevel: int = 1) -> None:
        """Say one thing, under the code it is registered as.

        The one route out for everything the engine says at a call. It keeps the
        notice -- so a pass can print what it said, and an MCP painter can be told at
        all -- and then warns, which is what a painter at a Python prompt has always
        seen and what every ``pytest.warns(UserWarning, ...)`` in the suite reads.

        Kept **beside** ``history.records`` and never in it: rule 8 of the plan this
        came from, and the reason is that a mark's texture is seeded from its index in
        the log. Anything new that took an index would repaint every painting made
        before it.

        ``code`` must be a key of :data:`easel.notices.NOTICES`; an unregistered one
        raises here rather than reaching a painter, because the registry is what
        `REFERENCE.md` and `easel explain` are held against and a code that is in one
        of the three and not the others is the drift this channel exists to stop.

        ``stacklevel`` counts from whatever called this, exactly as it counted when
        each of these sites called ``warnings.warn`` itself. The frame this method
        adds is put back here, so no site's number had to change when the channel
        went in -- and a number that was right for the painter's own line goes on
        pointing at it. It defaults to 1, meaning *whoever called this*, which is
        ``warnings.warn``'s own default read from the same place; every site here
        says a number, because a notice points at the painter's line and not at the
        engine's.
        """
        if code not in NOTICES:
            raise KeyError(
                f"{code!r} is not a registered notice. Add it to easel.notices.NOTICES "
                f"and to REFERENCE.md's table, which tests/test_notices.py holds "
                f"against each other."
            )
        self._notices.append(Notice(code, text))
        warnings.warn(EaselWarning(text, code), stacklevel=stacklevel + 1)

    def _adopt_notices(self, trial: Session) -> None:
        """Take what a throwaway copy said, because this session is what said it.

        :meth:`rehearse` and the price walk both work on a copy -- the copy is how a
        rehearsal spends a copy of the stream instead of the real one -- and a notice
        that landed on it would be thrown away with it. A painter at a Python prompt
        never noticed, because ``warnings.warn`` had already reached their console;
        through the MCP server, where the returned text is the only channel there is,
        it was the difference between being told and not.

        Named apart from :meth:`_adopt`, which takes on a whole session -- canvas,
        log and stream -- and is what :meth:`undo` rebuilds through. This one moves
        a list. Calling the wrong one here made ``rehearse`` commit its trial to the
        painting, which the *planning verbs leave nothing behind* test caught within
        the minute.
        """
        self._notices.extend(trial._notices)

    def notices(self, since: int | None = None) -> list[Notice]:
        """What this session has said at a call, oldest first.

        ``since`` is an index into this list -- ``len(s.notices())`` taken before the
        pass -- and not a log index, because a notice is not a mark: a plan that is
        priced and never painted says things and lays nothing. ``easel run`` prints
        ``s.notices(since=...)`` above the post-pass check, collapsed by code, facts
        before habits; see :func:`easel.notices.block`.

        A rehearsal copy starts with none of its own and keeps what it says, the way
        :meth:`scratch` handles every other kind of bookkeeping -- so a pass rehearsed
        and then painted says the same things twice, once on the copy and once for
        real, which is what a painter rehearsing expects.
        """
        if since is None:
            return list(self._notices)
        return list(self._notices[max(0, int(since)):])

    def reports(self) -> list[PassReport]:
        """What each pass was told after it ran, oldest first -- rehearsals included.

        Every ``easel run`` and every MCP ``run`` keeps the block it prints after a
        pass: what was said at the calls, then the post-pass check. **A rehearsed or
        counted pass keeps its block too**, flagged as such, though it commits nothing
        else -- because that is where a pass gets changed, and so where a check that
        misfires is seen and then rewritten away. Twice a painter watched *graded
        passage laid too narrow* fire on marks that were not a passage, both times in
        a rehearsal, and nothing in the file could show it afterwards.

        Each is a :class:`~easel.notices.PassReport`: ``scripts``, ``mode``
        (``"painted"``, ``"rehearsed"`` or ``"counted"``), ``at`` -- the log index the
        pass began at, so ``s.replay(upto=r.at)`` is the canvas it opened on -- and
        ``text``. ``str()`` of one is what ``easel log --reports`` prints.

        Saved in the ``.easel`` file beside the log and never in it, as the notices
        are. A painter running passes from Python prints :meth:`report` itself, and
        nothing is kept for that: this is the record of what the shell and the server
        printed, which a painter reading a session file afterwards cannot otherwise
        get back.
        """
        return list(self._reports)

    def _keep_report(self, target: Session, scripts: str, since: int, text: str) -> None:
        """Keep what a pass was told, on this session, whichever copy it ran on.

        ``target`` is the session the pass ran against -- this one, or a copy
        :meth:`scratch` handed out -- which is what says how it ran, and ``since`` is
        the log index the pass began at in *its* log, which a copy starts at nought.
        """
        if target is self:
            mode = "painted"
        else:
            mode = "counted" if target._counting else "rehearsed"
        self._reports.append(PassReport(str(scripts), mode,
                                        int(target._index_base) + int(since), str(text)))

    # -- what the painter says before painting -----------------------------------
    def plan(self, why=None, values=None, lightest=None, subject_share=None,
             bands=None, ground=None, clear: bool = False) -> Plan:
        """Write the plan down where the engine can see it. Returns it; print it.

        The guide has always asked a painter to settle these before the first mark,
        and until 0.6.0 there was nowhere to put any of them: *useful heuristics, but
        they're philosophy, not errors, and it doesn't know which*. ``Session(budget=)``
        was the first of these declarations; this is the rest of them::

            s.plan(why="under a pier the light arrives from below, so every form is "
                       "lit backwards",
                   values={sky: 0.70, water: 0.39, quay: 0.22},
                   lightest=lamp,
                   subject_share=0.40,
                   bands="subject",
                   ground="buried")

        Args:
            why: what the picture is for, in a sentence. Nothing measures it;
                :meth:`checklist` quotes it back at the end, which is the moment it
                is worth reading again.
            values: ``{place: value}``, the same dict :meth:`compare` takes -- so a
                plan written here can be handed to ``compare()`` unchanged. The
                post-pass check then carries a ``plan:`` line saying how many places
                are painted as promised, and registering it prices the **pairs**: two
                places planned closer than ``0.10`` read as one where they meet, and
                this is the one moment that question is free to ask.
            lightest: the place meant to be the lightest thing in the picture. The
                check ranks the plan's places and says when something else has taken
                the light -- one painting reached stroke 217 before it had any.
            subject_share: the share of the budget the subject gets, 0..1. The
                ``subject:`` line then always carries *against N% planned*, which
                needed ``report(subject_share=)`` by hand before -- and neither
                ``easel run`` nor the MCP ``run`` tool passed it, so from a shell the
                comparison had never once been printed.
            bands: ``"subject"`` declares that this picture's subject really does run
                in one direction. The stack-of-bars line then stops warning and starts
                counting: *how much crosses them*. It is the rule the corpus shows
                firing on one pass in seven, and the one two painters learnt to skim.
            ground: ``"showing"``, the default expectation, or ``"buried"`` -- this
                picture covers its ground on purpose, which is what a graded field
                edge to edge does. The ground line then prints its number without
                asking for some back.

            clear: start from nothing rather than from the plan already declared, so
                this call is the whole of it.

        Called with no arguments it simply hands back the plan the session is holding,
        which is what ``easel plan p.easel`` prints.

        Called again with some, it **changes what it is given and keeps the rest**, so
        a pass can add the lightest place to a plan written in a ``prelude.py`` without
        retyping its values; pass the empty version of a field to clear that one
        (``values={}``, ``bands=""``). A ``prelude.py`` re-registering the same plan
        before every pass says nothing the second time, which is what stops the pairs
        notice becoming a thing printed once a pass.

        The plan is saved in the ``.easel`` file, beside the log and never in it: a
        mark's texture is seeded from its place in ``history.records``, so anything
        new that took an index would repaint every painting made before it.
        """
        wanted = build_plan(why=why, values=values, lightest=lightest,
                            subject_share=subject_share, bands=bands, ground=ground,
                            onto=None if clear else self._plan)
        # Here rather than in `easel.plan`, because whether a place is anywhere on the
        # painting is a question about this canvas. `compare()` asks it of the same dict
        # and says the same thing; without it the check would print a `nan` after every
        # pass and the plan would be the only thing that could have said why.
        for place in [*wanted.values, wanted.lightest]:
            if place is not None and not place.outline.mask(*self.size).any():
                raise ValueError(
                    f"The planned place {place.name!r} covers no pixels of the canvas. "
                    f"A place in a plan has to be somewhere on the painting."
                )
        # The same values again are not news. A `prelude.py` runs before every pass, so
        # re-declaring is the ordinary case rather than the odd one, and without this the
        # pairs below would be said once a pass -- which is `LESSONS.md`'s seventh rule
        # broken by the one declaration meant to quieten the check down. The **values**
        # and not the whole plan, because they are all the pairs are read off: adding the
        # lightest place, or a sentence saying what the picture is for, is not a new
        # answer to a question about which masses meet.
        fresh = wanted.values != self._plan.values
        self._plan = wanted
        if fresh and wanted.values:
            self._say_pairs()
        return wanted

    def plan_pairs(self, near: float = _PLAN_TOUCH):
        """The plan's own pairs closer than the value threshold, and whether they meet.

        ``(a, b, gap, meets)`` tuples, closest first -- the same shape
        :attr:`easel.measure.Comparison.pairs` carries, because it is the same question
        asked of the same plan. Read off the plan and not off the canvas, so the answer
        arrives on the **empty** canvas: the one run the guide already tells a painter
        to make, and the one three rounds of painters skipped.

        ``near`` is how close two places have to come, as a fraction of the canvas long
        side, before they count as meeting; as :meth:`compare`, and for the same reason
        a plan carries no brushes.
        """
        gap_px = max(float(near) * float(self.canvas.long_side), 0.0)
        return self._plan.pairs(
            self.canvas.width, self.canvas.height,
            lambda a, b: _masks_meet(a, b, gap_px),
        )

    def _say_pairs(self) -> None:
        """The planned pairs that will read as one where they meet. See :meth:`plan`.

        Only the pairs that **meet** are said: three of one plan's four close pairs were
        masses that never touched, and the fourth was planned ``0.00`` apart and
        dissolved into its neighbour exactly where they met.
        """
        touching = [row for row in self.plan_pairs() if row[3]]
        if not touching:
            return
        said = "; ".join(f"{a} and {b} {gap:.2f} apart" for a, b, gap, _ in touching)
        self._notify(
            "plan-pairs",
            f"{len(touching)} planned pair{'s' if len(touching) != 1 else ''} "
            f"read as one where they meet: {said}. Two values closer than "
            f"{VALUE_THRESHOLD:.2f} read as one mass, and these places touch -- so "
            f"separate them in the plan now, or decide that the join is where the "
            f"edge goes.",
            stacklevel=3,
        )

    def explain(self, code: str) -> str:
        """The passage behind one notice, from the document that holds the measurement.

        ``s.explain("chisel-blank")``, and ``easel explain chisel-blank`` from a
        shell. This is where a rule's *reason* goes when its paragraph leaves the
        reading path: not deleted, delivered at the moment it applies. Raises
        ``KeyError`` naming every code there is.
        """
        return notice_text(code)

    def _note_assisted(self, what: str) -> None:
        """Record an assisted mode, once. See :attr:`assisted`."""
        if what not in self.assisted:
            self.assisted.append(what)

    def log(self, last: int = 10) -> str:
        """A short text summary of recent marks, and any assisted mode used.

        ``last`` is a count of **log records** -- the same thing :meth:`undo` and
        :meth:`replay` count, so the last three here are exactly what ``undo(3)``
        would take back. A ``dry``, a ``pencil`` and an ``erase`` are records and
        are free against the budget, so this number and :attr:`stroke_count` are
        not the same number.
        """
        text = self.history.summary(last)
        if self.assisted:
            text += "\nAssisted: " + "; ".join(self.assisted)
        return text

    # -- persistence ------------------------------------------------------------
    def save(self, path: str | Path) -> Path:
        """Save the whole session to a single ``.easel`` file (compressed npz).

        The CLI uses this so a painter can work in small increments from a shell
        without holding a Python process open. Everything but the time-lapse frames,
        which the log rebuilds (:meth:`timelapse_gif`), and stamped with the release
        that wrote it.
        """
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        meta = {
            "format": _EASEL_FORMAT,
            # The release that wrote the file, so a later one can say what a rebuild of
            # its log would lay differently (`older-engine`). New in 0.7.0 and read with
            # `.get`: every file saved before it has none, and is dated at load.
            "engine": _engine(),
            "width": self.canvas.width,
            "height": self.canvas.height,
            "texture": self.canvas.texture_name,
            "ground": self.canvas.ground_name,
            "ground_spec": self.canvas.ground_spec,
            "seed": self.seed,
            "timelapse": self.timelapse,
            "out_dir": str(self.out_dir),
            "budget": self.budget,
            # Nothing here reads this back since 0.5.0 -- a look is numbered from
            # what is in `out_dir`, which is the thing two sessions can both see.
            # It is still written because a 0.4.0 build reads the key and would
            # otherwise fail to load the file at all.
            "look_counter": _highest_numbered(self.out_dir, "look"),
            "stroke_count": self.canvas.stroke_count,
            "texture_strength": self.canvas.texture_strength,
            "rng_state": _encode_rng(self.rng),
            "palette_slots": {k: [float(c) for c in v] for k, v in self.palette.slots.items()},
            "marks": {k: [float(v[0]), float(v[1])] for k, v in self.marks.items()},
            # The overlay drawing. Kept beside the canvas the way the landmarks are,
            # because that is what it is: an older file has none and loads with none.
            "guides": [{"points": [[float(x), float(y)] for x, y in g["points"]],
                        "note": str(g.get("note", ""))} for g in self.guides],
            # What the post-pass check has already said about a stack of bars. A
            # painting worked from the shell is loaded and saved once per pass, so
            # without this the one rule that is meant to decay restarts every pass.
            "banding_told": (None if self._banding_told is None
                             else [int(self._banding_told[0]), int(self._banding_told[1])]),
            "has_sketch": bool(self.canvas.has_sketch),
            "assisted": list(self.assisted),
            # What the engine has said at a call, in order. Beside the log, never in
            # it -- see :meth:`_notify` -- and a key an older build does not read, so
            # a 0.5.0 Easel opens a file this one wrote.
            "notices": [[n.code, n.text] for n in self._notices],
            # What each pass was told afterwards, rehearsals included (`reports()`).
            # New in 0.7.0, beside the log for the same reason, and read with `.get`:
            # a 0.6.0 Easel opens a file this one wrote and never sees the key.
            "reports": [r.to_json() for r in self._reports],
            # What the painter wrote down before painting. Also a new key read with
            # `.get`, and beside the log for the same reason: a painting worked from
            # the shell is loaded and saved once a pass, so without this the plan
            # would have to be re-declared in every script that wanted it -- which is
            # exactly how the budget behaved before it was saved.
            "plan": self._plan.to_json(),
        }
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
                    # Always empty, since 0.7.0. The time-lapse was more than half of
                    # a painting's file -- 8.83 of 16.11 MB after 171 marks -- for a
                    # film a painter makes once, at the end, and the log rebuilds it
                    # exactly (`timelapse_gif`). Written empty rather than left out, so
                    # a 0.6.0 Easel, which reads the array, still opens the file.
                    frames=np.zeros((0, 1, 1, 3), dtype=np.uint8),
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
        """Reload a session saved by :meth:`save`.

        The canvas comes back as it was painted, under any later release: the file
        holds it, and loading never repaints. The time-lapse does not come back -- a
        file keeps no frames since 0.7.0 -- and is rebuilt from the log when one is
        asked for (:meth:`timelapse_gif`). A file saved by an earlier release whose log
        has marks a fix since then lays differently says so as it opens
        (``older-engine``), because an undo or a replay would lay them the new way.
        """
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
                # Before anything that can say something, because the first thing
                # this build says about a loaded file is often the out_dir line below.
                # A code this build does not know is dropped rather than kept: the
                # file may have been written by a later Easel, and a notice whose
                # registry row is missing has no kind to sort by and no reason to
                # print. New keys only, read with `.get`, so an older Easel opens a
                # file this one wrote and simply has no notices in it.
                s._notices = [
                    Notice(str(code), str(text))
                    for code, text in meta.get("notices", [])
                    if str(code) in NOTICES
                ]
                # Where what this load says begins: the shell and the server say it
                # before anything else, and the file's own notices are history.
                restored = len(s._notices)
                saved_by = _saved_by(meta)
                # New in 0.7.0: a file saved before it has none, and an entry this
                # build cannot read costs its own report and not the file.
                saved_reports = meta.get("reports")
                s._reports = [
                    report for report in (
                        PassReport.from_json(entry)
                        for entry in (saved_reports if isinstance(saved_reports, list)
                                      else []))
                    if report is not None
                ]
                # New in 0.6.0, read with `.get` and forgiving about its own contents:
                # a 0.5.0 file has no plan and opens with none. See `easel.plan`.
                s._plan = Plan.from_json(meta.get("plan"))
                s.seed = int(meta["seed"])
                s.rng = _decode_rng(meta["rng_state"])
                s.out_dir = Path(meta["out_dir"])
                _warn_foreign_out_dir(s, p, s.out_dir)
                budget = meta.get("budget")
                s.budget = None if budget is None else int(budget)
                s.timelapse = _as_timelapse(meta["timelapse"])
                s.marks = {
                    k: (float(v[0]), float(v[1])) for k, v in meta.get("marks", {}).items()
                }
                s.guides = [
                    {"points": [(float(x), float(y)) for x, y in g.get("points", ())],
                     "note": str(g.get("note", ""))}
                    for g in meta.get("guides", [])
                ]
                s._preparation = None
                s.assisted = [str(a) for a in meta.get("assisted", [])]
                told = meta.get("banding_told")
                s._banding_told = None if told is None else (int(told[0]), int(told[1]))
                s._index_base = 0
                s._is_trial = False
                s._stream_mark = None
                s._call_verb = ""
                s._call_boxed = False
                s._spent_base = 0
                s._prior = []
                s._counting = False
                s._uncounted = []
                s._clip_memo = None
                # Built by hand here, like everything above: a flag `__init__` sets and
                # this does not is an AttributeError on the first film of every pass
                # `easel run` paints from a file.
                s._film_call = ""
                s._solving = False
                s._opened = None
                s._load_notices = []

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
                # A file saved before 0.7.0 may carry its time-lapse, and keeps it: that
                # film is the painting as it was painted, and it goes on being recorded
                # here. A file with none -- every file since -- has its film rebuilt from
                # the log when one is asked for, and records nothing meanwhile.
                frames = data["frames"]
                s.history._frames = [f for f in frames] if frames.size else []
                s._film_from_log = not frames.size
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
        _warn_older_engine(s, p, saved_by)
        s._load_notices = s._notices[restored:]
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

    def replay(self, upto: int | None = None, frames: bool | int | None = None) -> Session:
        """Rebuild this painting from its log, optionally stopping after ``upto`` records.

        Returns a **new** session. The whole painting is reproducible from the log
        plus the seed, so this is also how the CLI undoes strokes: session files do
        not carry snapshots, but they do carry the log.

        ``frames`` overrides the rebuilt session's ``timelapse``, which is how
        :meth:`timelapse_gif` builds a film at a size nothing recorded: the marks
        land again, and this time a frame is kept after each of them at the size
        asked for. Nothing else about the rebuild changes.
        """
        records = self.history.records if upto is None else self.history.records[:upto]
        fresh = Session(
            self.canvas.width,
            self.canvas.height,
            texture=self.canvas.texture_name,
            ground=self.canvas.ground_spec,
            seed=self.seed,
            timelapse=self.timelapse if frames is None else frames,
            out_dir=self.out_dir,
            texture_strength=self.canvas.texture_strength,
            budget=self.budget,
        )
        for name, rgb in self.palette.slots.items():
            fresh.palette[name] = rgb
        fresh.marks = dict(self.marks)
        fresh.guides = [dict(g) for g in self.guides]
        fresh.assisted = list(self.assisted)
        fresh._banding_told = self._banding_told
        # The plan is beside the log rather than in it, so a rebuild from the log
        # alone would come back with none -- and a painting that has been undone back
        # a few marks has not changed its mind about what it is painting.
        fresh._plan = self._plan
        # The replayed session shares this one's out_dir. Numbering a look from the
        # directory rather than from a per-session counter is what keeps its very
        # next look()/preview()/rehearse()/compare() off a file this one already
        # wrote; the preparation is carried across so that ref_shape()/sketch() etc.
        # do not raise "No prepared reference yet" when this session has one.
        fresh._last_look = self._last_look
        fresh._preparation = self._preparation

        # Inside one call context, so the marks are laid without the warnings a
        # hand-laid mark gets: a replay is not a painter reaching for a pressure list.
        # The state and the verb each record carries are put back below regardless.
        with fresh._one_call("replay"):
            fresh._replay_records(records)
        # Where the generator is put. A replay lays every mark from its own per-index
        # seed and never draws the pass wander a mass draws, so left alone the fresh
        # session's stream would still sit at the seed -- a state a painting is only
        # ever in before its first mass, and the reason a CLI ``undo`` (which comes
        # through here) used to drift by 1.06% of the canvas against a clean rebuild
        # of the same scripts. The first record *not* replayed carries the state its
        # call began from, which is exactly where the kept painting stood; a whole
        # replay is this session as it stands, stream included.
        cut = self.history.records[upto:upto + 1] if upto is not None else []
        if cut:
            fresh._restore_stream(cut[0])
        else:
            fresh.rng.bit_generator.state = self.rng.bit_generator.state
        return fresh

    def _replay_records(self, records) -> None:
        """Lay a log's records on this session, one call each, carrying their own account."""
        fresh = self
        for record in records:
            if record.kind == "dry":
                made = fresh.dry(record.params.get("amount", 1.0),
                                 _place_from_params(record.params))
            elif record.kind == "pencil":
                made = fresh.pencil(
                    record.points,
                    pressure=float(record.pressure),
                    width=float(record.params.get("width", 0.0026)),
                    smooth=bool(record.params.get("smooth", True)),
                    note=record.note,
                )
            elif record.kind == "erase":
                made = fresh.erase(_place_from_params(record.params), note=record.note)
            else:
                params = dict(record.params)
                color = params.pop("color", record.color_hex or "#000000")
                glaze = bool(params.pop("glaze", False))
                smooth = bool(params.pop("smooth", True))
                held = params.pop("clip", None)
                clip = None if held is None else _clips_from_params(held)
                # A clip laid before 0.7.0 has no feather on its record and was cut on
                # the line, so it replays cut on the line: the default moved for new
                # marks, and never reaches a saved one.
                feather = float(params.pop("feather", 0.0))
                # Logs written before press existed have no key for it, and one stamp
                # is what they meant: they replay unchanged.
                press = int(params.pop("press", 1))
                made = fresh.stroke(
                    record.points,
                    brush=_brush_from_params(params),
                    color=(np.asarray(color, dtype=np.float32) if isinstance(color, list)
                           else color),
                    pressure=record.pressure,
                    glaze=glaze,
                    smooth=smooth,
                    press=press,
                    clip=clip,
                    feather=feather if clip else None,
                    note=record.note,
                )
            # The record's own account of the stream and of the call that laid it,
            # carried over verbatim: a replay never draws the wander, so what its
            # own marks would record is the seed, which is nowhere the painting was.
            for key in ("rng", "via", "boxed"):
                if key in record.params:
                    made.params[key] = record.params[key]
                else:
                    made.params.pop(key, None)

    def _adopt(self, other: Session) -> None:
        """Take on another session's canvas, history and rng, keeping our own identity."""
        self.canvas = other.canvas
        self.history = other.history
        # `other` is a fresh replay of exactly the kept records, and :meth:`replay`
        # has put its generator where this painting's stood before the undone marks
        # -- not adopting it left self.rng wherever it happened to be before the
        # undo, so a block_in()/sweep() painted after this path drew its wobble from
        # a stream a clean rebuild would never have produced.
        self.rng = other.rng

    # -- internals --------------------------------------------------------------
    @contextmanager
    def _one_call(self, verb: str = "", place=None):
        """Hold the generator's state for the length of one painting call.

        ``verb`` names the mass verb the call is, and rides on every record the call
        makes as ``params["via"]``, so that the log can tell a pass of a mass from a
        mark laid by hand -- which :meth:`report` needs and nothing else did.

        ``place`` is what the call was handed to fill, and rides the same way as
        ``params["boxed"]`` when it is a rectangle rather than a shape. The closing
        checklist asks *is any mass a rectangle that should have been a shape*, and
        until 0.6.0 nothing could answer it: a mass records the points of each of its
        passes and never the outline it was filling, so a box and the shape inscribed
        in it leave the same log. Written only when true, and read with ``.get``, so
        a 0.5.0 file opens unchanged and the key costs a painting nothing.

        Every record a call makes carries the state the stream was in when the call
        *began* -- see :meth:`_stream_state` -- so that undoing the call, whole or in
        part, puts the stream back to before it. It cannot be taken per record: a
        mass draws each pass's wander from the stream *between* its ``stroke()``
        calls, so by the time a pass's record is written its own draw has already
        happened, and a state taken there would leave the stream one draw past the
        undone mark rather than before it. Taken once, here, before the first draw,
        it is right for every record the call makes. Nested calls -- the contour of
        a clean block-in, ``cover``'s dry and fill -- share the outermost mark.
        """
        if self._stream_mark is not None:
            yield
            return
        self._stream_mark = _stream_of(self.rng)
        self._call_verb = verb
        self._call_boxed = isinstance(place, Region) if place is not None else False
        try:
            yield
        finally:
            self._stream_mark = None
            self._call_verb = ""
            self._call_boxed = False

    def _stream_state(self) -> dict:
        """The generator's state to record on a mark: the call's, or now."""
        return self._stream_mark if self._stream_mark is not None else _stream_of(self.rng)

    def _restore_stream(self, record: StrokeRecord) -> bool:
        """Put the generator back to where ``record``'s call began, if the log knows.

        Returns whether it could. A log written before 0.2.0 carries no state, and
        the stream is then left as it is -- which is what every undo did until now.
        """
        state = record.params.get("rng") if record.params else None
        if not state:
            return False
        self.rng = _stream_rng(state)
        return True

    def _say_uncounted(self, what: str) -> None:
        """Warn once, per count-only copy, about a question counting cannot answer."""
        if what in self._uncounted:
            return
        self._uncounted.append(what)
        self._notify("count-only", f"scratch(count_only=True): {what}", stacklevel=4)

    def _clip_cover(self, holds: tuple[Polygon, ...], feather: float = 0.0) -> np.ndarray:
        """The coverage mask a clipped stroke is multiplied by, remembered for a mass.

        ``block_in(edge="hard")`` hands every one of its passes the same outline, and
        building the mask is the one expensive thing about a clipped stroke: 78ms on
        a smoothed shape at 1200x800, against a few milliseconds for the dabs. A
        one-entry memo is the whole of what a mass needs, because its passes come one
        after another with nothing between. Keyed on the outlines' own points rather
        than on the objects, so two equal shapes share the answer and a freed one
        cannot be mistaken for a live one.

        Held inside more than one place, a dab lands where every one of them agrees:
        the masks multiply, which is what the word *and* means to a coverage between
        zero and one, and the memo holds the product so a mass pays for it once.

        ``feather`` breaks each outline's edge inward, against this canvas's tooth
        (:meth:`~easel.canvas.Canvas.broken_edge`), over that share of the long side
        measured from the outline itself -- or over a quarter of the shape's own width
        where it is narrower than four feathers, so a thin shape keeps its body
        (``Polygon._edge_depth``). It is in the key beside the outlines, because
        anything a mask is computed from has to be in its cache key (``LESSONS.md``,
        trap 5): the same outline at two feathers in one session is two masks.
        """
        width, height = self.canvas.width, self.canvas.height
        key = (tuple(one.points for one in holds), width, height, float(feather))
        if self._clip_memo is not None and self._clip_memo[0] == key:
            return self._clip_memo[1]
        px = float(feather) * self.canvas.long_side
        cover = None
        for one in holds:
            mask = one.coverage(width, height)
            if px > 0.0:
                rows, cols, depth, full = one._edge_depth(width, height, px, mask)
                if len(rows):
                    mask[rows, cols] = np.minimum(
                        mask[rows, cols],
                        self.canvas.broken_edge(rows, cols, depth, full))
            cover = mask if cover is None else cover * mask
        self._clip_memo = (key, cover)
        return cover

    def _snapshot(self, box: tuple[int, int, int, int] | None = None) -> None:
        """Push the canvas onto the undo stack, unless this session lays no paint.

        One place, because every verb that marks the canvas has to do it and a
        count-only copy has to do it nowhere -- see :meth:`scratch`. ``box`` is the
        part of the canvas the action about to happen can reach, where the caller
        knows it; the verbs that can touch anywhere (``dry``, ``erase``, ``pencil``)
        pass nothing and copy the lot.
        """
        if not self._counting:
            self.history.push_snapshot(self.canvas.snapshot(box))

    def _resolve_brush(self, brush, size, opacity, overrides: dict) -> Brush:
        b = brush if isinstance(brush, Brush) else get_brush(str(brush))
        _check_brush_overrides(overrides)
        changes = dict(overrides)
        if size is not None:
            changes["size"] = float(size)
        if opacity is not None:
            changes["opacity"] = float(opacity)
        b = b.with_(**changes) if changes else b
        # The one place a painter's `size=` becomes a brush, whichever verb took it,
        # and once per call: a mass hands its own passes the resolved `Brush` with no
        # `size=`, so this does not fire per pass. A `Brush` built by hand and handed
        # in whole is the painter's own and is left alone, the way a named scumble
        # brush is.
        if "size" in changes:
            _check_tip_pixels(self, b, self.canvas)
        if "jitter" in overrides:
            _check_jitter(self, b, float(overrides["jitter"]))
        return b

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
#: Arguments that are real somewhere in this API, are not :class:`~easel.brush.Brush`
#: fields, and are therefore swallowed by a painting call's ``**brush_overrides`` and
#: handed to ``Brush.with_()`` -- which raises about a keyword argument, from a class
#: the painter did not name, naming nothing they can act on. The value is what to say
#: instead. The guide's own promise is *"any brush field is also an override on any
#: painting call"*, so a painter who reads ``solid`` and ``glaze`` in an argument table
#: with no call named beside them has every reason to try this.
def _accepts(method) -> frozenset[str]:
    """Every keyword one of the painting calls takes, off its own signature.

    Read from the call rather than listed here, so that an argument added to a verb
    is an argument a plan may carry on the same day -- which is what went wrong the
    other way round: ``clip=`` was on ``stroke`` and a plan carrying it was refused.
    """
    return frozenset({n for n, q in inspect.signature(method).parameters.items()
                      if q.kind not in (q.VAR_KEYWORD, q.VAR_POSITIONAL)} - {"self"})


#: The brush fields, which are an override on any painting call and so on any entry
#: of a plan. One set, built from the dataclass, for the two checks that use it.
_BRUSH_FIELDS = frozenset(f.name for f in dataclass_fields(Brush))


#: What each kind of plan entry may carry, and the word that names the place it fills.
#: A plan is checked against this **before it is priced**, because pricing walks the
#: passes and never touches the brush overrides -- so a misspelled ``size`` prices
#: happily at the default and then raises when the same plan is painted. A quote for
#: a plan that cannot be painted is worse than no quote: it is the drift a plan object
#: exists to prevent, arriving as a price. The MCP server has refused these since it
#: was built (``_ACCEPTS`` there is this, imported); the library priced them.
PLAN_ACCEPTS = {
    "stroke": _accepts(Session.stroke),
    "mass": _accepts(Session.block_in) | {"shape"},
    "sweep": _accepts(Session.sweep),
    "scumble": _accepts(Session.scumble) | {"shape", "region"},
    "cover": _accepts(Session.cover) | {"cover"},
}


def _check_plan_keys(kind: str, entry: dict) -> None:
    """Refuse a keyword the call would not take, while the plan is still free."""
    unknown = sorted(set(entry) - PLAN_ACCEPTS[kind] - _BRUSH_FIELDS - {"label"})
    if unknown:
        raise ValueError(
            f"A {kind} does not take {', '.join(repr(k) for k in unknown)}. It takes "
            f"{', '.join(sorted(PLAN_ACCEPTS[kind]))} -- and any brush field, to "
            f"override one for this mark alone."
        )


_NOT_BRUSH_FIELDS = {
    "solid": (
        "solid= is an argument of block_in(), stroke(), sweep() and scumble() -- the "
        "pair of brush defaults load=1.0, load_falloff=0.0, which keeps a brush from "
        "running dry partway along -- and not a brush field. cover() lays that pair "
        "already: it is the burying recipe."
    ),
    "glaze": (
        "glaze= is a stroke() argument, not a brush field, and s.glaze(points, color) "
        "is the verb for one. A mass cannot be laid as a glaze -- a glaze is a film "
        "over paint that is already there: lay the mass, s.dry(), then glaze it."
    ),
    "edge": (
        "edge= is a block_in() argument ('ragged', 'clean' or 'hard') and a scumble() "
        "one ('ragged' or 'hard'), not a brush field, and sweep() takes the boundary "
        "itself as its first argument. To hold a mark inside a place that is not the "
        "one it fills, every verb that lays paint takes clip=."
    ),
    "density": (
        "density= is a block_in(), sweep() and cover() argument -- how far apart the "
        "passes run -- not a brush field."
    ),
    "overhang": (
        "overhang= is a block_in(), scumble() and cover() argument -- how far each "
        "pass runs past the ends of the place -- not a brush field."
    ),
    "pressure": (
        "pressure= is an argument of every painting call, not a brush field: it is a "
        "profile along one stroke rather than a property of the brush."
    ),
}


#: How far past its own path a mark can reach, in brush diameters, before the
#: jitter is counted: the dab mask is at most ``1.7`` radii across (``size_jitter``
#: is clipped there), which is ``0.85`` of a diameter from the centre.
_MARK_REACH = 0.85

#: How many standard deviations of the per-dab wander to allow for. The wander is
#: smoothed unit-variance noise scaled by ``jitter x diameter``, so six of them is
#: about one in a billion dabs -- and if one ever does land outside, the undo stack
#: is dropped rather than restored wrongly. See :meth:`Session.stroke`.
_MARK_SIGMA = 6.0


def _stroke_box(canvas, points, b: Brush, smooth: bool) -> tuple[int, int, int, int] | None:
    """The box of canvas one mark can reach, in pixels, before it is laid.

    The undo stack used to hold a copy of the whole canvas per mark -- 33 MB at
    1440x960, about 800 MB over the twenty-four that are kept, and 6.3 ms of copying
    before a dab lands. A mark touches a few percent of a canvas, and this is that
    few percent: the path it will be stamped along (the spline, where there is one,
    because a spline bows outside the points it was fitted through), grown by the
    dab's own radius, by the wander the brush is allowed, and by a hard margin for
    the tooth and the rounding.
    """
    pts = np.atleast_2d(np.asarray(points, dtype=np.float32))
    if pts.ndim != 2 or pts.shape[1] != 2 or not np.isfinite(pts).all():
        # A path this cannot measure is one `paint_stroke` is about to refuse in its
        # own words. Copy the whole canvas and let it: a box is an optimisation, and
        # an optimisation may not take an error message away from the painter.
        return None
    path = catmull_rom(pts) if (smooth and len(pts) >= 3) else pts
    diameter = max(b.size * canvas.long_side, 1.5)
    reach = diameter * (_MARK_REACH + _MARK_SIGMA * max(b.jitter, 0.0)) + 8.0
    xs = path[:, 0] * (canvas.width - 1)
    ys = path[:, 1] * (canvas.height - 1)
    x0 = int(np.clip(np.floor(xs.min() - reach), 0, canvas.width))
    x1 = int(np.clip(np.ceil(xs.max() + reach) + 1, 0, canvas.width))
    y0 = int(np.clip(np.floor(ys.min() - reach), 0, canvas.height))
    y1 = int(np.clip(np.ceil(ys.max() + reach) + 1, 0, canvas.height))
    return x0, y0, max(x1, x0), max(y1, y0)


def _within(bounds, box, canvas) -> bool:
    """Whether what a stroke actually stamped lies inside the box it was given."""
    if bounds is None:
        return True
    bx0, by0, bx1, by1 = bounds
    x0, y0, x1, y1 = box
    return (bx0 * (canvas.width - 1) >= x0 - 1.0
            and bx1 * (canvas.width - 1) <= x1 + 1.0
            and by0 * (canvas.height - 1) >= y0 - 1.0
            and by1 * (canvas.height - 1) <= y1 + 1.0)


#: How many panels one calibration sheet may hold. Two arguments vary together as
#: their combinations, so three sizes and four loads are already twelve marks and
#: twelve renders -- and a sheet nobody can compare at a glance is a contact sheet of
#: a question rather than an answer to it.
_MAX_PANELS = 12


def _vary_settings(vary: dict) -> list[dict]:
    """``{argument: [values]}`` as one dict per panel: every combination, in order."""
    combos: list[dict] = [{}]
    for key, values in vary.items():
        tried = list(values)
        if not tried:
            raise ValueError(
                f"rehearse(vary={{{key!r}: []}}) has nothing to try. Give the values "
                f"to lay the mark at: {{{key!r}: [0.02, 0.05]}}."
            )
        combos = [{**seen, key: value} for seen in combos for value in tried]
    if len(combos) > _MAX_PANELS:
        raise ValueError(
            f"rehearse(vary=...) would lay {len(combos)} panels, past the "
            f"{_MAX_PANELS} a sheet can be compared at a glance: the arguments vary "
            f"together, so their combinations multiply. Try one argument at a time."
        )
    return combos


def _setting_text(value) -> str:
    """One varied setting, as a label: short for a number, plain for anything else."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return str(value)
    return f"{float(value):.3g}"


def _as_timelapse(value) -> bool | int:
    """``timelapse=`` as it is kept: ``True``/``False``, or a frame size in pixels.

    A bool is a bool and an int is a size, which ``isinstance(True, int)`` makes
    worth being careful about. Saved under the same key it always was, so a build
    that only knows the flag reads ``bool(360)`` and is right.
    """
    if isinstance(value, bool) or value is None:
        return bool(value)
    px = int(value)
    if px < 1:
        raise ValueError(
            f"Session(timelapse={value!r}) is True, False, or the frame's long side "
            f"in pixels, which is at least 1. The default is {DEFAULT_FRAME_PX}."
        )
    return px


def _highest_numbered(out_dir: Path, prefix: str) -> int:
    """The largest ``N`` in ``<out_dir>/<prefix>_NNN.png``, or ``0`` for none.

    A directory is the one piece of state every session writing into it can see,
    so it is where a look's number comes from. See :meth:`Session._next_free_path`.
    """
    highest = 0
    for existing in Path(out_dir).glob(f"{prefix}_*.png"):
        number = existing.stem[len(prefix) + 1:]
        if number.isdigit():
            highest = max(highest, int(number))
    return highest


def _check_smudge_size(session, size: float) -> None:
    """Warn when a smudge is wide enough to drag a lobe instead of softening a join.

    The same shape as the scumble's two warnings: the verb still does exactly what it
    was asked, and says what it is about to look like. The measurement it is reading
    off is in :meth:`Session.smudge` -- past about ``0.02`` a single pass buys no more
    softening and goes on reaching further into the dark mass, and four of five
    smudges in one painting arrived as pale finger-shaped lobes at ``0.024``-``0.032``.
    """
    if float(size) <= SMUDGE_MAX:
        return
    session._notify(
        "smudge-wide",
        f"smudge(size={float(size):.3g}) is past the {SMUDGE_MAX:.3g} where one pass "
        f"stops softening a join and starts dragging a lobe. Measured on a steep "
        f"step, one pass carries the lighter mass 1.3% of the canvas height into the "
        f"darker at {SMUDGE_SIZE:.3g}, 2.3% at 0.040 and 4.4% at 0.070 -- for a join "
        f"no softer than {SMUDGE_SIZE:.3g} already leaves it. Rehearse it, or use "
        f"size={SMUDGE_SIZE:.3g} and put the rest in with paint.",
        stacklevel=3,
    )


#: A step at least this far apart in value is a boundary between two masses: the
#: ``0.10`` every pair of masses in the guide is read by. A smudge whose path crosses
#: one drags the first mass into the second. See :func:`_check_smudge_path`.
_SMUDGE_STEP = 0.10

#: How far a smudge may run along a boundary before the strip it leaves reads as a band
#: of its own, as a share of the canvas long side. ``RECIPES.md``'s *past about a tenth
#: of the canvas*, and what the strip does at every length measured: one pass along a
#: hard step leaves a strip about one brush tall at the value halfway between the two
#: masses, the same at ``0.05`` long as at ``0.80`` -- a softened corner at the short
#: end, and from here on a drawn line of a third value.
_SMUDGE_LONG = 0.10

#: The smallest step across a smudge's path that it counts as following a boundary. The
#: strip lands halfway, so each of its two edges is half the step; and a join between two
#: colours at close values still leaves a strip of a third colour, so this is half the
#: ``0.10`` and not the whole of it.
_SMUDGE_FOLLOW = 0.05


def _box_mean(view: np.ndarray, r: int) -> np.ndarray:
    """A ``(2r+1)`` square mean of a 2-D array, off an integral image, edges held.

    A value read off one pixel of a painted canvas is the tooth as much as the paint;
    averaged over a few pixels it is the paint, which is what a smudge meets.
    """
    if r <= 0:
        return view.astype(np.float32)
    k = 2 * r + 1
    pad = np.pad(view.astype(np.float64), r + 1, mode="edge")
    ii = pad.cumsum(axis=0).cumsum(axis=1)
    h, w = view.shape
    total = ii[k:k + h, k:k + w] - ii[0:h, k:k + w] - ii[k:k + h, 0:w] + ii[0:h, 0:w]
    return (total / (k * k)).astype(np.float32)


class _SmudgeRead(NamedTuple):
    """What :func:`_smudge_samples` read along a smudge's path, one entry per sample."""

    arc: np.ndarray       # distance from the start, as a share of the canvas long side
    behind: np.ndarray    # the value half a brush back along the path
    ahead: np.ndarray     # ...and half a brush on
    along: np.ndarray     # the step between those two: a boundary being crossed
    across: np.ndarray    # the step across the path: a boundary being followed
    on: np.ndarray        # the value under the sample itself
    points: np.ndarray    # the sample, normalised


def _smudge_samples(canvas, path, size: float, smooth: bool = True):
    """What a smudge meets along the path it is about to be dragged down.

    The path the stroke will actually be stamped along -- the spline, where there is
    one -- walked a quarter-brush at a time, and at every sample the canvas value one
    brush apart *along* the path and *across* it: the first is a boundary the smudge
    is crossing, the second a boundary it is following. Read off the canvas before the
    smudge lands and sampled, never rasterised, so it costs a few hundred reads of a
    crop of the canvas and not a copy of it.

    Returns a :class:`_SmudgeRead` -- per sample, the distance from the start of the
    path as a share of the canvas long side, the values half a brush behind and ahead
    along the path and the step between them, the step across it, the value under the
    sample itself, and its normalised point -- or ``None`` for a path of one point.
    """
    pts = np.atleast_2d(np.asarray(path, dtype=np.float32))
    if pts.ndim != 2 or pts.shape[1] != 2 or len(pts) < 2 or not np.isfinite(pts).all():
        return None
    line = catmull_rom(pts) if (smooth and len(pts) >= 3) else pts
    w, h = canvas.width, canvas.height
    px = np.stack([line[:, 0] * (w - 1), line[:, 1] * (h - 1)], axis=1).astype(np.float64)
    seg = np.hypot(*np.diff(px, axis=0).T)
    total = float(seg.sum())
    diameter = max(float(size) * canvas.long_side, 1.5)
    if total < 1.0:
        return None
    count = int(np.clip(total / max(diameter * 0.25, 1.0), 8, 512)) + 1
    cum = np.concatenate([[0.0], np.cumsum(seg)])
    want = np.linspace(0.0, total, count)
    walk = np.stack([np.interp(want, cum, px[:, 0]), np.interp(want, cum, px[:, 1])], axis=1)
    tangent = np.gradient(walk, axis=0)
    tangent /= np.maximum(np.hypot(tangent[:, 0], tangent[:, 1]), 1e-9)[:, None]
    normal = np.stack([-tangent[:, 1], tangent[:, 0]], axis=1)
    half = 0.5 * diameter
    reach = half + 4.0
    x0 = int(np.clip(np.floor(walk[:, 0].min() - reach), 0, w - 1))
    x1 = int(np.clip(np.ceil(walk[:, 0].max() + reach) + 1, x0 + 1, w))
    y0 = int(np.clip(np.floor(walk[:, 1].min() - reach), 0, h - 1))
    y1 = int(np.clip(np.ceil(walk[:, 1].max() + reach) + 1, y0 + 1, h))
    # The values view, over the crop the samples can reach: sRGB-encoded luminance,
    # the number `look(values=True)` shows and every threshold here is written in.
    view = _box_mean(linear_to_srgb(luminance(canvas.rgb[y0:y1, x0:x1])), 2)

    def at(q: np.ndarray) -> np.ndarray:
        cols = np.clip(np.round(q[:, 0]).astype(int) - x0, 0, x1 - x0 - 1)
        rows = np.clip(np.round(q[:, 1]).astype(int) - y0, 0, y1 - y0 - 1)
        return view[rows, cols]

    behind, ahead = at(walk - tangent * half), at(walk + tangent * half)
    return _SmudgeRead(
        arc=want / float(canvas.long_side),
        behind=behind,
        ahead=ahead,
        along=np.abs(ahead - behind),
        across=np.abs(at(walk + normal * half) - at(walk - normal * half)),
        on=at(walk),
        points=np.stack([walk[:, 0] / max(w - 1, 1), walk[:, 1] / max(h - 1, 1)], axis=1),
    )


def _smudge_crossing(read: _SmudgeRead, size: float) -> tuple[int, float] | None:
    """Where a smudge's path crosses a boundary and goes on past it, or ``None``.

    A step shows in every sample within half a brush of it, so the samples that see
    one come in runs about a brush long, and which of them saw it first says nothing
    about where the line is. The line is where the value *on the path itself* passes
    halfway between the two masses -- read half a brush behind and ahead of the run's
    strongest sample, where each is whole -- and that point is found between samples,
    not at one: a step blurred symmetrically crosses its halfway value on the edge.

    A crossing counts with half a brush of path before the line, so the brush has
    taken up the first mass, and a quarter-brush after it, so its centre goes on over
    and its half-width carries the first mass three-quarters of a brush in. A smudge
    that only starts or stops on the line carries half a brush across at most, which
    is what one run along the join does anyway.

    Returns ``(sample, arc)`` -- the strongest sample of the strongest crossing that
    counts, and the distance of its line from the start of the path -- or ``None``.
    """
    arc, along, on = read.arc, read.along, read.on
    seen = (along >= _SMUDGE_STEP) & (along >= read.across)
    length = float(arc[-1])
    best = None
    n = len(seen)
    i = 0
    while i < n:
        if not seen[i]:
            i += 1
            continue
        j = i
        while j + 1 < n and seen[j + 1]:
            j += 1
        k = i + int(np.argmax(along[i:j + 1]))
        half = 0.5 * (float(read.behind[k]) + float(read.ahead[k]))
        lo, hi = max(i - 1, 0), min(j + 1, n - 1)
        side = np.sign(on[lo:hi + 1] - half)
        flips = np.nonzero(side[:-1] * side[1:] < 0)[0]
        if len(flips):
            m = lo + int(flips[0])
            rise = float(on[m + 1] - on[m])
            t = (half - float(on[m])) / rise if rise else 0.5
            where = float(arc[m]) + float(np.clip(t, 0.0, 1.0)) * float(arc[m + 1] - arc[m])
        else:
            where = float(arc[k])
        if where / size >= 0.5 and (length - where) / size >= 0.25:
            if best is None or along[k] > along[best[0]]:
                best = (k, where)
        i = j + 1
    return best


def _check_smudge_path(session, path, size: float, smooth: bool = True) -> None:
    """Say, before a smudge lands, what it will do to the boundaries it meets.

    Two things, off one reading of the canvas along the path (:func:`_smudge_samples`):

    - **``smudge-across``**, a fact: the path crosses a step of at least
      :data:`_SMUDGE_STEP` -- more of it along the path than across it -- arriving
      from one mass and going on into the other (:func:`_smudge_crossing` says how
      far on each side counts). Dragged across a boundary it carries the first mass about a
      brush into the second, which is the thumbprint finding 3 of the 0.5.0 cohort
      reported. Measured with the start of the stroke fixed (a smudge carries only
      what it has picked up since 0.6.0): ``1.2`` brushes at ``size=0.04`` across a
      step from ``0.20`` to ``0.78``, either way round, and ``0.5`` at the same
      settings along it.
    - **``smudge-long``**, a habit: the path follows a boundary -- a step of at least
      :data:`_SMUDGE_FOLLOW` across it -- for more than :data:`_SMUDGE_LONG` of the
      canvas. Its strip is about a brush tall at any length and lands halfway between
      the two values, so over a long boundary it reads as a third band. A habit and not
      a fact, because a painter can want the band: two paintings smoothed the broken
      lit edge of a neck this way and it read as intended.

    Neither is said on a counted copy, which borrowed the canvas and has laid none of
    the pass that the smudge would meet.
    """
    if session._counting:
        return
    read = _smudge_samples(session.canvas, path, size, smooth)
    if read is None:
        return
    arc, along, across, points = read.arc, read.along, read.across, read.points
    size = max(float(size), 1e-6)
    length = float(arc[-1])
    found = _smudge_crossing(read, size)
    if found is not None:
        i, line = found
        x, y = (float(v) for v in points[i])
        session._notify(
            "smudge-across",
            f"smudge crosses a boundary at ({x:.2f}, {y:.2f}), {line:.2f} from where "
            f"it starts: the value steps {along[i]:.2f} along the path there and "
            f"{across[i]:.2f} across it. Dragged across a boundary a smudge carries the "
            f"first mass into the second -- about a brush of it, as a thumbprint. Run "
            f"it along the boundary instead: hand it the boundary's own points, or a "
            f"stretch of the shape's outline (shape.closed[i:j]).",
            stacklevel=3,
        )
    follows = across >= _SMUDGE_FOLLOW
    run = float(follows.mean()) * length
    if run >= _SMUDGE_LONG:
        step = float(np.median(across[follows]))
        session._notify(
            "smudge-long",
            f"smudge runs {run:.2f} of the canvas along a boundary, a step of {step:.2f} "
            f"across it: its strip is about a brush tall at any length and lands halfway "
            f"between the two, so over this length it reads as a third band -- dark, "
            f"mid, light, two edges where there was one. Smudge the stretch you mean to "
            f"lose, under about {_SMUDGE_LONG:.2f}, and lay paint across the rest.",
            stacklevel=3,
        )


#: How far a pixel's colour has to move, in Oklab, before it counts as under a film.
#: Separates the paint a film laid from the arithmetic at its fringe, where a soft tip
#: fades through thousandths that no eye reads and that would only dilute the mean.
_FILM_FOOTPRINT = 0.005

#: The value shift over a film's own footprint at which it stops shifting a mass and
#: lays a new one. Where the guide's own glaze table puts it -- a warm film over a cool
#: dark moves the value ``0.085`` at ``opacity=0.14``, *a stripe of a different
#: colour* -- and the corpus's own p90: the 222 films of the 0.5.0 corpus move the
#: passage under them ``0.033`` at the median and ``0.081`` at p90.
_FILM_NEW_MASS = 0.08

#: How far a film may be mixed from what it lands on, in the Oklab chroma plane --
#: hue and saturation, the plane :meth:`~easel.palette.Palette.chroma_of` measures
#: in -- before it lays a colour of its own rather than tinting the passage. The
#: guide's own recipes mix their films ``0.031``-``0.051`` from the field they land
#: on; every film the corpus shows as a bloom sits at ``0.080`` or more -- the harbour's
#: searchlight at ``0.085``, the lighthouse's orange glow over a violet sky at ``0.190``.
#: The corpus's p90 is ``0.068``. It is a distance in the mixing and not in the result,
#: because no opacity rescues it: a lower opacity is the same colour, fainter.
_FILM_FAR = 0.07


def _film_shift(before: np.ndarray, after: np.ndarray,
                color=None) -> tuple[float, float, int]:
    """What a film did to the passage it landed on: ``(value, mixed, pixels)``.

    ``before`` and ``after`` are the same box of linear RGB either side of the film.
    Over the pixels whose colour moved more than :data:`_FILM_FOOTPRINT` -- the
    film's own footprint, as :meth:`Session.glaze` measures ``to_value=`` over --
    ``value`` is the mean change in value (the sRGB-encoded luminance
    ``look(values=True)`` shows), and ``mixed`` is how far the film's own ``color``
    sits from the mean colour it landed on, in the Oklab chroma plane (``0.0`` when
    no colour is given).
    """
    ok_before = linear_to_oklab(before)
    moved = np.sqrt(((linear_to_oklab(after) - ok_before) ** 2).sum(axis=-1)) > _FILM_FOOTPRINT
    pixels = int(moved.sum())
    if not pixels:
        return 0.0, 0.0, 0
    value = np.abs(linear_to_srgb(luminance(after[moved]))
                   - linear_to_srgb(luminance(before[moved])))
    mixed = 0.0
    if color is not None:
        film = linear_to_oklab(np.asarray(color, dtype=np.float32))
        under = linear_to_oklab(before[moved].mean(axis=0))
        mixed = float(np.hypot(float(film[1] - under[1]), float(film[2] - under[2])))
    return float(value.mean()), mixed, pixels


def _check_glaze_far(session, box, before: np.ndarray, color, aimed: bool = False,
                     stacklevel: int = 3) -> None:
    """Say what a film did once it has landed, when it did more than a film is for.

    Finding 4 of the 0.5.0 cohort: *green blooms over blue water, a searchlight on a
    flat sheet*. A glaze is strong in proportion to its distance from what it lands
    on, in hue as well as in value, and the guide's answer -- mix it close, then
    choose an opacity -- had a table and no instrument. This is the instrument, and it
    measures the paint rather than predicting it, as ``holes`` does: the film is laid,
    and the box it could reach is read either side of it.

    Two ways past what a film is for, one code. The value moved by
    :data:`_FILM_NEW_MASS` or more, which is a new mass -- not said about a film
    given ``to_value=``, which asked for exactly that shift. Or the film was mixed
    :data:`_FILM_FAR` or more from what it lands on, in hue and chroma, which no
    opacity rescues and no ``to_value=`` either: that search finds a value, and the
    colour it lands at is still the film's.
    """
    x0, y0, x1, y1 = box
    value, mixed, pixels = _film_shift(before, session.canvas.rgb[y0:y1, x0:x1], color)
    if pixels < 16:
        return
    if value >= _FILM_NEW_MASS and not aimed:
        session._notify(
            "glaze-far",
            f"this film moved the passage under it by {value:.3f} in value, over its own "
            f"footprint: past {_FILM_NEW_MASS:.2f} a film stops shifting a mass and lays "
            f"a new one. Aim it at the value the passage should read afterwards "
            f"(to_value=), or lay the change as paint.",
            stacklevel=stacklevel,
        )
    elif mixed >= _FILM_FAR:
        session._notify(
            "glaze-far",
            f"this film was mixed {mixed:.3f} from what it lands on in hue and chroma "
            f"(Oklab), and moved the value {value:.3f}: that far off, a film does not "
            f"tint the passage, it lays a colour of its own over it. Mix it close to "
            f"what it lands on -- s.palette.mix(field, film, ...) -- because a lower "
            f"opacity is the same colour, fainter.",
            stacklevel=stacklevel,
        )


#: The density at which a comb's own gaps close on a solid mass. Below it the passes
#: are further apart than the width the comb actually covers -- about three-quarters
#: of its own -- and the mass keeps the holes. Measured on a shaped mass at
#: ``size=0.04``: ``0.1552%`` bare at ``density=0.8`` and ``0.0000%`` at this.
_COMB_CLOSES_AT = 1.2


def _check_solid_comb(session, b: Brush, density: float, solid: bool,
                      stacklevel: int = 3) -> None:
    """Say, at the call, what share of a solid comb mass will come back bare.

    Two painters reported holes inside a ``solid=True`` mass as *shaped block-in
    paths wandering apart*. They are not: a ``flat`` leaves ``0.0000%`` bare at every
    size and density tried, and the comb leaves them at any spacing under
    ``_COMB_CLOSES_AT`` -- because ``solid=`` sets ``load`` and ``load_falloff`` and
    nothing else, so it closes the gaps *along* a pass and not the ones the comb's
    own missing bristles leave *across* it.

    A **fact**, not a habit: nothing here says the comb is the wrong brush, and no
    default moves. A comb is the right tip for foliage, cloth and anything with
    strands in it, and its holes only read where the ground is darker than the paint
    -- ``0.16%`` of the mass on a mid ground and ``3.16%`` on a dark one, which is
    the number worth printing at the call.
    """
    asked = solid or (b.load >= 1.0 and b.load_falloff <= 0.0)
    if not asked or b.tip != "bristle" or float(density) >= _COMB_CLOSES_AT:
        return
    session._notify(
        "solid-comb",
        f"block_in(solid=True) with a bristle ({b.name!r}): solid= sets load=1.0 and "
        f"load_falloff=0.0, which closes the gaps along each pass and not the ones "
        f"the comb leaves across it. Measured at size=0.04, density=0.8, a shaped "
        f"mass comes back 0.16% bare in 47 blobs on a mid ground -- and 3.16% in 373 "
        f"blobs, the largest 2270 px, on a dark one, because a hole is a contrast "
        f"rather than a gap. density={_COMB_CLOSES_AT:.3g} closes them, at about a "
        f"fifth more passes; a 'flat' or 'knife' closes them at this density for the "
        f"same money; crossed passes for twice it.",
        stacklevel=stacklevel,
    )


#: How much of a mass has to come back bare before the ``holes:`` line says so. The
#: corpus's own solid masses run ``0.000`` at the median and ``0.066`` at p90 for a
#: ``flat``, so half a percent is comfortably above what a mass that worked leaves
#: and well under the ``3.16%`` a comb leaves where the holes actually read.
_HOLES_FLOOR = 0.005

#: How far the paint has to sit from the ground before a hole in it is visible, in
#: value. **A hole is a contrast, not a gap** (`CALIBRATION.md`, B2): the same comb,
#: the same call, leaves ``0.16%`` bare on ``toned_grey`` and ``3.16%`` on a dark
#: ground -- not because it left more holes, but because *bare* means within
#: ``10/255`` of the ground and a mass painted near its own ground has nothing to
#: show through. Under this, the holes are there and nobody can see them, so saying
#: so is the noise `LESSONS.md` rule 2 is about.
_HOLES_CONTRAST = 0.15


def _check_holes(session, place, b: Brush, color, stacklevel: int = 1) -> None:
    """What a mass laid solid actually came back with, measured (finding 2).

    Solid by ``solid=True`` or by a brush already carrying ``load=1.0,
    load_falloff=0.0``, which is what :meth:`~easel.session.Session.cover` lays and
    refuses ``solid=`` as a duplicate of.

    :func:`_check_solid_comb` predicts this at the call from the brush and the
    density; this measures the canvas once the paint is on it, which is the only way
    to answer for the *shape*, the *ground* and the *overlap* a prediction cannot
    see. The two are one pair on purpose: a painter who ignores the prediction and
    lays it anyway gets the number, and a painter who took the advice gets silence.

    **The share is of the shape's own interior**, a brush in from the outline, so
    that a ragged edge -- which is what ``edge="ragged"`` is *for* -- is not counted
    as a hole. And *bare* is :meth:`~easel.canvas.Canvas.ground_showing`'s own
    definition, within ``10/255`` of the bare canvas, which is what that method means
    by it and what an eye means by it.

    Silent under :data:`_HOLES_CONTRAST`, because a hole is a contrast and not a
    gap. A mass painted within a seventh of its own ground has holes nobody can see.
    Ungated, this fired after **8%** of the 343 passes of the corpus replay
    (`CALIBRATION.md`), which is over the plan's noise ceiling; the gate is what
    makes it worth printing, and it is the reason B2's own ``3.16%`` on a dark ground
    does not print -- that number is burnt umber failing to register on near-black,
    not a hole anybody can see.
    """
    if session._counting:
        # A counted copy borrowed the canvas and laid nothing on it: the paint this
        # call would have put down is not there to find holes in, so every pixel of
        # the shape would read bare and the line would be a lie about a real mass.
        return
    inner = _clean_fill(place, b.size * 0.6)
    mask = session.canvas._mask_of(inner)
    if mask is None:
        x0, y0, x1, y1 = session.canvas.region_px(inner)
        mask = np.zeros((session.canvas.height, session.canvas.width), dtype=bool)
        mask[y0:y1, x0:x1] = True
    if int(mask.sum()) < 64:
        # Smaller than the brush that laid it: the inset has eaten the shape, which
        # `clean-small` is the notice for, and there is no interior left to measure.
        return
    share = session.canvas.ground_showing(where=mask)
    if share < _HOLES_FLOOR:
        return
    # Both through the palette's own instrument, so the two numbers are comparable
    # and are the ones `look(values=True)` shows -- sRGB-encoded luminance, not
    # linear. The ground is averaged over the bare canvas rather than read off the
    # spec, because a ground is shaded by its own tooth and a painter may have
    # given a mixture.
    ground = float(linear_to_srgb(luminance(session.canvas.bare())).mean())
    laid = session.palette.value_of(session._resolve_color(color))
    if abs(laid - ground) < _HOLES_CONTRAST:
        return
    session._notify(
        "holes",
        f"holes: {share:.2%} of this solid {b.name!r} mass came back bare -- the "
        f"ground showing through it, at {abs(laid - ground):.2f} of value between "
        f"the two, which is enough to read. solid= sets load and load_falloff and "
        f"closes the gaps along a pass, not the ones a comb leaves across it: a "
        f"denser pass, a 'flat' or 'knife', or crossed passes close these.",
        stacklevel=stacklevel,
    )


#: The tips whose width does not follow pressure: a chisel is the width it was given.
_CHISEL_TIPS = ("flat", "bristle", "knife")

#: Under this many pixels wide an oriented tip stops depositing paint at all. It is a
#: count of **pixels**, not a ``size``, and that is the whole point: the cliff sits at
#: the same pixel width on every canvas, so the ``size`` it corresponds to moves by a
#: factor of four between a 300px canvas and a 1200px one. Measured on a solid
#: block-in with every clause of *a plane that is a plane* -- ``density=1.0``,
#: ``solid=True``, ``opacity=1.0``, ``pressure="even"`` -- a mixture at ``0.865`` over
#: a ground at ``0.395``, 600x600 linen: a ``flat`` lands ``0.399`` at 3.5px and
#: ``0.683`` at 5px, and one stroke of a ``flat``, ``bristle`` or ``knife`` deposits
#: **zero** paint at 1-2px against a ``round_hard``'s 44-51 pixels' worth. Checked on
#: 300, 600 and 1200px canvases: the knee is at 4px on all three.
_CHISEL_MIN_PX = 4.0


def _check_tip_pixels(session, b: Brush, canvas, stacklevel: int = 4) -> None:
    """Warn when an oriented tip is too few pixels wide to lay any paint.

    Not an aesthetic rule like the comb floor, which a painter can want to break: a
    chisel under about four pixels does not make a poor mark, it makes **no mark**,
    and is still charged against the budget. A painter spent four rehearsals on a
    bird's head laid at ``size=0.005`` that came back a dark fuzzy ball rather than
    the mixture it was given.

    The condition the request proposed was ``size`` under about ``0.008``, and that
    is the wrong unit: ``size`` is a fraction of the canvas long side, so ``0.008``
    is 2.4px on a 300px canvas -- already dead -- and 9.6px on a 1200px one, which
    is a perfectly good small brush. Measured on three canvas sizes, the cliff is at
    four *pixels* on all of them. A round tip has no such cliff and is what to reach
    for at this scale; ``liner`` is a ``round_hard`` at ``size=0.005`` for exactly
    this reason and does not trip it.
    """
    if b.tip not in _CHISEL_TIPS:
        return
    px = b.size * float(canvas.long_side)
    if px >= _CHISEL_MIN_PX:
        return
    session._notify(
        "chisel-blank",
        f"a {b.tip} tip at size={b.size:.4g} is {px:.1f} pixels wide on this canvas, "
        f"under the {_CHISEL_MIN_PX:.0f} where an oriented tip stops depositing paint "
        f"at all -- the mark is charged and lands nothing. Measured, a solid mass laid "
        f"this small comes back the value of whatever it was laid over. Use round_hard "
        f"(or liner, which is one) at this scale, or size="
        f"{_CHISEL_MIN_PX / float(canvas.long_side):.4g} and up.",
        stacklevel=stacklevel,
    )

#: Under this share of the canvas, :meth:`Session.report` says the ground has gone.
#: A **judgement**, not a measurement, and the one number in the check that is: the
#: closing checklist says *there should be* some ground showing and does not say how
#: much. It is placed an order of magnitude from each of the two anchors there are.
#: Above: a mottled ``density=1.0`` mass leaves **4.4%** of its interior within
#: ``0.05`` of bare, which is ground plainly showing and what a first pass is for.
#: Below: a painting whose warm ground had been chosen to be seen through, and was
#: not, finished at **0.07%**. Raise or ignore it freely -- the number beside it is
#: the instrument, and this is only what makes a painter look at the number.
_GROUND_FLOOR = 0.005

#: A mark shorter than this many brush widths is a *shape* rather than a pass, and
#: the one a painter reaches for a pressure list on expecting a taper. Longer than
#: this, a list on a chisel is grading the paint along a pass, which it does.
_SHORT_MARK_WIDTHS = 4.0


#: How many times the ``Brush.jitter`` default an override may ask for before it says
#: so. ``jitter`` is the standard deviation of each dab's offset **in tip diameters**,
#: smoothed along the stroke, so what it buys is width: measured on a straight
#: ``liner`` stroke at ``pressure="even"``, 1024x768, the painted band is **1.2**
#: brushes across at the default, **1.8** at ``0.1``, **2.2** at ``0.2`` and **3.7**
#: at ``0.5``. Five times the default is where a line stops being one brush wide,
#: which is the thing a line is. A painter read *halving both halves the wander* as
#: naming an operation rather than a number, passed ``0.5``, and every member of a
#: greenhouse frame came back a chain of beads; the call looked exactly like the
#: recipe and nothing said a word.
_JITTER_MULTIPLE = 5.0

#: What the band widens to, per unit of ``jitter``, in tip diameters: the slope of the
#: measured run above, end to end, quoted in the warning so the painter gets a number
#: rather than an adjective. It runs a little under the middle of that table and lands
#: on its far end, which is where this fires hardest and where it matters.
_JITTER_WIDTHS = 5.3


def _check_jitter(session, b: Brush, asked: float) -> None:
    """Warn when a ``jitter=`` override is a multiple of the default rather than a tweak.

    The same shape as the comb floor and the chisel-pixel floor: a number a painter
    can reach for out of a recipe, with no good outcome past a measured wall. It fires
    on the *override* and not on a brush's own field, because every named brush in the
    box sits between ``0`` and ``0.03`` and a ``Brush`` built by hand is the painter's
    own -- the way :func:`_check_tip_pixels` only looks when ``size`` was asked for.
    """
    default = float(next(f for f in dataclass_fields(Brush) if f.name == "jitter").default)
    if asked <= _JITTER_MULTIPLE * default:
        return
    session._notify(
        "jitter-beads",
        f"jitter={asked:g} is {asked / default:.0f} times the default of {default:g}. "
        f"It is the wander of each dab in tip diameters, so it comes out as width: a "
        f"stroke lands about {1.2 + _JITTER_WIDTHS * (asked - default):.1f} brushes "
        f"across here against 1.2 at the default, which is a chain of beads rather "
        f"than a line. Past {_JITTER_MULTIPLE * default:g} a mark stops being one "
        f"brush wide. To halve the wander, pass jitter={default / 2:g}.",
        stacklevel=4,
    )


def _check_pressure_on_tip(session, b: Brush, pressure, pts: np.ndarray, canvas) -> None:
    """Warn when a pressure list on a chisel tip is asking for a width it cannot give.

    The documentation already says an oriented tip keeps its chisel under any
    pressure, and two painters read it and laid every pot as a rectangle with chisel
    ends anyway -- *warning is not method*. So the engine says it at the call, in the
    shape ``smudge``'s size warning has: only for a list with more than one value
    (a named profile is the engine's own, and a scalar asks for nothing along the
    mark), and only on a mark short enough to be a shape rather than a pass, because
    a list on a long pass of a `flat` is how a passage brightens toward one side and
    is doing exactly what it should.
    """
    if b.tip not in _CHISEL_TIPS or isinstance(pressure, str):
        return
    arr = np.atleast_1d(np.asarray(pressure, dtype=np.float32))
    if arr.size < 2 or float(arr.max() - arr.min()) < 0.05:
        return
    # The mark's length in the brush's own unit, the canvas long side.
    long = float(canvas.long_side)
    dx = (float(pts[:, 0].max()) - float(pts[:, 0].min())) * canvas.width / long
    dy = (float(pts[:, 1].max()) - float(pts[:, 1].min())) * canvas.height / long
    if math.hypot(dx, dy) > _SHORT_MARK_WIDTHS * b.size:
        return
    shown = ", ".join(f"{float(v):g}" for v in arr[:4]) + (", ..." if arr.size > 4 else "")
    session._notify(
        "chisel-pressure",
        f"pressure=[{shown}] on a {b.tip} tip changes the paint, not the width: a "
        f"chisel keeps the width it was given, so this mark comes back a rectangle "
        f"with a lighter end rather than a taper. A mark that tapers wants "
        f"round_hard or liner, whose width follows pressure; a flat or knife wants a "
        f"length.",
        stacklevel=4,
    )


#: How many times its axis price a shaped block-in with ``direction`` left off may
#: cost before it says so. Measured on one painting's two tower planes: 3.9x and 11x
#: at the default against ``"axis"``, and 1.0x on the one mass wider than tall.
_DIRECTION_RATIO = 2.5


def _check_default_direction(session, place, b: Brush, density: float, overhang,
                             stacklevel: int = 2) -> None:
    """Warn when a shaped block-in with ``direction`` left off costs far more than its axis.

    The default is horizontal and stays horizontal -- ``"axis"`` would be right nearly
    always and moving the default would move every painting ever made. What changes
    is that the price walk, which already has the number, says it: a painter costed
    two planes at 9 and 9 with ``direction=90``, wrote the calls without it, and the
    rehearsal came back charging 124 for a pass budgeted at 40.
    """
    if not isinstance(place, Polygon):
        return
    # On a trial copy: walking the passes draws their wander, and the count does
    # not depend on it.
    trial = session._trial_session()
    laid = sum(1 for _ in trial._block_in_paths(place, b, None, density, overhang))
    along = sum(1 for _ in trial._block_in_paths(place, b, "axis", density, overhang))
    if laid <= _DIRECTION_RATIO * max(along, 1):
        return
    session._notify(
        "direction-default",
        f"block_in of {place.name or 'this shape'} with direction= left off runs its "
        f"passes horizontally and lays {laid} of them, stepping down the whole "
        f"height; along the mass's own axis it is {along} (direction=\"axis\", or "
        f"{place.axis:.0f} degrees). That is {laid / max(along, 1):.1f}x the price.",
        stacklevel=stacklevel,
    )


def _check_direction_sequence(session, place, b: Brush, direction, density: float,
                              overhang, stacklevel: int = 2) -> None:
    """Warn when a sequence of directions costs far more than any one angle in it.

    A sequence is *one whole pass per angle*, and the mass is charged the **sum**.
    That is the price walk's other blind spot: the default-direction check above
    fires on ``direction`` left off, and nothing fired on a painter who did choose
    one and chose ten. Measured on one painting's room mass, same brush, same
    density, same call: ``"axis"`` **4** strokes, a single ``-17`` degrees **7**,
    ``"cross"`` **15**, and a ten-angle sequence **85** -- which is exactly
    ``4 + 5 + 7 + 7 + 9 + 10 + 10 + 11 + 11 + 11``, the ten angles' own prices
    added up.

    The painter who raised this guessed the mechanism was that the stack is sized
    for the steepest angle in the list, which would have made the sequence cost
    about what its dearest member costs. It does not: **every angle is paid for in
    full**, and a steep angle on a wide mass is several times a shallow one, so the
    bill grows with the list and not with its worst entry. Their own numbers
    reproduce to the stroke; the mechanism they offered as a guess, and marked as
    one, is the half that was wrong.

    So the threshold is the request's own words -- *priced far above any single
    angle in it*. Two angles can never be more than twice the dearer of them, which
    leaves the pair idiom every painting in this repository uses (a cross at the
    mass's own angle, ``(4, 94)``) silent, and catches the list that is really a
    stack. The remedy is the pair: two directions break a comb, which is what the
    guide asks for, and ten do not break it any further.
    """
    dirs = _pass_directions(direction)
    if len(dirs) < 2:
        return
    # On a trial copy, for :func:`_check_default_direction`'s reason: walking the
    # passes draws their wander, and the count does not depend on it.
    trial = session._trial_session()

    def price(d) -> int:
        return sum(1 for _ in trial._block_in_paths(place, b, d, density, overhang))

    each = [price(d) for d in dirs]
    total, dearest = sum(each), max(each)
    if total <= _DIRECTION_RATIO * max(dearest, 1):
        return
    # Normalised into [0, 180): a mass whose axis is 90 would otherwise be sent to
    # `("axis", 180)`, which is horizontal written the long way round.
    across = (place.axis + 90.0) % 180.0
    pair = price(("axis", across))
    session._notify(
        "direction-sequence",
        f"block_in of {place.name or 'this shape'} with a sequence of {len(dirs)} "
        f"directions lays one whole pass at every one of them and is charged the "
        f"sum: {total} strokes, from {' + '.join(str(e) for e in each)}. No single "
        f"angle in the list costs more than {dearest} -- a sequence is not one pass "
        f"stacked, it is {len(dirs)} passes. Two directions are what breaks a comb "
        f"and {len(dirs)} do not break it further: a cross at the mass's own angle, "
        f"direction=(\"axis\", {across:.0f}), is {pair} here.",
        stacklevel=stacklevel,
    )


#: The tips whose pass end is a straight line across the pass, and so stacks into a
#: step. Narrower than :data:`_CHISEL_TIPS`, which is about width following pressure
#: and counts the comb among them: a comb's end is broken into bristles and a disc's
#: is round, which is why both measure at a twentieth of a chisel's on the same shape
#: (``CALIBRATION.md``, *The chisel staircase*).
_STAIR_TIPS = ("flat", "knife")

#: How tall a ledge has to be, in brush widths, before it reads as a step down the
#: boundary rather than as the ragged edge a ``block_in`` has anyway.
_STAIR_RISE = 2.0

#: ...and how many ledges the outline has to take before it is a staircase and not a
#: single jag. Three is where the corpus and the guide part company: the band
#: ``CALIBRATION.md`` measures the staircase on takes **5.8**, Kimi's rock face
#: **5.0** and *a mass built of planes* **11.7** on its lit plane, while the one
#: guide block that comes near without being one -- a half-canvas rectangle swept six
#: degrees off its own top edge, which takes a single end on the top and one on the
#: bottom -- takes **2.0**.
_STAIR_LEDGES = 3.0


def _outline_sides(place) -> list:
    """A place's outline, as the straight sides a pass can end against."""
    if isinstance(place, Polygon):
        pts = list(place.closed)
    else:
        r = as_region(place)
        pts = [(r.x0, r.y0), (r.x1, r.y0), (r.x1, r.y1), (r.x0, r.y1), (r.x0, r.y0)]
    return list(zip(pts, pts[1:], strict=False))


def _pass_unit(place, direction, canvas) -> tuple[float, float]:
    """The direction a pass runs, as a unit vector **in brush units**.

    ``direction=`` and :attr:`Polygon.axis` are angles in the normalised ``0..1``
    space a place is written in; a brush ``size`` is a share of the long side, and
    the staircase a painter sees is in pixels. On 1024x768 the two readings of *45
    degrees* are seven degrees apart -- more than the whole window this rule lives in
    -- so both ends of every comparison below are brought into brush units first.
    :func:`_line_angle` exists for the same reason, one layer up.
    """
    degrees = place.axis if direction == "axis" else _angle_of(direction)
    theta = math.radians(degrees)
    long = float(canvas.long_side)
    dx = math.cos(theta) * canvas.width / long
    dy = math.sin(theta) * canvas.height / long
    length = math.hypot(dx, dy) or 1.0
    return dx / length, dy / length


def _stair_ledges(place, direction, size: float, density: float, canvas) -> list:
    """Per straight side of a place: how many pass ends land on it, and how far apart.

    The mechanism, rather than a window of angles fitted to it. Passes run along
    ``d``, spaced ``step`` apart along the normal ``n``, and each one ends where it
    leaves the outline. A side whose extent **across** the passes is ``across`` takes
    ``across / step`` of those ends, and they are spread over its extent **along**
    them -- so each step down it is

        rise = along / (across / step) = step x cot(theta)

    and that one line says the whole of it. At ``theta = 0`` the passes run along the
    side and none of them ends on it. At ``theta = 90`` every end lands on the same
    line and the rise goes to nothing. The fault is in between, and because ``cot``
    is steep near zero it is **nearest parallel that it is worst**: a side three
    degrees off the passes takes its handful of ends eight brush widths apart, which
    is the lit band ``CALIBRATION.md`` measures at 22% horizontal edges against 1%
    for a comb.

    Returns ``(ledges, rise_in_brush_widths, side_length)`` per side, tallest step
    first. ``direction`` is read the way :meth:`Session._block_in_paths` reads it --
    left off is horizontal, ``"cross"`` and a sequence are one pass per angle -- and
    every angle is walked, because a mass swept twice stairs on whichever of the two
    it is nearest one of its sides.
    """
    long = float(canvas.long_side)
    ux, uy = canvas.width / long, canvas.height / long
    step = _pass_step(size, density)
    out = []
    for pass_dir in _pass_directions("horizontal" if direction is None else direction):
        dx, dy = _pass_unit(place, pass_dir, canvas)
        nx, ny = -dy, dx
        for p0, p1 in _outline_sides(place):
            ex, ey = (p1[0] - p0[0]) * ux, (p1[1] - p0[1]) * uy
            across, along = abs(ex * nx + ey * ny), abs(ex * dx + ey * dy)
            ledges = across / step
            if ledges < 1.0:
                # Fewer than one whole pass end: no ledge on this side at all, and a
                # `rise` that is the arithmetic running away towards parallel -- 110
                # brush widths on a canvas one wide. Dropped before it is read off.
                continue
            out.append((ledges, (along / ledges) / size, math.hypot(ex, ey)))
    return sorted(out, key=lambda row: -row[1])


def _check_chisel_staircase(session, place, b: Brush, direction, density: float,
                            canvas, stacklevel: int = 2) -> None:
    """Warn when a chisel fills a mass along a straight side it runs *nearly* along.

    Finding 1 of the 0.5.0 cohort, and the commonest way a mass comes back wrong:
    Kimi's rock faces are ``RECIPES.md``'s *a mass built of planes* character for
    character, and a worked example is an instruction.

    **The rule is the mechanism and not a window of angles**, because the window the
    plan proposed did not survive being measured. It asked what share of the outline
    lay more than fifteen degrees from both parallel and square to the passes -- which
    measures how irregular a shape is, not how it stairs. It was **silent on the lit
    band** ``CALIBRATION.md`` measures the staircase on and silent on Kimi's rock
    face, while firing on an ellipse, a blob and a rectangle swept at 28 degrees:
    three shapes with no straight side to align to, and so nothing to offer a painter
    who reads it. :func:`_stair_ledges` has the arithmetic that replaced it; the short
    of it is that ``cot`` is steep near zero, so it is *nearest parallel* that a
    chisel steps worst, which is the half of the range that window excluded.

    Two remedies, and the measurement decides which is named how. Passes **along** the
    side are free and exact -- ``direction=`` takes the side's own two points, the form
    that exists because three painters worked the screen angle out by hand and typed a
    number that meant something else (:func:`_line_angle`) -- but only where the sides
    run **parallel**: on a tapered shape no one angle serves both, and aligning to the
    silhouette took ``RECIPES.md``'s cylinder from twenty brush widths to seven rather
    than to nothing. The comb always works, because its pass end is broken into
    bristles instead of being a line: 22% of the lit band's strong edges horizontal
    against **1%**, on the same shape at the same density.

    ``edge="hard"`` is **not** offered, and ``PAINTING.md`` claimed it closed this
    until 0.6.0. These are pass ends *inside* the mask, so masking the outline does
    not move them: 22% to **20%**. ``edge="clean"`` halves it to 11% and is not
    enough either, which is why this fires on ``"ragged"`` and would be right to fire
    on ``"clean"`` if the table in ``CALIBRATION.md`` did not say so plainly instead.

    **The comb is offered only where a comb is a brush.** Under
    ``_REPORT_SMALL_BRISTLE`` a bristle is four streaks with gaps, and the post-pass
    check says so -- so this remedy, taken at the size it fired at, traded one fault
    for another. It is how *a mass built of planes* came to paint the woven surface
    its own *Goes wrong as* names, when step 6 of the 0.6.0 round took this advice for
    faces at ``0.014``-``0.02``. Below the floor the second remedy is ``edge="clean"``
    beside ``direction=`` -- the sides the passes run along close exactly, and the
    clean edge halves the rest -- which is what that recipe lays now.
    """
    if b.tip not in _STAIR_TIPS or not isinstance(place, (Polygon, Region)):
        return
    rows = [row for row in _stair_ledges(place, direction, b.size, density, canvas)
            if row[1] >= _STAIR_RISE]
    ends = sum(row[0] for row in rows)
    if ends < _STAIR_LEDGES:
        return
    if b.size >= _REPORT_SMALL_BRISTLE:
        other = ("; or lay it with a comb ('bristle'), whose pass ends break rather "
                 "than stack.")
    else:
        other = (f", and edge='clean' for the sides it cannot follow, which halves the "
                 f"steps there. Not a comb: under size={_REPORT_SMALL_BRISTLE:g} a "
                 f"bristle is four streaks with gaps, a woven plane rather than a flat "
                 f"one.")
    session._notify(
        "chisel-staircase",
        f"a {b.name!r} filling {getattr(place, 'name', '') or 'this shape'} ends "
        f"{ends:.0f} of its passes on straight sides it runs nearly along, and steps "
        f"up to {rows[0][1]:.0f} brush widths from one end to the next: those sides "
        f"come back as a staircase rather than as the line they were drawn as. Give "
        f"direction= that side's own two points, which closes it exactly where the "
        f"sides run parallel{other}",
        stacklevel=stacklevel,
    )


#: Past this multiple of the place it was handed, a call is painting somewhere else as
#: well as where it was sent: see :func:`_spill_over`. Over the corpus's own tail rather
#: than inside it -- over 299 masses of 21 paintings a ``block_in`` covers ``1.126``
#: times its place at the median and ``1.474`` at p90, a banded ``scumble`` ``1.287``
#: and ``1.573`` -- and over every mass the guide itself recommends, none of which
#: lands over ``1.49`` (``CALIBRATION.md``, *Paint that lands outside the place*).
_SPILL_RATIO = 1.6

#: ...and past this for a banded ``scumble``, whose own brush breaks past the band by
#: design. The brush is three of the band's steps, and on a canvas that is not square
#: the step is taken in the canvas's height while the brush is sized against its long
#: side, so an ordinary band laid along its own axis covers up to about 1.7x itself --
#: the band the verb's brush was tuned on, ``0.80 x 0.40`` at ``n=8``, covers 1.69x at
#: 320x240, and would have been told it spilled at 1.6. B17's band crossed at 30
#: degrees covers 2.95x. Mapped over seven canvases, seven places and six pass counts,
#: ``2.0`` is silent on three in four bands laid along their own axis (median 1.63x) --
#: the rest are squares given four to six passes, whose own brush is two-thirds of the
#: place or more -- and says it on 85% of the same bands crossed at 30 to 60 degrees.
_SPILL_RATIO_BAND = 2.0

#: Under this many pixels a brush does not land where its outline says it will: a comb
#: that narrow is a few streaks with gaps, and a chisel lays next to nothing
#: (``chisel-blank``). On the bench the reach below was fitted on, a 7 px ``flat``
#: predicted at 1.68x came back at 0.65x and a 10 px comb predicted at 1.65x came back
#: at 0.47x -- so a spill is not the question there, and the rule stays out of it.
_SPILL_MIN_PX = 12.0

#: How far each tip's paint reaches past the line its pass runs along, in half-brush
#: widths: across the pass, and past each of its two ends. Fitted on 126 masses and
#: bands laid for the purpose on three canvases and measured the way the corpus replay
#: measures a call -- a pixel whose value moved by more than ``0.004`` is painted --
#: against the passes the call actually laid. A chisel ends square; a disc ends round,
#: and narrows under the default taper; a comb that runs dry reaches least.
_SPILL_REACH = {
    "flat": (1.00, 0.2),
    "knife": (1.00, 0.2),
    "bristle": (0.90, 0.4),
    "round_hard": (0.80, 0.8),
    "round_soft": (0.80, 0.8),
}

#: ...and a comb laid solid, as a banded ``scumble`` has been since 0.6.0, which reaches
#: the whole of its width because nothing along a pass runs dry.
_SPILL_REACH_SOLID_COMB = (1.05, 0.2)


def _spill_reach(b: Brush) -> tuple[float, float]:
    """How far ``b``'s paint reaches past its pass line: across it, and past its ends."""
    if b.tip == "bristle" and b.load >= 1.0 and b.load_falloff <= 0.0:
        return _SPILL_REACH_SOLID_COMB
    return _SPILL_REACH.get(b.tip, (1.0, 0.5))


def _spill(place, paths, b: Brush, canvas, holds=()) -> tuple[float, float]:
    """What a call's passes will cover, against the place it was handed.

    Returns ``(covered / place, share of what is covered that lies outside it)``,
    predicted off the passes themselves rather than measured off the paint: every pass
    is a strip ``_spill_reach(b)`` half-brushes either side of its line and past its
    ends -- square ends for a chisel or a comb, round ones for a disc -- laid on a grid
    of whole pixels over the window the call can reach, clipped to the canvas and to
    every outline the call is held inside. The grid is coarsened until the window is at
    most 256 cells across, which keeps a full-canvas mass to a few milliseconds and a
    small one at full resolution, where one pixel of rounding is a share of the answer.

    Measured on the bench the reach was fitted on, against the paint: off by **1.8%**
    on average for a chisel, **1.7%** for a banded scumble, **4.2%** for a round tip
    and **4.7%** for a comb that runs dry.
    """
    w, h = int(canvas.width), int(canvas.height)
    across, end = _spill_reach(b)
    width = b.size * float(canvas.long_side)
    r, e = across * width * 0.5, end * width * 0.5
    round_tip = b.tip.startswith("round")
    lines = [np.asarray(p, dtype=np.float64).reshape(-1, 2) * (w, h) for p in paths]
    lines = [p for p in lines if len(p) >= 2]
    x0, y0, x1, y1 = place.bounds
    reach = r + e
    if lines:
        every = np.concatenate(lines)
        lo_x, hi_x = float(every[:, 0].min()) - reach, float(every[:, 0].max()) + reach
        lo_y, hi_y = float(every[:, 1].min()) - reach, float(every[:, 1].max()) + reach
    else:
        lo_x, hi_x, lo_y, hi_y = x0 * w, x1 * w, y0 * h, y1 * h
    lo_x, hi_x = max(0.0, min(lo_x, x0 * w)), min(float(w), max(hi_x, x1 * w))
    lo_y, hi_y = max(0.0, min(lo_y, y0 * h)), min(float(h), max(hi_y, y1 * h))
    if hi_x - lo_x < 1.0 or hi_y - lo_y < 1.0:
        return 0.0, 0.0
    cell = max(1.0, math.ceil(max(hi_x - lo_x, hi_y - lo_y) / 256.0))
    nx = max(1, math.ceil((hi_x - lo_x) / cell))
    ny = max(1, math.ceil((hi_y - lo_y) / cell))
    xs = lo_x + (np.arange(nx, dtype=np.float64) + 0.5) * cell
    ys = lo_y + (np.arange(ny, dtype=np.float64) + 0.5) * cell
    covered = np.zeros((ny, nx), dtype=bool)
    for line in lines:
        last = len(line) - 2
        for i in range(len(line) - 1):
            (ax, ay), (bx, by) = line[i], line[i + 1]
            length = math.hypot(bx - ax, by - ay)
            if length < 1e-9:
                continue
            dx, dy = (bx - ax) / length, (by - ay) / length
            c0 = max(0, int((min(ax, bx) - reach - lo_x) / cell))
            c1 = min(nx, int((max(ax, bx) + reach - lo_x) / cell) + 2)
            r0 = max(0, int((min(ay, by) - reach - lo_y) / cell))
            r1 = min(ny, int((max(ay, by) + reach - lo_y) / cell) + 2)
            if c1 <= c0 or r1 <= r0:
                continue
            sx = xs[None, c0:c1] - ax
            sy = ys[r0:r1, None] - ay
            t = sx * dx + sy * dy
            off = np.abs(sy * dx - sx * dy)
            if round_tip:
                strip = (t >= 0.0) & (t <= length) & (off <= r)
                if i == 0:
                    strip |= sx * sx + sy * sy <= e * e
                if i == last:
                    strip |= (sx - (bx - ax)) ** 2 + (sy - (by - ay)) ** 2 <= e * e
            else:
                start = -e if i == 0 else 0.0
                stop = length + (e if i == last else 0.0)
                strip = (t >= start) & (t <= stop) & (off <= r)
            covered[r0:r1, c0:c1] |= strip
    gx, gy = xs[None, :] / w, ys[:, None] / h
    if isinstance(place, Polygon):
        mine = place.inside(gx, gy)
    else:
        mine = (gx >= x0) & (gx <= x1) & (gy >= y0) & (gy <= y1)
    for hold in holds or ():
        covered &= hold.inside(gx, gy)
    asked, laid = int(mine.sum()), int(covered.sum())
    if not asked or not laid:
        return 0.0, 0.0
    return laid / asked, float((covered & ~mine).sum()) / laid


def _spill_over(session, place, b: Brush, over: float, walk, holds=(),
                line: float = _SPILL_RATIO):
    """``(ratio, outside)`` when a call will cover ``line`` times its place or more.

    ``None`` otherwise -- and ``None`` without walking a single pass wherever the
    arithmetic already says it cannot get there: a brush under :data:`_SPILL_MIN_PX`,
    or a place whose box, grown by the furthest any pass of this brush can reach, is
    itself under the ratio. That bound is generous, so an ordinary mass often gets past
    it; what it saves is the walk on the small brushes and the big places.

    ``over`` is the call's overhang in brush widths, ``walk`` a function of a trial
    session that yields the call's pass lines -- walked there because the wander is
    drawn from the stream, and the stream is the real painting's.
    """
    canvas = session.canvas
    if b.size * float(canvas.long_side) < _SPILL_MIN_PX:
        return None
    long = float(canvas.long_side)
    ux, uy = canvas.width / long, canvas.height / long
    # The furthest a pass can reach past the place: the overhang past its ends, the
    # tip's own reach past its line (a little over half a brush at most), and the
    # sideways wander, whose three sigma is about half a brush more.
    grow = b.size * (max(float(over or 0.0), 0.0) + 1.0)
    x0, y0, x1, y1 = place.bounds
    box = ((min(1.0, x1 + grow / ux) - max(0.0, x0 - grow / ux))
           * (min(1.0, y1 + grow / uy) - max(0.0, y0 - grow / uy)))
    area = place.area if isinstance(place, Polygon) else (x1 - x0) * (y1 - y0)
    if area <= 0.0 or box / area < line:
        return None
    paths = list(walk(session._trial_session()))
    ratio, outside = _spill(place, paths, b, canvas, holds)
    return (ratio, outside) if ratio >= line else None


def _shorter_side(place, canvas) -> float:
    """A place's shorter extent, as a share of the canvas's long side -- a brush's unit."""
    long = float(canvas.long_side)
    x0, y0, x1, y1 = place.bounds
    return min((x1 - x0) * canvas.width / long, (y1 - y0) * canvas.height / long)


def _check_mass_spill(session, place, fill, b: Brush, direction, density: float,
                      overhang, holds, stacklevel: int = 2) -> None:
    """Warn when a ragged ``block_in`` will lay paint well outside the place it was given.

    Finding 8 of the 0.5.0 cohort and the most expensive first mistake with shapes on
    record: a pass stops where its *centre* meets the outline and the brush hangs half
    its width past it, so a brush that is a large part of the mass lays the mass and a
    rim of the same paint round it, over whatever its neighbours are. The guide's
    three answers -- inset the place by half the brush, a brush under a fifth of it,
    ``edge="clean"`` -- have been in ``PAINTING.md`` since shapes existed; this says
    the number at the call, where one painting lost 72 strokes and its only ``undo``.

    **Measured on the passes, not read off a rule of thumb.** The plan's version was
    *a brush over a fifth of the shorter extent*, and the guide's own first
    ``block_in`` lays a brush 60% of its shape and lands 1.48x of it -- silent here,
    because the multiple is what paints the neighbours and not the fraction.

    Not said inside :meth:`Session.cover`, whose ends run outside the area on purpose:
    its own docstring's canonical call paints about three times its cell, and a rule
    that fires on the canonical call is a rule painters learn to ignore.
    """
    shaped = isinstance(place, Polygon)
    over = (0.0 if shaped else 0.35) if overhang is None else float(overhang)
    found = _spill_over(
        session, place, b, over,
        lambda trial: (path for _, path, _ in trial._block_in_paths(fill, b, direction,
                                                                     density, overhang)),
        holds,
    )
    if found is None:
        return
    ratio, outside = found
    short = _shorter_side(place, session.canvas)
    session._notify(
        "spill",
        f"block_in on {getattr(place, 'name', '') or ('this shape' if shaped else 'this region')} "
        f"lays about {ratio:.1f}x the place it was handed, {outside:.0%} of the paint "
        f"outside it: a {b.name!r} at size={b.size:.3g} is {b.size / max(short, 1e-9):.0%} "
        f"of the place's shorter side ({short:.3f}), and a brush hangs half its width past "
        f"every pass it lays. Inset the place by half the brush "
        f"(place.inset({b.size * 0.5:.3g})), or take a brush under a fifth of it "
        f"(size={short / 5:.3g}); edge=\"hard\" holds the paint to the outline, its "
        f"edge broken by the tooth rather than cut.",
        stacklevel=stacklevel,
    )


def _check_band_spill(session, place, b: Brush, degrees: float, step: float, n: int,
                      overhang: float, picked: bool, axis: bool, holds,
                      stacklevel: int = 2) -> None:
    """Warn when a banded ``scumble`` will lay paint well outside its band (B17).

    The brush is picked from the step between passes, and the step from the band's
    extent *across the passes* -- which, crossed at an angle, is most of the band's
    length rather than its depth. So the brush grows with the angle and lands over
    whatever is either side of the band: a band ``0.20`` deep at ``n=8`` covers
    **1.49x** itself laid along its own axis, **2.95x** at 30 degrees and **3.57x** at
    60, where 72% of the paint is outside it. Nothing warned about the middle of that.

    **Not capped**, which the round measured: capping the brush at the band's own depth
    still leaves 2.22x and 2.04x, and capping it at half the depth brings the bars
    back -- 3.2% and 15.8% of the band bare between passes. The angle is the painter's
    and the gradient runs along it, so the remedy that keeps both is the hold:
    ``edge="hard"`` lays the same passes and masks every dab to the band.
    """
    shaped = isinstance(place, Polygon)
    found = _spill_over(
        session, place, b, overhang,
        lambda trial: (path for path, _ in (
            trial._shape_paths(place, degrees, step, b.size * overhang) if shaped
            else trial._angled_paths(place, degrees, step, b.size * overhang))),
        holds, line=_SPILL_RATIO_BAND,
    )
    if found is None:
        return
    ratio, outside = found
    short = _shorter_side(place, session.canvas)
    turn = "" if axis else " direction=\"axis\" runs them along it instead."
    session._notify(
        "spill",
        f"scumble on {getattr(place, 'name', '') or 'this band'} lays about {ratio:.1f}x "
        f"the band, {outside:.0%} of the paint outside it: its {n} passes step "
        f"{step:.3f} apart across it at {degrees:.0f} degrees, so the brush "
        f"{'picked from that step is' if picked else 'is'} {b.size:.3g} -- "
        f"{b.size / max(short, 1e-9):.1f}x the band's own depth ({short:.3f}). "
        f"edge=\"hard\" lays the same passes held to the band, its edge broken by the "
        f"tooth rather than cut.{turn}",
        stacklevel=stacklevel,
    )


#: Past this share of a shape's shorter extent, a clean edge's half-brush inset is
#: taking the mass rather than a rim off it: see :func:`_check_clean_size`.
_CLEAN_SHARE = 0.25


#: The tips whose silhouette is a disc, so their overhang goes out in **every**
#: direction rather than across the pass.
_ROUND_TIPS = ("round_soft", "round_hard")

#: Narrower than this, a shape is a *feature* rather than a mass, and a disc's fringe
#: lands on a drawing rather than on a soft edge nobody minds. ``CALIBRATION.md``'s own
#: scale ladder under *At the scale of a feature* puts a mass at about ``0.3`` of the
#: canvas across and a plane within it at ``0.015-0.025``; the leaf that raised this is
#: ``0.046``. Without it the rule fires on a mass a third of the canvas wide laid with
#: a round tip, which is the guide's own advice for a soft silhouette -- and tells the
#: painter to lay it as a pair of strokes, which at that size is nonsense.
_ROUND_FEATURE = 0.1


def _check_round_block(session, place, b: Brush, canvas, stacklevel: int = 3) -> None:
    """Warn when a round tip is blocking in a shape too small to hold it.

    A chisel's overhang is across its pass; a disc's is all the way round, laid at
    small sizes as separate discs -- a fringe rather than a soft edge. On a small
    shape that fringe *is* the silhouette, and a painter's pressed leaf, a ``hull``
    ``0.055`` across at its narrowest blocked in with a ``round_hard`` at
    ``size=0.013``, came back in their own word a cauliflower. It was relaid as two
    tapering strokes that meet plus a midrib.

    The number that predicts it is the same one :func:`_check_clean_size` uses -- the
    brush's share of the shape's shorter extent, in the brush's own unit -- and it
    fires at the same quarter, so this rule adds no new threshold. Measured on that
    leaf as it was actually painted (``0.046`` across at its narrowest, 1200x800),
    painted area as a multiple of the shape's own:

    ========  ==============  ========
    share     ``round_hard``  ``flat``
    ========  ==============  ========
    ``0.11``  ``1.19``        ``1.07``
    ``0.20``  ``1.38``        ``1.23``
    ``0.25``  ``1.53``        ``1.32``
    ``0.28``  ``1.61``        ``1.34``
    ``0.50``  ``2.17``        ``1.68``
    ========  ==============  ========

    The painter's own call is the ``0.28`` row: half again as much canvas as the
    shape, all of it landing on the boundary that *is* the drawing. A chisel at the
    same share lands a third more, which is why the remedy names one. There is no
    knee -- the extra area is about ``2x`` the share, because a disc's fringe is its
    perimeter times half its width -- so the quarter is where the clean-edge rule
    already draws its line and not a second judgement.

    Only on a shape narrower than :data:`_ROUND_FEATURE`, and only on a ragged edge.
    Over that width the same share is a mass with a soft silhouette, which is what the
    guide recommends a round tip for; under it the fringe *is* the drawing.
    ``edge="clean"`` is left to :func:`_check_clean_size`, which fires at the same
    share and says a different thing about the same combination, and ``edge="hard"``
    masks the fringe away, which is one of the remedies this names.
    """
    if b.tip not in _ROUND_TIPS:
        return
    long = float(canvas.long_side)
    short = min(place.width * canvas.width / long, place.height * canvas.height / long)
    if not 0.0 < short < _ROUND_FEATURE:
        return
    share = b.size / short
    if share <= _CLEAN_SHARE:
        return
    session._notify(
        "round-fringe",
        f"block_in({place.name or 'a shape'}) with a round tip ({b.name!r}) at "
        f"size={b.size:.3g}, on a feature {short:.3f} across at its narrowest: the "
        f"brush is {share:.0%} of that. A round tip's overhang goes out all the way "
        f"round, so at this share the mass lands about half again the area of the "
        f"shape and the fringe is the silhouette. Use a chisel ('flat', 'knife') at "
        f"this size, size={_CLEAN_SHARE * short:.3g} and under, edge='hard' to hold "
        f"the paint inside the outline, its edge broken by the tooth rather than a "
        f"fringe of discs, or lay the shape as a pair of strokes that meet.",
        stacklevel=stacklevel,
    )


def _check_clean_size(session, place, b: Brush, canvas, stacklevel: int = 2,
                      verb: str = "block_in") -> None:
    """Warn when a clean edge's brush is a large share of the place's shorter extent.

    ``edge="clean"`` insets the fill by half the brush all the way round, which is a
    rim on a large mass and most of a small one; the contour pass then puts the outer
    half of the brush back on the line, so the *paint* still covers the shape -- but
    it covers it as one chisel pass with the corners the tip leaves, not as the
    shape that was drawn. A painter's lantern cap ``0.036`` deep at ``size=0.016``
    came back a rounded mushroom. The number that predicts it is the brush's share
    of the shape's shorter extent, in the brush's own unit (the canvas long side).

    **A region is asked the same** (0.6.0). This was a shape's check only, and
    :meth:`Session.cover` is usually handed a region: a place 108x60 px on a 900x600
    canvas, buried ``edge="clean"`` with the default ``flat`` at ``size=0.1``, is
    inset to a sliver, gets two stubs laid in its middle, and leaves ``15%`` of the
    mistake it was burying showing on a worked passage -- and nothing was said
    (``CALIBRATION.md``, *A burial and the place it was handed*). ``verb`` is the call
    the painter made, so a burial is told about ``cover`` and not about the
    ``block_in`` it lays.
    """
    long = float(canvas.long_side)
    short = min(place.width * canvas.width / long, place.height * canvas.height / long)
    if short <= 0.0:
        return
    share = b.size / short
    if share <= _CLEAN_SHARE:
        return
    kept = _place_area(place.inset(b.size * 0.5)) / max(_place_area(place), 1e-12)
    shaped = isinstance(place, Polygon)
    other = ("leave edge= off: the default holds the burial to its place and breaks "
             "its border against the tooth"
             if verb == "cover" else "leave the edge ragged")
    session._notify(
        "clean-small",
        f"{verb}(edge='clean') at size={b.size:.3g} on "
        f"{place.name or ('a shape' if shaped else 'a region')} "
        f"{short:.3f} across at its narrowest: the brush is {share:.0%} of that, so "
        f"the half-brush inset keeps {kept:.0%} of the {'shape' if shaped else 'region'} "
        f"to fill and the contour pass lays the rest as one chisel stroke, corners "
        f"rounded off. Use a brush under a quarter of the shorter extent -- "
        f"size={_CLEAN_SHARE * short:.3g} here -- or {other}.",
        stacklevel=stacklevel,
    )


def _place_area(place) -> float:
    """Share of the canvas a shape or a region covers, 0..1."""
    if isinstance(place, Polygon):
        return place.area
    return place.width * place.height


def _check_brush_overrides(overrides: dict) -> None:
    """Reject a keyword that is not a brush field, naming the call that does take it.

    Every painting call ends its signature with ``**brush_overrides`` and hands them
    to :meth:`~easel.brush.Brush.with_`, which is what makes *any brush field is also
    an override on any painting call* true. The cost is that a keyword belonging to a
    *different* call lands there too, and ``dataclasses.replace`` reports it as
    ``Brush.__init__() got an unexpected keyword argument``: a class the painter never
    mentioned, and no hint that ``solid`` is real and lives one call over.
    """
    if not overrides:
        return
    fields = {f.name for f in dataclass_fields(Brush)}
    for key in overrides:
        if key in fields:
            continue
        known = _NOT_BRUSH_FIELDS.get(key)
        if known is None:
            near = get_close_matches(key, sorted(fields), n=1)
            known = (f"{key}= is not a brush field."
                     + (f" Did you mean {near[0]}=?" if near else ""))
        raise TypeError(
            f"{known}\nThe brush fields an override may set are: "
            f"{', '.join(sorted(fields - {'meta'}))}."
        )


#: Named pressure profiles that are their own mirror image, and so mean the same
#: thing whichever end of a pass is laid first. Listed rather than derived so that
#: a pass laid at ``taper`` -- the default, and the great majority of every painting
#: ever made here -- goes through :func:`_canvas_order_pressure` untouched and lands
#: byte-for-byte where it always did.
_SYMMETRIC_PRESSURES = ("taper", "even", "swell")

#: The asymmetric profiles that mirror onto each other exactly.
_MIRRORED_PRESSURES = {"press_in": "lift_off", "lift_off": "press_in"}


def _canvas_order_pressure(pressure):
    """The same pressure profile, for a pass that is laid the other way round.

    Consecutive passes of a mass run in opposite directions -- the way a hand comes
    back across the canvas, and the reason a stack of passes does not stack all its
    run-out along one edge. A pressure profile, though, is applied along the path's
    own order, so on every second pass an asymmetric one arrives mirrored: measured
    on four horizontal passes at ``pressure=[0.0, 1.0]``, the paint at the two ends
    came back ``0.35 / 0.56``, ``0.52 / 0.33``, ``0.35 / 0.57``, ``0.56 / 0.34``.
    A passage meant to brighten toward one side could not be laid with the verb at
    all; it had to be hand-written as six separate strokes.

    So the profile is reversed for the passes that are, which leaves the *paint*
    alternating -- which is what it is for -- and the *pressure* reading the same
    way across the canvas on every pass.

    Symmetric profiles and scalars are returned unchanged rather than reversed into
    an equal-but-differently-computed array, so that nothing already painted moves.
    """
    if isinstance(pressure, str):
        name = pressure.lower()
        if name in _SYMMETRIC_PRESSURES:
            return pressure
        if name in _MIRRORED_PRESSURES:
            return _MIRRORED_PRESSURES[name]
        # `dab` is the one asymmetric profile with no named mirror; an unknown name
        # raises here with pressure_curve's own complaint, as it would anyway.
        return pressure_curve(pressure, 64)[::-1]
    arr = np.atleast_1d(np.asarray(pressure, dtype=np.float32))
    return pressure if arr.size < 2 else arr[::-1]


def _inward_depth(place, brush_size: float = 0.0) -> float:
    """How far a centred scumble steps in: half the patch's shorter extent.

    The radius of a round patch and the half-width of a long one, which is where
    the ramp lands on its spine. Floored at half a brush so a patch smaller than
    the brush still gets a step to walk.

    One place, so the ring step a brush size is *derived* from and the ring step
    the rings are actually laid on cannot drift apart.
    """
    return max(0.5 * min(place.width, place.height), brush_size * 0.5)


#: How many ring steps wide a centred scumble's brush should be. Below about two
#: the rings stop overlapping and the ramp comes back as stripes; above about four
#: the last rings bury the first and the middle goes flat. Measured on an ellipse
#: 0.72x0.24 at ``n=7``, opacity 0.5, bristle -- the share of the patch sitting
#: within 0.06 of the centre value: 44% at five steps wide, 12% at three, 0.2% at
#: under two. Three is the usable middle, and the one this picks.
_INWARD_STEPS = 3.0


def _inward_size(place, n: int) -> float:
    """The brush a centred scumble wants: about three of its own ring steps.

    ``scumble(direction="inward")`` steps its rings ``depth / n`` apart and lays
    each over the ones before it, so the brush and the step are one mechanism and
    not two settings. Left to the preset's default the bristle is ``0.11`` -- five
    steps wide on the patch above, wide enough that the last rings bury the first
    and nearly half the patch comes back one flat colour with a rim of ramp round
    it. That is the solid sun a painter rehearses three times and then abandons the
    verb for.

    So with no ``size=`` the verb sizes its own brush. An explicit ``size=``, or a
    :class:`~easel.brush.Brush` carrying one, is a painter's choice and is left
    alone -- :func:`_check_inward_brush` says so when it is wide enough to fill.
    """
    step = _inward_depth(place) / max(n, 1)
    # The Brush constructor takes (0, 1]; a large `n` on a small patch would
    # otherwise derive its way to zero and raise from somewhere unhelpful.
    return float(min(max(_INWARD_STEPS * step, 0.01), 1.0))


#: Fewer rings than this and a centred scumble reads as steps rather than a
#: fall-off, whatever the brush is: the verb's own docstring is *below about five
#: the steps start to read*, and the guide's recipe uses eight. It is the other
#: wall of the window :func:`_check_inward_comb` measures -- ``n`` has to be small
#: enough that the brush is still a brush, and large enough to be a ramp.
_INWARD_MIN_RINGS = 5


def _check_inward_comb(session, place, b: Brush, n: int, named: bool) -> None:
    """Warn when a centred scumble's brush is too *narrow* to be a brush.

    :func:`_check_inward_brush` is the other side of this one wall, and until now
    the verb warned from that side only: a brush wide enough to fill the patch flat
    said so, and a brush too narrow to lay anything said nothing. But the brush is
    ``3 x depth / n`` and the painter sets ``n``, so **more rings on a shallow patch
    buy a narrower brush rather than finer banding** -- and past the point where
    that brush is under the post-pass check's comb floor it is four streaks with
    gaps. The arithmetic is exact: the derived brush clears ``0.025`` only while
    ``n <= 120 x depth``, so a patch ``0.0667`` deep carries the recipe's eight
    rings and nothing shallower does.

    A painter met this at ``n=12`` on a patch ``0.075`` deep, read the bristle
    warning the post-pass check gave as an unrelated complaint, and spent two more
    rehearsals. Both halves of the window are now said at the call, in the shape
    the other scumble warnings have: the verb lays what it was asked for and says
    what it will look like.

    Where no ``n`` fits at all -- a patch so shallow that even the fewest rings that
    still read as a fall-off leave a comb under the floor -- there is nothing to
    tune, and the warning names the recipe that lays a glow that shallow instead.
    """
    # The floor is a two-figure number, and a brush that *rounds* to it is not
    # under it: a polygon of an ellipse comes a hair short of its own extents, so
    # the `n` that sits exactly on the boundary derives 0.024998 rather than
    # 0.025, and a warning reading "0.025, under the 0.025" is noise.
    floor = _REPORT_SMALL_BRISTLE - 0.0005
    if b.tip != "bristle" or b.size >= floor:
        return
    depth = _inward_depth(place)
    fits = int(_INWARD_STEPS * depth / floor)
    if named:
        remedy = (f"Leave size= off and the verb picks {_inward_size(place, n):.3g} "
                  f"from the ring step.")
    elif fits >= _INWARD_MIN_RINGS:
        remedy = (f"The brush is 3 x depth / n, so more rings on a patch this "
                  f"shallow buy a narrower brush and not finer banding: this one "
                  f"carries {fits} rings before the comb goes under the floor. Drop "
                  f"to n={fits}.")
    else:
        remedy = (f"No n fits: this patch is {depth:.3g} deep, and at the fewest "
                  f"rings that still read as a fall-off ({_INWARD_MIN_RINGS}) the "
                  f"brush is {_INWARD_STEPS * depth / _INWARD_MIN_RINGS:.3g}, still "
                  f"under the floor. A glow this shallow is not a bloom on a "
                  f"surface -- lay it as a volume of lit air, three glazes along "
                  f"the axis of the light (RECIPES.md).")
    session._notify(
        "inward-comb",
        f"scumble(direction='inward', n={n}) on a patch {depth:.3g} deep lays its "
        f"rings with a bristle {b.size:.3g} wide, under the {_REPORT_SMALL_BRISTLE} "
        f"where a comb is four streaks with gaps rather than a brush. {remedy}",
        stacklevel=3,
    )


def _check_inward_brush(session, place, b: Brush, n: int) -> None:
    """Warn when a centred scumble's brush is wide enough to fill the patch flat.

    The same shape of warning ``cost()`` gives for a plan that would eat the
    budget: the verb still does what it was asked, and says what it will look
    like. Silence here cost one painter three rehearsals and the verb.
    """
    step = _inward_depth(place, b.size) / max(n, 1)
    widest = _INWARD_STEPS * step
    if b.size <= widest * 1.05:
        return
    session._notify(
        "inward-flat",
        f"scumble(direction='inward') with a brush {b.size:.3g} wide on a patch "
        f"whose rings step {step:.3g} apart: {b.size / step:.1f} steps. The last "
        f"rings bury the first, so the middle comes back one flat colour with a "
        f"rim of ramp round it rather than a fall-off. Keep the brush under about "
        f"three ring steps -- size={widest:.3g} here -- or leave size= off and it "
        f"is picked for you.",
        stacklevel=3,
    )


#: How many pass steps wide a banded scumble's brush should be. The passes step
#: ``extent / n`` apart and overlap, and the overlap is what closes the joins
#: stepping alone would leave. Measured on a band ``0.80x0.40`` at ``n=8`` (a step of
#: ``0.050``), bristle, opacity ``0.5``, 640x384 linen, ground ``0.53`` -- the sd of
#: the across-band profile's own one-step ripple, and the value span the ramp
#: actually delivered against the ``0.20``-to-``0.70`` it was asked for:
#:
#: | brush | ripple | delivered |
#: |---|---|---|
#: | 0.5 steps | 0.004 | 0.50..0.54 -- the ground, barely painted |
#: | 1 step | 0.014 | 0.31..0.59 |
#: | 1.5 steps | 0.015 | 0.27..0.63 |
#: | 2 steps | 0.008 | 0.25..0.62 |
#: | 3 steps | 0.007 | 0.26..0.63 |
#: | 4 steps | 0.005 | 0.28..0.64 |
#: | 6 steps | 0.006 | 0.36..0.63 -- the last passes burying the first |
#:
#: So the ripple is worst at one to one and a half steps, which is where a preset's
#: default usually lands, and the ramp starts collapsing past about five. Three is
#: the middle of the window, and the same figure the inward case picks.
_LINEAR_STEPS = 3.0

#: Below this many steps the passes stop overlapping and the passage comes back as
#: stripes with the ground showing between them.
_LINEAR_MIN_STEPS = 2.0


def _linear_size(step: float) -> float:
    """The brush a banded scumble wants: about three of its own pass steps."""
    return float(min(max(_LINEAR_STEPS * step, 0.01), 1.0))


def _check_linear_brush(session, b: Brush, step: float, n: int) -> None:
    """Warn when a banded scumble's brush is too narrow to close its own joins.

    The inward case has warned about a brush wider than its rings since the third
    session; this is the same failure at the other end of the same curve, on the
    other direction of the same verb. A painter who hands it a brush narrower than
    the step gets the thing the verb exists to prevent -- a wide quiet passage laid
    as a stack of bars -- and got it silently.
    """
    steps = b.size / max(step, 1e-9)
    if steps >= _LINEAR_MIN_STEPS:
        return
    session._notify(
        "scumble-bars",
        f"scumble() with a brush {b.size:.3g} wide on a band whose {n} passes step "
        f"{step:.3g} apart: {steps:.1f} steps. The passes do not overlap, so the "
        f"passage comes back as bars with the ground showing between them. Use about "
        f"three steps -- size={_LINEAR_STEPS * step:.3g} here -- or leave size= off "
        f"and it is picked for you.",
        stacklevel=3,
    )


def _pass_lengths(place, degrees: float, n: int) -> tuple[float, float, float]:
    """How long the first, the middle and the last of ``n`` passes across a place are.

    The passes of a banded scumble step across the place along the normal of
    ``degrees`` and run along it; each one is cut to the outline, so on a wedge the
    first pass and the last are very different lengths. Measured the way
    :meth:`Session._shape_paths` lays them, at the two end offsets -- and at the
    middle one, because a **rectangle** is not a wedge and its ends say nothing: a
    band crossed at an angle has short passes at both corners and its longest pass
    through the centre, which is the one that answers *is this band narrower than the
    brush*.
    """
    pts = np.asarray(place.points, dtype=np.float64)
    cx, cy = place.box.center
    theta = math.radians(float(degrees))
    dx, dy = math.cos(theta), math.sin(theta)
    nx, ny = -dy, dx
    offs = (pts[:, 0] - cx) * nx + (pts[:, 1] - cy) * ny
    lo_n, hi_n = float(offs.min()), float(offs.max())

    def length_at(off: float) -> float:
        origin = (cx + nx * off, cy + ny * off)
        return sum(t1 - t0 for t0, t1 in _spans_inside(place, origin, (dx, dy)))

    half = 0.5 * (hi_n - lo_n) / max(n, 1)
    return (length_at(lo_n + half), length_at(0.5 * (lo_n + hi_n)),
            length_at(hi_n - half))


#: A shape whose pass length at one end is this many times the other's is a wedge,
#: and one brush cannot serve both ends of it.
_WEDGE_RATIO = 2.0


def _check_scumble_ends(session, place, degrees: float, b: Brush, n: int,
                        stacklevel: int = 2) -> bool:
    """Warn when a banded scumble's brush is wider than its passes at one end.

    The brush is picked from the *step* between passes (three of them), which closes
    the joins on a band whose passes are all about one length. A shape whose width
    varies along the stepping axis has passes of very different lengths, and a
    brush right for the wide end is wider than the pass is long at the narrow one:
    the passes there are dabs, and the paint blooms past the outline. One painter's
    wedge, ``0.045`` across at the mouth and ``0.42`` at the far edge, bloomed at
    the mouth and read as barely there at the wide end, and was abandoned for a
    hand-built version in five pieces each sized to its own width.

    Returns whether it said anything, because :func:`_check_spill` measures the same
    bloom as a multiple of the band and one call should hear about it once.
    """
    shape = place if isinstance(place, Polygon) else polygon(as_region(place))
    first, middle, last = _pass_lengths(shape, degrees, n)
    narrow, wide = min(first, last), max(first, last)
    if not isinstance(place, Polygon):
        # A band is not a wedge: its passes are all one length along its own axes,
        # and vary only at the two corners when they cross it at an angle. So the
        # question its ends answer is not *which end is the brush wrong for* -- it is
        # whether the **whole band** is narrower than the brush laying it, which is
        # the case the shape branch below calls dabs. A band crossed at an angle
        # paints well outside itself for a different reason, measured on the brush
        # rather than on the passes.
        if middle <= 0.0 or b.size <= middle:
            return False
        session._notify(
            "scumble-dabs",
            f"scumble on {place.name or 'this band'}: every pass is shorter "
            f"({middle:.3f} at its longest) than the brush laying it ({b.size:.3g}), "
            f"so the passes are dabs and the paint blooms past the band. The passes "
            f"run the short way across this place -- turn direction=, or lay a band "
            f"this narrow as a stroke.",
            stacklevel=stacklevel,
        )
        return True
    if narrow <= 0.0 or b.size <= narrow:
        return False
    if wide >= _WEDGE_RATIO * narrow:
        session._notify(
            "scumble-wedge",
            f"scumble on {place.name or 'this shape'}: its width varies "
            f"{wide / narrow:.0f}x along the direction the passes step -- the passes "
            f"run {narrow:.3f} long at one end and {wide:.3f} at the other, and the "
            f"brush is {b.size:.3g} wide. Picked for one end it is wrong for the "
            f"other: at the narrow end the passes are dabs wider than the shape, "
            f"and the paint blooms past it. Lay it as two or three bands each sized "
            f"to its own width, or hand it size= for the end that matters.",
            stacklevel=stacklevel,
        )
    else:
        session._notify(
            "scumble-dabs",
            f"scumble on {place.name or 'this shape'}: every pass is shorter "
            f"({narrow:.3f}) than the brush laying it ({b.size:.3g}), so the passes "
            f"are dabs and the paint blooms past the outline. The passes run the "
            f"short way across this place -- turn direction=, or lay a mass this "
            f"narrow as a stroke.",
            stacklevel=stacklevel,
        )
    return True


def _normal_extent(place, degrees: float) -> float:
    """How far a place reaches across a sweep at ``degrees``, along that sweep's normal.

    The span :meth:`Session._shape_paths` and :meth:`Session._angled_paths` divide by
    the pass step to decide how many passes a mass takes. :meth:`Session.scumble`
    needs the arithmetic the other way round -- it is told how many passes to lay and
    has to work out the step that gives exactly that many -- so the extent is lifted
    out here rather than being measured twice in two slightly different ways.
    """
    if isinstance(place, Polygon):
        pts = np.asarray(place.points, dtype=np.float64)
        cx, cy = place.box.center
        corners = [(float(x), float(y)) for x, y in pts]
    else:
        r = as_region(place)
        cx, cy = (r.x0 + r.x1) * 0.5, (r.y0 + r.y1) * 0.5
        corners = [(r.x0, r.y0), (r.x0, r.y1), (r.x1, r.y0), (r.x1, r.y1)]
    theta = math.radians(float(degrees))
    nx, ny = -math.sin(theta), math.cos(theta)
    offs = [(x - cx) * nx + (y - cy) * ny for x, y in corners]
    return max(max(offs) - min(offs), 1e-6)


def _mass_reason(fill, b: Brush, direction, density: float, laid: int) -> str:
    """Why a mass costs what it costs, off the geometry the price was counted from.

    One cause wearing three hats, and a painter who is told which hat can fix the
    call instead of redesigning the mass. The passes step across the place's extent
    *along each pass normal* -- which is the bounding box, so a long curved shape pays
    for the box its curve sweeps out -- once per direction, and each pass line comes
    back as however many pieces of it are really inside a concave shape.
    """
    dirs = _pass_directions("horizontal" if direction is None else direction)
    band = _pass_step(b.size, density)
    extents = [_normal_extent(fill, fill.axis if d == "axis" else _angle_of(d))
               for d in dirs]
    lines = sum(max(1, int(round(e / band))) for e in extents)
    parts = []
    if len(dirs) > 1:
        parts.append(f"{len(dirs)} directions (one mass rarely needs two)")
        parts.append(f"{lines // len(dirs)} passes each stepping across "
                     f"{max(extents):.2f} of the canvas")
    else:
        parts.append(f"{lines} passes stepping across {max(extents):.2f} of the canvas")
    if laid > lines * 1.15:
        # The mechanism and the remedy in one breath: a painter told only that the
        # outline cut the passes went looking for a different outline.
        parts.append(f"each cut into {laid / max(lines, 1):.1f} pieces by the outline "
                     f"-- lay the straight stretches as strokes, or use a wider brush")
    return ", ".join(parts)


#: The check's thresholds, each one a number a real pass of a real painting tripped.
_REPORT_MIN_MARKS = 10          # one brush at one size: over this many marks
_REPORT_ANGLE_MARKS = 12        # a stack: this many long marks within...
_REPORT_ANGLE_DEG = 6.0         # ...this many degrees of one another
_REPORT_SMALL_BRISTLE = 0.025   # a comb under this is four streaks with gaps...
_REPORT_STARVED_LOAD = 0.6      # ...unless it was starved this far, where they are the mark
_REPORT_CROSSING_DEG = 30.0     # a long mark this far off the bars runs across them
_REPORT_EARLY_MARKS = 60        # small marks inside the first this many are detail first
_REPORT_SMALL_MARK = 0.02       # ...where small is under this
_REPORT_EARLY_COUNT = 8         # ...and this many of them is the fault
_REPORT_ROUND_MARKS = 3         # small round-tip marks at tip_wobble=0 that are one disc
_ROUND_CAPSULE_WIDTHS = 7.0     # ...where "small" is also shorter than this many widths
_REPORT_DISC_RADIUS = 0.06      # ...and over a whole painting, discs this close are one passage

# `_ROUND_CAPSULE_WIDTHS` is `PAINTING.md`'s own number for the other half of the same
# fault: a `round_hard` mark "needs to be about 7x longer than it is wide before it
# stops reading as one" capsule. Under it, the mark is the tip's silhouette; over it,
# it is a line, and a `liner` drawing fine lines at `tip_wobble=0` is the guide's own
# advice and must not trip this.

# `_REPORT_DISC_RADIUS` is what a whole painting asks of the disc rule in place of a
# pass (finding 12 of the 0.5.0 cohort). A pass is one passage, so the discs it lays are
# seen together; a painting is many, and over all of it the rule was adding up a lamp,
# a moon, two notches, two edge highlights and a glint laid in six passes and calling
# them *one disc printed 8 times*. Discs within this distance of one another, in the
# brush's unit and joined link by link, are one passage. On the 21 finished paintings
# the line went from 14 checklists to 10 -- the four it left were discs standing alone,
# and every repeated passage stayed -- and read the same at any radius from 0.06 to
# 0.15, where 0.04 starts losing groups. `CALIBRATION.md`, *The closing audit, over a
# whole painting*.

# `_REPORT_STARVED_LOAD` is the one threshold here that narrows a rule rather than
# setting one, and it exists because the rule above it was being ignored. A painting
# whose subject is broken glints on water, grit under a flood and feather groups on a
# bird tripped *a bristle under 0.025* twenty-eight times and was right to skip it
# every time: at those loads the comb's gaps **are** the mark. Checked against both
# of that session's paintings, every small-bristle call site in them named an
# explicit `load` and not one used the preset's own `0.9` -- 15 of 16 at or under
# `0.6` in the first painting and 12 of 12 in the second. `0.6` is the top of the
# run-out window `CALIBRATION.md` already publishes for a deliberately broken mark,
# not a new number. What still fires is what the rule was written for: a small
# *loaded* comb, which is a solid plane laid with the wrong tip. A check a painter
# learns to skip costs the other five rules their credibility.


def _mark_length_and_angle(r: StrokeRecord, canvas) -> tuple[float, float]:
    """A mark's chord in the brush's unit (the long side), and its angle mod 180."""
    pts = np.asarray(r.points, dtype=np.float64)
    if len(pts) < 2:
        return 0.0, 0.0
    long = float(canvas.long_side)
    dx = (float(pts[-1, 0]) - float(pts[0, 0])) * canvas.width / long
    dy = (float(pts[-1, 1]) - float(pts[0, 1])) * canvas.height / long
    return math.hypot(dx, dy), math.degrees(math.atan2(dy, dx)) % 180.0


def _angle_centre(angles) -> float:
    """The middle of a cluster of angles that are already ``mod 180``.

    A plain median is wrong here and wrong in the one direction that matters most.
    Marks lying along the horizontal come back as a mixture of ``179`` and ``1``,
    which the clustering above correctly reads as two degrees apart -- and whose
    median is ``90``. So the commonest stack of bars there is named *vertical*, and
    the line a painter is meant to act on points at right angles to the fault. The
    same number steers :func:`_graded_band`'s normal, where it measures the spread
    of a horizontal band *along* the band instead of across it.

    Doubling the angles maps ``mod 180`` onto the whole circle, where a mean has no
    seam, and halving the result brings it back.
    """
    doubled = np.radians(np.asarray(list(angles), dtype=np.float64) * 2.0)
    mean = math.atan2(float(np.sin(doubled).mean()), float(np.cos(doubled).mean()))
    return math.degrees(mean) / 2.0 % 180.0


def _two_ways(values: np.ndarray) -> float:
    """The value that splits a place's pixels into its two clearest parts.

    Otsu's threshold on a 64-bin histogram: the cut that puts the most of the
    variance *between* the two parts and the least inside them. Used by
    :meth:`Session._check_one_mass` to say what the two parts of a straddling place
    actually read, because *this place holds a 0.26 and a 0.55* is a fact a painter
    can act on and *this place is spread* is not.

    A histogram rather than a sort, so the cost does not depend on how big the place
    is; 64 bins, because the answer is going to be printed to three decimals against
    a spread of tenths, and a finer split moves it by less than that.
    """
    hist, edges = np.histogram(values, bins=64, range=(0.0, 1.0))
    mids = (edges[:-1] + edges[1:]) / 2.0
    below = hist.cumsum()
    total = below[-1]
    weight = (hist * mids).cumsum()
    ok = (below > 0) & (total - below > 0)
    between = np.zeros(mids.shape, dtype=np.float64)
    # The usual rearrangement: between-class variance without the two class means,
    # which are a division apiece and cancel.
    between[ok] = ((weight[-1] * below[ok] / total - weight[ok]) ** 2
                   / (below[ok] * (total - below[ok]) / total))
    return float(mids[int(np.argmax(between))])


def _call_of(r: StrokeRecord):
    """What one call the mark belongs to: a mass verb's passes share a key.

    The passes of one mass carry the verb's name and the stream state the call began
    from, and two calls of the same verb cannot share a state, because every mass
    draws from the stream at least once. A mark laid by hand is a call of its own.
    """
    via = r.params.get("via") if r.params else None
    if not via:
        return ("hand", r.index)
    state = r.params.get("rng") or {}
    return (via, state.get("state"), state.get("inc"))


def _angle_name(degrees: float) -> str:
    if degrees < _REPORT_ANGLE_DEG or degrees > 180.0 - _REPORT_ANGLE_DEG:
        return "horizontal"
    if abs(degrees - 90.0) < _REPORT_ANGLE_DEG:
        return "vertical"
    return f"{degrees:.0f} degrees"


#: A graded passage laid by hand has to clear this many of its own steps, the same
#: number ``scumble`` warns on: see :data:`_LINEAR_MIN_STEPS`. Below about a quarter
#: of a step the marks are further apart than four brushes and are separate marks
#: rather than a passage laid badly, so the rule does not reach down there.
_REPORT_BAND_FLOOR = 0.25

#: How many marks make a passage rather than a row of things. Three is the fewest
#: that can have a step at all, and it was three until 0.4.0 -- which is also the
#: number of strokes a small container's body takes, so ten pots on a bench came back
#: as *30 marks at stepping colours*, which are ten objects. Five is over the count of
#: anything this engine's recipes build out of parallel strokes and under every graded
#: passage anyone has laid: ``RECIPES.md``'s hand-rolled band is six strokes, the dawn
#: band that the rule was written for is seven, and a ``scumble`` is ``n``.
_REPORT_BAND_MARKS = 5

#: How wide a gap, in narrowest brushes, breaks one run of parallel marks into two.
#: The same four brushes the floor below is built on, applied *between neighbours*
#: rather than to the set's median step: three trunks were already excluded by the
#: median, and ten pots three strokes each were not, because within a pot the step is
#: three quarters of a brush and only the gaps between pots are wide.
_REPORT_BAND_GAP = 4.0

#: How many times the value sequence across a run may change direction and still be a
#: graded passage. One: a band that brightens, or brightens and falls back, is a
#: passage; the ninth session's dawn band rises over four marks and falls over three.
#: Two ramps laid end to end -- a ``scumble`` of 7 and a ``scumble`` of 8 over
#: adjacent bands, which this rule summed and then offered a remedy three times
#: either band's own step -- turn twice, and ten pots at three terracotta values turn
#: nine times.
_REPORT_BAND_TURNS = 1

#: How many distinct colours a stack of parallel marks needs before it counts as
#: *graded* rather than as a mass. This is what keeps every ``block_in`` out of the
#: rule: its passes step ``size * (1 - 0.45 * density)`` apart, which is always
#: under two brushes, and they are all one colour, so the joins a graded passage
#: shows at that spacing do not arise.
_REPORT_BAND_COLOURS = 3


def _graded_band(long_marks, canvas) -> tuple[int, float, float, float] | None:
    """The largest stack of parallel, stepping-coloured marks whose brush is too narrow.

    ``scumble`` has picked its own brush from its own step since 0.2.0 and says so
    when handed a narrower one -- but ``RECIPES.md`` teaches the hand-rolled form of
    the same passage (*a passage brightening toward one side* is six ``stroke()``
    calls with the sizes written out), and a hand-laid stack gets none of that
    protection. Measured on one painting against itself: its sky, laid with
    ``scumble(n=11)`` and the brush left to the verb, sits at a uniform 4.0 steps and
    its across-band wobble is ``0.037``; its dawn band, seven strokes with brushes
    chosen by hand, tapers 4.2 to **1.7** steps and wobbles ``0.072`` -- twice as
    rough, same canvas, same painter, same pass structure.

    Returns ``(count, step, narrowest brush, brushes per step)`` or ``None``.

    The conditions are narrow on purpose, because a check a painter learns to skip
    costs the other rules their credibility:

    * **parallel and long**, as the stack-of-bars rule counts them;
    * **at three or more distinct colours**, which is what makes it a *graded*
      passage. A mass is one colour however its passes are spaced, and that is what
      keeps every ``block_in`` out of this -- at ``density=1.0`` its passes are
      ``0.55`` of a brush apart, which is under two steps and perfectly right;
    * **spaced between a quarter of a brush and two**, so that marks four brushes
      apart -- three trunks, three cables, three reflections -- are separate marks
      and not a passage laid badly;
    * **in one run**, with no gap between neighbours wider than
      :data:`_REPORT_BAND_GAP` brushes. The spacing clause above is on the set's
      *median* step, which three trunks fail and ten pots of three strokes each do
      not: inside a pot the step is three quarters of a brush, and only the gaps
      between pots are wide;
    * **and stepping one way**, turning at most :data:`_REPORT_BAND_TURNS` time. A
      band that brightens, or brightens and falls back, is a passage. A sequence that
      turns again is a row of things -- ten pots at three terracotta values, or two
      ``scumble`` ramps laid end to end and summed into one stack with a remedy three
      times either band's own step.

    Marks that lay **no colour of their own** are dropped before any of this: a
    ``smudge`` drags what is already there, and one counted at ``size=0.02`` among two
    block-ins and two glazes made itself the narrowest brush in a five-mark
    "passage" it had contributed no colour to.
    """
    long_marks = [(r, a) for r, a in long_marks
                  if float(r.params.get("smudge", 0.0) or 0.0) < 1.0]
    best: list[tuple[StrokeRecord, float]] = []
    for _, centre in long_marks:
        near = [(r, a) for r, a in long_marks
                if min(abs(a - centre), 180.0 - abs(a - centre)) <= _REPORT_ANGLE_DEG]
        if len(near) > len(best):
            best = near
    if len(best) < _REPORT_BAND_MARKS:
        return None

    # Where each mark sits across the stack, in the brush's own unit.
    long_side = float(canvas.long_side)
    angle = math.radians(_angle_centre(a for _, a in best))
    nx, ny = -math.sin(angle), math.cos(angle)
    across = []
    for r, _ in best:
        pts = np.asarray(r.points, dtype=np.float64)
        x = float(pts[:, 0].mean()) * canvas.width / long_side
        y = float(pts[:, 1].mean()) * canvas.height / long_side
        across.append((x * nx + y * ny, r))
    across.sort(key=lambda pair: pair[0])
    run = _longest_run(across)
    if len(run) < _REPORT_BAND_MARKS:
        return None

    colours = {tuple(round(float(v), 4) for v in (r.params.get("color") or ()))
               for _, r in run}
    if len(colours - {()}) < _REPORT_BAND_COLOURS:
        return None
    if _value_turns([r for _, r in run]) > _REPORT_BAND_TURNS:
        return None

    steps = np.diff(np.asarray([off for off, _ in run]))
    steps = steps[steps > 1e-9]
    if steps.size < _REPORT_BAND_MARKS - 1:
        return None
    step = float(np.median(steps))
    brush = min(float(r.params.get("size", 0.0)) for _, r in run)
    if brush <= 0.0 or step <= 0.0:
        return None
    per_step = brush / step
    if not _REPORT_BAND_FLOOR <= per_step < _LINEAR_MIN_STEPS:
        return None
    return len(run), step, brush, per_step


def _longest_run(across) -> list[tuple[float, StrokeRecord]]:
    """The longest stretch of ``(offset, record)`` with no wide gap in it.

    Wide is :data:`_REPORT_BAND_GAP` brushes, measured on the narrower of the two
    marks either side of the gap, so a fine mark next to a broad one is judged by the
    fine one. Input sorted by offset.
    """
    runs: list[list[tuple[float, StrokeRecord]]] = [[]]
    for i, (off, r) in enumerate(across):
        if i:
            prev_off, prev = across[i - 1]
            narrow = min(float(r.params.get("size", 0.0)),
                         float(prev.params.get("size", 0.0)))
            if off - prev_off > _REPORT_BAND_GAP * narrow:
                runs.append([])
        runs[-1].append((off, r))
    return max(runs, key=len)


def _value_turns(run: list[StrokeRecord]) -> int:
    """How many times the value of the colour changes direction along a run.

    Flat steps are not turns: the dawn band repeats its lightest colour at the top
    and still rises once and falls once. Colours a hair apart are flat too, at the
    hundredth a value plan is written to -- otherwise noise in the fourth decimal
    counts as a direction.
    """
    values = [float(luminance(np.asarray(r.params.get("color") or (0.0, 0.0, 0.0),
                                         dtype=np.float32))) for r in run]
    signs = []
    for a, b in zip(values, values[1:], strict=False):
        if abs(b - a) < 0.005:
            continue
        signs.append(1 if b > a else -1)
    return sum(1 for a, b in zip(signs, signs[1:], strict=False) if a != b)


def _crossing_marks(records, centre: float, canvas) -> int:
    """Long marks that run *across* a stack of bars at ``centre`` rather than along it.

    What re-arms the stack-of-bars warning. The warning's own text concedes *unless
    the subject runs that way*, and it cannot tell whether the subject does -- so it
    is said once, and again only when the picture has acquired something that crosses
    what it was said about. This is how the picture is asked.

    ``_REPORT_CROSSING_DEG`` is 30 rather than the 6 the cluster is gathered within,
    because the question here is not *is this mark in the stack* but *does this mark
    read as running across it*. A piling 15 degrees off a run of joists is still part
    of the layer cake; the same piling square to them is what breaks it.

    30 because the pier's own angles are bimodal and it sits in the gap: of its 251
    long marks, 175 lie within 10 degrees of the bars and 43 within 20 degrees of
    square to them, with 33 spread between. Swept over that painting pass by pass,
    **every threshold from 20 to 60 degrees prints the same three lines** -- the
    first stack, the pilings crossing it, and the stack rebuilt afterwards. 15 prints
    four and 0 prints seven, which is the rule with no decay at all. So the number is
    the middle of a plateau rather than a knee, and nothing in reach of it is close.
    """
    long_marks = []
    for r in records:
        length, angle = _mark_length_and_angle(r, canvas)
        if length <= 0.0 or length < 2.0 * float(r.params.get("size", 0.0)):
            continue
        long_marks.append((r, angle))
    n = 0
    for _, angle in _one_per_scumble(long_marks):
        off = abs(angle - centre)
        if min(off, 180.0 - off) >= _REPORT_CROSSING_DEG:
            n += 1
    return n


def _one_per_scumble(long_marks: list[tuple[StrokeRecord, float]]):
    """Long marks with each ``scumble`` call kept as its first pass alone.

    A band laid by :meth:`Session.scumble` is one mass at one angle, and its passes are
    sized to overlap -- three of its own steps -- which is what closes a graded field
    rather than what stacks bars. Counted one by one, they outvoted everything else a
    pass laid: the guide's own graded field, in close colours a smooth field, came back
    *17 of 17 long marks ... a stack of bars*, and over the corpus 10 of the 46 bars
    lines painters were shown were passes led by a scumble -- skies, fog, water. So the
    stack-of-bars rule and the crossings that re-arm it count a scumble once, and
    whether its own passes show as bars is the band's business: ``scumble-bars`` at the
    call. Ruled 2026-09-21, at a known price -- BigPickle's whole-painting line, the one
    true positive of its round, reached its share only by counting the sky passes its
    own painter called fine, and goes silent with them.
    """
    seen = set()
    out = []
    for r, angle in long_marks:
        if r.params and r.params.get("via") == "scumble":
            key = _call_of(r)
            if key in seen:
                continue
            seen.add(key)
        out.append((r, angle))
    return out


#: A daisy: this many hand-laid marks at least :data:`_DAISY_MIN` long leaving one point
#: outward -- the petals, or the spokes of a wagon wheel. Five, because the corpus's
#: tree forks and grass tufts come in threes and fours, and a sun given rays by a loop
#: comes in eights and twelves.
_DAISY_MARKS = 5

#: ...each at least this long, as a share of the long side, so a sparkle of four ticks
#: round a highlight is not a daisy.
_DAISY_MIN = 0.02

#: ...and at least this many times as long as its brush is wide, because a petal or a
#: spoke is a line. Films as wide as they are long, crossing at a point, are a glow:
#: the heron's lamp -- five films `1.1`-`1.4` times as long as they are wide, its pole
#: and the two strokes of its fixture -- leaves no gap over `94` degrees, and one film
#: more would have been called a daisy.
_DAISY_THIN = 2.0

#: ...leaving the point in every direction: no gap in the circle of their directions
#: wider than this. A tree's branches and its trunk leave a fork with three gaps of
#: `120` degrees, grass and a fan of rays one of `290` or more; a daisy of eight petals
#: leaves `45`, and a twelve-ray sun `30`.
_DAISY_GAP = 90.0

#: A radiating set is one loop over angles, so the marks of one are a few calls apart:
#: this many either side of the pair whose lines meet at the hub are counted.
_DAISY_WINDOW = 12


def _daisy(marks: list[StrokeRecord], canvas) -> tuple[int, float, tuple[float, float]] | None:
    """The widest set of hand-laid marks leaving one point in every direction, or ``None``.

    Returns ``(count, widest gap in degrees, hub)``. The hub is where two consecutive
    marks' lines meet -- a daisy or a sunburst is laid by one loop over angles -- and a
    mark near them counts if its line runs through the hub (within a sixth of its own
    length), it points away from it, and it starts within its own length of it, so a
    ray may start at a disc's rim as well as at its centre. Only marks that read as
    lines are counted -- :data:`_DAISY_THIN` -- so a glow of wide films is not one.
    """
    w1, h1 = max(canvas.width - 1, 1), max(canvas.height - 1, 1)
    long = float(canvas.long_side)
    starts, ends, lengths = [], [], []
    for r in marks:
        if r.params.get("via") or r.kind == "smudge" or len(r.points) < 2:
            continue
        p = np.asarray(r.points, dtype=np.float64) * np.array([w1, h1])
        length = float(np.hypot(*np.diff(p, axis=0).T).sum())
        width = float(r.params.get("size", 0.0)) * long
        if length >= _DAISY_MIN * long and length >= _DAISY_THIN * width:
            starts.append(p[0])
            ends.append(p[-1])
            lengths.append(length)
    n = len(lengths)
    if n < _DAISY_MARKS:
        return None
    a_all, b_all, l_all = np.array(starts), np.array(ends), np.array(lengths)
    chord = b_all - a_all
    d_all = chord / np.maximum(np.hypot(*chord.T), 1e-9)[:, None]
    parallel = math.sin(math.radians(8.0))
    best = None
    for i in range(n - 1):
        cross = d_all[i, 0] * d_all[i + 1, 1] - d_all[i, 1] * d_all[i + 1, 0]
        if abs(cross) < parallel:
            continue
        gap_x = a_all[i + 1, 0] - a_all[i, 0]
        gap_y = a_all[i + 1, 1] - a_all[i, 1]
        hub = a_all[i] + ((gap_x * d_all[i + 1, 1] - gap_y * d_all[i + 1, 0]) / cross) * d_all[i]
        lo, hi = max(0, i - _DAISY_WINDOW), min(n, i + _DAISY_WINDOW + 2)
        a, b, ln, d = a_all[lo:hi], b_all[lo:hi], l_all[lo:hi], d_all[lo:hi]
        to_a, to_b = np.hypot(*(a - hub).T), np.hypot(*(b - hub).T)
        far = np.where((to_a <= to_b)[:, None], b, a)
        rel = hub - a
        off = np.abs(d[:, 0] * rel[:, 1] - d[:, 1] * rel[:, 0])
        ok = (off <= ln / 6.0) & (np.minimum(to_a, to_b) <= ln)
        count = int(ok.sum())
        if count < _DAISY_MARKS:
            continue
        out = far[ok] - hub
        angles = np.sort(np.mod(np.degrees(np.arctan2(out[:, 1], out[:, 0])), 360.0))
        gap = float(np.diff(np.concatenate([angles, angles[:1] + 360.0])).max())
        if best is None or (count, -gap) > (best[0], -best[1]):
            best = (count, gap, (float(hub[0]) / w1, float(hub[1]) / h1))
    return best


#: A loop's signature: this many marks of one brush laid one after another...
_LOOP_MARKS = 6

#: ...evenly spaced along a line: the spread of the gaps between them, over their mean.
#: Of the corpus's runs at one length or a ramp, the one loop measures `0.24` and the
#: next run `0.45`; a hand-placed row measures well over half.
_LOOP_SPACING = 0.35

#: ...at one length (the spread of their lengths over the mean), or a strict ramp of
#: lengths, which is a loop too: the ziggurat.
_LOOP_LENGTH = 0.15

#: ...on a line: no mark further off it than this many gaps.
_LOOP_STRAIGHT = 3.0


def _loop_runs(marks: list[StrokeRecord], canvas) -> list[dict]:
    """Runs of consecutive hand-laid marks of one brush that carry a loop's signature.

    One length (or a strict ramp of them), one spacing, on a line, and far enough apart
    to read as marks -- the gap between neighbours at least a mark's own width, because
    six overlapping passes of one film are a graded passage and not a row of anything.
    Consecutive, because a loop lays its marks one call after another, and that is also
    what keeps this from measuring every pair of marks a painting holds.
    """
    w1, h1 = max(canvas.width - 1, 1), max(canvas.height - 1, 1)
    long = float(canvas.long_side)
    runs: list[list[StrokeRecord]] = []
    current: list[StrokeRecord] = []
    for r in marks:
        ok = not r.params.get("via") and r.kind != "smudge" and len(r.points) >= 2
        if ok and current and r.brush == current[0].brush:
            current.append(r)
            continue
        if len(current) >= _LOOP_MARKS:
            runs.append(current)
        current = [r] if ok else []
    if len(current) >= _LOOP_MARKS:
        runs.append(current)
    found = []
    for run in runs:
        paths = [np.asarray(r.points, dtype=np.float64) * np.array([w1, h1]) for r in run]
        lengths = np.array([float(np.hypot(*np.diff(p, axis=0).T).sum()) for p in paths]) / long
        centres = np.array([p.mean(axis=0) for p in paths]) / long
        rel = centres - centres.mean(axis=0)
        axis = np.linalg.svd(rel, full_matrices=False)[2][0]
        order = np.argsort(rel @ axis)
        gaps = np.diff((rel @ axis)[order])
        width = float(np.mean([float(r.params.get("size", 0.0)) for r in run]))
        if gaps.mean() <= 0.0 or gaps.mean() < width:
            continue
        spacing = float(gaps.std() / gaps.mean())
        straight = float(np.abs(rel @ np.array([-axis[1], axis[0]])).max() / gaps.mean())
        ordered = lengths[order]
        ramp = bool(np.all(np.diff(ordered) > 0) or np.all(np.diff(ordered) < 0))
        spread = float(lengths.std() / max(lengths.mean(), 1e-9))
        if spacing <= _LOOP_SPACING and straight <= _LOOP_STRAIGHT and (
                spread <= _LOOP_LENGTH or ramp):
            found.append(dict(count=len(run), brush=run[0].brush, length=float(lengths.mean()),
                              spacing=spacing, ramp=ramp))
    return found


#: A mark counts as watched when it is this small -- a detail -- or noted ``subject``...
_BURIED_SMALL = 0.02

#: ...and as showing when its value stands this far off what is round it.
_BURIED_SHOWING = 0.05

#: It is buried when a pass leaves it under this share of the contrast it had...
_BURIED_KEPT = 0.5

#: ...and the pass is told when a film or a mass buried this many.
_BURIED_MARKS = 3

#: What counts as a layer laid over things, rather than another thing painted in front:
#: the passes of a mass, and a film.
_BURYING_VIAS = ("block_in", "sweep", "scumble", "cover")


def _mark_samples(record: StrokeRecord, canvas) -> tuple[np.ndarray, np.ndarray]:
    """Eight points along a mark in pixels, and the sideways step to what is round it."""
    w1, h1 = max(canvas.width - 1, 1), max(canvas.height - 1, 1)
    p = np.asarray(record.points, dtype=np.float64).reshape(-1, 2) * np.array([w1, h1])
    if len(p) > 1:
        seg = np.hypot(*np.diff(p, axis=0).T)
        cum = np.concatenate([[0.0], np.cumsum(seg)])
        if cum[-1] > 0.0:
            want = np.linspace(0.0, cum[-1], 8)
            p = np.stack([np.interp(want, cum, p[:, 0]), np.interp(want, cum, p[:, 1])], 1)
    if len(p) > 1:
        t = np.gradient(p, axis=0)
        t /= np.maximum(np.hypot(t[:, 0], t[:, 1]), 1e-9)[:, None]
        side = np.stack([-t[:, 1], t[:, 0]], axis=1)
    else:
        side = np.array([[1.0, 0.0]])
    reach = 1.5 * max(float(record.params.get("size", 0.01)) * canvas.long_side, 2.0) + 2.0
    return p, side * reach


def _to_path(pts: np.ndarray, path: np.ndarray) -> np.ndarray:
    """How far each point is from a polyline, in the points' own units."""
    if len(path) == 1:
        return np.hypot(*(pts - path[0]).T)
    a, b = path[:-1], path[1:]
    ab = b - a
    t = ((pts[:, None, :] - a[None]) * ab[None]).sum(axis=2) / np.maximum(
        (ab * ab).sum(axis=1)[None], 1e-12)
    foot = a[None] + np.clip(t, 0.0, 1.0)[..., None] * ab[None]
    return np.hypot(*(pts[:, None, :] - foot).transpose(2, 0, 1)).min(axis=1)


def _buried(opened: np.ndarray, now: np.ndarray, earlier: list[StrokeRecord],
            laid: list[StrokeRecord], canvas) -> tuple[int, int, str] | None:
    """Earlier details a film or a mass took out of sight: ``(buried, showing, what)``,
    ``what`` naming the layers that did it (``a film``, ``a scumble``...).

    ``opened`` and ``now`` are the values view as the pass began and as it ended.
    ``earlier`` is every mark before the pass, ``laid`` the records the pass made. A
    watched mark -- a detail under :data:`_BURIED_SMALL`, or noted ``subject`` -- that
    stood :data:`_BURIED_SHOWING` off what is round it when the pass began and is left
    at under :data:`_BURIED_KEPT` of that contrast is lost; it counts when what covered
    it was a film or the passes of a mass, because another thing painted over a far
    thing's details is back-to-front done right.
    """
    h, w = now.shape
    changed = np.abs(now - opened) > 0.02
    if not changed.any():
        return None
    before, after = _box_mean(opened, 1), _box_mean(now, 1)

    def at(view, q):
        cols = np.clip(np.round(q[:, 0]).astype(int), 0, w - 1)
        rows = np.clip(np.round(q[:, 1]).astype(int), 0, h - 1)
        return view[rows, cols]

    layers = []
    for q in laid:
        if q.kind in History.UNPAINTED_KINDS or not q.points:
            continue
        if q.kind == "glaze":
            what = "a film"
        elif q.params.get("via") in _BURYING_VIAS:
            what = f"a {q.params['via']}"
        else:
            continue
        path = np.asarray(q.points, dtype=np.float64).reshape(-1, 2) * np.array(
            [max(canvas.width - 1, 1), max(canvas.height - 1, 1)])
        reach = 0.5 * float(q.params.get("size", 0.02)) * canvas.long_side + 3.0
        layers.append((path, reach, what))
    if not layers:
        return None
    showing = buried = 0
    kinds: set[str] = set()
    for r in earlier:
        if r.params.get("via") or r.kind in History.UNPAINTED_KINDS or not r.points:
            continue
        if not (float(r.params.get("size", 1.0)) < _BURIED_SMALL
                or "subject" in str(r.note).lower()):
            continue
        pts, side = _mark_samples(r, canvas)
        if float(changed[np.clip(np.round(pts[:, 1]).astype(int), 0, h - 1),
                         np.clip(np.round(pts[:, 0]).astype(int), 0, w - 1)].mean()) < 0.5:
            continue
        was = float(np.mean(np.abs(at(before, pts)
                                   - 0.5 * (at(before, pts + side) + at(before, pts - side)))))
        if was < _BURIED_SHOWING:
            continue
        showing += 1
        left = float(np.mean(np.abs(at(after, pts)
                                    - 0.5 * (at(after, pts + side) + at(after, pts - side)))))
        if left >= _BURIED_KEPT * was:
            continue
        for path, reach, what in layers:
            if float((_to_path(pts, path) <= reach).mean()) >= 0.5:
                buried += 1
                kinds.add(what)
                break
    if buried < _BURIED_MARKS:
        return None
    return buried, showing, " and ".join(sorted(kinds))


def _small_combs(marks: list[StrokeRecord]) -> list[StrokeRecord]:
    """The marks the small-comb rule counts: a loaded bristle under the comb's floor.

    Under ``_REPORT_SMALL_BRISTLE`` a bristle is four streaks with gaps rather than a
    brush -- unless it was starved on purpose, at or under ``_REPORT_STARVED_LOAD``,
    where the comb's gaps are the mark and not the fault.

    Args:
        marks: the marks to look through.

    Returns:
        The loaded small combs, in log order.
    """
    return [r for r in marks
            if r.params.get("tip") == "bristle"
            and float(r.params.get("size", 1.0)) < _REPORT_SMALL_BRISTLE
            and float(r.params.get("load", 1.0)) > _REPORT_STARVED_LOAD]


def _discs(marks: list[StrokeRecord], canvas) -> list[StrokeRecord]:
    """The marks the disc rule counts: each one a round tip's own silhouette.

    Hand-laid, at ``tip_wobble=0``, under ``_REPORT_SMALL_MARK`` and no longer than
    ``_ROUND_CAPSULE_WIDTHS`` of its own width -- past that a round tip is drawing a
    line, which is what a ``liner`` is for.

    Args:
        marks: the marks to look through.
        canvas: the canvas they were laid on, for its proportions.

    Returns:
        The marks that print the tip's disc, in log order.
    """
    found = []
    for r in marks:
        if r.params.get("tip") not in _ROUND_TIPS or r.params.get("via"):
            continue
        if float(r.params.get("tip_wobble", 0.0) or 0.0) > 0.0:
            continue
        size = float(r.params.get("size", 1.0))
        if size >= _REPORT_SMALL_MARK:
            continue
        length, _ = _mark_length_and_angle(r, canvas)
        if length <= _ROUND_CAPSULE_WIDTHS * size:
            found.append(r)
    return found


def _disc_groups(discs: list[StrokeRecord], canvas,
                 radius: float = _REPORT_DISC_RADIUS) -> list[tuple[int, tuple[float, float]]]:
    """The discs a whole painting shows together: how many in each group, and where.

    Joined link by link in the brush's unit (the long side): a disc within ``radius``
    of any disc of a group is in that group, so a row of pots joins up along the stairs
    while a lamp and a moon on opposite sides of the picture stay two marks. A mark is
    placed at the middle of its own path.

    Args:
        discs: the marks the disc rule counted.
        canvas: the canvas they were laid on, for its proportions.
        radius: how close two discs sit to be seen together, in the brush's unit.

    Returns:
        ``(count, (x, y))`` for every group of ``_REPORT_ROUND_MARKS`` or more, the
        largest first, placed at the mean of its marks as canvas fractions -- the
        ``(x, y)`` every place in the engine is given in.
    """
    long = float(canvas.long_side)
    middles = []
    for r in discs:
        pts = np.asarray(r.points, dtype=np.float64).reshape(-1, 2)
        if len(pts):
            middles.append((0.5 * (pts[:, 0].min() + pts[:, 0].max()),
                            0.5 * (pts[:, 1].min() + pts[:, 1].max())))
    if not middles:
        return []
    at = np.asarray(middles, dtype=np.float64)
    units = at * np.array([canvas.width / long, canvas.height / long])
    root = list(range(len(at)))

    def find(i: int) -> int:
        while root[i] != i:
            root[i] = root[root[i]]
            i = root[i]
        return i

    # A row at a time rather than the whole distance table, which a painting of a few
    # thousand dots would make a few hundred megabytes of.
    for i in range(len(units) - 1):
        for j in np.nonzero(np.hypot(*(units[i + 1:] - units[i]).T) <= radius)[0]:
            root[find(i)] = find(i + 1 + int(j))
    members: dict[int, list[int]] = {}
    for i in range(len(at)):
        members.setdefault(find(i), []).append(i)
    found = [(len(group), (float(at[group, 0].mean()), float(at[group, 1].mean())))
             for group in members.values() if len(group) >= _REPORT_ROUND_MARKS]
    return sorted(found, key=lambda one: -one[0])


def _pass_findings(marks: list[StrokeRecord], earlier: int, canvas,
                   banding=None, bands: str = "", whole: bool = False) -> list[str]:
    """The lines :meth:`Session.report` prints, one per rule that fired.

    ``banding`` decides whether the stack-of-bars line is worth printing this time,
    given the angle it would be printed about, and answers with the number of long
    marks crossing the bars or ``None`` for *not this time*. Left off, it always
    prints and the crossings are counted over ``marks`` -- which is the whole painting
    on the audit that leaves it off. The session passes
    :meth:`Session._banding_wanted`, which is what makes that one rule decay.

    ``bands`` is the painter's own declaration, from :meth:`Session.plan`. Given
    ``"subject"`` the stack-of-bars **warning** becomes the method's next **question**,
    as a number: the warning's own text concedes *unless the subject runs that way*,
    and a painter who has declared that it does has answered the only part of it the
    engine could not. It is the rule the corpus shows firing on one pass in seven even
    with its decay, and the one two painters learnt to skim.

    ``whole`` is the closing audit -- :meth:`Session.checklist`, and :meth:`Session.report`
    with ``since`` left off -- where ``marks`` is a painting and not a pass, and two rules
    written for a pass would add the painting up (finding 12 of the 0.5.0 cohort: *265
    marks with a bristle*, *one disc printed 176 times*). The small-comb rule says
    nothing there: it is a choice of brush for the marks about to be laid, which a
    finished painting has none of, and a pass that laid a habit's worth said so when it
    was laid. The disc rule counts only the discs a painting shows together, leaves a
    signature out, and says where they are: a lamp, a moon and a glint laid in three
    passes are three marks, not one disc printed three times. Every other rule reads the
    whole painting as it always has.
    """
    out: list[str] = []
    if not marks:
        return out
    calls = {_call_of(r) for r in marks}

    # One brush at one size, across two or more calls.
    tools = {(r.brush, round(float(r.params.get("size", 0.0)), 4)) for r in marks}
    if len(marks) >= _REPORT_MIN_MARKS and len(calls) >= 2 and len(tools) == 1:
        (brush, size), = tools
        out.append(
            f"all {len(marks)} marks are {brush} at size={size:g}, in {len(calls)} "
            f"calls: one brush at one size for a whole pass reads as one tool. Vary "
            f"the size, the brush or the pressure between things."
        )

    # A stack of passes at one angle, from two or more calls -- a scumble counting once.
    long_marks = []
    for r in marks:
        length, angle = _mark_length_and_angle(r, canvas)
        if length >= 2.0 * float(r.params.get("size", 0.0)) and length > 0.0:
            long_marks.append((r, angle))
    bars = _one_per_scumble(long_marks)
    best: list[tuple[StrokeRecord, float]] = []
    for _, centre in bars:
        near = [(r, a) for r, a in bars
                if min(abs(a - centre), 180.0 - abs(a - centre)) <= _REPORT_ANGLE_DEG]
        if len(near) > len(best):
            best = near
    if (len(best) >= _REPORT_ANGLE_MARKS and len(best) >= 0.6 * len(bars)
            and len({_call_of(r) for r, _ in best}) >= 2):
        centre = _angle_centre(a for _, a in best)
        crossings = (_crossing_marks(marks, centre, canvas) if banding is None
                     else banding(centre))
        if crossings is not None:
            if bands == "subject":
                # Declared, so the bars are the subject and not the fault. What is left
                # to ask is the next question of the method -- whether anything crosses
                # them -- because a picture of nothing but parallel marks is a layer
                # cake whether or not the subject runs that way.
                # A bare count and no denominator: the crossings are counted over the
                # whole picture -- which is the question, since what crosses the bars
                # need not have been laid in this pass -- and `long_marks` is this
                # pass's. Printing one over the other read as *14 of 14* on a picture
                # holding 42.
                crossed = (f"{crossings} long mark{'s' if crossings != 1 else ''} in "
                           f"the picture cross them at {_REPORT_CROSSING_DEG:.0f} "
                           f"degrees or more"
                           if crossings else "nothing crosses them yet")
                out.append(
                    f"bands declared as the subject: {len(best)} long marks run within "
                    f"{_REPORT_ANGLE_DEG:.0f} degrees of {_angle_name(centre)}, and "
                    f"{crossed}."
                )
            else:
                out.append(
                    f"{len(best)} of {len(long_marks)} long marks run within "
                    f"{_REPORT_ANGLE_DEG:.0f} degrees of {_angle_name(centre)}, from "
                    f"{len({_call_of(r) for r, _ in best})} calls: a stack of bars "
                    f"unless the subject runs that way. Vary direction= between "
                    f"passes, or sweep each mass along its own axis. Say "
                    f"s.plan(bands='subject') if it does, and this line will count "
                    f"what crosses them instead."
                )

    # A hand-laid graded passage whose brush is too narrow for its own step.
    band = _graded_band(long_marks, canvas)
    if band is not None:
        count, step, brush, steps = band
        out.append(
            f"{count} marks at stepping colours run parallel {step:.3f} apart, and the "
            f"narrowest brush laying them is {brush:.3g} -- {steps:.1f} of that step. "
            f"Under {_LINEAR_MIN_STEPS:.0f} the passes stop overlapping and a graded "
            f"passage comes back as bars. Use about three steps "
            f"(size={_LINEAR_STEPS * step:.3g} here), or hand the passage to scumble(), "
            f"which sizes its own brush from its own step."
        )

    # A bristle too small to be a brush. A pass's rule and not a painting's: what it
    # asks for is a brush for the next marks.
    small_comb = [] if whole else _small_combs(marks)
    if len(small_comb) >= 3:
        out.append(
            f"{len(small_comb)} marks with a bristle under size={_REPORT_SMALL_BRISTLE} "
            f"at a load over {_REPORT_STARVED_LOAD}: a comb that small is four streaks "
            f"with gaps, not a brush. round_hard reads at that size; a small solid "
            f"plane wants flat at pressure='even'."
        )

    # Detail before the masses are down.
    small = [r for r in marks if float(r.params.get("size", 1.0)) < _REPORT_SMALL_MARK]
    if earlier + len(marks) <= _REPORT_EARLY_MARKS and len(small) >= _REPORT_EARLY_COUNT:
        out.append(
            f"{len(small)} marks under size={_REPORT_SMALL_MARK} inside the painting's "
            f"first {_REPORT_EARLY_MARKS}: detail before the masses are down. A good "
            f"painting is mostly big statements."
        )

    # A round tip printing its own outline, over and over.
    discs = _discs(marks, canvas)
    remedy = (f"Two plain round dabs share 97% of their silhouette; tip_wobble=0.35 is a "
              f"brush set down once and 0.7 a clot, redrawn per mark the way a bristle's "
              f"comb is. Or give the mark a length -- a round tip reads as a capsule "
              f"under {_ROUND_CAPSULE_WIDTHS:.0f} times its own width.")
    if whole:
        # Over a painting only the discs seen together are one disc printed over and
        # over, and a signature is lettering, which the budget waives as well.
        groups = _disc_groups([r for r in discs if not History.is_signature(r)], canvas)
        if len(groups) == 1:
            (count, (x, y)), = groups
            out.append(
                f"{count} small marks with a round tip at tip_wobble=0 sit together "
                f"around ({x:.2f}, {y:.2f}): that is one disc printed {count} times. "
                f"{remedy}"
            )
        elif groups:
            places = ", ".join(f"{count} around ({x:.2f}, {y:.2f})"
                               for count, (x, y) in groups[:3])
            more = f", and {len(groups) - 3} more" if len(groups) > 3 else ""
            out.append(
                f"{sum(count for count, _ in groups)} small marks with a round tip at "
                f"tip_wobble=0 sit together in {len(groups)} places -- {places}{more}: "
                f"each is one disc printed over and over. {remedy}"
            )
    elif len(discs) >= _REPORT_ROUND_MARKS:
        out.append(
            f"{len(discs)} small marks with a round tip at tip_wobble=0: that is one "
            f"disc printed {len(discs)} times. {remedy}"
        )

    # A pressure list asking a chisel for a width.
    tapered = []
    for r in marks:
        if r.params.get("via") or r.params.get("tip") not in _CHISEL_TIPS:
            continue
        if isinstance(r.pressure, str):
            continue
        arr = np.atleast_1d(np.asarray(r.pressure, dtype=np.float32))
        if arr.size < 2 or float(arr.max() - arr.min()) < 0.05:
            continue
        length, _ = _mark_length_and_angle(r, canvas)
        if length <= _SHORT_MARK_WIDTHS * float(r.params.get("size", 0.0)):
            tapered.append(r)
    if tapered:
        tips = sorted({str(r.params.get("tip")) for r in tapered})
        out.append(
            f"{len(tapered)} short mark{'s' if len(tapered) != 1 else ''} with a "
            f"pressure list on a {'/'.join(tips)} tip: pressure changes a chisel's "
            f"paint, not its width, so these are rectangles with a lighter end. A "
            f"mark that tapers wants round_hard or liner."
        )

    # A daisy: hand-laid marks leaving one point in every direction.
    daisy = _daisy(marks, canvas)
    if daisy is not None and daisy[1] <= _DAISY_GAP:
        count, gap, (hx, hy) = daisy
        out.append(
            f"{count} hand-laid marks leave one point, at ({hx:.2f}, {hy:.2f}), in every "
            f"direction -- no gap between them wider than {gap:.0f} degrees: a daisy, or "
            f"a wagon wheel, which is what strokes radiating from a centre draw unless "
            f"the subject radiates. A patch light in the middle is "
            f"scumble(direction=\"inward\"); light in the air is a few films along its "
            f"axis."
        )

    # A loop's signature: one length, one spacing, no clumps and no holes.
    runs = _loop_runs(marks, canvas)
    if runs:
        run = runs[0]
        more = (f" (and {len(runs) - 1} more run{'s' if len(runs) > 2 else ''} like it)"
                if len(runs) > 1 else "")
        size = "stepping in length" if run["ramp"] else f"all {run['length']:.3f} long"
        out.append(
            f"{run['count']} {run['brush']} marks laid one after another, {size}, evenly "
            f"spaced on a line -- the gaps vary {run['spacing']:.0%}{more}: a loop's "
            f"signature, one length and one spacing with no clumps and no holes. Vary the "
            f"lengths and the gaps by hand, or let one mark carry the passage."
        )
    return out


def _buried_line(buried: int, showing: int, what: str) -> str:
    """The report line for :func:`_buried`, whose numbers it carries."""
    return (
        f"this pass took {buried} earlier details out of sight, of the {showing} that "
        f"were showing under it -- each left at under half the contrast it had with what "
        f"is round it, and {what} did it: a layer laid over near things is a mass at a "
        f"depth. Lay it before them, or lay them again after it -- unless taking them "
        f"out of sight was the point."
    )


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
    """One entry per pass: the names as before, plus angles, lines, and sequences.

    ``"cross"`` stays two named passes. A number is one pass at that angle, a pair of
    points is one pass along the line through them, and a sequence is one pass each --
    so a cross at an angle is ``(30, 118)``, which is what a mass wants when its own
    axis is not the canvas's.
    """
    if isinstance(direction, str):
        return ["horizontal", "vertical"] if direction == "cross" else [direction]
    if isinstance(direction, (int, float)):
        return [float(direction)]
    along = _line_angle(direction)
    if along is not None:
        return [along]
    passes: list = []
    for item in direction:
        passes.extend(_pass_directions(item))
    if not passes:
        raise ValueError("block_in(direction=...) was given an empty sequence")
    return passes


def _line_angle(direction) -> float | None:
    """A pair of points as the angle a pass along that line runs at, or ``None``.

    ``direction=`` is an angle in the **normalised** ``0..1`` space, which is not the
    angle it is on screen unless the canvas is square: on 1000x500,
    ``block_in(band, direction=-23)`` lays its passes at **-12 degrees on screen**,
    and on 1024x768 ``45`` runs at ``37``. Every instrument agrees with every other
    -- ``cost_line``'s *stepping across N* is measured in the same space, to the
    hundredth -- and all of them disagree with the picture, which is where a painter
    is looking. Three painters wrote a metric projection, computed the screen slope of
    an edge, typed it in, and got passes at some other angle; one of them laid *passes
    along the sloped boundary*, the recipe for a gable at 41 degrees, at 33.

    So this takes the two points instead and does the arithmetic, which is what every
    painter typing an angle was trying to say. The conversion is nothing -- the angle
    a pass runs at *is* ``atan2`` of the normalised delta -- and that is exactly why
    nobody could see it was needed.

    A pair of numbers is still a pair of angles (``direction=(30, 118)`` is a cross),
    because a number is not a point. A path of three or more points has no one angle
    and says so rather than being read as a sequence of angles.
    """
    if isinstance(direction, (str, int, float)) or not _is_path(direction):
        return None
    pts = [tuple(float(v) for v in p) for p in direction]
    if len(pts) != 2:
        raise ValueError(
            f"direction= takes a line of two points -- direction=((0.33, 0.01), "
            f"(0.58, 0.29)), meaning along this line on the screen -- and was given "
            f"{len(pts)} of them. A curve has no one angle; take the two ends of the "
            f"stretch you mean."
        )
    (x0, y0), (x1, y1) = pts
    dx, dy = x1 - x0, y1 - y0
    if math.hypot(dx, dy) < 1e-9:
        raise ValueError(
            f"direction= was given a line of zero length, ({x0}, {y0}) to ({x1}, "
            f"{y1}). Two different points name a direction; one names a place."
        )
    return math.degrees(math.atan2(dy, dx))


#: The named directions as angles, for the shaped sweep. The rectangle branches
#: keep their own hand-written geometry so that every painting made before shapes
#: existed replays byte for byte; these are the same lines, as numbers.
_NAMED_ANGLES = {"horizontal": 0.0, "vertical": 90.0, "diagonal": -45.0}


def _angle_of(direction) -> float:
    """A direction as degrees: a name, a number, or a line of two points."""
    if isinstance(direction, str):
        if direction not in _NAMED_ANGLES:
            raise ValueError(
                f"Unknown direction {direction!r}. Use 'horizontal', 'vertical', "
                f"'diagonal', 'cross', 'axis', a number of degrees, or a line of two "
                f"points to run along."
            )
        return _NAMED_ANGLES[direction]
    along = _line_angle(direction)
    return float(direction) if along is None else along


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


def _masks_meet(a: np.ndarray, b: np.ndarray, gap_px: float) -> bool:
    """Do two places overlap, or come within ``gap_px`` pixels of each other?

    Overlap is one ``&``. The near case is the same test after growing one of them by
    ``gap_px``, done by rolling rather than by a distance transform: the neighbourhood
    is a square, and a square is separable, so it costs ``2r`` shifts down each axis
    rather than ``(2r+1)^2`` over both -- forty on a fine brush's radius instead of
    seventeen hundred. A square over-reaches a disc by root two at the corners, which
    at this radius is under a pixel of a judgement whose own number is a stand-in.
    """
    if np.any(a & b):
        return True
    r = int(round(gap_px))
    if r < 1:
        return False
    grown = a
    for axis in (0, 1):
        out = grown.copy()
        for shift in [s for step in range(1, r + 1) for s in (step, -step)]:
            moved = np.roll(grown, shift, axis=axis)
            # `roll` wraps, so the rows or columns that came round the far side are
            # cleared: a mass at the top of the canvas is not next to one at the foot.
            edge = slice(None, shift) if shift > 0 else slice(shift, None)
            moved[edge if axis == 0 else (slice(None), edge)] = False
            out |= moved
        grown = out
    return bool(np.any(grown & b))


def _cover_overhang(edge: str, overhang):
    """How far a burial's passes run past their ends, once ``edge`` has had its say.

    Here rather than inside :meth:`Session.cover` because :meth:`Session.cost` has to
    charge what the call lays, and a burial is priced as the block-in it becomes.
    """
    if overhang is not None:
        return float(overhang)
    if edge == "clean":
        return 0.0          # the inset plus the contour already reach the line
    if edge == "hard":
        return None         # nothing can cross the outline: block_in's own rule
    return 1.0              # ragged: ends a brush outside, where no edge is drawn


def _cover_as_mass(spec: dict) -> dict:
    """A burial as the block-in it lays, for the one pricing walk to charge.

    The edge is written in even when the entry leaves it off, because a burial's
    default is not a block-in's: :meth:`Session.cover` holds itself to its place
    (``"hard"``) where a mass breaks past its boundary (``"ragged"``).
    """
    edge = spec.get("edge", "hard")
    mass = {k: v for k, v in spec.items()
            if k in ("place", "brush", "size", "direction", "density", "note")}
    mass.setdefault("brush", "flat")
    mass.setdefault("direction", "horizontal")
    mass["edge"] = edge
    mass["overhang"] = _cover_overhang(edge, spec.get("overhang"))
    return mass


def _brush_overrides_of(spec: dict) -> dict:
    """The brush fields carried by a plan entry, which override that call's brush."""
    return {k: v for k, v in spec.items() if k in _BRUSH_FIELDS}


def _mass_overhang(edge: str, overhang):
    """How far a mass's passes run past their ends, once ``edge`` has had its say.

    Only ``"hard"`` has anything to add: nothing can land outside the outline, so the
    one thing an overhang still does there is carry every pass end up to it. The rest
    is :meth:`Session._block_in_paths`'s own pair of defaults. Here rather than in
    that walk because the walk is handed a fill and never learns which edge asked
    for it -- and :meth:`Session.cost` has to charge what :meth:`Session.block_in`
    lays.

    **Two brushes and not one** (0.6.0, the default moved). One was not enough,
    because the fault is pressure and not reach: the default ``pressure="taper"``
    arrives at zero one brush out, so at ``overhang=1.0`` every pass met the outline
    at part pressure -- and a round tip, which loses *width* with pressure, met it
    at part width too. Measured on a 3 px strip just inside a sloping outline, laid
    solid: a ``round_hard`` left ``0.85%``-``3.26%`` of it bare at one brush and
    ``0.055%``-``0.33%`` at two; a ``flat``, ``0.00%``-``0.66%`` against ``0.000%``.
    Nothing can cross the mask, so the whole cost is a few more dabs on each pass --
    the stroke count is identical at 15, 18, 22 and 25 passes, which is why
    :meth:`Session.cost` quotes the same number either way.
    """
    return 2.0 if edge == "hard" and overhang is None else overhang


def _as_outline(place) -> Polygon:
    """Whatever a painter hands ``clip=``, as one closed outline.

    A shape is itself; a region, a name or a 4-tuple becomes the polygon of its
    rectangle; a run of points is the outline it draws. One place, because ``clip``
    is also what goes in the log and comes back out of it on a replay, and it has to
    be the same thing both ways.
    """
    if (isinstance(place, (list, tuple)) and len(place) > 2
            and all(_looks_like_point(one) for one in place)):
        return polygon([(float(x), float(y)) for x, y in place])
    held = as_place(place)
    return held if isinstance(held, Polygon) else polygon(held)


def _as_outlines(clip) -> tuple[Polygon, ...]:
    """Whatever a painter hands ``clip=``, as every outline the paint is held inside.

    One place is one outline, which is what a clip has been since
    ``block_in(edge="hard")`` was built. A **list** of places is all of them at once,
    and the paint lands only where they all agree -- which is what
    ``block_in(shape, edge="hard", clip=window)`` means and is the only honest thing
    for it to mean: held to its own outline, and to the window as well.
    """
    if clip is None:
        return ()
    if isinstance(clip, (Polygon, Region, str)):
        return (_as_outline(clip),)
    if (isinstance(clip, (list, tuple)) and len(clip) > 0
            and not _looks_like_bounds(clip)
            and not all(_looks_like_point(one) for one in clip)):
        return tuple(_as_outline(one) for one in clip)
    return (_as_outline(clip),)


def _clip_params(holds: tuple[Polygon, ...]):
    """The outlines a held stroke was clipped to, as the log carries them.

    One hold is **one outline**, exactly as every clipped stroke has been logged
    since the first one -- so a painting made before a mark could be held by two
    places replays unchanged, and one made now still loads in a build that only
    knows about one. Two or more are a list of outlines, which such a build refuses
    to read rather than reading as a single outline and painting something else.
    """
    outlines = [[[float(x), float(y)] for x, y in one.points] for one in holds]
    return outlines[0] if len(outlines) == 1 else outlines


def _clips_from_params(held) -> tuple[Polygon, ...]:
    """The other way round: what :func:`_clip_params` wrote, back as outlines."""
    many = bool(held) and not _looks_like_point(held[0])
    return tuple(polygon([(float(x), float(y)) for x, y in one])
                 for one in (held if many else [held]))


def _mass_hold(place, edge: str, clip):
    """Every outline a mass's passes are held inside: its own, and whatever was asked.

    ``edge="hard"`` is a clip -- the mass held to the place it is filling -- and
    ``clip=`` is a clip, so a mass given both is held by both. One place for it,
    because :meth:`Session.block_in`, :meth:`Session.cover` and
    :meth:`Session.scumble` all have to answer the same question the same way.
    """
    holds = _as_outlines(clip)
    if edge == "hard":
        holds = (_as_outline(place),) + holds
    return holds or None


#: How far inside a held outline its edge breaks when ``feather=`` is left off, as a
#: fraction of the long side like ``size``: two pixels on a canvas 1024 wide, three at
#: 1440. **0.7.0; every clip was cut on the line before it.** Chosen blind by the
#: painter whose verdict raised it, first of four candidates, for the tower, the
#: lantern and the cap it had laid hard; ``0.003`` read ragged on anything made.
#:
#: A share of the long side and not a count of pixels, measured at 1440x960, where the
#: painter found the bench's copy of it *a little chewed*: built, the edge there bites
#: at the export's own pixels as 1024's does -- ``0.94`` px at its largest against
#: ``0.94``, wandering ``0.44`` about a straight line against ``0.40`` -- and two
#: pixels are no closer (``1.06``, ``0.38``). ``CALIBRATION.md``, *A held edge,
#: broken*.
_EDGE_FEATHER = 0.002

#: Past this a ``feather=`` is most of a small place -- and far likelier a count of
#: pixels typed into a unit that is not one.
_FEATHER_MAX = 0.05


def _held_feather(feather, held: bool, verb: str) -> float:
    """The feather a call's held edge breaks over, from what the painter passed.

    Left off, the default where the call holds its paint to an outline and nothing
    where it does not. Given, it has to have an edge to break: a ragged mass is
    broken by its own brush, and a feather handed to a call that holds nothing would
    change nothing and say nothing, so it is refused -- except ``0``, which asks for
    what such a call does anyway, so a helper that passes it on every mark is not
    refused on the marks it does not clip.
    """
    if feather is None:
        return _EDGE_FEATHER if held else 0.0
    try:
        f = float(feather)
    except (TypeError, ValueError):
        raise ValueError(f"{verb}(feather={feather!r}) is a number: how far inside the "
                         f"outline the edge breaks, a fraction of the long side like "
                         f"size.") from None
    if not math.isfinite(f) or f < 0.0:
        raise ValueError(f"{verb}(feather={feather!r}) is how far inside the outline the "
                         f"edge breaks, and is zero or more: 0 cuts it on the line.")
    if f > _FEATHER_MAX:
        raise ValueError(
            f"{verb}(feather={feather!r}) is a fraction of the canvas's long side, like "
            f"size -- {_EDGE_FEATHER} is two pixels at 1024 -- so this is the edge "
            f"broken over {f:.0%} of the canvas. Up to {_FEATHER_MAX} is taken.")
    if f > 0.0 and not held:
        raise ValueError(
            f"{verb}(feather={feather!r}) breaks the edge of an outline the paint is held "
            f"inside, and this call holds it to none: give it clip=, or edge='hard' on a "
            f"call that fills a place. A ragged edge is broken by the brush already.")
    return f


def _smudge_path(edge, size: float) -> list:
    """What :meth:`Session.smudge` drags along: points as given, a shape as its outline.

    Points pass straight through, so every mark ever made with two of them still
    lands where it landed. A shape or a region comes back as its own boundary,
    resampled the way :meth:`Session.sweep` resamples one -- fine enough to follow a
    curve, coarse enough that a long outline stays quick.
    """
    if isinstance(edge, (Polygon, Region, str)):
        place = as_place(edge)
        outline = place.closed if isinstance(place, Polygon) else polygon(place).closed
        spine, _ = _sweep_spine(outline, True, max(float(size) * 0.5, 0.01))
        return [(float(x), float(y)) for x, y in spine]
    return edge


def _clean_fill(place, amount: float):
    """What ``block_in(edge="clean")`` fills: the place inset, except at the frame.

    The inset is there so the brush's *outer* half lands on the line the painter
    drew. Where the outline leaves the canvas there is no line out there to land on,
    and pulling the fill in leaves a strip of bare ground along the frame: measured
    on a full-width mass drawn from ``y 0.70`` past the bottom to ``1.05``, a
    ``flat`` at ``size=0.09``, insetting it everywhere left **15.1%** of the bottom
    row unpainted and its corner half way back to bare ground, against **3.6%** for
    the same mass filled ragged. Dropping the inset at the frame leaves **0.3%** --
    better than ragged, because the contour pass runs along the frame too. A mass
    that meets the frame should run off it.

    Since 0.4.0 that is what :meth:`~easel.regions.Region.inset` and
    :meth:`~easel.regions.Polygon.inset` do for anybody, so this is the call and no
    longer the rule. It was the asymmetry that cost a painting: a mass held off the
    seam by hand with ``GLASS.inset(0.024)`` kept the erosion ``edge="clean"`` had
    always dropped, and left the strip down the right frame that this docstring
    describes.
    """
    return as_place(place).inset(float(amount))


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


def _sweep_spine(edge, closed, spacing: float, smooth: bool = True) -> tuple[np.ndarray, bool]:
    """The boundary a sweep follows: smoothed, then resampled at even arc length.

    Smoothed first because that is the curve the strokes will actually paint -- a
    stroke fits a spline through its points, so offsetting the raw corners would
    step the passes off the painted edge. Even spacing is what lets the offset be
    measured in one part-brush and the cross passes be laid in the mass's own
    coordinates rather than the canvas's.

    ``smooth=False`` keeps the edge's own straight sides and corners: the spine is
    the polyline itself, resampled with every vertex kept. That is what a drawn
    polygon's contour wants -- a spline through four sparse corners bows outward by
    tens of pixels, and a `block_in` fill is cut against the straight sides, so the
    smoothed contour and the fill it was meant to finish did not agree about where
    the mass stopped. The stroke laid along the spine still fits its own spline
    through these points, but they sit a part-brush apart, and a spline through
    points that close together is the polyline to within a pixel or two.

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

    dense = (catmull_rom(pts.astype(np.float32), samples_per_segment=12).astype(np.float64)
             if smooth else pts)
    cum = _arc_length(dense)
    total = float(cum[-1])
    if total < 1e-9:
        raise ValueError("sweep(edge=...) has no length: every point is the same place.")

    # Enough points to follow the curve, few enough that a long edge stays quick.
    count = int(np.clip(round(total / max(spacing, 1e-4)) + 1, 4, 96))
    at = np.linspace(0.0, total, count)
    if not smooth and len(dense) <= 96:
        # The corners themselves, so an even resampling cannot cut one off between
        # two samples. An outline dense enough to be smooth already needs none.
        at = np.unique(np.concatenate([at, cum]))
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


def _values_of(rgb8: np.ndarray) -> np.ndarray:
    """An 8-bit RGB array as values, 0..1: what ``look(values=True)`` shows.

    One home for it, because the value of a place is what half of this file measures --
    the plan's own lines, the greyscale of a comparison sheet, and the clusters a
    finished canvas is read for.
    """
    srgb = np.asarray(rgb8, dtype=np.float32) / 255.0
    return linear_to_srgb(luminance(srgb_to_linear(srgb)))


def _grey(rgb8: np.ndarray) -> Image.Image:
    """An 8-bit RGB array as the greyscale the painter sees, for the comparison sheet."""
    grey = (_values_of(rgb8) * 255.0 + 0.5).astype(np.uint8)
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


def _stream_of(rng: np.random.Generator) -> dict:
    """The generator's state as the four numbers a log record carries.

    The PCG64 state proper and its increment, plus the one cached 32-bit draw the
    generator may be holding -- everything :func:`_decode_rng` needs, without the
    name of the bit generator repeated on every record.
    """
    state = rng.bit_generator.state
    inner = state["state"]
    return {"state": int(inner["state"]), "inc": int(inner["inc"]),
            "has_uint32": int(state.get("has_uint32", 0)),
            "uinteger": int(state.get("uinteger", 0))}


def _stream_rng(stored: dict) -> np.random.Generator:
    """A generator at the state a log record carries. The inverse of :func:`_stream_of`."""
    return _decode_rng({"bit_generator": "PCG64",
                        "state": {"state": stored["state"], "inc": stored["inc"]},
                        "has_uint32": stored.get("has_uint32", 0),
                        "uinteger": stored.get("uinteger", 0)})


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


def _warn_foreign_out_dir(session, session_path: Path, out_dir: Path) -> None:
    """Say so when a loaded session will write its looks outside the working directory.

    ``out_dir`` round-trips through the session file because that is how ``easel look
    p.easel`` keeps writing to the same place across CLI invocations -- load-bearing,
    not an oversight. The cost is that loading a ``.easel`` file somebody else made
    writes wherever *they* set it, and until now it did so silently, including to an
    absolute path outside the working directory.

    The path is still honoured. It is the same field a painter legitimately sets with
    ``--out-dir`` when creating a session, so refusing it here would break their setup
    to guard against a file they wrote themselves. What changes is that it is no
    longer silent: loading someone else's session now says where it is about to
    write, once, and the painter can point it elsewhere.

    Two places count as unsurprising: the working directory, and the directory the
    session file itself sits in -- looks beside the painting are the normal
    arrangement, and warning about them would fire on almost every load, which is how
    a warning stops being read at all. What is left is the case worth saying out
    loud: a file that writes somewhere related to neither.
    """
    try:
        resolved = out_dir.expanduser().resolve()
        roots = [Path.cwd().resolve(), session_path.expanduser().resolve().parent]
    except OSError:  # pragma: no cover - an unresolvable cwd is not ours to repair
        return
    if any(resolved == root or root in resolved.parents for root in roots):
        return
    session._notify(
        "foreign-out-dir",
        f"{session_path} writes its looks to {resolved}, which is neither in the "
        f"working directory nor beside the session file. That path came from the "
        f"session file, not from you. Set session.out_dir, or pass --out-dir, to "
        f"send them somewhere else.",
        stacklevel=3,
    )


def _engine() -> str:
    """This build's release number, as a session file is stamped with it.

    Read at the call rather than imported at the top, because ``easel/__init__``
    defines it after it has imported this module.
    """
    import easel

    return str(easel.__version__)


#: The release that first wrote a ``notices`` key into a session file, on every save.
#: Nothing before it wrote one, so a file without an ``engine`` stamp is dated by it.
_NOTICES_SINCE = "0.6.0"


def _saved_by(meta: dict) -> str:
    """The release that wrote a session file, as far as the file can say.

    Its ``engine`` stamp, since 0.7.0. Before the stamp, the ``notices`` key dates a
    file to 0.6.0 -- which writes it on every save, and nothing earlier writes it at
    all -- and a file with neither was saved by 0.5.0 or earlier, which is ``""``:
    older than every fix :data:`~easel.notices.REBUILDS` lists. A stamp with no
    number in it is read as no stamp.
    """
    engine = meta.get("engine")
    if isinstance(engine, str) and version_key(engine):
        return engine.strip()
    return _NOTICES_SINCE if "notices" in meta else ""


def _warn_older_engine(session, session_path: Path, saved_by: str) -> None:
    """Say so when a rebuild of a loaded file's log would not lay what was painted.

    The file holds the canvas, so a painting opens as it was painted under any later
    release; what does not is anything **rebuilt** from its log -- an undo from the
    shell or the server, :meth:`Session.replay`, a film made from the log -- because a
    rebuild lays every mark again with the engine installed, and a fix to how a mark
    is laid reaches it. A painter whose own notes promise a pixel-identical rebuild
    under the release that painted it asked to be told when that stops being true.

    Said once: the file's next save stamps it with this release, and a painting
    continued here is this release's painting from then on. Said only where it
    moves something -- a count of the marks each fix lays differently, and nothing
    for a log with none of them in it -- and only by a later release: a file from a
    later one is not dated against fixes this build has never heard of.
    """
    engine = _engine()
    if version_key(saved_by) >= version_key(engine):
        return
    records = session.history.records
    moved = rebuild_moves(saved_by, records)
    if not moved:
        return
    touched = sum(1 for record in records
                  if any(change.moves(record) for change, _ in moved))
    fixes = "; ".join(
        f"{change.what} ({change.version}, {count} mark{'s' if count != 1 else ''})"
        for change, count in moved
    )
    who = f"Easel {saved_by}" if saved_by else "Easel 0.5.0 or earlier"
    one = touched == 1
    back = (f"Rebuilt under {saved_by} (pip install easel-paint=={saved_by}), it comes "
            f"back as it was painted." if saved_by
            else f"A fix before {_NOTICES_SINCE} is not counted here; CHANGELOG.md names "
                 f"those under each release.")
    session._notify(
        "older-engine",
        f"{session_path} was saved by {who}, and {touched} of the marks in its log "
        f"{'lays' if one else 'lay'} differently under {engine}: {fixes}. The canvas is "
        f"as it was painted, since loading never repaints; anything rebuilt from the log "
        f"-- an undo, a replay, a film made from it -- lays "
        f"{'that mark' if one else 'those marks'} the new way and will not match the "
        f"canvas where {'it is' if one else 'they are'}. {back}",
        stacklevel=3,
    )
