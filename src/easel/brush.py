"""Brushes: procedural tip masks plus the dynamics that make a stroke look painted.

A brush is a *tip mask* (a small float32 stamp) plus a set of dynamics. Strokes are
made by stamping the tip along a path -- the same approach MyPaint and Krita use.
There is no fluid simulation here and there is not meant to be.

Tip masks are built in a local frame where ``u`` runs along the direction of travel
and ``v`` runs across it. A flat or bristle brush is short in ``u`` and wide in
``v``, so its striations smear into streaks along the stroke. That is where the
painterly quality comes from, so the bristle tip gets the most attention.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field, replace

import numpy as np

__all__ = ["Brush", "BRUSHES", "brush", "TIPS", "tip_mask", "bristles_for"]

#: Tip shapes available to :class:`Brush`.
TIPS = ("round_soft", "round_hard", "flat", "bristle", "knife")

# Angles are quantised before a mask is built, so a curved stroke reuses masks
# instead of rebuilding one per dab. 10 degrees is fine enough not to show.
_ANGLE_STEP_DEG = 10.0
_MASK_CACHE: dict[tuple, np.ndarray] = {}
_MASK_CACHE_LIMIT = 16384
# Sub-pixel phases per axis. Dab centres are placed to this fraction of a pixel.
_SUBPIXEL_STEPS = 4
#: Radius quantisation, in steps per pixel. Every quantity a mask is built from has
#: to be in its cache key, or the cache hands back a mask built for a different
#: brush. This one was keyed on ``ceil(radius)`` while the mask was computed from
#: the exact radius, so a tip at r=5.9 got whatever r=5.1 had built earlier in the
#: process -- and the painting a script produced depended on what had run before it
#: in the same interpreter. The general rule is trap 5 in ``LESSONS.md``.
_RADIUS_STEPS = 4

#: The width of one bristle streak, as a fraction of the canvas long side, when a
#: brush does not pin its own :attr:`Brush.bristle_count`. A bristle is a physical
#: thing: a wider brush holds *more* of them, not fatter ones. The comb used to be
#: a fixed count across the tip, so its streaks scaled with the brush -- 3 px at
#: ``size=0.02`` and 26 px at ``size=0.18`` on a 900 px canvas,
#: which is why a big quiet mass came out as corduroy and a detail stroke carried
#: the brush's pattern rather than the feature's. The default is set so that the
#: `bristle` preset at its own default size keeps the 22 bristles it always had.
BRISTLE_PITCH = 0.005
#: No bristle narrower than this, in pixels. Below about a pixel the comb stops
#: being a comb and becomes aliasing noise, which is worse than no comb at all.
_MIN_BRISTLE_PX = 1.2

#: How far a fully wobbled round tip reaches off its own radius, either way. The
#: stamp is built this much larger so the outline has room to swell into, and the
#: silhouette is drawn to the same figure so a wobbled mark keeps the *size* it was
#: asked for on average rather than quietly shrinking below it.
_WOBBLE_REACH = 0.35


@dataclass(frozen=True)
class Brush:
    """A brush: what shape it is, and how it behaves as it moves.

    Sizes are **normalised**: ``size`` is the tip diameter as a fraction of the
    canvas long side, so a brush behaves the same on any canvas.

    Attributes:
        name: label used in the stroke log and the sampler sheet.
        tip: one of :data:`TIPS`.
        size: tip diameter as a fraction of the canvas long side (0..1).
        opacity: paint opacity at full pressure and full load.
        hardness: 0 is a soft airbrushed edge, 1 is a cut edge.
        spacing: distance between dabs, as a fraction of the tip extent *along the
            direction of travel*. For a round tip that is the diameter; for a flat,
            bristle or knife tip it is ``aspect * diameter``, since those tips are
            thin in the direction they move. Above ~0.5 the dabs read as beads;
            below ~0.05 strokes get expensive for no visible gain.
        jitter: random offset per dab, as a fraction of tip diameter.
        size_jitter: random per-dab size variation (0..1). A little of this stops
            every stroke from having an identical edge.
        load: how much paint the brush picks up. It runs out along a stroke.
        load_falloff: how fast the load runs out. 0 means never.
        angle_follow: rotate the tip to the direction of travel.
        angle: fixed tip angle in degrees, used when ``angle_follow`` is False.
        aspect: tip thickness along travel, as a fraction of its width. Only used
            by the non-round tips.
        wetness: how wet the deposited paint is (0..1).
        thickness_gain: how much paint height a full-strength dab adds.
        smudge: how much colour the brush picks up from the canvas and drags. 0
            paints pure colour, 1 only moves what is already there.
        texture_sensitivity: how strongly canvas tooth gates deposition. Higher
            values give a drier, more broken stroke on rough surfaces.
        bristle_count: number of bristles for the bristle tip. ``0``, the default,
            derives it from ``size`` and ``bristle_pitch``, so a bigger brush has
            more streaks rather than wider ones. Set it to pin a comb.
        bristle_pitch: the width of one bristle streak, as a fraction of the canvas
            long side. Ignored when ``bristle_count`` is set.
        bristle_seed: fixes the striation pattern for a given brush. The comb is
            also varied per *stroke* (see :func:`easel.stroke.paint_stroke`); this
            seed is what the variation is drawn around.
        tip_wobble: how far the tip's own silhouette wanders off a disc, as a
            fraction of its radius. ``0``, the default, is the disc every round mark
            in every painting made before this was. Above it the outline is redrawn
            **per stroke**, the way the bristle comb is, so five marks are five
            silhouettes rather than five copies of one -- which is what a small
            irregular mark is, and what the box otherwise has exactly one tip for.
            Only the round tips take it: a ``flat`` or a ``knife`` is a chisel, and
            its rectangle is the mass it lays.
    """

    name: str = "round"
    tip: str = "round_soft"
    size: float = 0.06
    opacity: float = 0.9
    hardness: float = 0.5
    spacing: float = 0.12
    jitter: float = 0.02
    size_jitter: float = 0.06
    load: float = 1.0
    load_falloff: float = 0.55
    angle_follow: bool = True
    angle: float = 0.0
    aspect: float = 1.0
    wetness: float = 0.85
    thickness_gain: float = 0.5
    smudge: float = 0.0
    texture_sensitivity: float = 0.6
    bristle_count: int = 0
    bristle_pitch: float = BRISTLE_PITCH
    bristle_seed: int = 0
    tip_wobble: float = 0.0
    meta: dict = field(default_factory=dict, compare=False, repr=False)

    def __post_init__(self) -> None:
        if self.tip not in TIPS:
            raise ValueError(f"Unknown tip {self.tip!r}. Choose one of: {', '.join(TIPS)}")
        if not 0.0 < self.size <= 1.0:
            raise ValueError(f"size must be in (0, 1], got {self.size}")
        if self.spacing <= 0.0:
            raise ValueError(f"spacing must be > 0, got {self.spacing}")
        if self.bristle_count < 0:
            raise ValueError(
                f"bristle_count must be >= 0, got {self.bristle_count}. "
                f"0 derives the comb from the brush's size."
            )
        if self.bristle_pitch <= 0.0:
            raise ValueError(f"bristle_pitch must be > 0, got {self.bristle_pitch}")
        if not 0.0 <= self.tip_wobble <= 1.0:
            raise ValueError(
                f"tip_wobble is how far the tip's silhouette wanders off a disc, as "
                f"a fraction of its radius: 0 to 1, got {self.tip_wobble}."
            )

    def scaled(self, factor: float) -> Brush:
        """A copy of this brush at a different size. ``scaled(0.5)`` is half as wide."""
        return replace(self, size=float(np.clip(self.size * factor, 1e-4, 1.0)))

    def with_(self, **changes) -> Brush:
        """A copy with dynamics overridden: ``bristle.with_(opacity=0.4)``."""
        return replace(self, **changes)

    # -- mask ---------------------------------------------------------------------
    def mask(
        self,
        radius_px: float,
        angle_rad: float,
        frac_x: float = 0.0,
        frac_y: float = 0.0,
        comb: int = 0,
        count: int | None = None,
        wobble_seed: int = 0,
    ) -> np.ndarray:
        """The tip stamp for this brush at a given radius, direction and sub-pixel phase.

        Args:
            comb: which comb to print, for the bristle tip. A stroke draws one of
                these and uses it for all of its dabs, so the striations stay put
                along the stroke and differ from the next stroke's.
            count: how many bristles across the tip. A stroke works this out once
                from the brush's nominal size; left out, it is derived here from
                the radius asked for.
            wobble_seed: which silhouette to print, for a round tip carrying
                :attr:`tip_wobble`. Drawn once per stroke, like ``comb``, and for
                the same reason: a brush picked up again is not the brush it was.
        """
        return tip_mask(
            tip=self.tip,
            radius_px=radius_px,
            angle_rad=angle_rad if self.angle_follow else math.radians(self.angle),
            hardness=self.hardness,
            aspect=self.aspect,
            bristle_count=(
                count if count is not None
                else bristles_for(self.size, self.bristle_pitch,
                                  radius_px * 2.0, self.bristle_count)
            ),
            bristle_seed=self.bristle_seed,
            frac_x=frac_x,
            frac_y=frac_y,
            comb=comb,
            wobble=self.tip_wobble,
            wobble_seed=wobble_seed,
        )

    def bristles(self, diameter_px: float) -> int:
        """How many bristles this brush combs a stroke into, at ``diameter_px`` wide."""
        return bristles_for(self.size, self.bristle_pitch, diameter_px, self.bristle_count)


def bristles_for(size: float, pitch: float, diameter_px: float, count: int = 0) -> int:
    """How many bristles a tip of ``size`` combs a stroke into.

    A bristle has a width of its own: ``pitch``, as a fraction of the canvas long
    side. A wider brush therefore holds more of them rather than fatter ones, which
    is what keeps a big mass from printing corduroy and a small mark from carrying
    the brush's signature instead of the feature's. ``count``, when non-zero, pins
    the comb and ignores the pitch.

    Never fewer than three -- two bristles is not a comb -- and never so many that
    one would be drawn narrower than :data:`_MIN_BRISTLE_PX`, where the comb stops
    reading as bristles and starts reading as noise.
    """
    n = int(count) if int(count) > 0 else int(round(float(size) / max(float(pitch), 1e-6)))
    limit = int(max(3.0, float(diameter_px) / _MIN_BRISTLE_PX))
    return int(min(max(n, 3), max(limit, 3)))


def tip_mask(
    tip: str,
    radius_px: float,
    angle_rad: float,
    hardness: float,
    aspect: float = 1.0,
    bristle_count: int = 22,
    bristle_seed: int = 0,
    frac_x: float = 0.0,
    frac_y: float = 0.0,
    comb: int = 0,
    wobble: float = 0.0,
    wobble_seed: int = 0,
) -> np.ndarray:
    """Build (and cache) a tip stamp as a float32 array in 0..1.

    The returned array is square with an odd side length, so it has a true centre.

    ``frac_x`` / ``frac_y`` shift the stamp by a sub-pixel amount, quantised to
    :data:`_SUBPIXEL_STEPS` phases per axis. Without this, dab centres snap to whole
    pixels and the dab spacing beats against the pixel grid, striping every stroke
    made with a thin tip.

    ``comb`` picks which set of bristles the tip has -- their spacing, where they
    sit across the tip, and which of them are missing. It is part of the cache key,
    so a stroke that draws one comb and holds it prints the same striations from
    end to end while the next stroke prints different ones.

    ``wobble`` and ``wobble_seed`` are the same idea for a round tip's outline: how
    far it wanders off a disc, and which wander. Both are in the key, and at
    ``wobble=0`` -- every preset in the box -- the stamp is the disc it always was.
    """
    # Quantise the radius *before* anything is computed from it, so that the mask is
    # a pure function of the cache key. A quarter of a pixel is finer than the
    # sub-pixel phase, so nothing visible is given up.
    r_steps = max(_RADIUS_STEPS, int(round(float(radius_px) * _RADIUS_STEPS)))
    r = r_steps / _RADIUS_STEPS
    is_round = tip in ("round_soft", "round_hard")
    # A wobbled silhouette swells as well as bites, so the stamp is built with room
    # for the swell. Without it the far side of the outline would be cut off square
    # by the edge of its own array, which is a chisel end on a mark that exists to
    # not have one.
    wob = float(np.clip(wobble, 0.0, 1.0)) if is_round else 0.0
    ri = int(math.ceil(r * (1.0 + _WOBBLE_REACH * wob)))
    # Round tips are rotation-invariant, so collapse their angle to one cache entry.
    if is_round:
        angle_bucket = 0
    else:
        steps = int(360 / _ANGLE_STEP_DEG)
        angle_bucket = int(round(math.degrees(angle_rad) / _ANGLE_STEP_DEG)) % steps

    px_phase = int(round(float(frac_x) * _SUBPIXEL_STEPS)) % _SUBPIXEL_STEPS
    py_phase = int(round(float(frac_y) * _SUBPIXEL_STEPS)) % _SUBPIXEL_STEPS

    key = (
        tip,
        r_steps,
        angle_bucket,
        px_phase,
        py_phase,
        round(float(hardness), 2),
        round(float(aspect), 3),
        int(bristle_count),
        int(bristle_seed),
        int(comb),
        round(wob, 3),
        int(wobble_seed) if wob > 0.0 else 0,
    )
    cached = _MASK_CACHE.get(key)
    if cached is not None:
        return cached

    n = 2 * ri + 1
    base = np.arange(n, dtype=np.float32) - ri
    lin_x = (base - px_phase / _SUBPIXEL_STEPS) / r
    lin_y = (base - py_phase / _SUBPIXEL_STEPS) / r
    yy, xx = np.meshgrid(lin_y, lin_x, indexing="ij")

    theta = angle_bucket * _ANGLE_STEP_DEG * math.pi / 180.0
    ct, st = math.cos(theta), math.sin(theta)
    # u runs along the direction of travel, v runs across it.
    u = xx * ct + yy * st
    v = -xx * st + yy * ct

    hard = float(np.clip(hardness, 0.0, 0.999))
    # Edge softness in normalised units; at least one pixel, so nothing aliases.
    edge = max((1.0 - hard) * 0.9, 1.0 / r)

    if is_round:
        d = np.sqrt(u * u + v * v)
        limit = 1.0 if wob <= 0.0 else _wobbled_edge(u, v, wob, wobble_seed)
        mask = _falloff(d, limit, edge)
    elif tip == "knife":
        # A blade: thin rectangle with almost no give at the edges.
        blade_edge = max(0.06 * (1.0 - hard) + 0.02, 1.0 / r)
        mask = _falloff(np.abs(u), max(aspect, 1e-3), max(aspect * 0.9, blade_edge))
        mask = mask * _falloff(np.abs(v), 1.0, blade_edge)
    else:  # flat and bristle share a rectangular body
        # The along-travel edge gets a soft ramp scaled to the tip thickness. A thin
        # tip with a hard u-edge lays down a row of discrete bars as it advances,
        # which reads as machine stripes; a soft ramp lets consecutive dabs merge.
        # A full-width ramp (no flat top) in u: overlapping triangular profiles sum
        # to a near-constant coverage, where a plateau profile ripples at the dab
        # frequency and stripes the stroke.
        u_edge = max(aspect, 1.0 / r)
        mask = _falloff(np.abs(u), max(aspect, 1e-3), u_edge)
        mask = mask * _falloff(np.abs(v), 1.0, edge * 0.5)
        if tip == "bristle":
            mask = mask * _bristle_profile(v, bristle_count, bristle_seed, comb)

    mask = np.clip(mask, 0.0, 1.0).astype(np.float32)
    if len(_MASK_CACHE) > _MASK_CACHE_LIMIT:  # pragma: no cover - only on huge sessions
        _MASK_CACHE.clear()
    _MASK_CACHE[key] = mask
    return mask


def _falloff(dist: np.ndarray, limit: float, edge: float) -> np.ndarray:
    """1 inside ``limit``, ramping smoothly to 0 over a band of width ``edge``."""
    t = (limit - dist) / max(edge, 1e-5)
    t = np.clip(t, 0.0, 1.0)
    return (t * t * (3.0 - 2.0 * t)).astype(np.float32)


def _wobbled_edge(u: np.ndarray, v: np.ndarray, wobble: float, seed: int) -> np.ndarray:
    """Where a round tip's outline sits, angle by angle: a disc that has been handled.

    Three low harmonics round the tip, drawn from ``seed``. Low, because what is
    wanted is a silhouette with a couple of lobes and a flat side -- the shape of a
    loaded brush set down once -- and not a crinkle, which at the size these marks
    are made reads as noise on the edge rather than as a shape.

    It swells as far as it bites, so the mark keeps its nominal size: the alternative
    is an outline that only ever takes radius away, and then a painter who asks for
    an irregular mark gets a smaller one and has to find that out by measuring it.
    """
    rng = np.random.default_rng([7717, int(seed)])
    ang = np.arctan2(v, u)
    harm = np.zeros_like(ang)
    for k in (1, 2, 3):
        amplitude = float(rng.uniform(0.4, 1.0))
        phase = float(rng.uniform(0.0, 2.0 * math.pi))
        harm += amplitude * np.sin(k * ang + phase)
    # Three sines of amplitude up to one sum to at most three and typically to about
    # half that; scaled here so the usual wander fills the reach and an occasional
    # one is clipped by it rather than running past the stamp it is drawn in.
    harm = np.clip(harm / 1.6, -1.0, 1.0)
    return (1.0 + _WOBBLE_REACH * float(wobble) * harm).astype(np.float32)


def _bristle_profile(v: np.ndarray, count: int, seed: int, comb: int = 0) -> np.ndarray:
    """Per-bristle alpha across the tip width.

    The pattern is fixed for a given ``(seed, comb)``, so striations stay put along a
    stroke the way real bristles do, rather than shimmering from dab to dab. What
    changes between strokes is ``comb``: the brush is picked up again, and its
    spacing, where the comb sits across the tip, and which bristles are missing are
    all drawn afresh. Without that, every wide bristle mark in a painting printed
    the identical set of streaks and masses went to corduroy.
    """
    rng = np.random.default_rng([1000 + int(seed), int(comb)])
    # Spacing: the comb is not the same width every time the brush is picked up.
    n = max(3, int(round(max(3, int(count)) * float(rng.uniform(0.86, 1.16)))))
    # Phase: where the comb sits across the tip, in bristles. Decides which bristle
    # lands on the edge of the mark, which is most of what an edge looks like.
    phase = float(rng.uniform(0.0, 1.0))

    top = n + 1
    strengths = rng.uniform(0.45, 1.0, size=top + 1).astype(np.float32)
    # Some bristles are missing or splayed. These gaps are what read as dry brush.
    gaps = rng.random(top + 1) < 0.22
    if gaps.any():
        strengths[gaps] *= rng.uniform(0.0, 0.25, size=int(gaps.sum())).astype(np.float32)
    # Bristles cluster slightly rather than sitting on a perfect comb.
    offsets = rng.uniform(-0.4, 0.4, size=top + 1).astype(np.float32)

    idx_f = (v + 1.0) * 0.5 * (n - 1) + phase
    base = np.clip(idx_f.astype(np.int32), 0, top)
    idx = np.clip(np.round(idx_f + offsets[base]), 0, top).astype(np.int32)
    return strengths[idx]


# --------------------------------------------------------------------------------------
# Presets
# --------------------------------------------------------------------------------------
#: Named brushes. One line each on what they are for -- see PAINTER.md.
BRUSHES: dict[str, Brush] = {
    # Soft round: blending, soft edges, glazes. The least painterly; use sparingly.
    "round_soft": Brush(
        name="round_soft",
        tip="round_soft",
        size=0.06,
        hardness=0.2,
        opacity=0.75,
        spacing=0.09,
        jitter=0.015,
        load=1.0,
        load_falloff=0.35,
        angle_follow=False,
        wetness=0.9,
        thickness_gain=0.35,
        texture_sensitivity=0.35,
    ),
    # Hard round: deliberate marks, dots, small accents, drawing-like strokes.
    "round_hard": Brush(
        name="round_hard",
        tip="round_hard",
        size=0.045,
        hardness=0.85,
        opacity=0.95,
        spacing=0.07,
        jitter=0.02,
        size_jitter=0.03,
        load=1.0,
        load_falloff=0.5,
        angle_follow=False,
        wetness=0.8,
        thickness_gain=0.55,
        texture_sensitivity=0.5,
    ),
    # Liner: fine lines at feature scale -- the sharpest, thinnest mark in a picture.
    # Nothing new in the engine: lines render at their nominal width down to about
    # three pixels (there is a test), so this is one word for what
    # otherwise takes four overrides on round_hard. No jitter of any kind, because
    # at this size a jitter of two per cent of the canvas *is* the line.
    "liner": Brush(
        name="liner",
        tip="round_hard",
        size=0.005,
        hardness=1.0,
        opacity=0.95,
        spacing=0.05,
        jitter=0.0,
        size_jitter=0.0,
        load=1.0,
        load_falloff=0.18,
        angle_follow=False,
        wetness=0.6,
        thickness_gain=0.35,
        texture_sensitivity=0.35,
    ),
    # Flat: block-in, clean chisel edges, planes. Rotates to follow the stroke.
    "flat": Brush(
        name="flat",
        tip="flat",
        size=0.1,
        hardness=0.75,
        opacity=0.9,
        spacing=0.09,
        jitter=0.02,
        size_jitter=0.07,
        load=1.0,
        load_falloff=0.6,
        angle_follow=True,
        aspect=0.26,
        wetness=0.85,
        thickness_gain=0.65,
        texture_sensitivity=0.65,
    ),
    # Bristle: the workhorse. Broken, streaky, alive. Reach for this first.
    "bristle": Brush(
        name="bristle",
        tip="bristle",
        size=0.11,
        hardness=0.65,
        opacity=0.88,
        spacing=0.09,
        jitter=0.03,
        size_jitter=0.1,
        load=0.9,
        load_falloff=0.55,
        angle_follow=True,
        aspect=0.3,
        wetness=0.85,
        thickness_gain=0.8,
        texture_sensitivity=0.95,
    ),
    # Palette knife: flat slabs of thick paint with a hard edge; drags what it meets.
    "knife": Brush(
        name="knife",
        tip="knife",
        size=0.09,
        hardness=0.97,
        opacity=1.0,
        spacing=0.09,
        jitter=0.005,
        size_jitter=0.03,
        load=1.0,
        load_falloff=1.1,
        angle_follow=True,
        aspect=0.18,
        wetness=0.6,
        thickness_gain=1.0,
        smudge=0.35,
        texture_sensitivity=0.25,
    ),
    # Smudge: carries no paint of its own; picks up the canvas and drags it.
    "smudge": Brush(
        name="smudge",
        tip="round_soft",
        size=0.07,
        hardness=0.25,
        opacity=0.6,
        spacing=0.06,
        jitter=0.01,
        load=1.0,
        load_falloff=0.0,
        angle_follow=False,
        wetness=0.95,
        thickness_gain=0.0,
        smudge=1.0,
        texture_sensitivity=0.3,
    ),
}


def brush(name: str, **overrides) -> Brush:
    """Look up a preset by name, optionally overriding dynamics.

    Example::

        b = brush("bristle", size=0.2, opacity=0.6)
    """
    key = name.lower()
    if key not in BRUSHES:
        raise KeyError(f"Unknown brush {name!r}. Available: {', '.join(sorted(BRUSHES))}")
    b = BRUSHES[key]
    return b.with_(**overrides) if overrides else b
