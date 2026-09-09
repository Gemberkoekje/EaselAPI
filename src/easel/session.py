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
from easel.palette import Palette
from easel.regions import Region, as_region
from easel.stroke import paint_stroke

__all__ = ["Session"]

_EASEL_FORMAT = 1


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

        index = len(self.history.records)
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
                ``"cross"``. Vary this between passes so the marks are not parallel.
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

        passes: list[str] = (
            ["horizontal", "vertical"] if direction == "cross" else [direction]
        )
        for pass_dir in passes:
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

    def _block_paths(self, r: Region, direction: str, band: float, over: float):
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

    # -- canvas state -----------------------------------------------------------
    def dry(self, amount: float = 1.0, region=None) -> StrokeRecord:
        """Dry the canvas so the next paint covers instead of mixing."""
        r = as_region(region) if region is not None else None
        self.canvas.dry(amount, r)
        return self.history.add(
            StrokeRecord(
                index=len(self.history.records),
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
        if depth:
            snap = self.history.pop_snapshots(n)
            if snap is not None:
                self.canvas.restore(snap)
                return min(n, depth)
        # No snapshots -- this session came off disk. Rebuild from the log instead,
        # which costs a full repaint but is exact.
        keep = max(0, len(self.history.records) - n)
        undone = len(self.history.records) - keep
        self._adopt(self.replay(upto=keep))
        return undone

    # -- looking ----------------------------------------------------------------
    def look(
        self,
        scale: int | None = DEFAULT_LOOK_SIZE,
        grid: bool = False,
        values: bool = False,
        region=None,
        reference: str | Path | Image.Image | None = None,
        diff: bool = False,
        path: str | Path | None = None,
        impasto: bool = True,
    ) -> Path:
        """Look at the canvas. Returns the path to a PNG.

        Look every five to fifteen strokes. A stroke you did not look at was a guess.

        Args:
            scale: long-side pixel limit; ``None`` for full resolution.
            grid: overlay the labelled A-H by 1-8 grid.
            values: greyscale, for judging the value structure.
            region: crop to a region, at full resolution.
            reference: place a reference image alongside for comparison.
            diff: tint what changed since the previous ``look()``.
            path: where to write. Defaults to ``out_dir/look_NNN.png``.
            impasto: shade paint height as relief.
        """
        ref_img = None
        if reference is not None:
            ref_img = reference if isinstance(reference, Image.Image) else load_reference(reference)

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
        )
        self._last_look = current

        if path is None:
            self._look_counter += 1
            path = self.out_dir / f"look_{self._look_counter:03d}.png"
        return save_look(img, path)

    def look_image(self, **kwargs) -> Image.Image:
        """The same view as :meth:`look`, returned as a PIL image instead of a path."""
        ref = kwargs.pop("reference", None)
        ref_img = None
        if ref is not None:
            ref_img = ref if isinstance(ref, Image.Image) else load_reference(ref)
        diff = kwargs.pop("diff", False)
        img = render_look(
            self.canvas, reference=ref_img,
            diff_against=self._last_look if diff else None, **kwargs
        )
        self._last_look = self.canvas.to_srgb8(impasto=kwargs.get("impasto", True))
        return img

    # -- output -----------------------------------------------------------------
    def export(self, path: str | Path, impasto: bool = True) -> Path:
        """Write the finished painting as a PNG at full resolution."""
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        Image.fromarray(self.canvas.to_srgb8(impasto=impasto), mode="RGB").save(p)
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
        }
        frames = self.history._frames
        # Written through an open handle: np.savez_compressed appends ".npz" to a
        # path that lacks it, which would make `easel new p.easel` write p.easel.npz
        # and every later command fail to find its own session.
        #
        # The canvas tooth and grain are a pure function of (texture, size, seed,
        # strength), so they are rebuilt on load rather than stored.
        with open(p, "wb") as fh:
            np.savez_compressed(
                fh,
                meta=np.array(json.dumps(meta)),
                log=np.array(self.history.to_json()),
                rgb=self.canvas.rgb,
                wetness=self.canvas.wetness,
                thickness=self.canvas.thickness,
                frames=np.stack(frames) if frames else np.zeros((0, 1, 1, 3), dtype=np.uint8),
                last_look=self._last_look if self._last_look is not None
                else np.zeros((0, 0, 3), dtype=np.uint8),
            )
        return p

    @classmethod
    def load(cls, path: str | Path) -> Session:
        """Reload a session saved by :meth:`save`."""
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(
                f"No session at {p}. Create one with `easel new` before painting."
            )
        with np.load(p, allow_pickle=False) as data:
            meta = json.loads(str(data["meta"]))
            if meta.get("format") != _EASEL_FORMAT:
                raise ValueError(
                    f"Session file {p} has format {meta.get('format')}, "
                    f"this build of Easel writes format {_EASEL_FORMAT}."
                )
            s = cls.__new__(cls)
            s.seed = int(meta["seed"])
            s.rng = _decode_rng(meta["rng_state"])
            s.out_dir = Path(meta["out_dir"])
            s.timelapse = bool(meta["timelapse"])
            s._look_counter = int(meta["look_counter"])

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

        for record in records:
            if record.kind == "dry":
                fresh.dry(record.params.get("amount", 1.0), record.params.get("region"))
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
