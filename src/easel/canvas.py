"""The canvas: linear-light RGB plus the per-pixel state that makes paint behave.

One canvas, no layers. Real painting has no layers, and the constraint is the
point: the painter learns to work in passes. Undo exists, but it is scraping the
canvas, not a free action.

Three channels beyond colour:

``wetness``
    0..1. Paint landing on wet pixels mixes with what is there instead of covering
    it. Wetness decays as strokes accumulate, so the painter does not have to
    manage it constantly.
``thickness``
    Paint height. Drives the optional impasto relief at export, and makes heavily
    loaded areas resist new paint slightly.
``height``
    The canvas tooth (see :mod:`easel.texture`). Read-only after creation. This is
    what turns a low paint load into a dry-brush stroke without any special case.
``sketch``
    Graphite, 0..1. A channel, not a layer: it sits *under* the paint and paint
    covers it in proportion to how much actually landed, so it shows through thin
    paint and where the ground shows and is gone under an opaque mass. A painter
    does not start on a blank canvas, and making the underdrawing disappear is a
    large part of what painting is.
"""

from __future__ import annotations

import math

import numpy as np

from easel.color import blend_wet, linear_to_srgb, luminance, parse_color, srgb_to_linear
from easel.history import DEFAULT_FRAME_PX
from easel.texture import make_texture, value_noise

__all__ = ["Canvas", "GROUNDS", "GRAPHITE", "build_surface", "tooth_ceiling"]

# How the surface height and its finer grain combine into the field that gates
# deposition. Kept here rather than inline in `stamp` so that `tooth_ceiling` below
# measures exactly the field the gate will see.
# The weave is coherent and periodic; the grain is not. Weighted 0.72/0.28 the
# weave still won, and a broad scumble at load 0.55 -- inside the window PAINTER.md
# calls usable, on the default surface -- printed the linen as an even dot screen
# across the whole canvas. This was predicted when the gate was written and deferred
# "with the sampler and a real painting as the evidence"; a rehearsal run produced
# both. At 0.52/0.48 the weave still organises the breakup but no longer prints as a
# lattice.
_TOOTH_HEIGHT_W = 0.52
_TOOTH_GRAIN_W = 0.48

#: How much tooth the gate's smoothstep rises over, above the need a load sets. The
#: stamp's own gate and a held edge's (:meth:`Canvas.broken_edge`) read the tooth with
#: the one band, so an edge breaks the way a starving brush does.
_GATE_BAND = 0.18


def build_surface(
    texture: str, height: int, width: int, seed: int, texture_strength: float = 1.0
) -> tuple[np.ndarray, np.ndarray]:
    """Build the canvas tooth and its grain from a seed.

    Returns ``(height_map, grain)``. Both are a pure function of the arguments, so a
    saved session stores neither -- it rebuilds them on load.

    The grain is a fine aperiodic field mixed into the tooth when gating deposition.
    The woven textures are near-periodic, and gating a periodic height field with a
    smooth threshold produces a halftone dot screen as paint runs out, which reads as
    print rather than as dry brush. The grain breaks that up.
    """
    rng = np.random.default_rng(seed)
    height_map = make_texture(texture, height, width, rng, texture_strength)
    # The grain carries real weight in the gate, so its scale has to belong to the
    # surface. One fixed fine grain for every texture made all three break up at the
    # grain's scale instead of their own -- cold-press paper stopped leaving chunky
    # islands and started speckling like cloth.
    divisor = {"rough": 11, "linen": 3, "smooth": 4}.get(texture.lower(), 4)
    cells = max(24, max(width, height) // divisor)
    grain = value_noise((height, width), cells, rng).astype(np.float32)
    return height_map, grain


def tooth_ceiling(height_map: np.ndarray, grain: np.ndarray, stride: int = 4) -> float:
    """The highest tooth a starving brush can still reach: the 95th percentile.

    Deposition is gated by a threshold that rises as the brush empties. Left
    unbounded that threshold climbs clean off the top of a surface whose tooth
    occupies a narrow range -- every texture is centred near 0.5, but the gating
    field spans 0.27 on smooth against 0.50 on rough -- and the stroke stops dead
    instead of breaking up. Capping the threshold here means a brush always has some
    peaks left to catch on, whatever it is painting on.

    Sampled on a stride: a texture's percentiles do not need every pixel, and this
    runs once per canvas.
    """
    sample = (height_map[::stride, ::stride] * _TOOTH_HEIGHT_W
              + grain[::stride, ::stride] * _TOOTH_GRAIN_W)
    return float(np.percentile(sample, 95.0))

#: Ground colours the canvas can be primed with, as sRGB hex.
GROUNDS: dict[str, str] = {
    "white": "#F6F4F0",
    "warm_white": "#F3EDE1",
    "toned_grey": "#8C8880",
    "toned_warm_grey": "#94897A",
    "burnt_sienna": "#9A6A50",
    "umber_wash": "#7A6A57",
    "cool_grey": "#828A90",
}

def _PIGMENT_NAMES() -> frozenset[str]:
    """The pigment names, for naming the other namespace when one is used here.

    Imported inside the call rather than at the top: :mod:`easel.palette` imports
    :mod:`easel.color`, which is this module's own dependency, and a module-level
    import here would close the circle for the sake of one error message.
    """
    from easel.palette import PIGMENTS
    return frozenset(PIGMENTS)


# Wetness left after one stroke elapses. Slow enough that wet-into-wet is usable
# for a passage, fast enough that the painter is not fighting mud twenty strokes on.
_WET_DECAY_PER_STROKE = 0.94
_MAX_THICKNESS = 4.0

#: How close to bare a pixel has to be, per sRGB channel, to count as ground still
#: showing through. ``10/255`` is the tighter of the two a painter measured on a
#: finished canvas whose warm ground had been chosen to be seen through and was not:
#: **0.07%** at this, **0.32%** at ``16/255``.
_GROUND_TOLERANCE = 10.0 / 255.0

#: Graphite at full density, as sRGB. Dark and slightly cool, not black -- a pencil
#: line on a toned ground reads as a grey, and an underdrawing that reads as black
#: is one the painter will chase instead of paint through.
GRAPHITE = "#3A3A40"
# Width of the tooth band a pencil crosses as pressure rises. Narrow: the point of
# a pencil is small enough that it skips whole valleys rather than half-filling them.
_GRAPHITE_BAND = 0.13


class Canvas:
    """A paintable surface.

    Args:
        width: pixel width.
        height: pixel height.
        texture: surface tooth -- ``"smooth"``, ``"linen"`` or ``"rough"``.
        ground: a key of :data:`GROUNDS`, a hex string, or an (r, g, b) tuple.
        seed: fixes the texture weave; the same seed gives the same surface.
        texture_strength: scales the tooth. 0 is a perfectly flat surface.

    Coordinates are normalised 0..1 with the origin at the top-left. Pixel
    coordinates are an implementation detail and are never exposed to the painter.
    """

    def __init__(
        self,
        width: int,
        height: int,
        texture: str = "linen",
        ground: str = "white",
        seed: int = 0,
        texture_strength: float = 1.0,
    ) -> None:
        # NaN and Infinity both compare False to `< 8`, so a plain `width < 8`
        # check lets either through and `int(width)` then fails with a raw,
        # unrelated ValueError ("cannot convert float NaN to integer") or
        # OverflowError ("cannot convert float infinity to integer") instead of
        # this constructor's own clear message.
        if (not (math.isfinite(width) and math.isfinite(height))
                or width < 8 or height < 8):
            raise ValueError(f"Canvas must be at least 8x8, got {width}x{height}")
        self.width = int(width)
        self.height = int(height)
        self.seed = int(seed)
        self.texture_name = texture
        self.ground_name = ground if isinstance(ground, str) else "custom"
        # The exact argument, kept so a session can be rebuilt from its log.
        self.ground_spec = ground if isinstance(ground, str) else [float(v) for v in ground]

        if not math.isfinite(texture_strength):
            # Left unchecked this silently NaNs the whole tooth field (and every
            # pixel it gates), which renders as solid black with no error at all.
            raise ValueError(
                f"Canvas texture_strength must be a finite number, got "
                f"{texture_strength!r}."
            )
        self.texture_strength = float(texture_strength)
        self.height_map, self.grain = build_surface(
            texture, self.height, self.width, seed, texture_strength
        )
        self.tooth_ceiling = tooth_ceiling(self.height_map, self.grain)

        self.rgb = self.bare()

        self.wetness = np.zeros((self.height, self.width), dtype=np.float32)
        self.thickness = np.zeros((self.height, self.width), dtype=np.float32)
        # Graphite. `has_sketch` keeps the cost of the channel at zero for a painting
        # that never draws: `stamp` is the hot loop and it is called millions of times.
        self.sketch = np.zeros((self.height, self.width), dtype=np.float32)
        self.has_sketch = False
        self.stroke_count = 0

    # -- coordinates -----------------------------------------------------------------
    @property
    def long_side(self) -> int:
        """The longer pixel dimension; brush sizes are a fraction of this."""
        return max(self.width, self.height)

    def to_px(self, x: float, y: float) -> tuple[float, float]:
        """Normalised (x, y) to pixel coordinates. Internal use."""
        return x * (self.width - 1), y * (self.height - 1)

    @property
    def ground_color(self) -> np.ndarray:
        """The ground as a colour, ready to paint with or to mix.

        A ground is a third namespace beside the pigments and the painter's own
        slots, and it was the only one with no way out: ``ground_name`` and
        ``ground_spec`` say what it is called and what it was made from, and a
        painter who wanted the value they can plainly see had to
        :meth:`~easel.session.Session.sample` an unpainted corner of canvas for it.
        This is that colour, without the tooth's shading on it -- so
        ``p.at_value(s.ground, 0.62)`` and ``p.mix(s.ground, "ultramarine", 0.3)``
        both mean what they look like.
        """
        return self._resolve_ground(self.ground_spec)

    def bare(self) -> np.ndarray:
        """The linear RGB this canvas started as: its ground, shaded by its own tooth.

        Computed rather than kept, because it is the constructor's own two lines and
        a stored copy would be a third of a canvas carried around for a question
        nobody used to ask. It is the reference :meth:`ground_showing` diffs against,
        and it is exact: same ground, same texture, same seed, same shading.
        """
        rgb = np.empty((self.height, self.width, 3), dtype=np.float32)
        rgb[:] = self._resolve_ground(self.ground_spec)
        # The ground is not perfectly even: the tooth shades it very slightly.
        rgb *= (1.0 + (self.height_map - 0.5) * 0.06)[..., None]
        return np.clip(rgb, 0.0, 1.0, out=rgb)

    def ground_showing(self, tolerance: float = _GROUND_TOLERANCE,
                       where: np.ndarray | None = None) -> float:
        """The share of the canvas still within ``tolerance`` of bare ground, ``0..1``.

        The closing checklist asks *is there anywhere the ground still shows
        through? There should be* -- and there was no way to answer it short of
        building a bare canvas and diffing it, which is what a painter finally did
        **after** the painting was finished, having already lost the thing the ground
        was chosen for. A warm ground at ``0.425`` picked so that anything showing
        through a cool film would read as warmth coming through; the interior laid at
        ``density=1.0, load=1.0`` bought a solid support for the fine marks and spent
        the ground to get it, and **0.07%** of the finished canvas was still within
        ``10/255`` of bare.

        Per channel in sRGB, not by value: a cool film laid over a warm ground at the
        same lightness has covered it, and a measure that only reads value would call
        that bare. Graphite is not paint and does not count -- a drawing over the
        ground is still ground showing through.

        Args:
            tolerance: how close to bare a pixel has to be to count, as a fraction of
                the full range. The default is ``10/255``, which is the tighter of
                the two the painter measured; ``16/255`` gave ``0.32%`` on the same
                canvas.
            where: a boolean mask of the pixels to ask about, the canvas's own shape.
                Omitted, the whole canvas. It is what the ``holes:`` line asks with:
                *bare* inside a mass that was just laid solid is the same question as
                *bare* over the picture, and asking it through one definition is what
                keeps `CALIBRATION.md`'s number and this method's from drifting. An
                empty mask has no pixels to average, and answers ``0.0``.

        Returns:
            The share, ``0..1`` -- of the masked pixels when ``where`` is given, and
            of the whole canvas otherwise.
        """
        now = linear_to_srgb(self.composite(impasto=False, sketch=False))
        was = linear_to_srgb(self.bare())
        bare = np.abs(now - was).max(axis=2) <= float(tolerance)
        if where is None:
            return float(np.mean(bare))
        mask = np.asarray(where, dtype=bool)
        return float(bare[mask].mean()) if mask.any() else 0.0

    def _resolve_ground(self, ground) -> np.ndarray:
        if isinstance(ground, str) and not ground.startswith("#"):
            key = ground.lower().replace(" ", "_").replace("-", "_")
            if key not in GROUNDS:
                # A pigment name here is not a typo, it is the other namespace: the
                # painter meant the colour and this argument takes the canvas it is
                # painted on. Say which is which rather than listing the grounds at
                # somebody who named a paint.
                paint = ""
                if key in _PIGMENT_NAMES():
                    paint = (f" {ground!r} is a pigment, not a ground: the two are "
                             f"different namespaces. To lay the canvas in it, pass "
                             f"its hex -- Session(ground=p['{key}']) takes a colour "
                             f"as well as a name.")
                raise ValueError(
                    f"Unknown ground {ground!r}. Choose one of: {', '.join(sorted(GROUNDS))}, "
                    f"or pass a hex string.{paint}"
                )
            return parse_color(GROUNDS[key])
        return parse_color(ground)

    # -- painting --------------------------------------------------------------------
    def stamp(
        self,
        cx: float,
        cy: float,
        mask: np.ndarray,
        color: np.ndarray,
        strength: float,
        load: float,
        wetness_gain: float,
        thickness_gain: float,
        texture_sensitivity: float,
        glaze: bool = False,
        clip: np.ndarray | None = None,
    ) -> float:
        """Deposit one dab. Centre is in pixel coordinates and may be fractional.

        Everything outside the canvas is clipped away, so a stroke can safely run
        off the edge -- which is what a painter does at the border of a canvas.

        ``clip`` is a second, optional mask the size of the canvas: the dab is
        multiplied by it, so a pass can be held inside an outline rather than
        stopping wherever its tip happens to fall. That is what
        ``block_in(edge="hard")`` is, and it is the only way this engine ends a pass
        on a line rather than on a chisel end. Fractional values feather the
        boundary; zero is outside it.

        Returns:
            How much paint actually landed, as the sum of the deposited alpha --
            roughly "how many pixels' worth of opaque paint". Zero means the dab
            made no mark at all, which the painter otherwise has no way to see.
        """
        n = mask.shape[0]
        r = n // 2
        # Round to the nearest pixel; sub-pixel placement comes from jitter and the
        # dab spacing rather than from resampling every stamp.
        ix, iy = int(round(cx)), int(round(cy))
        x0, y0 = ix - r, iy - r
        x1, y1 = x0 + n, y0 + n

        # Clip the stamp against the canvas.
        sx0, sy0 = max(0, -x0), max(0, -y0)
        cx0, cy0 = max(0, x0), max(0, y0)
        cx1, cy1 = min(self.width, x1), min(self.height, y1)
        if cx1 <= cx0 or cy1 <= cy0:
            return 0.0
        sub = mask[sy0 : sy0 + (cy1 - cy0), sx0 : sx0 + (cx1 - cx0)]
        if clip is not None:
            sub = sub * clip[cy0:cy1, cx0:cx1]
            if not np.any(sub > 1e-4):
                return 0.0

        # Gating tooth: the surface height, roughened by the aperiodic grain.
        tooth = (self.height_map[cy0:cy1, cx0:cx1] * _TOOTH_HEIGHT_W
                 + self.grain[cy0:cy1, cx0:cx1] * _TOOTH_GRAIN_W)
        wet = self.wetness[cy0:cy1, cx0:cx1]
        thick = self.thickness[cy0:cy1, cx0:cx1]
        dst = self.rgb[cy0:cy1, cx0:cx1]

        alpha = sub * float(np.clip(strength, 0.0, 1.0))

        # Canvas tooth gating. A full brush fills the valleys too; as the load runs
        # out, only the peaks still receive paint. This is where dry brush comes from.
        #
        # The threshold is capped at the surface's own tooth ceiling. Without that cap
        # it climbs past the highest peak on a narrow-toothed surface and the stroke
        # stops dead: a bristle brush below about a third of its load deposited
        # literally nothing on smooth or linen while still marking rough. Broken is
        # the point; stopping dead is not.
        ts = float(np.clip(texture_sensitivity, 0.0, 1.0))
        if ts > 0.0:
            need = min((1.0 - float(np.clip(load, 0.0, 1.0))) * ts, self.tooth_ceiling)
            gate = np.clip((tooth - need) / _GATE_BAND, 0.0, 1.0)
            gate = gate * gate * (3.0 - 2.0 * gate)
            # Even a full brush sits slightly heavier on the peaks.
            gate = gate * (1.0 - 0.22 * ts * (1.0 - tooth))
            alpha = alpha * gate

        # Paint already piled up resists a little more paint.
        alpha = alpha * (1.0 - 0.12 * np.clip(thick, 0.0, 1.0))

        # Wet paint mixes instead of covering.
        effective = alpha * (1.0 - 0.55 * wet)
        np.clip(effective, 0.0, 1.0, out=effective)
        if not np.any(effective > 1e-4):
            return 0.0

        self.rgb[cy0:cy1, cx0:cx1] = blend_wet(dst, color, effective)

        if self.has_sketch:
            # Paint buries the underdrawing in proportion to what actually landed.
            # Not to what was aimed at: a dab the tooth refused leaves the graphite
            # untouched, which is why the drawing survives in the broken places and
            # in the ground, exactly where a painter still wants to see it.
            sk = self.sketch[cy0:cy1, cx0:cx1]
            np.multiply(sk, 1.0 - effective, out=sk)

        if not glaze:
            # A glaze is a thin film: it colours, but it does not build height.
            np.add(thick, alpha * float(thickness_gain), out=thick)
            np.clip(thick, 0.0, _MAX_THICKNESS, out=thick)

        np.maximum(wet, alpha * float(wetness_gain), out=wet)
        # Thickness two lines above is clamped the same way; wetness was not,
        # so a brush override with an out-of-range wetness_gain (or a NaN one)
        # could pin a pixel's wetness far above 1.0 -- or to NaN, permanently.
        # `effective = alpha * (1.0 - 0.55 * wet)` then goes negative and clips
        # to zero for every dab that lands there, so the pixel stops accepting
        # any paint at all until wetness decays back down, which at the normal
        # 6%-per-stroke rate can take hundreds of strokes for a large overshoot
        # and never happens at all for NaN.
        np.clip(wet, 0.0, 1.0, out=wet)
        return float(effective.sum())

    def broken_edge(self, rows: np.ndarray, cols: np.ndarray, depth: np.ndarray,
                    px) -> np.ndarray:
        """How much paint a held edge lets through at each pixel just inside it, ``0..1``.

        The inward edge a clip is cut with since 0.7.0 (``feather=``): nothing at the
        drawn line, everything ``px`` pixels in, and between the two the canvas's own
        tooth decides, read the way :meth:`stamp` reads a starving brush -- near the
        line only the peaks take paint, deeper in the valleys do too. So the boundary
        breaks at the weave's scale and stays crisp where the tooth is high, which is
        what a loaded brush's edge does over tooth, rather than blurring, which is what
        a ramp alone does.

        Args:
            rows, cols: the pixels, as indices into the canvas.
            depth: how far inside the outline each one sits, in pixels; negative is
                outside, and lets nothing through.
            px: how deep the edge reaches full paint, in pixels -- the feather, or
                per pixel, where a thin shape takes less (``Polygon._edge_depth``).
        """
        tooth = (self.height_map[rows, cols] * _TOOTH_HEIGHT_W
                 + self.grain[rows, cols] * _TOOTH_GRAIN_W)
        full = np.maximum(np.asarray(px, dtype=np.float32), 1e-6)
        ramp = np.clip(np.asarray(depth, dtype=np.float32) / full, 0.0, 1.0)
        gate = np.clip((tooth - (1.0 - ramp) * self.tooth_ceiling) / _GATE_BAND, 0.0, 1.0)
        gate = gate * gate * (3.0 - 2.0 * gate)
        gate = np.where(ramp >= 1.0, 1.0, gate)
        return np.where(ramp <= 0.0, 0.0, gate).astype(np.float32)

    def sample(self, cx: float, cy: float, mask: np.ndarray) -> np.ndarray:
        """Average canvas colour under a stamp. Used by smudge and knife drag."""
        n = mask.shape[0]
        r = n // 2
        ix, iy = int(round(cx)), int(round(cy))
        x0, y0 = ix - r, iy - r
        sx0, sy0 = max(0, -x0), max(0, -y0)
        cx0, cy0 = max(0, x0), max(0, y0)
        cx1, cy1 = min(self.width, x0 + n), min(self.height, y0 + n)
        if cx1 <= cx0 or cy1 <= cy0:
            return np.zeros(3, dtype=np.float32)
        sub = mask[sy0 : sy0 + (cy1 - cy0), sx0 : sx0 + (cx1 - cx0)]
        total = float(sub.sum())
        if total < 1e-6:
            return np.zeros(3, dtype=np.float32)
        window = self.rgb[cy0:cy1, cx0:cx1]
        return (np.tensordot(sub, window, axes=([0, 1], [0, 1])) / total).astype(np.float32)

    # -- drawing ---------------------------------------------------------------------
    def rub(self, cx: float, cy: float, mask: np.ndarray, strength: float, bite: float) -> float:
        """Rub graphite onto the surface at one point. No paint, no wetness, no height.

        Args:
            cx, cy: centre in pixel coordinates.
            mask: the pencil tip stamp.
            strength: darkness of the graphite, 0..1.
            bite: how much of the tooth the point reaches into, 0..1. A light hand
                catches only the peaks and leaves a broken line; a hard one fills
                the valleys too.

        Graphite accumulates as a maximum, not a sum. Consecutive dabs along a line
        overlap almost completely, and any additive rule turns a pencil line into a
        solid bar within a few dabs. Density is chosen with ``strength``, which is
        what the pressure of a real pencil does.

        Returns:
            How much graphite landed, as the sum of the deposited density.
        """
        n = mask.shape[0]
        r = n // 2
        ix, iy = int(round(cx)), int(round(cy))
        x0, y0 = ix - r, iy - r
        sx0, sy0 = max(0, -x0), max(0, -y0)
        cx0, cy0 = max(0, x0), max(0, y0)
        cx1, cy1 = min(self.width, x0 + n), min(self.height, y0 + n)
        if cx1 <= cx0 or cy1 <= cy0:
            return 0.0
        sub = mask[sy0 : sy0 + (cy1 - cy0), sx0 : sx0 + (cx1 - cx0)]

        tooth = (self.height_map[cy0:cy1, cx0:cx1] * _TOOTH_HEIGHT_W
                 + self.grain[cy0:cy1, cx0:cx1] * _TOOTH_GRAIN_W)
        # Same shape as the paint gate, and capped the same way, so a pencil on
        # smooth panel is a near-continuous line and one on rough paper is a chain
        # of grains -- which is the whole reason the tooth is modelled at all.
        need = min((1.0 - float(np.clip(bite, 0.0, 1.0))) * 0.62, self.tooth_ceiling)
        gate = np.clip((tooth - need) / _GRAPHITE_BAND, 0.0, 1.0)
        gate = gate * gate * (3.0 - 2.0 * gate)

        ink = sub * gate * float(np.clip(strength, 0.0, 1.0))
        before = self.sketch[cy0:cy1, cx0:cx1]
        landed = float(np.maximum(ink - before, 0.0).sum())
        np.maximum(before, ink, out=before)
        if landed > 0.0:
            self.has_sketch = True
        return landed

    def erase_sketch(self, region=None) -> None:
        """Clear the graphite, all of it or inside one region or shape."""
        if region is None:
            self.sketch[:] = 0.0
            self.has_sketch = False
            return
        mask = self._mask_of(region)
        if mask is None:
            x0, y0, x1, y1 = self.region_px(region)
            self.sketch[y0:y1, x0:x1] = 0.0
        else:
            self.sketch[mask] = 0.0
        self.has_sketch = bool(self.sketch.any())

    def wetness_at(self, cx: float, cy: float) -> float:
        """Wetness at one point, in pixel coordinates. Cheap: no window average."""
        ix, iy = int(round(cx)), int(round(cy))
        if not (0 <= ix < self.width and 0 <= iy < self.height):
            return 0.0
        return float(self.wetness[iy, ix])

    # -- drying ----------------------------------------------------------------------
    def dry(self, amount: float = 1.0, region=None) -> None:
        """Dry the canvas, all of it or one region.

        ``amount`` of 1.0 dries completely; 0.5 halves the remaining wetness.
        """
        a = float(np.clip(amount, 0.0, 1.0))
        if region is None:
            self.wetness *= 1.0 - a
            return
        mask = self._mask_of(region)
        if mask is None:
            x0, y0, x1, y1 = self.region_px(region)
            self.wetness[y0:y1, x0:x1] *= 1.0 - a
        else:
            self.wetness[mask] *= 1.0 - a

    def tick_wetness(self) -> None:
        """Called once per stroke: paint dries slowly on its own."""
        self.wetness *= _WET_DECAY_PER_STROKE
        self.stroke_count += 1

    def _mask_of(self, region) -> np.ndarray | None:
        """A shaped place as a boolean mask, or ``None`` for a plain rectangle.

        Duck-typed on ``mask``, the way ``region_px`` is duck-typed on ``bounds``, so
        the canvas keeps knowing nothing about the composition helpers -- and so a
        rectangle still goes through the slice it always did.
        """
        mask = getattr(region, "mask", None)
        return None if mask is None else mask(self.width, self.height)

    def region_px(self, region) -> tuple[int, int, int, int]:
        """Normalised region bounds to integer pixel bounds, clipped to the canvas.

        Always at least one pixel wide and tall, and always inside the canvas: x0
        is clamped to leave room for it *before* x1 is computed, so a region that
        touches or runs past the far edge does not push x1 one column past the
        array (a silently empty slice, not an error) the way clamping x0 and x1
        independently to the same [0, width] range would.
        """
        bounds = getattr(region, "bounds", region)
        rx0, ry0, rx1, ry1 = (float(v) for v in bounds)
        x0 = int(np.clip(round(rx0 * self.width), 0, max(self.width - 1, 0)))
        y0 = int(np.clip(round(ry0 * self.height), 0, max(self.height - 1, 0)))
        x1 = int(np.clip(round(rx1 * self.width), x0 + 1, self.width))
        y1 = int(np.clip(round(ry1 * self.height), y0 + 1, self.height))
        return x0, y0, x1, y1

    # -- export ----------------------------------------------------------------------
    def composite(self, impasto: bool = True, sketch: bool = True) -> np.ndarray:
        """The surface as it would be seen, in linear light: paint, relief, graphite.

        One place, so that the export, the greyscale view and the time-lapse
        thumbnails all agree about what is on the canvas. A value read off one of
        them and acted on in another is the failure mode this guards against.
        """
        rgb = self.rgb
        if impasto and float(self.thickness.max()) > 1e-3:
            t = np.clip(self.thickness, 0.0, _MAX_THICKNESS)
            # Gradient of the paint surface; light from the upper left.
            gy, gx = np.gradient(t)
            relief = np.clip((gx + gy) * 0.35, -0.5, 0.5)
            rgb = np.clip(rgb * (1.0 + relief[..., None] * 0.30), 0.0, 1.0)
        if sketch and self.has_sketch:
            # Whatever graphite the paint has not buried, over the top. Applied
            # after the relief: pencil adds no height, so it must not be embossed.
            g = self.sketch[..., None]
            rgb = rgb * (1.0 - g) + _graphite_linear() * g
        return rgb

    def to_srgb8(self, impasto: bool = True, sketch: bool = True) -> np.ndarray:
        """Render to an 8-bit sRGB array (h, w, 3), ready for PNG encoding.

        Args:
            impasto: shade the paint height as low relief, lit from the top-left.
                Subtle by design -- it should read as texture, not as embossing.
            sketch: show the graphite the paint has not covered.
        """
        return (linear_to_srgb(self.composite(impasto, sketch)) * 255.0 + 0.5).astype(np.uint8)

    def thumbnail_srgb8(self, max_side: int = DEFAULT_FRAME_PX) -> np.ndarray:
        """A small 8-bit sRGB view, for time-lapse frames.

        Downsamples in linear space *before* the sRGB conversion. Converting the
        full canvas and then shrinking it costs the same as a full export on every
        single stroke, which is most of the price of leaving the time-lapse on.
        """
        longest = max(self.width, self.height)
        step = max(1, int(np.ceil(longest / float(max(max_side, 1)))))
        full = self.composite(impasto=False, sketch=True)
        if step == 1:
            return (linear_to_srgb(full) * 255.0 + 0.5).astype(np.uint8)
        # Box-average each block rather than point-sampling, so the thumbnail does
        # not alias the canvas weave into moire.
        #
        # Each axis is capped at its own size before dividing: `step` is sized
        # off the *longer* axis, and a canvas far thinner than that on the other
        # axis (an extreme aspect ratio, still >= 8px, the minimum) would
        # otherwise floor that axis's block count to zero -- a zero-width or
        # zero-height frame that corrupts the time-lapse and crashes
        # ``save_gif()`` on it. For the common case both axes are already at
        # least `step`, so this caps to nothing and the result is unchanged.
        step_y = min(step, self.height)
        step_x = min(step, self.width)
        h = (self.height // step_y) * step_y
        w = (self.width // step_x) * step_x
        blocks = full[:h, :w].reshape(h // step_y, step_y, w // step_x, step_x, 3)
        small = blocks.mean(axis=(1, 3))
        return (linear_to_srgb(small) * 255.0 + 0.5).astype(np.uint8)

    def values(self, sketch: bool = True) -> np.ndarray:
        """The canvas as 8-bit greyscale: the value structure, the way a painter squints."""
        lum = luminance(self.composite(impasto=False, sketch=sketch))
        return (linear_to_srgb(lum) * 255.0 + 0.5).astype(np.uint8)

    # -- state -----------------------------------------------------------------------
    def snapshot(self, box: tuple[int, int, int, int] | None = None) -> dict:
        """A copy of every mutable channel, for undo -- of all of it, or of one box.

        A mark touches a few percent of a canvas and the undo stack used to keep
        twenty-four copies of the whole of it: about **33 MB a stroke** at 1440x960,
        so roughly **800 MB resident**, and 6.3 ms of copying before a dab lands
        (``CALIBRATION.md``, B15). Given the box the mark can reach, this copies that
        box instead, and :meth:`restore` writes it back where it came from. The
        stack is then unwound newest first -- see
        :meth:`easel.history.History.pop_snapshots` -- because a box holds the state
        before *its own* mark and nothing about the marks laid after it.
        """
        if box is None:
            return {
                "rgb": self.rgb.copy(),
                "wetness": self.wetness.copy(),
                "thickness": self.thickness.copy(),
                # Paint buries graphite destructively, so undoing a stroke has to
                # bring back the drawing it covered. ``None`` records "there was no
                # drawing here yet", which is not the same as "leave the drawing
                # alone" -- and it keeps a painting that never draws from carrying
                # twenty-four spare colour planes around in its undo stack.
                "sketch": self.sketch.copy() if self.has_sketch else None,
                "stroke_count": np.int64(self.stroke_count),
            }
        x0, y0, x1, y1 = box
        return {
            "box": (int(x0), int(y0), int(x1), int(y1)),
            "rgb": self.rgb[y0:y1, x0:x1].copy(),
            "thickness": self.thickness[y0:y1, x0:x1].copy(),
            "sketch": self.sketch[y0:y1, x0:x1].copy() if self.has_sketch else None,
            # Whole, because wetness is the one channel a mark changes everywhere:
            # :meth:`tick_wetness` dries the entire canvas a little per stroke, so
            # there is no box that holds what a mark did to it. It is one plane
            # against the colour's three, and it is the cheap one to keep.
            "wetness": self.wetness.copy(),
            "stroke_count": np.int64(self.stroke_count),
        }

    def restore(self, snap: dict) -> None:
        """Restore a snapshot taken by :meth:`snapshot`, whole or by its box."""
        box = snap.get("box")
        if box is not None:
            x0, y0, x1, y1 = box
            self.rgb[y0:y1, x0:x1] = snap["rgb"]
            self.thickness[y0:y1, x0:x1] = snap["thickness"]
            self.wetness = np.array(snap["wetness"], dtype=np.float32, copy=True)
            stored = snap.get("sketch")
            if stored is not None:
                self.sketch[y0:y1, x0:x1] = stored
                self.has_sketch = True
            self.stroke_count = int(snap["stroke_count"])
            return
        self.rgb = np.array(snap["rgb"], dtype=np.float32, copy=True)
        self.wetness = np.array(snap["wetness"], dtype=np.float32, copy=True)
        self.thickness = np.array(snap["thickness"], dtype=np.float32, copy=True)
        if "sketch" in snap:
            stored = snap["sketch"]
            if stored is None:
                self.sketch[:] = 0.0
                self.has_sketch = False
            else:
                self.sketch = np.array(stored, dtype=np.float32, copy=True)
                self.has_sketch = True
        self.stroke_count = int(snap["stroke_count"])

    def trial_copy(self) -> Canvas:
        """A canvas that can be painted on and thrown away.

        The mutable channels are copied; the tooth, its grain and the ceiling
        derived from them are *shared*, because they never change and they are the
        expensive part. This is what :meth:`easel.session.Session.rehearse` paints
        on, so that trying a mark three ways costs three small copies rather than
        three canvases.
        """
        c = Canvas.__new__(Canvas)
        c.__dict__.update(self.__dict__)
        c.rgb = self.rgb.copy()
        c.wetness = self.wetness.copy()
        c.thickness = self.thickness.copy()
        c.sketch = self.sketch.copy()
        return c

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return (
            f"Canvas({self.width}x{self.height}, texture={self.texture_name!r}, "
            f"ground={self.ground_name!r}, strokes={self.stroke_count})"
        )


_GRAPHITE_LINEAR: np.ndarray | None = None


def _graphite_linear() -> np.ndarray:
    """The graphite colour in linear light. Parsed once."""
    global _GRAPHITE_LINEAR
    if _GRAPHITE_LINEAR is None:
        _GRAPHITE_LINEAR = parse_color(GRAPHITE)
    return _GRAPHITE_LINEAR


def from_srgb_array(arr: np.ndarray) -> np.ndarray:
    """Helper for tests and reference loading: 8-bit sRGB to linear float32."""
    return srgb_to_linear(np.asarray(arr, dtype=np.float32) / 255.0)
