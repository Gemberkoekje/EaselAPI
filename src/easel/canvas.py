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
"""

from __future__ import annotations

import numpy as np

from easel.color import blend_wet, linear_to_srgb, luminance, parse_color, srgb_to_linear
from easel.texture import make_texture, value_noise

__all__ = ["Canvas", "GROUNDS", "build_surface"]


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
    grain = value_noise((height, width), max(48, max(width, height) // 3), rng).astype(np.float32)
    return height_map, grain

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

# Wetness left after one stroke elapses. Slow enough that wet-into-wet is usable
# for a passage, fast enough that the painter is not fighting mud twenty strokes on.
_WET_DECAY_PER_STROKE = 0.94
_MAX_THICKNESS = 4.0


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
        if width < 8 or height < 8:
            raise ValueError(f"Canvas must be at least 8x8, got {width}x{height}")
        self.width = int(width)
        self.height = int(height)
        self.seed = int(seed)
        self.texture_name = texture
        self.ground_name = ground if isinstance(ground, str) else "custom"
        # The exact argument, kept so a session can be rebuilt from its log.
        self.ground_spec = ground if isinstance(ground, str) else [float(v) for v in ground]

        self.texture_strength = float(texture_strength)
        self.height_map, self.grain = build_surface(
            texture, self.height, self.width, seed, texture_strength
        )

        ground_lin = self._resolve_ground(ground)
        self.rgb = np.empty((self.height, self.width, 3), dtype=np.float32)
        self.rgb[:] = ground_lin
        # The ground is not perfectly even: the tooth shades it very slightly.
        shade = 1.0 + (self.height_map - 0.5) * 0.06
        self.rgb *= shade[..., None]
        np.clip(self.rgb, 0.0, 1.0, out=self.rgb)

        self.wetness = np.zeros((self.height, self.width), dtype=np.float32)
        self.thickness = np.zeros((self.height, self.width), dtype=np.float32)
        self.stroke_count = 0

    # -- coordinates -----------------------------------------------------------------
    @property
    def long_side(self) -> int:
        """The longer pixel dimension; brush sizes are a fraction of this."""
        return max(self.width, self.height)

    def to_px(self, x: float, y: float) -> tuple[float, float]:
        """Normalised (x, y) to pixel coordinates. Internal use."""
        return x * (self.width - 1), y * (self.height - 1)

    def _resolve_ground(self, ground) -> np.ndarray:
        if isinstance(ground, str) and not ground.startswith("#"):
            key = ground.lower().replace(" ", "_").replace("-", "_")
            if key not in GROUNDS:
                raise ValueError(
                    f"Unknown ground {ground!r}. Choose one of: {', '.join(sorted(GROUNDS))}, "
                    f"or pass a hex string."
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
    ) -> None:
        """Deposit one dab. Centre is in pixel coordinates and may be fractional.

        Everything outside the canvas is clipped away, so a stroke can safely run
        off the edge -- which is what a painter does at the border of a canvas.
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
            return
        sub = mask[sy0 : sy0 + (cy1 - cy0), sx0 : sx0 + (cx1 - cx0)]

        # Gating tooth: the surface height, roughened by the aperiodic grain.
        tooth = self.height_map[cy0:cy1, cx0:cx1] * 0.72 + self.grain[cy0:cy1, cx0:cx1] * 0.28
        wet = self.wetness[cy0:cy1, cx0:cx1]
        thick = self.thickness[cy0:cy1, cx0:cx1]
        dst = self.rgb[cy0:cy1, cx0:cx1]

        alpha = sub * float(np.clip(strength, 0.0, 1.0))

        # Canvas tooth gating. A full brush fills the valleys too; as the load runs
        # out, only the peaks still receive paint. This is where dry brush comes from.
        ts = float(np.clip(texture_sensitivity, 0.0, 1.0))
        if ts > 0.0:
            need = (1.0 - float(np.clip(load, 0.0, 1.0))) * ts
            band = 0.18
            gate = np.clip((tooth - need) / band, 0.0, 1.0)
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
            return

        self.rgb[cy0:cy1, cx0:cx1] = blend_wet(dst, color, effective)

        if not glaze:
            # A glaze is a thin film: it colours, but it does not build height.
            np.add(thick, alpha * float(thickness_gain), out=thick)
            np.clip(thick, 0.0, _MAX_THICKNESS, out=thick)

        np.maximum(wet, alpha * float(wetness_gain), out=wet)

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
        else:
            x0, y0, x1, y1 = self.region_px(region)
            self.wetness[y0:y1, x0:x1] *= 1.0 - a

    def tick_wetness(self) -> None:
        """Called once per stroke: paint dries slowly on its own."""
        self.wetness *= _WET_DECAY_PER_STROKE
        self.stroke_count += 1

    def region_px(self, region) -> tuple[int, int, int, int]:
        """Normalised region bounds to integer pixel bounds, clipped to the canvas."""
        bounds = getattr(region, "bounds", region)
        rx0, ry0, rx1, ry1 = (float(v) for v in bounds)
        x0 = int(np.clip(round(rx0 * self.width), 0, self.width))
        x1 = int(np.clip(round(rx1 * self.width), 0, self.width))
        y0 = int(np.clip(round(ry0 * self.height), 0, self.height))
        y1 = int(np.clip(round(ry1 * self.height), 0, self.height))
        return x0, y0, max(x1, x0 + 1), max(y1, y0 + 1)

    # -- export ----------------------------------------------------------------------
    def to_srgb8(self, impasto: bool = True) -> np.ndarray:
        """Render to an 8-bit sRGB array (h, w, 3), ready for PNG encoding.

        Args:
            impasto: shade the paint height as low relief, lit from the top-left.
                Subtle by design -- it should read as texture, not as embossing.
        """
        rgb = self.rgb
        if impasto and float(self.thickness.max()) > 1e-3:
            t = np.clip(self.thickness, 0.0, _MAX_THICKNESS)
            # Gradient of the paint surface; light from the upper left.
            gy, gx = np.gradient(t)
            relief = np.clip((gx + gy) * 0.35, -0.5, 0.5)
            rgb = np.clip(rgb * (1.0 + relief[..., None] * 0.30), 0.0, 1.0)
        return (linear_to_srgb(rgb) * 255.0 + 0.5).astype(np.uint8)

    def thumbnail_srgb8(self, max_side: int = 360) -> np.ndarray:
        """A small 8-bit sRGB view, for time-lapse frames.

        Downsamples in linear space *before* the sRGB conversion. Converting the
        full canvas and then shrinking it costs the same as a full export on every
        single stroke, which is most of the price of leaving the time-lapse on.
        """
        longest = max(self.width, self.height)
        step = max(1, int(np.ceil(longest / float(max(max_side, 1)))))
        if step == 1:
            return self.to_srgb8(impasto=False)
        # Box-average each block rather than point-sampling, so the thumbnail does
        # not alias the canvas weave into moire.
        h = (self.height // step) * step
        w = (self.width // step) * step
        blocks = self.rgb[:h, :w].reshape(h // step, step, w // step, step, 3)
        small = blocks.mean(axis=(1, 3))
        return (linear_to_srgb(small) * 255.0 + 0.5).astype(np.uint8)

    def values(self) -> np.ndarray:
        """The canvas as 8-bit greyscale: the value structure, the way a painter squints."""
        lum = luminance(self.rgb)
        return (linear_to_srgb(lum) * 255.0 + 0.5).astype(np.uint8)

    # -- state -----------------------------------------------------------------------
    def snapshot(self) -> dict[str, np.ndarray]:
        """A copy of every mutable channel, for undo."""
        return {
            "rgb": self.rgb.copy(),
            "wetness": self.wetness.copy(),
            "thickness": self.thickness.copy(),
            "stroke_count": np.int64(self.stroke_count),
        }

    def restore(self, snap: dict) -> None:
        """Restore a snapshot taken by :meth:`snapshot`."""
        self.rgb = np.array(snap["rgb"], dtype=np.float32, copy=True)
        self.wetness = np.array(snap["wetness"], dtype=np.float32, copy=True)
        self.thickness = np.array(snap["thickness"], dtype=np.float32, copy=True)
        self.stroke_count = int(snap["stroke_count"])

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return (
            f"Canvas({self.width}x{self.height}, texture={self.texture_name!r}, "
            f"ground={self.ground_name!r}, strokes={self.stroke_count})"
        )


def from_srgb_array(arr: np.ndarray) -> np.ndarray:
    """Helper for tests and reference loading: 8-bit sRGB to linear float32."""
    return srgb_to_linear(np.asarray(arr, dtype=np.float32) / 255.0)
