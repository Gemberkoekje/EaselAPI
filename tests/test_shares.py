"""Step 6 of 0.9.0, workstream F: a share of the budget for each part of a picture.

As the painter of Uktarl's Room chose (``paintings/Claude/uktarl_krannoc/answers.md``, E):
**of the budget, not of the marks so far**. After Uktarl's head his 102 marks were 48% of
the 212 laid, and the ``subject:`` line said so against 30% planned; of the budget he had
23%. The last of four figures was painted at 22 strokes against the 45 it would have been
given, with 40 in hand -- *a line saying "near bandit: 22 of 45" at the end would have sent
them there*.

``s.plan(shares={part: share})``, a part being the marks whose ``note=`` holds its name,
the longer name winning where two do (the owner's choice, through the plan); a standing
``shares:`` line, each part's strokes against its share of the budget.
"""

from __future__ import annotations

import json
import warnings

import pytest

from easel import Session
from easel.cli import main
from easel.plan import Plan


def make(tmp_path, budget: int | None = 40) -> Session:
    return Session(480, 320, texture="linen", ground="toned_grey", seed=7, out_dir=tmp_path,
                   timelapse=False, budget=budget)


def lay(s: Session, n: int, note: str = "", y: float = 0.2) -> None:
    """``n`` hand-laid strokes, one record each, all carrying ``note``."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for i in range(n):
            s.stroke([(0.1, y + i * 0.01), (0.6, y + i * 0.01)], "bristle", "burnt_umber",
                     size=0.02, note=note)


def shares_line(text: str) -> str:
    found = [line.strip() for line in text.splitlines() if line.strip().startswith("shares:")]
    return found[0] if found else ""


# -- the line --------------------------------------------------------------------------------
def test_each_part_against_its_share_of_the_budget_not_of_the_marks_so_far(tmp_path):
    """The painter's split, on a budget of 40: the subject laid first has every mark so
    far, and the line says how much of *its share of the budget* that is."""
    s = make(tmp_path)
    s.plan(shares={"uktarl": 0.25, "the near bandit": 0.10})
    lay(s, 6, "uktarl")
    said = shares_line(s.report(since=0))
    assert said == "shares: uktarl 6 of 10, the near bandit 0 of 4"
    lay(s, 5, "the near bandit", y=0.6)
    said = shares_line(s.report(since=6))
    assert said == "shares: uktarl 6 of 10, the near bandit 5 of 4 (over)"


def test_a_part_is_the_name_in_the_note_and_the_longer_name_wins(tmp_path):
    """In any case, anywhere in the note, as the ``subject:`` line reads ``subject`` -- so
    a block-in's own note, *block-in Uktarl's body*, is Uktarl's -- and where two names
    are in one note, the longer: *the near bandit's hood* is not the bandit's too."""
    s = make(tmp_path)
    s.plan(shares={"bandit": 0.2, "near bandit": 0.1, "Uktarl": 0.25})
    lay(s, 2, "UKTARL: the wig")
    lay(s, 3, "the near bandit's hood", y=0.5)
    lay(s, 1, "the bandit at the left", y=0.7)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s.block_in(s.circle((0.8, 0.5), 0.05, name="Uktarl's hand"), "bristle",
                   "burnt_umber", size=0.03)
    hand = sum(1 for r in s.history.records if "hand" in r.note)
    assert hand >= 1 and all("Uktarl's hand" in r.note
                             for r in s.history.records[6:])
    said = shares_line(s.report(since=0))
    over = " (over)" if 2 + hand > 10 else ""
    assert said == f"shares: bandit 1 of 8, near bandit 3 of 4, Uktarl {2 + hand} of 10{over}"
    assert s.plan().part_of("") is None and s.plan().part_of("the sky") is None


def test_marks_in_no_part_are_counted_and_a_signature_is_in_none(tmp_path):
    s = make(tmp_path)
    s.plan(shares={"the figure": 0.5})
    lay(s, 3, "the figure")
    lay(s, 2, "", y=0.5)
    lay(s, 2, "signature", y=0.8)
    assert shares_line(s.report(since=0)) == "shares: the figure 3 of 20; 2 in no part"


def test_rounded_to_a_stroke_as_the_painter_rounded_its_own_split(tmp_path):
    """The painter's table: 25% of 450 is 112, 11% is 50, 10% is 45, 5% is 22."""
    s = make(tmp_path, budget=450)
    s.plan(shares={"uktarl": 0.25, "the lady": 0.11, "the near bandit": 0.10,
                   "the floor": 0.05})
    lay(s, 1, "uktarl")
    assert shares_line(s.report(since=0)) == (
        "shares: uktarl 1 of 112, the lady 0 of 50, the near bandit 0 of 45, "
        "the floor 0 of 22")


def test_a_standing_line_said_on_change_and_every_time_at_the_end(tmp_path):
    """A standing line, as step 5 built them: over a pass it prints when it changed, and
    the closing checklist and an audit print it whatever."""
    s = make(tmp_path)
    s.plan(shares={"the figure": 0.5})
    lay(s, 2, "the figure")
    first = s.report(since=0)
    assert "shares: the figure 2 of 20" in first
    here = len(s.history.records)
    assert "shares" in s.report(since=here).split("unchanged:")[1]
    lay(s, 1, "the figure")
    assert "shares: the figure 3 of 20" in s.report(since=here)
    assert "shares: the figure 3 of 20" in s.checklist()
    assert "shares: the figure 3 of 20" in s.report()


def test_no_shares_no_line(tmp_path):
    s = make(tmp_path)
    lay(s, 2, "the figure")
    assert "shares:" not in s.report(since=0) and "shares:" not in s.checklist()


# -- the declaration ---------------------------------------------------------------------------
def test_what_a_share_is_and_what_it_is_not(tmp_path):
    s = make(tmp_path)
    with pytest.raises(ValueError, match="adds up to 120%"):
        s.plan(shares={"a": 0.7, "b": 0.5})
    with pytest.raises(ValueError, match="not 25"):
        s.plan(shares={"a": 25})
    with pytest.raises(ValueError, match="not '25%'"):
        s.plan(shares={"a": "25%"})
    with pytest.raises(ValueError, match="cannot tell apart"):
        s.plan(shares={"Uktarl": 0.2, "uktarl": 0.1})
    with pytest.raises(ValueError, match="no name"):
        s.plan(shares={" ": 0.2})
    with pytest.raises(TypeError, match="dict of parts"):
        s.plan(shares=[("a", 0.2)])
    assert not s.plan().shares, "a refused declaration declares nothing"
    s.plan(shares={"a": 0.6, "b": 0.4})
    assert s.plan().shares == (("a", 0.6), ("b", 0.4)), "all of it is allowed"


def test_shares_divide_a_budget_so_a_painting_without_one_is_told(tmp_path):
    s = make(tmp_path, budget=None)
    with pytest.raises(ValueError, match="budget=450"):
        s.plan(shares={"the figure": 0.3})


def test_kept_with_the_rest_of_the_plan_and_cleared_with_the_empty_version(tmp_path):
    s = make(tmp_path)
    s.plan(why="a figure in a doorway", shares={"the figure": 0.3, "the door": 0.2})
    s.plan(key="low")
    assert s.plan().shares == (("the figure", 0.3), ("the door", 0.2))
    assert "shares of the budget: the figure 30%, the door 20%" in str(s.plan())
    s.plan(shares={})
    assert not s.plan().shares and s.plan().why == "a figure in a doorway"


def test_saved_in_the_file_and_an_older_file_opens_without_them(tmp_path):
    s = make(tmp_path)
    s.plan(shares={"the figure": 0.3})
    lay(s, 1, "the figure")
    path = tmp_path / "p.easel"
    s.save(path)
    back = Session.load(path)
    assert back.plan().shares == (("the figure", 0.3),)
    assert "shares: the figure 1 of 12" in back.checklist()

    plan = json.loads(json.dumps(s.plan().to_json()))
    assert plan["shares"] == [["the figure", 0.3]]
    assert Plan.from_json({k: v for k, v in plan.items() if k != "shares"}).shares == ()
    assert Plan.from_json(dict(plan, shares=[["ok", 0.2], "junk", [1]])).shares == (
        ("ok", 0.2),), "an entry this build cannot read is dropped, as a key is"


def test_easel_plan_declares_shares_from_the_shell(tmp_path, capsys):
    session = tmp_path / "p.easel"
    assert main(["new", str(session), "--size", "320x240", "--budget", "200",
                 "--out-dir", str(tmp_path / "out")]) == 0
    assert main(["plan", str(session), "--share", "the figure", "0.3",
                 "--share", "the wall", "0.25"]) == 0
    assert "shares of the budget: the figure 30%, the wall 25%" in capsys.readouterr().out
    assert Session.load(session).plan().shares == (("the figure", 0.3), ("the wall", 0.25))
    assert main(["plan", str(session), "--share", "the figure", "a third"]) != 0
    assert "--share 'the figure' 0.30" in capsys.readouterr().err
