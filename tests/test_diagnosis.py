"""`DIAGNOSIS.md` against the documents it indexes.

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
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "DIAGNOSIS.md"

INDEXED = ("PAINTER.md", "PAINTING.md", "RECIPES.md", "REFERENCE.md", "CALIBRATION.md")

#: A pointer is `FILE.md` -> *Heading*, and the heading is matched as a prefix so a row
#: can name a section without repeating all of it.
POINTER = re.compile(r"`([A-Z]+\.md)`\s*→\s*\*([^*]+)\*")

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
