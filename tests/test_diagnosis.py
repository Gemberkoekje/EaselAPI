"""`DIAGNOSIS.md` against the documents it indexes, and against the command that reads it.

An index is a promise that following a pointer lands somewhere. It carries no content
of its own -- every row is a symptom and a location -- so the only way it can be wrong
is to point at a heading that has moved or gone, and that is a silent failure: the
painter reading it is already stuck, and a dead pointer costs them the rehearsal the
index was written to save. An index that has drifted is worse than none, for the same
reason `REFERENCE.md` is tested against the engine rather than read against it.

The size cap is the other half. This file exists because the guide is long; it stops
being worth having the moment it starts explaining anything, and a cap is the only
mechanism this repository has found that holds a document to its job. Over it, the fix
is to cut rows, never to raise the number.

Since `easel diagnose` the promise is stronger, and so are these tests. The pointer is
no longer something a painter follows -- the tool follows it and hands back the passage
-- so a heading that has moved is not a dead link in prose, it is a command that answers
with an apology. `test_every_pointer_comes_back_as_a_passage` is the one that matters
now: it does what the command does, to all 92 of them.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from easel import diagnosis, docs
from easel.cli import main

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "DIAGNOSIS.md"

INDEXED = ("PAINTER.md", "PAINTING.md", "RECIPES.md", "REFERENCE.md", "CALIBRATION.md")

#: A pointer is `FILE.md` -> *Heading*, and the heading is matched as a prefix so a row
#: can name a section without repeating all of it.
#:
#: The arrow is ASCII because the file ships in the wheel now, and `->` is what this
#: project spells a rightwards arrow: U+2192 is outside cp1252, so 92 of them made
#: `print(easel.docs.read("diagnosis"))` die on a Windows console. See
#: `tests/test_guide.py::test_a_shipped_document_prints_on_a_cp1252_console`.
POINTER = re.compile(r"`([A-Z]+\.md)`\s*->\s*\*([^*]+)\*")

#: Rows on this page are `| symptom | pointers |` and nothing else.
ROW = re.compile(r"^\|(?!-)(.+)\|(.+)\|\s*$", re.M)

MAX_LINES = 130


def _norm(text: str) -> str:
    return re.sub(r"[`*]", "", text).strip().casefold()


def _headings(name: str) -> list[str]:
    body = (ROOT / name).read_text(encoding="utf-8")
    return [_norm(h) for h in re.findall(r"^#{2,4} (.+)$", body, re.M)]


HEADINGS = {name: _headings(name) for name in INDEXED}
POINTERS = [
    (doc, heading)
    for doc, heading in POINTER.findall(INDEX.read_text(encoding="utf-8"))
]
ROWS = [
    (left, right)
    for left, right in ROW.findall(INDEX.read_text(encoding="utf-8"))
    if _norm(left) not in ("what you are looking at",)
]


def test_the_index_has_rows() -> None:
    """A guard on the two regexes above: if either stops matching, every other test
    in this file passes vacuously."""
    assert len(ROWS) > 40
    assert len(POINTERS) > 60


@pytest.mark.parametrize("doc, heading", sorted(set(POINTERS)))
def test_every_pointer_lands_on_a_heading(doc: str, heading: str) -> None:
    assert doc in HEADINGS, f"{doc} is not one of the indexed documents"
    wanted = _norm(heading)
    assert any(h.startswith(wanted) for h in HEADINGS[doc]), (
        f"DIAGNOSIS.md points at {doc} -> {heading!r}, which is not a heading there. "
        f"A heading has moved or been renamed; fix the pointer, not this test."
    )


@pytest.mark.parametrize("doc", INDEXED)
def test_every_indexed_document_is_reachable(doc: str) -> None:
    """A document nobody points at is a document this index does not cover, which is
    the failure that cannot be seen by following pointers."""
    assert (ROOT / doc).is_file()
    assert any(d == doc for d, _ in POINTERS), f"no row points into {doc}"


@pytest.mark.parametrize("left, right", ROWS)
def test_every_row_is_a_symptom_and_a_pointer(left: str, right: str) -> None:
    """The rule that keeps this an index. The left column describes what is on the
    canvas and the right column is pointers -- nothing on this page explains anything,
    because the moment it does it is a sixth copy of the guide."""
    assert _norm(left), "a row with no symptom in it"
    assert POINTER.search(right), f"row {left.strip()!r} has no pointer in it"


def test_the_index_does_not_point_at_itself() -> None:
    assert "DIAGNOSIS.md`" not in INDEX.read_text(encoding="utf-8").split("---", 1)[1]


def test_the_index_stays_one_screen() -> None:
    """See the docstring. Over the cap, cut rows."""
    lines = INDEX.read_text(encoding="utf-8").splitlines()
    assert len(lines) <= MAX_LINES, (
        f"DIAGNOSIS.md is {len(lines)} lines against a cap of {MAX_LINES}. "
        f"Cut rows rather than raising the cap -- it is the only thing holding this "
        f"file to being an index."
    )


# -- the index as something the engine reads -------------------------------------------
def test_the_index_ships_with_the_engine() -> None:
    """For three releases `grep -i rings DIAGNOSIS.md` was the whole interface, and it
    only worked from a checkout: the build shipped five documents and this was not one
    of them, so a painter who ran `pip install easel-paint` had no file to grep.

    `tests/test_guide.py` holds the other half -- that the wheel's force-include table
    and `docs.DOCUMENTS` name the same six files."""
    assert docs.DOCUMENTS["diagnosis"] == "DIAGNOSIS.md"
    assert docs.document_path("diagnosis").is_file()


def test_the_index_is_reachable_from_a_bare_import() -> None:
    """`REFERENCE.md` and `DIAGNOSIS.md` both tell a painter to call
    `easel.diagnosis.answer()`, and absence from `dir(easel)` is a claim -- it is how
    `easel.docs` spent two releases looking like something that did not exist.

    A subprocess for the reason `tests/test_guide.py` uses one: importing the module
    anywhere in this process binds the attribute for the rest of it, so the same
    assertion made in-process passes whether or not `__init__.py` imports it."""
    import subprocess
    import sys

    probe = (
        "import easel; "
        "assert 'diagnosis' in dir(easel), 'dir(easel) does not list diagnosis'; "
        "assert easel.diagnosis.answer('concentric rings').strip()"
    )
    done = subprocess.run([sys.executable, "-c", probe], capture_output=True, text=True)
    assert done.returncode == 0, done.stderr


def test_the_parser_finds_every_row_the_regex_does() -> None:
    """`easel.diagnosis` parses this file line by line and the tests above parse it
    with a regex. Two readings of one format, which is the point: a change to the
    file that only one of them survives shows up here rather than as a command that
    quietly stopped covering a third of the index."""
    assert len(diagnosis.rows()) == len(ROWS)
    assert sum(len(row.pointers) for row in diagnosis.rows()) == len(POINTERS)


def test_every_row_knows_which_section_it_is_under() -> None:
    """The group is what a painter gets handed when their words match nothing: it has
    to be the file's own `##` headings and not the empty string."""
    assert all(row.group for row in diagnosis.rows())
    assert "An edge" in {row.group for row in diagnosis.rows()}


@pytest.mark.parametrize("row", diagnosis.rows(), ids=lambda r: r.symptom[:50])
def test_every_pointer_comes_back_as_a_passage(row: diagnosis.Row) -> None:
    """The promise `easel diagnose` makes, done the way the command does it.

    `test_every_pointer_lands_on_a_heading` checks that the heading exists. This
    checks the rest of the journey -- prefix resolved to a real heading line, section
    sliced out of the document, something in it -- because that is what a painter now
    receives. A pointer that lands on a heading whose section comes back empty was a
    cosmetic fault when a person followed it and is a broken answer now.
    """
    for pointer in row.pointers:
        body = pointer.passage()
        assert len(body.split()) > 20, (
            f"{pointer.document} -> {pointer.heading!r} resolves to {len(body.split())} "
            f"words. The heading is there; the section under it is not."
        )


# -- matching --------------------------------------------------------------------------
@pytest.mark.parametrize("words, expected", [
    ("concentric rings", "A glow with visible concentric rings"),
    ("a staircase along a boundary", "A staircase along a boundary"),
    ("thumbprint", "A thumbprint at the end of a smudge"),
    ("the ground shows through in flecks", "A mottled field with the ground showing"),
    ("every edge is equally sharp", "Every edge equally sharp"),
    ("a mechanical straight line", "A mechanical straight line"),
])
def test_the_words_a_painter_would_use_find_the_row(words: str, expected: str) -> None:
    """The rows are written in the words a painter uses for the thing in front of
    them, which is the whole reason a dumb overlap is enough. Each of these is a
    description of what is on the canvas, not a guess at the cause."""
    found = diagnosis.match(words)
    assert found, f"{words!r} matched nothing"
    assert found[0].symptom.startswith(expected), (
        f"{words!r} best-matched {found[0].symptom!r}, not {expected!r}"
    )


def test_a_plural_and_its_singular_are_the_same_question() -> None:
    """A painter types `ring` and the row says `rings`, or the other way round. That
    is the whole of the stemming and the whole of what it is for."""
    assert diagnosis.match("ring")[0] == diagnosis.match("rings")[0]
    assert diagnosis.match("pass")[0] == diagnosis.match("passes")[0]


def test_a_short_precise_row_beats_a_long_one_that_mentions_the_word() -> None:
    """`smudge` appears in four rows. Asked about the thumbprint specifically, the
    thumbprint row wins -- the tie-break is what share of the row the question
    accounts for, so a row that merely contains the term in passing loses."""
    found = diagnosis.match("a thumbprint at the end of a smudge")
    assert found[0].symptom == "A thumbprint at the end of a smudge"


def test_words_that_match_no_row_fall_back_to_the_section() -> None:
    """A painter who has the wrong vocabulary should still be aimed at the right part
    of the index rather than told nothing.

    `gradient` is the case: it is a word the index groups by and that no symptom uses
    -- the rows say *graded*, *gradated*, *a stack of bands* -- so matching on rows
    alone answers nothing to a perfectly reasonable question."""
    assert not any("gradient" in diagnosis._words(row.symptom) for row in diagnosis.rows())
    found = diagnosis.match("gradient")
    assert found and all("gradient" in row.group for row in found)


def test_nothing_at_all_says_what_the_index_covers() -> None:
    """The one answer that is allowed to be a list: it is shorter than the file, and
    it is how a painter learns the words to ask again with."""
    text = diagnosis.answer("borogoves")
    assert "Nothing in the index matches" in text
    for group in ("An edge", "Colour, value, paint", "What it cost"):
        assert group in text


# -- what the command hands back --------------------------------------------------------
def test_the_answer_is_the_passage_and_not_the_pointer() -> None:
    """The whole of G5. The index's own instruction is *follow the pointer; do not
    work from the row*, and the one session that had it followed none in 293 strokes
    -- so the tool follows it. What comes back is the target, entire."""
    row = next(r for r in diagnosis.rows() if "concentric rings" in r.symptom)
    passage = row.pointers[0].passage()
    text = diagnosis.answer(row.symptom)

    assert row.symptom in text, "the row it matched should be named"
    assert passage.strip() in text, "the passage itself should be there, whole"
    assert len(text.split()) > 200, "a pointer is short; a passage is not"


def test_a_row_with_two_pointers_hands_back_both() -> None:
    """Two pointers means the reason is split across two documents -- the mechanism in
    one, the number in the other -- and handing over one of them is handing over half
    an answer."""
    row = next(r for r in diagnosis.rows() if len(r.pointers) == 2)
    text = diagnosis.passages(row)
    for pointer in row.pointers:
        assert pointer.document in text
        assert pointer.passage().strip() in text


def test_the_other_matches_are_offered_as_symptoms() -> None:
    """Not as passages. Four passages at once is the reading this index exists to
    avoid; four symptoms is how you ask again in better words."""
    text = diagnosis.answer("a glow")
    assert "ask again in more of their words" in text
    others = diagnosis.match("a glow")[1:]
    assert others and all(f"* {row.symptom}" in text for row in others)


def test_the_listing_is_symptoms_without_their_passages() -> None:
    text = diagnosis.listing()
    assert all(row.symptom in text for row in diagnosis.rows())
    assert "block_in" not in text, "a listing that has picked up a passage"


# -- from a shell ------------------------------------------------------------------------
@pytest.mark.parametrize("argv", [
    ["diagnose"],
    ["diagnose", "concentric", "rings"],
    ["diagnose", "--list"],
    ["diagnose", "--list", "edge"],
    ["diagnose", "borogoves"],
    ["guide", "--diagnosis"],
])
def test_the_command_runs_and_prints_something(argv: list[str], capsys) -> None:
    assert main(argv) == 0
    assert capsys.readouterr().out.strip()


def test_the_shell_prints_the_passage(capsys) -> None:
    """End to end, the way a painter meets it: words in, the measurement out."""
    assert main(["diagnose", "a", "glow", "with", "concentric", "rings"]) == 0
    out = capsys.readouterr().out
    assert "CALIBRATION.md" in out
    assert "the rings step" in out.casefold(), "the measurement, not the pointer"


def test_the_listing_is_shorter_than_the_answer(capsys) -> None:
    main(["diagnose", "--list", "concentric rings"])
    listed = capsys.readouterr().out
    main(["diagnose", "concentric rings"])
    answered = capsys.readouterr().out
    assert 0 < len(listed) < len(answered)
