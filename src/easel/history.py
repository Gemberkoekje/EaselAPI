"""Stroke history: the log, undo snapshots, replay, and the time-lapse.

Every stroke is recorded as data, not as pixels. That buys three things: the whole
painting replays from the log plus the seed, the human watching gets a time-lapse
for free, and a painting can be inspected as a sequence of decisions rather than a
flat image.

Undo restores a snapshot. Snapshots are expensive (they copy the canvas), so only
the most recent :data:`MAX_SNAPSHOTS` are kept -- which is also why the painter's
guide describes undo as scraping the canvas rather than as a free action.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

import numpy as np
from PIL import Image

__all__ = ["StrokeRecord", "History", "MAX_SNAPSHOTS"]

#: How many undo steps are kept. Older snapshots are dropped, not the log entries.
MAX_SNAPSHOTS = 24

#: Cap on time-lapse frames held in memory. Past this the sequence is decimated
#: (every other frame dropped), which keeps the whole arc of the painting visible
#: while bounding both memory and the size of a saved session.
MAX_FRAMES = 200


@dataclass
class StrokeRecord:
    """One entry in the painting log. Enough to replay the stroke exactly."""

    index: int
    kind: str  # "stroke", "dry", "glaze", "smudge", "pencil", "erase"
    brush: str = ""
    color_hex: str = ""
    points: list = field(default_factory=list)
    pressure: object = "taper"
    dabs: int = 0
    #: Pixels' worth of opaque paint this mark actually deposited. A stroke can be
    #: stamped in full and deposit nothing, and this is what says so.
    paint: float = 0.0
    note: str = ""
    params: dict = field(default_factory=dict)

    def to_json(self) -> dict:
        d = asdict(self)
        d["points"] = [[round(float(x), 5), round(float(y), 5)] for x, y in self.points]
        if isinstance(d["pressure"], np.ndarray):  # pragma: no cover - defensive
            d["pressure"] = [float(v) for v in d["pressure"]]
        return d


def _short(value: float) -> str:
    """A paint quantity at a glance: 940, 4.2k, 1.1M."""
    if value >= 1e6:
        return f"{value / 1e6:.1f}M"
    if value >= 1e3:
        return f"{value / 1e3:.1f}k"
    return f"{value:.0f}"


class History:
    """The stroke log plus a bounded stack of canvas snapshots."""

    def __init__(self) -> None:
        self.records: list[StrokeRecord] = []
        self._snapshots: list[dict] = []
        self._frames: list[np.ndarray] = []

    # -- log ---------------------------------------------------------------------
    def add(self, record: StrokeRecord) -> StrokeRecord:
        self.records.append(record)
        return record

    #: Log entries that are not marks of paint. The stroke budget in the brief's
    #: definition of done counts paint, so drawing, erasing, drying and looking are
    #: all free -- a painter who has to spend strokes on the underdrawing will skip
    #: the underdrawing, which is the opposite of what M6 is for.
    UNPAINTED_KINDS = ("dry", "look", "pencil", "erase")

    @property
    def stroke_count(self) -> int:
        """How many marks of paint have been made. Drawing and drying do not count."""
        return sum(1 for r in self.records if r.kind not in History.UNPAINTED_KINDS)

    def summary(self, last: int = 10) -> str:
        """A short text log of recent actions, for the painter to re-read."""
        if not self.records:
            return "(nothing painted yet)"
        lines = []
        for r in self.records[-last:]:
            bits = [f"#{r.index:03d}", r.kind]
            if r.brush:
                bits.append(r.brush)
            if r.color_hex:
                bits.append(r.color_hex)
            if r.dabs:
                bits.append(f"{r.dabs} dabs")
            if r.kind not in History.UNPAINTED_KINDS and r.dabs:
                # Say it plainly when a mark laid no paint: the painter is looking
                # at the log precisely because the canvas did not change.
                bits.append("NO PAINT LANDED" if r.paint < 1.0 else f"{_short(r.paint)} paint")
            elif r.kind == "pencil":
                bits.append("NOTHING DREW" if r.paint < 1.0 else f"{_short(r.paint)} graphite")
            if r.note:
                bits.append(f"-- {r.note}")
            lines.append(" ".join(bits))
        return "\n".join(lines)

    # -- undo --------------------------------------------------------------------
    def push_snapshot(self, snap: dict) -> None:
        self._snapshots.append(snap)
        if len(self._snapshots) > MAX_SNAPSHOTS:
            self._snapshots.pop(0)

    def pop_snapshots(self, n: int) -> dict | None:
        """Take the state from ``n`` steps back, discarding what is undone."""
        if n <= 0 or not self._snapshots:
            return None
        n = min(n, len(self._snapshots))
        snap = self._snapshots[-n]
        del self._snapshots[-n:]
        del self.records[-n:]
        return snap

    @property
    def undo_depth(self) -> int:
        """How many strokes can still be undone."""
        return len(self._snapshots)

    # -- time-lapse --------------------------------------------------------------
    def add_frame(self, rgb8: np.ndarray, max_side: int = 360) -> None:
        """Record a small frame for the time-lapse."""
        img = Image.fromarray(rgb8, mode="RGB")
        longest = max(img.size)
        if longest > max_side:
            f = max_side / float(longest)
            img = img.resize(
                (max(1, int(img.size[0] * f)), max(1, int(img.size[1] * f))), Image.LANCZOS
            )
        self._frames.append(np.asarray(img, dtype=np.uint8))
        if len(self._frames) > MAX_FRAMES:
            # Thin the sequence rather than dropping the beginning: the early
            # block-in is the most interesting part of a time-lapse.
            self._frames = self._frames[::2]

    @property
    def frame_count(self) -> int:
        return len(self._frames)

    def save_gif(self, path: str | Path, fps: float = 8.0, hold_last: float = 1.5) -> Path:
        """Write the time-lapse as an animated GIF."""
        if not self._frames:
            raise ValueError(
                "No time-lapse frames were recorded. Create the session with "
                "timelapse=True, or call session.capture_frame() as you paint."
            )
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        frames = [Image.fromarray(f, mode="RGB").convert("P", palette=Image.ADAPTIVE)
                  for f in self._frames]
        per_frame = max(20, int(round(1000.0 / max(fps, 0.1))))
        durations = [per_frame] * len(frames)
        durations[-1] = max(per_frame, int(hold_last * 1000))
        frames[0].save(
            p, save_all=True, append_images=frames[1:], duration=durations, loop=0, optimize=True
        )
        return p

    def save_contact_sheet(self, path: str | Path, columns: int = 6) -> Path:
        """Write the time-lapse as a single contact sheet of thumbnails."""
        if not self._frames:
            raise ValueError("No time-lapse frames were recorded.")
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)

        step = max(1, len(self._frames) // 36)
        picked = self._frames[::step][:36]
        fh, fw = picked[0].shape[:2]
        thumb_w = 220
        thumb_h = max(1, int(round(fh * thumb_w / fw)))
        rows = (len(picked) + columns - 1) // columns
        pad = 6
        sheet = Image.new(
            "RGB",
            (columns * thumb_w + pad * (columns + 1), rows * thumb_h + pad * (rows + 1)),
            (28, 28, 30),
        )
        for i, frame in enumerate(picked):
            thumb = Image.fromarray(frame, mode="RGB").resize((thumb_w, thumb_h), Image.LANCZOS)
            cx = pad + (i % columns) * (thumb_w + pad)
            cy = pad + (i // columns) * (thumb_h + pad)
            sheet.paste(thumb, (cx, cy))
        sheet.save(p)
        return p

    # -- serialisation -----------------------------------------------------------
    def to_json(self) -> str:
        return json.dumps([r.to_json() for r in self.records], indent=1)

    @staticmethod
    def records_from_json(text: str) -> list[StrokeRecord]:
        return [StrokeRecord(**entry) for entry in json.loads(text)]

    def save_log(self, path: str | Path) -> Path:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(self.to_json(), encoding="utf-8")
        return p
