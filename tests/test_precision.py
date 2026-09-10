"""M6: the tools for working below the size of a grid cell.

The drawing under the paint, landmarks, matching crops, the preview, the rehearsal,
the value numbers and the prepared reference. Nothing in this milestone places a
stroke for the painter, so most of what is worth asserting is about what these
tools *do not* do: preview paints nothing, rehearse commits nothing, and neither
disturbs the painting that follows.

Where a test could pass by asking the API what it did, it asks the canvas instead.
Both M4 engine defects were invisible from the return value.
"""

from __future__ import annotations

import json

import numpy as np
import pytest
from PIL import Image, ImageDraw

from easel import Session
from easel.brush import _MASK_CACHE, brush, tip_mask
from easel.look import MIN_CROP_SIZE, render_look
from easel.prepare import _trace_outline, prepare_reference
from easel.regions import Region, as_region, cell, span


@pytest.fixture
def reference(tmp_path):
    """A synthetic 'ordinary object': masses with real edges and real value steps.

    More masses than any one level wants to find, on purpose. A picture with
    exactly four things in it cannot show that a finer level finds more, and a
    fixture that cannot fail the thing it is testing is not testing it.
    """
    w, h = 480, 360
    img = Image.new("RGB", (w, h), (176, 168, 152))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w, int(h * 0.52)], fill=(120, 126, 134))          # wall
    d.rectangle([0, int(h * 0.30), int(w * 0.22), int(h * 0.52)],
                fill=(96, 104, 116))                                     # wall shadow
    d.rectangle([0, int(h * 0.52), w, h], fill=(158, 128, 96))           # table
    d.rectangle([int(w * 0.74), int(h * 0.52), w, h], fill=(186, 158, 122))  # lit table
    d.ellipse([int(w * 0.33), int(h * 0.30), int(w * 0.63), int(h * 0.72)],
              fill=(226, 222, 214))                                      # body
    d.ellipse([int(w * 0.33), int(h * 0.27), int(w * 0.63), int(h * 0.35)],
              fill=(198, 194, 188))                                      # rim
    d.ellipse([int(w * 0.37), int(h * 0.29), int(w * 0.59), int(h * 0.33)],
              fill=(84, 76, 68))                                         # inside
    d.ellipse([int(w * 0.60), int(h * 0.40), int(w * 0.74), int(h * 0.58)],
              fill=(226, 222, 214))                                      # handle
    d.ellipse([int(w * 0.63), int(h * 0.44), int(w * 0.70), int(h * 0.54)],
              fill=(158, 128, 96))
    d.ellipse([int(w * 0.31), int(h * 0.66), int(w * 0.70), int(h * 0.76)],
              fill=(112, 92, 70))                                        # cast shadow
    d.ellipse([int(w * 0.08), int(h * 0.58), int(w * 0.24), int(h * 0.70)],
              fill=(140, 88, 74))                                        # something else
    path = tmp_path / "reference.png"
    img.save(path)
    return path


def make(tmp_path, **kw):
    kw.setdefault("timelapse", False)
    return Session(480, 360, texture="linen", ground="toned_grey", seed=4,
                   out_dir=tmp_path, **kw)


# --------------------------------------------------------------------------------------
# The pencil and the sketch channel
# --------------------------------------------------------------------------------------
def test_pencil_draws_graphite_and_nothing_else(tmp_path):
    """No paint, no wetness, no paint height. It is a drawing, not a mark."""
    s = make(tmp_path)
    before = s.canvas.rgb.copy()
    record = s.pencil([(0.2, 0.3), (0.8, 0.4)])

    assert s.canvas.has_sketch and s.canvas.sketch.max() > 0.2
    assert record.paint > 0, "the pencil reported drawing nothing"
    assert np.array_equal(s.canvas.rgb, before), "the pencil deposited paint"
    assert float(s.canvas.wetness.max()) == 0.0
    assert float(s.canvas.thickness.max()) == 0.0


def test_drawing_is_free(tmp_path):
    """Drawing, erasing and drying do not spend the painter's stroke budget.

    The definition of done counts strokes. A painter charged for the underdrawing
    is a painter who skips the underdrawing, which is the opposite of the point.
    """
    s = make(tmp_path)
    s.pencil([(0.2, 0.3), (0.8, 0.4)])
    s.pencil([(0.3, 0.7), (0.7, 0.6)])
    s.erase("upper-left")
    s.dry()
    assert s.stroke_count == 0
    s.stroke([(0.1, 0.1), (0.4, 0.4)], "bristle", "burnt_umber")
    assert s.stroke_count == 1


def test_paint_buries_the_drawing_in_proportion_to_what_lands(tmp_path):
    """An opaque mass takes the graphite; a veil leaves most of it."""
    def survives(**stroke_kw):
        s = make(tmp_path)
        s.pencil([(0.2, 0.5), (0.8, 0.5)], pressure=0.8)
        # The mean over the band, not the max: the max reports the one grain
        # the tooth happened to spare, which is not what 'buried' means.
        band = (slice(170, 190), slice(120, 360))
        before = float(s.canvas.sketch[band].mean())
        s.stroke([(0.2, 0.5), (0.8, 0.5)], **stroke_kw)
        return float(s.canvas.sketch[band].mean()) / max(before, 1e-6)

    opaque = survives(brush="flat", color="titanium_white", size=0.12)
    veil = survives(brush="round_soft", color="titanium_white", size=0.12,
                    opacity=0.10, glaze=True)
    assert opaque < 0.10, f"an opaque mass left {opaque:.0%} of the drawing showing"
    assert 0.35 < veil < 0.85, f"a veil left {veil:.0%} of the drawing -- expected a veil"
    assert veil > opaque


def test_the_drawing_survives_where_the_tooth_refused_the_paint(tmp_path):
    """Thin paint shows the drawing *and the ground* through it.

    A starved brush deposits nothing in the valleys, so the graphite there is
    untouched. That is why an underdrawing keeps working through a scumble, and it
    falls out of gating burial on what landed rather than on what was aimed at.
    """
    s = make(tmp_path)
    s.pencil([(0.1, 0.5), (0.9, 0.5)], pressure=0.9)
    drawn = s.canvas.sketch > 0.05
    s.stroke([(0.1, 0.5), (0.9, 0.5)], "bristle", "titanium_white", size=0.1,
             load=0.2, load_falloff=1.3)
    assert (s.canvas.sketch[drawn] > 0.05).any(), \
        "a starved stroke wiped out graphite it never covered"


def test_erase_clears_only_where_asked(tmp_path):
    s = make(tmp_path)
    s.pencil([(0.05, 0.25), (0.95, 0.25)], pressure=0.8)
    s.erase(Region(0.0, 0.0, 0.5, 1.0))
    left = s.canvas.sketch[:, : s.canvas.width // 2]
    right = s.canvas.sketch[:, s.canvas.width // 2:]
    assert float(left.max()) == 0.0
    assert float(right.max()) > 0.1
    s.erase()
    assert not s.canvas.has_sketch and float(s.canvas.sketch.max()) == 0.0


def test_the_drawing_can_be_hidden_in_a_look_and_in_an_export(tmp_path):
    s = make(tmp_path)
    s.pencil([(0.1, 0.5), (0.9, 0.5)], pressure=1.0)
    with_it = np.asarray(s.look_image(sketch=True), dtype=np.int16)
    without = np.asarray(s.look_image(sketch=False), dtype=np.int16)
    assert np.abs(with_it - without).max() > 8, "look(sketch=False) showed the drawing"

    shown = np.asarray(Image.open(s.export(tmp_path / "a.png")), dtype=np.int16)
    hidden = np.asarray(Image.open(s.export(tmp_path / "b.png", sketch=False)),
                        dtype=np.int16)
    assert np.abs(shown - hidden).max() > 8
    # The default keeps it: what is on the canvas is what comes out.
    assert np.array_equal(shown, np.asarray(Image.open(s.export(tmp_path / "c.png")),
                                            dtype=np.int16))


def test_undo_brings_back_a_drawing_the_paint_covered(tmp_path):
    s = make(tmp_path)
    s.pencil([(0.2, 0.5), (0.8, 0.5)], pressure=0.9)
    drawing = s.canvas.sketch.copy()
    s.stroke([(0.2, 0.5), (0.8, 0.5)], "flat", "titanium_white", size=0.12)
    assert float(s.canvas.sketch.max()) < float(drawing.max())
    s.undo(1)
    assert np.array_equal(s.canvas.sketch, drawing), \
        "undo restored the paint but not the drawing under it"


def test_sketch_lines_returns_what_was_drawn(tmp_path):
    s = make(tmp_path)
    s.pencil([(0.2, 0.3), (0.5, 0.4), (0.8, 0.3)])
    s.stroke([(0.1, 0.1), (0.2, 0.2)], "bristle", "burnt_umber")
    s.pencil([(0.3, 0.7), (0.7, 0.7)])
    lines = s.sketch_lines()
    assert len(lines) == 2, "sketch_lines picked up something that was not a pencil line"
    assert lines[0][0] == pytest.approx((0.2, 0.3))
    assert len(lines[1]) == 2


def test_a_painting_with_a_drawing_in_it_replays_exactly(tmp_path):
    s = make(tmp_path)
    s.mark("a", 0.3, 0.4)
    s.pencil([(0.2, 0.3), (0.5, 0.45), (0.8, 0.3)], pressure=0.7)
    s.stroke([(0.2, 0.6), (0.8, 0.62)], "bristle", "burnt_umber", size=0.08)
    s.erase(Region(0.0, 0.0, 0.25, 1.0))
    s.pencil([(0.4, 0.8), (0.9, 0.75)])

    again = s.replay()
    assert np.array_equal(again.canvas.rgb, s.canvas.rgb)
    assert np.array_equal(again.canvas.sketch, s.canvas.sketch)
    assert again.marks == s.marks


def test_the_drawing_and_the_landmarks_survive_a_round_trip_through_disk(tmp_path):
    s = make(tmp_path)
    s.pencil([(0.2, 0.3), (0.8, 0.4)], pressure=0.8)
    s.mark("chin", 0.42, 0.66)
    s.stroke([(0.1, 0.8), (0.9, 0.85)], "bristle", "burnt_umber")
    path = s.save(tmp_path / "p.easel")

    back = Session.load(path)
    assert np.array_equal(back.canvas.sketch, s.canvas.sketch)
    assert back.canvas.has_sketch
    assert back.marks == {"chin": (0.42, 0.66)}
    assert np.array_equal(back.canvas.to_srgb8(), s.canvas.to_srgb8())


def test_a_session_that_never_drew_stores_no_graphite(tmp_path):
    """The channel is a whole colour plane. A painting that never drew should not
    carry one on disk, and must still load with an empty one."""
    s = make(tmp_path)
    s.stroke([(0.1, 0.1), (0.9, 0.9)], "bristle", "burnt_umber")
    with np.load(s.save(tmp_path / "p.easel"), allow_pickle=False) as data:
        assert data["sketch"].size == 0
    back = Session.load(tmp_path / "p.easel")
    assert not back.canvas.has_sketch
    assert back.canvas.sketch.shape == (back.canvas.height, back.canvas.width)


def test_a_session_saved_before_m6_still_loads(tmp_path):
    """Format 1 files have no graphite channel and no landmarks. They still open."""
    s = make(tmp_path)
    s.stroke([(0.1, 0.1), (0.9, 0.9)], "bristle", "burnt_umber")
    path = s.save(tmp_path / "old.easel")

    with np.load(path, allow_pickle=False) as data:
        fields = {k: data[k] for k in data.files}
    meta = json.loads(str(fields.pop("meta")))
    meta["format"] = 1
    meta.pop("marks", None)
    meta.pop("has_sketch", None)
    fields.pop("sketch")
    with open(path, "wb") as fh:
        np.savez_compressed(fh, meta=np.array(json.dumps(meta)), **fields)

    back = Session.load(path)
    assert back.marks == {}
    assert not back.canvas.has_sketch
    assert np.array_equal(back.canvas.to_srgb8(), s.canvas.to_srgb8())


# --------------------------------------------------------------------------------------
# Landmarks
# --------------------------------------------------------------------------------------
def test_landmarks_are_named_points_usable_in_a_path(tmp_path):
    s = make(tmp_path)
    assert s.mark("eye_l", 0.42, 0.31) == (0.42, 0.31)
    s.mark("eye_r", 0.58, 0.31)
    s.stroke([s.pt("eye_l"), s.pt("eye_r")], "liner", "burnt_umber")
    assert s.stroke_count == 1

    s.mark("eye_l", 0.44, 0.32)
    assert s.pt("eye_l") == (0.44, 0.32), "marking the same name did not move the mark"
    s.unmark("eye_l")
    with pytest.raises(KeyError, match="eye_r"):
        s.pt("eye_l")          # the message lists what *is* marked


def test_marking_a_non_finite_point_explains_itself(tmp_path):
    """np.clip does not sanitise NaN, so a non-finite mark used to be silently
    accepted and written into the session's JSON metadata as a bare NaN/Infinity
    token -- valid to this codebase's own json.loads, but not standard JSON.
    """
    s = make(tmp_path)
    with pytest.raises(ValueError, match="real position"):
        s.mark("bad", float("nan"), 0.5)
    with pytest.raises(ValueError, match="real position"):
        s.mark("bad", 0.5, float("inf"))


def test_landmarks_are_drawn_on_both_panels(tmp_path, reference):
    s = make(tmp_path)
    plain = np.asarray(s.look_image(reference=reference), dtype=np.int16)
    s.mark("here", 0.2, 0.5)
    marked = np.asarray(s.look_image(reference=reference), dtype=np.int16)

    left = slice(0, plain.shape[1] // 2 - 8)      # the reference panel
    right = slice(plain.shape[1] // 2 + 8, None)  # the canvas panel
    assert not np.array_equal(plain[:, left], marked[:, left]), \
        "the landmark never reached the reference panel"
    assert not np.array_equal(plain[:, right], marked[:, right])


def test_a_landmark_outside_a_crop_is_not_drawn_in_it(tmp_path):
    s = make(tmp_path)
    inside = np.asarray(s.look_image(region=cell("D4")), dtype=np.int16)
    s.mark("far", 0.95, 0.95)
    assert np.array_equal(inside, np.asarray(s.look_image(region=cell("D4")),
                                             dtype=np.int16))


# --------------------------------------------------------------------------------------
# Matching crops and the fine grid
# --------------------------------------------------------------------------------------
def test_a_crop_with_a_reference_crops_both_panels(tmp_path, reference):
    """The one thing a close look must not do is compare a detail to a thumbnail."""
    s = make(tmp_path)
    ref = Image.open(reference).convert("RGB")
    whole = render_look(s.canvas, reference=ref)
    cropped = render_look(s.canvas, reference=ref, region=cell("D4"))

    # In the whole view the reference panel holds the dark table band; in a crop of
    # D4 -- upper middle -- it must not.
    def panel(img):
        arr = np.asarray(img, dtype=np.float32)
        return arr[:, : arr.shape[1] // 2 - 8]

    assert panel(whole).std() > panel(cropped).std() * 1.5, \
        "the reference panel was not cropped with the canvas"


def test_a_small_crop_is_enlarged_to_feature_scale(tmp_path):
    """One cell of a 480-wide canvas is 60 px. Nothing can be judged in 60 px."""
    s = make(tmp_path)
    img = s.look_image(region=cell("D4"))
    assert max(img.size) >= MIN_CROP_SIZE
    assert MIN_CROP_SIZE / 60 >= 5, "a cell must show at five times or more"


def test_the_fine_grid_is_a_different_grid(tmp_path):
    s = make(tmp_path)
    coarse = np.asarray(s.look_image(region=cell("D4"), grid=True), dtype=np.int16)
    fine = np.asarray(s.look_image(region=cell("D4"), grid="fine"), dtype=np.int16)
    plain = np.asarray(s.look_image(region=cell("D4")), dtype=np.int16)
    assert not np.array_equal(fine, plain), "grid='fine' drew nothing"
    assert not np.array_equal(fine, coarse), "grid='fine' drew the coarse grid"


def test_a_cell_or_a_span_can_be_named_as_a_string(tmp_path):
    """Read a label off a gridded look and hand it straight back."""
    assert as_region("D4").bounds == cell("D4").bounds
    assert as_region("C3:F6").bounds == span("C3", "F6").bounds
    assert as_region("upper-band").name == "upper-band"
    with pytest.raises(KeyError, match="D4"):
        as_region("nonsense-region")

    s = make(tmp_path)
    assert s.look_image(region="D4").size == s.look_image(region=cell("D4")).size


# --------------------------------------------------------------------------------------
# Preview: plan, then check, then paint
# --------------------------------------------------------------------------------------
def test_preview_paints_nothing_and_logs_nothing(tmp_path, reference):
    s = make(tmp_path)
    s.stroke([(0.1, 0.2), (0.9, 0.3)], "bristle", "burnt_umber")
    before, records = s.canvas.rgb.copy(), len(s.history.records)

    s.preview([{"points": [(0.2, 0.6), (0.8, 0.7)], "brush": "bristle", "size": 0.08}],
              reference=reference, region=span("C3", "F6"), grid="fine")

    assert np.array_equal(s.canvas.rgb, before), "preview put paint on the canvas"
    assert len(s.history.records) == records, "preview wrote to the log"


def test_preview_takes_a_bare_path_a_list_of_paths_or_dicts(tmp_path):
    """A plan written once is checked, rehearsed and painted without being rewritten."""
    s = make(tmp_path)
    one = s._stroke_specs([(0.1, 0.2), (0.5, 0.5)])
    assert len(one) == 1 and len(one[0]["points"]) == 2

    many = s._stroke_specs([[(0.1, 0.2), (0.5, 0.5)], [(0.6, 0.6), (0.9, 0.9)]])
    assert len(many) == 2

    dicts = s._stroke_specs({"points": [(0.1, 0.2)], "brush": "liner"})
    assert dicts[0]["brush"] == "liner"

    with pytest.raises(ValueError, match="points"):
        s._stroke_specs([{"brush": "liner"}])


def test_preview_actually_draws_the_intended_strokes(tmp_path):
    s = make(tmp_path)
    plain = np.asarray(Image.open(s.look(path=tmp_path / "plain.png")), dtype=np.int16)
    shown = np.asarray(
        Image.open(s.preview([[(0.2, 0.5), (0.8, 0.5)]], path=tmp_path / "prev.png")),
        dtype=np.int16,
    )
    assert np.abs(plain - shown).max() > 30, "the preview overlay is invisible"


# --------------------------------------------------------------------------------------
# Rehearsal: try it on a scrap of canvas
# --------------------------------------------------------------------------------------
def test_rehearse_commits_nothing(tmp_path, reference):
    s = make(tmp_path)
    s.block_in("upper-half", color="burnt_umber", density=0.6)
    before, records = s.canvas.rgb.copy(), len(s.history.records)

    s.rehearse([{"points": [(0.2, 0.6), (0.8, 0.7)], "brush": "knife", "size": 0.06}],
               reference=reference, region=span("C3", "F6"))

    assert np.array_equal(s.canvas.rgb, before), "the rehearsal was painted for real"
    assert len(s.history.records) == records


def test_what_you_rehearse_is_what_you_get(tmp_path):
    """The trial strokes are seeded as the next strokes of the real painting.

    Otherwise a rehearsal shows one mark and the canvas gets another, and the whole
    tool is a lie the painter would be right to stop using.
    """
    plan = [{"points": [(0.2, 0.4), (0.5, 0.55), (0.8, 0.45)], "brush": "bristle",
             "color": "titanium_white", "size": 0.07}]

    a = make(tmp_path)
    a.stroke([(0.1, 0.8), (0.9, 0.85)], "bristle", "burnt_umber")
    trial = a._trial_session()
    for spec in plan:
        trial.stroke(**spec)

    b = make(tmp_path)
    b.stroke([(0.1, 0.8), (0.9, 0.85)], "bristle", "burnt_umber")
    for spec in plan:
        b.stroke(**spec)

    assert np.array_equal(trial.canvas.rgb, b.canvas.rgb), \
        "the rehearsed mark is not the mark that lands"


def test_rehearsing_does_not_change_the_painting_that_follows(tmp_path):
    """A rehearsal must not consume the session's random stream."""
    def run(rehearse: bool):
        s = make(tmp_path)
        if rehearse:
            s.rehearse([[(0.2, 0.3), (0.8, 0.4)]], region="D4")
            s.rehearse([[(0.3, 0.6), (0.7, 0.5)]], region="D4")
        s.block_in("lower-half", color="burnt_umber", density=0.7)
        return s.canvas.rgb

    assert np.array_equal(run(True), run(False))


# --------------------------------------------------------------------------------------
# compare(): the numbers behind a squint
# --------------------------------------------------------------------------------------
def test_comparing_a_painting_against_itself_is_zero(tmp_path, reference):
    s = make(tmp_path)
    s.block_in("all", color="yellow_ochre", density=1.0, size=0.2)
    mirror = tmp_path / "mirror.png"
    s.export(mirror)

    c = s.compare(mirror)
    assert c.max_delta < 0.02, f"a painting differs from itself by {c.max_delta:.3f}"
    assert not c.off


def test_compare_reports_the_value_the_painter_can_see(tmp_path, reference):
    """Guarding NOTES.md gotcha 0: a measurement in a space the painter cannot see.

    ``compare`` must speak in the same numbers as ``look(values=True)``, or the
    painter reads 0.5 off one and is told 0.21 by the other.
    """
    s = make(tmp_path)
    s.block_in("all", color="titanium_white", density=1.0, size=0.2)
    c = s.compare(reference)
    seen = np.asarray(s.canvas.values(), dtype=np.float32).mean() / 255.0
    measured = float(np.mean([cell.canvas for cell in c.cells]))
    assert abs(seen - measured) < 0.02, (
        f"compare says {measured:.2f} where the greyscale view shows {seen:.2f}"
    )


def test_compare_finds_the_mass_that_is_out(tmp_path, reference):
    s = make(tmp_path)
    c = s.compare(reference)
    worst = c.worst(1)[0]
    assert abs(worst.delta) == pytest.approx(c.max_delta)
    assert all(abs(x.delta) > c.threshold for x in c.off)
    assert c["A1"].label == "A1"
    assert len(c.cells) == 64
    assert c.path is not None and c.path.exists()
    assert "delta = canvas - reference" in str(c)


def test_compare_inside_a_region_measures_its_tenths(tmp_path, reference):
    """The labels are the ones look(grid='fine') shows, so a cell that is out names
    the place to fix."""
    s = make(tmp_path)
    c = s.compare(reference, region=cell("D4"))
    assert len(c.cells) == 100
    assert c.cells[0].label == "0,0"
    assert c.columns == [str(i) for i in range(10)]
    # A tenth's label reads straight back into point(u, v).
    x, y = cell("D4").point(0.3, 0.6)
    assert 0.0 <= x <= 1.0 and 0.0 <= y <= 1.0


# --------------------------------------------------------------------------------------
# prepare(): the reference cut into numbered masses
# --------------------------------------------------------------------------------------
def test_prepare_finds_the_masses_and_covers_the_picture(reference):
    prep = prepare_reference(reference, level="coarse", seed=4)
    assert 4 <= len(prep) <= 9, f"coarse should be five to eight masses, got {len(prep)}"
    assert sum(a.share for a in prep.areas) == pytest.approx(1.0, abs=1e-6)
    assert all(a.outline for a in prep.areas), "an area came back with no outline"
    assert all(0.0 <= a.value <= 1.0 for a in prep.areas)

    biggest = prep.areas[0]
    assert biggest.cells, "the largest mass sits in no grid cell"
    assert biggest.neighbours, "the largest mass touches nothing"
    assert all(0.0 <= h <= 1.0 for h in biggest.neighbours.values())


def test_a_finer_level_finds_more_masses(reference):
    coarse = prepare_reference(reference, level="coarse", seed=4)
    medium = prepare_reference(reference, level="medium", seed=4)
    assert len(medium) > len(coarse)


def test_preparing_the_same_photograph_twice_gives_the_same_map(reference):
    a = prepare_reference(reference, level="coarse", seed=4)
    b = prepare_reference(reference, level="coarse", seed=4)
    assert np.array_equal(a.labels, b.labels)


def test_the_painter_can_correct_the_map(reference):
    """The automation joins hair to a wall. Merge and split are how that gets said."""
    prep = prepare_reference(reference, level="medium", seed=4)
    before = len(prep)
    a, b = prep.numbers[0], prep.numbers[1]

    kept = prep.merge(a, b)
    assert kept == min(a, b)
    assert len(prep) == before - 1
    assert b not in prep.numbers

    parts = prep.split(kept, into=2)
    assert parts[0] == kept, "splitting renumbered the area the painter had named"
    assert len(prep) == before
    assert all(p in prep.numbers for p in parts)


def test_outline_traces_the_largest_run_when_merge_joins_two_that_do_not_touch():
    """merge()'s own docstring example is hair split by an ear -- two pieces that
    do not touch. A Moore-neighbour trace can only follow one boundary, and it
    used to follow whichever run happened to contain the mask's topmost-then-
    leftmost pixel rather than the larger one its own docstring promises.
    """
    mask = np.zeros((20, 20), dtype=bool)
    mask[1:4, 1:4] = True       # 9 px, earlier in raster order
    mask[10:18, 10:18] = True   # 64 px, the run an outline should mean
    outline = _trace_outline(mask)
    xs = [p[0] * 20 for p in outline]
    ys = [p[1] * 20 for p in outline]
    assert min(xs) >= 9 and min(ys) >= 9, "traced the small run instead of the largest"


def test_prepared_areas_can_be_looked_at_and_painted(tmp_path, reference):
    s = make(tmp_path)
    prep = s.prepare(reference)
    n = prep.areas[0].number

    assert isinstance(s.ref_region(n), Region)
    assert s.ref_region(n).bounds == prep[n].bounds
    assert len(s.ref_outline(n)) >= 3
    assert prep.overlay_path.exists()
    s.look(region=s.ref_region(n), reference=reference, path=tmp_path / "area.png")


def test_the_machine_laid_sketch_is_drawing_not_painting(tmp_path, reference):
    """`sketch()` is an assisted mode. Whatever else it is, it must not paint."""
    s = make(tmp_path)
    s.prepare(reference)
    before = s.canvas.rgb.copy()
    records = s.sketch()

    assert records, "sketch() laid no lines"
    assert all(r.kind == "pencil" for r in records)
    assert s.stroke_count == 0
    assert np.array_equal(s.canvas.rgb, before)
    assert s.canvas.has_sketch


def test_asking_for_a_preparation_before_making_one_says_so(tmp_path):
    s = make(tmp_path)
    with pytest.raises(RuntimeError, match="prepare"):
        s.ref_region(1)


# --------------------------------------------------------------------------------------
# The liner, and the mask cache the goldens caught
# --------------------------------------------------------------------------------------
def test_the_liner_draws_a_line_of_its_nominal_width(tmp_path):
    """REHEARSAL2's eye test: lines render at their nominal width down to 3 px."""
    s = Session(600, 600, texture="smooth", ground="white", seed=1,
                out_dir=tmp_path, timelapse=False)
    s.stroke([(0.2, 0.5), (0.8, 0.5)], "liner", "burnt_umber", pressure="even")
    column = s.canvas.rgb[:, 300, :].mean(axis=1)
    dark = np.nonzero(column < column.max() - 0.05)[0]
    width = int(dark.max() - dark.min() + 1) if len(dark) else 0
    nominal = brush("liner").size * 600
    assert 1 <= width <= nominal + 3, f"a {nominal:.0f}px liner drew {width}px"


def test_the_liner_does_not_wobble():
    b = brush("liner")
    assert b.jitter == 0.0 and b.size_jitter == 0.0, \
        "at this size a jitter of two per cent of the canvas is the whole line"


def test_a_tip_mask_is_a_pure_function_of_its_arguments():
    """REVIEW.md finding 19, found by the goldens on their first run.

    The mask cache was keyed on the *rounded* radius while the mask was built from
    the exact one, so a brush at r=5.9 got whatever r=5.1 had built earlier in the
    process -- and what a script painted depended on what had run before it.
    """
    _MASK_CACHE.clear()
    fresh = tip_mask("round_hard", 5.9, 0.0, 0.9).copy()

    _MASK_CACHE.clear()
    tip_mask("round_hard", 5.1, 0.0, 0.9)          # poison the cache with a near radius
    after = tip_mask("round_hard", 5.9, 0.0, 0.9)
    assert np.array_equal(fresh, after), "the mask cache still depends on call history"


def test_the_same_script_paints_the_same_pixels_in_a_dirtied_process(tmp_path):
    """The determinism promise, stated at the level the painter cares about."""
    def paint():
        s = make(tmp_path)
        s.block_in("upper-half", color="burnt_umber", density=0.8, size=0.13)
        s.stroke([(0.1, 0.7), (0.5, 0.75), (0.9, 0.68)], "bristle", "yellow_ochre",
                 size=0.061)
        return s.canvas.to_srgb8()

    first = paint()
    for r in (3.3, 7.7, 11.1, 19.9):
        tip_mask("bristle", r, 0.4, 0.65, aspect=0.3)
    assert np.array_equal(first, paint())


def test_the_area_overlay_can_be_redrawn_after_a_correction(tmp_path, reference):
    """Merge changes the map. The picture of the map has to change with it."""
    s = make(tmp_path)
    prep = s.prepare(reference, level="medium")
    first = prep.overlay_path.read_bytes()

    a, b = prep.numbers[0], prep.numbers[1]
    prep.merge(a, b)
    s.look_areas(reference)
    assert prep.overlay_path.read_bytes() != first, \
        "the overlay still shows a map the table no longer describes"


def test_undo_takes_back_the_first_line_too(tmp_path):
    """The snapshot before the first pencil line has no drawing in it, and 'no
    drawing' has to mean *erase*, not 'leave whatever is there'."""
    s = make(tmp_path)
    s.pencil([(0.2, 0.5), (0.8, 0.5)], pressure=0.9)
    assert s.canvas.has_sketch
    s.undo(1)
    assert not s.canvas.has_sketch, "undo left the first pencil line on the canvas"
    assert float(s.canvas.sketch.max()) == 0.0


# --------------------------------------------------------------------------------------
# What the M6 final pass found: three fresh sessions, in rehearsal3/
# --------------------------------------------------------------------------------------
def test_erase_takes_the_line_out_of_sketch_lines_too(tmp_path):
    """REHEARSAL3, assisted run: erase cleared the graphite and left the record.

    So a painter who rubbed a line out and then re-laid the drawing from
    ``sketch_lines()`` -- the documented way to recover a drawing a block-in has
    buried -- silently resurrected exactly the lines it had decided were wrong.
    """
    s = make(tmp_path)
    s.pencil([(0.05, 0.5), (0.45, 0.5)])
    s.pencil([(0.55, 0.5), (0.95, 0.5)])
    s.erase(Region(0.0, 0.0, 0.5, 1.0))

    lines = s.sketch_lines()
    assert len(lines) == 1, "sketch_lines still hands back a line that was erased"
    assert min(x for x, _ in lines[0]) > 0.5


def test_erase_cuts_a_line_that_only_crosses_the_region(tmp_path):
    """The pieces outside survive, cut at the region's edge, and undo restores them."""
    s = make(tmp_path)
    s.pencil([(0.05, 0.5), (0.95, 0.5)])
    s.erase(Region(0.4, 0.0, 0.6, 1.0))

    pieces = s.sketch_lines()
    assert len(pieces) == 2, "a line crossing the erased band came back whole"
    assert pieces[0][-1][0] == pytest.approx(0.4, abs=1e-4)
    assert pieces[1][0][0] == pytest.approx(0.6, abs=1e-4)

    s.undo(1)
    assert len(s.sketch_lines()) == 1, "undo did not put the erased line back"


def test_block_in_sweeps_at_an_angle_the_named_directions_cannot_reach(tmp_path):
    """The human's note on the M6 pass: every mass came out of a horizontal or
    vertical sweep, so every mass had the canvas's own edges. A hillside wants its
    own axis, and 28 degrees is not one of the four names."""
    def paint(direction):
        s = make(tmp_path)
        s.block_in(Region(0.2, 0.2, 0.8, 0.8, "mass"), "flat", "burnt_umber",
                   direction=direction, size=0.13)
        return s.canvas.to_srgb8(impasto=False), s.stroke_count

    flat_rgb, flat_n = paint("horizontal")
    angled_rgb, angled_n = paint(28)
    assert angled_n > 0
    assert not np.array_equal(flat_rgb, angled_rgb), \
        "block_in(direction=28) laid the same marks as the horizontal sweep"

    crossed_rgb, crossed_n = paint((28, 118))
    assert crossed_n > angled_n, "a sequence of angles did not lay one pass each"
    assert not np.array_equal(crossed_rgb, angled_rgb)


def test_the_named_block_in_directions_still_paint_exactly_what_they_did(tmp_path):
    """Angles are additive. Every painting made before them has to replay unchanged,
    which is also what keeps the golden images honest."""
    def paint(direction):
        s = make(tmp_path)
        s.block_in("center", "bristle", "burnt_umber", direction=direction, size=0.12)
        return s.canvas.to_srgb8(impasto=False)

    assert np.array_equal(paint("cross"), paint(["horizontal", "vertical"])), \
        "'cross' stopped meaning a horizontal pass and then a vertical one"


def test_compare_separates_cells_no_paint_can_reach(tmp_path, reference):
    """The split still has to work for what is left below the floor after M6b.

    It was built (finding 21) because the palette floored at 0.23 and a lamp-lit
    photograph has whole masses under that. M6b took the floor down to the model's
    own, so an ordinary dark cell is now the painter's work again -- but a
    photograph can still hold a few cells below anything a pigment reaches, and
    those must not be reported as strokes worth spending.
    """
    s = make(tmp_path)
    dark = Image.new("RGB", (480, 360), (3, 3, 3))
    dark_path = tmp_path / "dark.png"
    dark.save(dark_path)

    c = s.compare(dark_path)
    assert c.floor == pytest.approx(s.palette.darkest_value)
    assert c.unreachable, "a near-black reference reported nothing out of reach"
    assert len(c.fixable) + len(c.unreachable) == len(c.off)
    assert all(cell.ref < c.floor - c.threshold for cell in c.unreachable)
    assert "cannot be painted" in c.table()

    # And a reference the palette can reach must not be written off as impossible.
    assert not s.compare(reference).unreachable


def test_a_shadow_a_photograph_would_hold_is_now_the_painters_own_work(tmp_path):
    """The M6b criterion, as a test.

    Before M6b a cell at value 0.10 -- an ordinary lamp-lit shadow, nothing
    exotic -- was below anything a stroke could reach, and `compare()` had to
    excuse it. Two fresh sessions each spent about twenty-five strokes finding
    that out (finding 21). It has to be reachable now, or the darks did not move
    far enough to matter.
    """
    s = make(tmp_path)
    shadow = Image.new("RGB", (480, 360), (25, 25, 25))     # value 0.098
    shadow_path = tmp_path / "shadow.png"
    shadow.save(shadow_path)

    c = s.compare(shadow_path)
    assert not c.unreachable, (
        "a lamp-lit shadow is still being written off as unpaintable; "
        f"floor {c.floor:.3f}"
    )


def test_the_palette_floor_is_the_models_own_and_not_the_swatches(tmp_path):
    """M6b: the box bottoms out where the *engine* does, not where the swatches did.

    The reflectance floor in `color.py` is 0.01 linear, which is value 0.10 -- the
    darkest neutral this model can represent at all. Before M6b the palette stopped
    0.13 above it, because mixing never goes below the darkest ingredient and the
    darkest ingredient was a chart swatch rather than a masstone. The remaining gap
    is the hue the pigments still carry: a coloured dark cannot sit on the floor in
    all three channels at once, and pigments with no hue left would break the
    mixtures findings 5 and 6 protect.
    """
    s = make(tmp_path)
    floor = s.palette.darkest_value
    assert 0.10 < floor < 0.15, f"palette floor {floor:.3f}"
    assert floor == pytest.approx(
        min(s.palette.value_of(n) for n in set(s.palette.pigment_names))
    )

    # The mixture that is the whole point of a box without black.
    mixed = s.palette.value_of(s.palette.mix("ultramarine", "burnt_umber", 0.5))
    assert mixed < 0.15, f"ultramarine + burnt umber reads {mixed:.3f}, not a dark"


def test_the_dark_swatches_state_a_colour_the_engine_can_lay(tmp_path):
    """A channel below the reflectance floor renders as the floor.

    So a swatch written darker than 0.01 linear would claim a colour no stroke can
    put down, and `value_of` would disagree with the canvas. Finding 5 asks only
    that no channel is zero; the darks, which is where the floor bites, are held to
    the stronger rule.
    """
    from easel.color import _FLOOR, parse_color
    from easel.palette import PIGMENTS

    for name, hexval in PIGMENTS.items():
        assert float(parse_color(hexval).min()) > 0.0, f"{name} has a zero channel"

    for name in ("burnt_umber", "ultramarine", "alizarin",
                 "burnt_sienna", "viridian", "cerulean"):
        lowest = float(parse_color(PIGMENTS[name]).min())
        assert lowest >= float(_FLOOR), (
            f"{name} states {PIGMENTS[name]}, whose lowest channel {lowest:.4f} is "
            f"under the {float(_FLOOR)} reflectance floor and renders lighter"
        )
