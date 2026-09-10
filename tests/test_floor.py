"""M8b: the Kubelka-Munk reflectance floor, kept out of the picture.

The floor exists so the mixing arithmetic behaves (finding 5: without it a
near-zero channel's K/S swamps every mixture and red + blue comes out green). It
had also become a floor on the *result*, because `blend_wet` clipped both colours
into the K/S band and never took the clip back off. Two things followed, and both
are tested here:

* a canvas pixel below the floor was rounded up to it by any dab whose square
  bounding box it fell in -- with no paint landing on it at all, and
* a colour below the floor could not be laid as written at any opacity.

The tests that matter most are the ones asserting nothing happens: paint that is
not landing must not change the pixel it is not landing on.
"""

from __future__ import annotations

import numpy as np
import pytest

from easel import Session
from easel.brush import BRUSHES
from easel.canvas import Canvas
from easel.color import (
    _FLOOR,
    _outside_band,
    blend_wet,
    linear_to_srgb,
    mix,
    mix_many,
    parse_color,
)
from easel.palette import PIGMENTS, Palette

#: Colours outside the K/S band, which is where the clip used to bite. `cadmium_yellow`
#: is the one shipped pigment with a channel under the floor (blue, 0.006).
BELOW_THE_FLOOR = ["#000000", "#010101", "#FFC012", "#02030A"]

#: What "returns the canvas untouched" is allowed to mean in linear light. The blend
#: puts the mixture back together as ``mixed + (dst - mixed)``, and where `dst` is far
#: under the floor those two are too far apart for the subtraction to cancel bit for
#: bit in float32. Measured at 4.7e-10 over the colour cube, which is nothing in the
#: eight bits that reach the PNG -- the tests below check that separately and exactly.
CANCELS_TO = 1e-8


def srgb8(linear) -> np.ndarray:
    """The 0..255 numbers that actually reach the PNG."""
    return np.round(linear_to_srgb(np.asarray(linear, dtype=np.float32)) * 255.0).astype(int)


# --------------------------------------------------------------------------------------
# Paint that is not landing must not change anything
# --------------------------------------------------------------------------------------
def test_zero_amount_returns_the_canvas_untouched():
    """`amount` of 0 is "no paint here", and the pixel must not move.

    `Canvas.stamp` writes `blend_wet` back over a dab's whole square bounding box,
    most of which is outside the round tip and has an amount of exactly zero. Anything
    that moves there is the engine repainting pixels the brush never touched, which is
    what this whole phase is about.
    """
    rng = np.random.default_rng(7)
    dst = rng.uniform(0.0, 1.0, size=(16, 16, 3)).astype(np.float32)
    dst[0, 0] = 0.0                                     # true black, under the floor
    dst[0, 1] = [0.002, 0.5, 0.999]                     # one channel under it
    dst[0, 2] = 1.0                                     # and one at the ceiling
    out = blend_wet(dst, parse_color("#C08A2E"), np.zeros((16, 16), dtype=np.float32))
    assert np.allclose(out, dst, rtol=0.0, atol=CANCELS_TO)
    assert np.array_equal(srgb8(out), srgb8(dst)), "the exported pixel must not move at all"


def test_zero_amount_does_not_drift_when_it_is_repeated():
    """The identity has to hold under repetition, not just once.

    A pixel sits under the bounding box of every dab that passes near it -- thousands
    of them over a painting. The first version of this fix measured the clip against
    `np.clip` rather than against what the K/S round trip actually returns, which left
    a constant 1.7e-6 gap in one direction on every blend: sub-floor pixels leaked
    downward, and a near-black went 23 levels adrift over 5000 dabs. It is not enough
    for the blend to be nearly an identity; the error has to cancel rather than add.
    """
    src = parse_color("#C08A2E")
    dst = np.random.default_rng(1).uniform(0.0, 1.0, size=(24, 24, 3)).astype(np.float32)
    dst[0] = 0.0                                        # under the floor
    dst[1] = _FLOOR                                     # exactly on it, which used to creep
    zero = np.zeros((24, 24), dtype=np.float32)

    x = dst.copy()
    for _ in range(2000):
        x = blend_wet(x, src, zero)
    assert np.array_equal(srgb8(x), srgb8(dst))
    assert float(np.abs(x - dst).max()) < 1e-5, f"drifted by {float(np.abs(x - dst).max()):.2e}"


def test_a_dab_does_not_lift_the_black_in_its_bounding_box():
    """The reproduction from REVIEW.md's open entry, through the engine.

    A `round_soft` tip is a circle; its mask is a square. The corners of that square
    are zero, so a black pixel there used to come away at sRGB 25 -- a visible grey,
    from a dab whose mask value at that pixel is 0.0.
    """
    c = Canvas(64, 64, texture="smooth", ground="#FFFFFF", seed=0)
    c.rgb[:] = 0.0
    mask = BRUSHES["round_soft"].mask(radius_px=12.0, angle_rad=0.0)
    corner = 8, 8                                        # inside the box, outside the tip
    offset = corner[0] - (20 - mask.shape[0] // 2)
    assert mask[offset, offset] == 0.0, "the fixture must aim at a pixel the tip misses"

    c.stamp(20.0, 20.0, mask, parse_color("#C08A2E"), strength=1.0, load=1.0,
            wetness_gain=0.9, thickness_gain=0.0, texture_sensitivity=0.0)
    assert np.array_equal(c.rgb[corner], np.zeros(3, dtype=np.float32))


def test_the_lift_at_a_soft_edge_is_proportional_to_what_lands():
    """Where paint *is* landing, thinly, it moves the pixel thinly.

    The floor used to make the first thousandth of a dab worth as much as the last:
    every amount above zero arrived at sRGB 25-ish on black. The curve now starts at
    the canvas colour and rises with the paint.
    """
    dst = np.zeros((1, 1, 3), dtype=np.float32)
    src = parse_color("#C08A2E")
    lifts = [int(srgb8(blend_wet(dst, src, np.full((1, 1), a, dtype=np.float32))[0, 0])[0])
             for a in (0.0, 1e-4, 1e-3, 1e-2, 0.05, 0.5)]
    assert lifts[0] == 0
    assert lifts == sorted(lifts), f"lift must not go backwards: {lifts}"
    assert lifts[3] <= 2, f"a hundredth of a dab moved black by {lifts[3]} of 255"


# --------------------------------------------------------------------------------------
# A colour below the floor can be laid as written
# --------------------------------------------------------------------------------------
@pytest.mark.parametrize("hexval", BELOW_THE_FLOOR)
def test_full_strength_paint_lands_as_written(hexval):
    """`amount` of 1 is "all of this colour, here", and the colour arrives.

    The same `mixed + (want - mixed)` cancellation as at the other end, so the same
    two assertions: exact in the eight bits that reach the PNG, and to within
    `CANCELS_TO` in linear light.
    """
    want = parse_color(hexval)
    dst = np.tile(parse_color("#F3EDE1"), (4, 4, 1))
    got = blend_wet(dst, want, np.ones((4, 4), dtype=np.float32))
    assert np.array_equal(srgb8(got), srgb8(np.broadcast_to(want, got.shape))), \
        f"{hexval}: asked for {srgb8(want)}, got {srgb8(got[0, 0])}"
    assert np.allclose(got, want, rtol=0.0, atol=CANCELS_TO), hexval


def test_a_stroke_can_reach_black():
    """Through the whole engine, not just the blend: a painter asking for black.

    The engine has no black pigment on purpose, but a painter who supplies one has
    to get it. This used to bottom out at sRGB 25 whatever was painted.
    """
    s = Session(96, 96, texture="smooth", ground="warm_white", seed=3, timelapse=False)
    s.block_in("all", brush="flat", color="#000000", density=1.0, size=0.3)
    s.block_in("all", brush="flat", color="#000000", density=1.0, size=0.3)
    darkest = int(srgb8(s.canvas.rgb).min())
    assert darkest < 8, f"the darkest pixel painted with black is sRGB {darkest}"


@pytest.mark.parametrize("name", sorted(set(PIGMENTS)))
def test_every_pigment_lays_the_colour_its_swatch_states(name):
    """The swatch and the canvas have to be the same colour.

    M6b held the darks to the stronger rule of being written at or above the floor,
    because a channel under it rendered as the floor and `value_of` would then
    disagree with the paint. That rule was a workaround for this defect: the check
    worth making is not where a swatch is written but whether the engine can lay it,
    and `cadmium_yellow` -- whose blue is under the floor and always has been --
    now passes it.
    """
    p = Palette()
    want = parse_color(PIGMENTS[name])
    dst = np.tile(parse_color("#F3EDE1"), (2, 2, 1))
    got = blend_wet(dst, want, np.ones((2, 2), dtype=np.float32))[0, 0]
    assert np.array_equal(srgb8(got), srgb8(want)), (
        f"{name} states {p.hex(want)} and lays {p.hex(got)}"
    )


# --------------------------------------------------------------------------------------
# The mixing model the floor is there for
# --------------------------------------------------------------------------------------
def test_the_canvas_and_the_palette_are_the_same_mixture():
    """`blend_wet` is `mix_many` on two colours, per pixel, and has to stay that way.

    The palette's number is what the painter reads before committing a stroke; the
    canvas's pixel is what the stroke does. If they drift, neither can be trusted
    (finding 16, from the other direction). Includes a colour outside the K/S band,
    which is the case that could have made them drift.
    """
    rng = np.random.default_rng(11)
    for _ in range(8):
        a = rng.uniform(0.0, 1.0, size=3).astype(np.float32)
        b = rng.uniform(0.0, 1.0, size=3).astype(np.float32)
        for t in (0.0, 0.15, 0.5, 0.85, 1.0):
            on_canvas = blend_wet(np.tile(a, (1, 1, 1)), b,
                                  np.full((1, 1), t, dtype=np.float32))[0, 0]
            on_palette = mix_many([a, b], [1.0 - t, t])
            assert np.array_equal(srgb8(on_canvas), srgb8(on_palette))
            assert np.allclose(on_canvas, on_palette, rtol=0.0, atol=1e-5)

    yellow = parse_color(PIGMENTS["cadmium_yellow"])       # blue is under the floor
    blue = parse_color(PIGMENTS["ultramarine"])
    on_canvas = blend_wet(np.tile(yellow, (1, 1, 1)), blue,
                          np.full((1, 1), 0.5, dtype=np.float32))[0, 0]
    assert np.array_equal(srgb8(on_canvas), srgb8(mix(yellow, blue, 0.5)))


def test_mixing_a_colour_with_nothing_returns_that_colour():
    """A zero-weight ingredient must not change the answer, at either end.

    `mix("cadmium_yellow", anything, 0.0)` used to come back seven levels of blue
    lighter than cadmium yellow, because the clip was applied to the ingredients and
    never taken off the mixture.
    """
    for hexval in BELOW_THE_FLOOR + ["#3355AA", "#F7F4EF"]:
        c = parse_color(hexval)
        # A colour inside the K/S band is left exactly where this engine has always
        # left it: the round trip and nothing else, which is why no existing painting
        # moved. One outside the band is what this phase is about, and is held tighter.
        tol = 1e-5 if not _outside_band(c) else CANCELS_TO
        for got in (mix(c, "#3355AA", 0.0), mix("#3355AA", c, 1.0)):
            assert np.allclose(got, c, rtol=0.0, atol=tol), hexval
            assert np.array_equal(srgb8(got), srgb8(c)), hexval


def test_the_floor_still_keeps_red_plus_blue_violet():
    """Finding 5, which is what the floor is for, and finding 6 beside it.

    The clip is still applied to the K/S arithmetic; only its effect on the answer
    is now weighted by how much of each ingredient is in the mixture. So the
    mixtures the floor and the exponent were tuned against must not have moved.
    """
    p = Palette()
    r, g, b = (float(v) for v in p.mix("cadmium_red", "ultramarine", 0.5))
    assert r > g and b > g, f"red + blue should lean violet, got {p.hex(p.mix('cadmium_red', 'ultramarine', 0.5))}"

    r, g, b = (float(v) for v in p.mix("cadmium_yellow", "ultramarine", 0.5))
    assert g > r and g > b, "yellow + blue should lean green"

    assert p.value_of(p.mix("ultramarine", "titanium_white", 0.5)) - \
        p.value_of("ultramarine") > 0.15, "white should still tint"

    assert p.value_of(p.mix("ultramarine", "burnt_umber", 0.5)) < 0.15, "the dark should still be dark"


def test_a_below_floor_colour_does_not_swamp_a_mixture():
    """The reason the floor cannot simply be lowered, checked from the other side.

    Un-clipping the *result* is safe; un-clipping the arithmetic is not. A pigment
    with a near-zero channel still has to mix like paint rather than dominating,
    so black mixed half and half with white must land as a mid grey and not as black.
    """
    p = Palette()
    grey = mix("#000000", "#F7F4EF", 0.5)
    assert 0.25 < p.value_of(grey) < 0.75, f"black + white 0.5 reads {p.value_of(grey):.3f}"
    assert float(np.ptp(grey)) < 0.05, f"black + white should stay neutral, got {p.hex(grey)}"


def test_the_engine_still_cannot_paint_a_negative_reflectance():
    """Whatever the clip puts back, the result stays a colour."""
    rng = np.random.default_rng(3)
    dst = rng.uniform(0.0, 0.02, size=(32, 32, 3)).astype(np.float32)
    for hexval in BELOW_THE_FLOOR:
        for a in (0.0, 0.001, 0.4, 1.0):
            out = blend_wet(dst, parse_color(hexval), np.full((32, 32), a, dtype=np.float32))
            assert out.dtype == np.float32
            assert float(out.min()) >= 0.0 and float(out.max()) <= 1.0
            assert np.isfinite(out).all()


def test_work_inside_the_band_is_bit_for_bit_what_it_was():
    """Nothing that stays inside the K/S band may move, at all.

    This is what lets every painting made before this phase replay into the same
    pixels: the correction is not "small" for in-band work, it is *absent*, because
    `_outside_band` says there is nothing to correct. Checked against the pre-M8b
    formula written out in full rather than against a stored number, so it cannot
    quietly become "close enough".

    The corpus agrees: the seven golden images, `samples/brushes.png`,
    `samples/shapes.png` and both real paintings in `m7/repaint.py` come back byte
    for byte identical (`m8b/README.md`).
    """
    def pre_m8b(dst, src, amount):
        from easel.color import _INV_MIX_EXPONENT, _from_ks, _ks_pow, _to_ks
        a = amount[..., None].astype(np.float32)
        src_b = np.broadcast_to(np.asarray(src, dtype=np.float32), dst.shape)
        return _from_ks((_ks_pow(_to_ks(dst)) * (1.0 - a)
                         + _ks_pow(_to_ks(src_b)) * a) ** _INV_MIX_EXPONENT)

    rng = np.random.default_rng(19)
    # Every pigment on the palette is in band except cadmium_yellow, and so is every
    # reflectance this model produces, so this is what ordinary painting looks like.
    dst = rng.uniform(float(_FLOOR), 1.0 - 1e-4, size=(32, 32, 3)).astype(np.float32)
    for name in ("burnt_umber", "ultramarine", "titanium_white", "yellow_ochre"):
        src = parse_color(PIGMENTS[name])
        for amount in (np.zeros((32, 32), dtype=np.float32),
                       rng.uniform(0.0, 1.0, size=(32, 32)).astype(np.float32),
                       np.ones((32, 32), dtype=np.float32)):
            assert np.array_equal(blend_wet(dst, src, amount), pre_m8b(dst, src, amount)), name


def test_the_floor_is_still_where_finding_5_put_it():
    """A guard on the constant itself: this phase moved the clip's *effect*, not it."""
    assert float(_FLOOR) == pytest.approx(0.01)
