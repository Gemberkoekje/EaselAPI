"""Procedural canvas and paper textures.

A texture is a height map in 0..1 with a mean near 0.5. Paint deposition is
modulated by this height: a brush low on paint catches only the peaks, which is
where dry-brush comes from for free. Nothing here is decorative -- the texture is
load-bearing for how strokes read.
"""

from __future__ import annotations

import numpy as np

__all__ = ["TEXTURES", "make_texture", "value_noise", "fbm"]

#: Available canvas surfaces, in order of tooth.
TEXTURES = ("smooth", "linen", "rough")


def value_noise(shape: tuple[int, int], cells: int, rng: np.random.Generator) -> np.ndarray:
    """Smooth value noise: a random lattice, bilinearly interpolated with smoothstep."""
    h, w = shape
    cy = max(2, int(cells * h / max(w, 1)) + 1)
    cx = max(2, cells + 1)
    lattice = rng.random((cy, cx), dtype=np.float32)

    # Sample positions in lattice space.
    ys = np.linspace(0, cy - 1, h, dtype=np.float32)
    xs = np.linspace(0, cx - 1, w, dtype=np.float32)
    y0 = np.floor(ys).astype(np.int32)
    x0 = np.floor(xs).astype(np.int32)
    y1 = np.minimum(y0 + 1, cy - 1)
    x1 = np.minimum(x0 + 1, cx - 1)
    fy = (ys - y0)[:, None]
    fx = (xs - x0)[None, :]
    # Smoothstep so the lattice does not show as diamonds.
    fy = fy * fy * (3.0 - 2.0 * fy)
    fx = fx * fx * (3.0 - 2.0 * fx)

    top = lattice[np.ix_(y0, x0)] * (1 - fx) + lattice[np.ix_(y0, x1)] * fx
    bot = lattice[np.ix_(y1, x0)] * (1 - fx) + lattice[np.ix_(y1, x1)] * fx
    return (top * (1 - fy) + bot * fy).astype(np.float32)


def fbm(
    shape: tuple[int, int],
    rng: np.random.Generator,
    octaves: int = 5,
    base_cells: int = 8,
    gain: float = 0.5,
    lacunarity: float = 2.0,
) -> np.ndarray:
    """Fractal sum of value noise, normalised to 0..1."""
    total = np.zeros(shape, dtype=np.float32)
    amp = 1.0
    cells = base_cells
    norm = 0.0
    for _ in range(octaves):
        total += value_noise(shape, int(cells), rng) * amp
        norm += amp
        amp *= gain
        cells *= lacunarity
    total /= max(norm, 1e-6)
    return _normalise(total)


def _normalise(a: np.ndarray) -> np.ndarray:
    lo, hi = float(a.min()), float(a.max())
    if hi - lo < 1e-6:
        return np.full_like(a, 0.5)
    return ((a - lo) / (hi - lo)).astype(np.float32)


def make_texture(
    name: str, height: int, width: int, rng: np.random.Generator, strength: float = 1.0
) -> np.ndarray:
    """Build a height map for the named surface.

    Args:
        name: one of :data:`TEXTURES` -- ``"smooth"``, ``"linen"`` or ``"rough"``.
        height: canvas height in pixels.
        width: canvas width in pixels.
        rng: seeded generator, so the same seed gives the same weave.
        strength: scales the tooth. 0 gives a perfectly flat surface.

    Returns:
        float32 array (height, width) in 0..1, mean near 0.5.
    """
    key = name.lower()
    if key not in TEXTURES:
        raise ValueError(f"Unknown texture {name!r}. Choose one of: {', '.join(TEXTURES)}")

    shape = (height, width)
    long_side = max(height, width)

    if key == "smooth":
        # A gessoed panel: almost flat, with a faint roll from the priming.
        base = fbm(shape, rng, octaves=3, base_cells=6, gain=0.55)
        grain = value_noise(shape, max(24, long_side // 12), rng)
        h = 0.5 + (base - 0.5) * 0.35 + (grain - 0.5) * 0.18
        amplitude = 0.30

    elif key == "linen":
        # Woven threads: a warp and a weft, each with slight thread-to-thread variation.
        ys = np.arange(height, dtype=np.float32)[:, None]
        xs = np.arange(width, dtype=np.float32)[None, :]
        # Threads coarse enough to read as weave rather than as a moire screen.
        thread = max(4.5, long_side / 130.0)  # pixels per thread
        # Generous wobble: a perfectly periodic weave beats against the dab grid.
        wobble_y = (value_noise(shape, 22, rng) - 0.5) * thread * 1.6
        wobble_x = (value_noise(shape, 22, rng) - 0.5) * thread * 1.6
        warp = np.sin((xs + wobble_x) * (2 * np.pi / thread))
        weft = np.sin((ys + wobble_y) * (2 * np.pi / thread))
        # Over-under weave: the two threads alternate rather than simply adding.
        weave = np.maximum(warp, weft) * 0.5 + (warp * weft) * 0.25
        slubs = fbm(shape, rng, octaves=3, base_cells=10, gain=0.5)  # irregular thick threads
        h = 0.5 + weave * 0.5 + (slubs - 0.5) * 0.35
        amplitude = 0.62

    else:  # rough
        # Cold-press paper: pitted, with a wide range of hill sizes.
        base = fbm(shape, rng, octaves=6, base_cells=7, gain=0.55)
        pits = value_noise(shape, max(40, long_side // 7), rng)
        h = 0.5 + (base - 0.5) * 0.9 + (pits - 0.5) * 0.5
        h = np.clip(h, 0.0, 1.0)
        h = h**1.15  # bias toward valleys, so the tooth catches paint
        amplitude = 0.85

    h = _normalise(h)
    amp = float(np.clip(amplitude * strength, 0.0, 1.0))
    return np.clip(0.5 + (h - 0.5) * amp, 0.0, 1.0).astype(np.float32)
