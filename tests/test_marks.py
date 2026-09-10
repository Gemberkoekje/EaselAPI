"""M7: what a mark looks like at the scale of a feature.

Three changes, and every one of them alters every stroke in the engine, so the
golden images are the gate and these are the properties underneath them:

* the bristle comb is drawn per *stroke*, so two marks with one brush are not the
  same mark, and its streaks have a width of their own rather than the brush's,
* width follows pressure on the round tips, so a lid line, a brow or a lash can
  taper in one stroke instead of two of different sizes,
* ``dab(press=n)`` stamps the same spot n times inside one mark.

Where a test could ask the API what it did, it asks the canvas instead.
"""

from __future__ import annotations

import numpy as np
import pytest

from easel import Session
from easel.brush import bristles_for, brush
from easel.canvas import Canvas
from easel.stroke import paint_stroke, press_width


def _bare_bristle(size: float = 0.12):
    """A bristle brush with everything but the comb turned off.

    Jitter, size jitter and the tooth all move a mark about; with them on, two
    strokes differ whether or not the comb does, and the test would pass on the
    engine it is meant to fail on.
    """
    return brush("bristle", size=size, jitter=0.0, size_jitter=0.0,
                 texture_sensitivity=0.0, load_falloff=0.0)


def _mark(b, index: int, size_px=(900, 600)) -> np.ndarray:
    """Paint one horizontal mark on a fresh canvas as stroke number ``index``."""
    c = Canvas(*size_px, texture="smooth", ground="warm_white", seed=3)
    before = c.rgb.copy()
    paint_stroke(c, [(0.08, 0.5), (0.92, 0.5)], b, "#FFFFFF", "even",
                 np.random.default_rng([3, index]))
    return np.abs(c.rgb - before).max(axis=2)


def _cross_section(deposit: np.ndarray, x0: int, x1: int) -> np.ndarray:
    col = deposit[:, x0:x1].mean(axis=1)
    ink = np.nonzero(col > col.max() * 0.12)[0]
    return col[ink[0] : ink[-1] + 1]


def _height(deposit: np.ndarray) -> int:
    rows = np.nonzero(deposit.max(axis=1) > 0.004)[0]
    return int(rows[-1] - rows[0] + 1) if len(rows) else 0


# --------------------------------------------------------------------------------------
# The comb
# --------------------------------------------------------------------------------------
def test_two_strokes_of_one_brush_do_not_print_the_same_comb():
    """REHEARSAL2.md, *Still open*: every wide bristle mark printed identical streaks."""
    b = _bare_bristle()
    first = _mark(b, 0)
    for index in (1, 2, 3):
        other = _mark(b, index)
        assert not np.array_equal(first, other), (
            f"stroke {index} printed exactly the same mark as stroke 0 -- "
            f"the brush is stamping one fixed comb again"
        )
    a = _cross_section(first, 380, 520)
    c = _cross_section(_mark(b, 2), 380, 520)
    n = min(len(a), len(c))
    assert float(np.corrcoef(a[:n], c[:n])[0, 1]) < 0.95, \
        "two strokes still comb the paint the same way"


def test_the_comb_holds_along_a_stroke():
    """It must vary between strokes and *not* within one: bristles do not shimmer."""
    deposit = _mark(_bare_bristle(), 0)
    near = _cross_section(deposit, 200, 260)
    far = _cross_section(deposit, 620, 680)
    n = min(len(near), len(far))
    assert float(np.corrcoef(near[:n], far[:n])[0, 1]) > 0.9, \
        "the striations move about along the stroke instead of staying put"


def test_a_bigger_brush_has_more_bristles_and_not_wider_ones():
    """A bristle is a physical thing. Nine times the brush, nine times the bristles."""
    pitch = brush("bristle").bristle_pitch
    counts = {size: bristles_for(size, pitch, size * 900) for size in (0.02, 0.06, 0.18)}
    assert counts[0.18] == pytest.approx(counts[0.02] * 9, rel=0.15)
    for size, n in counts.items():
        streak_px = size * 900 / n
        assert 3.0 < streak_px < 6.0, \
            f"a streak at size {size} is {streak_px:.1f}px; it should not follow the brush"


def test_the_comb_is_never_finer_than_the_pixels_it_is_drawn_on():
    """A comb below a pixel is not a comb, it is aliasing."""
    assert bristles_for(0.2, 0.0001, 12.0) <= 10
    assert bristles_for(0.001, 0.005, 400.0) == 3


def test_an_explicit_bristle_count_is_still_obeyed():
    b = brush("bristle", size=0.18, bristle_count=7)
    assert b.bristles(0.18 * 900) == 7


def test_a_negative_bristle_count_explains_itself():
    with pytest.raises(ValueError, match="bristle_count"):
        brush("bristle", bristle_count=-2)


# --------------------------------------------------------------------------------------
# Pressure and width
# --------------------------------------------------------------------------------------
def test_pressure_changes_the_width_of_a_round_mark():
    """REVIEW.md's open finding: 0.1 and 1.0 used to cover an identical bounding box."""
    b = brush("round_hard", size=0.06, jitter=0.0, size_jitter=0.0)
    heavy = _height(_mark(b, 0, (600, 400)))       # `_mark` paints at even pressure
    c = Canvas(600, 400, texture="smooth", ground="warm_white", seed=3)
    before = c.rgb.copy()
    paint_stroke(c, [(0.1, 0.5), (0.9, 0.5)], b, "#402010", 0.12,
                 np.random.default_rng([3, 0]))
    light = _height(np.abs(c.rgb - before).max(axis=2))
    assert light < heavy * 0.7, \
        f"a mark at pressure 0.12 is {light}px against {heavy}px at full pressure"


def test_a_taper_is_one_stroke_and_not_two_of_different_sizes():
    """The second rehearsal's eye test: a lid, a brow and a lash all taper."""
    c = Canvas(600, 400, texture="smooth", ground="warm_white", seed=3)
    before = c.rgb.copy()
    b = brush("liner", size=0.02)
    paint_stroke(c, [(0.1, 0.5), (0.9, 0.5)], b, "#402010", [1.0, 0.0],
                 np.random.default_rng([3, 0]))
    deposit = np.abs(c.rgb - before).max(axis=2)
    start = _height(deposit[:, 100:160])
    end = _height(deposit[:, 460:520])
    assert end < start * 0.6, f"the mark ends at {end}px having started at {start}px"


def test_a_light_touch_thins_a_fine_line_instead_of_dropping_it():
    """The floor of a pixel or two. Without it the dabs of a liner at a light
    pressure fall under the half-pixel guard in `paint_stroke` and the line is not
    thin, it is absent."""
    c = Canvas(600, 400, texture="smooth", ground="white", seed=3)
    before = c.rgb.copy()
    b = brush("liner", size=0.004)          # 2.4 px wide; 0.8 px at this pressure
    r = paint_stroke(c, [(0.1, 0.5), (0.9, 0.5)], b, "#101010", 0.05,
                     np.random.default_rng([3, 0]))
    deposit = np.abs(c.rgb - before).max(axis=2)
    assert r.paint > 0.0 and _height(deposit) >= 1, "a light touch left nothing at all"


def test_the_oriented_tips_keep_their_chisel():
    """Only the round tips follow pressure: a flat brush's width is the mass it lays."""
    for name in ("flat", "bristle", "knife"):
        b = brush(name, size=0.1, jitter=0.0, size_jitter=0.0)
        heavy = _height(_mark(b, 0, (600, 400)))
        c = Canvas(600, 400, texture="smooth", ground="warm_white", seed=3)
        before = c.rgb.copy()
        paint_stroke(c, [(0.1, 0.5), (0.9, 0.5)], b, "#402010", 0.2,
                     np.random.default_rng([3, 0]))
        light = _height(np.abs(c.rgb - before).max(axis=2))
        assert abs(light - heavy) <= 3, \
            f"{name} changed width with pressure: {heavy}px to {light}px"


def test_a_preview_reports_the_width_the_mark_will_have():
    b = brush("round_hard")
    assert press_width(b, "even") == pytest.approx(1.0)
    assert press_width(b, 0.2) < 0.6
    assert press_width(b, "taper", n=1) < 0.7, "a lone stamp only sees the start of a taper"
    assert press_width(brush("flat"), 0.2) == pytest.approx(1.0)


# --------------------------------------------------------------------------------------
# dab(press=n)
# --------------------------------------------------------------------------------------
def _session(tmp_path, **kw):
    return Session(400, 300, texture="smooth", ground="toned_grey", seed=4,
                   out_dir=tmp_path, timelapse=False, **kw)


def test_press_stamps_the_same_spot_and_costs_one_mark(tmp_path):
    s = _session(tmp_path)
    once = s.dab(0.3, 0.5, color="titanium_white", size=0.06)
    thrice = s.dab(0.7, 0.5, color="titanium_white", size=0.06, press=3)
    assert s.stroke_count == 2, "a pressed dab must cost one stroke, not three"
    assert (once.dabs, thrice.dabs) == (1, 3)
    assert thrice.paint > once.paint * 3, \
        "three stamps landed no more paint than three of the light first touch"
    assert len(thrice.points) == 1, "a pressed dab is still one point"


def test_a_pressed_dab_reaches_its_colour(tmp_path):
    """The brief's reason for `press`: one dab lands about a third of the way there."""
    white = np.asarray([1.0, 1.0, 1.0], dtype=np.float32)
    reach = []
    for press in (1, 3):
        s = _session(tmp_path)
        ground = s.canvas.rgb[150, 200].copy()
        s.dab(0.5, 0.5, color="titanium_white", size=0.08, press=press)
        got = s.canvas.rgb[150, 200]
        reach.append(float(np.mean((got - ground) / np.maximum(white - ground, 1e-6))))
    assert reach[0] < 0.4, f"one dab already lands {reach[0]:.2f} of the way to white"
    assert reach[1] > reach[0] * 1.8, f"three stamps only reached {reach[1]:.2f}"


def test_press_replays_and_survives_a_save(tmp_path):
    s = _session(tmp_path)
    s.stroke([(0.1, 0.4), (0.9, 0.45)], "bristle", "burnt_umber", size=0.1)
    s.dab(0.5, 0.5, color="titanium_white", size=0.05, press=4)
    painted = s.canvas.to_srgb8()

    assert np.array_equal(s.replay().canvas.to_srgb8(), painted)
    loaded = Session.load(s.save(tmp_path / "p.easel"))
    assert np.array_equal(loaded.replay().canvas.to_srgb8(), painted)


def test_a_log_written_before_press_replays_unchanged(tmp_path):
    """Default 1, so a record with no `press` key means one stamp -- as it always did."""
    s = _session(tmp_path)
    s.dab(0.5, 0.5, color="titanium_white", size=0.05)
    expected = s.canvas.to_srgb8()

    old = s.replay(upto=0)
    for record in s.history.records:
        record.params.pop("press", None)
    old.history = s.history
    assert np.array_equal(old.replay().canvas.to_srgb8(), expected)


def test_press_on_a_path_says_so(tmp_path):
    s = _session(tmp_path)
    with pytest.raises(ValueError, match="single point"):
        s.stroke([(0.2, 0.2), (0.8, 0.8)], "round_hard", "burnt_umber", press=3)


def test_press_below_one_says_so(tmp_path):
    s = _session(tmp_path)
    with pytest.raises(ValueError, match="press must be at least 1"):
        s.dab(0.5, 0.5, press=0)
