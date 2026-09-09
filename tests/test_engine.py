"""Property tests for the engine.

Three properties matter most, and they are the ones the brief calls out:

* strokes never write outside the canvas,
* undo restores exact state,
* replay from the log reproduces the export byte for byte.

Everything else here guards a specific bug that was actually hit while building.
"""

from __future__ import annotations

import numpy as np
import pytest

from easel import Session
from easel.brush import BRUSHES, brush, tip_mask
from easel.canvas import Canvas
from easel.color import linear_to_srgb, mix, parse_color, srgb_to_linear
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
    assert tinted > base * 2.0, "50/50 with white should lighten substantially"


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


def test_rough_texture_breaks_a_stroke_more_than_smooth():
    """Canvas tooth must actually gate deposition, or dry brush is a lie.

    The property is *brokenness*, not coverage. A rough surface has a wider spread
    of peaks and valleys, so a starved brush skips across it -- leaving more paint
    on the peaks than a smooth surface does, but in a far patchier band. Total ink
    is the wrong measure; spatial variance within the band is the right one.
    """

    def brokenness(texture: str) -> float:
        c = Canvas(400, 80, texture=texture, ground="white", seed=2)
        b = brush("bristle", size=0.16, load=0.35, load_falloff=0.0)
        paint_stroke(c, [(0.05, 0.5), (0.95, 0.5)], b, "#101010", "even",
                     np.random.default_rng(1))
        return float(c.rgb.mean(axis=2)[30:50, 40:360].std())

    assert brokenness("rough") > brokenness("smooth") * 1.3


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
