"""Step 7 of 0.9.0, workstream H: a light in a picture that is dark on purpose.

As the painter of Uktarl's Room chose (``paintings/Claude/uktarl_krannoc/answers.md``, G):
**H1 and H2, not H3**. H1 is the documents' -- *a picture is low-key while its top
twentieth stays under the box's middle* said where ``key=`` is introduced, which the
painter read as ``nothing above 0.35``, the row's example. H2 is the line's: with no key
declared, where the ``values:`` line says *no clear light* and the plan names a light that
stands ``0.10`` clear of everything else, it says so and names ``key="low"``. Nothing is
silenced; the key stays a declaration that buys a question (0.8.0's ruling).
"""

from __future__ import annotations

import warnings

import numpy as np

from easel import Session, docs, span
from easel.checklist import values_line

#: A dark picture: nothing above 0.40 at its top twentieth, against a box whose middle
#: is 0.545, said 0.54.
DARK = np.linspace(0.15, 0.40, 40000, dtype=np.float32).reshape(200, 200)
REACH = (0.13, 0.96)
NAMED = "s.plan(key='low') if the picture is dark on purpose"


def test_no_key_and_a_light_that_stands_clear_names_the_light_and_the_key():
    said = values_line(DARK, reach=REACH, light=("Uktarl's face", 0.69, 0.50))
    assert said.endswith(
        "; no clear light -- nothing above 0.39, and the box's own middle is 0.54; "
        "Uktarl's face stands clear -- 0.69 at its brightest twentieth against 0.50 for "
        "everything else, 0.19 over: say s.plan(key='low') if the picture is dark on "
        "purpose"), said


def test_a_light_that_does_not_stand_clear_adds_nothing():
    """*No clear light* is then the whole of it, as before."""
    plain = values_line(DARK, reach=REACH)
    assert values_line(DARK, reach=REACH, light=("lamp", 0.45, 0.40)) == plain
    assert values_line(DARK, reach=REACH, light=("lamp", 0.30, 0.40)) == plain
    assert values_line(DARK, reach=REACH, light=None) == plain


def test_only_beside_no_clear_light():
    """A picture with its light is told so, whatever the plan names; a declared key asks
    its own question."""
    lit = np.linspace(0.15, 0.90, 40000, dtype=np.float32).reshape(200, 200)
    assert NAMED not in values_line(lit, reach=REACH, light=("lamp", 0.95, 0.80))
    low = values_line(DARK, reach=REACH, key="low", light=("lamp", 0.69, 0.50))
    assert NAMED not in low and "low-key, as the plan says" in low
    assert "lamp stands clear -- 0.69" in low
    assert NAMED not in values_line(DARK, reach=REACH, key="high",
                                    light=("lamp", 0.69, 0.50))


def make(tmp_path) -> Session:
    return Session(320, 240, texture="linen", ground="toned_grey", seed=7, out_dir=tmp_path,
                   timelapse=False)


def paint_dark_room(s: Session) -> None:
    room, lamp = span("A1", "H8"), span("D4", "D4")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s.block_in(room, "flat", s.palette.at_value("burnt_umber", 0.18, light="white"),
                   direction="axis", solid=True)
        s.block_in(lamp, "flat", s.palette.at_value("ochre", 0.80), direction="axis",
                   edge="hard", solid=True)


def values_of(text: str) -> str:
    found = [ln.strip() for ln in text.splitlines() if ln.strip().startswith("values:")]
    return found[0] if found else ""


def test_on_a_painting_the_line_reads_the_light_the_plan_names(tmp_path):
    """The light read off the plan's view, as the `lightest:` line reads it, and the key
    it names, declared, turns the clause into the key's own question."""
    s = make(tmp_path)
    lamp = span("D4", "D4")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s.plan(values={span("A1", "H8"): 0.18, lamp: 0.80}, lightest=lamp)
    paint_dark_room(s)
    line = values_of(s.report(since=0))
    assert "no clear light" in line and "D4 stands clear --" in line and NAMED in line, line
    s.plan(key="low")
    line = values_of(s.checklist())
    assert "low-key, as the plan says" in line and "D4 stands clear --" in line, line
    assert NAMED not in line


def test_with_no_light_named_the_line_is_as_it_was(tmp_path):
    s = make(tmp_path)
    paint_dark_room(s)
    line = values_of(s.report(since=0))
    assert "no clear light" in line and "stands clear" not in line, line


def test_the_card_and_the_reference_say_what_counts_as_low_key():
    """H1. The painter read the reference's example, *nothing above 0.35*, as the rule;
    the rule was in the same row only as the condition for leaving the key. Rule first,
    where `key=` is introduced: on the card, and at the head of the reference's row."""
    rule = "top twentieth stays under the box's middle"
    assert rule in " ".join(docs.front_page().split())
    rows = [ln for ln in docs.read("reference").splitlines()
            if ln.startswith('| `key="low"`')]
    assert len(rows) == 1 and rule in rows[0].split("|")[2][:160], rows
