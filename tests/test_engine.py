"""Property tests for the engine.

Three properties matter most, and they are the ones the brief calls out:

* strokes never write outside the canvas,
* undo restores exact state,
* replay from the log reproduces the export byte for byte.

Everything else here guards a specific bug that was actually hit while building.
"""

from __future__ import annotations

import subprocess
import sys

import numpy as np
import pytest

from easel import Session
from easel.brush import BRUSHES, brush, tip_mask
from easel.canvas import Canvas
from easel.color import linear_to_srgb, mix, parse_color, srgb_to_linear
from easel.history import History
from easel.palette import Palette
from easel.regions import Region, cell, region
from easel.stroke import PRESSURE_PROFILES, catmull_rom, paint_stroke, pressure_curve
from easel.texture import TEXTURES, make_texture


# --------------------------------------------------------------------------------------
# Canvas and bounds
# --------------------------------------------------------------------------------------
def test_canvas_channels_are_initialised():
    c = Canvas(64, 48, texture="linen", ground="toned_grey", seed=1)
    assert c.rgb.shape == (48, 64, 3)
    assert c.rgb.dtype == np.float32
    assert c.wetness.shape == (48, 64)
    assert c.thickness.shape == (48, 64)
    assert np.all(c.wetness == 0)
    assert 0.0 <= float(c.height_map.min()) and float(c.height_map.max()) <= 1.0


@pytest.mark.parametrize("name", sorted(BRUSHES))
def test_strokes_never_write_outside_the_canvas(name):
    """A stroke may run off the edge; it must not raise or corrupt memory."""
    s = Session(96, 72, seed=3, timelapse=False)
    # Deliberately absurd coordinates, well outside 0..1 in both directions.
    s.stroke([(-0.6, -0.4), (0.5, 0.5), (1.7, 1.4)], brush=name, color="cadmium_red")
    assert s.canvas.rgb.shape == (72, 96, 3)
    assert np.isfinite(s.canvas.rgb).all()
    assert float(s.canvas.rgb.min()) >= 0.0
    assert float(s.canvas.rgb.max()) <= 1.0


def test_stroke_entirely_off_canvas_is_harmless():
    s = Session(64, 64, seed=1, timelapse=False)
    before = s.canvas.rgb.copy()
    s.stroke([(-3.0, -3.0), (-2.5, -2.8)], brush="bristle", color="ultramarine")
    assert np.array_equal(before, s.canvas.rgb)


def test_single_point_makes_a_dab():
    s = Session(80, 80, seed=1, timelapse=False)
    before = s.canvas.rgb.copy()
    s.dab(0.5, 0.5, "round_hard", "cadmium_red", size=0.2)
    assert not np.array_equal(before, s.canvas.rgb)


def test_nan_or_inf_point_is_rejected_not_a_cryptic_numpy_crash():
    """A NaN/Inf coordinate used to reach ``np.arange`` inside path resampling and
    fail there with an opaque numpy error, rather than a clear message naming the
    bad input -- plausible for an agent whose own coordinate math momentarily
    divides by zero.
    """
    s = Session(64, 64, seed=1, timelapse=False)
    with pytest.raises(ValueError, match="finite"):
        s.stroke([(0.5, 0.5), (float("nan"), 0.5)], "round_hard", "cadmium_red")
    with pytest.raises(ValueError, match="finite"):
        s.pencil([(0.1, 0.1), (float("inf"), 0.9)])


# --------------------------------------------------------------------------------------
# Determinism, undo and replay
# --------------------------------------------------------------------------------------
def _paint(seed: int) -> Session:
    s = Session(120, 90, texture="linen", ground="toned_grey", seed=seed, timelapse=False)
    s.palette["mid"] = s.palette.mix("cerulean", "titanium_white", 0.5)
    s.block_in("upper-half", brush="bristle", color="mid", density=0.6, size=0.2)
    s.dry(1.0)
    s.stroke([(0.1, 0.7), (0.5, 0.66), (0.9, 0.74)], "flat", "burnt_umber", size=0.12)
    s.dab(0.6, 0.4, "round_hard", "cadmium_red", size=0.08)
    return s


def test_same_seed_gives_the_same_painting():
    a, b = _paint(7), _paint(7)
    assert np.array_equal(a.canvas.to_srgb8(), b.canvas.to_srgb8())


def test_different_seeds_give_different_paintings():
    a, b = _paint(7), _paint(8)
    assert not np.array_equal(a.canvas.to_srgb8(), b.canvas.to_srgb8())


def test_undo_restores_exact_state():
    s = _paint(5)
    before = s.canvas.rgb.copy()
    wet_before = s.canvas.wetness.copy()
    s.stroke([(0.2, 0.3), (0.8, 0.35)], "bristle", "cadmium_yellow")
    assert not np.array_equal(before, s.canvas.rgb)
    assert s.undo(1) == 1
    assert np.array_equal(before, s.canvas.rgb)
    assert np.array_equal(wet_before, s.canvas.wetness)


def test_undo_more_than_history_is_safe():
    s = Session(48, 48, seed=1, timelapse=False)
    assert s.undo(5) == 0


def test_undo_after_dry_lands_on_the_state_before_dry_not_before_the_stroke():
    """dry() mutates the canvas and must snapshot first, like every other mark.

    It used to add a log record without pushing a snapshot, so undo(1) right
    after a dry() popped the *previous* mark's snapshot -- restoring state from
    before the stroke that came before the dry, while only dropping the dry
    record from the log. That desyncs the canvas from what the log still claims
    happened, and replaying the (still-intact) log then disagrees with what is
    on screen.
    """
    s = Session(64, 64, seed=1, timelapse=False)
    s.stroke([(0.1, 0.1), (0.6, 0.6)], "bristle", "cadmium_red")
    after_stroke = s.canvas.rgb.copy()
    s.dry(1.0)
    assert s.undo(1) == 1
    assert [r.kind for r in s.history.records] == ["stroke"]
    assert np.array_equal(s.canvas.rgb, after_stroke)
    assert np.array_equal(s.canvas.rgb, s.replay().canvas.rgb)


def test_undo_beyond_cached_snapshots_matches_a_fresh_reload():
    """undo(n) must answer the same way regardless of how many snapshots happen
    to be cached in this process -- only :data:`MAX_SNAPSHOTS` are kept, so a
    long-running script asking to undo further than that used to silently undo
    fewer strokes than requested instead of falling back to exact log replay,
    the way the identical session reloaded from disk already correctly does.
    """
    from easel.history import MAX_SNAPSHOTS

    n = MAX_SNAPSHOTS + 6
    s = Session(48, 48, seed=2, timelapse=False)
    for i in range(n):
        s.stroke([(0.1, 0.1), (0.15 + 0.01 * i, 0.5)], "bristle", "burnt_umber")
    expected = s.replay(upto=len(s.history.records) - n).canvas.to_srgb8()
    assert s.undo(n) == n
    assert np.array_equal(s.canvas.to_srgb8(), expected)


def test_replay_reproduces_the_export_byte_for_byte():
    s = _paint(11)
    assert np.array_equal(s.canvas.to_srgb8(), s.replay().canvas.to_srgb8())


def test_replay_upto_matches_undo():
    s = _paint(13)
    n = len(s.history.records)
    partial = s.replay(upto=n - 1).canvas.to_srgb8()
    s.undo(1)
    assert np.array_equal(s.canvas.to_srgb8(), partial)


# --------------------------------------------------------------------------------------
# Colour
# --------------------------------------------------------------------------------------
def test_srgb_linear_round_trip():
    x = np.linspace(0.0, 1.0, 64, dtype=np.float32)
    assert np.allclose(linear_to_srgb(srgb_to_linear(x)), x, atol=1e-5)


def test_pigment_mixing_does_not_make_mud():
    """Yellow and blue must make green, and red and blue must make violet.

    Plain RGB averaging fails both. So does Kubelka-Munk without a reflectance
    floor, which sends red + blue to green.
    """
    p = Palette()
    green = p.mix("cadmium_yellow", "ultramarine", 0.5)
    r, g, b = (float(v) for v in green)
    assert g > r and g > b, f"yellow + blue should lean green, got {p.hex(green)}"

    violet = p.mix("cadmium_red", "ultramarine", 0.5)
    r, g, b = (float(v) for v in violet)
    assert r > g and b > g, f"red + blue should lean violet, got {p.hex(violet)}"


def test_white_actually_lightens():
    p = Palette()
    base = p.value_of("ultramarine")
    tinted = p.value_of(p.mix("ultramarine", "titanium_white", 0.5))
    # `value_of` reports perceptual value, so "substantially" is a number of value
    # steps, not a ratio. A nine-step scale puts about 0.12 between neighbours; half
    # a canvas of white has to move the colour further than one such step.
    assert tinted - base > 0.15, "50/50 with white should lighten substantially"


def test_value_of_agrees_with_the_values_view():
    """The number and the greyscale picture are the painter's two value instruments.

    They have to give the same reading. `value_of` used to return *linear*
    luminance while `look(values=True)` showed sRGB lightness, so the two
    disagreed by the whole transfer curve: burnt umber read 0.04 as a number and
    0.23 in the view, and every mixed dark reported an identical 0.04.
    """
    p = Palette()
    for name in ["titanium_white", "cadmium_yellow", "yellow_ochre",
                 "burnt_sienna", "burnt_umber", "ultramarine"]:
        s = Session(64, 64, ground=p.hex(name), seed=1, timelapse=False)
        shown = float(s.canvas.values().mean()) / 255.0
        assert p.value_of(name) == pytest.approx(shown, abs=0.01), name


def test_value_of_separates_the_darks():
    """Darks have to be distinguishable, or the instrument is useless where it matters."""
    p = Palette()
    assert p.value_of("burnt_sienna") - p.value_of("burnt_umber") > 0.05


def test_mix_endpoints_are_exact():
    a, b = parse_color("#3355aa"), parse_color("#aa5533")
    assert np.allclose(mix(a, b, 0.0), a, atol=1e-3)
    assert np.allclose(mix(a, b, 1.0), b, atol=1e-3)


def test_unknown_colour_names_explain_themselves():
    with pytest.raises(ValueError, match="Unknown colour"):
        parse_color("chartreuse-supreme")


def test_palette_slots():
    p = Palette()
    p["sky"] = p.mix("cerulean", "titanium_white", 0.6)
    assert "sky" in p
    assert p.hex("sky").startswith("#")
    with pytest.raises(KeyError):
        p["nonexistent"]


# --------------------------------------------------------------------------------------
# Brushes and strokes
# --------------------------------------------------------------------------------------
@pytest.mark.parametrize("name", sorted(BRUSHES))
def test_every_brush_makes_a_visible_mark(name):
    s = Session(160, 120, ground="toned_grey", seed=2, timelapse=False)
    # Smudge carries no paint of its own, so give it something to move first.
    if name == "smudge":
        s.stroke([(0.1, 0.5), (0.9, 0.5)], "bristle", "titanium_white", size=0.25)
    before = s.canvas.rgb.copy()
    s.stroke([(0.15, 0.4), (0.5, 0.5), (0.85, 0.45)], brush=name, color="cadmium_red", size=0.12)
    changed = np.abs(s.canvas.rgb - before).max(axis=2) > 1e-3
    assert changed.sum() > 20, f"{name} left almost no mark"


def test_tip_masks_are_normalised_and_odd_sized():
    for tip in ("round_soft", "round_hard", "flat", "bristle", "knife"):
        m = tip_mask(tip, 9.0, 0.5, 0.7, aspect=0.3)
        assert m.shape[0] == m.shape[1]
        assert m.shape[0] % 2 == 1
        assert 0.0 <= float(m.min()) and float(m.max()) <= 1.0
        assert float(m.max()) > 0.4, f"{tip} tip is nearly empty"


def test_bristle_striations_are_stable_for_a_brush():
    """Bristles must not shimmer from dab to dab -- the pattern is fixed per brush."""
    a = tip_mask("bristle", 12.0, 0.0, 0.65, aspect=0.3, bristle_seed=4)
    b = tip_mask("bristle", 12.0, 0.0, 0.65, aspect=0.3, bristle_seed=4)
    c = tip_mask("bristle", 12.0, 0.0, 0.65, aspect=0.3, bristle_seed=5)
    assert np.array_equal(a, b)
    assert not np.array_equal(a, c)


def test_paint_load_runs_out_along_a_stroke():
    c = Canvas(600, 100, texture="rough", ground="white", seed=1)
    b = brush("bristle", size=0.12, load_falloff=1.4)
    r = paint_stroke(c, [(0.02, 0.5), (0.98, 0.5)], b, "#101010", "even",
                     np.random.default_rng(1))
    assert r.end_load < 0.5, "a long stroke should exhaust most of its load"
    lum = c.rgb.mean(axis=2)[50]
    start = float(lum[60:140].mean())
    end = float(lum[460:540].mean())
    assert end > start, "the far end of the stroke should carry less paint"


@pytest.mark.parametrize("profile", PRESSURE_PROFILES)
def test_pressure_profiles_are_finite_and_bounded(profile):
    v = pressure_curve(profile, 50)
    assert v.shape == (50,)
    assert np.isfinite(v).all(), f"{profile} produced NaN"
    assert float(v.min()) >= 0.0 and float(v.max()) <= 1.0


def test_pressure_accepts_scalar_and_list():
    assert np.allclose(pressure_curve(0.5, 10), 0.5)
    ramp = pressure_curve([0.0, 1.0], 5)
    assert ramp[0] < ramp[-1]


def test_unknown_pressure_profile_explains_itself():
    with pytest.raises(ValueError, match="Unknown pressure profile"):
        pressure_curve("fortissimo", 10)


def test_empty_pressure_list_explains_itself():
    with pytest.raises(ValueError, match="pressure list"):
        pressure_curve([], 10)


def test_catmull_rom_passes_through_its_endpoints():
    pts = np.array([[0.1, 0.1], [0.5, 0.9], [0.9, 0.2]], dtype=np.float32)
    curve = catmull_rom(pts)
    assert np.allclose(curve[0], pts[0], atol=1e-4)
    assert np.allclose(curve[-1], pts[-1], atol=1e-4)
    assert len(curve) > len(pts)


def test_short_paths_pass_through_unchanged():
    pts = np.array([[0.2, 0.2], [0.8, 0.8]], dtype=np.float32)
    assert np.array_equal(catmull_rom(pts), pts)


# --------------------------------------------------------------------------------------
# Paint behaviour
# --------------------------------------------------------------------------------------
def test_wet_paint_mixes_and_dry_paint_covers():
    """The same yellow over blue: mixes toward green while wet, covers once dry."""

    def over_blue(dry_first: bool) -> np.ndarray:
        s = Session(140, 140, ground="white", seed=4, timelapse=False)
        s.block_in("all", brush="flat", color="ultramarine", density=1.0, size=0.3)
        if dry_first:
            s.dry(1.0)
        s.stroke([(0.15, 0.5), (0.85, 0.5)], "flat", "cadmium_yellow",
                 size=0.25, pressure="even")
        return s.canvas.rgb[70, 60:80].mean(axis=0)

    wet, dried = over_blue(False), over_blue(True)
    assert float(dried[0]) > float(wet[0]), "drying first should let yellow cover"
    assert float(wet[2]) > float(dried[2]), "wet blue should still show through"


def test_dry_reduces_wetness():
    s = Session(64, 64, seed=1, timelapse=False)
    s.stroke([(0.2, 0.5), (0.8, 0.5)], "bristle", "cadmium_red", size=0.3)
    assert float(s.canvas.wetness.max()) > 0.1
    s.dry(1.0)
    assert float(s.canvas.wetness.max()) < 1e-6


def test_glaze_does_not_build_thickness():
    s = Session(80, 80, seed=1, timelapse=False)
    s.glaze([(0.2, 0.5), (0.8, 0.5)], "alizarin", opacity=0.3)
    assert float(s.canvas.thickness.max()) == 0.0


def _starved_band(texture: str, load: float) -> np.ndarray:
    """The painted band left by one starved stroke, as luminance."""
    c = Canvas(400, 80, texture=texture, ground="white", seed=2)
    b = brush("bristle", size=0.16, load=load, load_falloff=0.0)
    paint_stroke(c, [(0.05, 0.5), (0.95, 0.5)], b, "#101010", "even",
                 np.random.default_rng(1))
    return c.rgb.mean(axis=2)[30:50, 40:360]


def _mean_run(band: np.ndarray) -> float:
    """Mean length of an unbroken covered run along a row: how chunky the marks are."""
    runs, n = [], 0
    for row in band < 0.6:
        for covered in row:
            if covered:
                n += 1
            elif n:
                runs.append(n)
                n = 0
        if n:
            runs.append(n)
            n = 0
    return float(np.mean(runs)) if runs else 0.0


@pytest.mark.parametrize("texture", TEXTURES)
def test_canvas_tooth_gates_deposition(texture):
    """Tooth must gate the paint: a starved brush leaves far less than a full one."""
    full = float((1.0 - _starved_band(texture, 1.0)).sum())
    starved = float((1.0 - _starved_band(texture, 0.35)).sum())
    assert starved < full * 0.6


@pytest.mark.parametrize("texture", TEXTURES)
def test_a_starved_stroke_still_marks_every_surface(texture):
    """A low load must break a stroke up, never stop it dead.

    The gate threshold used to be an absolute height while each texture occupies a
    different span, so on the narrow-toothed surfaces the threshold climbed clean
    off the top of the tooth: a bristle brush below about a third of its load
    deposited *nothing at all* on smooth and linen, while rough still marked. The
    painter got a full dab count back and an unchanged canvas. See REVIEW.md
    finding 11.
    """
    band = _starved_band(texture, 0.15)
    assert float((1.0 - band).sum()) > 100.0, "a starved stroke laid no paint at all"
    assert float((band > 0.9).mean()) > 0.15, "a starved stroke was not broken up"


def test_surfaces_break_up_at_their_own_scale():
    """Rough leaves chunky islands; linen's fine weave leaves fine speckle."""
    rough = _mean_run(_starved_band("rough", 0.35))
    linen = _mean_run(_starved_band("linen", 0.35))
    assert rough > linen * 1.5


@pytest.mark.parametrize("texture", TEXTURES)
def test_textures_are_deterministic(texture):
    a = make_texture(texture, 60, 80, np.random.default_rng(3))
    b = make_texture(texture, 60, 80, np.random.default_rng(3))
    assert np.array_equal(a, b)


# --------------------------------------------------------------------------------------
# Composition helpers
# --------------------------------------------------------------------------------------
def test_named_regions_are_inside_the_canvas():
    from easel.regions import REGION_NAMES

    for name in REGION_NAMES:
        r = region(name)
        assert 0.0 <= r.x0 < r.x1 <= 1.0
        assert 0.0 <= r.y0 < r.y1 <= 1.0


def test_grid_cells_tile_the_canvas():
    a1, h8 = cell("A1"), cell("H8")
    assert a1.x0 == 0.0 and a1.y0 == 0.0
    assert h8.x1 == pytest.approx(1.0)
    assert h8.y1 == pytest.approx(1.0)
    assert cell("d6").bounds == cell("D6").bounds


def test_bad_cell_label_explains_itself():
    with pytest.raises(ValueError, match="Bad cell"):
        cell("Z9")


@pytest.mark.parametrize("label", ["A12", "D67", "B23"])
def test_two_digit_row_typo_is_rejected_not_silently_truncated(label):
    """``text[1:] not in GRID_ROWS`` checked substring membership, not a single
    valid row character -- "12" in "12345678" is True, so "A12" silently
    resolved to cell A1 instead of raising.
    """
    with pytest.raises(ValueError, match="Bad cell"):
        cell(label)


def test_relative_placement():
    from easel.regions import below, between, right_of

    top = region("top-left")
    under = below(top, 0.2)
    assert under.y0 == pytest.approx(top.y1)
    assert right_of(top, 0.1).x0 == pytest.approx(top.x1)
    span = between(region("top-left"), region("bottom-right"))
    assert span.x1 > span.x0 and span.y1 > span.y0


def test_region_helpers_stay_in_bounds():
    """Over-insetting must not blow up mid-painting; it collapses to a sliver."""
    r = Region(0.05, 0.05, 0.2, 0.2).inset(0.5)
    assert 0.0 <= r.x0 < r.x1 <= 1.0
    assert 0.0 <= r.y0 < r.y1 <= 1.0


def test_block_in_leaves_visible_brushwork():
    """A block-in must not be a flat fill -- the marks have to vary."""
    s = Session(200, 150, ground="white", seed=6, timelapse=False)
    s.block_in("all", brush="bristle", color="burnt_umber", density=0.8, size=0.2)
    painted = s.canvas.rgb.mean(axis=2)
    assert float(painted.std()) > 0.01, "block-in produced a flat, unpainterly fill"


def test_block_in_passes_alternate_direction():
    """Consecutive passes must run opposite ways, the way a hand comes back.

    Paint runs out along a stroke. Passes that all start at the same edge stack
    their run-out and leave the whole mass lighter on the side they end at -- a
    machine's signature. See REVIEW.md finding 12.
    """
    s = Session(120, 120, ground="white", seed=6, timelapse=False)
    records = s.block_in("all", brush="bristle", color="burnt_umber",
                         direction="horizontal", density=1.0, size=0.12)
    starts = [r.points[0][0] for r in records]
    assert len(set(round(x) for x in starts)) == 2, "every pass started at the same edge"


def test_block_in_does_not_leave_a_run_out_gradient():
    """The blocked-in mass must not fade across the canvas as the passes run out."""
    s = Session(300, 300, ground="white", seed=12, timelapse=False)
    s.block_in("all", brush="bristle", color="ultramarine",
               direction="horizontal", density=1.0)
    lum = s.canvas.rgb.mean(axis=2)
    left, right = float(lum[:, :100].mean()), float(lum[:, 200:].mean())
    assert abs(right - left) < 0.08, f"block-in fades across the canvas: {left:.3f} to {right:.3f}"


# --------------------------------------------------------------------------------------
# look() and history
# --------------------------------------------------------------------------------------
def test_look_writes_a_png(tmp_path):
    s = Session(120, 90, seed=1, timelapse=False, out_dir=tmp_path)
    s.stroke([(0.2, 0.5), (0.8, 0.5)], "bristle", "cadmium_red")
    p = s.look(grid=True)
    assert p.exists() and p.suffix == ".png"


def test_look_variants_render(tmp_path):
    s = Session(120, 90, seed=1, timelapse=False, out_dir=tmp_path)
    s.stroke([(0.2, 0.5), (0.8, 0.5)], "bristle", "cadmium_red")
    assert s.look_image(values=True).mode == "RGB"
    assert s.look_image(region="top-left").size[0] > 0
    s.look_image()  # establishes a baseline for the diff
    s.stroke([(0.2, 0.7), (0.8, 0.7)], "flat", "ultramarine")
    assert s.look_image(diff=True).size[0] > 0


def test_look_downsamples_to_the_requested_size(tmp_path):
    s = Session(2000, 1000, seed=1, timelapse=False, out_dir=tmp_path)
    assert max(s.look_image(scale=512).size) == 512


def test_history_logs_every_mark():
    s = Session(80, 80, seed=1, timelapse=False)
    s.stroke([(0.2, 0.2), (0.8, 0.8)], "bristle", "ultramarine", note="first")
    s.dry(0.5)
    assert len(s.history.records) == 2
    assert s.stroke_count == 1  # drying is not a mark
    assert "first" in s.log()


def test_signature_marks_are_free_up_to_the_allowance():
    """The guide grants five free marks to sign with; the counter must honour it.

    Two REHEARSAL6 painters found that it did not, by watching `stroke_count` go past
    the budget they were painting to, and one of them undid a finished mark to pay for
    its signature. Past the allowance every signature mark is charged, so a painter
    cannot buy strokes by noting them.
    """
    s = Session(80, 80, seed=1, timelapse=False)
    for _ in range(3):
        s.stroke([(0.2, 0.2), (0.8, 0.8)], "bristle", "ultramarine")
    assert s.stroke_count == 3

    for _ in range(History.SIGNATURE_ALLOWANCE):
        s.stroke([(0.85, 0.9), (0.9, 0.88)], "liner", "ultramarine", note="signature")
    assert s.stroke_count == 3, "marks noted `signature` are free up to the allowance"

    s.stroke([(0.85, 0.8), (0.9, 0.78)], "liner", "ultramarine", note="signature")
    assert s.stroke_count == 4, "past the allowance a signature mark is charged"
    assert len(s.history.records) == 3 + History.SIGNATURE_ALLOWANCE + 1


def test_timelapse_and_contact_sheet(tmp_path):
    s = Session(80, 60, seed=1, timelapse=True)
    for i in range(4):
        s.stroke([(0.1, 0.2 + i * 0.2), (0.9, 0.25 + i * 0.2)], "bristle", "burnt_umber")
    assert s.timelapse_gif(tmp_path / "t.gif").exists()
    assert s.contact_sheet(tmp_path / "t.png").exists()


def test_timelapse_without_frames_explains_itself():
    s = Session(64, 64, seed=1, timelapse=False)
    with pytest.raises(ValueError, match="No time-lapse frames"):
        s.timelapse_gif("unused.gif")


# --------------------------------------------------------------------------------------
# Persistence
# --------------------------------------------------------------------------------------
def test_session_round_trips_through_disk(tmp_path):
    s = _paint(21)
    path = tmp_path / "p.easel"
    s.save(path)
    assert path.exists(), "save must honour the exact filename it was given"

    loaded = Session.load(path)
    assert np.array_equal(s.canvas.to_srgb8(), loaded.canvas.to_srgb8())
    assert loaded.seed == s.seed
    assert len(loaded.history.records) == len(s.history.records)
    assert "mid" in loaded.palette


def test_loading_a_missing_session_explains_itself(tmp_path):
    with pytest.raises(FileNotFoundError, match="No session at"):
        Session.load(tmp_path / "nope.easel")


def test_undo_after_reload_uses_replay(tmp_path):
    """A session off disk has no snapshots, so undo has to rebuild from the log."""
    s = _paint(23)
    path = tmp_path / "p.easel"
    s.save(path)

    expected = s.replay(upto=len(s.history.records) - 1).canvas.to_srgb8()
    loaded = Session.load(path)
    assert loaded.undo(1) == 1
    assert np.array_equal(loaded.canvas.to_srgb8(), expected)


def test_block_in_after_a_reload_draws_from_the_same_stream_as_never_saving(tmp_path):
    """block_in()/sweep() draw their pass wobble from Session.rng, which round-trips
    through save/load via ``_encode_rng``/``_decode_rng``. Nothing else in this
    file paints with block_in on a session obtained from ``Session.load()``, so a
    broken rng round-trip would pass the whole suite silently -- this pins the
    exact scenario finding 1's fix (a corrupted rng_state used to fail open onto
    an entropy-seeded generator instead of raising) protects.
    """
    reference = Session(64, 64, seed=5, timelapse=False)
    reference.stroke([(0.1, 0.1), (0.5, 0.5)], "bristle", "burnt_umber")
    reference.block_in(cell("B2"), "bristle", "ultramarine", density=0.8)
    reference.block_in(cell("D4"), "bristle", "ultramarine", density=0.8)

    reloaded = Session(64, 64, seed=5, timelapse=False)
    reloaded.stroke([(0.1, 0.1), (0.5, 0.5)], "bristle", "burnt_umber")
    reloaded.block_in(cell("B2"), "bristle", "ultramarine", density=0.8)
    path = tmp_path / "p.easel"
    reloaded.save(path)
    reloaded = Session.load(path)
    reloaded.block_in(cell("D4"), "bristle", "ultramarine", density=0.8)

    assert np.array_equal(reference.canvas.to_srgb8(), reloaded.canvas.to_srgb8())


def test_save_replaces_the_file_atomically_and_leaves_no_temp_behind(tmp_path):
    """The `.easel` file is the only copy of the painting: a crash partway through
    an in-place write must not be able to leave it truncated.
    """
    path = tmp_path / "p.easel"
    _paint(1).save(path)
    assert [f.name for f in tmp_path.iterdir()] == ["p.easel"]


def test_a_corrupted_session_file_raises_a_clear_error(tmp_path):
    """A truncated `.easel` file -- exactly what a crash partway through a
    non-atomic save used to risk leaving behind -- surfaced as a raw
    ``zipfile.BadZipFile`` traceback instead of the same clear message every
    other session-file problem gets.
    """
    path = tmp_path / "p.easel"
    _paint(1).save(path)
    path.write_bytes(path.read_bytes()[:100])
    with pytest.raises(ValueError, match="not a valid Easel session file"):
        Session.load(path)


# --------------------------------------------------------------------------------------
# The `easel` CLI
# --------------------------------------------------------------------------------------
def test_new_refuses_to_clobber_an_existing_session_without_force(tmp_path):
    from easel.cli import main

    path = tmp_path / "p.easel"
    assert main(["new", str(path), "--size", "32x32"]) == 0
    s = Session.load(path)
    s.stroke([(0.1, 0.1), (0.5, 0.5)], "bristle", "cadmium_red")
    s.save(path)

    assert main(["new", str(path), "--size", "16x16"]) == 1
    assert Session.load(path).stroke_count == 1, "the refused `new` must not touch the file"

    assert main(["new", str(path), "--size", "16x16", "--force"]) == 0
    assert Session.load(path).stroke_count == 0


def test_a_corrupted_session_file_fails_the_cli_cleanly(tmp_path, capsys):
    from easel.cli import main

    path = tmp_path / "p.easel"
    _paint(1).save(path)
    path.write_bytes(path.read_bytes()[:100])
    assert main(["look", str(path)]) == 1
    assert "easel:" in capsys.readouterr().err


def test_run_reports_a_syntax_error_without_touching_the_session(tmp_path):
    from easel.cli import main

    session = tmp_path / "p.easel"
    script = tmp_path / "bad.py"
    assert main(["new", str(session), "--size", "32x32"]) == 0
    script.write_text('print "not valid python 3"\n', encoding="utf-8")
    assert main(["run", str(session), str(script)]) == 1
    assert Session.load(session).stroke_count == 0


# --------------------------------------------------------------------------------------
# Errors are helpful
# --------------------------------------------------------------------------------------
def test_unknown_brush_lists_the_real_ones():
    with pytest.raises(KeyError, match="Available"):
        brush("sable-supreme")


def test_unknown_region_lists_the_real_ones():
    with pytest.raises(KeyError, match="Available"):
        region("north-by-northwest")


def test_unknown_texture_and_ground_explain_themselves():
    with pytest.raises(ValueError, match="Unknown texture"):
        Canvas(32, 32, texture="velvet")
    with pytest.raises(ValueError, match="Unknown ground"):
        Canvas(32, 32, ground="chartreuse")


def test_tiny_canvas_is_rejected():
    with pytest.raises(ValueError, match="at least 8x8"):
        Canvas(4, 4)


# --------------------------------------------------------------------------------------
# Telling the painter what actually happened
# --------------------------------------------------------------------------------------
def test_a_stroke_reports_how_much_paint_landed():
    """Dabs are attempts; paint is what stuck. The painter needs the second number."""
    s = Session(200, 150, ground="white", seed=4, timelapse=False)
    full = s.stroke([(0.1, 0.5), (0.9, 0.5)], "bristle", "ultramarine", pressure="even")
    starved = s.stroke([(0.1, 0.8), (0.9, 0.8)], "bristle", "ultramarine",
                       pressure="even", load=0.08, load_falloff=0.0)
    assert full.dabs == starved.dabs, "the two strokes should stamp the same dabs"
    assert full.paint > starved.paint * 3.0, "a starved stroke should lay far less paint"
    assert starved.paint > 0.0, "a starved stroke should still lay something"


def test_the_log_says_when_a_mark_laid_no_paint():
    """A mark that changed nothing must say so, not read like any other stroke."""
    s = Session(120, 90, ground="white", seed=4, timelapse=False)
    s.stroke([(0.1, 0.5), (0.9, 0.5)], "bristle", "ultramarine", opacity=0.0)
    assert "NO PAINT LANDED" in s.log(1)


def test_paint_survives_a_save_and_reload(tmp_path):
    s = Session(100, 80, ground="white", seed=4, timelapse=False)
    s.stroke([(0.1, 0.5), (0.9, 0.5)], "bristle", "ultramarine")
    reloaded = Session.load(s.save(tmp_path / "p.easel"))
    assert reloaded.history.records[0].paint == pytest.approx(s.history.records[0].paint)


def test_the_cli_runs_as_a_module():
    """`easel` is not always on PATH, so `python -m easel` has to work."""
    result = subprocess.run(
        [sys.executable, "-m", "easel", "brushes"],
        capture_output=True, text=True, timeout=120,
    )
    assert result.returncode == 0, result.stderr
    assert "bristle" in result.stdout



@pytest.mark.parametrize("direction", ["horizontal", "vertical", "diagonal", "cross"])
@pytest.mark.parametrize("size", [0.20, 0.08])
def test_block_in_stays_inside_its_region(direction, size):
    """A mass must land where it was asked for, give or take a brush width.

    `diagonal` used to draw each pass as the whole 45-degree line through the
    region without clipping it, so every pass ran out sideways by the region's own
    height -- a block-in aimed at the middle of the canvas smeared across all of
    it, and the overspill did not shrink when you took a smaller brush.
    """
    r = Region(0.40, 0.42, 0.70, 0.62)
    s = Session(1000, 600, ground="toned_grey", seed=5, timelapse=False)
    before = s.canvas.rgb.copy()
    s.block_in(r, "bristle", "titanium_white", density=0.9, size=size,
               direction=direction)

    touched = np.abs(s.canvas.rgb - before).max(axis=2) > 1e-3
    ys, xs = np.nonzero(touched)
    assert xs.size, "the block-in laid no paint at all"

    slack = size + 0.02          # half a brush either side, plus the overhang
    assert xs.min() / 1000 >= r.x0 - slack
    assert xs.max() / 1000 <= r.x1 + slack
    assert ys.min() / 600 >= r.y0 - slack
    assert ys.max() / 600 <= r.y1 + slack


def test_the_reference_gets_the_same_grid_and_the_same_greyscale():
    """Side by side is for comparing, so both panels must be treated alike.

    The grid used to stop at the edge of the painting, which is the one place it
    is least needed -- a painter copying a reference needs to name a place on the
    reference and hit the same place on the canvas. And `values=True` converted
    only the canvas, so the guide's own "compare value structure, not colour" call
    put a greyscale painting beside a full-colour photograph.
    """
    from PIL import Image

    from easel.look import render_look

    s = Session(200, 200, ground="toned_grey", seed=1, timelapse=False)
    ref = Image.new("RGB", (300, 200), (200, 40, 40))

    plain = np.asarray(render_look(s.canvas, reference=ref))
    gridded = np.asarray(render_look(s.canvas, reference=ref, grid=True))
    left = slice(0, plain.shape[1] // 3)
    assert not np.array_equal(plain[:, left], gridded[:, left]), \
        "the grid never reached the reference panel"

    grey = np.asarray(render_look(s.canvas, reference=ref, values=True))[:, left]
    spread = np.abs(grey[:, :, 0].astype(int) - grey[:, :, 2].astype(int)).max()
    assert spread <= 1, "the reference was left in colour beside a greyscale canvas"


# --------------------------------------------------------------------------------------
# M5, second rehearsal: naming a run of cells, and crops you can actually read.


def test_span_covers_both_cells_in_either_order():
    from easel.regions import span

    a = span("E5", "H8")
    assert a.bounds == (0.5, 0.5, 1.0, 1.0)
    assert span("H8", "E5").bounds == a.bounds
    assert span("B2", "B2").bounds == cell("B2").bounds
    assert a.name == "E5:H8"


def test_span_is_in_scope_for_easel_run(tmp_path):
    from easel.regions import span

    assert span("A1", "B2").bounds == (0.0, 0.0, 0.25, 0.25)
    import easel

    assert "span" in easel.__all__


def test_look_enlarges_a_small_crop(tmp_path):
    from easel.look import MIN_CROP_SIZE, render_look

    s = Session(1200, 800, seed=1, out_dir=tmp_path, timelapse=False)
    crop = render_look(s.canvas, region=cell("D6"))          # 150 x 100 px of canvas
    assert max(crop.size) >= MIN_CROP_SIZE
    assert abs(crop.width / crop.height - 1.5) < 0.05        # the cell's own aspect
    # a crop that is already big enough is left at its own size
    big = render_look(s.canvas, region=region("all"), scale=None)
    assert big.size == (1200, 800)
