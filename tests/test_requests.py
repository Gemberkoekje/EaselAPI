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

import warnings

import numpy as np
import pytest
from PIL import Image

from easel import (
    Region,
    Session,
    blob,
    brush,
    cell,
    hull,
    polygon,
    ribbon,
    span,
    union,
)
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
    reference lists them without saying which call takes them."""
    s = make(tmp_path)
    with pytest.raises(TypeError, match=r"block_in\(\) argument"):
        s.scumble("upper-half", "burnt_umber", "titanium_white", 4, solid=True)
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
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        s.block_in(cap, "flat", "burnt_umber", size=0.005, edge="clean", direction="axis")
        s.block_in(cap, "flat", "burnt_umber", size=0.016, direction="axis")   # ragged


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
    means. It asks now -- a question, because three of that painting's four close
    pairs were masses that never met."""
    s = make(tmp_path)
    result = s.compare({Region(0.0, 0.0, 1.0, 0.3, name="sea"): 0.40,
                        Region(0.4, 0.3, 0.6, 0.9, name="tower"): 0.40,
                        Region(0.0, 0.9, 1.0, 1.0, name="rock"): 0.21})
    assert result.pairs == [("sea", "tower", pytest.approx(0.0))]
    table = result.table()
    assert "do these two touch" in table and "sea / tower, 0.00 apart" in table
    apart = s.compare({Region(0.0, 0.0, 1.0, 0.3, name="sea"): 0.40,
                       Region(0.0, 0.9, 1.0, 1.0, name="rock"): 0.21})
    assert apart.pairs == [] and "do these two touch" not in apart.table()


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
    for i in range(3):
        s.stroke([(0.2 + i * 0.1, 0.45), (0.22 + i * 0.1, 0.47)], "bristle", "burnt_umber",
                 size=0.012)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s.stroke([(0.5, 0.5), (0.52, 0.56)], "flat", "burnt_umber", size=0.03,
                 pressure=[1.0, 0.35])
    report = s.report()
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
