"""The engine changes the pears session asked for, and what each one is for.

One painter took the guide at its word, painted a still life from it with no
reference, and wrote down what the engine had cost them. Every test here guards one
item from that list, so the reason for each is the same shape: a painter spent
strokes, or spent attention, on something the engine could have held.

Two of them are really about arithmetic agreeing with itself -- ``cost`` quoting what
``paint`` charges, a rehearsal landing where the painting lands -- and those matter
more than they look. A plan that is checked and then retyped is a plan that drifts,
and the drift arrives as paint.

Where a test could ask the API what it did, it asks the canvas instead.
"""

from __future__ import annotations

import warnings

import numpy as np
import pytest
from PIL import Image

from easel import Session, blob, cell, hull, span, union
from easel.cli import main, run_script
from easel.palette import Palette


def make(tmp_path, **kw):
    """A small session that writes its looks under the test's own directory."""
    kw.setdefault("timelapse", False)
    return Session(320, 240, texture="linen", ground="toned_grey", seed=7,
                   out_dir=tmp_path, **kw)


# -- paint(plan): the fourth verb of the planning loop ---------------------------------
def test_paint_charges_exactly_what_cost_quoted(tmp_path):
    """The whole point of one plan object: the quote and the bill are the same number.

    Masses and sweeps are the expensive marks and the ones no painter can count by
    hand, so a quote that drifts from what is charged is worse than no quote.
    """
    shape = make(tmp_path).circle((0.5, 0.5), 0.16)
    edge = [(0.05, 0.75), (0.5, 0.72), (0.95, 0.78)]
    plan = [
        {"shape": shape, "brush": "flat", "color": "burnt_umber", "size": 0.06},
        {"edge": edge, "into": "down", "depth": 0.12, "brush": "bristle",
         "color": "ultramarine", "size": 0.05},
        {"points": [(0.2, 0.3), (0.6, 0.35)], "brush": "liner", "size": 0.005},
    ]
    s = make(tmp_path)
    quoted = s.cost(plan)
    assert len(s.paint(plan)) == quoted


def test_a_rehearsed_plan_lands_exactly_where_it_was_rehearsed(tmp_path):
    """What is tried on the scrap of canvas is what gets painted, pixel for pixel.

    This is the promise that makes rehearsing worth a painter's time; without it a
    rehearsal is a suggestion, and a painter who cannot trust it will not use it.
    """
    plan = {"shape": blob(cell("D5"), 0.12, seed=2), "brush": "bristle",
            "color": "burnt_umber", "size": 0.07}
    s = make(tmp_path)
    trial = s.scratch()
    for kind, spec in s._plan_specs(plan):
        trial._lay(kind, spec)
    s.paint(plan)
    assert np.array_equal(trial.canvas.rgb, s.canvas.rgb)


def test_paint_takes_the_plan_preview_and_cost_take(tmp_path):
    """A bare place is a mass to all four verbs, not just to three of them."""
    s = make(tmp_path)
    shape = s.circle((0.5, 0.5), 0.12)
    assert len(s.paint(shape)) == make(tmp_path).cost(shape)


def test_paint_notes_only_what_has_no_note_of_its_own(tmp_path):
    s = make(tmp_path)
    records = s.paint([{"points": [(0.2, 0.2), (0.4, 0.4)], "note": "mine"},
                       {"points": [(0.5, 0.5), (0.7, 0.7)]}], note="the pass")
    assert [r.note for r in records] == ["mine", "the pass"]


# -- the budget ------------------------------------------------------------------------
def test_the_budget_counts_down_and_survives_being_saved(tmp_path):
    """A painter is told to write the split down. This is the engine holding it."""
    s = make(tmp_path, budget=40)
    s.stroke([(0.1, 0.1), (0.5, 0.5)])
    assert (s.spent, s.remaining) == (1, 39)
    assert "1 of 40 strokes spent, 39 left" in s.budget_line()

    back = Session.load(s.save(tmp_path / "p.easel"))
    assert (back.budget, back.remaining) == (40, 39)
    assert back.replay().budget == 40


def test_no_budget_still_says_what_was_spent(tmp_path):
    s = make(tmp_path)
    s.stroke([(0.1, 0.1), (0.5, 0.5)])
    assert s.remaining is None
    assert s.budget_line() == "1 strokes spent (no budget set)"


def test_an_overrun_says_so_rather_than_resting_at_zero(tmp_path):
    s = make(tmp_path, budget=2)
    for _ in range(5):
        s.stroke([(0.1, 0.1), (0.5, 0.5)])
    assert s.remaining == -3
    assert "3 OVER budget" in s.budget_line()


def test_cost_flags_a_plan_that_would_eat_the_budget(tmp_path):
    """Twelve strokes sounds small until it is most of what is left."""
    s = make(tmp_path, budget=8)
    plan = {"shape": s.circle((0.5, 0.5), 0.2), "brush": "flat", "size": 0.05}
    with pytest.warns(UserWarning, match="of the 8 left"):
        s.cost(plan)
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        s.cost(plan, share=0)          # asked not to flag, so it must not


def test_cost_is_silent_without_a_budget(tmp_path):
    s = make(tmp_path)
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        s.cost({"shape": s.circle((0.5, 0.5), 0.2), "brush": "flat", "size": 0.05})


# -- cover(): the burying recipe, with its clauses already set -------------------------
def test_cover_lays_the_burying_recipe(tmp_path):
    """Every clause earns its place, and load_falloff is the one that gets missed.

    A full-width correction at load=1.0 still runs dry and speckles at its far end
    without it -- which is the failure that sends a painter back to correct the
    correction.
    """
    s = make(tmp_path)
    s.block_in(cell("D5"), "bristle", "ultramarine")
    dark = s.canvas.rgb.copy()
    records = s.cover(cell("D5"), "titanium_white")

    assert records, "cover laid nothing"
    assert all(r.params["load"] == 1.0 for r in records)
    assert all(r.params["load_falloff"] == 0.0 for r in records)
    assert all(r.params["opacity"] == 1.0 for r in records)
    assert all(r.pressure == "even" for r in records)
    # It buried: the middle of the cell is lighter than the blue it covered.
    mid = (slice(100, 140), slice(140, 180))
    assert s.canvas.rgb[mid].mean() > dark[mid].mean() + 0.2


def test_cover_dries_the_area_first_and_the_dry_is_free(tmp_path):
    s = make(tmp_path)
    s.block_in(cell("D5"), "bristle", "ultramarine")
    before = s.stroke_count
    records = s.cover(cell("D5"), "titanium_white")
    kinds = [r.kind for r in s.history.records[before:]]
    assert kinds[0] == "dry"
    assert "dry" not in [r.kind for r in records]   # drying is not a mark


def test_cover_refuses_the_recipe_to_a_comb(tmp_path):
    """A bristle does not bury: its comb leaves the old paint showing between streaks."""
    s = make(tmp_path)
    with pytest.warns(UserWarning, match="does not bury"):
        s.cover(cell("D5"), "titanium_white", brush="bristle")


# -- scumble(): the soft passage, as paint rather than as smudging ---------------------
def test_scumble_lays_exactly_the_passes_it_was_asked_for(tmp_path):
    """Charged as n, so a soft passage can be budgeted before it is laid."""
    s = make(tmp_path)
    assert len(s.scumble(span("A3", "H5"), "burnt_umber", "titanium_white", 8)) == 8


def test_scumble_steps_from_one_value_to_the_other(tmp_path):
    s = make(tmp_path)
    records = s.scumble(span("A3", "H5"), "burnt_umber", "titanium_white", 6)
    values = [Palette().value_of(r.color_hex) for r in records]
    assert values == sorted(values), "the passes did not step in one direction"
    assert values[0] < values[-1]
    # And the ends really are the two colours asked for.
    assert records[0].color_hex.lower() == Palette().hex("burnt_umber").lower()


def test_scumble_needs_at_least_two_values(tmp_path):
    s = make(tmp_path)
    with pytest.raises(ValueError, match="at least two passes"):
        s.scumble(span("A3", "H5"), "burnt_umber", "titanium_white", 1)


# -- block_in(edge="clean"): the contour a small mass wants ----------------------------
def _spill_px(session, shape, **kw):
    """How far past the outline any paint landed, in pixels."""
    before = session.canvas.rgb.copy()
    session.block_in(shape, **kw)
    changed = np.abs(session.canvas.rgb - before).max(axis=2) > 0.01
    h, w = changed.shape
    ys, xs = np.nonzero(changed & ~shape.mask(w, h))
    if not len(xs):
        return 0.0
    pts = np.asarray(shape.closed, dtype=np.float64)
    ax, ay = pts[:-1, 0] * w, pts[:-1, 1] * h
    ex, ey = pts[1:, 0] * w - ax, pts[1:, 1] * h - ay
    lens = np.maximum(ex ** 2 + ey ** 2, 1e-12)
    t = np.clip(((xs[:, None] - ax) * ex + (ys[:, None] - ay) * ey) / lens, 0.0, 1.0)
    return float(np.hypot(xs[:, None] - (ax + t * ex),
                          ys[:, None] - (ay + t * ey)).min(axis=1).max())


def test_a_clean_edge_keeps_the_paint_nearer_the_drawn_line(tmp_path):
    """The fringe of dots round a small mass is the half-brush overhang a round tip
    lays as separate discs. Insetting the fill and drawing the contour pulls it in."""
    shape = make(tmp_path).circle((0.5, 0.5), 0.18, wobble=0.12, seed=3)
    kw = dict(brush="round_hard", color="burnt_umber", size=0.09)
    ragged = _spill_px(make(tmp_path), shape, edge="ragged", **kw)
    clean = _spill_px(make(tmp_path), shape, edge="clean", **kw)
    assert clean < ragged


def test_a_clean_edge_is_priced_as_it_is_painted(tmp_path):
    """Including the contour pass: the inset fill is cheaper, the contour costs one."""
    shape = make(tmp_path).circle((0.5, 0.5), 0.16)
    spec = {"shape": shape, "brush": "flat", "color": "burnt_umber",
            "size": 0.06, "edge": "clean"}
    s = make(tmp_path)
    quoted = s.cost(spec)
    records = s.paint(spec)
    assert len(records) == quoted
    assert sum(r.note.startswith("clean edge") for r in records) == 1


def test_a_clean_edge_says_so_when_the_brush_cannot_draw_one(tmp_path):
    s = make(tmp_path)
    with pytest.warns(UserWarning, match="stringier contour"):
        s.block_in(s.circle((0.5, 0.5), 0.16), "bristle", "burnt_umber",
                   size=0.06, edge="clean")


def test_an_unknown_edge_is_refused_while_it_is_still_free(tmp_path):
    s = make(tmp_path)
    with pytest.raises(ValueError, match="'ragged'"):
        s.block_in(cell("D5"), "flat", "burnt_umber", edge="soft")


# -- shapes in this canvas's own units -------------------------------------------------
def test_a_circle_is_round_in_pixels_not_in_coordinates():
    """The one unit trap in the API: 0.1 across is not 0.1 down on a 4:3 canvas."""
    s = Session(1024, 768, timelapse=False)
    x0, y0, x1, y1 = s.circle((0.5, 0.5), 0.1).bounds
    assert (x1 - x0) * 1024 == pytest.approx((y1 - y0) * 768, abs=1.0)


def test_a_wobbled_circle_is_round_too():
    s = Session(1024, 768, timelapse=False)
    x0, y0, x1, y1 = s.circle((0.5, 0.5), 0.1, wobble=0.2, seed=4).bounds
    # Wobble moves the outline, so this is roundness in the large, not to the pixel.
    assert (x1 - x0) * 1024 == pytest.approx((y1 - y0) * 768, rel=0.15)


def test_union_keeps_the_waist_that_hull_fills_in():
    """Two circles and a waist is a pear. A hull of the same two is a lozenge."""
    s = Session(1024, 768, timelapse=False)
    top, body = s.circle((0.45, 0.44), 0.06), s.circle((0.45, 0.60), 0.09)
    assert union(top, body).area < hull([top, body]).area


def test_union_refuses_shapes_that_do_not_touch():
    """Silently returning the larger of two masses is the failure worth refusing."""
    s = Session(1024, 768, timelapse=False)
    with pytest.raises(ValueError, match="do not all touch"):
        union(s.circle((0.1, 0.1), 0.03), s.circle((0.9, 0.9), 0.03))


def test_union_needs_more_than_one_shape():
    s = Session(1024, 768, timelapse=False)
    with pytest.raises(ValueError, match="at least two shapes"):
        union(s.circle((0.5, 0.5), 0.1))


def test_smooth_cuts_the_corners_and_keeps_the_mass():
    """A silhouette a brush can follow, from a shape built out of a few points."""
    square = Session(600, 600, timelapse=False).circle(cell("D5"), 0.2, wobble=0.4, seed=1)
    rounder = square.smooth()
    assert len(rounder.points) == len(square.points) * 4
    # Corner cutting pulls slightly inside the original, and only slightly.
    assert 0.8 < rounder.area / square.area < 1.0


def test_smoothing_nothing_changes_nothing():
    shape = Session(600, 600, timelapse=False).circle(cell("D5"), 0.2)
    assert shape.smooth(0).points == shape.points


# -- palette.at_value(): reaching a value from either side -----------------------------
@pytest.mark.parametrize("target", [0.20, 0.35, 0.50, 0.75])
def test_at_value_hits_the_value_from_either_side(target):
    """The guide's helper only added white, so it could only go up."""
    p = Palette()
    dark = p.mix("ultramarine", "burnt_umber", 0.4)
    assert p.value_of(p.at_value(dark, target)) == pytest.approx(target, abs=1e-3)
    assert p.value_of(p.at_value("yellow_ochre", target)) == pytest.approx(target, abs=1e-3)


def test_at_value_returns_the_base_when_it_is_already_there():
    p = Palette()
    assert p.hex(p.at_value("yellow_ochre", p.value_of("yellow_ochre"))) == p.hex("yellow_ochre")


@pytest.mark.parametrize("target", [0.99, 0.02])
def test_at_value_raises_rather_than_handing_back_the_wrong_value(target):
    """A painter who asks for 0.30 and is given 0.41 finds out a mass later."""
    with pytest.raises(ValueError, match="out of reach"):
        Palette().at_value("yellow_ochre", target)


# -- compare() against a plan ----------------------------------------------------------
def test_compare_measures_the_canvas_against_a_written_value_plan(tmp_path):
    """With no photograph the planned values live only in the painter's head.

    Nothing checked the canvas against them, which is half the precision tooling
    unavailable to anyone painting from a subject they imagined.
    """
    s = make(tmp_path)
    sky, ground = span("A1", "H4"), span("A5", "H8")
    s.block_in(sky, "flat", s.palette.at_value("cerulean", 0.72), size=0.09)
    s.block_in(ground, "flat", s.palette.at_value("burnt_umber", 0.35), size=0.09)

    result = s.compare({sky: 0.72, ground: 0.35})
    assert result.against == "plan"
    assert "delta = canvas - plan" in str(result)
    assert result.max_delta < 0.10
    assert result.path.exists()
    assert not result.off


def test_compare_against_a_plan_names_the_place_that_is_out(tmp_path):
    s = make(tmp_path)
    ground = span("A5", "H8")
    s.block_in(ground, "flat", s.palette.at_value("burnt_umber", 0.30), size=0.09)
    result = s.compare({ground: 0.80})           # painted far darker than planned
    assert [c.label for c in result.off] == [ground.name.upper()]
    assert result.off[0].delta < -0.10


def test_a_plan_key_has_to_be_a_place(tmp_path):
    s = make(tmp_path)
    with pytest.raises(KeyError, match="not a place"):
        s.compare({"the sky": 0.7})


def test_an_empty_plan_is_refused(tmp_path):
    with pytest.raises(ValueError, match="empty plan"):
        make(tmp_path).compare({})


def test_a_planned_value_is_a_value(tmp_path):
    with pytest.raises(ValueError, match="runs 0..1"):
        make(tmp_path).compare({cell("D5"): 42})


# -- smaller time-lapses ---------------------------------------------------------------
def test_every_and_scale_make_a_smaller_gif(tmp_path):
    """235 marks made a 2.6 MB GIF, and consecutive frames differ by one stroke."""
    s = make(tmp_path, timelapse=True)
    for i in range(20):
        s.dab(0.1 + i * 0.04, 0.5, "round_hard", "burnt_umber")

    full = s.timelapse_gif(tmp_path / "full.gif")
    small = s.timelapse_gif(tmp_path / "small.gif", every=4, scale=120)
    with Image.open(full) as a, Image.open(small) as b:
        assert b.n_frames < a.n_frames
        assert max(b.size) <= 120
    assert small.stat().st_size < full.stat().st_size


def test_thinning_still_ends_on_the_finished_painting(tmp_path):
    """A time-lapse that stops one stroke short is the wrong picture, however small."""
    s = make(tmp_path, timelapse=True)
    for i in range(10):
        s.dab(0.1 + i * 0.08, 0.5, "round_hard", "burnt_umber")
    last = s.history._frames[-1]
    s.timelapse_gif(tmp_path / "t.gif", every=4)
    assert np.array_equal(s.history._frames[-1], last)


@pytest.mark.parametrize("every", [0, -1])
def test_every_keeps_every_nth_frame_so_it_is_at_least_one(tmp_path, every):
    s = make(tmp_path, timelapse=True)
    s.dab(0.5, 0.5)
    with pytest.raises(ValueError, match="at least 1"):
        s.timelapse_gif(tmp_path / "t.gif", every=every)


# -- where a loaded session writes ------------------------------------------------------
def test_a_session_that_writes_somewhere_foreign_says_so(tmp_path):
    """Loading a .easel someone handed you used to write wherever they set out_dir,
    silently. The path is still honoured -- it is no longer silent."""
    elsewhere = tmp_path / "theirs" / "out"
    session = Session(64, 48, timelapse=False, out_dir=elsewhere)
    path = session.save(tmp_path / "mine" / "p.easel")
    with pytest.warns(UserWarning, match="neither in the working directory"):
        Session.load(path)


def test_looks_beside_the_painting_are_not_worth_a_warning(tmp_path):
    """The normal arrangement. A warning that fires on every load is not read."""
    session = Session(64, 48, timelapse=False, out_dir=tmp_path / "out")
    path = session.save(tmp_path / "p.easel")
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        Session.load(path)


# -- the shell: rehearsing a pass, and a prelude -----------------------------------------
def test_rehearsing_a_pass_commits_nothing(tmp_path, capsys):
    """About sixty of the pears painting's 224 strokes went on masses laid once and
    disliked. Every one was a pass that could have been rehearsed and was not,
    because rehearsing meant retyping the pass as a plan."""
    session = tmp_path / "p.easel"
    assert main(["new", str(session), "--size", "320x240", "--out-dir",
                 str(tmp_path / "out"), "--budget", "50"]) == 0
    script = tmp_path / "pass.py"
    script.write_text('s.block_in("D5", "flat", "burnt_umber", size=0.06)\n')

    assert main(["run", str(session), str(script), "--rehearse"]) == 0
    out = capsys.readouterr().out
    assert "Nothing committed" in out and "of the 50 left" in out
    assert Session.load(session).stroke_count == 0        # the file is untouched

    assert main(["run", str(session), str(script)]) == 0
    assert Session.load(session).stroke_count > 0


def test_a_prelude_beside_the_session_is_loaded_and_announced(tmp_path, capsys):
    """Helpers had to be loaded with exec(open(...).read()) at the top of every pass."""
    session = tmp_path / "p.easel"
    main(["new", str(session), "--size", "320x240", "--out-dir", str(tmp_path / "out")])
    (tmp_path / "prelude.py").write_text('def band(a, b):\n    return (0.0, a, 1.0, b)\n')
    script = tmp_path / "pass.py"
    script.write_text('s.block_in(band(0.1, 0.4), "flat", "burnt_umber", size=0.06)\n')

    assert main(["run", str(session), str(script)]) == 0
    assert "Prelude:" in capsys.readouterr().out
    assert Session.load(session).stroke_count > 0

    # And it can be turned off, which is the only way to prove it was doing anything.
    assert main(["run", str(session), str(script), "--no-prelude"]) == 1


def test_a_prelude_that_raises_stops_before_the_pass_starts(tmp_path):
    session = make(tmp_path)
    result = run_script(session, 's.stroke([(0.1, 0.1), (0.5, 0.5)])',
                        "pass.py", prelude="raise RuntimeError('bad helper')")
    assert result.code == 1
    assert not result.save
    assert session.stroke_count == 0
