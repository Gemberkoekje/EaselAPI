"""Step 5 of 0.9.0: the check -- a habit declared in a place, and lines said on change.

As the painter of Uktarl's Room chose (``paintings/Claude/uktarl_krannoc/answers.md``,
C, and ``answers-step2.md``, 3b, 4a, 7a, 7b and 8):

- **the disc rule as it is**, with a habit declared **per place**: inside the places a
  plan names, small round marks are counted with the painter's reason instead of warned
  about, and the closing checklist quotes every reason back;
- **the pass rule leaves a signature out**, as the closing audit always has;
- **a standing line only when it changes**, against the painting as committed, the
  lines left out named on one line; an audit and the closing checklist print them all.
"""

from __future__ import annotations

import json
import warnings

import pytest

from easel import Session, ellipse, polygon
from easel.cli import main
from easel.plan import Plan

FACE = ellipse((0.30, 0.50), 0.08, 0.10, name="the face")
CARDS = polygon([(0.55, 0.70), (0.70, 0.70), (0.70, 0.85), (0.55, 0.85)], name="the cards")
#: Four features inside the face, and three dots in a row well away from it.
FEATURES = [(0.28, 0.48), (0.32, 0.48), (0.30, 0.53), (0.31, 0.55)]
ROW = [(0.80, 0.20), (0.83, 0.20), (0.86, 0.20)]


def make(tmp_path, w: int = 480, h: int = 320) -> Session:
    return Session(w, h, texture="linen", ground="toned_grey", seed=7, out_dir=tmp_path,
                   timelapse=False)


def dots(s: Session, where, **kw) -> None:
    """Small round dabs at tip_wobble=0 -- one disc each -- at the places given."""
    for x, y in where:
        s.dab(x, y, "round_hard", "titanium_white", size=0.012, press=3, **kw)


def ground(s: Session) -> None:
    """A mass over the whole canvas, so the standing lines have paint to read."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s.block_in((0.0, 0.0, 1.0, 1.0), "bristle", "burnt_umber", size=0.1)


# -- the signature ------------------------------------------------------------------------
def test_the_pass_rule_leaves_a_signature_out_as_the_closing_audit_does(tmp_path):
    """Answer 8: ``p17_finish.py``'s report named records 425 to 428, all four noted
    ``signature``, as one disc printed four times. The closing checklist has always left
    signatures out; the pass rule now does too."""
    s = make(tmp_path)
    dots(s, [(0.86, 0.92), (0.89, 0.92), (0.92, 0.92), (0.95, 0.92)], note="signature")
    assert "one disc printed" not in s.report(since=0)
    dots(s, ROW)
    assert "one disc printed 3 times" in s.report(since=4)


# -- a habit declared in a place -----------------------------------------------------------
def test_a_declared_place_counts_its_discs_with_the_reason_and_warns_nowhere_else(tmp_path):
    """Per place, not per painting (answer C): the faces and the fan of cards, and not
    the candle or the relief, where a disc printed over and over is the real risk."""
    s = make(tmp_path)
    s.plan(habits={"disc": {FACE: "the features of a face", CARDS: "the fan of cards"}})
    dots(s, FEATURES)
    said = s.report(since=0)
    assert "one disc printed" not in said
    assert "nothing to report" in said, "a declared count is not a thing to look at"
    assert ("discs declared: 4 in the face ('the features of a face') -- counted, not "
            "warned about, as the plan says") in said
    assert "the cards" not in said, "a pass says only the places it laid discs in"

    dots(s, ROW)
    said = s.report(since=4)
    assert "one disc printed 3 times" in said
    assert "discs declared" not in said

    # Both in one pass: the rule counts only what lies outside every declared place.
    before = len(s.history.records)
    dots(s, FEATURES[:2] + ROW)
    said = s.report(since=before)
    assert "one disc printed 3 times" in said and "2 in the face" in said


def test_the_closing_checklist_quotes_every_reason_back(tmp_path):
    """As it quotes ``why``: every place declared, one nothing fell in included."""
    s = make(tmp_path)
    s.plan(habits={"disc": {FACE: "the features of a face", CARDS: "the fan of cards"}})
    dots(s, FEATURES)
    said = s.checklist()
    assert ("discs declared: 4 in the face ('the features of a face'), 0 in the cards "
            "('the fan of cards')") in said
    assert "one disc printed" not in said
    assert "discs declared: 4 in the face" in s.report(), "the audit says it too"


def test_a_disc_is_in_a_place_by_the_middle_of_its_path(tmp_path):
    """One point a mark, the one the closing audit already groups discs by: a mark is in
    one place, never half in two."""
    s = make(tmp_path)
    left = polygon([(0.1, 0.1), (0.5, 0.1), (0.5, 0.9), (0.1, 0.9)], name="left")
    s.plan(habits={"disc": {left: "on purpose"}})
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for y in (0.3, 0.4, 0.5):
            # Each runs from inside the place to outside it; its middle is outside.
            s.stroke([(0.46, y), (0.58, y)], "round_hard", "titanium_white", size=0.019)
    said = s.report(since=0)
    assert "one disc printed 3 times" in said and "discs declared" not in said


def test_habits_take_a_place_and_a_reason_and_refuse_the_rest(tmp_path):
    s = make(tmp_path)
    with pytest.raises(ValueError, match="bands='subject'"):
        s.plan(habits={"bars": {FACE: "the water"}})
    with pytest.raises(ValueError, match="no reason"):
        s.plan(habits={"disc": {FACE: ""}})
    with pytest.raises(ValueError, match="Per place"):
        s.plan(habits={"disc": "the features of four faces"})
    with pytest.raises(TypeError, match="dict of habits"):
        s.plan(habits=["disc"])
    with pytest.raises(ValueError, match="covers no pixels"):
        s.plan(habits={"disc": {ellipse((0.5, 0.5), 0.0005, 0.0005): "nowhere"}})
    assert not s.plan().habits, "nothing refused was declared"

    # A cell or a span names a place, as a value plan's keys do.
    held = s.plan(habits={"disc": {"C3:D4": "a face"}})
    assert [h.place.name for h in held.habits] == ["C3:D4"]
    assert "habit: disc in C3:D4 -- 'a face'" in str(held)


def test_habits_are_kept_in_the_file_changed_alone_and_cleared(tmp_path):
    s = make(tmp_path)
    s.plan(why="three bandits at cards", habits={"disc": {FACE: "the features"}})
    s.plan(key="low")
    assert s.plan().habits and s.plan().key == "low", "another field keeps the habits"
    path = s.save(tmp_path / "p.easel")
    back = Session.load(path).plan()
    assert back == s.plan()
    assert back.habits[0].place.outline.points == FACE.points
    s.plan(habits={})
    assert not s.plan().habits and s.plan().why == "three bandits at cards"


def test_a_habit_this_build_cannot_name_is_dropped_on_load():
    """As an unknown key is: a plan written by a later Easel loads as what this one
    knows, and its disc rule warns where the later one counted."""
    data = Plan(habits=()).to_json()
    face = {"name": "f", "points": [[0.1, 0.1], [0.2, 0.1], [0.2, 0.2]], "value": None}
    data["habits"] = [{"habit": "disc", "reason": "a face", "place": face},
                      {"habit": "glints", "reason": "water", "place": face},
                      {"habit": "disc", "reason": "broken"}]
    habits = Plan.from_json(json.loads(json.dumps(data))).habits
    assert [(h.habit, h.reason) for h in habits] == [("disc", "a face")]


# -- the standing lines, on change ---------------------------------------------------------
def _standing(text: str) -> dict[str, str]:
    return {line.strip().split(":", 1)[0]: line.strip() for line in text.splitlines()
            if line.startswith("  ") and not line.startswith(("  -", "    "))}


def test_a_pass_prints_the_standing_lines_that_changed_and_names_the_rest(tmp_path):
    """Answer 7a and 7b: 61% of the painter's standing lines, and 40% of the corpus's,
    were the line before word for word. A pass prints those that changed; the others
    are named on one line, so a missing line never reads as one not measured."""
    s = make(tmp_path)
    ground(s)
    first = _standing(s.report(since=0))
    assert {"values", "edges", "ground"} <= set(first) and "unchanged" not in first

    before = len(s.history.records)
    dots(s, FEATURES)
    second = _standing(s.report(since=before))
    full = _standing(s.report())
    assert set(second) - {"unchanged"} <= set(full)
    named = second["unchanged"].split(": ", 1)[1].split(", ")
    assert named and all(full[label] == first[label] for label in named)
    assert all(full[label] != first.get(label) for label in second
               if label != "unchanged")
    # An audit and the closing checklist print every line.
    assert "unchanged" not in full and {"values", "edges", "ground"} <= set(full)
    assert "unchanged:" not in s.checklist()


def test_a_pass_with_nothing_changed_says_so_in_one_line(tmp_path):
    s = make(tmp_path)
    ground(s)
    s.report(since=0)
    here = len(s.history.records)
    # A pass that lays nothing: every standing line is the one before.
    said = s.report(since=here)
    assert said.splitlines()[-1].startswith("  unchanged: ")
    assert "values:" not in said and "edges:" not in said


def test_a_reading_from_another_record_is_not_the_painting_the_pass_opened_on(tmp_path):
    """An undo, or a pass nobody reported, leaves the last reading about a painting the
    pass did not open on: every line prints."""
    s = make(tmp_path)
    ground(s)
    s.report(since=0)
    dots(s, ROW)                                      # laid, never reported
    here = len(s.history.records)
    dots(s, FEATURES)
    assert "unchanged:" not in s.report(since=here)


def test_a_rehearsal_is_compared_against_the_painting_as_committed(tmp_path, capsys):
    """Answer 7a: a pass rehearsed two to four times wants each version to say what it
    would change on the painting, not what changed since the version thrown away. And
    the reading is kept in the file, since the shell loads it once a pass."""
    session = tmp_path / "p.easel"
    assert main(["new", str(session), "--size", "320x240", "--out-dir",
                 str(tmp_path / "out")]) == 0
    base = tmp_path / "base.py"
    base.write_text("s.block_in((0, 0, 1, 1), 'bristle', 'burnt_umber', size=0.1)\n")
    light = tmp_path / "light.py"
    light.write_text("s.block_in((0.1, 0.1, 0.5, 0.5), 'flat', 'titanium_white', "
                     "size=0.06)\n")
    small = tmp_path / "small.py"
    small.write_text("s.dab(0.9, 0.9, 'round_hard', 'burnt_umber', size=0.01)\n")
    assert main(["run", str(session), str(base)]) == 0
    capsys.readouterr()
    assert Session.load(session)._standing is not None, "the reading is saved"

    def rehearse(script) -> dict[str, str]:
        assert main(["run", str(session), str(script), "--rehearse"]) == 0
        return _standing(capsys.readouterr().out)

    lit = rehearse(light)
    assert "values" in lit, "a light block moves the values"
    # Rehearsed after it, a pass that changes little is compared against the
    # painting as committed -- not against the light it never had.
    quiet = rehearse(small)
    assert "values" not in quiet and "values" in quiet["unchanged"]
    assert rehearse(light) == lit, "the same rehearsal says the same thing again"


def test_easel_plan_declares_a_habit_from_the_shell(tmp_path, capsys):
    session = tmp_path / "p.easel"
    assert main(["new", str(session), "--size", "320x240", "--out-dir",
                 str(tmp_path / "out")]) == 0
    assert main(["plan", str(session), "--habit", "disc", "C3:D4", "the features of a face",
                 "--habit", "disc", "F6", "the fan of cards"]) == 0
    assert "habit: disc in F6 -- 'the fan of cards'" in capsys.readouterr().out
    held = Session.load(session).plan().habits
    assert [(h.place.name, h.reason) for h in held] == [
        ("C3:D4", "the features of a face"), ("F6", "the fan of cards")]
    assert main(["plan", str(session), "--habit", "bars", "A1", "water"]) != 0
    assert "bands='subject'" in capsys.readouterr().err


def test_a_pass_that_raised_printed_no_lines_so_none_are_unchanged_after_it(tmp_path, capsys):
    """A committed pass that raises is saved with what it laid, and prints the error, not
    its check: the next pass is not told *unchanged* about lines nobody read."""
    session = tmp_path / "p.easel"
    assert main(["new", str(session), "--size", "320x240", "--out-dir",
                 str(tmp_path / "out")]) == 0
    base = tmp_path / "base.py"
    base.write_text("s.block_in((0, 0, 1, 1), 'bristle', 'burnt_umber', size=0.1)\n")
    broken = tmp_path / "broken.py"
    broken.write_text("s.block_in((0.1, 0.1, 0.5, 0.5), 'flat', 'titanium_white', "
                      "size=0.06)\nraise RuntimeError('stopped')\n")
    nothing = tmp_path / "nothing.py"
    nothing.write_text("pass\n")
    assert main(["run", str(session), str(base)]) == 0
    assert main(["run", str(session), str(broken)]) != 0
    capsys.readouterr()
    assert main(["run", str(session), str(nothing)]) == 0
    said = _standing(capsys.readouterr().out)
    assert "unchanged" not in said and {"values", "edges", "ground"} <= set(said)
    # And from there, as ever, a pass that changes nothing says so in one line.
    assert main(["run", str(session), str(nothing)]) == 0
    assert set(_standing(capsys.readouterr().out)) == {"unchanged"}
