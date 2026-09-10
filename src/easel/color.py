"""Colour handling: sRGB <-> linear conversion and pigment-style subtractive mixing.

All pixel work inside Easel happens in **linear-light float32 RGB** in the range
0..1. Conversion to sRGB happens once, at export.

Mixing naive RGB averages turns every mixture grey-brown, which is the single
fastest way to make a painting look like clip-art. Easel therefore mixes in
Kubelka-Munk absorption/scattering space (single-constant approximation), which
keeps blue + yellow leaning green instead of sliding to grey.

The Kubelka-Munk arithmetic needs a reflectance floor to behave (see ``_FLOOR``),
but that floor is not allowed to become a floor on what can be painted: the clip is
taken back off the mixture in proportion to how much of each ingredient is in it, so
mixing nothing into a colour returns that colour unchanged.

Known limit of the single-constant model: white is a weaker lightener here than
real titanium white, which is a strong scatterer. Mixing 50/50 with white lightens
less than you would expect on a real palette -- reach for a higher white ratio, or
use :meth:`easel.palette.Palette.tint`.

If the optional ``pymixbox`` package is installed *and* its licence suits your
project, Easel will use it instead -- it is a better model. See the note in
:func:`mix` about why it is not a hard dependency.
"""

from __future__ import annotations

import numpy as np

__all__ = [
    "srgb_to_linear",
    "linear_to_srgb",
    "parse_color",
    "mix",
    "mix_many",
    "luminance",
    "linear_to_oklab",
    "MIXBOX_AVAILABLE",
]

# --------------------------------------------------------------------------------------
# Optional Mixbox backend
# --------------------------------------------------------------------------------------
# NOTE ON LICENCE: the reference Mixbox implementation is distributed under a
# CC BY-NC licence (non-commercial). Easel is MIT, so Mixbox is an *opt-in extra*
# rather than a dependency: `pip install easel-paint[mixbox]`. Without it, the
# built-in Kubelka-Munk approximation below is used, which is cruder but free of
# licence entanglement. Set EASEL_DISABLE_MIXBOX=1 to force the built-in model.
try:  # pragma: no cover - depends on optional install
    import os

    if os.environ.get("EASEL_DISABLE_MIXBOX"):
        raise ImportError
    import mixbox as _mixbox

    MIXBOX_AVAILABLE = True
except Exception:  # pragma: no cover
    _mixbox = None
    MIXBOX_AVAILABLE = False


# --------------------------------------------------------------------------------------
# Transfer functions
# --------------------------------------------------------------------------------------
def srgb_to_linear(x: np.ndarray) -> np.ndarray:
    """Convert sRGB-encoded values in 0..1 to linear light."""
    x = np.asarray(x, dtype=np.float32)
    return np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4).astype(np.float32)


def linear_to_srgb(x: np.ndarray) -> np.ndarray:
    """Convert linear-light values in 0..1 to sRGB encoding."""
    x = np.clip(np.asarray(x, dtype=np.float32), 0.0, 1.0)
    return np.where(x <= 0.0031308, x * 12.92, 1.055 * x ** (1 / 2.4) - 0.055).astype(np.float32)


def luminance(linear_rgb: np.ndarray) -> np.ndarray:
    """Rec. 709 relative luminance of linear RGB. Accepts (...,3)."""
    rgb = np.asarray(linear_rgb, dtype=np.float32)
    return (0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]).astype(np.float32)


#: Linear sRGB to the LMS cone space Oklab is built on, and the cube-root stage
#: after it. Constants from Bjorn Ottosson's derivation.
_OKLAB_M1 = np.array(
    [[0.4122214708, 0.5363325363, 0.0514459929],
     [0.2119034982, 0.6806995451, 0.1073969566],
     [0.0883024619, 0.2817188376, 0.6299787005]], dtype=np.float32)
_OKLAB_M2 = np.array(
    [[0.2104542553, 0.7936177850, -0.0040720468],
     [1.9779984951, -2.4285922050, 0.4505937099],
     [0.0259040371, 0.7827717662, -0.8086757660]], dtype=np.float32)


def linear_to_oklab(linear_rgb: np.ndarray) -> np.ndarray:
    """Linear RGB to Oklab. Accepts (..., 3).

    A perceptual space, so that "these two areas are the same colour" means what a
    painter means by it. Euclidean distance in sRGB does not: it puts two dark
    browns further apart than a dark brown and a mid grey, which is how an
    automatic segmentation ends up cutting a coat along its folds.
    """
    rgb = np.asarray(linear_rgb, dtype=np.float32)
    lms = rgb @ _OKLAB_M1.T
    lms = np.cbrt(np.maximum(lms, 0.0), dtype=np.float32)
    return (lms @ _OKLAB_M2.T).astype(np.float32)


# --------------------------------------------------------------------------------------
# Colour parsing
# --------------------------------------------------------------------------------------
def parse_color(value) -> np.ndarray:
    """Coerce a colour into linear-light float32 RGB.

    Accepts:

    * ``"#rrggbb"`` / ``"#rgb"`` hex strings (interpreted as sRGB),
    * a named pigment from :mod:`easel.palette` (e.g. ``"ultramarine"``),
    * a 3-tuple/list/ndarray of 0..1 floats (interpreted as sRGB), or
    * an existing linear ndarray of shape (3,) produced by Easel itself.
    """
    if isinstance(value, np.ndarray) and value.dtype == np.float32 and value.shape == (3,):
        return value
    if isinstance(value, str):
        s = value.strip()
        if s.startswith("#"):
            return srgb_to_linear(_hex_to_rgb(s))
        from easel.palette import PIGMENTS  # local import avoids a cycle

        key = s.lower().replace(" ", "_")
        if key in PIGMENTS:
            return srgb_to_linear(_hex_to_rgb(PIGMENTS[key]))
        raise ValueError(
            f"Unknown colour {value!r}. Use a hex string like '#3355aa', an (r, g, b) "
            f"tuple, or one of the pigment names: {', '.join(sorted(PIGMENTS))}"
        )
    arr = np.asarray(value, dtype=np.float32)
    if arr.shape != (3,):
        raise ValueError(f"Colour must have 3 components, got shape {arr.shape}")
    return srgb_to_linear(np.clip(arr, 0.0, 1.0))


def _hex_to_rgb(s: str) -> np.ndarray:
    s = s.lstrip("#")
    if len(s) == 3:
        s = "".join(c * 2 for c in s)
    if len(s) != 6:
        raise ValueError(f"Bad hex colour: #{s}")
    return np.array([int(s[i : i + 2], 16) / 255.0 for i in (0, 2, 4)], dtype=np.float32)


# --------------------------------------------------------------------------------------
# Pigment mixing
# --------------------------------------------------------------------------------------
# Reflectance floor. This is not just a divide-by-zero guard: real pigments never
# absorb a channel completely, and a hard zero makes that channel's K/S explode and
# swamp every mixture (cadmium red + ultramarine comes out dark green instead of
# violet). 0.01 is the smallest floor that keeps mixtures behaving like paint.
#
# It is a floor on the *mixing arithmetic* and nowhere else. It used to be a floor
# on the answer too, because the clip was applied to each ingredient and never taken
# back off: mixing a colour with nothing returned the clipped colour, so a channel
# below 0.01 could not be laid however opaquely it was painted, and -- worse -- a
# canvas pixel below 0.01 was rounded up to it by any dab whose *bounding box* it
# fell in, with no paint landing on it at all. `_solo` and `_unclip` below put that
# part back, weighted the same way the mixture is, so the floor keeps finding 5 fixed
# without deciding how dark the picture is allowed to go.
_FLOOR = np.float32(0.01)
_EPS = np.float32(1e-4)

# Mixtures are combined as a power mean of K/S with this exponent, rather than a
# plain (p=1) arithmetic mean.
#
# Why: single-constant Kubelka-Munk treats white as just another reflectance, but
# real titanium white is a powerful scatterer that dominates a mixture well beyond
# its volume share. At p=1 a 50/50 white mix barely lightens, which is wrong and
# actively misleading to paint with. A lower exponent gives white its real tinting
# strength while leaving the mixtures that matter behaving like paint: yellow + blue
# stays olive, red + blue stays violet, and nothing collapses toward grey.
#
# How this number is set: white must carry a 50/50 mixture about a quarter of the
# way up the palette's own value range. That is what p=0.5 did for the old, much
# lighter pigments (0.235 of the range). Darkening the masstones (M6b) widened the
# range from 0.73 to 0.83 and left p=0.5 crossing only 0.158 of it -- finding 6's
# complaint coming back by the back door, with nothing about white changed. p=0.35
# puts it at 0.234, and the named mixes land where they did: cerulean + white at
# 0.7 goes 0.698 -> 0.707, the ultramarine/burnt-sienna cool grey 0.567 -> 0.555.
# Lower than this and yellow + blue loses its green and goes brown, which is one of
# the two mixtures the exponent exists to protect.
_MIX_EXPONENT = np.float32(0.35)


#: The exponent's inverse, precomputed: the power mean weights ``K/S ** p`` and then
#: raises the weighted sum back by ``1 / p``.
_INV_MIX_EXPONENT = np.float32(1.0 / float(_MIX_EXPONENT))


def _to_ks(reflectance: np.ndarray) -> np.ndarray:
    """Kubelka-Munk K/S from reflectance (single-constant approximation)."""
    r = np.clip(reflectance, _FLOOR, 1.0 - _EPS)
    return ((1.0 - r) ** 2) / (2.0 * r)


def _ks_pow(ks: np.ndarray) -> np.ndarray:
    """``K/S ** p``, the space the power mean averages in.

    Split out so ``mix_many`` and ``blend_wet`` cannot drift apart: the palette's
    number and the canvas's pixel have to be the same mixture or neither can be
    trusted (REVIEW.md finding 16, from the other direction).
    """
    return np.power(ks, _MIX_EXPONENT, dtype=np.float32)


def _from_ks(ks: np.ndarray) -> np.ndarray:
    """Invert K/S back to reflectance."""
    ks = np.maximum(ks, 0.0)
    return np.clip(1.0 + ks - np.sqrt(ks * ks + 2.0 * ks), 0.0, 1.0).astype(np.float32)


def _solo(ks_p: np.ndarray) -> np.ndarray:
    """What the K/S round trip does to one ingredient on its own: the weight-1 mixture.

    Equal to the ingredient itself for anything inside the K/S band, but only to
    within a few parts in a million -- ``_to_ks`` and ``_from_ks`` are not exact
    inverses in float32, and neither is raising to ``p`` and back. Outside the band
    it is the clipped colour instead, which is the whole point.
    """
    return _from_ks(ks_p ** _INV_MIX_EXPONENT)


def _outside_band(colors: np.ndarray) -> bool:
    """Whether the K/S clip actually bites on any channel of ``colors``.

    When it does not -- which is every pigment on the palette but one, and every
    reflectance this model produces -- the correction below is identically the
    float32 round trip and nothing else, a few parts in a million. Testing for that
    costs two reductions; computing it costs a pow and a square root over the whole
    dab, on every dab of every stroke. Skipping it also keeps this engine bit for bit
    where it was for work that never leaves the band, which is what lets a painting
    made before this phase replay into the same pixels.
    """
    return bool(colors.min() < _FLOOR or colors.max() > 1.0 - _EPS)


def _unclip(mixed: np.ndarray, offset: np.ndarray) -> np.ndarray:
    """Put back what the K/S round trip took off the ingredients, weighted as they were.

    ``offset`` is each ingredient's own ``c - _solo(c)`` averaged by the *same*
    weights the mixture used. For a colour outside the K/S band that is the clip,
    carried through the mix in proportion to how much of that colour is actually
    there -- the floor stays where the mixing arithmetic needs it and stops being a
    floor on the result.

    Measuring the offset against ``_solo`` rather than against ``np.clip`` directly
    is what makes the ends *exact*, and it is not a nicety. The K/S round trip lands
    a hair below its own input, so an offset that ignored it would leave
    ``amount = 0`` short by that hair -- and a pixel under the floor would then be
    clipped up, offset back down past where it started, and leak a little further on
    every dab whose bounding box it fell in. Measured at 1.7e-6 per blend, one
    direction, no convergence: 5000 dabs took a near-black 23 levels adrift. Against
    ``_solo`` the two cancel to within 5e-10 at either end. The last of that is
    ``mixed + (c - mixed)`` rounding, where a colour far under the floor and the floor
    itself are too far apart to cancel bit for bit in float32; it is nothing in the
    eight bits that reach the PNG, and unlike the leak it does not accumulate.
    """
    return np.clip(mixed + offset, 0.0, 1.0).astype(np.float32)


def mix(a, b, ratio: float = 0.5) -> np.ndarray:
    """Mix two colours like paint. ``ratio`` is the proportion of ``b``.

    ``mix(x, y, 0.0)`` is ``x``; ``mix(x, y, 1.0)`` is ``y``.
    """
    ca, cb = parse_color(a), parse_color(b)
    t = float(np.clip(ratio, 0.0, 1.0))
    return mix_many([ca, cb], [1.0 - t, t])


def mix_many(colors, weights=None) -> np.ndarray:
    """Mix N linear-RGB colours with optional weights, in pigment space."""
    cols = np.stack([parse_color(c) for c in colors]).astype(np.float32)
    if weights is None:
        w = np.full(len(cols), 1.0 / len(cols), dtype=np.float32)
    else:
        w = np.asarray(weights, dtype=np.float32)
        total = float(w.sum())
        w = w / total if total > 0 else np.full(len(cols), 1.0 / len(cols), dtype=np.float32)

    if MIXBOX_AVAILABLE:  # pragma: no cover - optional path
        srgb = [linear_to_srgb(c) * 255.0 for c in cols]
        latents = [np.asarray(_mixbox.rgb_to_latent(tuple(s)), dtype=np.float32) for s in srgb]
        blended = np.sum(np.stack(latents) * w[:, None], axis=0)
        out = np.asarray(_mixbox.latent_to_rgb(tuple(blended.tolist())), dtype=np.float32) / 255.0
        return srgb_to_linear(out)

    ks = _ks_pow(_to_ks(cols))
    mixed = _from_ks(np.sum(ks * w[:, None], axis=0) ** _INV_MIX_EXPONENT)
    if not _outside_band(cols):
        return mixed
    return _unclip(mixed, np.sum((cols - _solo(ks)) * w[:, None], axis=0))


def blend_wet(dst: np.ndarray, src: np.ndarray, amount: np.ndarray) -> np.ndarray:
    """Per-pixel pigment blend used by wet-into-wet painting.

    ``dst`` is (h, w, 3) linear RGB already on the canvas, ``src`` is the incoming
    colour (3,) or (h, w, 3), and ``amount`` is (h, w) in 0..1 giving how much of
    the incoming paint displaces what is there.

    This is :func:`mix_many` on two colours weighted ``1 - amount`` and ``amount``,
    per pixel, and has to stay that way: the palette's number and the canvas's pixel
    are the same mixture or neither can be trusted. The ends hold to the eighth bit
    of the export -- ``amount`` of 0 returns ``dst`` and 1 lays ``src`` -- which
    matters because :meth:`easel.canvas.Canvas.stamp` blends a dab's whole square
    bounding box, most of which is outside the tip and has an ``amount`` of zero.
    """
    a = amount[..., None].astype(np.float32)
    inv_a = np.float32(1.0) - a
    # The incoming colour is one colour per stroke and not one per pixel in every call
    # the engine itself makes, so its K/S conversion is worked out on the (3,) colour
    # and left to broadcast rather than done per pixel.
    src_c = np.asarray(src, dtype=np.float32)
    ks_src = _ks_pow(_to_ks(src_c))
    ks_dst = _ks_pow(_to_ks(dst))
    mixed = _from_ks((ks_dst * inv_a + ks_src * a) ** _INV_MIX_EXPONENT)

    # Each side is corrected only if the clip bites on it. A pixel that settles a hair
    # *under* the floor is caught by this test on the next dab and pinned there, so it
    # cannot creep down a millionth at a time.
    terms = []
    if _outside_band(src_c):
        terms.append((src_c - _solo(ks_src)) * a)
    if _outside_band(dst):
        terms.append((dst - _solo(ks_dst)) * inv_a)
    if not terms:
        return mixed
    return _unclip(mixed, terms[0] if len(terms) == 1 else terms[0] + terms[1])
