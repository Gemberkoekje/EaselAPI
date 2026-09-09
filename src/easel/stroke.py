"""Strokes: a path, a brush, and a pressure profile, stamped as a run of dabs.

The path is smoothed with a Catmull-Rom spline, so three rough points become a
curve rather than two straight segments. That matters: a painter gives a gesture,
not a polyline, and perfectly straight lines are one of the fastest ways to make
an image look mechanical.

Paint runs out along a stroke. The brush starts with a load and spends it; as the
load drops, the canvas tooth starts to show through and the stroke breaks up on
its own. Nothing here special-cases dry brush -- it falls out of load plus tooth.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from easel.brush import Brush
from easel.canvas import Canvas
from easel.color import mix_many, parse_color

__all__ = ["PRESSURE_PROFILES", "StrokeResult", "paint_stroke", "catmull_rom", "pressure_curve"]

#: Named pressure profiles. Anything else can be given as a scalar or a list.
PRESSURE_PROFILES = ("taper", "press_in", "lift_off", "even", "swell", "dab")

# How many brush diameters a full load lasts, before falloff is applied.
_LOAD_DISTANCE_DIAMETERS = 10.0


@dataclass
class StrokeResult:
    """What a stroke actually did. Returned so the log can replay it exactly."""

    dabs: int
    length_px: float
    end_load: float
    bounds: tuple[float, float, float, float]  # normalised x0, y0, x1, y1

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return f"StrokeResult(dabs={self.dabs}, length={self.length_px:.0f}px, end_load={self.end_load:.2f})"


# --------------------------------------------------------------------------------------
# Path
# --------------------------------------------------------------------------------------
def catmull_rom(points: np.ndarray, samples_per_segment: int = 24) -> np.ndarray:
    """Smooth a polyline into a Catmull-Rom spline.

    Args:
        points: (n, 2) array of normalised coordinates.
        samples_per_segment: how finely each segment is subdivided.

    Returns:
        (m, 2) array of densely sampled points. A 1- or 2-point input is passed
        through unchanged, since there is no curve to fit.
    """
    p = np.asarray(points, dtype=np.float32)
    if p.ndim != 2 or p.shape[1] != 2:
        raise ValueError(f"Path must be an (n, 2) array of points, got shape {p.shape}")
    if len(p) < 3:
        return p

    # Duplicate the endpoints so the curve starts and ends where the painter asked.
    ext = np.vstack([p[0], p, p[-1]])
    t = np.linspace(0.0, 1.0, samples_per_segment, endpoint=False, dtype=np.float32)[:, None]
    t2, t3 = t * t, t * t * t

    p0, p1, p2, p3 = ext[:-3], ext[1:-2], ext[2:-1], ext[3:]
    out = []
    for i in range(len(p1)):
        a = 2.0 * p1[i]
        b = p2[i] - p0[i]
        c = 2.0 * p0[i] - 5.0 * p1[i] + 4.0 * p2[i] - p3[i]
        d = -p0[i] + 3.0 * p1[i] - 3.0 * p2[i] + p3[i]
        out.append(0.5 * (a + b * t + c * t2 + d * t3))
    out.append(p[-1][None, :])
    return np.vstack(out).astype(np.float32)


def _resample(path_px: np.ndarray, spacing_px: float):
    """Walk a dense path at fixed arc-length intervals.

    Returns (positions, angles, distances) where ``angles`` are the direction of
    travel in radians and ``distances`` are arc length from the start.
    """
    if len(path_px) == 1:
        return path_px.copy(), np.zeros(1, dtype=np.float32), np.zeros(1, dtype=np.float32)

    deltas = np.diff(path_px, axis=0)
    seg_len = np.hypot(deltas[:, 0], deltas[:, 1])
    cum = np.concatenate([[0.0], np.cumsum(seg_len)]).astype(np.float32)
    total = float(cum[-1])
    step = max(float(spacing_px), 0.5)

    if total < 1e-6:
        return path_px[:1].copy(), np.zeros(1, dtype=np.float32), np.zeros(1, dtype=np.float32)

    targets = np.arange(0.0, total + step * 0.5, step, dtype=np.float32)
    xs = np.interp(targets, cum, path_px[:, 0]).astype(np.float32)
    ys = np.interp(targets, cum, path_px[:, 1]).astype(np.float32)
    pos = np.stack([xs, ys], axis=1)

    # Direction of travel at each dab, from the neighbouring dabs.
    if len(pos) > 1:
        d = np.gradient(pos, axis=0)
        angles = np.arctan2(d[:, 1], d[:, 0]).astype(np.float32)
    else:
        angles = np.zeros(1, dtype=np.float32)
    return pos, angles, targets


# --------------------------------------------------------------------------------------
# Pressure
# --------------------------------------------------------------------------------------
def pressure_curve(pressure, n: int) -> np.ndarray:
    """Turn a pressure spec into ``n`` per-dab values in 0..1.

    Accepts a named profile from :data:`PRESSURE_PROFILES`, a scalar, or a list of
    values which are interpolated along the stroke.
    """
    if n <= 0:
        return np.zeros(0, dtype=np.float32)
    t = np.linspace(0.0, 1.0, n, dtype=np.float32) if n > 1 else np.zeros(1, dtype=np.float32)

    if isinstance(pressure, str):
        name = pressure.lower()
        if name == "taper":
            # Lands light, presses through the middle, lifts off. The default.
            # sin(pi) lands a hair below zero in float32, and a negative base with a
            # fractional exponent is NaN, so clamp before raising to a power.
            arch = np.clip(np.sin(np.pi * t), 0.0, 1.0)
            return (0.28 + 0.72 * arch**0.6).astype(np.float32)
        if name == "press_in":
            return (0.22 + 0.78 * t**0.7).astype(np.float32)
        if name == "lift_off":
            return (0.22 + 0.78 * (1.0 - t) ** 0.7).astype(np.float32)
        if name == "even":
            return np.ones(n, dtype=np.float32)
        if name == "swell":
            return (0.45 + 0.55 * np.sin(np.pi * t) ** 2).astype(np.float32)
        if name == "dab":
            return (1.0 - 0.85 * t**2).astype(np.float32)
        raise ValueError(
            f"Unknown pressure profile {pressure!r}. "
            f"Use one of {', '.join(PRESSURE_PROFILES)}, a number, or a list."
        )

    arr = np.atleast_1d(np.asarray(pressure, dtype=np.float32))
    if arr.size == 1:
        return np.full(n, float(np.clip(arr[0], 0.0, 1.0)), dtype=np.float32)
    src_t = np.linspace(0.0, 1.0, arr.size, dtype=np.float32)
    return np.clip(np.interp(t, src_t, arr), 0.0, 1.0).astype(np.float32)


# --------------------------------------------------------------------------------------
# Painting
# --------------------------------------------------------------------------------------
def _wander(rng: np.random.Generator, n: int, dims: int, span: int = 9) -> np.ndarray:
    """Smoothed unit-variance noise along a stroke: a slow wander, not white noise."""
    raw = rng.normal(0.0, 1.0, size=(n + span * 2, dims)).astype(np.float32)
    if n < 2 or span < 2:
        return raw[:n]
    kernel = np.hanning(span * 2 + 1).astype(np.float32)
    kernel /= np.sqrt(np.sum(kernel * kernel))  # keep unit variance after smoothing
    out = np.empty((n, dims), dtype=np.float32)
    for d in range(dims):
        out[:, d] = np.convolve(raw[:, d], kernel, mode="same")[span : span + n]
    return out



def paint_stroke(
    canvas: Canvas,
    points,
    brush: Brush,
    color,
    pressure="taper",
    rng: np.random.Generator | None = None,
    glaze: bool = False,
    smooth: bool = True,
) -> StrokeResult:
    """Stamp a stroke onto the canvas.

    Args:
        canvas: the surface to paint on.
        points: normalised (x, y) points, origin top-left. One point makes a dab.
        brush: the brush to use.
        color: any colour :func:`easel.color.parse_color` accepts.
        pressure: a named profile, a scalar, or a per-point list.
        rng: seeded generator. Required for a reproducible painting.
        glaze: deposit colour without building paint height.
        smooth: fit a spline through the points. Turn this off for a deliberate
            hard-cornered mark.

    Returns:
        A :class:`StrokeResult` describing what was stamped.
    """
    rng = rng if rng is not None else np.random.default_rng(0)
    pts = np.atleast_2d(np.asarray(points, dtype=np.float32))
    if pts.shape[1] != 2:
        raise ValueError(f"Points must be (n, 2) normalised coordinates, got shape {pts.shape}")

    base_color = parse_color(color)
    path = catmull_rom(pts) if (smooth and len(pts) >= 3) else pts

    # Normalised to pixels. Brush size is a fraction of the canvas long side.
    px = np.empty_like(path)
    px[:, 0] = path[:, 0] * (canvas.width - 1)
    px[:, 1] = path[:, 1] * (canvas.height - 1)

    diameter = max(brush.size * canvas.long_side, 1.5)
    radius = diameter * 0.5
    # Spacing is measured against the tip's extent *along travel*, not its width. A
    # flat or knife tip is thin in that direction, so spacing it like a round tip
    # leaves visible gaps between stamps and the stroke reads as a picket fence.
    along = diameter if brush.tip in ("round_soft", "round_hard") else diameter * brush.aspect
    spacing_px = max(brush.spacing * max(along, diameter * 0.12), 1.0)

    pos, angles, dists = _resample(px, spacing_px)
    n = len(pos)
    press = pressure_curve(pressure, n)

    # Per-dab randomness, drawn once so the stroke is reproducible.
    #
    # The wobble is *smoothed* along the stroke rather than drawn independently per
    # dab. Independent noise makes neighbouring dabs clump and gap, which shows up
    # as banding at the dab frequency; a slow wander gives the organic, slightly
    # uneven edge a real brush leaves, without the ripple.
    jitter_xy = _wander(rng, n, 2) * (brush.jitter * diameter)
    size_var = 1.0 + _wander(rng, n, 1)[:, 0] * (brush.size_jitter * 0.5)
    size_var = np.clip(size_var, 0.45, 1.7)

    # Paint load spends itself over the stroke, measured in brush diameters travelled.
    consumed = dists / max(diameter * _LOAD_DISTANCE_DIAMETERS, 1e-5)
    load = np.clip(brush.load * np.exp(-brush.load_falloff * consumed), 0.0, 1.0)

    carried = base_color.copy()
    pickup = 0.45 if brush.smudge > 0.0 else 0.0

    # How readily the brush picks up wet paint it is dragged through.
    #
    # This is what makes wet-into-wet actually behave like wet-into-wet. Merely
    # reducing a dab's alpha over wet paint is algebraically the same as using a
    # smaller alpha, so a hundred overlapping dabs still converge on the pure
    # colour and the stroke ends up looking exactly like one laid on dry canvas.
    # A real brush dragged through wet paint comes away carrying a mixture, and
    # everything it lays down after that is contaminated. That is modelled here.
    #
    # The brush also keeps delivering paint from its own reservoir, and that part
    # matters just as much: contamination on its own accumulates without bound, so
    # a stroke drags whatever it first touched across the whole canvas and washes
    # out to the ground colour. With replenishment the carried colour settles at a
    # stable mixture within a few dabs instead of drifting.
    WET_PICKUP = 0.15
    BRUSH_REFRESH = 0.25

    min_x = min_y = 1.0
    max_x = max_y = 0.0
    stamped = 0

    for i in range(n):
        cx = float(pos[i, 0] + jitter_xy[i, 0])
        cy = float(pos[i, 1] + jitter_xy[i, 1])
        r = radius * float(size_var[i])
        if r < 0.6:
            continue
        # Split the centre into a whole pixel and a sub-pixel phase; the phase is
        # baked into the stamp so dabs are not all snapped to the pixel grid.
        ix = math.floor(cx)
        iy = math.floor(cy)
        mask = brush.mask(r, float(angles[i]), cx - ix, cy - iy)

        if brush.smudge > 0.0:
            sampled = canvas.sample(float(ix), float(iy), mask)
            if float(sampled.sum()) > 0.0:
                carried = mix_many([carried, sampled], [1.0 - pickup, pickup])
            dab_color = (
                carried
                if brush.smudge >= 1.0
                else mix_many([base_color, carried], [1.0 - brush.smudge, brush.smudge])
            )
        else:
            # Sample at the *leading edge* of the tip, not under its centre.
            # Consecutive dabs overlap by ~95%, so a brush sampling under itself
            # only ever tastes the paint it just laid down and never picks up what
            # it is being dragged through. The front of the tip is where it meets
            # wet paint.
            lead_x = cx + math.cos(float(angles[i])) * r
            lead_y = cy + math.sin(float(angles[i])) * r
            wet_here = canvas.wetness_at(lead_x, lead_y)
            if wet_here > 0.03:
                sampled = canvas.sample(float(math.floor(lead_x)),
                                        float(math.floor(lead_y)), mask)
                if float(sampled.sum()) > 0.0:
                    take = float(np.clip(wet_here * WET_PICKUP, 0.0, 0.9))
                    carried = mix_many([carried, sampled], [1.0 - take, take])
                carried = mix_many([carried, base_color],
                                   [1.0 - BRUSH_REFRESH, BRUSH_REFRESH])
            else:
                # Dry canvas: the brush carries exactly what it was loaded with, so
                # painting on dry ground is unchanged by any of this.
                carried = base_color
            dab_color = carried

        ld = float(load[i])
        # As the paint runs out the mark gets thinner as well as more broken.
        strength = brush.opacity * float(press[i]) * (0.35 + 0.65 * ld)

        canvas.stamp(
            float(ix),
            float(iy),
            mask,
            dab_color,
            strength=strength,
            load=ld,
            wetness_gain=brush.wetness,
            thickness_gain=brush.thickness_gain * ld,
            texture_sensitivity=brush.texture_sensitivity,
            glaze=glaze,
        )
        stamped += 1

        nx, ny = cx / max(canvas.width - 1, 1), cy / max(canvas.height - 1, 1)
        rn = r / canvas.long_side
        min_x, max_x = min(min_x, nx - rn), max(max_x, nx + rn)
        min_y, max_y = min(min_y, ny - rn), max(max_y, ny + rn)

    canvas.tick_wetness()

    if stamped == 0:
        return StrokeResult(0, 0.0, float(brush.load), (0.0, 0.0, 0.0, 0.0))
    return StrokeResult(
        dabs=stamped,
        length_px=float(dists[-1]) if len(dists) else 0.0,
        end_load=float(load[-1]) if len(load) else float(brush.load),
        bounds=(
            float(np.clip(min_x, 0.0, 1.0)),
            float(np.clip(min_y, 0.0, 1.0)),
            float(np.clip(max_x, 0.0, 1.0)),
            float(np.clip(max_y, 0.0, 1.0)),
        ),
    )


def stroke_angle(points) -> float:
    """Overall direction of a path in radians. Useful for orienting a flat brush."""
    p = np.atleast_2d(np.asarray(points, dtype=np.float32))
    if len(p) < 2:
        return 0.0
    return float(math.atan2(p[-1, 1] - p[0, 1], p[-1, 0] - p[0, 0]))
