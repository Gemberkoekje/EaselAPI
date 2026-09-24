"""The engine changes the painting sessions asked for, and what each one is for.

Two painters took the guide at its word, painted from it with no reference, and
wrote down what the engine had cost them: a still life, then the inside of a car
wash. Every test here guards one item from those lists, so the reason for each is
the same shape: a painter spent strokes, or spent attention, on something the engine
could have held.

Two of them are really about arithmetic agreeing with itself -- ``cost`` quoting what
``paint`` charges, a rehearsal landing where the painting lands -- and those matter
more than they look. A plan that is checked and then retyped is a plan that drifts,
and the drift arrives as paint.

Where a test could ask the API what it did, it asks the canvas instead.
"""

from __future__ import annotations

import math
import re
import warnings
from contextlib import nullcontext

import numpy as np
import pytest
from PIL import Image

from easel import (
    Polygon,
    Region,
    Session,
    blob,
    brush,
    cell,
    ellipse,
    hull,
    polygon,
    ribbon,
    roughen,
    span,
    union,
)
from easel.cli import main, run_script
from easel.palette import Palette
from easel.session import GLAZE_OPACITY


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
    # It buried: the middle of the cell is lighter than the blue it covered. D5 is
    # x 120-160, y 120-150 here; the window used to sit on its corner, which only a
    # burial that ran past the cell could lighten.
    mid = (slice(125, 145), slice(125, 155))
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
    assert Session.load(session).stroke_count == 0        # the painting is untouched

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


# ======================================================================================
# The second session: the car wash. A painter who had read the repo, painting through
# the shell, who probed every claim before writing it down -- and whose probes caught
# one of the first session's numbers as well as six of the engine's own.
# ======================================================================================

# -- scumble(direction="inward"): a value falling off from a point ---------------------
def _values_at(s, points):
    v = s.canvas.values() / 255.0
    h, w = v.shape
    return [float(v[int(y * h), int(x * w)]) for x, y in points]


def test_a_centred_scumble_falls_off_from_the_middle_in_both_directions(tmp_path):
    """The band version grades edge to edge, which is a band and not a glow. A lit
    patch goes dark at every edge, and the hand-rolled answer -- strokes radiating
    from a shared centre -- comes back as a daisy."""
    s = make(tmp_path)
    patch = s.circle((0.5, 0.5), 0.22, wobble=0.1, seed=2)
    s.scumble(patch, "burnt_umber", "titanium_white", 9, direction="inward", size=0.07)

    left, centre, right = _values_at(s, [(0.32, 0.5), (0.5, 0.5), (0.68, 0.5)])
    top, bottom = _values_at(s, [(0.5, 0.32), (0.5, 0.68)])
    assert centre > left and centre > right, "it did not fall off across the patch"
    assert centre > top and centre > bottom, "it did not fall off down the patch"


def test_a_centred_scumble_costs_the_passes_it_was_asked_for(tmp_path):
    """Charged as n, the same as the band version, so a glow can be budgeted."""
    s = make(tmp_path)
    assert len(s.scumble(s.circle((0.5, 0.5), 0.2), "burnt_umber", "titanium_white",
                         8, direction="inward", size=0.06)) == 8


def test_a_centred_scumble_ends_on_the_colour_it_was_given(tmp_path):
    """color_a on the boundary and color_b in the middle, whichever way round the
    painter wants the light."""
    s = make(tmp_path)
    records = s.scumble(s.circle((0.5, 0.5), 0.2), "burnt_umber", "titanium_white", 6,
                        direction="inward", size=0.06)
    values = [Palette().value_of(r.color_hex) for r in records]
    assert values == sorted(values)
    assert records[0].color_hex.lower() == Palette().hex("burnt_umber").lower()


# -- block_in(solid=True): density spaces the passes, it does not fill them ------------
def _interior(s, place, margin):
    v = s.canvas.values() / 255.0
    h, w = v.shape
    x0, y0, x1, y1 = place.bounds
    return v[int((y0 + margin) * h):int((y1 - margin) * h),
             int((x0 + margin) * w):int((x1 - margin) * w)]


def test_a_solid_block_in_is_solid_and_costs_the_same(tmp_path):
    """density=1.0 looks like a request for a solid mass and is not one: the passes
    still run dry along their length. Measured, the interior goes from sd 0.063 with
    4.4% of it still within 0.05 of bare ground to sd 0.007 and none, for the same
    passes and the same money."""
    place = span("B2", "G6")
    kw = dict(brush="flat", color="burnt_umber", size=0.030, density=1.0)
    speckled, solid = make(tmp_path), make(tmp_path)
    ground = _interior(speckled, place, 0.030).copy()
    n_speckled = len(speckled.block_in(place, **kw))
    n_solid = len(solid.block_in(place, solid=True, **kw))

    assert n_solid == n_speckled, "solid paint is not more passes"
    assert _interior(solid, place, 0.030).std() < _interior(speckled, place, 0.030).std() / 4
    bare = np.abs(_interior(solid, place, 0.030) - ground) < 0.05
    assert not bare.any(), "solid paint left bare ground inside the mass"


def test_asking_for_a_starved_brush_beside_it_still_gets_one(tmp_path):
    """`solid` is a pair of defaults, not an override. A painter who says load=0.2
    means it."""
    s = make(tmp_path)
    records = s.block_in(cell("D5"), "flat", "burnt_umber", size=0.06, solid=True,
                         load=0.2)
    assert records[0].params["load"] == pytest.approx(0.2)
    assert records[0].params["load_falloff"] == pytest.approx(0.0)


# -- the round tips stop repeating themselves -----------------------------------------
def _silhouettes(s, tip, **kw):
    """Two marks of the same tip, each cropped to its own box."""
    out = []
    for x in (0.3, 0.7):
        before = s.canvas.rgb.copy()
        s.dab(x, 0.5, tip, "titanium_white", size=0.05, press=3, **kw)
        changed = np.abs(s.canvas.rgb - before).max(axis=2) > 0.01
        ys, xs = np.nonzero(changed)
        out.append(changed[ys.min():ys.max() + 1, xs.min():xs.max() + 1])
    return out


def _overlap(a, b):
    h, w = max(a.shape[0], b.shape[0]), max(a.shape[1], b.shape[1])
    pads = []
    for m in (a, b):
        pad = np.zeros((h, w), bool)
        oy, ox = (h - m.shape[0]) // 2, (w - m.shape[1]) // 2
        pad[oy:oy + m.shape[0], ox:ox + m.shape[1]] = m
        pads.append(pad)
    return float((pads[0] & pads[1]).sum() / max((pads[0] | pads[1]).sum(), 1))


def test_a_wobbled_round_tip_does_not_print_the_same_mark_twice(tmp_path):
    """Five round dabs are five copies of one disc, and a painter who wants a small
    irregular mark lays them, looks, and lays them again. The comb is redrawn per
    stroke for exactly this reason; so is this."""
    plain = _overlap(*_silhouettes(make(tmp_path), "round_hard"))
    wobbled = _overlap(*_silhouettes(make(tmp_path), "round_hard", tip_wobble=0.7))
    assert plain > 0.9, "two plain dabs should be near enough the same disc"
    assert wobbled < plain - 0.1, "the wobbled marks repeated themselves"


def test_the_disc_is_still_there_when_nothing_asks_for_a_wobble(tmp_path):
    """Every painting made before this one replays as it was: the default is 0, and
    at 0 the stamp is the disc it always was."""
    a, b = make(tmp_path), make(tmp_path)
    a.dab(0.5, 0.5, "round_hard", "titanium_white", size=0.05, press=3)
    b.dab(0.5, 0.5, "round_hard", "titanium_white", size=0.05, press=3, tip_wobble=0.0)
    assert np.array_equal(a.canvas.rgb, b.canvas.rgb)


def test_a_wobble_is_a_fraction_of_the_radius(tmp_path):
    s = make(tmp_path)
    with pytest.raises(ValueError, match="0 to 1"):
        s.dab(0.5, 0.5, "round_hard", "titanium_white", tip_wobble=1.4)


# -- a clean edge does not inset across the canvas frame -------------------------------
def _bottom_row_unpainted(session, shape, **kw):
    """How much of the canvas's last row the mass left as bare ground."""
    ground = session.canvas.values()[-1] / 255.0
    session.block_in(shape, solid=True, **kw)
    return float(np.mean(np.abs(session.canvas.values()[-1] / 255.0 - ground) < 0.02))


def test_a_clean_edge_still_runs_off_the_canvas(tmp_path):
    """The inset is there so the brush's outer half lands on the drawn line. Where the
    outline leaves the canvas there is no line to land on, and insetting it anyway
    holds the mass half a brush off the frame: the same mass, filled clean with the
    inset applied all the way round, leaves 17% of the bottom row as bare ground.

    Laid solid, so that what is being measured is where the fill stopped and not a
    pass running dry at its far end.
    """
    mass = polygon([(-0.05, 0.70), (0.50, 0.73), (1.05, 0.70), (1.05, 1.05), (-0.05, 1.05)])
    kw = dict(brush="flat", color="burnt_umber", size=0.16)
    assert _bottom_row_unpainted(make(tmp_path), mass, edge="ragged", **kw) == 0.0
    assert _bottom_row_unpainted(make(tmp_path), mass, edge="clean", **kw) == 0.0


def test_a_mass_inside_the_canvas_is_inset_exactly_as_before(tmp_path):
    """The frame rule fires on an outline that reaches the frame and nowhere else."""
    shape = make(tmp_path).circle((0.5, 0.5), 0.16)
    from easel.session import _clean_fill
    assert _clean_fill(shape, 0.03).points == shape.inset(0.03).points


def test_a_clean_edge_at_the_frame_is_priced_as_it_is_painted(tmp_path):
    """The quote walks the same inset the paint does, frame and all."""
    mass = polygon([(0.05, 0.70), (0.95, 0.72), (0.95, 1.05), (0.05, 1.05)])
    spec = {"shape": mass, "brush": "flat", "color": "burnt_umber",
            "size": 0.06, "edge": "clean"}
    s = make(tmp_path)
    assert len(s.paint(spec)) == make(tmp_path).cost(spec)


# -- a rehearsal's looks are numbered apart from the painting's ------------------------
def test_two_rehearsals_can_be_put_side_by_side(tmp_path, capsys):
    """Rehearsing is what a painter does repeatedly, to compare versions of one pass.
    The look counter restarted on every rehearsal, so each one wrote over the last --
    and over the painting's own look_001.png before that."""
    session = tmp_path / "p.easel"
    out = tmp_path / "out"
    assert main(["new", str(session), "--size", "320x240", "--out-dir", str(out)]) == 0
    script = tmp_path / "pass.py"
    script.write_text('s.block_in("D5", "flat", "burnt_umber", size=0.06)\n')

    main(["run", str(session), str(script)])
    main(["look", str(session)])
    capsys.readouterr()
    main(["run", str(session), str(script), "--rehearse"])
    main(["run", str(session), str(script), "--rehearse"])

    printed = capsys.readouterr().out
    assert "rehearse_001.png" in printed and "rehearse_002.png" in printed
    assert sorted(p.name for p in out.glob("*.png")) == [
        "look_001.png", "rehearse_001.png", "rehearse_002.png"]


def test_a_scrap_of_canvas_does_not_write_over_the_painting_in_python_either(tmp_path):
    """`easel run --rehearse` is `scratch()` from the shell, and the same defect."""
    s = make(tmp_path)
    s.look()
    assert s.scratch().look().name == "rehearse_001.png"
    assert (tmp_path / "look_001.png").exists()


# -- cost() says why a number is large -------------------------------------------------
def test_cost_names_the_crossing_that_doubled_it(tmp_path):
    s = make(tmp_path)
    spec = {"shape": span("A4", "H5"), "brush": "bristle", "size": 0.05}
    assert "directions" not in s.cost_line(spec)
    crossed = s.cost_line(dict(spec, direction="cross"))
    assert "2 directions" in crossed
    assert s.cost(dict(spec, direction="cross")) > s.cost(spec)


def test_cost_names_the_box_the_passes_step_across(tmp_path):
    """A ribbon pays for the box its bend sweeps out, not for its own width, and the
    number alone sends a painter off to redesign the shape."""
    s = make(tmp_path)
    bent = ribbon([(0.15, 0.8), (0.5, 0.35), (0.9, 0.75)], 0.032)
    line = s.cost_line({"shape": bent, "brush": "bristle", "size": 0.015})
    assert "stepping across" in line and "pieces by the outline" in line


def test_the_budget_warning_says_what_the_big_entry_is_doing(tmp_path):
    s = make(tmp_path, budget=60)
    with pytest.warns(UserWarning, match="directions"):
        s.cost({"shape": span("A4", "H5"), "brush": "bristle", "size": 0.05,
                "direction": "cross"})


def test_the_breakdown_adds_up_to_what_cost_says(tmp_path):
    s = make(tmp_path)
    plan = [{"shape": s.circle((0.5, 0.5), 0.16), "brush": "flat", "size": 0.06},
            {"edge": [(0.05, 0.75), (0.5, 0.72), (0.95, 0.78)], "into": "down",
             "depth": 0.12, "size": 0.05},
            {"points": [(0.2, 0.3), (0.6, 0.35)]}]
    assert sum(n for n, _ in s.cost_of(plan)) == s.cost(plan)
    assert [bool(why) for _, why in s.cost_of(plan)] == [True, True, False]


# -- smudge follows a boundary, and a shape is one -------------------------------------
# 0.04 is the size the bend measurement in CALIBRATION.md was taken at, and these
# three tests are about *which points* a pass is given rather than how wide it is, so
# they keep it and ignore the advice the engine now gives about anything over 0.03.
@pytest.mark.filterwarnings(r"ignore:smudge\(size=:UserWarning")
def test_a_smudge_walks_a_shape_s_own_outline(tmp_path):
    """Following a curve meant sampling coordinates off it by hand, which is the step
    a painter skips -- and the guide's examples, every one of them two points, are
    what teaches them to skip it."""
    s = make(tmp_path)
    mass = s.circle((0.5, 0.5), 0.2)
    s.block_in(mass, "flat", "burnt_umber", size=0.08)
    record = s.smudge(mass, size=0.04)
    assert len(record.points) > 8, "a shape came back as a straight pass"
    assert all(mass.box.inset(-0.05).bounds[0] <= x for x, _ in record.points)


@pytest.mark.filterwarnings(r"ignore:smudge\(size=:UserWarning")
def test_a_run_of_points_is_still_used_exactly_as_given(tmp_path):
    """Every smudge ever made with two points still lands where it landed."""
    s = make(tmp_path)
    points = [(0.30, 0.40), (0.38, 0.41)]
    assert np.allclose(s.smudge(points, size=0.04).points, points, atol=1e-6)


#: A boundary with a bend in it: light above, dark below, and a curve that a painter
#: reading two points off it would flatten into the chord between its ends.
_BEND_X0, _BEND_X1 = 0.30, 0.70


def _bend_y(x):
    t = (x - _BEND_X0) / (_BEND_X1 - _BEND_X0)
    return 0.40 + 0.09 * t + 0.06 * np.sin(np.pi * t)


def _with_a_bent_boundary(tmp_path):
    """Two masses meeting along that curve, dry, on a canvas big enough to measure."""
    s = Session(640, 480, texture="linen", ground="toned_grey", seed=7,
                timelapse=False, out_dir=tmp_path)
    xs = np.linspace(-0.05, 1.05, 24)
    edge = [(float(x), float(_bend_y(np.clip(x, _BEND_X0, _BEND_X1))
                            + 0.225 * (x - np.clip(x, _BEND_X0, _BEND_X1))))
            for x in xs]
    s.block_in(polygon([(-0.05, 0.05), (1.05, 0.05), *edge[::-1]]), "flat",
               "titanium_white", size=0.10, solid=True)
    s.block_in(polygon([*edge, (1.05, 0.98), (-0.05, 0.98)]), "flat",
               "burnt_umber", size=0.10, solid=True)
    s.dry()
    return s


def _boundary_line(s):
    """Where the light meets the dark, column by column, as a fraction of the height."""
    v = s.canvas.values() / 255.0
    h, w = v.shape
    out = []
    for column in range(int((_BEND_X0 + 0.02) * w), int((_BEND_X1 - 0.02) * w)):
        lo = int((_bend_y(column / w) - 0.09) * h)
        hi = int((_bend_y(column / w) + 0.09) * h)
        strip = v[lo:hi, column]
        middle = 0.5 * (float(strip[:6].mean()) + float(strip[-6:].mean()))
        crossings = np.nonzero((strip[:-1] - middle) * (strip[1:] - middle) <= 0)[0]
        out.append((lo + float(crossings[0])) / h if len(crossings) else np.nan)
    return np.array(out)


@pytest.mark.filterwarnings(r"ignore:smudge\(size=:UserWarning")
def test_a_smudge_along_a_curve_moves_the_boundary_less_than_its_chord(tmp_path):
    """Two points on a bend give a pass that starts along the boundary and ends across
    it: the same thumbprint, arriving more slowly. On a straight edge the two are the
    same pass to the pixel, which is why every two-point example in the guide read as
    permission to flatten a curve."""
    def moved(points):
        s = _with_a_bent_boundary(tmp_path)
        before = _boundary_line(s)
        s.smudge(points, size=0.04)
        return float(np.nanmean(np.abs(_boundary_line(s) - before)))

    ends = [(_BEND_X0, float(_bend_y(_BEND_X0))), (_BEND_X1, float(_bend_y(_BEND_X1)))]
    chord = moved(ends)
    along = moved([(float(x), float(_bend_y(x)))
                   for x in np.linspace(_BEND_X0, _BEND_X1, 4)])
    assert along < chord * 0.6, f"the curve moved the boundary {along}, the chord {chord}"


# ======================================================================================
# The third session: a lighthouse at dusk. A painter who had read the repo and both
# earlier paintings, and who probed every claim on a 512x384 canvas before writing it
# down. Their list is ordered by how many rehearsals each item would have saved, and
# so is this one: none of their strokes went on repainting, but eighteen rehearsals
# went on finding out what the verbs do.
# ======================================================================================

# -- scumble(direction="inward"): the brush comes from the ring step -------------------
def _flat_share(s, place, value, window=0.06):
    """The share of a patch sitting within ``window`` of one value: how much of a
    fall-off has been buried flat by rings wider than the step between them."""
    v = s.canvas.values() / 255.0
    mask = place.mask(s.canvas.width, s.canvas.height)
    return float(((np.abs(v - value) < window) & mask).sum() / mask.sum())


def test_a_centred_scumble_sizes_its_own_brush_from_its_ring_step(tmp_path):
    """The rings step ``depth / n`` apart and each is laid over the ones before it, so
    a brush much wider than the step buries the first rings under the last: the middle
    comes back one flat colour with a rim of ramp round it, which is a sun and not a
    glow. The guide's example gives no ``size=``, so it ran at the bristle's default
    0.11 -- five steps wide on any patch a painter would call a glow. Three rehearsals,
    and the verb was abandoned for hand-rolled strokes that do less than it could."""
    patch = make(tmp_path).circle((0.5, 0.5), 0.2)

    picked = make(tmp_path)
    picked.scumble(patch, "burnt_umber", "titanium_white", 7, direction="inward")
    preset = make(tmp_path)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        preset.scumble(patch, "burnt_umber", "titanium_white", 7, direction="inward",
                       size=0.11)

    lit = Palette().value_of("titanium_white")
    assert _flat_share(preset, patch, lit) > _flat_share(picked, patch, lit) * 1.5, (
        "the picked brush buried as much of the patch as the preset's default did"
    )


def test_a_centred_scumble_says_when_the_brush_it_was_given_will_fill(tmp_path):
    """It still lays what it was asked for -- an explicit size is a painter's choice --
    but the choice is no longer silent. The same shape of warning ``cost()`` gives a
    plan that would eat the budget."""
    s = make(tmp_path)
    with pytest.warns(UserWarning, match="ring"):
        s.scumble(s.circle((0.5, 0.5), 0.2), "burnt_umber", "titanium_white", 7,
                  direction="inward", size=0.11)

    with warnings.catch_warnings():
        warnings.simplefilter("error")            # a brush inside the step is silent
        s.scumble(s.circle((0.5, 0.5), 0.2), "burnt_umber", "titanium_white", 7,
                  direction="inward", size=0.03)


# -- easel run: several passes in order, against one copy ------------------------------
def _two_passes(tmp_path):
    a = tmp_path / "a.py"
    a.write_text('s.block_in("C3", "flat", "burnt_umber", size=0.06)\n')
    b = tmp_path / "b.py"
    b.write_text('s.stroke([(0.3, 0.6), (0.7, 0.62)], "flat", "titanium_white",'
                 ' size=0.05)\n')
    return a, b


def test_running_two_passes_together_is_running_them_one_after_the_other(tmp_path):
    """A pass that goes on top of another pass has to be judged on it, and the wrapper
    that did it -- a script that ``exec()``s each file -- was in nobody's log. Worth
    having only if it is the same painting either way, so that is what is asserted."""
    a, b = _two_passes(tmp_path)
    together, apart = tmp_path / "one.easel", tmp_path / "two.easel"
    for path in (together, apart):
        assert main(["new", str(path), "--size", "320x240", "--seed", "5",
                     "--out-dir", str(tmp_path / "out")]) == 0

    assert main(["run", str(together), str(a), str(b)]) == 0
    assert main(["run", str(apart), str(a)]) == 0
    assert main(["run", str(apart), str(b)]) == 0

    one, two = Session.load(together), Session.load(apart)
    assert one.stroke_count == two.stroke_count
    assert np.array_equal(one.canvas.rgb, two.canvas.rgb), (
        "two passes run together did not land where they land run separately"
    )


def test_rehearsing_several_passes_lays_them_on_one_copy(tmp_path, capsys):
    """The sea and the rocks were rehearsed together five times, and the three
    finishing passes once. One copy, in order, and nothing committed."""
    a, b = _two_passes(tmp_path)
    session = tmp_path / "p.easel"
    assert main(["new", str(session), "--size", "320x240", "--out-dir",
                 str(tmp_path / "out"), "--budget", "60"]) == 0

    assert main(["run", str(session), str(a), str(b), "--rehearse"]) == 0
    out = capsys.readouterr().out
    assert "a.py, b.py" in out and "Nothing committed" in out
    assert Session.load(session).stroke_count == 0

    # The count is both passes, not just the last one.
    rehearsed = int(out.split("Rehearsed")[1].split(" strokes")[0].split(":")[1])
    assert main(["run", str(session), str(a), str(b)]) == 0
    assert Session.load(session).stroke_count == rehearsed


def test_a_pass_that_fails_keeps_what_the_passes_before_it_painted(tmp_path, capsys):
    """The rule a single pass already follows -- a half-finished pass is still work --
    reaching across the sequence, and saying which one stopped it."""
    a, _ = _two_passes(tmp_path)
    bad = tmp_path / "bad.py"
    bad.write_text("def (\n")                      # does not parse: nothing of its own
    session = tmp_path / "p.easel"
    main(["new", str(session), "--size", "320x240", "--out-dir", str(tmp_path / "out")])

    assert main(["run", str(session), str(a), str(bad)]) == 1
    assert "after a.py" in capsys.readouterr().err
    assert Session.load(session).stroke_count > 0


# -- a rehearsal can be diffed against the painting ------------------------------------
def test_a_rehearsal_diffs_against_the_painting_it_is_a_copy_of(tmp_path):
    """``look(diff=True)`` inside a rehearsal had nothing to diff against: the copy's
    last look was empty, so the one question a rehearsal exists to answer -- what would
    this pass change -- could not be asked of it as a tint."""
    s = make(tmp_path)
    s.block_in("C3", "flat", "burnt_umber", size=0.06)
    s.look()

    trial = s.scratch()
    assert trial._last_look is not None
    trial.block_in("F6", "flat", "titanium_white", size=0.06)

    tinted = np.asarray(Image.open(trial.look(diff=True)).convert("RGB"),
                        dtype=np.float32)
    plain = np.asarray(Image.open(trial.look()).convert("RGB"), dtype=np.float32)

    def redness(img, place):
        x0, y0, x1, y1 = s.canvas.region_px(cell(place))
        crop = img[y0:y1, x0:x1]
        return float((crop[..., 0] - 0.5 * (crop[..., 1] + crop[..., 2])).mean())

    # What the trial laid is tinted; what was already there when the look was taken
    # is knocked back instead.
    assert redness(tinted, "F6") > redness(plain, "F6") + 8
    assert redness(tinted, "C3") < redness(plain, "C3") + 8


# -- a pressure list reads the same way on every pass ----------------------------------
def _pass_ends(s, y0, y1):
    """How much paint landed at each end of a horizontal band."""
    rgb = np.asarray(s.canvas.rgb, dtype=np.float64)
    h, w = rgb.shape[:2]
    band = rgb[int(y0 * h):int(y1 * h), :, 0]
    return float(band[:, :int(0.12 * w)].mean()), float(band[:, int(0.88 * w):].mean())


# A deliberately narrow brush: these two measure where each pass runs *heavy*, which
# needs the passes to be separable, so they take the bars the verb now warns about.
@pytest.mark.filterwarnings(r"ignore:scumble\(\) with a brush:UserWarning")
def test_a_pressure_list_lands_the_same_way_round_on_every_pass(tmp_path):
    """Consecutive passes run in opposite directions, which is what keeps a stack from
    stacking all its run-out along one edge -- but the pressure profile went with them,
    so ``pressure=[0.0, 1.0]`` landed heavy at alternating ends: measured at 0.35/0.56,
    0.52/0.33, 0.35/0.57, 0.56/0.34. A passage meant to brighten toward one side could
    not be laid with the verb at all; six strokes of one painting's afterglow are
    hand-written for exactly this, and they are the strokes most likely to be wanted
    again."""
    s = make(tmp_path)
    s.scumble((0.1, 0.25, 0.9, 0.75), "cadmium_red", "cadmium_red", 4, brush="flat",
              size=0.08, direction=0, opacity=1.0, pressure=[0.0, 1.0])

    heavy_ends = []
    for i in range(4):
        lo, hi = _pass_ends(s, 0.26 + i * 0.125, 0.355 + i * 0.125)
        heavy_ends.append("right" if hi > lo else "left")
    assert heavy_ends == ["right"] * 4, heavy_ends


@pytest.mark.filterwarnings(r"ignore:scumble\(\) with a brush:UserWarning")
def test_a_mirrored_profile_lands_the_same_way_round_on_every_pass(tmp_path):
    """The same defect wearing a name: ``press_in`` is a pressure list with a word
    for it, and it flipped the same way. ``press_in`` and ``lift_off`` are each
    other's mirror, so the fix is to swap them rather than to reverse a curve."""
    s = make(tmp_path)
    s.scumble((0.1, 0.25, 0.9, 0.75), "cadmium_red", "cadmium_red", 4, brush="flat",
              size=0.08, direction=0, opacity=1.0, pressure="press_in")

    heavy_ends = []
    for i in range(4):
        lo, hi = _pass_ends(s, 0.26 + i * 0.125, 0.355 + i * 0.125)
        heavy_ends.append("right" if hi > lo else "left")
    assert heavy_ends == ["right"] * 4, heavy_ends


def test_the_default_profile_is_left_exactly_as_it_was(tmp_path):
    """``taper`` is its own mirror image, so it goes through untouched rather than
    being reversed into an equal-but-differently-computed array. Every painting made
    here before this was laid at ``taper``, and they all still replay."""
    def lay(pressure):
        s = make(tmp_path)
        s.block_in((0.1, 0.25, 0.9, 0.75), "flat", "burnt_umber", size=0.08,
                   direction="horizontal", pressure=pressure)
        return np.array(s.canvas.rgb)

    assert np.array_equal(lay("taper"), lay("taper"))
    assert not np.array_equal(lay("taper"), lay("press_in"))


# -- sample(): the colour that is already there ----------------------------------------
def test_sampling_the_canvas_gives_a_colour_the_palette_takes_as_itself(tmp_path):
    """The canvas holds linear light and a plain (r, g, b) tuple is read as sRGB, so a
    mean read off ``s.canvas.rgb`` and handed back as a tuple comes back a different
    colour: a toned_grey ground reads 0.53, its own mean as a tuple reads 0.25. It cost
    one painter a rehearsal -- a halo's outer rings, meant to be the sky's own colour,
    landed near black."""
    s = make(tmp_path)
    p = s.palette
    ground = p.value_of(s.sample())

    lin = np.asarray(s.canvas.rgb, dtype=np.float64).reshape(-1, 3).mean(axis=0)
    p["by_tuple"] = tuple(float(v) for v in lin)
    p["by_sample"] = s.sample()

    assert p.value_of("by_sample") == pytest.approx(ground, abs=0.005)
    assert abs(p.value_of("by_tuple") - ground) > 0.2       # the trap it replaces


def test_sampling_reads_the_place_it_was_given(tmp_path):
    s = make(tmp_path)
    s.block_in("C3", "flat", "titanium_white", size=0.06, solid=True)
    s.block_in("F6", "flat", "burnt_umber", size=0.06, solid=True)
    p = s.palette
    assert p.value_of(s.sample(cell("C3"))) > p.value_of(s.sample())
    assert p.value_of(s.sample(cell("F6"))) < p.value_of(s.sample())


def test_sampling_a_shape_reads_the_shape_and_not_its_box(tmp_path):
    """A halo ring, a moon's dark side and a repair are all shapes, and the box round
    a shape is mostly what the shape is not."""
    s = make(tmp_path)
    dark = s.circle((0.5, 0.5), 0.18)
    s.block_in(dark, "flat", "burnt_umber", size=0.05, solid=True)
    assert s.palette.value_of(s.sample(dark)) < s.palette.value_of(s.sample(dark.box))


# -- a clean edge draws the line the painter drew --------------------------------------
def test_the_contour_of_a_clean_edge_does_not_wander(tmp_path):
    """The bargain of ``edge="clean"`` is that the outer half of the brush lands on the
    line the painter drew, and a wander carried by three draws moves whole sections of
    the contour off it at once. One painter filled a ridge clean, got a row of rounded
    knobs along the top, and could not tell whether it was the wander or the outline's
    own corners under a wide brush. It is the wander: the brush's ``jitter``, which is
    what they reached for, does not move this at all."""
    ridge = polygon([(-0.05, 0.40), (0.15, 0.36), (0.35, 0.42), (0.55, 0.34),
                     (0.75, 0.40), (1.05, 0.36), (1.05, 1.05), (-0.05, 1.05)])

    def top_line(seed, wander):
        # Its own seed each time: what the wander costs is how far the contour moves
        # off the drawn line when nothing but the draw behind it has changed.
        s = Session(320, 240, texture="linen", ground="toned_grey", seed=seed,
                    out_dir=tmp_path, timelapse=False)
        before = np.array(s.canvas.rgb)
        if wander:                       # what the contour used to get
            real = s._sweep_wobble

            def wobble(at, length, step, ring, _on=True):
                return real(at, length, step, ring, True)

            s._sweep_wobble = wobble
        s.block_in(ridge, "flat", "burnt_umber", size=0.08, density=1.0, solid=True,
                   direction="horizontal", edge="clean")
        painted = np.abs(np.asarray(s.canvas.rgb) - before).sum(axis=2) > 0.01
        h, w = painted.shape
        tops = []
        for x in range(int(0.1 * w), int(0.9 * w)):
            rows = np.flatnonzero(painted[:, x])
            tops.append(float(rows[0]) if len(rows) else np.nan)
        return float(np.nanmean(tops))

    def drift(wander):
        """How far the whole contour sits off the drawn line, seed to seed."""
        return float(np.std([top_line(seed, wander) for seed in range(6)]))

    assert drift(False) < drift(True) * 0.6, (
        f"the contour still wanders: {drift(False)} against {drift(True)}"
    )


# ======================================================================================
# The fourth session: a night street. 286 strokes of 300, 56 rehearsals, no repainted
# mass and no undo -- so its list is six things the engine could have held rather than
# six damaged passages. Two of its six carried a measurement; the other four were
# observed in rehearsal, and re-measuring them first is why two of the tests below
# guard an answer that is not the one the request asked for.
# ======================================================================================

# -- the paint and the view of it: one number, and it says which one it is --------------
def _lit_mass(tmp_path, **kw):
    """A mass laid over a wall, both solid, on a canvas big enough to average over."""
    s = Session(512, 384, texture="linen", ground="toned_grey", seed=5,
                out_dir=tmp_path, timelapse=False)
    s.palette["wall"] = s.palette.at_value("burnt_umber", 0.17)
    s.palette["fascia"] = s.palette.at_value("burnt_umber", 0.26)
    s.block_in((0.0, 0.0, 1.0, 1.0), "flat", "wall", size=0.05, solid=True)
    s.dry()
    s.block_in(Region(0.20, 0.35, 0.80, 0.55, name="fascia"), "flat", "fascia",
               size=0.030, **kw)
    return s, Region(0.22, 0.37, 0.78, 0.53, name="fascia")


def test_the_view_and_the_paint_report_the_same_value(tmp_path):
    """The request was for the two instruments to stop disagreeing about a solid mass.
    Measured, they never did: the relief is a *gradient*, so it lifts one side of every
    ridge of paint and drops the other by as much, and that cancels over any area larger
    than the ridge. What the session actually lacked was a way to ask -- so the repair is
    that the question is now one line, and the answer to it is *no difference*."""
    for solid in (False, True):
        s, inner = _lit_mass(tmp_path, solid=solid)
        paint = s.palette.value_of(s.sample(inner))
        view = s.palette.value_of(s.sample(inner, rendered=True))
        assert abs(view - paint) < 0.005, (
            f"solid={solid}: the view reads {view:.3f} against the paint's {paint:.3f}"
        )


def test_a_solid_mass_lands_where_it_was_mixed_in_the_view_too(tmp_path):
    """The same finding from the other side, and the one that matters to a value plan:
    ``solid=True`` sets maximum paint height, and maximum height is the case the request
    expected to read lightest in the view. It does not -- the exported picture and the
    values view agree to the thousandth."""
    s, inner = _lit_mass(tmp_path, solid=True)
    x0, y0, x1, y1 = s.canvas.region_px(inner)
    with_relief = s.canvas.to_srgb8(impasto=True)[y0:y1, x0:x1]
    without = s.canvas.to_srgb8(impasto=False)[y0:y1, x0:x1]
    assert abs(float(with_relief.mean()) - float(without.mean())) / 255.0 < 0.002


def test_compare_says_which_of_the_two_surfaces_it_measured(tmp_path):
    """A value plan that reads clean while the picture looks wrong is a table nobody can
    argue with, because it does not say what it measured. Now it does, and it names the
    call that reports the other one."""
    s, inner = _lit_mass(tmp_path, solid=True)
    table = s.compare({inner: 0.26}).table()
    assert "the paint" in table
    assert "rendered=True" in table


# -- a banded scumble sizes its own brush, the way the centred one does ----------------
def _band_ripple(s, band):
    """The across-band profile's own one-step ripple: what a stack of bars measures as."""
    v = s.canvas.values() / 255.0
    x0, y0, x1, y1 = s.canvas.region_px(band)
    inset = int(0.12 * (x1 - x0))
    profile = v[y0:y1, x0 + inset:x1 - inset].mean(axis=1)
    step_px = max(3, int(round(band.height / 8 * s.canvas.height)))
    smooth = np.convolve(profile, np.ones(step_px) / step_px, mode="same")
    core = slice(step_px, len(profile) - step_px)
    return float(np.abs(profile - smooth)[core].std())


def _scumbled(tmp_path, band, **kw):
    s = Session(640, 480, texture="linen", ground="toned_grey", seed=7,
                out_dir=tmp_path, timelapse=False)
    s.palette["a"] = s.palette.at_value("burnt_umber", 0.20)
    s.palette["b"] = s.palette.at_value("titanium_white", 0.70)
    records = s.scumble(band, "a", "b", 8, **kw)
    return s, records


def test_a_banded_scumble_sizes_its_own_brush_from_its_pass_step(tmp_path):
    """The centred case has picked its brush off its ring step since the third session;
    the banded case had the same failure and kept the preset's default, which is one to
    one and a half steps on an ordinary band -- the worst place on the curve. A painter
    lost the brightest mass in a painting to it twice and abandoned the verb."""
    band = Region(0.10, 0.30, 0.90, 0.70, name="band")
    s, records = _scumbled(tmp_path, band)
    step = band.height / 8
    assert records[0].params["size"] == pytest.approx(3.0 * step, rel=1e-6)

    with warnings.catch_warnings():         # the bars, on purpose, to measure them
        warnings.simplefilter("ignore", UserWarning)
        narrow, _ = _scumbled(tmp_path, band, size=step)
    assert _band_ripple(s, band) < _band_ripple(narrow, band) * 0.75, (
        "the brush it picks is no better than the one that left the bars"
    )


def test_a_banded_scumble_says_when_the_brush_it_was_given_will_stripe(tmp_path):
    """Named, the size is the painter's and is left alone -- with the same warning the
    centred case gives for the opposite mistake, because silence is what cost the
    rehearsals."""
    band = Region(0.10, 0.30, 0.90, 0.70, name="band")
    with pytest.warns(UserWarning, match="do not overlap"):
        _scumbled(tmp_path, band, size=0.02)
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        _scumbled(tmp_path, band, size=0.15)


def test_a_brush_handed_in_whole_is_still_the_painters_choice(tmp_path):
    """A ``Brush`` carries a size somebody chose. A preset's *name* does not, which is
    the distinction the centred case already draws."""
    band = Region(0.10, 0.30, 0.90, 0.70, name="band")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        _, records = _scumbled(tmp_path, band, brush=brush("flat", size=0.06))
    assert records[0].params["size"] == pytest.approx(0.06)


# -- a smudge softens a join; past a measured width it drags a lobe ---------------------
def test_a_smudge_defaults_to_a_width_that_softens_rather_than_drags(tmp_path):
    """What ``size`` buys stops at about 0.02 and what it costs does not, so the default
    sat four times past the knee of its own curve -- and the guide's examples followed
    it. Four of five smudges in one pass arrived as pale finger-shaped lobes."""
    s = make(tmp_path)
    assert s.smudge([(0.30, 0.50), (0.60, 0.50)]).params["size"] == pytest.approx(0.020)


def test_a_wide_smudge_says_what_it_will_look_like(tmp_path):
    """It still does exactly what it was asked. The guide warns about this at length and
    correctly; a warning at the call is what the length was standing in for."""
    s = make(tmp_path)
    with pytest.warns(UserWarning, match="dragging a lobe"):
        s.smudge([(0.30, 0.40), (0.60, 0.40)], size=0.06)
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        s.smudge([(0.30, 0.60), (0.60, 0.60)], size=0.02)


def test_a_narrower_smudge_carries_less_of_the_light_mass_into_the_dark(tmp_path):
    """The measurement the window is drawn from, in one line: the reach past a steep
    boundary grows with the brush while the softening stops improving."""
    def reach(size):
        s = Session(640, 480, texture="linen", ground="toned_grey", seed=7,
                    out_dir=tmp_path, timelapse=False)
        s.palette["lit"] = s.palette.at_value("titanium_white", 0.78)
        s.palette["wall"] = s.palette.at_value("burnt_umber", 0.17)
        s.block_in(polygon([(-0.05, 0.02), (1.05, 0.02), (1.05, 0.50), (-0.05, 0.50)]),
                   "flat", "lit", size=0.030, solid=True)
        s.block_in(polygon([(-0.05, 0.50), (1.05, 0.50), (1.05, 0.98), (-0.05, 0.98)]),
                   "flat", "wall", size=0.030, solid=True)
        s.dry()
        before = s.canvas.values() / 255.0
        h, w = before.shape
        columns = slice(int(0.42 * w), int(0.58 * w))
        middle = before[:, columns].mean(axis=1)
        edge = int(np.argmax(np.abs(np.diff(middle))[int(0.35 * h):int(0.65 * h)]))
        edge += int(0.35 * h)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            s.smudge([(0.30, (edge + 0.5) / h), (0.70, (edge + 0.5) / h)], size=size)
        lifted = ((s.canvas.values() / 255.0)[:, columns].mean(axis=1) - middle)[edge:]
        into_the_dark = np.flatnonzero(lifted > 0.03)
        return (int(into_the_dark.max()) + 1) / h if len(into_the_dark) else 0.0

    assert reach(0.020) < reach(0.070) * 0.5


# -- three documented surfaces that raised, and what they say now ----------------------
def test_solid_and_glaze_name_the_call_that_takes_them(tmp_path):
    """*Any brush field is also an override on any painting call* is true, and it means
    a keyword belonging to a neighbouring call lands in ``**brush_overrides`` and comes
    back as ``Brush.__init__() got an unexpected keyword argument`` -- a class the
    painter never mentioned. Both of these are real arguments one call over, and the
    reference lists them without saying which call takes them.

    ``solid=`` is now an argument of the four verbs that lay a mass or a mark, so the
    row that teaches it is left for the one call that does not take it because it
    lays that pair already."""
    s = make(tmp_path)
    with pytest.raises(TypeError, match="the burying recipe"):
        s.cover("upper-half", "burnt_umber", solid=True)
    with pytest.raises(TypeError, match=r"stroke\(\) argument"):
        s.block_in("upper-half", "flat", "burnt_umber", glaze=True)
    with pytest.raises(TypeError, match="Did you mean load"):
        s.block_in("upper-half", "flat", "burnt_umber", lode=1.0)


def test_a_shapes_box_unpacks_like_any_other_rectangle(tmp_path):
    """``shape.box`` is documented as the rectangle a mass is priced on, and unpacking a
    rectangle is the obvious thing to do with one. It raised."""
    mass = blob(cell("D5"), wobble=0.2, name="mass")
    x0, y0, x1, y1 = mass.box
    assert (x0, y0, x1, y1) == mass.bounds
    assert tuple(mass.box) == mass.box.bounds


# -- overhang lengthens the passes, and which edges that is turns with direction -------
def test_overhang_reaches_past_the_ends_of_the_pass_not_the_sides(tmp_path):
    """*How far each pass runs past the ends of the place* is accurate and cost a painter
    two masses: which two edges the "ends" are turns with ``direction``, so the same
    argument that keeps a horizontal mass off its own left edge runs a vertical one down
    off its foot and onto whatever it is standing on."""
    shape = polygon([(0.30, 0.30), (0.70, 0.30), (0.70, 0.60), (0.30, 0.60)], name="lit")

    def reach(direction, overhang):
        s = Session(640, 480, texture="linen", ground="toned_grey", seed=7,
                    out_dir=tmp_path, timelapse=False)
        before = np.array(s.canvas.rgb)
        s.block_in(shape, "bristle", "titanium_white", size=0.030, solid=True,
                   direction=direction, overhang=overhang)
        painted = np.abs(np.asarray(s.canvas.rgb) - before).sum(axis=2) > 0.01
        h, w = painted.shape
        sideways = np.flatnonzero(painted[int(0.35 * h):int(0.55 * h), :].any(axis=0))
        updown = np.flatnonzero(painted[:, int(0.35 * w):int(0.65 * w)].any(axis=1))
        return (0.30 * w - float(sideways.min()), 0.30 * h - float(updown.min()))

    flat_sides, flat_top = reach("horizontal", 0.0)
    long_sides, long_top = reach("horizontal", 1.0)
    assert long_sides > flat_sides + 8, "overhang did not lengthen a horizontal pass"
    assert abs(long_top - flat_top) <= 2, "it moved an edge the passes do not end on"

    up_sides, up_top = reach("vertical", 0.0)
    down_sides, down_top = reach("vertical", 1.0)
    assert down_top > up_top + 8, "the same argument did nothing to a vertical pass"
    assert abs(down_sides - up_sides) <= 2, "and it moved the sides instead"


# ======================================================================================
# The greenhouse sessions: one subject, three painters. Each left a request list beside
# its painting, and the strongest signal the collection has produced came from all
# three hitting one call -- edge="clean" on a mass narrow relative to its brush -- from
# three different shapes. Two of the three re-measured their own claims before making
# them; the third's are checked here before anything is built on them, which is
# LESSONS.md's rule, and it held every one this time.
# ======================================================================================

# -- the contour of a clean edge follows the polygon's own edges -----------------------
def _paint_above(s: Session, shape, top_edge: float) -> float:
    """Pixels of paint standing above a shape's top edge, in its own x-band."""
    ground = s.canvas.rgb[:4].reshape(-1, 3).mean(axis=0)
    on = np.abs(s.canvas.rgb - ground).sum(axis=2) > 0.03
    w, h = s.canvas.width, s.canvas.height
    band = on[:, int(shape.box.x0 * w):int(shape.box.x1 * w)]
    return (top_edge - np.nonzero(band.any(axis=1))[0].min() / h) * h


def test_the_clean_contour_stops_where_the_fill_stops(tmp_path):
    """Three painters, three shapes, one call: a pointed arch above a tapering tower, a
    cap eaten to a mushroom, and a 65px arch over a four-cornered tower, which the third
    isolated to the contour's spline bowing through two sparse corners. The fill is cut
    against the polygon's straight sides, so the contour now runs along the same line
    -- and the dusk example's own tower, which arched 45px, stops at its top edge."""
    tower = polygon([(0.30, 0.90), (0.40, 0.90), (0.38, 0.20), (0.32, 0.20)])
    above = {}
    for edge in ("ragged", "clean"):
        s = Session(1024, 768, texture="linen", ground="toned_grey", seed=3,
                    out_dir=tmp_path, timelapse=False)
        s.block_in(tower, "flat", "burnt_umber", size=0.02, solid=True, direction=90,
                   edge=edge)
        above[edge] = _paint_above(s, tower, 0.20)
    assert above["clean"] < 8, f"the contour stands {above['clean']:.0f}px above the top edge"
    assert abs(above["clean"] - above["ragged"]) < 4, "clean and ragged disagree on the top"


def test_a_clean_edge_says_when_its_brush_is_a_large_share_of_a_narrow_mass(tmp_path):
    """The cap: 0.036 deep, a flat at 0.016 -- the half-brush inset keeps half of it and
    the corners go first. The number that predicts it is the brush's share of the
    shorter extent, in the brush's own unit, and past a quarter the call says so.
    ``preview`` says the same, because the guide already says to preview the inset
    shape and this is that sentence with a number on it."""
    cap = polygon([(0.148, 0.114), (0.362, 0.114), (0.302, 0.078), (0.208, 0.078)],
                  name="cap")
    s = make(tmp_path)
    with pytest.warns(UserWarning, match="of the shorter extent"):
        s.block_in(cap, "flat", "burnt_umber", size=0.016, edge="clean", direction="axis")
    with pytest.warns(UserWarning, match="of the shorter extent"):
        s.preview({"shape": cap, "brush": "flat", "size": 0.016, "edge": "clean"})
    # Under the threshold this rule is silent. Not *nothing* is said: at 0.005 on this
    # canvas a flat is 1.6 pixels wide, which the tip-pixels rule catches -- so the
    # assertion is about this warning rather than about silence.
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        s.block_in(cap, "flat", "burnt_umber", size=0.005, edge="clean", direction="axis")
        s.block_in(cap, "flat", "burnt_umber", size=0.016, direction="axis")   # ragged
    assert not [c for c in caught if "of the shorter extent" in str(c.message)]


# -- a pressure list on a chisel tip -------------------------------------------------------
def test_a_pressure_list_on_a_chisel_tip_says_it_changes_paint_not_width(tmp_path):
    """Two painters read that an oriented tip keeps its chisel under a pressure list and
    laid every pot as a rectangle with chisel ends anyway. So the engine says it at the
    call -- on a short mark, where a list can only have been asking for a taper. A list
    on a long pass of a flat is how a passage brightens toward one side, and a list on
    the passes of a mass is the canvas-order feature; neither is a mistake."""
    s = make(tmp_path)
    with pytest.warns(UserWarning, match="changes the paint, not the width"):
        s.stroke([(0.50, 0.50), (0.52, 0.56)], "flat", "burnt_umber", size=0.03,
                 pressure=[1.0, 0.35])
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        s.stroke([(0.10, 0.50), (0.90, 0.55)], "flat", "burnt_umber", size=0.06,
                 pressure=[0.0, 0.55, 1.0])                              # a long pass
        s.stroke([(0.50, 0.50), (0.52, 0.56)], "round_hard", "burnt_umber", size=0.03,
                 pressure=[1.0, 0.35])                                   # width follows
        s.stroke([(0.50, 0.50), (0.52, 0.56)], "flat", "burnt_umber", size=0.03,
                 pressure="taper")                                       # the engine's own
        s.block_in(cell("D5"), "flat", "burnt_umber", size=0.02, pressure=[0.0, 1.0])


# -- a shaped block_in with direction left off ------------------------------------------------
def _lit_band():
    return polygon([(0.303, 0.268), (0.307, 0.400), (0.311, 0.540), (0.318, 0.680),
                    (0.330, 0.820), (0.344, 0.905), (0.398, 0.940), (0.384, 0.820),
                    (0.368, 0.680), (0.357, 0.540), (0.348, 0.400), (0.340, 0.258)],
                   name="lit band").smooth(3)


def test_a_shaped_block_in_with_direction_left_off_says_when_the_axis_is_cheaper(tmp_path):
    """Costed at 9 and 9 with ``direction=90``, written without it, charged 43 and 55:
    the default steps down the whole height. The default does not move -- that would
    move every painting ever made -- but the price walk, which has the number, says
    it, from ``cost`` and from the call alike, and stays quiet on a mass wider than
    it is tall and on a direction the painter chose."""
    s = Session(560, 430, texture="linen", ground="toned_warm_grey", seed=41,
                out_dir=tmp_path, timelapse=False)
    plan = {"shape": _lit_band(), "brush": "flat", "size": 0.022}
    with pytest.warns(UserWarning, match="direction= left off"):
        left_off = s.cost(plan, share=0)
    along = s.cost(dict(plan, direction="axis"), share=0)
    assert left_off > 2.5 * along
    with pytest.warns(UserWarning, match="direction= left off"):
        s.block_in(_lit_band(), "flat", "burnt_umber", size=0.022)
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        s.cost(dict(plan, direction="horizontal"), share=0)          # chosen, not left off
        s.cost({"shape": polygon([(0.19, 0.13), (0.32, 0.13), (0.32, 0.22), (0.19, 0.22)]),
                "brush": "flat", "size": 0.03}, share=0)               # wider than tall


# -- a banded scumble across a wedge ---------------------------------------------------------
def test_a_banded_scumble_says_when_its_brush_is_wider_than_the_passes_at_one_end(tmp_path):
    """The auto-sized brush closes the joins between passes, which is right on a band and
    wrong on a wedge: picked for the step, it is wider than the whole narrow end, and
    the paint blooms past the outline there. The warning names both pass lengths.
    A band -- the case the fix was tuned on -- says nothing."""
    s = make(tmp_path)
    wedge = polygon([(0.64, 0.28), (0.64, 0.325), (0.0, 0.62), (0.0, 0.20)], name="beam")
    with pytest.warns(UserWarning, match="width varies"):
        s.scumble(wedge, "burnt_umber", "titanium_white", 8, direction="vertical")
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        s.scumble(Region(0.10, 0.30, 0.90, 0.70), "burnt_umber", "titanium_white", 8)


# -- the pairs inside a value plan ---------------------------------------------------------
def test_a_value_plan_names_the_pairs_planned_within_the_threshold(tmp_path):
    """Every place inside tolerance and two of them planned 0.00 apart: the sheet scored
    each against its own target and never the gap *between* two, which is what 0.10
    means. It lists them now -- and says which of them meet, per the round below."""
    s = make(tmp_path)
    result = s.compare({Region(0.0, 0.0, 1.0, 0.3, name="sea"): 0.40,
                        Region(0.4, 0.3, 0.6, 0.9, name="tower"): 0.40,
                        Region(0.0, 0.9, 1.0, 1.0, name="rock"): 0.21})
    assert result.pairs == [("sea", "tower", pytest.approx(0.0), True)]
    table = result.table()
    assert "will read as one mass" in table and "sea / tower, 0.00 apart" in table
    apart = s.compare({Region(0.0, 0.0, 1.0, 0.3, name="sea"): 0.40,
                       Region(0.0, 0.9, 1.0, 1.0, name="rock"): 0.21})
    assert apart.pairs == [] and "planned within" not in apart.table()


# -- undo puts the generator back where a clean rebuild has it ------------------------------
def _three_masses(tmp_path, detour):
    """A mass, a detour that is undone, and a third mass -- hashed against no detour."""
    shape = polygon([(0.1, 0.1), (0.6, 0.15), (0.5, 0.7), (0.15, 0.6)])

    def start():
        s = Session(160, 120, seed=5, timelapse=False, out_dir=tmp_path)
        s.palette["c"] = s.palette.mix("ultramarine", "burnt_umber", 0.4)
        s.block_in(shape, "flat", "c", size=0.06)
        return s

    def finish(s):
        s.block_in(shape, "bristle", "c", size=0.05, direction="axis")
        return np.array(s.canvas.rgb)

    clean = finish(start())
    s = start()
    s = detour(s, shape) or s
    return clean, finish(s)


def test_undoing_a_mass_puts_the_generator_back_before_it(tmp_path):
    """A mass draws its pass wander from the session's stream, so undoing one used to
    leave the stream past it and the next mass drew wander a clean rebuild never had.
    Every record now carries the state its call began from -- taken once, before the
    first draw, because a mass draws *between* the strokes it records."""
    def undo_a_mass(s, shape):
        n = len(s.block_in(shape, "knife", "c", size=0.06))
        assert s.undo(n) == n

    clean, after = _three_masses(tmp_path, undo_a_mass)
    assert np.array_equal(clean, after)


def test_undo_through_the_session_file_is_the_painting(tmp_path):
    """``easel undo`` loads, undoes and saves, and the undo rebuilds from the log. A
    painter measured the working session drifting 1.06% of its pixels from a clean
    rebuild of the same scripts and committed the rebuild instead. Two things were
    wrong: the rebuilt stream sat at the seed, and the log rounded every point to five
    decimals, so a wobbled pass came back a hair off its line."""
    def cli_undo(s, shape):
        s.stroke([(0.2, 0.2), (0.8, 0.8)], "bristle", "c")
        path = tmp_path / "p.easel"
        s.save(path)
        t = Session.load(path)
        assert t.undo(1) == 1
        t.save(path)
        return Session.load(path)

    clean, after = _three_masses(tmp_path, cli_undo)
    assert np.array_equal(clean, after)


def test_a_saved_log_replays_the_painting_exactly(tmp_path):
    """The half of the undo finding that had nothing to do with undo: a replay from a
    saved log is what `easel undo` is, and it was not the painting."""
    s = make(tmp_path)
    s.block_in(blob(cell("D5"), 0.2, seed=2), "flat", "burnt_umber", size=0.05)
    s.save(tmp_path / "p.easel")
    again = Session.load(tmp_path / "p.easel").replay()
    assert np.array_equal(again.canvas.rgb, s.canvas.rgb)


def test_a_log_written_without_the_stream_still_loads_and_undoes(tmp_path):
    """A log from before 0.2.0 carries no state. It loads, it undoes, and the stream is
    left where the old undo left it -- the one thing that cannot be recovered."""
    s = make(tmp_path)
    s.block_in(cell("C3"), "flat", "burnt_umber", size=0.06)
    s.stroke([(0.2, 0.6), (0.8, 0.6)], "bristle", "titanium_white")
    for r in s.history.records:
        r.params.pop("rng", None)
    s.save(tmp_path / "old.easel")
    old = Session.load(tmp_path / "old.easel")
    assert old.undo(1) == 1
    assert old.stroke_count == s.stroke_count - 1
    assert not old._restore_stream(old.history.records[0])


def test_a_pass_of_a_mass_says_which_verb_laid_it(tmp_path):
    """The log could not tell a pass of a mass from a mark laid by hand, and the
    post-pass check needs to. A hand mark carries no such note."""
    s = make(tmp_path)
    passes = s.block_in(cell("C3"), "flat", "burnt_umber", size=0.06)
    hand = s.stroke([(0.2, 0.6), (0.8, 0.6)], "bristle", "titanium_white")
    assert all(r.params["via"] == "block_in" for r in passes)
    assert "via" not in hand.params
    assert len({r.params["rng"]["state"] for r in passes}) == 1, (
        "the passes of one call do not share the state the call began from"
    )


# -- the planning verbs leave the stream untouched ------------------------------------------
def test_the_planning_verbs_change_nothing_laid_after_them(tmp_path):
    """The property *rehearse everything* rests on, asserted rather than assumed: a
    bristle stroke laid after each free verb is the stroke laid with no verb before
    it. ``pencil``, ``dry`` and ``erase`` are the documented exceptions -- they are
    logged, and a mark's texture is seeded from its place in the log."""
    def build(pre):
        s = make(tmp_path)
        plan = [{"points": [(0.1, 0.5), (0.9, 0.5)], "brush": "bristle",
                 "color": "burnt_umber", "size": 0.08}]
        {"none": lambda: None, "look": lambda: s.look(),
         "values": lambda: s.look(values=True), "preview": lambda: s.preview(plan),
         "rehearse": lambda: s.rehearse(plan), "cost": lambda: s.cost(plan),
         "compare": lambda: s.compare({"all": 0.3}),
         "pencil": lambda: s.pencil([(0.1, 0.1), (0.9, 0.9)]),
         "dry": lambda: s.dry()}[pre]()
        s.stroke([(0.1, 0.5), (0.9, 0.5)], "bristle", "burnt_umber", size=0.08)
        return np.array(s.canvas.rgb)

    base = build("none")
    for verb in ("look", "values", "preview", "rehearse", "cost", "compare"):
        assert np.array_equal(build(verb), base), f"{verb}() changed the stroke after it"
    for verb in ("pencil", "dry"):
        assert not np.array_equal(build(verb), base), f"{verb}() is logged: it should shift"


# -- a rehearsal copy carries the painting's count -------------------------------------------
def test_a_rehearsed_pass_sees_the_paintings_own_count(tmp_path, capsys):
    """Inside a lone ``easel run --rehearse`` a script read ``stroke_count`` 0 and the
    whole budget, while its ``compare()`` plainly saw the painted canvas. The copy now
    continues the painting's numbers; what it laid itself is its own log, which is
    what the shell's line reports."""
    s = make(tmp_path, budget=100)
    s.block_in(cell("C3"), "flat", "burnt_umber", size=0.06)
    laid = s.spent
    trial = s.scratch()
    assert (trial.stroke_count, trial.remaining) == (laid, 100 - laid)
    trial.stroke([(0.2, 0.6), (0.8, 0.6)], "bristle", "titanium_white")
    assert (trial.spent, trial.remaining) == (laid + 1, 100 - laid - 1)
    assert trial.history.stroke_count == 1
    assert trial.budget_line() == f"{laid + 1} of 100 strokes spent, {100 - laid - 1} left"

    session = tmp_path / "p.easel"
    s.save(session)
    script = tmp_path / "pass.py"
    script.write_text('print("inside:", s.stroke_count, s.remaining)\n'
                      's.stroke([(0.3, 0.6), (0.7, 0.62)], "flat", "titanium_white")\n')
    assert main(["run", str(session), str(script), "--rehearse"]) == 0
    out = capsys.readouterr().out
    assert f"inside: {laid} {100 - laid}" in out
    assert f"Rehearsed pass.py: 1 strokes of the {100 - laid} left" in out


# -- chroma_of: how vivid, beside how light -----------------------------------------------------
def test_chroma_is_zero_for_a_grey_and_the_engine_lays_what_it_was_given(tmp_path):
    """A mixture read more vivid on the canvas than its numbers suggested, twice. The
    engine side of that, measured, is nothing: a solid plane reads back at the
    mixture's own chroma in the paint and in the view. What moves is the eye, judging
    it against the field -- so the instrument is the mixture's chroma beside the
    field's, which is what ``chroma_of`` is for."""
    p = Palette()
    assert p.chroma_of("#808080") == pytest.approx(0.0, abs=1e-4)
    assert p.chroma_of("cadmium_red") > p.chroma_of("yellow_ochre") > p.chroma_of("burnt_umber")
    assert p.chroma_of(p.desaturate("cadmium_red", 0.5)) < p.chroma_of("cadmium_red")

    s = Session(512, 384, texture="linen", ground="toned_warm_grey", seed=5,
                out_dir=tmp_path, timelapse=False)
    s.palette["m"] = s.palette.mix("yellow_ochre", "viridian", 0.30)
    s.block_in((0.20, 0.35, 0.80, 0.65), "flat", "m", size=0.03, solid=True)
    inner = (0.23, 0.38, 0.77, 0.62)
    mixed = s.palette.chroma_of("m")
    assert abs(s.palette.chroma_of(s.sample(inner)) - mixed) < 0.01
    assert abs(s.palette.chroma_of(s.sample(inner, rendered=True)) - mixed) < 0.01


# -- cost_line names the remedy in the same breath -----------------------------------------------
def test_cost_line_names_the_fix_beside_the_cut(tmp_path):
    """A stair drawn as one bent ribbon cost 141 of 340; cut into straight flights it
    cost five. ``cost_line`` said the outline cut the passes and not what to do about
    it, which is the one thing the guide's worked example does say."""
    s = make(tmp_path)
    bent = ribbon([(0.20, 0.30), (0.45, 0.62), (0.78, 0.34)], 0.029)
    line = s.cost_line({"shape": bent, "brush": "bristle", "size": 0.015})
    assert "pieces by the outline -- lay the straight stretches as strokes" in line
    assert "wider brush" in line


# -- the post-pass check ---------------------------------------------------------------------
def _stack(s):
    s.block_in(Region(0.1, 0.1, 0.9, 0.4, name="far"), "flat", "burnt_umber", size=0.04)
    s.block_in(Region(0.1, 0.5, 0.9, 0.8, name="near"), "flat", "burnt_umber", size=0.04)


def test_the_check_reads_a_stack_of_bars_off_the_log(tmp_path):
    """Two masses, every pass horizontal: the loudest tell in every painting made here.
    One mass alone is one decision and says nothing; two at one angle is the fault."""
    s = make(tmp_path)
    before = len(s.history.records)
    _stack(s)
    report = s.report(since=before)
    assert "long marks run within 6 degrees of horizontal, from 2 calls" in report
    assert "one brush at one size" in report          # both flat at 0.04, two calls

    one = make(tmp_path)
    one.block_in(Region(0.1, 0.1, 0.9, 0.4, name="far"), "flat", "burnt_umber", size=0.04)
    assert "nothing to report" in one.report()


def test_the_check_reads_small_combs_and_asked_for_tapers_off_the_log(tmp_path):
    """A bristle under 0.025 is four streaks with gaps, and a pressure list on a short
    chisel mark is a taper that was never going to happen -- both real passes of real
    paintings, and both counted rather than repeated as prose."""
    s = make(tmp_path)
    before = len(s.history.records)
    for i in range(3):
        s.stroke([(0.2 + i * 0.1, 0.45), (0.22 + i * 0.1, 0.47)], "bristle", "burnt_umber",
                 size=0.012)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s.stroke([(0.5, 0.5), (0.52, 0.56)], "flat", "burnt_umber", size=0.03,
                 pressure=[1.0, 0.35])
    report = s.report(since=before)
    assert "3 marks with a bristle under size=0.025" in report
    assert "1 short mark with a pressure list on a flat tip" in report


def test_the_check_counts_the_subjects_share_against_the_plan(tmp_path):
    """The checklist asks for the number written down; the check writes it down."""
    s = make(tmp_path)
    s.stroke([(0.2, 0.5), (0.8, 0.5)], "bristle", "burnt_umber", note="subject")
    s.stroke([(0.2, 0.6), (0.8, 0.6)], "bristle", "burnt_umber")
    assert "subject: 1 of 2 marks so far (50%)" in s.report()
    assert "against 32% planned" in s.report(subject_share=0.32)
    assert "behind" in s.report(subject_share=0.60)
    assert "subject:" not in make(tmp_path).report()


def test_the_check_is_printed_beside_the_budget_line(tmp_path, capsys):
    """Where it was asked for: after every pass, over that pass; ``--check`` widens it
    to the painting, and ``easel log --check`` reads it without painting anything."""
    a = tmp_path / "a.py"
    a.write_text('s.block_in(Region(0.1, 0.1, 0.9, 0.4), "flat", "burnt_umber", size=0.04)\n'
                 's.block_in(Region(0.1, 0.5, 0.9, 0.8), "flat", "burnt_umber", size=0.04)\n')
    b = tmp_path / "b.py"
    b.write_text('s.stroke([(0.3, 0.6), (0.7, 0.62)], "round_hard", "titanium_white",'
                 ' size=0.05)\n')
    session = tmp_path / "p.easel"
    assert main(["new", str(session), "--size", "320x240", "--out-dir",
                 str(tmp_path / "out"), "--budget", "60"]) == 0
    assert main(["run", str(session), str(a), "--rehearse"]) == 0
    assert "check over this pass" in capsys.readouterr().out
    assert main(["run", str(session), str(a)]) == 0
    out = capsys.readouterr().out
    assert "of 60 strokes spent" in out and "from 2 calls" in out
    assert main(["run", str(session), str(b)]) == 0
    assert "check over this pass, 1 mark: nothing to report" in capsys.readouterr().out
    assert main(["run", str(session), str(b), "--check"]) == 0
    assert "check over the painting" in capsys.readouterr().out
    assert main(["log", str(session), "--check"]) == 0
    assert "long marks run within 6 degrees of horizontal" in capsys.readouterr().out


# ======================================================================================
# The eighth session: a pool at night, painted against a restricted document set. It is
# the split test's other arm, and what it failed at was lookup rather than judgement --
# so two of its three engine items are instruments for questions the engine could
# already answer and would not say out loud. Every number it quoted reproduced; one
# mechanism it offered as a guess did not, and the test that covers it says so.
# ======================================================================================

# -- a glaze aimed at a value rather than at a strength --------------------------------
def _film(tmp_path):
    """A dry cool-dark mass with a warm light film to lay over it."""
    s = make(tmp_path)
    p = s.palette
    p["dark"] = p.at_value(p.mix("ultramarine", "burnt_umber", 0.5), 0.30)
    p["warm"] = p.at_value(p.mix("cadmium_red", "yellow_ochre", 0.4), 0.62)
    s.block_in(span("A1", "H8"), "flat", "dark", size=0.18, solid=True,
               pressure="even", direction="horizontal")
    s.dry()
    return s, [(0.2, 0.5), (0.8, 0.5)], dict(brush="flat", size=0.18, pressure="even")


def _under(s: Session, before: np.ndarray) -> float:
    """The value of the paint wherever the film changed it."""
    mask = np.abs(s.canvas.rgb - before).sum(axis=2) > 1e-4
    return s.palette.value_of(s.canvas.rgb[mask].mean(axis=0))


@pytest.mark.parametrize("target", [0.34, 0.38, 0.42, 0.46])
def test_a_glaze_can_be_aimed_at_a_value(tmp_path, target):
    """``at_value`` for a mixture, and now the same instrument for a film.

    The window between *the hue underneath is dead* and *this is a new mass* is a few
    hundredths of opacity wide and sits somewhere different over every passage, so
    *mix the glaze close, then choose an opacity* is a search run by rehearsal. One
    painting spent six of them on it.
    """
    s, points, kw = _film(tmp_path)
    before = s.canvas.rgb.copy()
    spent = s.stroke_count
    s.glaze(points, "warm", to_value=target, **kw)
    assert abs(_under(s, before) - target) <= 0.005
    assert s.stroke_count == spent + 1, "the search runs on copies and costs one mark"


def test_solving_a_glaze_lays_the_same_film_as_typing_the_opacity(tmp_path):
    """The search runs on trial canvases off a *copy* of the stroke stream.

    If it did not, every mark after a solved film would move, and the instrument
    would cost the determinism promise to buy a number.
    """
    s, points, kw = _film(tmp_path)
    s.glaze(points, "warm", to_value=0.42, **kw)
    opacity = s.history.records[-1].params["opacity"]

    t, points, kw = _film(tmp_path)
    t.glaze(points, "warm", opacity=opacity, **kw)
    assert np.array_equal(s.canvas.rgb, t.canvas.rgb)


def test_a_glaze_left_alone_is_the_film_it_always_was(tmp_path):
    """The default did not move: 0.18, and the same pixels as naming it."""
    s, points, kw = _film(tmp_path)
    s.glaze(points, "warm", **kw)
    t, points, kw = _film(tmp_path)
    t.glaze(points, "warm", opacity=0.18, **kw)
    assert s.history.records[-1].params["opacity"] == 0.18
    assert np.array_equal(s.canvas.rgb, t.canvas.rgb)


def test_a_value_no_film_can_reach_raises_rather_than_landing_near_it(tmp_path):
    """``at_value``'s rule, for the same reason: a film silently landing at the wrong
    value is not found until ``compare`` says so, a mass later."""
    s, points, kw = _film(tmp_path)
    with pytest.raises(ValueError) as excinfo:
        s.glaze(points, "warm", to_value=0.95, **kw)
    said = str(excinfo.value)
    assert "out of reach" in said and "opacity=1.0" in said
    assert s.history.records[-1].kind == "dry", "no film was laid"


def test_a_film_cannot_be_given_both_a_strength_and_a_value(tmp_path):
    s, points, kw = _film(tmp_path)
    with pytest.raises(ValueError, match="both"):
        s.glaze(points, "warm", opacity=0.2, to_value=0.42, **kw)


# -- the inward scumble's other wall: n bounded by the patch ---------------------------
def _glow(tmp_path) -> Session:
    """A session with the two values a centred scumble steps between."""
    s = make(tmp_path)
    s.palette["shadow"] = s.palette.at_value(
        s.palette.mix("ultramarine", "burnt_umber", 0.5), 0.30)
    s.palette["lit"] = s.palette.at_value(
        s.palette.mix("cerulean", "titanium_white", 0.7), 0.70)
    return s


def _inward_said(s: Session, patch, n: int, **kw) -> str:
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        s.scratch().scumble(patch, "shadow", "lit", n, direction="inward", **kw)
    return " ".join(str(c.message) for c in caught)


def test_a_shallow_patch_says_it_cannot_carry_the_rings_asked_for(tmp_path):
    """The brush is ``3 x depth / n``, so more rings buy a *narrower* brush.

    A painter met this at n=12 on a patch 0.075 deep, read the post-pass check's
    bristle complaint as an unrelated one, and spent two more rehearsals. The verb
    had warned from the wide side since the third session and said nothing here.
    """
    s = _glow(tmp_path)
    patch = ellipse((0.5, 0.5), 0.30, 0.075, name="patch")
    said = _inward_said(s, patch, 12)
    assert "comb" in said and "0.0187" in said
    assert "Drop to n=9" in said
    assert _inward_said(s, patch, 8) == "", "eight rings fit here and should be quiet"


def test_a_patch_no_n_fits_is_sent_to_the_other_recipe(tmp_path):
    """Under about 0.042 deep even five rings comb, so there is nothing to tune: a
    glow that shallow is not a bloom on a surface."""
    s = _glow(tmp_path)
    said = _inward_said(s, ellipse((0.5, 0.5), 0.20, 0.03, name="patch"), 8)
    assert "No n fits" in said and "a volume of lit air" in said


def test_a_named_narrow_brush_is_told_what_the_verb_would_have_picked(tmp_path):
    s = _glow(tmp_path)
    patch = ellipse((0.5, 0.5), 0.30, 0.075, name="patch")
    said = _inward_said(s, patch, 8, size=0.015)
    assert "Leave size= off" in said and "0.0281" in said


# -- a sequence of directions is one pass per angle, and is charged the sum ------------
def _room() -> Polygon:
    wallbase = [(-0.05, 0.245), (0.38, 0.29), (0.72, 0.335), (1.05, 0.365)]
    return polygon([(-0.05, -0.05), (1.05, -0.05)] + wallbase[::-1], name="room")


def test_a_direction_sequence_costs_the_sum_of_its_angles(tmp_path):
    """Not the steepest of them, which is the mechanism the painter guessed and marked
    as a guess. Their own three numbers reproduce; the mechanism did not."""
    s = make(tmp_path)
    room = _room()
    base = {"shape": room, "brush": "bristle", "size": 0.16, "density": 0.9}
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        ten = [0, 12, -17, 30, -35, 50, 62, -70, 80, 95]
        each = [s.cost(dict(base, direction=a), share=0) for a in ten]
        total = s.cost(dict(base, direction=ten), share=0)
        assert s.cost(dict(base, direction="axis"), share=0) == 4
        assert s.cost(dict(base, direction=-17), share=0) == 7
        assert s.cost(dict(base, direction="cross"), share=0) == 15
    assert total == sum(each)
    assert total > max(each)


def test_the_price_walk_covers_a_sequence_and_leaves_the_pair_idiom_alone(tmp_path):
    """Two angles can never be more than twice the dearer of them, so the cross at a
    mass's own angle -- which every painting in this repository uses -- stays quiet."""
    s = make(tmp_path)
    room = _room()

    def warned(direction) -> str:
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            s.scratch().block_in(room, "bristle", "burnt_umber", density=0.9,
                                 size=0.16, direction=direction)
        return " ".join(str(c.message) for c in caught)

    said = warned([0, 12, -17, 30, -35, 50, 62, -70, 80, 95])
    assert "sequence of 10 directions" in said and "85 strokes" in said
    assert "4 + 5 + 7" in said, "the line has to show that the price is a sum"
    for pair in ("cross", (4, 94), (5, 173)):
        assert warned(pair) == "", f"{pair} is the affordable answer and should be quiet"


def test_a_sequence_is_priced_the_same_from_cost_and_from_the_call(tmp_path):
    """The quote and the bill come off one walk, as they do for every other mass."""
    s = make(tmp_path)
    room = _room()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        quoted = s.cost({"shape": room, "brush": "bristle", "size": 0.16,
                         "density": 0.9, "direction": [0, 40, 80]}, share=0)
        laid = len(s.block_in(room, "bristle", "burnt_umber", density=0.9, size=0.16,
                              direction=[0, 40, 80]))
    assert quoted == laid


# ======================================================================================
# The ninth session: a heron in a flooded lot, painted against the eighth's three files
# plus DIAGNOSIS.md -- the restricted arm again, with the symptom index. Two of its three
# engine items are measurements taken against an *open* item rather than new complaints,
# which is what that arm is for, and one of them settles the mechanism the eighth session
# guessed at. Its second attempt at the same subject produced the fourth.
# ======================================================================================

# -- a direction sequence lays a complete stack per angle ------------------------------
def test_a_direction_sequence_lays_a_whole_stack_at_every_angle(tmp_path):
    """The eighth session guessed *sized for the steepest*; the ninth measured the
    passes. ``direction=[0, 90]`` logs the 0-degree stack and the 90-degree stack, whole,
    one after the other -- which is why the price is the sum and not the maximum."""
    s = make(tmp_path)
    shape = polygon([(0.20, 0.42), (0.80, 0.40), (0.80, 0.52), (0.20, 0.54)], name="band")
    kw = dict(brush="bristle", color="burnt_umber", size=0.036, density=1.0, solid=True)

    def angles(direction) -> list[float]:
        t = s.scratch()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            recs = t.block_in(shape, direction=direction, **kw)
        return [_mark_angle(r, t.canvas) for r in recs]

    flat, upright = angles(0), angles(90)
    both = angles([0, 90])
    assert len(both) == len(flat) + len(upright), "one whole stack per angle"
    # The flat stack first, whole, then the upright one -- not interleaved and not
    # merged. Read as the angle each half runs at rather than pass by pass: every
    # pass wanders a degree or two off its own line, and the wander comes off a
    # stream the first stack has already spent, so the exact angles do not repeat.
    assert _runs_at(both[:len(flat)]) == _runs_at(flat) == 0
    assert _runs_at(both[len(flat):]) == _runs_at(upright) == 90


def _mark_angle(record, canvas) -> float:
    pts = record.points
    dx = (pts[-1][0] - pts[0][0]) * canvas.width
    dy = (pts[-1][1] - pts[0][1]) * canvas.height
    return float(np.degrees(np.arctan2(dy, dx)) % 180.0)


def _runs_at(angles: list[float]) -> int:
    """Which way a stack of passes runs, to the nearest right angle."""
    return int(round(float(np.median(angles)) / 90.0) * 90) % 180


# -- the check's bristle floor, narrowed to a loaded comb ------------------------------
def _combs(tmp_path, load: float, whole: bool = False) -> str:
    s = make(tmp_path)
    s.palette["c"] = s.palette.mix("ultramarine", "burnt_umber", 0.4)
    before = len(s.history.records)
    for i in range(4):
        s.stroke([(0.2, 0.3 + i * 0.1), (0.8, 0.32 + i * 0.1)], "bristle", "c",
                 size=0.012, load=load)
    return s.report() + s.checklist() if whole else s.report(since=before)


def test_a_starved_comb_under_the_floor_is_not_a_fault(tmp_path):
    """A painting made of broken glints on water, grit under a flood and feather groups
    tripped this twenty-eight times and was right to skip it every time. Checked against
    both of that session's paintings: every small-bristle call site named an explicit
    ``load`` and none used the preset's own ``0.9``."""
    assert "nothing to report" in _combs(tmp_path, 0.35)
    assert "nothing to report" in _combs(tmp_path, 0.6)


def test_a_loaded_comb_under_the_floor_still_is(tmp_path):
    """What the rule was written for: a small solid plane laid with the wrong tip."""
    said = _combs(tmp_path, 0.9)
    assert "bristle under size=0.025" in said and "load over 0.6" in said


def test_the_closing_audit_leaves_a_small_comb_to_the_pass(tmp_path):
    """Finding 12 of the 0.5.0 cohort: over a whole painting this rule added up *265
    marks with a bristle under size=0.025*, and the painter argued with the line -- the
    comb's gaps were the needles it wanted. The rule asks for a brush for the marks
    about to be laid, which a finished painting has none of, and a pass that laid a
    habit's worth said so when it was laid. So `report()` with no `since`, and
    `checklist()`, leave it to the pass -- which still says it."""
    assert "bristle under size=0.025" in _combs(tmp_path, 0.9)
    assert "bristle under size=0.025" not in _combs(tmp_path, 0.9, whole=True)


# -- a graded passage laid by hand, and what it is not ---------------------------------
def _graded(tmp_path):
    s = make(tmp_path)
    p = s.palette
    for name, v in (("a", 0.66), ("b", 0.70), ("c", 0.74), ("d", 0.78)):
        p[name] = p.at_value(p.mix("cadmium_red", "cerulean", 0.3), v)
    p["dark"] = p.at_value(p.mix("ultramarine", "burnt_umber", 0.5), 0.25)
    return s


def _band_line(s: Session) -> str:
    return next((ln for ln in s.report().splitlines() if "stepping colours" in ln), "")


def test_a_hand_laid_band_too_narrow_for_its_own_step_says_so(tmp_path):
    """``scumble`` has sized its own brush since 0.2.0; ``RECIPES.md`` teaches the
    hand-rolled form of the same passage, which gets none of that. One painting's sky
    sat at 4.0 steps and wobbled 0.037; its hand-laid dawn band tapered to 1.7 steps
    and wobbled 0.072, on the same canvas in the same pass structure."""
    s = _graded(tmp_path)
    for i, col in enumerate(("a", "b", "c", "d", "d", "c", "b")):
        y = 0.24 + i * 0.0185
        s.stroke([(-0.07, y + 0.012), (0.5, y), (1.07, y - 0.006)], "bristle", col,
                 size=0.058 - i * 0.0057, opacity=0.3, load=1.0, load_falloff=0.0)
    said = _band_line(s)
    assert "7 marks at stepping colours" in said and "scumble()" in said


def test_a_mass_is_not_a_graded_passage_however_its_passes_are_spaced(tmp_path):
    """The condition that keeps every ``block_in`` out of the rule. Its passes step
    ``size * (1 - 0.45 * density)`` apart -- always under two brushes -- and they are
    all one colour, so the joins a graded passage shows at that spacing do not arise."""
    for density, solid in ((1.0, True), (0.8, False), (0.5, False)):
        s = _graded(tmp_path)
        s.block_in(span("A1", "H4"), "bristle", "dark", size=0.06, density=density,
                   solid=solid, direction="horizontal")
        assert _band_line(s) == "", f"fired on a plain mass at density={density}"


def test_a_verb_sized_passage_is_quiet_and_a_narrow_one_is_not(tmp_path):
    """The discriminator, on the verb the rule borrows its number from."""
    quiet = _graded(tmp_path)
    quiet.scumble(span("A1", "H4"), "dark", "d", 11)
    assert _band_line(quiet) == ""

    loud = _graded(tmp_path)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        loud.scumble(span("A1", "H4"), "dark", "d", 11, size=0.02)
    assert "stepping colours" in _band_line(loud)


def test_marks_further_apart_than_four_brushes_are_separate_marks(tmp_path):
    """Three trunks, three cables, three reflections: parallel, differently coloured,
    and not a passage laid badly."""
    s = _graded(tmp_path)
    for x, col in ((0.20, "a"), (0.45, "c"), (0.70, "d")):
        s.stroke([(x, 0.25), (x + 0.01, 0.70)], "bristle", col, size=0.02)
    assert _band_line(s) == ""


# -- an oriented tip too few pixels wide to lay any paint ------------------------------
def _tip_warning(session: Session, build) -> list[str]:
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        build(session)
    return [str(c.message) for c in caught if "pixels wide" in str(c.message)]


def test_an_oriented_tip_under_four_pixels_says_it_lands_nothing(tmp_path):
    """Not an aesthetic rule: a chisel this small does not make a poor mark, it makes
    no mark, and is charged for it. Four rehearsals went on a bird's head laid at
    ``size=0.005`` that came back the colour of the water behind it."""
    s = make(tmp_path)                      # 320x240, so the long side is 320
    said = _tip_warning(s, lambda t: t.block_in(
        Region(0.3, 0.3, 0.7, 0.7), "flat", "burnt_umber", size=0.005, density=1.0,
        solid=True, pressure="even"))
    assert len(said) == 1, "once per call, not once per pass"
    assert "1.6 pixels wide" in said[0] and "round_hard" in said[0]


def test_the_threshold_is_pixels_and_not_a_size(tmp_path):
    """The request proposed ``size`` under ``0.008``, and that is the wrong unit: the
    same size is 2.4px on a 300px canvas and 9.6px on a 1200px one. Measured on three
    canvases, the cliff is at four *pixels* on all of them."""
    small = Session(320, 240, texture="linen", ground="toned_grey", seed=7,
                    out_dir=tmp_path, timelapse=False)
    large = Session(1280, 960, texture="linen", ground="toned_grey", seed=7,
                    out_dir=tmp_path, timelapse=False)
    def mark(t):
        t.stroke([(0.3, 0.5), (0.7, 0.5)], "flat", "burnt_umber", size=0.008)

    assert _tip_warning(small, mark), "2.6px on this canvas and should say so"
    assert not _tip_warning(large, mark), "10.2px on this canvas and is a real brush"


def test_a_round_tip_has_no_such_cliff(tmp_path):
    """It holds its colour small, which is why ``liner`` is a ``round_hard`` at 0.005."""
    s = make(tmp_path)
    for tip in ("round_hard", "round_soft", "liner"):
        assert not _tip_warning(
            s, lambda t, b=tip: t.stroke([(0.3, 0.5), (0.7, 0.5)], b, "burnt_umber",
                                         size=0.004))


def test_the_tiny_chisel_is_named_before_a_stroke_is_spent(tmp_path):
    """From ``cost()`` as well as from the call, like the other price-walk warnings."""
    s = make(tmp_path)
    said = _tip_warning(s, lambda t: t.cost(
        [{"region": Region(0.3, 0.3, 0.7, 0.7), "brush": "flat", "color": "burnt_umber",
          "size": 0.005}], share=0))
    assert said and "flat" in said[0]


# -- sample() averages the place it is given -------------------------------------------
def test_sampling_a_cell_measures_the_cell_and_not_the_mass_in_it(tmp_path):
    """A painter checked two masses by cell, concluded the engine was laying everything
    0.14 light, and wrote a probe to find out why. Both were ``at_value`` doing what it
    was asked; the cells contained the water the masses were standing in."""
    s = make(tmp_path)
    p = s.palette
    p["water"] = p.at_value(p.mix("cerulean", "burnt_umber", 0.45), 0.50)
    p["bird"] = p.at_value(p.mix("ultramarine", "burnt_umber", 0.55), 0.30)
    s.block_in(Region(0.0, 0.0, 1.0, 1.0), "flat", "water", size=0.09, solid=True,
               direction="horizontal", pressure="even", opacity=1.0)
    bird = polygon([(0.53, 0.44), (0.60, 0.42), (0.63, 0.50), (0.57, 0.56)], name="bird")
    s.block_in(bird, "flat", "bird", size=0.03, solid=True, direction="axis",
               pressure="even", opacity=1.0)

    by_cell = p.value_of(s.sample(cell("F5")))
    by_shape = p.value_of(s.sample(bird))
    assert abs(by_shape - 0.30) < 0.06, "the mass itself is near where it was mixed"
    assert by_cell > by_shape + 0.12, "and the cell is mostly the water around it"


# ======================================================================================
# The tenth session: a fogged greenhouse wall from outside, and the winter greenhouse
# interior painted before it and filed after it. Both rounds are in here together: they
# raised the same two items from opposite directions -- what `direction=` names, and a
# check that fires on a row of separate things -- and a test that guarded only one of
# them would be guarding half a fix.
# ======================================================================================

# -- the check reads the painting behind a rehearsal -----------------------------------
def test_the_first_sixty_rule_counts_the_painting_a_rehearsal_stands_on(tmp_path):
    """The rule that says *detail before the masses are down* policed the painting's
    first sixty marks and fired at 135, 162, 190, 243, 260 and 273 strokes spent -- on
    the ``--rehearse`` path only. A rehearsal copy starts with an empty log, so the
    rule's *earlier* term was nought however far along the painting was, and the guide
    has every painter rehearse first: the false positive was the answer they always
    got, and the correct silence only arrived after the decision it was meant to
    inform."""
    s = make(tmp_path)
    for i in range(70):
        s.stroke([(0.05 + 0.012 * i, 0.20), (0.05 + 0.012 * i, 0.30)], "flat",
                 "burnt_umber", size=0.05)
    assert s.spent >= 60

    def detail(session):
        before = len(session.history.records)
        for i in range(9):
            session.dab(0.2 + 0.03 * i, 0.8, "round_hard", "titanium_white", size=0.01)
        return session.report(since=before)

    trial = s.scratch()
    assert trial.history.records == []
    assert "detail before the masses are down" not in detail(trial)
    assert "detail before the masses are down" not in detail(s)

    # And it still fires where it should: nine small marks on a bare canvas.
    assert "detail before the masses are down" in detail(make(tmp_path).scratch())


def test_a_rehearsals_subject_share_is_the_paintings_share(tmp_path):
    """The other rule that reads across passes, and the same hole. A rehearsed pass
    reported its own marks as the whole painting, so a subject share measured where the
    guide says to measure it -- at the moment the subject is finished, which is a
    rehearsal -- came back as 100% of nine marks."""
    s = make(tmp_path)
    for i in range(6):
        s.stroke([(0.05, 0.1 + 0.1 * i), (0.95, 0.1 + 0.1 * i)], "flat", "burnt_umber",
                 size=0.05)
    trial = s.scratch()
    trial.stroke([(0.2, 0.75), (0.8, 0.75)], "flat", "titanium_white", size=0.05,
                 note="subject")
    trial.stroke([(0.2, 0.85), (0.8, 0.85)], "flat", "titanium_white", size=0.05,
                 note="subject")
    assert "subject: 2 of 8 marks so far (25%)" in trial.report()
    assert "against 40% planned" in trial.report(subject_share=0.40)
    assert "behind" in trial.report(subject_share=0.40)


# -- a jitter that is a multiple of the default rather than a tweak --------------------
def test_a_jitter_far_past_the_default_says_so(tmp_path):
    """``jitter=0.5`` was accepted in silence and beaded every member of a greenhouse
    frame. It is twenty-five times the default, from a call that otherwise looked
    exactly like the recipe -- and the check warns about a pressure list on a chisel
    tip, which is a subtler fault than this one. The number behind the wall is width:
    a stroke is 1.2 brushes across at the default and 3.7 at ``0.5``."""
    s = make(tmp_path)
    with pytest.warns(UserWarning, match="25 times the default"):
        s.stroke([(0.1, 0.5), (0.9, 0.5)], "flat", "burnt_umber", size=0.03, jitter=0.5)

    # The wall is five times the default, and under it nothing is said.
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        s.stroke([(0.1, 0.6), (0.9, 0.6)], "flat", "burnt_umber", size=0.03, jitter=0.1)
        s.stroke([(0.1, 0.7), (0.9, 0.7)], "flat", "burnt_umber", size=0.03)
        # A brush built by hand is the painter's own, the way the chisel floor has it.
        s.stroke([(0.1, 0.8), (0.9, 0.8)], brush("flat", size=0.03, jitter=0.5),
                 "burnt_umber")

    # And it is the width that is measured, not the adjective: the band the painter
    # got is the band the warning quotes.
    wide = Session(1024, 768, texture="linen", ground="toned_grey", seed=7,
                   out_dir=tmp_path, timelapse=False)
    bands = []
    for y, j in ((0.35, 0.02), (0.65, 0.5)):
        before = wide.canvas.rgb.copy()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            wide.stroke([(0.1, y), (0.9, y)], "liner", "burnt_umber", size=0.005,
                        jitter=j, pressure="even")
        rows = np.where((np.abs(wide.canvas.rgb - before).sum(axis=2) > 1e-3).any(axis=1))[0]
        bands.append((rows.max() - rows.min() + 1) / (0.005 * 1024))
    assert bands[0] < 1.4 and bands[1] > 3.0


# -- inset() leaves a boundary on the canvas frame where it is -------------------------
def _right_column_bare(session, place, **kw):
    """How much of the canvas's last column, where the mass reaches it, is bare ground."""
    rows = slice(int(0.15 * session.canvas.height), int(0.85 * session.canvas.height))
    ground = session.canvas.values()[rows, -1] / 255.0
    session.block_in(place, solid=True, **kw)
    now = session.canvas.values()[rows, -1] / 255.0
    return float(np.mean(np.abs(now - ground) < 0.02))


def test_inset_does_not_erode_a_boundary_that_lies_on_the_frame(tmp_path):
    """``edge="clean"`` has dropped its inset at the frame since 0.2.0, on the stated
    principle that *a mass that meets the frame should run off it*; plain ``inset()``
    eroded it, and the asymmetry is invisible from the call. ``GLASS.inset(0.024)``
    pulled a glass wall off ``x = 1.0``, the ground showed down the right edge of the
    finished painting, and the defect survived to the final inspection pass."""
    glass = polygon([(0.55, 0.05), (1.05, 0.02), (1.05, 0.98), (0.55, 0.95)], name="glass")
    kw = dict(brush="flat", color="burnt_umber", size=0.06)
    assert _right_column_bare(make(tmp_path), glass.inset(0.024), **kw) == 0.0
    assert _right_column_bare(make(tmp_path), glass.inset(0.024, frame=False), **kw) > 0.9

    # Per coordinate, not per point: the side at the frame stays, the rest moves in.
    kept = glass.inset(0.024)
    assert [x for x, _ in kept.points if x >= 1.0] == [1.0, 1.0]
    assert min(x for x, _ in kept.points) > 0.55
    assert min(y for _, y in kept.points) > 0.02

    # A region reaching the frame behaves the same way, and one that does not is
    # eroded exactly as before.
    assert Region(0.5, 0.0, 1.0, 0.8).inset(0.05) == Region(0.55, 0.0, 1.0, 0.75)
    assert Region(0.2, 0.2, 0.8, 0.8).inset(0.05) == Region(0.25, 0.25, 0.75, 0.75)
    # And growing is untouched: past the frame is where it was going anyway.
    assert Region(0.5, 0.0, 1.0, 0.8).inset(-0.05).bounds == pytest.approx(
        (0.45, 0.0, 1.0, 0.85))
    inside = make(tmp_path).circle((0.5, 0.5), 0.16)
    assert inside.inset(0.03).points == inside.inset(0.03, frame=False).points


# -- cover() can be told to stay inside the area it was given ---------------------------
def _cover_footprint(session, patch, **kw):
    """The share of ``patch``'s own area that a burial actually painted."""
    session.block_in(Region(0.0, 0.0, 1.0, 1.0), "flat", "burnt_umber", size=0.12,
                     solid=True)
    session.dry()
    before = session.canvas.rgb.copy()
    session.cover(patch, "titanium_white", **kw)
    changed = np.abs(session.canvas.rgb - before).sum(axis=2) > 1e-3
    w, h = session.size
    asked = (patch.x1 - patch.x0) * w * (patch.y1 - patch.y0) * h
    return float(changed.sum() / asked)


def test_cover_holds_a_burial_to_its_place_by_default(tmp_path):
    """``cover`` is offered as the answer to *you will reach for undo*, and until 0.6.0
    its recipe ran the ends of each pass a full brush outside the area. On a flat
    passage that is invisible. Used to bury a mis-made leaf inside a worked pane of
    glass it put a flat pale panel across a visibly larger patch, and the painter
    buried ``cover``'s own output by hand with marks shaped like the pane -- so the
    default moved to ``edge="hard"`` (F1), and the old recipe is one keyword away."""
    patch = Region(0.905, 0.380, 0.985, 0.478)

    def on_a_fresh_canvas(**kw):
        # 1024x768, the canvas the leaf's 3.07x was measured on.
        return _cover_footprint(
            Session(1024, 768, texture="linen", ground="toned_grey", seed=7,
                    out_dir=tmp_path, timelapse=False), patch, size=0.06, **kw)

    assert on_a_fresh_canvas() < 1.05, "the default stops at the place it was handed"
    assert on_a_fresh_canvas(edge="ragged") > 2.5, "and the old recipe runs its ends outside"


def _marred(tmp_path):
    """F1's bench on a bare canvas: a light stroke across the middle of a repair-sized
    place, 108x60 px on 900x600, dried -- with the values before it and after it."""
    s = Session(900, 600, texture="linen", ground="toned_grey", seed=7,
                out_dir=tmp_path, timelapse=False)
    before = s.canvas.values(sketch=False).astype(np.float32) / 255.0
    s.stroke([(0.465, 0.458), (0.535, 0.482)], "round_hard", "titanium_white",
             size=0.018, opacity=1.0, pressure="even")
    s.dry()
    return s, before, s.canvas.values(sketch=False).astype(np.float32) / 255.0


def _still_showing(s, before, marred) -> float:
    """The share of the mistake's own pixels still nearer the mistake than the ground."""
    view = s.canvas.values(sketch=False).astype(np.float32) / 255.0
    mistake = np.abs(marred - before) >= 0.10
    nearer = np.abs(view - marred) < np.abs(view - before)
    return float((nearer & mistake).sum() / mistake.sum())


def test_a_clean_burial_on_a_small_region_says_what_the_inset_leaves(tmp_path):
    """F1's bench found it: ``clean-small`` asked a shape and nothing else, and
    ``cover()`` is handed a region far more often than a shape. At the default
    ``flat``, ``size=0.1``, a place 108x60 px on 900x600 is inset to a sliver with two
    stubs laid in its middle, and a fifth of the mistake it was burying stays showing
    -- in silence. A region is asked what a shape is asked now, at the call and in
    ``preview``, and the line names the call the painter made."""
    place = Region(0.44, 0.42, 0.56, 0.52)
    s, before, marred = _marred(tmp_path)
    with pytest.warns(UserWarning, match=r"cover\(edge='clean'\) at size=0\.1 on a region"):
        s.cover(place, s.ground, edge="clean")
    assert _still_showing(s, before, marred) > 0.10, "the ends of the mistake stay showing"
    with pytest.warns(UserWarning, match="leave edge= off"):
        s.preview({"cover": place, "color": "burnt_umber", "edge": "clean"})
    with pytest.warns(UserWarning, match=r"block_in\(edge='clean'\) at size=0\.1 on a region"):
        make(tmp_path).block_in(place, "flat", "burnt_umber", edge="clean")
    # The neighbouring right things say nothing, and bury the whole mistake: the
    # default, and a clean edge at a brush under a quarter of the place.
    for kw in ({}, {"edge": "clean", "size": 0.015}):
        quiet, before, marred = _marred(tmp_path)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            quiet.cover(place, quiet.ground, **kw)
        assert not [c for c in caught if "of the shorter extent" in str(c.message)], kw
        assert _still_showing(quiet, before, marred) == 0.0, kw


# -- how much ground is still showing --------------------------------------------------
def test_the_check_says_how_much_ground_is_still_showing(tmp_path):
    """The closing checklist asks *is there anywhere the ground still shows through?
    There should be* -- and there was no way to tell short of building a bare canvas
    and diffing it, which is what a painter did after the painting was finished,
    having already lost the warm ground the whole picture was planned around. The
    instrument is the diff, and it is exact: same ground, same texture, same seed."""
    s = Session(400, 300, texture="linen", ground="umber_wash", seed=7,
                out_dir=tmp_path, timelapse=False)
    assert s.canvas.ground_showing() == 1.0
    assert "ground:" not in s.report(), "nothing painted yet is not a finding"

    s.block_in(Region(0.0, 0.0, 1.0, 1.0), "bristle", "ultramarine", size=0.09,
               density=0.7)
    loose = s.canvas.ground_showing()
    assert 0.01 < loose < 0.2, "a first pass leaves the ground showing, as the guide says"
    assert f"ground: {loose:.2%}" in s.report()
    assert "the checklist asks for some" not in s.report()

    s.block_in(Region(0.0, 0.0, 1.0, 1.0), "flat", "ultramarine", size=0.09,
               density=1.0, solid=True)
    assert s.canvas.ground_showing() < 0.001
    assert "the checklist asks for some" in s.report()

    # Per channel, not by value: a film at the ground's own lightness has covered it.
    cool = Session(400, 300, texture="linen", ground="umber_wash", seed=7,
                   out_dir=tmp_path, timelapse=False)
    same_value = cool.palette.at_value("ultramarine",
                                       cool.palette.value_of(cool.canvas.bare().mean(axis=(0, 1))))
    cool.block_in(Region(0.0, 0.0, 1.0, 1.0), "flat", same_value, size=0.09,
                  density=1.0, solid=True)
    assert cool.canvas.ground_showing() < 0.01

    # And graphite is not paint: a drawing over the ground is still ground showing.
    drawn = Session(400, 300, texture="linen", ground="umber_wash", seed=7,
                    out_dir=tmp_path, timelapse=False)
    drawn.pencil([(0.1, 0.1), (0.9, 0.9)], pressure=1.0)
    assert drawn.canvas.ground_showing() == 1.0


# -- the graded-passage rule, narrowed to a passage ------------------------------------
def _ramped(tmp_path):
    """A wide canvas with eight values of one mixture, light to dark."""
    s = Session(1024, 768, texture="linen", ground="toned_grey", seed=7,
                out_dir=tmp_path, timelapse=False)
    p = s.palette
    for i, v in enumerate((0.30, 0.38, 0.46, 0.54, 0.62, 0.70, 0.78, 0.86)):
        p[f"v{i}"] = p.at_value(p.mix("cadmium_red", "cerulean", 0.3), v)
    return s


def _lay(s, y, col, size):
    s.stroke([(0.05, y), (0.95, y)], "flat", col, size=size, load=1.0, load_falloff=0.0)


def test_a_row_of_separate_things_is_not_a_graded_passage(tmp_path):
    """Three times in one painting, and once in the next. Read against the rule's own
    code it took the largest set of long marks within six degrees of one angle across
    the whole pass, wanted three colours and a median step, and never asked whether
    the marks formed one contiguous band or whether their colours stepped one way.

    Ten pots on a bench, three vertical body strokes each at three terracotta values,
    came back as *30 marks at stepping colours ... 1.2 of that step*. They are ten
    objects: the step is three quarters of a brush **inside** a pot, and the gaps that
    matter are the ones between pots."""
    s = _ramped(tmp_path)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for i in range(10):
            x = 0.10 + i * 0.075
            for j, col in enumerate(("v1", "v3", "v5")):
                s.stroke([(x + j * 0.004, 0.52), (x + j * 0.004, 0.58)], "flat", col,
                         size=0.005)
    assert _band_line(s) == ""


def test_two_ramps_laid_end_to_end_are_not_one_passage(tmp_path):
    """Two overlapping ``scumble`` ramps over adjacent bands, ``n=7`` then ``n=8``,
    drew *15 marks at stepping colours* -- the two calls summed -- and the remedy it
    suggested was three times either band's own step, which would have been wrong for
    both. A passage steps one way; a sequence that turns twice is two of them."""
    one = _ramped(tmp_path)
    for i in range(8):
        _lay(one, 0.18 + i * 0.028, f"v{i}", 0.03)
    assert "8 marks at stepping colours" in _band_line(one), "one ramp still says so"

    two = _ramped(tmp_path)
    for i in range(8):
        _lay(two, 0.18 + i * 0.028, f"v{i % 4}", 0.03)
    assert _band_line(two) == ""


def test_a_smudge_lays_no_colour_and_is_not_counted_in_a_passage(tmp_path):
    """*5 marks at stepping colours run parallel 0.028 apart, and the narrowest brush
    laying them is 0.02* -- where the 0.02 was a smudge, counted with two block-in
    passes and two glazes. A smudge drags what is already there; it contributed no
    colour to the passage it was made the narrowest brush of."""
    quiet = _ramped(tmp_path)
    for i in range(5):
        _lay(quiet, 0.20 + i * 0.028, f"v{i}", 0.06)
    assert _band_line(quiet) == "", "a brush this wide for this step is right"

    smudged = _ramped(tmp_path)
    for i in range(5):
        _lay(smudged, 0.20 + i * 0.028, f"v{i}", 0.06)
    smudged.smudge([(0.05, 0.34), (0.95, 0.34)], size=0.02)
    assert _band_line(smudged) == ""

    # A mark that does lay colour at that size is the fault the rule was written for.
    painted = _ramped(tmp_path)
    for i in range(5):
        _lay(painted, 0.20 + i * 0.028, f"v{i}", 0.06)
    _lay(painted, 0.34, "v5", 0.02)
    assert "6 marks at stepping colours" in _band_line(painted)


# -- a round tip printing its own outline ----------------------------------------------
def _leaf():
    """The leaf pressed flat on the glass, off ``paintings/Claude/fogged_glass/p8_wet.py``."""
    return hull([(0.918, 0.405), (0.949, 0.393), (0.968, 0.424),
                 (0.951, 0.462), (0.921, 0.448)], name="leaf")


def test_several_small_round_marks_at_no_wobble_are_one_disc(tmp_path):
    """``tip_wobble`` defaults to ``0``, which is the disc the documentation warns
    about, so *several small marks with round_hard or liner* is the failure by
    default and the fix is opt-in. The closing checklist asks *is any small mark a
    disc, a capsule or a rectangle -- the tool's own shape rather than the thing's?*
    and this is that question, counted. Over a pass, which is one passage; the whole
    painting is the tests after this one."""
    s = Session(1200, 800, texture="linen", ground="toned_grey", seed=7,
                out_dir=tmp_path, timelapse=False)
    for i in range(4):
        s.dab(0.30 + 0.05 * i, 0.5, "round_hard", "titanium_white", size=0.012, press=3)
    assert "one disc printed 4 times" in s.report(since=0)

    wobbled = Session(1200, 800, texture="linen", ground="toned_grey", seed=7,
                      out_dir=tmp_path, timelapse=False)
    for i in range(4):
        wobbled.dab(0.30 + 0.05 * i, 0.5, "round_hard", "titanium_white", size=0.012,
                    press=3, tip_wobble=0.7)
    assert "one disc printed" not in wobbled.report(since=0)

    # A liner drawing fine lines is the guide's own advice and is not this fault: a
    # round tip stops reading as a capsule at about seven times its own width.
    lines = Session(1200, 800, texture="linen", ground="toned_grey", seed=7,
                    out_dir=tmp_path, timelapse=False)
    for i in range(4):
        lines.stroke([(0.30 + 0.05 * i, 0.3), (0.31 + 0.05 * i, 0.7)], "liner",
                     "titanium_white", size=0.004)
    assert "one disc printed" not in lines.report(since=0)


def _dots(s, where, **kw):
    """Small round dabs at tip_wobble=0 -- one disc each -- at the places given."""
    for x, y in where:
        s.dab(x, y, "round_hard", "titanium_white", size=0.012, press=3, **kw)


#: A lamp, a moon and a glint: three accents on three sides of the picture.
_APART = [(0.08, 0.10), (0.92, 0.12), (0.10, 0.92)]


def test_over_a_whole_painting_discs_standing_apart_are_not_one_disc(tmp_path):
    """Finding 12 of the 0.5.0 cohort, the disc half. A pass is one passage, so the
    discs it lays are seen together; a painting is many, and the closing audit was
    adding them up: one finished painting's *one disc printed 8 times* was a lamp, a
    moon, two notches, two edge highlights and a glint, laid in six passes. Over a
    whole painting only discs seen together count. What a pass says is unchanged."""
    s = Session(1200, 800, texture="linen", ground="toned_grey", seed=7,
                out_dir=tmp_path, timelapse=False)
    _dots(s, _APART)
    assert "one disc printed 3 times" in s.report(since=0)
    assert "small marks with a round tip" not in s.report()
    assert "small marks with a round tip" not in s.checklist()


def test_the_closing_audit_says_where_the_discs_sit_together(tmp_path):
    """The discs a painting does show together -- a row of pots, a glitter path -- are
    the rule's own fault, and at the end of a painting a count with no place is no help
    in finding them. So the line names each group, the largest first, as the ``(x, y)``
    every place in the engine is given in, and leaves the three standing apart out."""
    s = Session(1200, 800, texture="linen", ground="toned_grey", seed=7,
                out_dir=tmp_path, timelapse=False)
    _dots(s, [(0.30, 0.50), (0.34, 0.50), (0.38, 0.50), (0.42, 0.50)])
    _dots(s, [(0.76, 0.80), (0.80, 0.80), (0.84, 0.80)])
    _dots(s, _APART)
    assert "one disc printed 10 times" in s.report(since=0)
    said = s.checklist()
    assert ("7 small marks with a round tip at tip_wobble=0 sit together in 2 places -- "
            "4 around (0.36, 0.50), 3 around (0.80, 0.80): each is one disc printed over "
            "and over") in said
    assert "sit together in 2 places" in s.report()

    one = Session(1200, 800, texture="linen", ground="toned_grey", seed=7,
                  out_dir=tmp_path, timelapse=False)
    _dots(one, [(0.30, 0.50), (0.34, 0.50), (0.38, 0.50), (0.42, 0.50)])
    assert ("4 small marks with a round tip at tip_wobble=0 sit together around "
            "(0.36, 0.50): that is one disc printed 4 times") in one.checklist()


def test_a_signature_is_not_one_disc_printed_over_and_over(tmp_path):
    """A signature is lettering, and the budget already waives it; a dotted *i* and
    two full stops beside it are not a passage of discs. Left out over a whole
    painting, by the same test the budget uses."""
    s = Session(1200, 800, texture="linen", ground="toned_grey", seed=7,
                out_dir=tmp_path, timelapse=False)
    _dots(s, [(0.86, 0.92), (0.89, 0.92), (0.92, 0.92), (0.95, 0.92)], note="signature")
    assert "small marks with a round tip" not in s.checklist()


def test_a_round_tip_blocking_in_a_small_shape_says_so(tmp_path):
    """A ``hull`` ``0.046`` across at its narrowest with a ``round_hard`` at
    ``size=0.013`` -- a leaf pressed on the glass -- printed the shape's own scalloped
    boundary and came back, in the painter's word, a cauliflower. It was relaid as two
    tapering strokes that meet plus a midrib. A disc's overhang goes out all the way
    round, so at that share the mass lands half again the area of the shape."""
    s = Session(1200, 800, texture="linen", ground="toned_grey", seed=7,
                out_dir=tmp_path, timelapse=False)
    with pytest.warns(UserWarning, match="round tip .* at size=0.013"):
        s.block_in(_leaf(), "round_hard", "titanium_white", direction=34, density=1.0,
                   size=0.013, pressure="even")
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        s.block_in(_leaf(), "flat", "titanium_white", direction=34, density=1.0,
                   size=0.013, pressure="even")
        s.block_in(_leaf(), "round_hard", "titanium_white", direction=34, density=1.0,
                   size=0.009, pressure="even")

    # And what the warning is about, measured: the painted area against the shape's.
    def landed(brush, size):
        one = Session(1200, 800, texture="linen", ground="toned_grey", seed=7,
                      out_dir=tmp_path, timelapse=False)
        before = one.canvas.rgb.copy()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            one.block_in(_leaf(), brush, "titanium_white", size=size, density=1.0,
                         solid=True, direction=34, pressure="even", opacity=1.0)
        painted = np.abs(one.canvas.rgb - before).max(axis=2) > 0.01
        return painted.sum() / _leaf().mask(1200, 800).sum()

    assert landed("round_hard", 0.013) > 1.5
    assert landed("flat", 0.013) < landed("round_hard", 0.013)


# -- a hard clip: a pass that ends where the outline is --------------------------------
def _lit_face():
    """The lit band off ``scripts/probe_greenhouse_session.py``: boundaries about three
    degrees off vertical, and no horizontal feature of its own."""
    return polygon([(0.303, 0.268), (0.307, 0.400), (0.311, 0.540), (0.318, 0.680),
                    (0.330, 0.820), (0.344, 0.905), (0.398, 0.940), (0.384, 0.820),
                    (0.368, 0.680), (0.357, 0.540), (0.348, 0.400), (0.340, 0.258)]
                   ).smooth(3)


def _horizontal_edge_share(session, box, pad=0.01):
    """Share of the strong edges in a region running within 10 degrees of horizontal.

    The Sobel measure ``CALIBRATION.md``'s *Laying a mass along its own axis* table is
    built on. Higher is squarer; a staircase is a run of horizontal edges where the
    mass has no horizontal feature.
    """
    img = np.asarray(session.canvas.to_srgb8(impasto=True), dtype=np.float32) / 255.0
    h, w, _ = img.shape
    grey = (0.2126 * img[..., 0] ** 2.2 + 0.7152 * img[..., 1] ** 2.2
            + 0.0722 * img[..., 2] ** 2.2)
    x0, y0 = int((box.x0 - pad) * w), int((box.y0 - pad) * h)
    x1, y1 = int((box.x1 + pad) * w), int((box.y1 + pad) * h)
    g = grey[max(y0, 1):min(y1, h - 1), max(x0, 1):min(x1, w - 1)]
    gy, gx = np.gradient(g)
    mag = np.hypot(gx, gy)
    strong = mag > max(np.percentile(mag, 90), 1e-4)
    ang = np.degrees(np.arctan2(np.abs(gx[strong]), np.abs(gy[strong])))
    return float((ang < 10.0).mean())


def _laid(tmp_path, face, edge, brush="flat", size=0.020):
    s = Session(1120, 860, texture="linen", ground="toned_warm_grey", seed=41,
                out_dir=tmp_path, timelapse=False)
    s.palette["v"] = s.palette.at_value(s.palette.mix("yellow_ochre", "viridian", 0.30),
                                        0.25)
    before = s.canvas.rgb.copy()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s.block_in(face, brush, "v", size=size, density=1.0, solid=True, opacity=1.0,
                   pressure="even", direction=90, edge=edge)
    return s, np.abs(s.canvas.rgb - before).max(axis=2) > 0.01


def test_a_hard_clip_ends_a_pass_where_the_outline_is(tmp_path):
    """The chisel staircase and the half-brush spill are one defect, and it was the
    most common way a mass went wrong in one painting: four times. A gable came back
    as chisel ends stepping down both slopes; bench tops poked corners into the wall
    behind them; the dark under each bench spilled half a brush above the bench's far
    edge as a sawtooth. Three workarounds were used and none is in the recipes, one of
    them lowering a polygon 0.12 m in world space so the overhang stayed hidden."""
    face = _lit_face()
    ragged, ragged_px = _laid(tmp_path, face, "ragged")
    hard, hard_px = _laid(tmp_path, face, "hard")
    inside = face.mask(1120, 860)

    # The overhang table's own row: furthest paint past each edge, which should read
    # zero on every side.
    ys, xs = np.nonzero(hard_px)
    x0, y0, x1, y1 = face.bounds
    assert xs.min() >= x0 * 1120 - 1 and xs.max() <= x1 * 1120 + 1
    assert ys.min() >= y0 * 860 - 1 and ys.max() <= y1 * 860 + 1
    outside = float((hard_px & ~inside).sum()) / hard_px.sum()
    assert outside < 0.02, "only the boundary's own feathering lands outside"
    assert (ragged_px & ~inside).sum() > 10 * (hard_px & ~inside).sum()

    # The staircase probe's row: the share of horizontal edges on a mass that has none.
    assert _horizontal_edge_share(ragged, face.box) > 0.10
    assert _horizontal_edge_share(hard, face.box) < 0.06

    # Ragged stays the default, because a mass behind other things wants the brush to
    # break past its boundary.
    plain, plain_px = _laid(tmp_path, face, "ragged")
    assert np.array_equal(plain_px, ragged_px)


def test_a_hard_clip_is_priced_as_it_is_painted_and_replays(tmp_path):
    """Two promises every mass here makes: the quote is the bill, and the log is the
    painting. A clip is where the paint may land, so it has to be in the record."""
    face = _lit_face()
    spec = {"shape": face, "brush": "flat", "color": "burnt_umber", "size": 0.06,
            "edge": "hard", "direction": 20}
    s = Session(400, 300, texture="linen", ground="white", seed=7, out_dir=tmp_path,
                timelapse=False)
    quote = Session(400, 300, texture="linen", ground="white", seed=7, out_dir=tmp_path,
                    timelapse=False)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        assert len(s.paint(spec)) == quote.cost(spec)
    assert s.history.records[-1].params["clip"], "the clip is in the log"
    assert np.array_equal(s.canvas.rgb, s.replay().canvas.rgb)

    saved = s.save(tmp_path / "hard.easel")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        back = Session.load(saved).replay()
    assert np.array_equal(s.canvas.rgb, back.canvas.rgb)


def test_an_unknown_edge_names_all_three(tmp_path):
    s = make(tmp_path)
    with pytest.raises(ValueError, match="'hard'"):
        s.block_in(cell("D5"), "flat", "burnt_umber", edge="sharp")


# -- direction= as a line on the screen ------------------------------------------------
def _screen_angles(session, records):
    """Each pass's angle in **screen** degrees, mod 180."""
    w, h = session.size
    out = []
    for r in records:
        (x0, y0), (x1, y1) = r.points[0], r.points[-1]
        out.append(math.degrees(math.atan2((y1 - y0) * h, (x1 - x0) * w)) % 180.0)
    return out


def test_direction_can_be_the_line_you_can_see(tmp_path):
    """``direction=`` is an angle in the normalised coordinates, and on a canvas that
    is not square that is not the angle on screen: measured, ``direction=-23`` lays
    its passes at **-12 degrees** on 1000x500 and ``45`` runs at **37** on 1024x768.
    Every instrument agrees with every other and all of them disagree with the
    picture, which is where the painter is looking -- one laid *passes along the
    sloped boundary*, the remedy for a gable whose screen slope was 41 degrees, at
    33. So hand over the line and let the engine do the arithmetic."""
    band = Region(0.1, 0.3, 0.9, 0.7)
    kw = dict(brush="flat", color="burnt_umber", size=0.05, density=0.9)

    for (w, h), asked, on_screen in (((1000, 500), -23, 168.0), ((1024, 768), 45, 36.9)):
        s = Session(w, h, texture="linen", ground="white", seed=7, out_dir=tmp_path,
                    timelapse=False)
        s.block_in(band, **kw, direction=asked)
        assert np.median(_screen_angles(s, s.history.records)) == pytest.approx(
            on_screen, abs=0.5), "the units moved"

        # The same angle, handed over as a line drawn at it on the screen.
        long = max(w, h)
        run = 0.4
        line = ((0.30, 0.50),
                (0.30 + run * math.cos(math.radians(asked)) / (w / long),
                 0.50 + run * math.sin(math.radians(asked)) / (h / long)))
        t = Session(w, h, texture="linen", ground="white", seed=7, out_dir=tmp_path,
                    timelapse=False)
        t.block_in(band, **kw, direction=line)
        assert np.median(_screen_angles(t, t.history.records)) == pytest.approx(
            asked % 180.0, abs=0.5), "the line did not run where it was drawn"


def test_a_pair_of_numbers_is_still_two_angles(tmp_path):
    """The one thing the new form must not break: ``direction=(28, 118)`` is a cross
    at a mass's own angle, and a number is not a point."""
    from easel.session import _pass_directions
    assert _pass_directions((28, 118)) == [28.0, 118.0]
    assert _pass_directions(((0.0, 0.0), (1.0, 1.0))) == [45.0]
    assert _pass_directions([((0.0, 0.0), (1.0, 1.0)), 90]) == [45.0, 90.0]

    s = make(tmp_path)
    with pytest.raises(ValueError, match="line of two points"):
        s.block_in(cell("D5"), "flat", "burnt_umber",
                   direction=[(0.1, 0.2), (0.3, 0.4), (0.5, 0.6)])
    with pytest.raises(ValueError, match="zero length"):
        s.block_in(cell("D5"), "flat", "burnt_umber", direction=((0.2, 0.2), (0.2, 0.2)))


def test_a_scumble_takes_the_same_line(tmp_path):
    """``direction=`` means the same thing on every verb that takes one."""
    from easel.session import _angle_of
    assert _angle_of(((0.33, 0.01), (0.58, 0.29))) == pytest.approx(
        math.degrees(math.atan2(0.28, 0.25)))
    s = make(tmp_path)
    p = s.palette
    p["a"] = p.at_value(p.mix("ultramarine", "burnt_umber", 0.5), 0.3)
    p["b"] = p.at_value(p.mix("ultramarine", "burnt_umber", 0.5), 0.7)
    s.scumble(span("A1", "H4"), "a", "b", 8, direction=((0.0, 0.0), (1.0, 0.0)))
    laid = np.median(_screen_angles(s, s.history.records))
    assert min(laid, 180.0 - laid) < 2.0, "a horizontal line did not lay horizontal passes"


# -- a value plan's pairs, answered rather than asked -----------------------------------
def test_the_plan_says_which_close_pairs_actually_meet(tmp_path):
    """``compare({place: value})`` asked the painter *do these two touch?* and the two
    rounds after it was added answered it wrong -- one plan's ``0.00`` pair met along
    its whole far edge. Every place is a rectangle or a shape, and whether two of them
    overlap or share a boundary is one intersection test."""
    s = make(tmp_path)
    plan = {Region(0.0, 0.0, 1.0, 0.3, name="sea"): 0.40,
            Region(0.4, 0.3, 0.6, 0.9, name="tower"): 0.40,
            Region(0.0, 0.9, 1.0, 1.0, name="rock"): 0.42}
    table = s.compare(plan).table()
    assert "sea / tower, 0.00 apart (touch)" in table
    assert "tower / rock, 0.02 apart (touch)" in table
    # Only the touching pairs go under the line; the rest are named as not a fault.
    assert "the rest never meet" in table and "sea / rock (apart)" in table

    # A gap the painter can name: two masses a fine brush apart are adjacent, and the
    # same two a tenth of the canvas apart are not.
    near = {Region(0.1, 0.10, 0.9, 0.40, name="upper"): 0.70,
            Region(0.1, 0.405, 0.9, 0.70, name="lower"): 0.68}
    assert s.compare(near).pairs[0][3] is True
    assert s.compare(near, near=0.001).pairs[0][3] is False

    far = {Region(0.1, 0.10, 0.9, 0.30, name="upper"): 0.70,
           Region(0.1, 0.60, 0.9, 0.90, name="lower"): 0.68}
    result = s.compare(far)
    assert result.pairs[0][3] is False
    assert "none of them meet" in result.table()


# -- a count-only rehearsal: the price of a compound recipe -----------------------------
def _every_verb(s):
    """One call of each verb that marks the canvas, including a compound helper."""
    s.pencil([(0.1, 0.1), (0.5, 0.2), (0.9, 0.1)])
    s.block_in(span("A1", "H3"), "bristle", "burnt_umber", size=0.09, density=0.8,
               direction="axis")
    s.block_in(ellipse(span("C4", "F6")), "flat", "titanium_white", size=0.04,
               solid=True, direction=30, edge="hard")
    s.sweep([(0.05, 0.75), (0.5, 0.72), (0.95, 0.78)], "bristle", "yellow_ochre",
            into="down", depth=0.08, size=0.03)
    s.scumble(span("A7", "H8"), "burnt_umber", "titanium_white", 6)
    s.stroke([(0.2, 0.5), (0.8, 0.55)], "flat", "cerulean", size=0.02)
    s.dab(0.5, 0.5, "round_hard", "titanium_white", size=0.01, press=3)
    s.dry()
    s.glaze([(0.1, 0.45), (0.9, 0.45)], "cadmium_red", opacity=0.08)
    s.smudge([(0.2, 0.62), (0.8, 0.62)], size=0.02)
    s.cover(cell("G7"), "burnt_umber", size=0.03)


def test_a_counted_pass_costs_the_same_as_the_pass_it_is_counting(tmp_path):
    """``cost()`` prices one ``block_in`` or one ``sweep``; a helper that calls a dozen
    verbs had no price at all short of painting it on a copy, and the copy renders
    every dab. One painter budgeted thirteen pots at about 100 strokes, rehearsed at
    **220 against 142 left** at three minutes a go, and rebuilt the recipe from
    strokes at 108. The count is exact rather than an estimate: pass geometry is
    settled before anything is stamped."""
    def run(count_only):
        s = Session(512, 384, texture="linen", ground="toned_grey", seed=7,
                    out_dir=tmp_path, timelapse=False)
        trial = s.scratch(count_only=count_only)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            _every_verb(trial)
        return s, trial

    base, painted = run(False)
    _, counted = run(True)

    assert counted.spent == painted.spent and counted.spent > 0
    assert len(counted.history.records) == len(painted.history.records)
    for a, b in zip(painted.history.records, counted.history.records, strict=True):
        assert (a.kind, a.brush, a.note) == (b.kind, b.brush, b.note)
        assert a.points == b.points
        assert a.dabs == b.dabs
        assert a.params.get("size") == b.params.get("size")
    assert counted.report(since=0) != ""
    # Nothing was laid, so the canvas it borrowed is the canvas it started from.
    assert np.array_equal(counted.canvas.rgb, base.canvas.rgb)
    assert "ground:" not in counted.report(since=0), "it has no ground to report on"


def test_a_counted_film_aimed_at_a_value_says_it_was_not_solved(tmp_path):
    """The one question counting cannot answer. What a film delivers is measured off
    the paint under it, and a count-only run has laid none of its own pass -- so the
    search is skipped rather than answered against a canvas that does not exist, and
    said out loud, because an out-of-reach value raises when it is painted."""
    s = make(tmp_path)
    p = s.palette
    p["dark"] = p.at_value(p.mix("ultramarine", "burnt_umber", 0.5), 0.30)
    p["warm"] = p.at_value(p.mix("cadmium_red", "yellow_ochre", 0.4), 0.62)
    s.block_in(span("A1", "H8"), "flat", "dark", size=0.18, solid=True,
               pressure="even", direction="horizontal")
    s.dry()

    counted = s.scratch(count_only=True)
    with pytest.warns(UserWarning, match="priced but not solved"):
        counted.glaze([(0.2, 0.5), (0.8, 0.5)], "warm", to_value=0.42, size=0.18)
    with warnings.catch_warnings():
        warnings.simplefilter("error")           # said once, however many films
        counted.glaze([(0.2, 0.6), (0.8, 0.6)], "warm", to_value=0.42, size=0.18)
    assert counted.spent == s.spent + 2

    # A rehearsal still solves it, which is what a rehearsal is for.
    rehearsed = s.scratch()
    rehearsed.glaze([(0.2, 0.5), (0.8, 0.5)], "warm", to_value=0.42, size=0.18)
    assert rehearsed.history.records[-1].params["opacity"] != GLAZE_OPACITY


def test_the_shell_can_count_a_pass(tmp_path, capsys):
    """``easel run --count``: the price and the check, no look, nothing committed."""
    script = tmp_path / "pots.py"
    script.write_text(
        "from easel import polygon\n"
        "for i in range(6):\n"
        "    x = 0.08 + i * 0.13\n"
        "    body = polygon([(x, 0.60), (x + 0.09, 0.60), (x + 0.08, 0.72), (x + 0.02, 0.72)])\n"
        "    s.block_in(body, 'flat', 'burnt_sienna', size=0.02, solid=True, direction='axis')\n"
    )
    session = tmp_path / "p.easel"
    assert main(["new", str(session), "--size", "320x240", "--out-dir",
                 str(tmp_path / "out"), "--budget", "300"]) == 0
    capsys.readouterr()
    assert main(["run", str(session), str(script), "--count"]) == 0
    out = capsys.readouterr().out
    assert "Counted pots.py" in out and "Nothing painted, nothing committed." in out
    assert "check over this pass" in out
    assert ".png" not in out, "a counted pass has nothing to look at"

    # And the same pass rehearsed costs the same and does write a look.
    assert main(["run", str(session), str(script), "--rehearse"]) == 0
    rehearsed = capsys.readouterr().out
    counted_strokes = re.search(r"Counted pots\.py: (\d+) strokes", out).group(1)
    assert f"Rehearsed pots.py: {counted_strokes} strokes" in rehearsed
    assert ".png" in rehearsed


# -- a drawing paint cannot bury --------------------------------------------------------
def test_a_guide_survives_the_paint_and_stays_out_of_the_picture(tmp_path):
    """The method's own order costs a second drawing pass: landmarks before anything,
    pencil after the far masses, near masses on top. In one painting the bench tops
    buried the first drawing and the pass before the pots redrew every pot and the can
    before painting them; nine of eleven paintings never made that second pass, and
    the two passages one painter never drew were the two it named weakest. A landmark
    survives because it is a point held beside the canvas; this is the same mechanism
    along a path."""
    s = Session(600, 400, texture="linen", ground="toned_grey", seed=7,
                out_dir=tmp_path, timelapse=False)
    s.guide([(0.05, 0.40), (0.50, 0.42), (0.95, 0.38)], note="bench")
    s.pencil([(0.05, 0.60), (0.95, 0.62)])
    assert s.spent == 0, "neither a guide nor a drawing is a stroke"

    s.block_in(span("A1", "H8"), "flat", "burnt_umber", size=0.2, solid=True,
               opacity=1.0, pressure="even")

    def over(**kw):
        """How many pixels of the view are not the canvas underneath it."""
        view = np.asarray(s.look_image(scale=None, **kw), dtype=int)
        bare = np.asarray(s.canvas.to_srgb8(sketch=kw.get("sketch", True)), dtype=int)
        return int((np.abs(view - bare).sum(axis=2) > 10).sum())

    assert over() > 100, "the guide is gone: paint buried it after all"
    assert over(sketch=False) == 0, "look(sketch=False) has to leave it out"
    # And the picture itself never has it: export goes to the canvas, not the view.
    out = s.export(tmp_path / "painting.png")
    assert np.array_equal(np.asarray(Image.open(out).convert("RGB")),
                          s.canvas.to_srgb8(impasto=True, sketch=True))

    # A full-strength mass buries the pencil line it was drawn over, which is what
    # the two are for: one is the underdrawing, the other is the scaffolding.
    drawn = [ln for ln in s.sketch_lines()]
    assert drawn, "the pencil line is still in the log"
    band = s.canvas.sketch[int(0.60 * 400) - 2:int(0.62 * 400) + 2]
    assert float(band.max()) < 0.05, "the mass did not bury the graphite"


def test_a_guide_is_carried_through_save_load_and_replay(tmp_path):
    """It is held beside the canvas, the way the landmarks are, so it has to travel
    the same way they do -- and an older session file has none and loads with none."""
    s = make(tmp_path)
    s.guide([(0.1, 0.2), (0.9, 0.25)], note="eave")
    s.guide([(0.1, 0.8)], note="pot")
    s.stroke([(0.2, 0.5), (0.8, 0.5)], "flat", "burnt_umber", size=0.05)

    back = Session.load(s.save(tmp_path / "p.easel"))
    assert [g["note"] for g in back.guides] == ["eave", "pot"]
    assert back.guides[0]["points"] == [(0.1, 0.2), (0.9, 0.25)]
    assert [g["note"] for g in s.replay().guides] == ["eave", "pot"]
    assert [g["note"] for g in s.scratch().guides] == ["eave", "pot"]

    assert s.unguide("eave") == 1 and [g["note"] for g in s.guides] == ["pot"]
    assert s.unguide() == 1 and s.guides == []
    with pytest.raises(ValueError, match="at least one point"):
        s.guide([])


# -- a smudge on a long boundary leaves a strip, not a lost edge ------------------------
def _stepped(tmp_path, bound=0.50):
    """A hard step from 0.19 to 0.78 across the canvas, both masses clipped to their
    own edge so the boundary is a boundary and not a half-brush of overlap."""
    s = Session(1024, 768, texture="linen", ground="toned_grey", seed=7,
                out_dir=tmp_path, timelapse=False)
    p = s.palette
    p["dark"] = p.at_value(p.mix("ultramarine", "burnt_umber", 0.5), 0.17)
    p["lit"] = p.at_value(p.mix("yellow_ochre", "titanium_white", 0.5), 0.78)
    for place, colour in ((Region(0.0, 0.0, 1.0, bound), "dark"),
                          (Region(0.0, bound, 1.0, 1.0), "lit")):
        s.block_in(place, "flat", colour, size=0.06, solid=True, opacity=1.0,
                   pressure="even", direction="horizontal", edge="hard")
    s.dry()
    return s


def test_a_smudges_reach_does_not_grow_with_the_join(tmp_path):
    """One pass along each under-bench line, four points along a boundary about 0.4 of
    the canvas long, left a visible lighter band inside the dark for the whole length.
    The session guessed the asymmetric pull was doing something extra on a long
    boundary. It is not: the strip is the calibrated reach and nothing more, flat
    across a sixteen-fold range of join lengths, and what changes is what the same band
    reads as -- a softened corner over a short join, and *dark, mid, light* over a long
    one, which is two edges where there was one."""
    bound, row = 0.50, int(0.50 * 768)

    def strip(length):
        s = _stepped(tmp_path, bound)
        before = s.canvas.values(sketch=False).astype(np.float32) / 255.0
        x0 = 0.5 - length / 2.0
        s.smudge([(x0, bound), (x0 + length, bound)], size=0.02)
        after = s.canvas.values(sketch=False).astype(np.float32) / 255.0
        c0, c1 = int((x0 + length * 0.2) * 1024), int((x0 + length * 0.8) * 1024)
        lift = (after[:, c0:c1].mean(axis=1) - before[:, c0:c1].mean(axis=1))[:row]
        tall = 100.0 * int((lift > 0.01).sum()) / 768
        value = float(after[:, c0:c1].mean(axis=1)[:row][int(np.argmax(lift))])
        return tall, value

    heights, values = zip(*(strip(length) for length in (0.05, 0.10, 0.20, 0.40, 0.80)),
                          strict=True)
    assert max(heights) - min(heights) < 0.2, "the reach grew with the join after all"
    assert all(abs(h - 1.3) < 0.2 for h in heights), "not the calibrated reach"
    # And the band is a mid value, which over a long join is a second edge.
    assert all(abs(v - 0.51) < 0.04 for v in values)


# -- a warning that is said once rather than skimmed five times -------------------------
def _bar_line(session, since):
    """Whether the post-pass check called this pass a stack of bars."""
    return any("stack of bars" in line
               for line in session.report(since=since).split("\n"))


def _lay_bars(session, y0: float, angle: float = 0.0, n: int = 14, note: str = ""):
    """One pass of `n` long parallel marks, laid by hand so each is its own call."""
    before = len(session.history.records)
    for i in range(n):
        y = y0 + i * 0.012
        dx, dy = 0.4 * math.cos(math.radians(angle)), 0.4 * math.sin(math.radians(angle))
        session.stroke([(0.5 - dx / 2, y - dy / 2), (0.5 + dx / 2, y + dy / 2)],
                       "bristle", "burnt_umber", size=0.02, note=note)
    return before


def test_the_stack_of_bars_warning_is_said_once(tmp_path):
    """It fired on five passes of the pier -- the masses, the joists, the water, the
    second water pass and the focal pass -- on a subject that is joists, a waterline
    and a reflection, and does run that way. By the fourth the painter had stopped
    reading the line, which means it was also unread on the pass where it was right.
    The warning's own text concedes *unless the subject runs that way* and cannot tell
    whether the subject does, so it is said once and not again until the picture has
    acquired something that crosses it."""
    s = make(tmp_path)
    assert _bar_line(s, _lay_bars(s, 0.10)), "the first stack of bars goes unreported"
    assert not _bar_line(s, _lay_bars(s, 0.30)), "said twice about an unchanged picture"
    assert not _bar_line(s, _lay_bars(s, 0.50)), "and a third time"


def test_a_crossing_pass_lets_the_warning_speak_again(tmp_path):
    """What re-arms it: the painter answered the warning, the picture picked up
    something square to the bars, and is now stacking them again. That is a different
    situation from the one it was told about, so it is worth a line."""
    s = make(tmp_path)
    assert _bar_line(s, _lay_bars(s, 0.10))
    _lay_bars(s, 0.10, angle=90.0, n=14)                      # the pilings cross it
    assert _bar_line(s, _lay_bars(s, 0.30)), "the picture changed and the line did not"


def test_re_checking_one_pass_says_the_same_thing_twice(tmp_path):
    """A pass is identified by where the painting stood at its end, not by a call
    count, so asking the same question twice is not what spends the warning."""
    s = make(tmp_path)
    since = _lay_bars(s, 0.10)
    assert _bar_line(s, since) and _bar_line(s, since) and _bar_line(s, since)


def test_the_warning_is_still_quiet_after_a_save_and_a_reload(tmp_path):
    """A painting worked from the shell is loaded and saved once per pass -- which is
    how the pier was painted -- so a rule that decays has to decay across that."""
    s = make(tmp_path)
    assert _bar_line(s, _lay_bars(s, 0.10))
    s.save(tmp_path / "p.easel")
    again = Session.load(tmp_path / "p.easel")
    assert not _bar_line(again, _lay_bars(again, 0.30))


def test_a_rehearsal_does_not_spend_the_warning(tmp_path):
    """A rehearsal is thrown away. If rehearsing a pass consumed the one time the
    line is printed, the pass that is paid for would go unwarned."""
    s = make(tmp_path)
    trial = s.scratch()
    assert _bar_line(trial, _lay_bars(trial, 0.10)), "a rehearsal is not told"
    assert _bar_line(s, _lay_bars(s, 0.10)), "and the painting was told by the rehearsal"


def test_a_horizontal_stack_is_called_horizontal(tmp_path):
    """Marks along the horizontal come back as a mixture of 179 and 1 degrees, two
    degrees apart and clustered as such -- and a plain median of them is 90. So the
    commonest stack of bars there is was named *vertical*, and the painter was pointed
    at right angles to the fault."""
    s = make(tmp_path)
    since = _lay_bars(s, 0.10, angle=-0.6)
    line = [ln for ln in s.report(since=since).split("\n") if "stack of bars" in ln]
    assert line and "horizontal" in line[0], line


def test_a_scumble_counts_once_in_a_stack_of_bars(tmp_path):
    """`RECIPES.md`'s graded field -- two scumbles and two crossers -- came back *17 of
    17 long marks ... a stack of bars*, in its own colours a smooth field; and over the
    corpus 10 of the 46 bars lines painters were shown were passes led by a scumble. A
    scumble is one band at one angle whose passes are sized to overlap, and whether
    they show as bars is `scumble-bars`' question at the call. So it counts once --
    and the same bands laid by hand, or as masses, are still a stack."""
    field = make(tmp_path)
    since = len(field.history.records)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        field.scumble(polygon([(-0.06, -0.06), (1.06, -0.06), (1.06, 0.59), (-0.06, 0.62)]),
                      "titanium_white", "cerulean", 7, direction=4)
        field.scumble(polygon([(-0.06, 0.50), (1.06, 0.47), (1.06, 1.06), (-0.06, 1.06)]),
                      "cerulean", "ultramarine", 8, direction=3)
    assert not _bar_line(field, since), "a graded field of two ramps is two bands"

    stacked = make(tmp_path)
    since = len(stacked.history.records)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for top, size in ((0.0, 0.10), (0.25, 0.08), (0.5, 0.09), (0.75, 0.07)):
            stacked.block_in(Region(0.0, top, 1.0, top + 0.25), "bristle", "burnt_umber",
                             size=size, direction="horizontal")
    assert _bar_line(stacked, since), "four bands of masses are still a layer cake"


def test_a_scumble_across_the_bars_is_one_mark_crossing_them(tmp_path):
    """The crossings that re-arm the line, and that it counts once the bands are
    declared, count a scumble once too -- or one band laid across the bars would read
    as eight things crossing them."""
    from easel.session import _crossing_marks

    s = make(tmp_path)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s.scumble(Region(0.2, 0.1, 0.8, 0.9), "titanium_white", "cerulean", 8,
                  direction="vertical")
    assert _crossing_marks(s.history.records, 0.0, s.canvas) == 1


# -- a look is numbered from the directory, not from the session ------------------------
def test_two_sessions_in_one_directory_do_not_write_over_each_other(tmp_path):
    """Four of the nine exercises were run from one script, against four sessions
    sharing an out_dir, and produced one file: `look_001.png`, four times. The images
    were gone before they could be looked at, in the one part of the method that is
    only looking. A counter knows about the session holding it; the directory is the
    thing both sessions can see."""
    first, second = make(tmp_path), make(tmp_path)
    written = [first.look(), second.look(), first.look(), second.look()]
    assert [p.name for p in written] == [
        "look_001.png", "look_002.png", "look_003.png", "look_004.png"]
    assert len(set(written)) == 4 and all(p.exists() for p in written)


def test_a_reopened_painting_carries_on_where_the_directory_left_off(tmp_path):
    """Which is what `easel run` does between passes, and what the counter was
    carried through save and load for. It is not carried any more."""
    s = make(tmp_path)
    s.look()
    s.save(tmp_path / "p.easel")
    assert Session.load(tmp_path / "p.easel").look().name == "look_002.png"


def test_a_preview_and_a_compare_are_numbered_the_same_way(tmp_path):
    """Every view under `out_dir` shares the arrangement, so a second session
    previewing a plan does not land on the first one's preview either."""
    first, second = make(tmp_path), make(tmp_path)
    plan = [{"shape": cell("D5"), "brush": "flat", "color": "burnt_umber", "size": 0.06}]
    assert first.preview(plan).name == "preview_001.png"
    assert second.preview(plan).name == "preview_002.png"


# -- erase() takes both drawings ---------------------------------------------------------
def test_erase_takes_the_scaffolding_with_the_graphite(tmp_path):
    """Redrawing an arrangement left the old scaffolding fan on the view beside the
    new one -- two convergence points in one look, which is exactly the thing the
    drawing exists to judge. `erase()` is the word a painter reaches for, and the
    guide introduces the two drawings in one paragraph, so it takes both."""
    s = make(tmp_path)
    s.pencil([(0.1, 0.2), (0.9, 0.2)])
    s.guide([(0.1, 0.5), (0.9, 0.5)], note="horizon")
    s.guide([(0.2, 0.1), (0.2, 0.3)], note="post")
    s.erase()
    assert s.guides == [], "the scaffolding outlived the drawing it belongs to"
    assert s.sketch_lines() == []


def test_erasing_a_region_cuts_the_scaffolding_where_it_cuts_the_graphite(tmp_path):
    """The same rule as `sketch_lines()`: a path wholly inside goes, one wholly
    outside stays, one that crosses comes back as the pieces left over."""
    s = make(tmp_path)
    s.guide([(0.0, 0.5), (1.0, 0.5)], note="horizon")   # crosses column A
    s.guide([(0.5, 0.1), (0.5, 0.3)], note="post")      # nowhere near it
    assert s.erase(cell("A5")) is not None
    notes = sorted(g["note"] for g in s.guides)
    assert notes == ["horizon", "post"]
    cut = next(g for g in s.guides if g["note"] == "horizon")
    assert cut["points"][0][0] > 0.1, "the crossing path was not cut back"


def test_unguide_still_takes_one_labelled_part_and_leaves_the_rest(tmp_path):
    """`erase()` is for redrawing the whole arrangement. This is the other half."""
    s = make(tmp_path)
    s.guide([(0.1, 0.5), (0.9, 0.5)], note="horizon")
    s.guide([(0.2, 0.1), (0.2, 0.3)], note="post")
    assert s.unguide("post") == 1
    assert [g["note"] for g in s.guides] == ["horizon"]


# -- the guide the painter reads, and the guide the painter draws ------------------------
def test_the_documents_are_easel_docs_and_the_old_name_still_works():
    """`easel.guide` and `s.guide()` were two unrelated things under one name -- the
    module that reads the documents, and the method that lays scaffolding on the view
    -- and both are reached from one session. The module is `easel.docs`; the older
    name forwards, because a name that has shipped does not stop working."""
    import easel
    from easel import docs, guide

    assert guide.front_page() == docs.front_page()
    assert guide.DOCUMENTS == docs.DOCUMENTS
    assert "docs" in easel.__all__ and "guide" in easel.__all__


# -- a failed rehearsal says nothing was committed ---------------------------------------
def test_a_pass_that_raises_on_a_copy_does_not_say_it_was_saved(tmp_path):
    """A script that raised under `--rehearse` printed `easel: script raised, session
    saved with 180 strokes` -- and the count was the painting's, because a scratch
    copy continues the real numbers, so it read exactly like a commit. Nothing was
    committed: `_cmd_run` returns out of the rehearsing branch above the save. The
    painter stopped and verified the stroke count by hand before trusting it, twice."""
    from easel.cli import run_script

    s = make(tmp_path, budget=300)
    s.block_in(cell("D4"), "flat", "burnt_umber", size=0.08)
    before = s.stroke_count
    assert before > 0

    source = ("s.block_in(cell('B2'), 'flat', 'burnt_umber', size=0.08)\n"
              "raise ValueError('the pass broke here')\n")
    copy = s.scratch()
    result = run_script(copy, source, "pass09.py")

    assert result.code == 1
    assert "nothing committed" in result.report
    assert "saved" not in result.report
    # The copy's own marks, not the painting's count carried through it.
    laid = copy.history.stroke_count
    assert laid > 0 and copy.stroke_count == before + laid
    assert f"{laid} of this pass's marks" in result.report
    assert str(copy.stroke_count) not in result.report


def test_a_pass_that_raises_for_real_still_says_what_was_saved(tmp_path):
    """The other half: a half-finished pass on the painting itself is still work, and
    the line that says so is the one a painter has always read."""
    from easel.cli import run_script

    s = make(tmp_path, budget=300)
    result = run_script(s, "s.block_in(cell('B2'), 'flat', 'burnt_umber', size=0.08)\n"
                           "raise ValueError('boom')\n", "pass09.py")
    assert result.code == 1 and result.save
    assert f"session saved with {s.stroke_count} strokes" in result.report


def test_a_copy_that_calls_exit_says_it_too(tmp_path):
    """`exit()` returns through its own branch, which carried the same sentence."""
    from easel.cli import run_script

    s = make(tmp_path, budget=300)
    copy = s.scratch()
    result = run_script(copy, "s.block_in(cell('B2'), 'flat', 'burnt_umber', size=0.08)\n"
                              "exit(1)\n", "pass09.py")
    assert result.code == 1 and "nothing committed" in result.report


def test_the_shell_says_it_on_a_rehearsal_that_raises(tmp_path, capsys):
    """End to end, because the message is printed by the CLI and the bug was that the
    CLI printed it on a path where nothing is written."""
    import easel.cli as cli

    s = make(tmp_path, budget=300)
    s.block_in(cell("D4"), "flat", "burnt_umber", size=0.08)
    s.save(tmp_path / "p.easel")
    script = tmp_path / "pass09.py"
    script.write_text("s.dab((0.5, 0.5), 'round_soft', 'burnt_umber')\nraise ValueError('x')\n")

    code = cli.main(["run", str(tmp_path / "p.easel"), str(script), "--rehearse",
                     "--no-prelude"])
    err = capsys.readouterr().err
    assert code == 1 and "nothing committed" in err
    # And the session on disk is untouched: the count it had before the failed pass.
    assert Session.load(tmp_path / "p.easel").stroke_count == s.stroke_count


# -- sample() over a place that holds two masses ------------------------------------------
def _two_masses(tmp_path):
    """A canvas with a dark field and one light mass standing in it."""
    s = make(tmp_path)
    s.palette["field"] = s.palette.at_value("burnt_umber", 0.25)
    s.palette["thing"] = s.palette.at_value("yellow_ochre", 0.60)
    s.cover(Region(0.0, 0.0, 1.0, 1.0), "field")
    s.dry()
    s.block_in(ellipse(span("C3", "D4")), "flat", "thing", size=0.06, solid=True,
               edge="hard")
    s.dry()
    return s


def test_sampling_across_two_masses_says_the_mean_is_neither(tmp_path):
    """A span that crossed a hand returned 0.342 where the table read 0.258, and the
    edge painted with it landed as a pale halo above the hand. The documentation does
    say to hand it the mass; the painter had read it, and the failure is silent,
    arrives as a number, and goes straight into paint. The engine can answer a
    question the painter cannot ask about their own place: is there one thing here?"""
    s = _two_masses(tmp_path)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        got = s.sample(span("C3", "E5"))
    said = [str(w.message) for w in caught if "more than one mass" in str(w.message)]
    assert said, [str(w.message) for w in caught]
    # It names both parts, each within a hundredth of what was planned, and the
    # number it is about to hand back, which lies between them and is neither.
    dark, light = (float(n) for n in re.findall(r"about (\d\.\d+)", said[0]))
    assert dark == pytest.approx(0.25, abs=0.03)
    assert light == pytest.approx(0.60, abs=0.05)
    here = s.palette.value_of(got)
    assert dark < here < light
    assert f"{here:.3f}" in said[0] and "hand it the mass" in said[0]


def test_handing_it_the_mass_is_silent_however_wide_the_mass_is(tmp_path):
    """The remedy the warning names cannot be the thing that trips it. A mass with a
    turn in it is spread by design -- the hands that raised this measure 0.093 and
    0.100 handed whole, both above the threshold -- so a shape is never asked."""
    s = _two_masses(tmp_path)
    mass = ellipse(span("C3", "D4"))
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        s.sample(mass)
        # ...and one that is genuinely two masses, still handed in as a shape.
        s.sample(hull([(0.05, 0.05), (0.95, 0.05), (0.95, 0.95), (0.05, 0.95)]))
    assert not [w for w in caught if "more than one mass" in str(w.message)]


def test_one_mass_with_a_glint_on_it_is_not_two(tmp_path):
    """A place that is 97% one thing has a mean that is still that thing's. The
    minority share is what keeps a highlight, a bean or a signature mark from turning
    every cell it lands in into a warning."""
    s = _two_masses(tmp_path)
    s.dab(0.80, 0.80, "round_hard", "thing", size=0.02)
    s.dry()
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        s.sample(span("F6", "H8"))
    assert not [w for w in caught if "more than one mass" in str(w.message)]


def test_a_clear_patch_of_one_mass_is_silent(tmp_path):
    """The other end of it: the cell a painter is right to sample."""
    s = _two_masses(tmp_path)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        s.sample(cell("A1"))
    assert not caught, [str(w.message) for w in caught]


def test_the_check_reads_the_paint_and_not_the_place(tmp_path):
    """A bare canvas is one mass however it is sampled, so the rule cannot fire before
    anything is painted -- which is when `s.sample()` is the documented way to read
    the ground."""
    s = make(tmp_path)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        s.sample()
        s.sample(span("A1", "H8"))
    assert not caught, [str(w.message) for w in caught]


# -- clip=, edge= and solid= on every verb that lays paint -----------------------------
def _held_outside(s, place, before) -> float:
    """The share of the pixels outside ``place`` that this session's paint moved.

    *Outside* is where the place covers nothing at all, rather than where a pixel's
    centre falls outside it: a clip multiplies by coverage, so the boundary's own
    half-covered pixels take half a dab and are inside the promise.
    """
    outside = place.coverage(s.canvas.width, s.canvas.height) <= 0.0
    moved = np.abs(s.canvas.rgb - before).sum(axis=2) > 1e-4
    return float((moved & outside).sum()) / float(max(outside.sum(), 1))


def test_every_verb_that_lays_paint_takes_clip(tmp_path):
    """``clip=`` was a named argument of ``stroke`` alone, so the four mass verbs came
    back with *clip= is not a brush field* -- an error that named neither ``stroke``
    nor ``edge="hard"``, the two things that would have answered the question. A mass
    is the call that most wants to end on a line rather than on its own tip."""
    s = make(tmp_path)
    s.palette["c"] = s.palette.mix("ultramarine", "burnt_umber", 0.4)
    window = polygon([(0.05, 0.05), (0.45, 0.05), (0.45, 0.95), (0.05, 0.95)],
                     name="window")
    for lay in (
        lambda: s.block_in(span("C3", "F6"), "flat", "c", size=0.05, clip=window),
        lambda: s.sweep([(0.2, 0.30), (0.8, 0.34)], "flat", "c", into="down",
                        depth=0.12, size=0.05, clip=window),
        lambda: s.cover(span("C3", "F6"), "c", size=0.05, clip=window),
        lambda: s.scumble(span("C3", "F6"), "c", "titanium_white", 4, size=0.05,
                          clip=window),
    ):
        before = s.canvas.rgb.copy()
        assert lay(), "the call lays paint"
        assert _held_outside(s, window, before) == 0.0


def test_a_mass_held_by_two_places_lands_where_they_agree(tmp_path):
    """``edge="hard"`` is a clip pointed at the mass's own outline, so a mass given both
    is held by both. The log carries one outline as it always has and a pair as a pair,
    which is what makes a held mass replay as itself."""
    s = make(tmp_path)
    s.palette["c"] = s.palette.mix("ultramarine", "burnt_umber", 0.4)
    mass = polygon([(0.2, 0.2), (0.8, 0.25), (0.7, 0.8), (0.25, 0.7)], name="mass")
    window = polygon([(0.0, 0.0), (0.5, 0.0), (0.5, 1.0), (0.0, 1.0)], name="window")
    before = s.canvas.rgb.copy()
    records = s.block_in(mass, "flat", "c", size=0.05, edge="hard", clip=window)
    assert _held_outside(s, mass, before) == 0.0
    assert _held_outside(s, window, before) == 0.0
    # One hold is logged as one outline, as it has been since edge="hard" was built;
    # two are logged as two, so an older build refuses the file rather than reading
    # the pair as a single outline and painting something else.
    held = records[0].params["clip"]
    assert len(held) == 2 and isinstance(held[0][0], list)
    one = s.stroke([(0.1, 0.5), (0.9, 0.5)], "flat", "c", size=0.05, clip=mass)
    assert isinstance(one.params["clip"][0][0], float)
    assert np.array_equal(s.replay().canvas.rgb, s.canvas.rgb)


def test_scumble_takes_the_hard_edge_a_mass_takes(tmp_path):
    """A wide band scumbled at an angle paints up to three times its own area, because
    the auto brush is measured across the band's bounding box. ``edge="hard"`` is the
    remedy the plan names, and it was a ``block_in`` word: on a scumble it raised an
    error naming ``block_in()`` and ``sweep()`` and not the caller."""
    s = make(tmp_path)
    s.palette["c"] = s.palette.mix("ultramarine", "burnt_umber", 0.4)
    band = span("B3", "G5")
    before = s.canvas.rgb.copy()
    s.scumble(band, "c", "titanium_white", 8, direction=30, edge="hard")
    assert _held_outside(s, polygon(band), before) == 0.0
    loose = make(tmp_path)
    loose.palette["c"] = loose.palette.mix("ultramarine", "burnt_umber", 0.4)
    was = loose.canvas.rgb.copy()
    loose.scumble(band, "c", "titanium_white", 8, direction=30)
    assert _held_outside(loose, polygon(band), was) > 0.05
    with pytest.raises(ValueError, match="a passage has none to draw"):
        s.scumble(band, "c", "titanium_white", 8, edge="clean")


def test_solid_is_taken_wherever_it_has_a_meaning(tmp_path):
    """``solid=True`` is ``load=1.0, load_falloff=0.0`` -- the clause painters type by
    hand most often, and the one ``block_in`` has always had a word for. Everywhere
    else it raised a teaching error that explained the pair rather than taking it."""
    def paint(**kw):
        s = make(tmp_path)
        s.palette["c"] = s.palette.mix("ultramarine", "burnt_umber", 0.4)
        s.stroke([(0.1, 0.2), (0.9, 0.25)], "flat", "c", size=0.06, **kw)
        s.sweep([(0.15, 0.5), (0.85, 0.55)], "flat", "c", into="down", depth=0.1,
                size=0.05, **kw)
        s.scumble(span("B6", "G8"), "c", "titanium_white", 4, size=0.05, **kw)
        return s.canvas.rgb

    assert np.array_equal(paint(solid=True), paint(load=1.0, load_falloff=0.0))
    # ...and an explicit load= beside it still wins, as it does on block_in.
    assert np.array_equal(paint(solid=True, load=0.3), paint(load=0.3, load_falloff=0.0))
    s = make(tmp_path)
    with pytest.raises(TypeError, match="lays that pair already"):
        s.cover("upper-half", "burnt_umber", solid=True)


def test_a_band_scumbled_the_short_way_says_its_passes_are_dabs(tmp_path):
    """The ends check returned at once for a rectangle, so the guide's own ``span(...)``
    bands could never trip it: a band crossed the short way came back as a row of dabs
    blooming past it, in silence. A band is not a wedge -- its passes vary only at the
    corners -- so what it is asked is whether the whole band is narrower than its
    brush."""
    s = make(tmp_path)
    s.palette["c"] = s.palette.mix("ultramarine", "burnt_umber", 0.4)
    with pytest.warns(UserWarning, match="every pass is shorter"):
        s.scumble(span("A1", "B8"), "c", "titanium_white", 8, direction="horizontal")
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        s.scumble(span("A1", "B8"), "c", "titanium_white", 8)            # the long way
        s.scumble(span("A1", "H4"), "c", "titanium_white", 8, direction=30)


# -- a plan that holds every verb that lays a passage ----------------------------------
def test_a_passage_and_a_burial_are_planned_priced_and_painted_as_themselves(tmp_path):
    """The planner knew three kinds -- mark, mass, sweep -- so a ``scumble`` or a
    ``cover`` could not be planned, priced, previewed or rehearsed at all: the first
    raised *a stroke spec needs 'points'* and the second was quoted as something else.
    They are the two verbs a painter reaches for after looking at what is there, which
    is exactly when a plan is being written."""
    s = make(tmp_path)
    s.palette["a"] = s.palette.mix("ultramarine", "burnt_umber", 0.4)
    s.palette["b"] = s.palette.tint("yellow_ochre", 0.5)
    plan = [{"band": span("B3", "G5"), "color_a": "a", "color_b": "b", "n": 8},
            {"cover": cell("D7"), "color": "a"},
            {"shape": ellipse(span("C6", "E8")), "color_a": "a", "color_b": "b",
             "n": 5, "direction": "inward"}]
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        quoted = s.cost(plan, share=0)
        line = s.cost_line(plan)
        s.preview(plan)
        s.rehearse(plan)
        laid = s.paint(plan)
    assert quoted == len(laid), line
    assert "passes stepping across" in line and "rings stepping in" in line
    # A rehearsal is free, and the plan it rehearsed is the plan it painted.
    assert s.spent == len(laid)


def test_a_scumble_shaped_plan_is_not_priced_as_a_block_in(tmp_path):
    """The silent half of that bug: an entry carrying ``shape=`` and the two colours a
    passage steps between went down the mass branch and was quoted as a block-in --
    five where the call lays eight -- and raised only when ``paint`` reached the keys
    ``block_in`` does not take. The two colours are what tell a passage from a mass
    filling the same place."""
    s = make(tmp_path)
    s.palette["a"] = s.palette.mix("ultramarine", "burnt_umber", 0.4)
    s.palette["b"] = s.palette.tint("yellow_ochre", 0.5)
    band = {"shape": ellipse(span("C3", "F5")), "color_a": "a", "color_b": "b", "n": 8}
    mass = {"shape": ellipse(span("C3", "F5")), "color": "a"}
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        assert s.cost(band, share=0) == 8
        assert s.cost(band, share=0) != s.cost(mass, share=0)
        assert len(s.paint(band)) == 8


def test_a_plan_that_cannot_be_painted_is_not_priced(tmp_path):
    """``cost`` walks the passes and never touches the brush overrides, so a misspelled
    ``size`` priced happily at the default and raised when the same plan was painted --
    a quote for a plan that cannot be painted, which is worse than no quote. The MCP
    server has refused these since it was built; the library priced them."""
    s = make(tmp_path)
    for entry, says in (
        ({"shape": cell("D5"), "color": "burnt_umber", "sise": 0.04}, "A mass"),
        ({"points": [(0.2, 0.2), (0.8, 0.8)], "to_value": 0.5}, "A stroke"),
        ({"band": span("B3", "G5"), "color_a": "burnt_umber", "color_b": "white",
          "into": "down"}, "A scumble"),
        ({"cover": cell("D5"), "color": "burnt_umber", "wander": False}, "A cover"),
    ):
        with pytest.raises(ValueError, match=says):
            s.cost(entry, share=0)


# -- the count the subject line divides by ---------------------------------------------
def test_the_subject_line_counts_what_the_budget_counts(tmp_path):
    """*subject: 172 of 411 marks* against a budget that said 408: the line built its
    total out of every mark of paint, and the budget exempts the first five marks noted
    ``signature``. Two counts of the same painting, printed a line apart."""
    s = make(tmp_path)
    for i in range(5):
        s.stroke([(0.1 + i * 0.1, 0.3), (0.2 + i * 0.1, 0.4)], "flat", "burnt_umber",
                 size=0.04, note="subject rock")
    for i in range(3):
        s.stroke([(0.80, 0.90 - i * 0.02), (0.88, 0.92 - i * 0.02)], "liner",
                 "burnt_umber", note="signature")
    s.pencil([(0.1, 0.1), (0.2, 0.2)])
    assert s.stroke_count == 5
    line = [ln for ln in s.report().splitlines() if "subject:" in ln][0]
    assert "5 of 5 marks" in line and "(100%)" in line


# -- three namespaces, and the one with no way out -------------------------------------
def test_a_ground_is_a_colour_and_says_so_when_it_is_used_as_one(tmp_path):
    """A ground is named in the same breath as a size and then reached for as a colour,
    and the palette listed every pigment and slot without noticing that the name it was
    handed is a valid ground. Nothing exposed the ground as a colour either, so sampling
    an unpainted corner -- which measures the tooth's shading too -- was the only route
    to the value a painter can plainly see."""
    s = make(tmp_path)
    with pytest.raises(KeyError, match="is a ground, not a pigment"):
        s.palette["toned_grey"]
    with pytest.raises(ValueError, match="is a pigment, not a ground"):
        Session(80, 60, ground="ultramarine", out_dir=tmp_path)
    # ...and the ground is a colour, ready for the calls that take one.
    assert s.palette.value_of(s.ground) == pytest.approx(
        s.palette.value_of(s.sample(cell("A1"))), abs=0.02)
    s.palette["sky"] = s.palette.mix(s.ground, "ultramarine", 0.3)
    s.block_in(cell("D5"), "flat", s.palette.at_value(s.ground, 0.62), size=0.05)


# -- a documented trap the engine can detect -------------------------------------------
def test_a_0_to_255_colour_raises_and_names_both_fixes(tmp_path):
    """It clamped, so `[13, 12, 16]` -- a dark read straight off a photograph -- came
    back **white**, in silence, and `PAINTING.md` documented the trap. A documented trap
    the engine can see is a bug."""
    s = make(tmp_path)
    with pytest.raises(ValueError, match=r"0\.\.1, not 0\.\.255"):
        s.stroke([(0.2, 0.2), (0.6, 0.6)], "flat", [13, 12, 16])
    try:
        s.palette["dark"] = [200, 100, 50]
    except ValueError as caught:
        assert "(0.7843, 0.3922, 0.1961)" in str(caught) and "#c86432" in str(caught)
    # The form it names works, and so does every form that always did.
    s.palette["dark"] = [0.051, 0.047, 0.063]
    s.palette["same"] = "#0d0c10"


# -- the holes inside a solid mass, and whose they are ---------------------------------
def test_a_solid_comb_says_what_share_of_the_mass_comes_back_bare(tmp_path):
    """Reported twice as *shaped block-in paths wandering apart*, and it is neither the
    paths nor the shape: a `flat` leaves 0.0000% bare at every size and density tried,
    and a comb leaves holes because `solid=` sets `load` and `load_falloff` and nothing
    else. A fact at the call with the prices on it, and no default moved -- a comb is
    the right brush for anything with strands in it."""
    s = make(tmp_path)
    with pytest.warns(UserWarning, match="closes the gaps along each pass"):
        s.block_in(span("B3", "F6"), "bristle", "burnt_umber", size=0.04, solid=True)
    # The same, typed out by hand, is the same mass and says the same thing.
    with pytest.warns(UserWarning, match="3.16%"):
        s.block_in(span("B3", "F6"), "bristle", "burnt_umber", size=0.04,
                   load=1.0, load_falloff=0.0)
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        s.block_in(span("B3", "F6"), "flat", "burnt_umber", size=0.04, solid=True)
        s.block_in(span("B3", "F6"), "bristle", "burnt_umber", size=0.04, solid=True,
                   density=1.2)
        s.block_in(span("B3", "F6"), "bristle", "burnt_umber", size=0.04)


# -- a mass laid over paint that is still wet ------------------------------------------
def test_a_mass_can_dry_what_it_is_laid_over_first(tmp_path):
    """The rings that cost one painter their only `undo` were laid over a bezel still
    wet from the pass before: a film at `opacity=0.15` leaves about 0.13 wetness behind,
    which is past the 0.10 that makes a new mass. `cover()` has dried what it is about
    to bury since it was built; a mass could not, short of a `dry()` of its own."""
    s = make(tmp_path)
    s.palette["dark"] = s.palette.mix("ultramarine", "burnt_umber", 0.45)
    s.palette["pale"] = s.palette.tint("yellow_ochre", 0.6)

    def over_wet(**kw):
        t = s.scratch()
        t.block_in(cell("D5"), "flat", "dark", size=0.05, solid=True)
        t.block_in(cell("D5"), "flat", "pale", size=0.05, solid=True, **kw)
        return t.palette.value_of(t.sample(cell("D5").inset(0.02)))

    wet, dried = over_wet(), over_wet(dry_first=True)
    dark = s.palette.value_of(s.palette["dark"])
    pale = s.palette.value_of(s.palette["pale"])
    # Wet, the pale mass takes some of the dark under it and lands between the two;
    # dried, it lands as itself. Neither reaches the mixture exactly -- a mass is
    # paint over paint, not a fill.
    assert dark < wet < dried < pale
    assert dried - wet > 0.02


# -- the time-lapse: its size, and where a rehearsal's frames are -----------------------
def test_a_rehearsal_says_where_the_frames_are(tmp_path):
    """A rehearsal copy is created with the time-lapse off -- a film of a scrap of
    canvas is not what anybody wants -- so ``timelapse_gif`` on one raised *No
    time-lapse frames were recorded. Create the session with `timelapse=True`*, which
    is the one thing the painting already did."""
    s = make(tmp_path, timelapse=True)
    s.stroke([(0.1, 0.5), (0.9, 0.5)], "flat", "burnt_umber", size=0.05)
    trial = s.scratch()
    trial.stroke([(0.1, 0.6), (0.9, 0.6)], "flat", "burnt_umber", size=0.05)
    with pytest.raises(ValueError, match="rehearsal copy"):
        trial.timelapse_gif(tmp_path / "nope.gif")
    with pytest.raises(ValueError, match="rehearsal copy"):
        trial.contact_sheet(tmp_path / "nope.png")
    # The painting it came from has them, which is what the message says.
    assert s.timelapse_gif(tmp_path / "yes.gif").exists()


def test_the_frame_size_is_reachable_and_the_film_can_be_rebuilt(tmp_path):
    """Frames were recorded at 360 px beside a 1440 px painting, stored in the .easel
    file at that size, and nothing on the session or the CLI could ask for another --
    so a painting already made could not be helped. Two answers: say the size up
    front, or rebuild the film from the log afterwards, which needs no frames at all."""
    s = make(tmp_path, timelapse=120)
    for i in range(4):
        s.stroke([(0.1, 0.2 + i * 0.15), (0.9, 0.25 + i * 0.15)], "flat",
                 "burnt_umber", size=0.05)
    assert s.frame_px == 120
    # A frame is downsampled by a whole number of pixels, so the size asked for is a
    # ceiling rather than an exact width -- and it is a real one: left alone, this
    # canvas is under the 360 default and records its frames full size.
    assert max(Image.open(s.timelapse_gif(tmp_path / "small.gif")).size) <= 120
    # ...and from the log, at whatever size is asked for, this painting's own by default.
    assert max(Image.open(s.timelapse_gif(tmp_path / "big.gif", from_log=True)).size) == 320
    assert 120 < max(Image.open(
        s.timelapse_gif(tmp_path / "mid.gif", from_log=True, scale=200)).size) <= 200
    # A painting that recorded nothing is the case this really answers.
    off = make(tmp_path, timelapse=False)
    off.stroke([(0.1, 0.5), (0.9, 0.5)], "flat", "burnt_umber", size=0.05)
    with pytest.raises(ValueError, match="No time-lapse frames"):
        off.timelapse_gif(tmp_path / "none.gif")
    assert off.timelapse_gif(tmp_path / "rebuilt.gif", from_log=True).exists()


def test_a_mark_snapshots_the_box_it_can_reach_and_undoes_exactly(tmp_path):
    """Every stroke copied the whole canvas for undo -- 33 MB at 1440x960, about 800 MB
    over the twenty-four kept, and 6.3 ms before a dab lands. A mark touches a few
    percent of a canvas. The box is the path's own reach with the brush's jitter at six
    standard deviations on it, and undo is exact or it is nothing."""
    s = make(tmp_path, timelapse=False)
    s.palette["c"] = s.palette.mix("ultramarine", "burnt_umber", 0.4)
    s.block_in("upper-half", "bristle", "c", size=0.08, density=0.7)
    before, wet_before = s.canvas.rgb.copy(), s.canvas.wetness.copy()
    s.dab(0.5, 0.7, "round_hard", "c", size=0.05)
    s.stroke([(0.15, 0.8), (0.85, 0.78)], "flat", "c", size=0.04)
    kept = s.history._snapshots[-1]
    assert kept["box"] is not None
    assert kept["rgb"].nbytes < s.canvas.rgb.nbytes / 4
    assert s.undo(2) == 2
    assert np.array_equal(before, s.canvas.rgb)
    assert np.array_equal(wet_before, s.canvas.wetness)


def test_a_long_painting_stops_building_frames_it_would_throw_away(tmp_path,
                                                                   monkeypatch):
    """Past MAX_FRAMES the sequence is thinned by halves, so most of the frames a long
    painting built were built and then dropped -- at 42 ms each, on the dearest thing a
    mark does that is not paint. The film is the same one; the work is not done."""
    from easel.canvas import Canvas
    from easel.history import MAX_FRAMES

    built = []
    real = Canvas.thumbnail_srgb8

    def counted(self, *args, **kwargs):
        built.append(1)
        return real(self, *args, **kwargs)

    monkeypatch.setattr(Canvas, "thumbnail_srgb8", counted)
    s = make(tmp_path, timelapse=True)
    marks = MAX_FRAMES * 3
    for i in range(marks):
        s.dab(0.05 + (i % 20) * 0.045, 0.05 + (i // 20) * 0.03, "round_hard",
              "burnt_umber", size=0.01)
    assert s.history.frame_count <= MAX_FRAMES
    assert len(built) < marks * 0.75


# -- calibrating a mark before committing to it ----------------------------------------
def test_one_sheet_of_the_same_mark_at_several_settings(tmp_path):
    """*Easier calibration of size, load and pressure before committing.* A rehearsal
    already answers it one setting at a time, which makes four sizes four rehearsals,
    four whole-canvas renders, and four pictures nobody can hold side by side -- and a
    question about size is a question only comparison answers."""
    s = make(tmp_path)
    s.palette["dark"] = s.palette.mix("ultramarine", "burnt_umber", 0.45)
    plan = [{"points": [(0.3, 0.4), (0.6, 0.55)], "brush": "round_hard",
             "color": "dark"}]
    sheet = s.rehearse(plan, region=span("C3", "F6"),
                       vary={"size": [0.01, 0.02, 0.04, 0.07]})
    one = s.rehearse(plan, region=span("C3", "F6"))
    wide, tall = Image.open(sheet).size
    was_wide, was_tall = Image.open(one).size
    # Four panels of the same place, side by side, inside the long side asked for --
    # against one rehearsal of it, which is the shape of the place itself.
    assert wide > 3 * tall and was_wide < 2 * was_tall
    assert s.spent == 0                                 # free, like any rehearsal
    # Two arguments vary together, which is why there is a ceiling on how many.
    s.rehearse(plan, vary={"size": [0.02, 0.05], "pressure": ["taper", "even"]})
    with pytest.raises(ValueError, match="past the 12"):
        s.rehearse(plan, vary={"size": [0.01, 0.02, 0.04, 0.07],
                               "load": [0.2, 0.5, 1.0, 1.0]})
    with pytest.raises(ValueError, match="nothing to try"):
        s.rehearse(plan, vary={"size": []})


def test_a_rehearsed_setting_is_the_one_that_lands(tmp_path):
    """The whole bargain of a rehearsal: what it shows is what the painting gets. A
    sheet spends no stream either -- each panel is its own copy -- so the setting
    chosen off it lands as it was shown."""
    s = make(tmp_path)
    s.palette["dark"] = s.palette.mix("ultramarine", "burnt_umber", 0.45)
    plan = [{"points": [(0.3, 0.4), (0.6, 0.55)], "brush": "round_hard",
             "color": "dark", "size": 0.04}]
    s.rehearse(plan, vary={"size": [0.01, 0.02, 0.04]})
    after_sheet = s.scratch()
    after_sheet.paint(plan)
    plain = make(tmp_path)
    plain.palette["dark"] = plain.palette.mix("ultramarine", "burnt_umber", 0.45)
    plain.paint(plan)
    assert np.array_equal(after_sheet.canvas.rgb, plain.canvas.rgb)


# -- the plan a painter declares: workstream C -----------------------------------------
#
# *Useful heuristics, but they're philosophy, not errors, and it doesn't know which.*
# Inventoried and true: before 0.6.0 no acknowledge, suppress or declare mechanism
# existed anywhere in the API, so a painter whose subject really was horizontal could
# only read the same warning again. Every test here is one thing a painter can now write
# down, and what the check does with it -- because a declaration that changes nothing is
# a comment.
def _plan_line(session, label: str, since=None) -> str:
    """The one line of the post-pass check that starts with `label`, or ''."""
    return next((line.strip() for line in session.report(since=since).split("\n")
                 if line.strip().startswith(label)), "")


def test_a_plan_says_which_close_places_meet_and_stays_quiet_about_the_rest(tmp_path):
    """A plan finished all-green with two of its places planned `0.00` apart: they were
    the two that met, and one dissolved into the other exactly there. Three of that
    plan's four close pairs were fine, because those masses never met -- so *touching*
    is the whole of what picks a pair out, and the question is asked on the empty canvas,
    where it is free."""
    s = make(tmp_path)
    upper, lower = span("A1", "H4"), span("A5", "H8")
    with pytest.warns(UserWarning, match="read as one where they meet") as caught:
        s.plan(values={upper: 0.40, lower: 0.44})
    assert caught[0].message.code == "plan-pairs"
    assert "0.04 apart" in str(caught[0].message)

    # Two places just as close in value, nowhere near each other on the canvas.
    apart = make(tmp_path)
    with warnings.catch_warnings():
        warnings.simplefilter("error")           # any notice at all fails the test
        apart.plan(values={cell("A1"): 0.40, cell("H8"): 0.44})
    assert apart.plan_pairs() and not apart.plan_pairs()[0][3]


def test_the_same_plan_declared_again_says_nothing(tmp_path):
    """A `prelude.py` runs before every pass, so re-declaring is the ordinary case and
    not the odd one. Without this the pairs notice would be a thing printed once a pass,
    which is rule 7 broken by the one declaration meant to quieten the check down."""
    s = make(tmp_path)
    values = {span("A1", "H4"): 0.40, span("A5", "H8"): 0.44}
    with pytest.warns(UserWarning, match="plan"):
        s.plan(values=values)
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        s.plan(values=values)                    # same plan
        s.plan(why="and a sentence about it")     # a different field, same values
    # Changing the values is news again.
    with pytest.warns(UserWarning, match="read as one where they meet"):
        s.plan(values={span("A1", "H4"): 0.41, span("A5", "H8"): 0.44})


def test_the_check_measures_the_canvas_against_the_declared_values(tmp_path):
    """The `plan:` line: what a painter promised, against what is there. The sign is
    the canvas minus the plan, so `+` is lighter than promised."""
    s = make(tmp_path)
    upper, lower = span("A1", "H4"), span("A5", "H8")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s.plan(values={upper: 0.95, lower: 0.30})
        since = len(s.history.records)
        s.block_in(upper, "flat", "white", direction="axis")
    line = _plan_line(s, "plan:", since)
    assert line.startswith("plan: 1 of 2 places inside 0.10"), line
    # The one that is out is the one nobody painted, and it is named with its miss.
    assert "A5:H8 +0.2" in line, line
    # No values declared, no line: the check does not ask for a plan.
    assert not _plan_line(make(tmp_path), "plan:", 0)


def test_the_check_says_when_something_else_took_the_light(tmp_path):
    """One painting reached stroke 217 before it had any light at all. The declaration
    is the place the picture is lit by; the line ranks the plan's places and says when
    the light is somewhere else."""
    s = make(tmp_path)
    lamp, wall = span("A1", "D4"), span("E1", "H4")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s.plan(values={lamp: 0.70, wall: 0.30}, lightest=lamp)
        since = len(s.history.records)
        s.block_in(wall, "flat", "white", direction="axis")      # the wall, not the lamp
    line = _plan_line(s, "lightest:", since)
    assert line.startswith("lightest: E1:H4 reads"), line
    assert "the plan's own light" in line and "under" in line

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s.block_in(lamp, "flat", "white", direction="axis")      # and now the lamp
    assert "the lightest of the 2 places planned" in _plan_line(s, "lightest:", since)


def test_the_subject_share_is_compared_without_being_passed_in(tmp_path):
    """`report(subject_share=)` has taken this since 0.4.0 and neither `easel run` nor
    the MCP `run` tool ever passed it, so a painter working anywhere but a Python prompt
    had never once seen the comparison. Declared, it is always there."""
    s = make(tmp_path)
    s.plan(subject_share=0.40)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s.stroke([(0.2, 0.3), (0.5, 0.35)], "flat", "burnt_umber", note="subject")
    assert "against 40% planned" in _plan_line(s, "subject:")
    # The argument is the more specific of the two and wins.
    assert "against 90% planned" in s.report(subject_share=0.9)


def test_declaring_the_bands_turns_the_bars_warning_into_a_count(tmp_path):
    """The noisiest rule the engine has -- 47 of the corpus's 325 painted passes, 14%,
    after the decay that already cut the pier's seven firings to three -- and the one two
    painters learnt to skim. Its own text concedes *unless the subject runs that way*,
    it cannot tell whether the subject does, and the painter can. Declared, it stops
    warning and asks the method's next question instead."""
    s = make(tmp_path)
    s.plan(bands="subject")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        since = _lay_bars(s, 0.10)
    line = _plan_line(s, "- bands declared as the subject:", since)
    assert line, s.report(since=since)
    assert "nothing crosses them yet" in line
    assert not _bar_line(s, since), "declared, and still warned about"

    # And what crosses them is counted over the picture, which is the question.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        _lay_bars(s, 0.10, angle=90.0)
        since = _lay_bars(s, 0.30)
    assert "14 long marks in the picture cross them" in s.report(since=since)

    # Undeclared, the warning is unchanged -- and names the declaration.
    plain = make(tmp_path)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        since = _lay_bars(plain, 0.10)
    assert _bar_line(plain, since)
    assert "s.plan(bands='subject')" in plain.report(since=since)


def test_declaring_a_buried_ground_prints_the_number_without_asking_for_some(tmp_path):
    """Five of seven painters in one round accepted `ground: 0.0x% … the checklist asks
    for some` by hand, three naming the same cause: the breather they were told to leave
    was buried by the field they were told to lay. Both are right, and the picture
    decides which."""
    def bury(session):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            session.block_in("canvas", "flat", "white", direction="axis", solid=True)
        return session

    asked = bury(make(tmp_path))
    assert "the checklist asks for some" in _plan_line(asked, "ground:")

    declared = make(tmp_path)
    declared.plan(ground="buried")
    bury(declared)
    line = _plan_line(declared, "ground:")
    assert "buried, as the plan says" in line, line
    assert "the checklist asks for some" not in line
    # The number is still printed: a declaration is not a silence.
    assert "% of the canvas is still bare ground" in line


def test_a_plan_changes_what_it_is_given_and_keeps_the_rest(tmp_path):
    """So the values can be declared once in a `prelude.py` and the lightest place added
    from a pass, without the pass having to retype a plan it did not write."""
    s = make(tmp_path)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s.plan(why="the light arrives from below", values={span("A1", "H4"): 0.70},
               subject_share=0.40)
        added = s.plan(lightest=span("A1", "H4"))
    assert added.why == "the light arrives from below"
    assert [p.name for p in added.values] == ["A1:H4"] and added.subject_share == 0.40
    assert added.lightest.name == "A1:H4"
    # The empty version of a field clears that one; `clear` starts again.
    assert s.plan(values={}).values == ()
    assert not s.plan(clear=True).declared
    with pytest.raises(ValueError, match="runs 0..1"):
        s.plan(subject_share=40)
    with pytest.raises(ValueError, match="the word is 'subject'"):
        s.plan(bands="horizontal")
    # A place in a value plan promises a value; a place named for another reason is what
    # lightest= is for. And a place has to be somewhere on this canvas, or every line the
    # check prints about it would be a `nan` with nothing to say why.
    with pytest.raises(ValueError, match="no value"):
        s.plan(values={cell("D5"): None})
    with pytest.raises(ValueError, match="covers no pixels"):
        s.plan(values={ellipse((0.5, 0.5), 0.0005, 0.0005): 0.5})


def test_a_plan_survives_the_session_file_and_an_older_one_has_none(tmp_path):
    """A painting worked from the shell is loaded and saved once a pass -- which is how
    the pier was painted -- so a plan that did not survive that would have to be
    re-declared by every script that wanted it. New key, read with `.get`, so a 0.5.0
    file opens with no plan and a 0.5.0 build opens this one."""
    path = tmp_path / "p.easel"
    s = make(tmp_path)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s.plan(why="a sentence", values={span("A1", "H4"): 0.70},
               lightest=span("A1", "H4"), subject_share=0.4, bands="subject",
               ground="buried")
    s.save(path)
    back = Session.load(path)
    assert back.plan() == s.plan()               # every field, through JSON
    assert back.plan().values[0].outline == s.plan().values[0].outline
    # And equal well enough that re-declaring it says nothing. This is the whole painter
    # path: a `prelude.py` runs before every pass and declares the plan again, against a
    # session loaded from the file, so a plan that came back merely *similar* would have
    # the pairs notice printed once a pass for the rest of the painting.
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        back.plan(why="a sentence", values={span("A1", "H4"): 0.70},
                  lightest=span("A1", "H4"), subject_share=0.4, bands="subject",
                  ground="buried")

    # The same helper `tests/test_notices.py` wrote for the `notices` key, since this is
    # the same guard one key over: a differently-versioned Easel's meta, in place.
    from test_notices import _rewrite_meta

    _rewrite_meta(path, lambda meta: meta.pop("plan"))
    reopened = Session.load(path)
    assert not reopened.plan().declared
    assert "the checklist asks for some" not in reopened.report()  # nothing painted yet


def test_declaring_a_plan_leaves_the_log_and_the_stream_exactly_where_they_were(tmp_path):
    """Rule 8, which is why the plan lives beside `history.records` and not in it: a
    mark's texture is seeded from its index in the log, so anything new that took one
    would repaint every painting made before it."""
    def build(declare):
        s = make(tmp_path)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            if declare:
                s.plan(why="a sentence", values={span("A1", "H4"): 0.70,
                                                 span("A5", "H8"): 0.72},
                       bands="subject", ground="buried")
            s.stroke([(0.1, 0.2), (0.9, 0.25)], "bristle", "burnt_umber", size=0.05)
            s.block_in(cell("D5"), "flat", "burnt_umber", size=0.04, direction="axis")
        return s

    plain, declared = build(False), build(True)
    assert declared.plan().declared and not plain.plan().declared
    assert len(plain.history.records) == len(declared.history.records)
    assert np.array_equal(plain.canvas.rgb, declared.canvas.rgb)
    assert plain.rng.bit_generator.state == declared.rng.bit_generator.state


def test_the_plan_can_be_handed_to_compare_unchanged(tmp_path):
    """A plan that has to be retyped to be checked is a plan that drifts, and the drift
    arrives as paint. `s.plan()` hands back what the session holds; `compare()` takes
    it."""
    s = make(tmp_path)
    upper, lower = span("A1", "H4"), span("A5", "H8")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s.plan(values={upper: 0.95, lower: 0.30})
        result = s.compare(s.plan())
    assert {c.label for c in result.cells} == {"A1:H4", "A5:H8"}
    assert result.pairs == []                    # 0.65 apart, so no pair to report
    assert result.path.exists()
    with pytest.raises(ValueError, match="no values in it"):
        make(tmp_path).compare(make(tmp_path).plan())


def test_the_shell_declares_the_same_plan_the_api_does(tmp_path, capsys):
    """`easel plan`, so a painting worked from a shell can say what it is for. Its
    places are names rather than shapes, because a shell has no `blob()`."""
    path = tmp_path / "p.easel"
    make(tmp_path).save(path)
    assert main(["plan", str(path), "--value", "A1:H4=0.70", "--value", "A5:H8=0.74",
                 "--bands", "subject", "--ground", "buried",
                 "--why", "the light arrives from below"]) == 0
    printed = capsys.readouterr().out
    assert 'why: "the light arrives from below"' in printed
    assert "A1:H4 / A5:H8: 0.04 apart, and they meet" in printed

    back = Session.load(path)
    assert back.plan().bands == "subject" and back.plan().ground == "buried"
    assert [p.name for p in back.plan().values] == ["A1:H4", "A5:H8"]
    # And the notice is on the session, saved, rather than only on a console.
    assert [n.code for n in back.notices()] == ["plan-pairs"]

    assert main(["plan", str(path), "--clear"]) == 0
    assert not Session.load(path).plan().declared


def test_a_new_session_is_given_the_prelude_that_holds_the_call(tmp_path):
    """The decision taken on a painter who never declares a plan was *say it where it
    costs*: no message at the first stroke, no nag. So the one place the call is put in
    front of a painter is the file they are about to edit anyway -- a worked example is
    an instruction, and this is the instruction that has somewhere to be."""
    path = tmp_path / "p.easel"
    assert main(["new", str(path), "--size", "320x240"]) == 0
    prelude = tmp_path / "prelude.py"
    assert prelude.exists()
    body = prelude.read_text(encoding="utf-8")
    assert "s.plan(" in body and "subject_share" in body
    # Commented out: a plan filled in with somebody else's numbers is worse than none.
    assert all(line.startswith("#") or not line.strip()
               for line in body.split('"""')[-1].strip().split("\n"))

    # A painter's own prelude is never overwritten -- their mixtures live in it.
    prelude.write_text("# mine\n", encoding="utf-8")
    assert main(["new", str(path), "--size", "320x240", "--force"]) == 0
    assert prelude.read_text(encoding="utf-8") == "# mine\n"


# -- D1: the checks that came out of the 0.5.0 cohort's round --------------------------
def test_a_chisel_nearly_along_a_straight_side_says_it_will_stair(tmp_path):
    """Finding 1 of the cohort, and the commonest way a mass comes back wrong: a chisel
    filling a shape along a straight side it runs *nearly* along ends its passes down
    that side in ledges instead of drawing it. `CALIBRATION.md` measures the band --
    22% of its strong edges horizontal against 1% for a comb -- and `RECIPES.md`
    demonstrated it, which is how Kimi's rock faces came to be that call character for
    character.

    The threshold is the mechanism: a pass end lands every `step x cot(theta)` along
    the side, so it is *nearest parallel* that a chisel steps worst. The window of
    angles the plan proposed measured how irregular a shape was instead, and was
    silent on this very band."""
    band = polygon([(0.470, 0.180), (0.530, 0.180), (0.562, 0.820), (0.502, 0.820)])
    lay = dict(color="titanium_white", size=0.020, density=1.0, solid=True,
               pressure="even")

    s = make(tmp_path)
    with pytest.warns(UserWarning, match="come back as a staircase"):
        s.block_in(band, "flat", direction="vertical", **lay)
    said = [n for n in s.notices() if n.code == "chisel-staircase"]
    assert len(said) == 1 and "brush widths from one end to the next" in said[0].text

    # Every remedy it names at one size or another, and it must be silent on each: the
    # passes laid along the side's own two points, the clean edge it names under the
    # comb's floor, and the comb whose ends are bristles rather than a line.
    for label, call in (("along the side", dict(brush="flat",
                                                direction=[(0.470, 0.180), (0.502, 0.820)])),
                        ("a clean edge", dict(brush="flat", direction="vertical",
                                              edge="clean")),
                        ("a comb", dict(brush="bristle", direction="vertical"))):
        quiet = make(tmp_path)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            quiet.block_in(band, **{**lay, **call})
        assert not [n for n in quiet.notices() if n.code == "chisel-staircase"], label


def test_the_staircase_offers_a_comb_only_where_a_comb_is_a_brush(tmp_path):
    """Step 6 of the 0.6.0 round took this notice's second remedy for *a mass built of
    planes*, whose faces are `0.014`-`0.02` -- and the recipe then painted the woven
    surface its own *Goes wrong as* names, because under `0.025` a bristle is four
    streaks with gaps and `report()` says so. A remedy that trips the next rule at the
    size it was offered at is `LESSONS.md` rule 2 twice over. So under the floor the
    notice offers the clean edge beside `direction=`, and the comb only above it."""
    band = polygon([(0.470, 0.180), (0.530, 0.180), (0.562, 0.820), (0.502, 0.820)])
    said = {}
    for size in (0.020, 0.030):
        s = make(tmp_path)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            s.block_in(band, "flat", "titanium_white", size=size, density=1.0,
                       solid=True, pressure="even", direction="vertical")
        text, = [n.text for n in s.notices() if n.code == "chisel-staircase"]
        said[size] = text
    assert "edge='clean'" in said[0.020] and "lay it with a comb" not in said[0.020]
    assert "lay it with a comb" in said[0.030] and "edge='clean'" not in said[0.030]


def test_the_staircase_is_silent_on_a_curve_and_on_a_square_end(tmp_path):
    """`LESSONS.md` rule 2, as the cases that nearly got it wrong. A blob and an ellipse
    have no straight side to align to, so a rule that fires on them is naming a remedy
    that does not exist -- and the plan's own prototype fired on both. A rectangle swept
    square to its sides puts every pass end on one line, which is the thing a chisel is
    *for*."""
    quiet = make(tmp_path)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        quiet.block_in(blob(span("C3", "F6"), wobble=0.3, seed=2), "flat", "white",
                       size=0.06, density=1.0, solid=True)
        quiet.block_in(ellipse(span("B2", "G5")), "flat", "white", size=0.04,
                       direction="horizontal", density=1.0, solid=True)
        quiet.block_in(span("A5", "H8"), "flat", "white", size=0.06,
                       direction="horizontal", density=1.0, solid=True)
    assert not [n for n in quiet.notices() if n.code == "chisel-staircase"]


def _spilled(session) -> list:
    return [n for n in session.notices() if n.code == "spill"]


def test_a_band_crossed_at_an_angle_says_how_far_it_lands_outside(tmp_path):
    """Finding 8 and B17: a water scumble covered part of the sky. A banded scumble picks
    its brush from the step between passes, and the step from the band's extent across
    them -- which, crossed at an angle, is most of the band's length. So at 30 degrees
    the band `0.10-0.90 x 0.40-0.60` covers about three times itself, and nothing said
    so: the ends check fires at 60 degrees, where every pass is a dab, and not here.

    The multiple is predicted off the passes the call is about to lay, and the remedy
    it names first keeps both the angle and the gradient: the same passes, held."""
    band = Region(0.10, 0.40, 0.90, 0.60)
    s = make(tmp_path)
    with pytest.warns(UserWarning, match="the paint outside it"):
        s.scumble(band, "burnt_umber", "titanium_white", 8, direction=30)
    said = _spilled(s)
    assert len(said) == 1
    text = said[0].text
    # 2.95x measured on 1024x768; the prediction is off by under 2% on a band.
    assert re.search(r"lays about (2\.[89]|3\.[01])x the band", text), text
    assert "picked from that step" in text
    assert 'edge="hard"' in text and 'direction="axis"' in text

    # Silent along the band's own axis, where the same band covers 1.49x itself; silent
    # held to the band, which is the remedy; and silent at 60 degrees, where the ends
    # check has already said the paint blooms past the band -- one notice per bloom.
    for label, kw in (("along its axis", {"direction": "axis"}),
                      ("held to the band", {"direction": 30, "edge": "hard"})):
        quiet = make(tmp_path)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            quiet.scumble(band, "burnt_umber", "titanium_white", 8, **kw)
        assert not _spilled(quiet), label
    steep = make(tmp_path)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        steep.scumble(band, "burnt_umber", "titanium_white", 8, direction=60)
    assert {n.code for n in steep.notices()} >= {"scumble-dabs"}
    assert not _spilled(steep)


def test_a_planned_band_is_told_about_its_spill_when_it_is_priced(tmp_path):
    """`cost()` walks the same passes, so the quote says what the call will: a plan is
    where a painter decides the angle, and the one place it is free to change it."""
    band = Region(0.10, 0.40, 0.90, 0.60)
    entry = {"band": band, "color_a": "burnt_umber", "color_b": "titanium_white",
             "n": 8, "direction": 30}
    s = make(tmp_path)
    with pytest.warns(UserWarning, match="lays about"):
        s.cost([entry])
    assert _spilled(s)
    held = make(tmp_path)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        held.cost([{**entry, "edge": "hard"}])
    assert not _spilled(held)


def test_a_brush_too_big_for_its_mass_says_it_will_paint_the_neighbours(tmp_path):
    """The most expensive first mistake with shapes on record -- a rehearsal lost 72
    strokes and its only `undo` to it: a pass stops where its centre meets the outline
    and the brush hangs half its width past it, so a brush that is a large part of the
    mass lays the mass and a rim round it. The three answers `PAINTING.md` gives are
    each silent, at the numbers it gives them."""
    mass = blob(span("D4", "F6"), 0.22, wobble=0.3, seed=2)
    s = make(tmp_path)
    with pytest.warns(UserWarning, match="lays about"):
        s.block_in(mass, "flat", "burnt_umber", size=0.18)
    said = _spilled(s)
    assert len(said) == 1
    assert "of the place's shorter side" in said[0].text
    assert "place.inset(0.09)" in said[0].text

    for label, call in (
        ("inset by half the brush", lambda q: q.block_in(mass.inset(0.045), "flat",
                                                         "burnt_umber", size=0.09)),
        ("a smaller brush", lambda q: q.block_in(mass, "flat", "burnt_umber", size=0.06)),
        ("a clean edge", lambda q: q.block_in(mass, "flat", "burnt_umber", size=0.06,
                                              edge="clean")),
        ("held to the outline", lambda q: q.block_in(mass, "flat", "burnt_umber",
                                                     size=0.18, edge="hard")),
    ):
        quiet = make(tmp_path)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            call(quiet)
        assert not _spilled(quiet), label


def test_spill_is_silent_where_the_overrun_is_the_point_or_the_rule_of_thumb_is_wrong(
        tmp_path):
    """`LESSONS.md` rule 2, as the cases that would have got it wrong. `cover()` laid
    ragged runs its ends outside the area on purpose -- the recipe before 0.6.0 moved its
    default to `"hard"` -- and paints about three times its cell. `PAINTER.md`'s first
    `block_in` lays a brush 60% of its shape -- the plan's
    *a fifth of the shorter extent* would fire on it -- and lands 1.48x, because the
    multiple is what paints the neighbours and not the fraction. And under twelve
    pixels a brush does not land where its outline says: on the bench the reach was
    fitted on, a 7 px flat on a thin strip predicted at 1.68x came back at 0.65x."""
    quiet = make(tmp_path)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        quiet.cover(cell("D5"), "burnt_umber", edge="ragged")
        far = blob(span("B2", "G4"), wobble=0.3, seed=1)
        quiet.block_in(far, "bristle", "burnt_umber", density=0.8, size=0.18,
                       direction="axis")
        quiet.block_in(Region(0.05, 0.70, 0.95, 0.76), "flat", "burnt_umber",
                       size=0.02, direction="axis")
    assert not _spilled(quiet)


# -- D2: the checks that read the canvas under the mark --------------------------------
def _joined(tmp_path, width=512, height=384):
    """Two masses meeting on a line across the middle, a hard step from 0.20 to 0.78.

    Both held to their own edge, so the boundary is a step and not a half-brush of
    overlap, and dried, so what a test lays on it sits on it.
    """
    s = Session(width, height, texture="linen", ground="toned_grey", seed=7,
                out_dir=tmp_path, timelapse=False)
    p = s.palette
    p["dark"] = p.at_value(p.mix("ultramarine", "burnt_umber", 0.5), 0.20)
    p["light"] = p.at_value(p.mix("yellow_ochre", "titanium_white", 0.5), 0.78)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for place, colour in ((Region(0.0, 0.0, 1.0, 0.5), "dark"),
                              (Region(0.0, 0.5, 1.0, 1.0), "light")):
            s.block_in(place, "flat", colour, size=0.06, solid=True, opacity=1.0,
                       pressure="even", direction="horizontal", edge="hard")
    s.dry()
    return s


def _told(session, code: str) -> list:
    return [n for n in session.notices() if n.code == code]


def test_a_smudge_carries_only_what_it_has_picked_up(tmp_path):
    """Half of finding 3's thumbprint was the engine's. A smudge started loaded with
    titanium white and mixed 45% of the canvas into it per dab, so its first dabs laid
    55%, 30%, 17% white: a light cap at the start of every smudge, on a passage of one
    colour as much as across a boundary. Over a mass at 0.45 it lifted the first brush
    of the path by 0.13, and a painter who ran one down a dark pile got a light spot in
    the middle of it. It now changes nothing there.

    And the thumbprint `CALIBRATION.md` measured across a join -- the light carried 4.1
    brushes into the dark, *the length of its own path* -- was that cap, laid from the
    first dab onward by a pass that started in the dark. The same pass now carries the
    light half a brush in, which is what one run along the join does."""
    s = make(tmp_path)
    s.palette["mid"] = s.palette.at_value("burnt_sienna", 0.45)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s.block_in(Region(0.0, 0.0, 1.0, 1.0), "flat", "mid", size=0.08, solid=True,
                   pressure="even", direction="horizontal")
    s.dry()
    before = s.canvas.values(sketch=False).astype(np.float32) / 255.0
    s.smudge([(0.3, 0.5), (0.7, 0.5)])
    after = s.canvas.values(sketch=False).astype(np.float32) / 255.0
    assert float(np.abs(after - before).max()) < 0.03

    joined = _joined(tmp_path)
    before = joined.canvas.values(sketch=False).astype(np.float32) / 255.0
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        joined.smudge([(0.5, 0.30), (0.5, 0.70)], size=0.04)
    after = joined.canvas.values(sketch=False).astype(np.float32) / 255.0
    join = joined.canvas.height // 2
    lifted = np.nonzero(((after - before)[:join] > 0.05).any(axis=1))[0]
    deepest = (join - int(lifted.min())) / (0.04 * joined.canvas.long_side)
    assert deepest < 1.0, f"light carried {deepest:.1f} brushes into the dark"


def test_a_smudge_dragged_across_a_boundary_says_so(tmp_path):
    """The other half of finding 3, and the painter's: *run it along a boundary, never
    across one* was `PAINTER.md`'s second rule about `smudge`, and the thumbprints kept
    coming. Dragged across a boundary a smudge carries the first mass about a brush
    into the second -- 1.2 brushes at `size=0.04` on this step, either way round.

    Read off the canvas before the smudge lands, along the path it will be stamped
    down: a step of 0.10 or more, more of it along the path than across it, with half
    a brush of path either side. Silent along the join, inside one mass, and on a path
    that only starts or stops on the line -- which carries nothing across it."""
    for label, path in (("dark into light", [(0.5, 0.35), (0.5, 0.65)]),
                        ("light into dark", [(0.5, 0.65), (0.5, 0.35)])):
        s = _joined(tmp_path)
        with pytest.warns(UserWarning, match="crosses a boundary"):
            s.smudge(path)
        said = _told(s, "smudge-across")
        assert len(said) == 1 and "thumbprint" in said[0].text, label
        step = float(re.search(r"the value steps ([0-9.]+) along", said[0].text).group(1))
        assert step > 0.40, label
        # The line is placed where the path passes it, whichever way the step falls.
        line = float(re.search(r", ([0-9.]+) from where it starts", said[0].text).group(1))
        assert abs(line - 0.15 * 384 / 512) < 0.01, (label, line)

    for label, path in (("along the join", [(0.46, 0.50), (0.54, 0.50)]),
                        ("inside one mass", [(0.30, 0.20), (0.70, 0.20)]),
                        ("stopping on the line", [(0.50, 0.30), (0.50, 0.505)]),
                        ("starting on the line", [(0.50, 0.495), (0.50, 0.70)]),
                        ("stopping on it from the light", [(0.50, 0.70), (0.50, 0.495)]),
                        ("starting on it into the dark", [(0.50, 0.505), (0.50, 0.30)])):
        quiet = _joined(tmp_path)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            quiet.smudge(path)
        assert not _told(quiet, "smudge-across"), label


def test_a_long_smudge_along_a_boundary_says_it_leaves_a_band(tmp_path):
    """One pass along a hard step leaves a strip about a brush tall at the value halfway
    between the two masses, the same at 0.05 long as at 0.80: a softened corner over a
    short stretch, and over a long one *dark, mid, light* -- two edges where there was
    one. `RECIPES.md` said so in a paragraph, and its own block above the paragraph ran
    a smudge half the canvas long. A habit rather than a fact, because a painter can
    want the band; silent on the short stretch and on a long pass inside one mass."""
    s = _joined(tmp_path)
    with pytest.warns(UserWarning, match="reads as a third band"):
        s.smudge([(0.20, 0.50), (0.60, 0.50)])
    said = _told(s, "smudge-long")
    assert len(said) == 1 and "two edges where there was one" in said[0].text
    run = float(re.search(r"runs ([0-9.]+) of the canvas", said[0].text).group(1))
    assert 0.35 <= run <= 0.42
    assert not _told(s, "smudge-across"), "along a boundary is not across it"

    for label, path in (("a short stretch", [(0.46, 0.50), (0.54, 0.50)]),
                        ("long, inside one mass", [(0.10, 0.25), (0.90, 0.25)])):
        quiet = _joined(tmp_path)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            quiet.smudge(path)
        assert not _told(quiet, "smudge-long"), label


def _under_a_film(tmp_path):
    """The guide's own glaze table: a warm light film over a solid cool dark mass."""
    s = make(tmp_path)
    p = s.palette
    p["under"] = p.at_value(p.mix("ultramarine", "burnt_umber", 0.5), 0.30)
    p["film"] = p.at_value(p.mix("cadmium_yellow", "titanium_white", 0.4), 0.62)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s.block_in(Region(0.0, 0.0, 1.0, 1.0), "flat", "under", size=0.10, solid=True,
                   opacity=1.0, pressure="even", direction="horizontal")
    s.dry()
    return s


FILM = dict(brush="flat", size=0.18, pressure="even")


def test_a_film_far_from_what_it_lands_on_says_what_it_did(tmp_path):
    """Finding 4: *green blooms over blue water, a searchlight on a flat sheet*. A glaze
    is strong in proportion to its distance from what it lands on, in hue as well as
    in value, and the guide had a table for it and no instrument. Measured once the
    film has landed, over its own footprint.

    Two ways past what a film is for. The guide's own table: a warm light film over a
    cool dark at 0.14 moves the value 0.085 -- *a stripe of a different colour*, a new
    mass. At 0.05 it moves the value 0.03 and is still the same film, mixed far from
    what it lands on in hue -- *already neutral, the cool gone and nothing warm
    arrived* -- which no opacity rescues, because a lower opacity is the same colour,
    fainter. And `to_value=` does not rescue it either: the search finds a value, and
    the colour it lands at is still the film's."""
    s = _under_a_film(tmp_path)
    with pytest.warns(UserWarning, match="stops shifting a mass"):
        s.glaze([(0.2, 0.5), (0.8, 0.5)], "film", opacity=0.14, **FILM)
    said = _told(s, "glaze-far")
    assert len(said) == 1 and "to_value=" in said[0].text

    s = _under_a_film(tmp_path)
    with pytest.warns(UserWarning, match="from what it lands on in hue and chroma"):
        s.glaze([(0.2, 0.5), (0.8, 0.5)], "film", opacity=0.05, **FILM)
    text = _told(s, "glaze-far")[0].text
    assert "the same colour, fainter" in text
    assert float(re.search(r"was mixed ([0-9.]+) from", text).group(1)) >= 0.07

    s = _under_a_film(tmp_path)
    with pytest.warns(UserWarning, match="from what it lands on in hue and chroma"):
        s.glaze([(0.2, 0.5), (0.8, 0.5)], "film", to_value=0.36, **FILM)

    # Laid as a stroke with glaze=True, the same film is the same film.
    s = _under_a_film(tmp_path)
    with pytest.warns(UserWarning, match="stops shifting a mass"):
        s.stroke([(0.2, 0.5), (0.8, 0.5)], color="film", glaze=True, opacity=0.14, **FILM)


def test_a_session_loaded_from_its_file_lays_and_measures_a_film(tmp_path):
    """`easel run` paints from a file, and `Session.load` builds the session by hand
    rather than through `__init__`: a flag set in one and not the other is an
    AttributeError on the first film of every pass painted from the shell. Both ways of
    laying a film, on a session that came back from disk."""
    path = tmp_path / "p.easel"
    _under_a_film(tmp_path).save(path)
    s = Session.load(path)
    with pytest.warns(UserWarning, match="stops shifting a mass"):
        s.glaze([(0.2, 0.5), (0.8, 0.5)], "film", opacity=0.14, **FILM)
    s = Session.load(path)
    with pytest.warns(UserWarning, match="stops shifting a mass"):
        s.stroke([(0.2, 0.5), (0.8, 0.5)], color="film", glaze=True, opacity=0.14, **FILM)


def test_a_film_mixed_close_or_aimed_at_a_value_is_left_alone(tmp_path):
    """`LESSONS.md` rule 2, as the two cases the guide itself recommends. A film mixed
    close to what it lands on -- the lit-air recipe's own mixture, a step above the
    field and leaning to its colour -- is silent. And a film of the field's own hue
    given `to_value=` a long way from it asked for its shift, so moving the value past
    0.08 is what it was for: silent too, and so are the dozen search films the solver
    lays on copies to find its opacity."""
    s = _under_a_film(tmp_path)
    p = s.palette
    field = s.sample(Region(0.3, 0.3, 0.7, 0.7))
    level = p.value_of(field)
    p["close"] = p.at_value(p.mix(field, "titanium_white", 0.5), level + 0.06)
    p["lift"] = p.at_value(p.mix(field, "titanium_white", 0.5), level + 0.35)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        s.glaze([(0.2, 0.5), (0.8, 0.5)], "close", opacity=0.09, **FILM)
        s.glaze([(0.2, 0.5), (0.8, 0.5)], "lift", to_value=level + 0.12, **FILM)
    assert not _told(s, "glaze-far")
    assert not [w for w in caught if "this film" in str(w.message)]



# -- D3: the checks after the pass, off the log and the canvas it opened on -------------
def _dark_field(tmp_path):
    """A dark solid field to lay light marks on, dried."""
    s = Session(512, 384, texture="linen", ground="toned_grey", seed=7,
                out_dir=tmp_path, timelapse=False)
    p = s.palette
    p["dark"] = p.at_value(p.mix("ultramarine", "burnt_umber", 0.5), 0.25)
    p["light"] = p.at_value(p.mix("yellow_ochre", "titanium_white", 0.5), 0.80)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s.block_in(Region(0.0, 0.0, 1.0, 1.0), "flat", "dark", size=0.08, solid=True,
                   pressure="even", direction="horizontal")
    s.dry()
    return s


def _rays(s, centre, angles, length, brush="round_soft", size=0.012, rim=0.0):
    """Marks leaving one point, as a loop over angles lays them."""
    cx, cy = centre
    aspect = s.canvas.width / s.canvas.height
    for a in angles:
        dx, dy = math.cos(math.radians(a)), math.sin(math.radians(a))
        s.stroke([(cx + dx * rim, cy + dy * rim * aspect),
                  (cx + dx * length, cy + dy * length * aspect)], brush, "light", size=size)


def _pass_says(s, before, words) -> bool:
    return any(words in line for line in s.report(since=before).splitlines())


def test_marks_leaving_one_point_every_way_are_a_daisy(tmp_path):
    """Finding 6: *strokes radiating from one point -- a wagon wheel*. `PAINTER.md`,
    `RECIPES.md` and `scumble`'s own docstring all said it, and a painter drew one
    anyway: the fogged glass's tree, whose own verdict calls it *a grey mass with
    spoke-like branches*, is the one pass of the corpus this finds. A glow laid as
    petals and a sun given rays by a loop both leave their point in every direction --
    no gap in the circle wider than 90 degrees."""
    for label, lay in (
        ("a daisy of petals", lambda s: _rays(s, (0.5, 0.5), range(0, 360, 45), 0.10,
                                              rim=0.01)),
        ("a sun's rays, from its rim", lambda s: _rays(s, (0.5, 0.5), range(0, 360, 30),
                                                       0.18, size=0.02, rim=0.04)),
    ):
        s = _dark_field(tmp_path)
        before = len(s.history.records)
        lay(s)
        assert _pass_says(s, before, "a daisy"), label


def test_a_tree_grass_a_fan_of_rays_and_a_glow_are_not_a_daisy(tmp_path):
    """`LESSONS.md` rule 2, as four things that leave a point on purpose. The prototype
    this replaced gathered marks that merely lay near one another and fired on 22
    passes of the corpus, one of them a daisy: the rest were pine branches, pot rims, a
    greenhouse's perspective bars, fingers, and a fan of sun rays. A tree's branches
    and trunk leave the fork with gaps of 120 degrees, a tuft of grass and a fan of
    rays one of nearly 300. A glow of films as wide as they are long leaves its point
    every way, and is not petals: the heron's lamp was one film short of being told so."""
    for label, lay in (
        ("a tree", lambda s: (s.stroke([(0.5, 0.9), (0.5, 0.5)], "bristle", "light",
                                       size=0.02),
                              _rays(s, (0.5, 0.55), (-150, -120, -90, -60, -30), 0.12,
                                    brush="liner", size=0.006))),
        ("a tuft of grass", lambda s: _rays(s, (0.5, 0.8),
                                            (-125, -110, -100, -90, -80, -70, -55), 0.10,
                                            brush="liner", size=0.004)),
        ("a fan of rays", lambda s: _rays(s, (0.8, 0.1), (100, 115, 130, 145, 160), 0.35,
                                          size=0.03)),
        ("a glow of wide films", lambda s: _glow_of_films(s, (0.5, 0.5), range(0, 360, 45),
                                                          0.08)),
    ):
        s = _dark_field(tmp_path)
        before = len(s.history.records)
        lay(s)
        assert not _pass_says(s, before, "a daisy"), label


def _glow_of_films(s, centre, angles, length):
    """Films as wide as they are long leaving one point: a glow, not petals."""
    cx, cy = centre
    aspect = s.canvas.width / s.canvas.height
    p = s.palette
    p["glow"] = p.at_value(p.mix("dark", "light", 0.2), 0.34)     # mixed from its field
    for a in angles:
        dx, dy = math.cos(math.radians(a)), math.sin(math.radians(a))
        s.glaze([(cx, cy), (cx + dx * length, cy + dy * length * aspect)], "glow",
                opacity=0.12, size=length)


def test_one_length_and_one_spacing_is_a_loops_signature(tmp_path):
    """Finding 7: a reflection laid as a column of same-length marks -- *floating
    rectangles, small bricks, a ziggurat, spoon-shaped islands* -- four of the seven
    cohort painters' first take, and not one recipe for it. A loop leaves one length
    (or a strict ramp of them) at one spacing: no clumps and no holes."""
    for label, rows in (
        ("a column", [(0.55 + i * 0.04, 0.05) for i in range(8)]),
        ("a ziggurat", [(0.50 + i * 0.05, 0.20 - i * 0.025) for i in range(7)]),
    ):
        s = _dark_field(tmp_path)
        before = len(s.history.records)
        for y, half in rows:
            s.stroke([(0.5 - half, y), (0.5 + half, y)], "flat", "light", size=0.012,
                     pressure="even")
        assert _pass_says(s, before, "a loop's signature"), label


def test_a_row_placed_by_hand_or_laid_as_one_passage_is_not_a_loop(tmp_path):
    """The accepted versions: lengths and gaps varied by hand. And a graded pool laid as
    nine overlapping passes -- one of the corpus's -- is a passage and not a row: its
    marks sit closer than their own width, so no one of them reads."""
    rows = [(0.55, 0.07, 0.0), (0.58, 0.04, 0.01), (0.64, 0.09, -0.02), (0.66, 0.03, 0.02),
            (0.73, 0.06, 0.0), (0.81, 0.02, -0.01), (0.83, 0.05, 0.015)]
    s = _dark_field(tmp_path)
    before = len(s.history.records)
    for y, half, dx in rows:
        s.stroke([(0.5 - half + dx, y), (0.5 + half + dx, y + 0.004)], "flat", "light",
                 size=0.012, pressure="even")
    assert not _pass_says(s, before, "a loop's signature"), "by hand"

    s = _dark_field(tmp_path)
    before = len(s.history.records)
    for i in range(9):
        t = i / 8.0
        half, y = 0.2 + 0.1 * t, 0.6 + 0.2 * t
        s.stroke([(0.5 - half, y), (0.5 + half, y)], "flat", "light", size=0.11,
                 opacity=0.5, pressure="even")
    assert not _pass_says(s, before, "a loop's signature"), "one passage"


def _details(s):
    """Five small light marks on the dark field -- the near things a late layer buries."""
    for i in range(5):
        x = 0.25 + i * 0.12
        s.stroke([(x, 0.45), (x + 0.04, 0.47)], "round_hard", "light", size=0.008)
    s.dry()


def test_a_film_or_a_mass_laid_over_details_says_it_buried_them(tmp_path):
    """Finding 9, and the depth-order paragraph `LESSONS.md` lists as failed three runs
    running: *a late pass buries what stands in front of it*. The pass is told when a
    film or the passes of a mass take details that were showing as it opened out of
    sight -- read off the canvas as the pass began, which `_open_pass` keeps."""
    for label, layer in (
        ("a film", lambda s: s.glaze([(0.05, 0.46), (0.95, 0.46)], "dark", opacity=0.9,
                                     size=0.12)),
        ("a mass", lambda s: s.block_in(Region(0.05, 0.40, 0.95, 0.52), "flat", "dark",
                                        size=0.06, solid=True, pressure="even",
                                        direction="horizontal")),
    ):
        s = _dark_field(tmp_path)
        _details(s)
        before = s._open_pass()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            layer(s)
        said = [line for line in s.report(since=before).splitlines() if "out of sight" in line]
        assert said and "took 5 earlier details" in said[0], label


def test_what_is_painted_in_front_or_leaves_them_showing_is_not_a_burial(tmp_path):
    """`LESSONS.md` rule 2. The prototype counted every earlier detail under changed
    pixels and fired on 54 passes of the corpus, most of them a nearer thing painted over
    a farther thing's details -- back-to-front done right. A hand-laid stroke over them is
    that; a film that only tints them leaves them showing; and without the canvas as the
    pass opened there is nothing to say."""
    for label, layer in (
        ("a nearer thing, laid by hand", lambda s: s.stroke([(0.05, 0.46), (0.95, 0.46)],
                                                            "flat", "dark", size=0.1,
                                                            pressure="even")),
        ("a film that only tints them", lambda s: s.glaze([(0.05, 0.46), (0.95, 0.46)],
                                                          "dark", opacity=0.08,
                                                          size=0.12)),
    ):
        s = _dark_field(tmp_path)
        _details(s)
        before = s._open_pass()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            layer(s)
        assert not _pass_says(s, before, "out of sight"), label

    unopened = _dark_field(tmp_path)
    _details(unopened)
    before = len(unopened.history.records)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        unopened.glaze([(0.05, 0.46), (0.95, 0.46)], "dark", opacity=0.9, size=0.12)
    assert not _pass_says(unopened, before, "out of sight"), "no canvas to compare"


def test_the_canvas_a_pass_opened_on_comes_from_run_and_from_the_last_report(tmp_path,
                                                                            capsys):
    """`easel run` keeps the canvas as the pass begins, where it already takes the log
    index; a painter who calls `report()` after each pass in one script is given it by
    the report before."""
    s = _dark_field(tmp_path)
    _details(s)
    s.report()                                    # the pass before, checked
    before = len(s.history.records)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s.glaze([(0.05, 0.46), (0.95, 0.46)], "dark", opacity=0.9, size=0.12)
    assert _pass_says(s, before, "out of sight"), "from the report before"

    path = tmp_path / "p.easel"
    s = _dark_field(tmp_path)
    _details(s)
    s.save(path)
    script = tmp_path / "pass.py"
    script.write_text('s.glaze([(0.05, 0.46), (0.95, 0.46)], "dark", opacity=0.9, '
                      'size=0.12)\n', encoding="utf-8")
    assert main(["run", str(path), str(script)]) == 0
    assert "out of sight" in capsys.readouterr().out


# -- E: the standing measurement lines, and G4: the checklist --------------------------
#
# Every one of these answers a line of `PAINTER.md`'s closing checklist that a painter
# used to answer by looking. The thresholds are `CALIBRATION.md`'s, measured on the 21
# finished paintings of the corpus; the tests below are the two cases each line has to
# get right -- it fires with the exact words on the fault, and is silent on the
# neighbouring right thing.

def _values(session):
    """The canvas the measurement lines read: values, 0..1, graphite left out."""
    return session.canvas.values(sketch=False).astype(np.float32) / 255.0


def test_the_values_line_names_which_end_the_picture_is_missing(tmp_path):
    """Finding 12, and the pier's own verdict: *no clear light*. A picture can have
    three well-separated clusters and still have nothing light in it, because all
    three sit in the bottom third of what the box can reach -- so the range is asked
    against the palette before the clusters are asked against each other.

    The prototype printed the closest pair and nothing else, which says neither which
    end is missing nor that one is."""
    from easel.checklist import values_line

    reach = (0.13, 0.96)
    dark = np.full((200, 200), 0.24, dtype=np.float32)
    dark[:60] = 0.17
    dark[60:120] = 0.31
    assert "no clear light" in values_line(dark, reach=reach)
    assert "nothing above" in values_line(dark, reach=reach)

    light = np.full((200, 200), 0.93, dtype=np.float32)
    assert "no clear dark" in values_line(light, reach=reach)

    # The right thing, and the line has to be silent on it: three masses a clear step
    # apart, spanning the box. `LESSONS.md` rule 2 -- a picture that did the thing the
    # checklist asks for must not be told it did not.
    good = np.concatenate([np.full((66, 200), 0.20, dtype=np.float32),
                           np.full((67, 200), 0.52, dtype=np.float32),
                           np.full((67, 200), 0.88, dtype=np.float32)])
    said = values_line(good, reach=reach)
    assert "a clear light, mid and dark" in said
    assert "no clear" not in said


def test_the_values_line_says_when_two_masses_read_as_one(tmp_path):
    """The fogged glass: its two largest areas came in `0.008` apart, which is under
    the `0.10` that separates two masses, so the picture has two values and not three.
    The line says which pair and quotes the threshold, because a painter whose subject
    really is a fog bank should be able to read it and disagree."""
    from easel.checklist import values_line

    # A clear dark, and two lights that are the same light twice. The two close
    # masses carry most of the picture, which is what makes the clusterer split them
    # and is the fogged glass's own shape: its *two largest areas* were the pair.
    view = np.concatenate([np.full((50, 200), 0.22, dtype=np.float32),
                           np.full((75, 200), 0.80, dtype=np.float32),
                           np.full((75, 200), 0.81, dtype=np.float32)])
    said = values_line(view, reach=(0.13, 0.96))
    assert "top two clusters" in said and "read as one mass" in said
    assert "0.10" in said


def test_the_edges_line_divides_the_picture_between_hard_and_soft(tmp_path):
    """Finding 13: `report()` said *nothing to report* over a picture whose every
    boundary was crisp, and GPT's own verdict on it names *equally crisp boundaries*.
    Nothing in the log can see it -- an edge is what two neighbouring masses do to
    each other, not either one's arguments -- so this is measured off the canvas.

    **The prototype measured the wrong pixels.** Taking the top percentile of the
    gradient samples the sharpest pixels of whatever picture it is handed, so every
    canvas came back between 1.5 and 2.1 px and the `2.0` threshold was a coin flip:
    it called a hard-edged mass 41% hard and a ragged comb 84%, which is the wrong
    way round. The ridge-and-step selection here separates the one passage of the
    four below that a painter would call soft, which is what the line is for."""
    from easel.checklist import edges_line

    shape = polygon([(0.15, 0.15), (0.85, 0.20), (0.80, 0.80), (0.10, 0.75)])
    laid = {}
    for name, call in (("hard", dict(brush="flat", size=0.05, density=1.0,
                                     solid=True, edge="hard", pressure="even")),
                       ("soft", dict(brush="round_soft", size=0.09, density=0.6))):
        s = make(tmp_path)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            s.block_in(shape, color="titanium_white", **call)
        said = edges_line(s.canvas.values(sketch=False).astype(np.float32) / 255.0)
        laid[name] = (float(re.search(r"(\d+)%", said).group(1)),
                      float(re.search(r"median ([\d.]+) px", said).group(1)))
    assert laid["hard"][0] > laid["soft"][0], laid
    assert laid["soft"][0] == 0.0, laid
    assert laid["soft"][1] > laid["hard"][1], laid

    # A canvas with nothing on it has no boundary between two masses to measure, and
    # says so rather than reporting the tooth's own gradients as edges.
    assert edges_line(np.full((60, 60), 0.4, dtype=np.float32)) ==         "edges: nothing with an edge yet"


def test_the_pencil_line_counts_graphite_and_not_paint(tmp_path):
    """The checklist's own question, and the one line here whose right answer is not
    zero: a drawing showing through thin paint is a good thing and worth keeping. So
    this is a number and not a warning -- and it has to fall when the paint goes over
    the drawing."""
    s = make(tmp_path)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s.pencil([(0.10, 0.30), (0.90, 0.32)])
        drawn = float(re.search(r"([\d.]+)%", s._canvas_lines()[-1]).group(1))
        s.block_in(span("A1", "H8"), "flat", "titanium_white", size=0.08,
                   density=1.0, solid=True, pressure="even")
    assert drawn > 0.0
    # Buried under a solid white field: the graphite is still on the canvas and is no
    # longer showing, which is what the line measures and what a painter sees.
    lines = [one for one in s._canvas_lines() if one.startswith("pencil:")]
    assert lines and float(re.search(r"([\d.]+)%", lines[0]).group(1)) < drawn


def test_a_solid_mass_says_what_came_back_bare_where_it_would_read(tmp_path):
    """Finding 2, and B2's correction to it. `solid-comb` predicts the holes from the
    brush and the density; this measures the canvas once the paint is on it, which is
    the only way to answer for the shape, the ground and the overlap.

    **A hole is a contrast, not a gap** -- `CALIBRATION.md`'s own words. The same comb
    over the same shape leaves `0.16%` bare on `toned_grey` and `3.16%` on a dark
    ground, because *bare* means within `10/255` of the ground and a mass painted near
    its own ground has nothing to show through. The 3.16% is the measurement finding
    paint that barely registered, not a hole anybody can see, so the line is gated on
    the contrast and says the number it measured."""
    shape = polygon([(0.20, 0.20), (0.80, 0.25), (0.75, 0.80), (0.15, 0.75)])
    lay = dict(size=0.04, density=0.8, solid=True)

    s = Session(512, 384, ground="#2e332c", seed=3, out_dir=tmp_path, timelapse=False)
    with pytest.warns(UserWarning, match="came back bare"):
        s.block_in(shape, "bristle", "titanium_white", **lay)
    said = [n for n in s.notices() if n.code == "holes"]
    assert len(said) == 1 and "of value between the two" in said[0].text

    # The same comb, the same shape, the same ground -- and a colour that sits on that
    # ground. The holes are still there and nobody can see them.
    quiet = Session(512, 384, ground="#2e332c", seed=3, out_dir=tmp_path,
                    timelapse=False)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        quiet.block_in(shape, "bristle", "burnt_umber", **lay)
    assert not [n for n in quiet.notices() if n.code == "holes"]

    # And the brush that closes them: a flat leaves nothing bare at any size tried.
    flat = Session(512, 384, ground="#2e332c", seed=3, out_dir=tmp_path,
                   timelapse=False)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        flat.block_in(shape, "flat", "titanium_white", **lay)
    assert not [n for n in flat.notices() if n.code == "holes"]


def test_the_holes_line_measures_what_calibration_measured(tmp_path):
    """The same three numbers `CALIBRATION.md` prints for B2, off the engine's own
    method rather than off the probe's. The point of `ground_showing(where=)` is that
    there is one definition of *bare* and the document and the tool read it from the
    same place; two definitions is how the two drift apart."""
    place = Region(0.10, 0.10, 0.90, 0.90)
    got = {}
    for ground in ("toned_grey", "#2e332c"):
        s = Session(1440, 960, ground=ground, seed=7, out_dir=tmp_path, timelapse=False)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            s.block_in(place, "bristle", "burnt_umber", size=0.04, density=0.8,
                       solid=True, direction=37)
        inner = place.inset(0.04 * 0.8)
        x0, y0, x1, y1 = s.canvas.region_px(inner)
        mask = np.zeros((960, 1440), dtype=bool)
        mask[y0:y1, x0:x1] = True
        got[ground] = s.canvas.ground_showing(where=mask)
    # 0.1552% and 3.1550% in the document, off a different seed.
    assert 0.001 < got["toned_grey"] < 0.003, got
    assert 0.030 < got["#2e332c"] < 0.034, got
    assert got["#2e332c"] > got["toned_grey"] * 15


def test_the_boxes_line_counts_calls_and_not_passes(tmp_path):
    """*Is any mass a rectangle that should have been a shape? Check the background
    hardest.* A mass is many records -- one per pass -- so counting records would
    report one wide band as thirty rectangles. The log separates one call from the
    next by the generator's state at the call's start, which every record of that call
    carries, and that is what the count walks."""
    from easel.checklist import mass_counts

    s = make(tmp_path)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s.block_in(span("A1", "D4"), "flat", "titanium_white", size=0.05)
        s.block_in(span("E1", "H4"), "flat", "burnt_umber", size=0.05)
        s.block_in(polygon([(0.2, 0.5), (0.8, 0.55), (0.7, 0.9)]), "flat",
                   "burnt_umber", size=0.05)
        s.stroke([(0.1, 0.95), (0.4, 0.96)], "liner", "titanium_white", size=0.01)
    assert mass_counts(s.history.records) == (2, 3)
    assert "2 of 3 masses" in s.checklist()
    # The hand-laid mark is not a mass, and two calls in a row are two and not one.
    assert "check the background hardest" in s.checklist()


def test_the_unspent_line_asks_for_the_weakest_passage(tmp_path):
    """Finding 15, and the sharpest number the 0.5.0 cohort produced: five of its six
    budgeted paintings stopped under 45% of budget at a median of 42% spent, and none
    of the thirteen before them did. It is not a property of the engine, so the line
    prints the number and names the job rather than warning."""
    from easel.checklist import unspent_line

    assert "name the weakest passage" in unspent_line(120, 300)
    # Spent down to the last sixth: nothing left to redirect, so nothing is asked.
    assert "name the weakest passage" not in unspent_line(250, 300)
    assert "no budget set" in unspent_line(40, None)


def test_the_checklist_answers_the_measured_lines_and_asks_the_other_three(tmp_path):
    """G4: the closing checklist as output. Every line with a number behind it
    answered, and the three that nothing here can ask printed as questions with the
    painter's own `why` quoted back.

    The boundary is the point. `LESSONS.md` and `report()` both say *the check cannot
    see a composition*: a picture can pass every measured line and have quietly become
    a different picture, competently painted."""
    s = make(tmp_path, budget=300)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s.plan(why="the light coming off the water", subject_share=0.32)
        s.block_in(span("A1", "H4"), "flat", "cerulean", size=0.06)
        s.stroke([(0.3, 0.7), (0.6, 0.72)], "liner", "burnt_umber", size=0.01,
                 note="subject")
    said = s.checklist()
    for line in ("values:", "edges:", "ground:", "boxes:", "unspent:", "subject:"):
        assert line in said, line
    assert "the light coming off the water" in said
    assert "three this cannot answer" in said
    # The three are questions and not measurements, and the budget line is the
    # painting's own rather than a share of the pass.
    assert said.count("?") >= 3
    assert "300 marks spent" in said


def test_the_checklist_says_so_when_nothing_wrote_down_why(tmp_path):
    """The one line no measurement can replace, and the only honest thing to print
    when it was never written: say that it was not, and name the call. A painting with
    no `why` is not given a blank quotation to nod at."""
    s = make(tmp_path, budget=100)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s.block_in(span("A1", "H4"), "flat", "cerulean", size=0.06)
    said = s.checklist()
    assert "did not write down why" in said and "s.plan(why=...)" in said


def test_easel_check_prints_the_checklist_and_changes_nothing(tmp_path, capsys):
    """`easel check` is G4's other half, for a painter working from a shell. Read-only
    on purpose: a checklist asks the painting questions and changes nothing about it,
    so the file is not written back."""
    path = tmp_path / "p.easel"
    s = make(tmp_path, budget=200)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s.plan(why="a pier at low tide")
        s.block_in(span("A1", "H4"), "flat", "cerulean", size=0.06)
    s.save(path)
    before = path.read_bytes()

    assert main(["check", str(path)]) == 0
    said = capsys.readouterr().out
    assert "checklist for this painting" in said
    assert "a pier at low tide" in said
    assert path.read_bytes() == before


def test_the_standing_lines_are_left_off_a_counted_copy(tmp_path):
    """Rule: a counted copy borrowed the canvas and laid no paint on it, so every
    number read off that canvas would be the painting's and not the pass's. The ground
    line has been gated this way since 0.4.0 and the four canvas lines are gated with
    it -- including `holes:`, which would otherwise report every pixel of a counted
    mass as bare."""
    s = make(tmp_path)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s.block_in(span("A1", "H4"), "flat", "cerulean", size=0.06)
        counted = s.scratch(count_only=True)
        counted.block_in(polygon([(0.2, 0.5), (0.8, 0.55), (0.7, 0.9)]), "bristle",
                         "titanium_white", size=0.04, density=0.8, solid=True)
    said = counted.report()
    for line in ("values:", "edges:", "ground:", "pencil:"):
        assert line not in said, line
    assert not [n for n in counted.notices() if n.code == "holes"]


# -- F3: the load a banded scumble is laid at ------------------------------------------
def test_a_banded_scumble_lays_its_passes_solid(tmp_path):
    """The default move of `PLAN-0.6.0.md` workstream F, row 3.

    A ring has no far end to run dry at, so the inward case has defaulted
    ``load_falloff=0.0`` since it was written; a band's passes do have ends, and until
    0.6.0 they were laid on the brush's own load. The verb's own default brush is the
    one preset that does not start full (``bristle``, ``load=0.9,
    load_falloff=0.55``), which is why 40 of the 60 committed banded scumbles in the
    corpus type the pair by hand. Asked of the log rather than of the signature,
    because the pair reaches the passes through ``_resolve_brush`` and a signature
    does not show that.
    """
    s = make(tmp_path)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s.scumble(Region(0.1, 0.4, 0.9, 0.6), "burnt_umber", "titanium_white", 8)
    assert s.history.records, "a scumble lays passes"
    for rec in s.history.records:
        assert rec.params["load"] == 1.0
        assert rec.params["load_falloff"] == 0.0


def test_a_starved_band_is_still_one_keyword_away(tmp_path):
    """A default, not an override -- which is what makes it a default move and not a
    rule. `LESSONS.md`: *a default is worth more than a warning*, and a painter who
    wants a band that runs dry says so and is obeyed."""
    s = make(tmp_path)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s.scumble(Region(0.1, 0.4, 0.9, 0.6), "burnt_umber", "titanium_white", 8,
                  load_falloff=0.9, load=0.5)
    for rec in s.history.records:
        assert rec.params["load"] == 0.5
        assert rec.params["load_falloff"] == 0.9


def test_the_band_default_does_not_reach_the_inward_case(tmp_path):
    """The two directions are measured separately and only the band was moved.

    An inward scumble's ``load`` is worth `0.005%` of a patch against `0.012%` -- so
    nothing measured asked for it, and `LESSONS.md`'s first rule is that a default
    moves where a probe says it sits outside its window and nowhere else.
    """
    s = make(tmp_path)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s.scumble(s.circle((0.5, 0.5), 0.2), "burnt_umber", "titanium_white", 6,
                  direction="inward")
    for rec in s.history.records:
        assert rec.params["load"] == brush("bristle").load == 0.9
        assert rec.params["load_falloff"] == 0.0


def test_a_band_comes_back_off_the_ground_now_it_is_laid_solid(tmp_path):
    """The canvas rather than the log: five per cent of a passage coming back as bare
    ground is strata and not a ramp, and that is what this move is for. Measured on
    the full-size band in `CALIBRATION.md` at `5.17%` before and `0.01%` after; this
    is the same call on a small canvas, asking only that the band be covered."""
    s = Session(320, 240, texture="linen", ground="toned_grey", seed=7,
                timelapse=False, out_dir=tmp_path)
    band = Region(0.1, 0.4, 0.9, 0.6)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s.scumble(band, "burnt_umber", "titanium_white", 8)
    x0, y0, x1, y1 = s.canvas.region_px(band)
    mask = np.zeros((240, 320), dtype=bool)
    mask[y0:y1, x0:x1] = True
    assert s.canvas.ground_showing(where=mask) < 0.005


# -- F5: the overhang a hard edge carries ----------------------------------------------
def test_a_hard_edge_carries_two_brushes_of_overhang(tmp_path):
    """The default move of `PLAN-0.6.0.md` workstream F, row 5, and the fix for B8.

    ``edge="hard"`` masks every dab to the outline, so the one thing an overhang still
    does there is carry every pass end up to it -- and one brush did not, because the
    default ``pressure="taper"`` reaches zero one brush out and every pass met the
    outline at part pressure.
    """
    from easel.session import _mass_overhang
    assert _mass_overhang("hard", None) == 2.0
    assert _mass_overhang("ragged", None) is None
    assert _mass_overhang("clean", None) is None
    # An overhang the painter named is the painter's, whatever the edge.
    assert _mass_overhang("hard", 0.0) == 0.0
    assert _mass_overhang("hard", 0.5) == 0.5


def test_two_brushes_close_the_bites_inside_a_sloping_hard_edge(tmp_path):
    """`CALIBRATION.md`'s own case, on the canvas rather than off the constant.

    The 3 px strip just inside a mass whose sides slope, laid solid with a round tip
    -- which loses *width* with pressure and is therefore the worst case. The
    document measures `0.85%`-`3.26%` bare at one brush against `0.055%`-`0.33%` at
    two; this asks only for the order of magnitude, on a small canvas. With the edge
    cut on the line, as 0.6.0 measured it: since 0.7.0 the edge breaks inward on
    purpose, and a bite between pass ends is a different thing from a broken edge.
    """
    lean = math.tan(math.radians(14)) * 0.6
    place = polygon([(0.30, 0.18), (0.70, 0.18),
                     (0.70 + lean, 0.82), (0.30 + lean, 0.82)])
    share = {}
    for over in (1.0, None):
        s = Session(512, 384, texture="linen", ground="white", seed=7,
                    timelapse=False, out_dir=tmp_path)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            s.block_in(place, "round_hard", "burnt_umber", size=0.05, density=1.0,
                       solid=True, edge="hard", overhang=over, direction="vertical",
                       feather=0)
        strip = (place.mask(512, 384) & ~place.inset(3.0 / 512).mask(512, 384))
        share[over] = s.canvas.ground_showing(where=strip)
    assert share[None] < share[1.0] / 2.0, share


def test_the_hard_edge_overhang_costs_dabs_and_not_strokes(tmp_path):
    """Why this move is cheap enough to make: nothing can cross the mask, so the extra
    reach buys dabs. The pass count is what `cost()` quotes, and it does not move."""
    lean = math.tan(math.radians(14)) * 0.6
    place = polygon([(0.30, 0.18), (0.70, 0.18),
                     (0.70 + lean, 0.82), (0.30 + lean, 0.82)])
    laid = {}
    for over in (1.0, None):
        s = make(tmp_path)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            laid[over] = len(s.block_in(place, "flat", "burnt_umber", size=0.05,
                                        density=1.0, edge="hard", overhang=over,
                                        direction="vertical"))
    assert laid[None] == laid[1.0]
    s = make(tmp_path)
    quoted = s.cost({"shape": place, "brush": "flat", "color": "burnt_umber",
                     "size": 0.05, "density": 1.0, "edge": "hard",
                     "direction": "vertical"})
    assert quoted == laid[None]


def test_a_hard_edge_still_lets_nothing_outside_the_outline(tmp_path):
    """The promise the move must not break. Two brushes of reach past a pass's end is
    two brushes into the mask, which stops it -- so the outline does not move."""
    place = polygon([(0.30, 0.20), (0.70, 0.20), (0.72, 0.80), (0.28, 0.80)])
    s = Session(512, 384, texture="linen", ground="white", seed=7,
                timelapse=False, out_dir=tmp_path)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s.block_in(place, "round_hard", "burnt_umber", size=0.06, density=1.0,
                   solid=True, edge="hard", direction="vertical")
    outside = ~place.mask(512, 384)
    # Everything outside the outline is still the bare ground it started as, bar the
    # boundary's own feathering.
    assert s.canvas.ground_showing(where=outside) > 0.99


def test_a_scumbles_hard_edge_was_left_where_it_was(tmp_path):
    """Measured separately and not moved: a scumble's passes are `pressure="even"`
    already, which is the whole of B8's mechanism, so it has no pass-end bites to
    close and keeps its own `0.35`. With the edge cut on the line, as 0.6.0 measured
    it -- the break 0.7.0 gives every hold is not a bite."""
    import inspect
    assert inspect.signature(Session.scumble).parameters["overhang"].default == 0.35
    lean = math.tan(math.radians(14)) * 0.6
    place = polygon([(0.30, 0.18), (0.70, 0.18),
                     (0.70 + lean, 0.82), (0.30 + lean, 0.82)])
    s = Session(512, 384, texture="linen", ground="white", seed=7,
                timelapse=False, out_dir=tmp_path)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s.scumble(place, "burnt_umber", "umber", 8, edge="hard",
                  direction="vertical", feather=0)
    strip = (place.mask(512, 384) & ~place.inset(3.0 / 512).mask(512, 384))
    assert s.canvas.ground_showing(where=strip) < 0.001


# -- 0.7.0 E: looking without the scaffolding ------------------------------------------
def _pixels(path) -> np.ndarray:
    return np.asarray(Image.open(path).convert("RGB"))


def test_the_shell_takes_the_landmarks_off_a_look(tmp_path):
    """The lighthouse handover's painter wrote `clean_look.py` because `easel look` had
    no way to take the landmark labels off the details they named. `look(marks=False)`
    had one since 0.4.0; the shell and the MCP server did not."""
    session = tmp_path / "p.easel"
    assert main(["new", str(session), "--size", "320x240", "--out-dir",
                 str(tmp_path / "out"), "--no-prelude"]) == 0
    assert main(["look", str(session), "-o", str(tmp_path / "bare.png")]) == 0
    assert main(["mark", str(session), "lamp", "0.5", "0.4"]) == 0
    assert main(["look", str(session), "-o", str(tmp_path / "marked.png")]) == 0
    assert main(["look", str(session), "--no-marks",
                 "-o", str(tmp_path / "clean.png")]) == 0

    bare = _pixels(tmp_path / "bare.png")
    assert not np.array_equal(_pixels(tmp_path / "marked.png"), bare)
    assert np.array_equal(_pixels(tmp_path / "clean.png"), bare)


def test_the_drawing_on_the_view_goes_with_the_pencil(tmp_path):
    """`PLAN-0.7.0.md` said nothing hid the guides; measured, `sketch=False` always has.
    What was missing was anything saying so, so the flag and the argument say it now."""
    from easel.cli import build_parser

    s = make(tmp_path)
    bare = np.asarray(s.look_image(scale=None, sketch=False))
    s.guide([(0.1, 0.5), (0.9, 0.5)], note="line")
    assert not np.array_equal(np.asarray(s.look_image(scale=None)), bare)
    assert np.array_equal(np.asarray(s.look_image(scale=None, sketch=False)), bare)

    sub = next(a for a in build_parser()._actions if hasattr(a, "choices") and a.choices)
    said = {o: a.help for a in sub.choices["look"]._actions for o in a.option_strings}
    assert "guides" in said["--no-sketch"]
    assert "guide" in Session.look.__doc__.split("sketch:")[1].split("marks:")[0]


# -- 0.7.0 E: a whole pass is a plan ---------------------------------------------------
def test_a_film_written_as_the_grammar_says_is_the_film_the_verb_lays(tmp_path):
    """The painter's variants were whole passes of scumbles, strokes and glazes, run
    through a harness, because *as far as I could tell* a glaze could not go into a
    plan. It could, as a mark -- and the entry `REFERENCE.md` now spells out, with the
    verb's brush and opacity written in, lays the verb's film to the pixel."""
    band = [(0.10, 0.45), (0.50, 0.48), (0.90, 0.46)]
    canvases = []
    for how in ("verb", "plan"):
        s = make(tmp_path)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            s.block_in(span("A3", "H6"), "flat", "burnt_umber", size=0.08)
            s.dry()
            if how == "verb":
                s.glaze(band, "yellow_ochre")
            else:
                s.paint([{"points": band, "glaze": True, "brush": "round_soft",
                          "color": "yellow_ochre", "opacity": GLAZE_OPACITY}])
        canvases.append(s.canvas.rgb.copy())
    assert np.array_equal(*canvases)


def test_a_film_left_to_a_strokes_defaults_is_not_the_verbs(tmp_path):
    """Why the grammar writes the brush and the opacity out rather than leaving them:
    an entry takes a stroke's, a bristle at `0.88`, and that is a different film."""
    band = [(0.10, 0.45), (0.90, 0.46)]
    s = make(tmp_path)
    t = make(tmp_path)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s.glaze(band, "yellow_ochre")
        t.paint([{"points": band, "glaze": True, "color": "yellow_ochre"}])
    assert not np.array_equal(s.canvas.rgb, t.canvas.rgb)


# -- 0.7.0 C0: what the check said, rehearsals included --------------------------------
_LOOP = "\n".join(
    f's.stroke([(0.10, {0.20 + 0.05 * i:.2f}), (0.90, {0.20 + 0.05 * i:.2f})], '
    f'"flat", "ultramarine", size=0.02)'
    for i in range(6)) + "\n"


def test_a_rehearsal_keeps_what_its_check_said(tmp_path, capsys):
    """Both of the lighthouse painter's *graded passage laid too narrow* misfires were
    printed by rehearsals of passes rewritten before they were committed, and nothing
    in the session file said the rule had fired at all: the painter rebuilt both from
    its own transcript. What a pass is told is kept now, rehearsals and counts
    included, each saying which it was -- and it is exactly what was printed."""
    session = tmp_path / "p.easel"
    assert main(["new", str(session), "--size", "320x240", "--out-dir",
                 str(tmp_path / "out"), "--budget", "50", "--no-prelude"]) == 0
    painted = tmp_path / "pass.py"
    painted.write_text('s.block_in("D5", "flat", "burnt_umber", size=0.06)\n')
    loop = tmp_path / "loop.py"
    loop.write_text(_LOOP)

    assert main(["run", str(session), str(painted)]) == 0
    records = len(Session.load(session).history.records)
    capsys.readouterr()
    assert main(["run", str(session), str(loop), "--rehearse"]) == 0
    assert main(["run", str(session), str(loop), "--count"]) == 0
    printed = capsys.readouterr().out

    kept = Session.load(session).reports()
    assert [(r.mode, r.scripts, r.at) for r in kept] == [
        ("painted", "pass.py", 0), ("rehearsed", "loop.py", records),
        ("counted", "loop.py", records)]
    assert "a loop's signature" in kept[1].text
    assert kept[1].text in printed and kept[2].text in printed

    assert main(["log", str(session), "--reports", "-n", "2"]) == 0
    shown = capsys.readouterr().out
    assert "3 pass reports saved" in shown and "the last 2" in shown
    assert "rehearsed loop.py, from record" in shown and "painted pass.py" not in shown


def test_a_rehearsal_writes_nothing_of_itself_but_the_report(tmp_path):
    """The file is written after a rehearsal now, so everything else in it has to come
    back as it was: the log, the canvas and the stream -- the *planning verbs leave
    nothing behind* test, for the one planning path that writes."""
    session = tmp_path / "p.easel"
    assert main(["new", str(session), "--size", "320x240", "--out-dir",
                 str(tmp_path / "out"), "--no-prelude"]) == 0
    painted = tmp_path / "pass.py"
    painted.write_text('s.block_in("D5", "flat", "burnt_umber", size=0.06)\n')
    assert main(["run", str(session), str(painted)]) == 0
    before = Session.load(session)

    trial = tmp_path / "trial.py"
    trial.write_text(
        's.palette["tried"] = s.palette.mix("ultramarine", "titanium_white", 0.5)\n'
        's.mark("tried", 0.3, 0.3)\n'
        's.guide([(0.1, 0.1), (0.9, 0.1)], note="tried")\n'
        's.block_in("E6", "flat", "tried", size=0.06)\n')
    assert main(["run", str(session), str(trial), "--rehearse"]) == 0
    after = Session.load(session)

    assert after.history.to_json() == before.history.to_json()
    assert np.array_equal(after.canvas.rgb, before.canvas.rgb)
    assert after.rng.bit_generator.state == before.rng.bit_generator.state
    assert after.palette.slots.keys() == before.palette.slots.keys()
    assert after.marks == before.marks and after.guides == before.guides
    assert len(after.reports()) == len(before.reports()) + 1


def test_a_scrap_of_canvas_mixes_marks_and_draws_on_its_own(tmp_path):
    """Why the file can be written after a rehearsal at all: the copy shared the
    painting's palette, landmarks and guides, so a mixture tried on the scrap of canvas
    stayed on the painting -- harmless while nothing saved it. The painter's own
    harness tried variants on `scratch()` one after another, so each started on the
    last one's mixtures; its variants re-mixed every slot they used, and a variant
    that had not would have painted with the last one's."""
    s = make(tmp_path)
    s.palette["kept"] = s.palette.mix("burnt_umber", "titanium_white", 0.3)
    s.mark("kept", 0.2, 0.2)
    s.guide([(0.1, 0.9), (0.9, 0.9)], note="kept")

    c = s.scratch()
    assert "kept" in c.palette and c.pt("kept") == s.pt("kept")   # it starts from them
    c.palette["tried"] = c.palette.mix("ultramarine", "titanium_white", 0.5)
    c.palette["kept"] = "#ff0000"
    c.mark("tried", 0.4, 0.4)
    c.unmark("kept")
    c.guide([(0.1, 0.1), (0.9, 0.1)], note="tried")
    c.unguide("kept")

    assert sorted(s.palette.slots) == ["kept"]
    assert not np.array_equal(s.palette["kept"], c.palette["kept"])
    assert s.marks == {"kept": (0.2, 0.2)}
    assert [g["note"] for g in s.guides] == ["kept"]


def test_a_saved_report_is_read_forgivingly(tmp_path):
    """A file saved before 0.7.0 has no reports and opens with none; one written by a
    later Easel may carry a mode this build does not know, which is kept; and an entry
    this build cannot read costs its own line, not the file."""
    import json

    s = make(tmp_path)
    path = s.save(tmp_path / "p.easel")
    assert Session.load(path).reports() == []

    with np.load(path, allow_pickle=False) as data:
        arrays = {k: data[k] for k in data.files}
    meta = json.loads(str(arrays["meta"]))
    del meta["reports"]
    for saved, kept in ((None, []),
                        (5, []),
                        ([{"text": 3}, "junk", {"scripts": "a.py", "mode": "later",
                                                "at": 2, "text": "said"}],
                         [("a.py", "later", 2, "said")])):
        if saved is not None:
            meta["reports"] = saved
        arrays["meta"] = np.array(json.dumps(meta))
        with open(path, "wb") as fh:
            np.savez_compressed(fh, **arrays)
        got = [(r.scripts, r.mode, r.at, r.text) for r in Session.load(path).reports()]
        assert got == kept


def test_the_shell_says_when_a_file_has_no_reports(tmp_path, capsys):
    session = tmp_path / "p.easel"
    assert main(["new", str(session), "--size", "320x240", "--no-prelude"]) == 0
    capsys.readouterr()
    assert main(["log", str(session), "--reports"]) == 0
    assert "No pass reports saved" in capsys.readouterr().out


# -- 0.7.0 F1: the time-lapse leaves the file ------------------------------------------
def _painted(tmp_path, **kw):
    """A few marks of every kind that makes a frame, and a drying that does not."""
    kw.setdefault("timelapse", True)
    s = make(tmp_path, **kw)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s.block_in(cell("D5"), "bristle", "burnt_umber", size=0.03)
        s.stroke([(0.1, 0.2), (0.9, 0.25)], "flat", "ultramarine", size=0.04)
        s.dry()
        s.smudge([(0.3, 0.5), (0.7, 0.5)])
        s.pencil([(0.1, 0.9), (0.9, 0.9)])
    return s


def _stored(path, key: str):
    import json

    with np.load(path, allow_pickle=False) as data:
        return json.loads(str(data["meta"])) if key == "meta" else data[key]


def _rewrite_meta(path, change) -> None:
    """One `.easel` file's meta edited in place, the way another release wrote it."""
    import json

    with np.load(path, allow_pickle=False) as data:
        arrays = {k: data[k] for k in data.files}
    meta = json.loads(str(arrays["meta"]))
    change(meta)
    arrays["meta"] = np.array(json.dumps(meta))
    with open(path, "wb") as fh:
        np.savez_compressed(fh, **arrays)


def test_the_session_file_keeps_no_frames_and_the_film_comes_back_from_the_log(tmp_path):
    """The lighthouse handover's file was 16.1 MB after 171 marks, and 8.8 MB of it was
    a time-lapse its painter made once, at the end. The file keeps none now; a session
    loaded from it rebuilds the film from the log at the frame size it was made with --
    and that is the film it recorded, frame for frame."""
    s = _painted(tmp_path, timelapse=120)
    recorded = list(s.history._frames)
    path = s.save(tmp_path / "p.easel")
    assert _stored(path, "frames").shape == (0, 1, 1, 3)   # what 0.6.0 writes for none

    loaded = Session.load(path)
    assert loaded.history.frame_count == 0
    rebuilt = loaded._film()._frames
    assert len(rebuilt) == len(recorded)
    assert all(np.array_equal(a, b) for a, b in zip(rebuilt, recorded, strict=True))
    # A GIF merges a frame identical to the one before it, so the count is a floor.
    assert Image.open(loaded.timelapse_gif(tmp_path / "t.gif")).n_frames > 1
    assert Image.open(loaded.contact_sheet(tmp_path / "t.png")).size[0] > 0


def test_a_loaded_session_records_no_frames_and_its_film_ends_at_the_painting(tmp_path,
                                                                              monkeypatch):
    """A frame recorded after a load would begin the film in the middle of the painting,
    and every pass run from the shell is a load: so none is built -- the dearest thing a
    mark does that is not paint -- and the film asked for afterwards is the log's, with
    the pass in it."""
    from easel.canvas import Canvas

    path = _painted(tmp_path).save(tmp_path / "p.easel")
    loaded = Session.load(path)
    built = []
    real = Canvas.thumbnail_srgb8

    def counted(self, *args, **kwargs):
        built.append(1)
        return real(self, *args, **kwargs)

    monkeypatch.setattr(Canvas, "thumbnail_srgb8", counted)
    loaded.stroke([(0.2, 0.7), (0.8, 0.7)], "bristle", "burnt_umber")
    assert built == [] and loaded.history.frame_count == 0
    last = loaded._film()._frames[-1]
    assert np.array_equal(last, real(loaded.canvas, loaded.frame_px))


def test_an_undo_from_a_file_builds_no_frames(tmp_path, monkeypatch):
    """`easel undo` rebuilds the painting from the log, and the rebuild built a frame
    after every mark it laid again -- for a film the file's next save threw away."""
    from easel.canvas import Canvas

    s = _painted(tmp_path)
    expected = s.replay(upto=len(s.history.records) - 1).canvas.rgb
    loaded = Session.load(s.save(tmp_path / "p.easel"))
    built = []
    real = Canvas.thumbnail_srgb8
    monkeypatch.setattr(Canvas, "thumbnail_srgb8",
                        lambda self, *a, **k: built.append(1) or real(self, *a, **k))
    assert loaded.undo(1) == 1
    assert built == []
    assert np.array_equal(loaded.canvas.rgb, expected)


def test_a_file_that_kept_its_frames_keeps_them(tmp_path, monkeypatch):
    """A file saved before 0.7.0 carries its time-lapse, which is the painting as it was
    painted under the release that painted it -- so it is used, not rebuilt, and goes on
    being recorded."""
    s = _painted(tmp_path)
    recorded = np.stack(s.history._frames)
    path = s.save(tmp_path / "p.easel")
    with np.load(path, allow_pickle=False) as data:
        arrays = {k: data[k] for k in data.files}
    arrays["frames"] = recorded
    with open(path, "wb") as fh:
        np.savez_compressed(fh, **arrays)

    loaded = Session.load(path)
    assert loaded.history.frame_count == len(recorded)

    def no_rebuild(*args, **kwargs):
        raise AssertionError("a film the file kept was rebuilt")

    monkeypatch.setattr(Session, "replay", no_rebuild)
    loaded.stroke([(0.2, 0.7), (0.8, 0.7)], "bristle", "burnt_umber")
    assert loaded.history.frame_count == len(recorded) + 1
    assert loaded.timelapse_gif(tmp_path / "t.gif").exists()


def test_a_painting_made_without_a_time_lapse_is_still_told_how_to_have_one(tmp_path):
    """Off means no film was asked for, from a file as much as in one process; the
    film is one flag away, and the message says which."""
    path = _painted(tmp_path, timelapse=False).save(tmp_path / "p.easel")
    loaded = Session.load(path)
    with pytest.raises(ValueError, match="No time-lapse frames.*--from-log"):
        loaded.timelapse_gif(tmp_path / "none.gif")
    assert loaded.timelapse_gif(tmp_path / "built.gif", from_log=True).exists()


def test_the_shell_says_it_is_rebuilding_before_it_does(tmp_path, capsys):
    """`easel timelapse` was a read and is a repaint now: a command that goes quiet for
    half a minute looks like one that hung, so it says what it is doing first."""
    path = _painted(tmp_path).save(tmp_path / "p.easel")
    capsys.readouterr()
    assert main(["timelapse", str(path), str(tmp_path / "t.gif"), "--every", "2"]) == 0
    caught = capsys.readouterr()
    assert "Rebuilding the film from the log" in caught.err
    assert caught.out.strip() == str(tmp_path / "t.gif")


# -- 0.7.0 F2: the engine that saved a file, and what has moved since --------------------
def _smudged(tmp_path):
    """A painting with a smudge in it, and nothing else a fix since 0.5.0 moves: its mass
    is laid solid, so no pass of it runs dry (0.7.0's dry-brush fix, 0.7.0 B below)."""
    s = make(tmp_path)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s.block_in(span("C4", "F5"), "flat", "burnt_umber", size=0.05, solid=True)
        s.smudge([(0.3, 0.5), (0.7, 0.5)])
        s.smudge([(0.3, 0.6), (0.7, 0.6)])
    return s


def _said_at_load(path) -> list:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return [(n.code, n.text) for n in Session.load(path)._load_notices]


def test_a_file_says_which_release_saved_it(tmp_path):
    import easel

    path = make(tmp_path).save(tmp_path / "p.easel")
    assert _stored(path, "meta")["engine"] == easel.__version__


def test_a_file_from_before_the_stamp_is_dated_by_what_it_carries(tmp_path):
    """No file saved so far carries the stamp. 0.6.0 wrote a `notices` key on every save
    and nothing before it wrote one, so the key dates a file to 0.6.0, and its absence
    to 0.5.0 or earlier."""
    from easel.session import _saved_by

    assert _saved_by({"engine": "0.7.0", "notices": []}) == "0.7.0"
    assert _saved_by({"notices": []}) == "0.6.0"
    assert _saved_by({}) == ""
    assert _saved_by({"engine": "unknown", "notices": []}) == "0.6.0"


def test_an_older_file_says_which_marks_a_rebuild_lays_differently(tmp_path):
    """The painter's rider on the version: its notes promise a pixel-identical rebuild,
    which relies on the release that painted it. A file saved before a fix that moves
    some of its marks says so as it opens, with how many -- and the canvas itself is
    untouched, because loading never repaints."""
    s = _smudged(tmp_path)
    path = s.save(tmp_path / "p.easel")
    _rewrite_meta(path, lambda meta: (meta.pop("engine"), meta.pop("notices")))

    with pytest.warns(UserWarning, match="saved by Easel 0.5.0 or earlier") as caught:
        loaded = Session.load(path)
    said = [w.message for w in caught if getattr(w.message, "code", "") == "older-engine"]
    assert len(said) == 1
    text = str(said[0])
    assert "2 of the marks in its log lay differently" in text
    assert "a smudge no longer starts loaded with white" in text and "(0.6.0, 2 marks)" in text
    assert [n.code for n in loaded._load_notices] == ["older-engine"]
    assert np.array_equal(loaded.canvas.rgb, s.canvas.rgb)


def test_it_is_said_once_and_only_where_something_moves(tmp_path):
    """Said once: the next save stamps the file with this release, and a painting
    continued here is this release's from then on. And only where a fix moves one of
    its marks -- a painting with no smudge in it is not told about the smudge, and a
    file saved by 0.6.0 is not told about a fix 0.6.0 made."""
    path = _smudged(tmp_path).save(tmp_path / "p.easel")
    _rewrite_meta(path, lambda meta: (meta.pop("engine"), meta.pop("notices")))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        Session.load(path).save(path)
    assert _said_at_load(path) == []

    path = _smudged(tmp_path).save(tmp_path / "q.easel")
    _rewrite_meta(path, lambda meta: meta.pop("engine"))
    assert _said_at_load(path) == []

    plain = make(tmp_path)
    plain.stroke([(0.1, 0.5), (0.9, 0.5)], "flat", "burnt_umber", size=0.05, solid=True)
    path = plain.save(tmp_path / "r.easel")
    _rewrite_meta(path, lambda meta: (meta.pop("engine"), meta.pop("notices")))
    assert _said_at_load(path) == []


def test_a_fix_is_counted_against_the_release_that_saved_the_file(tmp_path, monkeypatch):
    """A fix after the release that saved a file, with a stand-in for one: the marks it
    moves are counted, the release that saved the file is named, and the way back is
    that release. A file from a later release than this one is not dated against fixes
    this build has never heard of. (Step 6's own fix is in the list too, and moves
    nothing here: the painting's mass is solid and a smudge does not run dry.)"""
    import sys

    from easel import notices

    session_module = sys.modules["easel.session"]
    later = notices.RebuildChange("9.0.0", "every flat lays a stand-in fix", "### none",
                                  lambda record, canvas: record.brush == "flat")
    monkeypatch.setattr(notices, "REBUILDS", (*notices.REBUILDS, later))
    monkeypatch.setattr(session_module, "_engine", lambda: "9.0.0")

    path = _smudged(tmp_path).save(tmp_path / "p.easel")
    _rewrite_meta(path, lambda meta: meta.update(engine="0.6.0"))
    (code, text), = _said_at_load(path)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        flats = sum(1 for r in Session.load(path).history.records if r.brush == "flat")
    assert code == "older-engine"
    assert f"{flats} of the marks in its log lay differently under 9.0.0" in text
    assert "smudge" not in text                              # 0.6.0 made that fix itself
    assert "pip install easel-paint==0.6.0" in text

    _rewrite_meta(path, lambda meta: meta.update(engine="10.0.0"))
    assert _said_at_load(path) == []


def test_the_shell_says_what_the_file_said_at_load_on_its_own(tmp_path, capsys):
    """What a file says as it opens reached the shell as a raw Python warning -- the
    engine's own file name and line first -- and an MCP painter not at all. The shell
    says it under its own heading, once, on stderr: stdout is where `look` prints the
    path a script reads back."""
    path = _smudged(tmp_path).save(tmp_path / "p.easel")
    _rewrite_meta(path, lambda meta: (meta.pop("engine"), meta.pop("notices")))
    capsys.readouterr()
    look = tmp_path / "look.png"
    assert main(["look", str(path), "-o", str(look)]) == 0
    caught = capsys.readouterr()
    assert caught.out.strip() == str(look)
    assert "at load, 1 thing said:" in caught.err
    assert caught.err.count("older-engine") == 1 and "EaselWarning" not in caught.err
    # ...and `look` saved the file, so it is not said again.
    assert main(["look", str(path), "-o", str(look)]) == 0
    assert "at load" not in capsys.readouterr().err


# -- 0.7.0 A: an edge that is not a step -----------------------------------------------
#: A rock with four straight sides, none of them on the frame.
_ROCK = polygon([(0.22, 0.78), (0.34, 0.22), (0.70, 0.30), (0.78, 0.74)], name="rock")


def _held_mass(tmp_path, feather, place=_ROCK, size=(512, 384)):
    s = Session(*size, texture="linen", ground="toned_grey", seed=7, timelapse=False,
                out_dir=tmp_path)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s.block_in(place, "flat", "burnt_umber", size=0.06, solid=True, edge="hard",
                   feather=feather)
    return s


def test_a_hard_edge_breaks_inside_its_outline_and_lands_nowhere_past_it(tmp_path):
    """The lighthouse handover's finding 1: *hard edges are all-or-nothing*, `0.30` in
    one pixel at the tower -- the clip was one pixel of four values and then a step.
    The edge is broken inward now: past the drawn line nothing lands at all, inside it
    the canvas's tooth decides how much of the feather's depth takes paint, and deeper
    than that it is the mass it always was."""
    cut, broken = _held_mass(tmp_path, 0.0), _held_mass(tmp_path, 0.008)
    px = 0.008 * 512
    rows, cols, depth, _ = _ROCK._edge_depth(512, 384, 40.0)
    bare = np.abs(broken.canvas.rgb - broken.canvas.bare()).max(axis=2) < 1e-6
    assert bare[rows[depth <= 0], cols[depth <= 0]].all()
    band = (depth > 0) & (depth < px)
    took = ~bare[rows[band], cols[band]]
    assert 0.2 < took.mean() < 0.9                       # broken: neither cut nor gone
    # Deeper in, the same mass -- to within the few levels a brush carries in from a
    # rim it picked wet paint up off (`WET_PICKUP` in `stroke.py`): 6 of 255 at most,
    # measured, against over a hundred inside the feather.
    moved = np.abs(cut.canvas.to_srgb8().astype(int)
                   - broken.canvas.to_srgb8().astype(int)).max(axis=2)
    assert moved[rows[band], cols[band]].max() > 60
    assert moved[rows[depth > px + 1.0], cols[depth > px + 1.0]].max() <= 8


def test_the_default_edge_is_broken_over_two_thousandths_of_the_long_side(tmp_path):
    """Chosen blind by the painter, first of four, for the made things it had laid
    hard; and on every hold, `clip=` as well as `edge="hard"`, because four of its nine
    edge-drawing calls were clips (`answers-step2.md`, 10 and 11)."""
    from easel.session import _EDGE_FEATHER

    assert _EDGE_FEATHER == 0.002
    s = make(tmp_path)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        mass = s.block_in(_ROCK, "flat", "burnt_umber", size=0.06, edge="hard")
        mark = s.stroke([(0.1, 0.5), (0.9, 0.5)], "flat", "burnt_umber", clip=_ROCK)
        ragged = s.block_in("D5", "flat", "burnt_umber", size=0.06)
    assert {r.params["feather"] for r in mass} == {0.002}
    assert mark.params["feather"] == 0.002
    assert all("feather" not in r.params and "clip" not in r.params for r in ragged)


def test_a_saved_clip_replays_at_the_feather_it_was_laid_with(tmp_path):
    """A moved default never reaches a saved log. A clip laid before 0.7.0 carries no
    feather and was cut on the line, and replays cut on the line; one laid since
    carries its own, the default included, and replays at that."""
    path = [(0.1, 0.45), (0.9, 0.55)]
    s = make(tmp_path)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s.stroke(path, "flat", "burnt_umber", size=0.2, clip=_ROCK, feather=0.01)
        s.stroke(path, "flat", "ultramarine", size=0.1, clip=_ROCK, feather=0)
    first, second = s.history.records
    assert first.params["feather"] == 0.01 and "feather" not in second.params
    saved = s.save(tmp_path / "p.easel")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        loaded = Session.load(saved)
        assert np.array_equal(loaded.replay().canvas.rgb, s.canvas.rgb)
        # The shape a 0.6.0 record has: a clip, and no feather.
        del loaded.history.records[0].params["feather"]
        cut = make(tmp_path)
        cut.stroke(path, "flat", "burnt_umber", size=0.2, clip=_ROCK, feather=0)
        cut.stroke(path, "flat", "ultramarine", size=0.1, clip=_ROCK, feather=0)
        assert np.array_equal(loaded.replay().canvas.rgb, cut.canvas.rgb)


def test_the_same_outline_at_two_feathers_is_two_masks(tmp_path):
    """The plan's risk: the mask memo serving a stale mask. Anything a mask is computed
    from has to be in its cache key (`LESSONS.md`, trap 5), and the feather is."""
    def lay(second, forget=False):
        s = make(tmp_path)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            s.stroke([(0.1, 0.40), (0.9, 0.40)], "flat", "burnt_umber", size=0.15,
                     clip=_ROCK, feather=0)
            if forget:
                s._clip_memo = None
            s.stroke([(0.1, 0.60), (0.9, 0.60)], "flat", "ultramarine", size=0.15,
                     clip=_ROCK, feather=second)
        return s.canvas.rgb

    assert np.array_equal(lay(0.01), lay(0.01, forget=True))
    assert not np.array_equal(lay(0.01), lay(0.0))


def test_a_side_on_the_frame_is_not_an_edge(tmp_path):
    """A mass that meets the frame should run off it, and a shape clamps a side drawn
    past the frame onto it: broken there, the frame would get a strip of ground down
    it. Only the one side that is a line moves."""
    band = Region(0.0, 0.0, 1.0, 0.5)
    cut = _held_mass(tmp_path, 0.0, place=band)
    broken = _held_mass(tmp_path, 0.01, place=band)
    moved = np.abs(cut.canvas.to_srgb8().astype(int)
                   - broken.canvas.to_srgb8().astype(int)).max(axis=2)
    assert moved[186:192].max() > 60                     # the line at y=0.5, row 192
    frame = np.concatenate([moved[:20, :].ravel(), moved[:180, :20].ravel(),
                            moved[:180, -20:].ravel()])
    assert frame.max() <= 1                              # the frame is not an edge


def test_a_thin_shape_keeps_its_body_and_breaks_at_its_rim(tmp_path):
    """A strip narrower than four feathers has no inside as deep as the feather, and
    ramped over the whole of it would be broken from both sides into its middle: a
    clip two pixels wide kept `37%` of its paint at the default on a 1024 canvas. The
    edge breaks over a quarter of the shape's own width there instead -- and a shape
    wider than four feathers is exactly what it was."""
    def painted(px):
        half = px / 768 / 2
        strip = polygon([(0.2, 0.5 - half), (0.8, 0.5 - half), (0.8, 0.5 + half),
                         (0.2, 0.5 + half)])
        s = Session(1024, 768, texture="linen", ground="toned_grey", seed=7,
                    timelapse=False, out_dir=tmp_path)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            s.stroke([(0.1, 0.5), (0.9, 0.5)], "flat", "burnt_umber", size=0.03,
                     solid=True, clip=strip)
        bare = np.abs(s.canvas.rgb - s.canvas.bare()).max(axis=2) < 0.02
        return 1.0 - bare[strip.mask(1024, 768)].mean()

    assert painted(2) > 0.95 and painted(4) > 0.95
    tower = polygon([(0.68, 0.54), (0.72, 0.54), (0.7135, 0.207), (0.6865, 0.207)])
    rows, cols, depth, full = tower._edge_depth(1024, 768, 2.048, tower.coverage(1024, 768))
    sides = (depth > 0) & (np.abs(rows - 380) < 100)
    assert np.allclose(full[sides], 2.048)

def _each_hold(s, verb: str, feather):
    """One call of ``verb`` held to the left half of the canvas, at ``feather``."""
    left = Region(0.0, 0.0, 0.5, 1.0)
    path = [(0.2, 0.48), (0.8, 0.52)]
    if verb == "stroke":
        return s.stroke(path, "flat", "burnt_umber", size=0.2, clip=left, feather=feather)
    if verb == "dab":
        return s.dab(0.5, 0.5, "round_hard", "burnt_umber", size=0.2, press=3, clip=left,
                     feather=feather)
    if verb == "glaze":
        return s.glaze(path, "burnt_umber", opacity=0.6, size=0.2, clip=left,
                       feather=feather)
    if verb == "smudge":
        s.block_in(Region(0.0, 0.0, 0.5, 1.0), "flat", "burnt_umber", size=0.1, solid=True)
        s.block_in(Region(0.5, 0.0, 1.0, 1.0), "flat", "titanium_white", size=0.1,
                   solid=True)
        return s.smudge([(0.35, 0.3), (0.65, 0.7)], size=0.04,
                        clip=Region(0.0, 0.0, 0.55, 1.0), feather=feather)
    if verb == "block_in":
        return s.block_in(Region(0.2, 0.2, 0.5, 0.8), "flat", "burnt_umber", size=0.06,
                          solid=True, edge="hard", feather=feather)
    if verb == "sweep":
        return s.sweep(path, "flat", "burnt_umber", into="down", depth=0.1, size=0.05,
                       clip=left, feather=feather)
    if verb == "scumble":
        return s.scumble(Region(0.2, 0.2, 0.5, 0.8), "burnt_umber", "titanium_white", 4,
                         size=0.05, edge="hard", feather=feather)
    return s.cover(Region(0.2, 0.2, 0.5, 0.8), "burnt_umber", size=0.05, feather=feather)


@pytest.mark.parametrize("verb", ["stroke", "dab", "glaze", "smudge", "block_in", "sweep",
                                  "scumble", "cover"])
def test_every_verb_that_holds_its_paint_breaks_the_edge(tmp_path, verb):
    """Every verb that takes a hold takes the feather that breaks it -- three of them
    through ``**kw``, which a signature does not show, so each is called."""
    canvases = []
    for feather in (0.0, 0.01):
        s = make(tmp_path)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            _each_hold(s, verb, feather)
        canvases.append(s.canvas.rgb.copy())
    assert not np.array_equal(*canvases)


def test_a_feather_needs_an_edge_to_break(tmp_path):
    """Given to a call that holds nothing, a feather would change nothing and say
    nothing -- a ragged edge is broken by its brush -- so it is refused; ``0`` asks for
    what such a call does anyway and is taken, so a helper passing it on every mark
    works. The unit is the long side's, like ``size``, and a pixel count is named as
    one. A burial is refused before its dry is laid."""
    path = [(0.1, 0.5), (0.9, 0.5)]
    s = make(tmp_path)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for call in (lambda: s.stroke(path, "flat", "burnt_umber", feather=0.003),
                     lambda: s.block_in("D5", "flat", "burnt_umber", feather=0.003),
                     lambda: s.block_in("D5", "flat", "burnt_umber", edge="clean",
                                        feather=0.003),
                     lambda: s.sweep(path, "flat", "burnt_umber", into="down",
                                     feather=0.003)):
            with pytest.raises(ValueError, match="holds it to none"):
                call()
        with pytest.raises(ValueError, match="long side, like size"):
            s.stroke(path, "flat", "burnt_umber", clip="D5", feather=2)
        with pytest.raises(ValueError, match="zero or more"):
            s.stroke(path, "flat", "burnt_umber", clip="D5", feather=-0.001)
        with pytest.raises(ValueError, match="holds it to none"):
            s.cover("D5", "burnt_umber", edge="ragged", feather=0.003)
        assert s.history.records == []
        s.stroke(path, "flat", "burnt_umber", feather=0)
    assert len(s.history.records) == 1


def test_a_plan_carries_the_feather(tmp_path):
    """An entry takes every keyword its call does, this one included -- priced,
    previewed, rehearsed and painted as it was written."""
    plan = [{"shape": _ROCK, "brush": "flat", "color": "burnt_umber", "size": 0.06,
             "edge": "hard", "feather": 0},
            {"points": [(0.1, 0.5), (0.9, 0.5)], "brush": "flat", "size": 0.1,
             "clip": _ROCK, "feather": 0.006}]
    s = make(tmp_path)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        quoted = s.cost(plan)
        s.preview(plan)
        s.rehearse(plan)
        laid = s.paint(plan)
    assert len(laid) == quoted
    assert all("feather" not in r.params for r in laid[:-1])
    assert laid[-1].params["feather"] == 0.006


def test_roughen_walks_an_outline_off_its_line_and_leaves_the_frame_alone():
    """A3, from the painter's own fifteen lines: *if A3 existed as a shape option, I'd
    have used it for rock*. A shape comes back a shape, the same seed the same outline
    -- and nothing on the frame moves, or a mass that ran off the canvas would pull
    back from it and leave a strip of ground."""
    land = polygon([(0.1, 0.6), (0.5, 0.42), (1.2, 0.5), (1.2, 1.2), (0.1, 1.2)],
                   name="land")
    rough = roughen(land, seed=3, aspect=4 / 3)
    assert isinstance(rough, Polygon) and rough.name == "land"
    assert len(rough.points) > len(land.points)
    assert roughen(land, seed=3, aspect=4 / 3).points == rough.points
    assert roughen(land, seed=4, aspect=4 / 3).points != rough.points
    framed = {p for p in land.points if p[0] >= 1.0 or p[1] >= 1.0}
    assert framed <= set(rough.points)
    assert not any(0.999 < x < 1.0 or 0.999 < y < 1.0 for x, y in rough.points)


def test_roughen_wanders_by_amp_keeps_a_runs_ends_and_calms_where_asked():
    """``amp`` is the typical distance off the line, in the long side's unit; a run
    keeps its two ends so it still meets the outline it is part of; and ``calm``
    stills the wander where something stands on it."""
    line = [(0.0, 0.5), (1.0, 0.5)]
    walked = roughen(line, amp=0.01, step=0.004, seed=5)
    assert walked[0] == (0.0, 0.5) and walked[-1] == (1.0, 0.5)
    spread = float(np.std([y - 0.5 for _, y in walked]))
    assert 0.006 < spread < 0.014
    still = roughen(line, amp=0.01, step=0.004, seed=5, calm=lambda x, y: 0.0)
    assert all(y == 0.5 for _, y in still)
    seat = roughen(line, amp=0.01, step=0.004, seed=5, calm=(0.5, 0.5))
    assert max(abs(y - 0.5) for x, y in seat if abs(x - 0.5) < 0.005) < 0.004
    with pytest.raises(ValueError, match="long side like size"):
        roughen(line, amp=-1)


# -- 0.7.0 B: a dry brush that streaks rather than speckles ----------------------------
@pytest.fixture
def old_gate(monkeypatch):
    """0.6.0's gate, for the length of a call: ``with old_gate(): ...``.

    Not a copy of the old stamp. The engine lays exactly 0.6.0's gate wherever
    ``Canvas.drag`` says a dab does not drag -- a loaded brush, a tooth that cannot gate
    it -- so a brush that never drags is 0.6.0's brush, line for line.
    """
    from contextlib import contextmanager

    from easel.canvas import Canvas

    @contextmanager
    def held():
        with monkeypatch.context() as m:
            m.setattr(Canvas, "drag", lambda self, load, need: 0.0)
            yield
    return held


def _field(value=0.56, size=(1024, 768), texture="linen"):
    """A canvas set to one colour rather than painted, so all that moves is the mark."""
    s = Session(*size, texture=texture, ground="burnt_sienna", seed=11, timelapse=False)
    s.palette["field"] = s.palette.at_value(s.palette.mix("cerulean", "titanium_white", 0.7),
                                            value)
    s.canvas.rgb[...] = s.palette["field"]
    s.palette["cloud"] = s.palette.at_value(s.palette.mix("ultramarine", "alizarin", 0.25),
                                            0.39)
    return s


def _took_paint(s, before):
    """Where a mark moved the canvas's values by an 8-bit level or more."""
    return np.abs(s.canvas.values(sketch=False).astype(int) - before) >= 1


def _runs_along(mask, step, axis):
    """How often a pixel that took paint has paint ``step`` pixels on along ``axis``."""
    if axis == 1:
        a, b = mask[:, :-step], mask[:, step:]
    else:
        a, b = mask[:-step, :], mask[step:, :]
    return float((a & b).sum() / max(a.sum(), 1))


def test_a_starving_bristle_drags_streaks_where_it_dotted(tmp_path, old_gate):
    """The lighthouse handover's finding 2: *dry-brush speckle reads as dirt*. The sky's
    own crosser at `load=0.45` landed 571 pieces with a median of 4 px, as long across
    the travel as along it -- the tooth gated a pixel at a time. Dragged, what it lays
    runs with the brush: paint a few pixels on along the travel is far likelier than a
    few pixels across it, which for dots it is not."""
    def lay(old):
        s = _field()
        before = s.canvas.values(sketch=False).astype(int)
        with warnings.catch_warnings(), (old_gate() if old else nullcontext()):
            warnings.simplefilter("ignore")
            s.stroke([(-0.06, 0.46), (0.5, 0.46), (1.06, 0.46)], "bristle", "cloud",
                     size=0.065, load=0.45, opacity=0.40, pressure="swell", smooth=False)
        return _took_paint(s, before)

    dots, streaks = lay(True), lay(False)
    # Measured: 0.32 along and 0.31 across three pixels on for the dots, 0.73 and 0.37
    # for the streaks.
    assert _runs_along(dots, 3, 1) < 1.25 * _runs_along(dots, 3, 0)
    assert _runs_along(streaks, 3, 1) > 1.6 * _runs_along(streaks, 3, 0)
    assert _runs_along(streaks, 3, 1) > 1.8 * _runs_along(dots, 3, 1)


def test_each_load_lays_about_the_paint_it_laid(tmp_path, old_gate):
    """The painter's condition, and the plan's decision 12: *the amount was right, the
    shape was wrong* -- a load keeps its meaning and only its shape changes. Summed over
    strokes at different places, each with its own comb, a starving bristle lays what it
    laid under 0.6.0's gate; one stroke on its own can differ, as brushes do."""
    paths = [[(0.05, y), (0.5, y + 0.03), (0.95, y + 0.01)] for y in (0.2, 0.35, 0.5, 0.65, 0.8)]

    def total(load, old):
        laid = 0.0
        for path in paths:
            s = _field()
            with warnings.catch_warnings(), (old_gate() if old else nullcontext()):
                warnings.simplefilter("ignore")
                laid += s.stroke(path, "bristle", "cloud", size=0.065, load=load,
                                 opacity=0.4).paint
        return laid

    for load in (0.35, 0.5, 0.7):
        assert total(load, False) == pytest.approx(total(load, True), rel=0.2), load


def test_a_loaded_mark_and_a_dab_lay_exactly_what_they_laid(tmp_path, old_gate):
    """A brush drags only as it runs dry -- under `0.9` of its load -- and a dab has no
    travel to drag along: so `solid=True`, the loaded presets over a short run, and a
    single stamp of a round tip lay what they laid under 0.6.0, to the bit."""
    def lay(old):
        s = make(tmp_path)
        with warnings.catch_warnings(), (old_gate() if old else nullcontext()):
            warnings.simplefilter("ignore")
            s.stroke([(0.1, 0.3), (0.9, 0.35)], "bristle", "burnt_umber", solid=True)
            s.stroke([(0.2, 0.5), (0.26, 0.52)], "flat", "yellow_ochre", size=0.04)
            s.glaze([(0.1, 0.7), (0.15, 0.71)], "ultramarine")
            s.dab(0.6, 0.6, "round_hard", "titanium_white", size=0.03, load=0.3)
            s.block_in("D5", "flat", "burnt_umber", size=0.06, solid=True)
        return s.canvas.rgb

    assert np.array_equal(lay(True), lay(False))


def test_the_log_and_the_stream_are_where_they_were(tmp_path, old_gate):
    """Rule 6 of the plan: nothing new may touch the log index or the random stream. The
    comb's bristles hold their paint by a draw from the comb itself, not from the
    stroke's generator, so a pass of starving marks logs what it logged and leaves the
    stream where it left it."""
    def lay(old):
        s = make(tmp_path)
        with warnings.catch_warnings(), (old_gate() if old else nullcontext()):
            warnings.simplefilter("ignore")
            s.stroke([(0.1, 0.3), (0.9, 0.35)], "bristle", "burnt_umber", load=0.4)
            s.block_in("C3", "bristle", "yellow_ochre", size=0.05, load=0.5)
            s.scumble("D4", "ultramarine", "yellow_ochre")
        return [r.to_json() for r in s.history.records], s.rng.bit_generator.state

    (old_log, old_state), (new_log, new_state) = lay(True), lay(False)
    for a, b in zip(old_log, new_log, strict=True):
        a.pop("paint"), b.pop("paint")
    assert old_log == new_log and old_state == new_state


def test_the_tooth_read_along_the_travel_keeps_the_tooths_own_values():
    """Read along the travel, the tooth is averaged over a thread's length -- and then
    given back its own distribution rank for rank, because an average is narrower than
    what it averages and would let a different share of the canvas through at every
    load: 22% more paint at `0.60` on rough, 12% less at `0.35`, as step 2 benched it.
    On every surface, in the tail a starving brush reads too: ranked against every
    fourth pixel, smooth's -- whose grain is a lattice four pixels apart -- came back
    wider than it is, and let through twice what it should at the tooth's ceiling."""
    from easel.canvas import _TOOTH_GRAIN_W, _TOOTH_HEIGHT_W, Canvas

    for texture in ("smooth", "linen", "rough"):
        c = Canvas(512, 384, texture=texture, seed=5)
        tooth = c.height_map * _TOOTH_HEIGHT_W + c.grain * _TOOTH_GRAIN_W
        for travel in (0.0, 0.5):
            along = c.tooth_along(travel)
            qs = np.r_[np.linspace(0.02, 0.98, 25), 0.99, 0.995]
            assert np.allclose(np.quantile(along, qs), np.quantile(tooth, qs), atol=0.005), \
                (texture, travel)
            assert along.min() >= tooth.min() and along.max() <= tooth.max()

    c = Canvas(512, 384, texture="linen", seed=5)
    tooth = c.height_map * _TOOTH_HEIGHT_W + c.grain * _TOOTH_GRAIN_W
    along = c.tooth_along(0.0)

    def corr(field, dx, dy):
        h, w = field.shape
        a = field[max(dy, 0):h + min(dy, 0), max(dx, 0):w + min(dx, 0)]
        b = field[max(-dy, 0):h + min(-dy, 0), max(-dx, 0):w + min(-dx, 0)]
        return float(np.corrcoef(a.ravel(), b.ravel())[0, 1])

    # Measured: 0.20 and 0.19 four pixels on, raw; 0.45 along and 0.18 across, read along.
    assert abs(corr(tooth, 4, 0) - corr(tooth, 0, 4)) < 0.05
    assert corr(along, 4, 0) > corr(along, 0, 4) + 0.15
    assert c.tooth_along(math.pi) is along                 # one field for both ways along
    assert c.trial_copy().tooth_along(0.0) is along        # and a rehearsal reads the same


def test_a_comb_between_its_bristles_lays_what_the_stroke_would():
    """B2, tuned: each bristle keeps a share of the tooth of its own -- the wettest
    more, the driest less, one gone dry nothing -- around a share chosen so the comb,
    each bristle weighed by how much of the tip it is, keeps what the stroke would.
    Down to a stroke that keeps a fraction of a percent, which the wettest bristle
    carries: a comb whose bristles could only be in or out laid nothing there, or one
    bristle's worth."""
    from easel.brush import bristle_shares
    from easel.canvas import DryComb

    rng = np.random.default_rng(3)
    for comb in range(1, 6):
        shares = bristle_shares(14, 0, comb)
        weights = rng.uniform(0.0, 1.0, shares.size)
        dry = DryComb(shares, weights)
        for kept in (0.002, 0.005, 0.05, 0.2, 0.5, 0.8, 0.95):
            each = dry.each(kept)
            assert float(each @ weights / weights.sum()) == pytest.approx(kept, rel=0.01)
            if 0.05 <= kept <= 0.8:
                assert each.max() - each.min() > 0.2      # and it is spread, not even
            if 0.05 <= kept <= 0.2:
                assert each.min() < 1e-3                  # its driest bristles out
    assert np.array_equal(bristle_shares(14, 0, 2), bristle_shares(14, 0, 2))
    assert sorted((bristle_shares(14, 0, 2) * bristle_shares(14, 0, 2).size).astype(int)) \
        == list(range(bristle_shares(14, 0, 2).size))    # one share in every slice


def test_drags_says_which_marks_the_gate_moves(tmp_path, old_gate):
    """The rebuild notice counts the marks this fix lays differently (`NOTES-step4.md`,
    4: *the one piece of it that has to be exact enough to count*). Asked of each mark
    before it is laid, `drags()` agrees with laying it both ways."""
    from easel.brush import brush
    from easel.stroke import drags

    marks = [
        ([(0.1, 0.5), (0.9, 0.52)], "bristle", {"load": 0.4}),
        ([(0.1, 0.5), (0.9, 0.52)], "flat", {"size": 0.03}),
        ([(0.1, 0.5), (0.9, 0.52)], "round_hard", {"size": 0.02, "load": 0.5}),
        ([(0.4, 0.5), (0.45, 0.5)], "flat", {"size": 0.04}),
        ([(0.1, 0.5), (0.9, 0.52)], "bristle", {"load": 1.0, "load_falloff": 0.0}),
        # The preset's own 0.9, which a stroke's float32 loads carry as 0.89999998:
        # loaded, not dragging, and not counted.
        ([(0.1, 0.5), (0.9, 0.52)], "bristle", {"load_falloff": 0.0}),
        ([(0.5, 0.5)], "round_hard", {"size": 0.04, "load": 0.3}),
        ([(0.5, 0.5)], "bristle", {"size": 0.06, "load": 0.4}),
        ([(0.1, 0.5), (0.9, 0.52)], "round_soft", {"texture_sensitivity": 0.0, "load": 0.2}),
    ]
    for points, name, kw in marks:
        size = kw.pop("size", None)
        b = brush(name, **({"size": size} if size else {}), **kw)
        laid = []
        for old in (True, False):
            s = make(tmp_path)
            with warnings.catch_warnings(), (old_gate() if old else nullcontext()):
                warnings.simplefilter("ignore")
                s.stroke(points, b, "titanium_white")
            laid.append(s.canvas.rgb)
        moved = not np.array_equal(*laid)
        assert drags(s.canvas, points, b) == moved, (name, kw)


def test_an_older_file_counts_its_marks_that_ran_dry(tmp_path, monkeypatch):
    """What the painter asked for with the version (question 8): told, as the file
    opens, which of its marks a rebuild lays differently under the release that dragged
    them. The count is the marks that ran dry and nothing else -- not the loaded ones,
    not the dab."""
    import sys

    from easel.stroke import drags

    s = make(tmp_path)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s.stroke([(0.1, 0.3), (0.9, 0.35)], "bristle", "burnt_umber", solid=True)
        s.stroke([(0.1, 0.5), (0.9, 0.52)], "bristle", "yellow_ochre", load=0.4)
        s.stroke([(0.1, 0.7), (0.9, 0.68)], "flat", "ultramarine", size=0.03)
        s.dab(0.5, 0.5, "round_hard", "titanium_white", size=0.03)
    path = s.save(tmp_path / "p.easel")
    _rewrite_meta(path, lambda meta: meta.update(engine="0.6.0"))
    monkeypatch.setattr(sys.modules["easel.session"], "_engine", lambda: "0.7.0")

    (code, text), = _said_at_load(path)
    assert code == "older-engine"
    assert "2 of the marks in its log lay differently under 0.7.0" in text
    assert "drags its paint into streaks" in text and "(0.7.0, 2 marks)" in text
    assert [drags(s.canvas, r.points, _brush_of(r)) for r in s.history.records] \
        == [False, True, True, False]


def test_a_file_from_before_both_fixes_hears_of_both_and_counts_each_mark_once(tmp_path):
    """A file saved by 0.5.0 or earlier is told of every fix since, each with its own
    count, and the total counts a mark once however many fixes move it."""
    s = make(tmp_path)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s.smudge([(0.3, 0.5), (0.7, 0.5)])
        s.stroke([(0.1, 0.6), (0.9, 0.62)], "bristle", "yellow_ochre", load=0.4)
        s.stroke([(0.1, 0.7), (0.9, 0.72)], "bristle", "burnt_umber", solid=True)
    path = s.save(tmp_path / "p.easel")
    _rewrite_meta(path, lambda meta: (meta.pop("engine"), meta.pop("notices")))

    (code, text), = _said_at_load(path)
    assert code == "older-engine" and "saved by Easel 0.5.0 or earlier" in text
    assert "2 of the marks in its log lay differently" in text
    assert "(0.6.0, 1 mark)" in text and "(0.7.0, 1 mark)" in text


def _brush_of(record):
    from dataclasses import fields

    from easel.brush import Brush

    names = {f.name for f in fields(Brush)} - {"meta"}
    return Brush(**{k: v for k, v in record.params.items() if k in names})
