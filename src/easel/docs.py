"""The guide, shipped inside the package it is a guide to.

`PAINTER.md` is this project's actual deliverable. The engine is the brush; the
guide is the method, and every measured run says the method is the half that
matters. But a wheel is built from `src/easel` and the guide lives at the
repository root, so the first two releases handed a painter who ran
`pip install easel-paint` the brush and none of the method: no `PAINTER.md`, no
`REFERENCE.md`, nothing in the package but modules.

The build now copies those documents to `easel/docs/` (the force-include table in
pyproject.toml), and this module finds them again -- from an installed package,
or from a checkout, where that directory does not exist because nothing has been
built yet. Both have to work: the repository itself is used through
`pip install -e .`, which is a checkout.

The guide is five of them rather than the three it started as, split by function --
method, situations, the engine's behaviour, facts, numbers -- and since the tenth
round every rule is stated once, in the file it belongs to, and linked from the
others; `scripts/check_guide_overlap.py` says whether a sentence has crept into
two files. `PAINTER.md` is held to :data:`FRONT_PAGE_WORDS` so that it stays the
file a painter can hold in their head. `LESSONS.md` has the reasoning.

`DIAGNOSIS.md` is a sixth file here and not a sixth guide file: it states no rule,
it is an index of symptoms pointing at the five, and it says on its own first line
that it is not for reading. It ships because it was written to be grepped and there
was nothing to grep from an installed wheel. :mod:`easel.diagnosis` is what reads
it, and `easel diagnose` is how a painter should meet it.

This module was `easel.guide` until 0.5.0, and that name still works -- but it
collided with `Session.guide()`, which lays scaffolding on the view and has
nothing to do with the documents. A painter reaches both from one session, and
the guide teaches the method without ever mentioning the module, so the name was
only ever going to be met twice with no warning that it meant two things. The
documents are what this reads, so `easel.docs` is what it is called.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

#: Document name -> its filename at the repository root. The keys are what
#: `easel guide` accepts. `tests/test_guide.py` checks this against the
#: force-include table in pyproject.toml, which is the half of the arrangement
#: that lives outside Python and would otherwise drift on its own.
#:
#: `diagnosis` is the sixth and the odd one out: it is an index rather than a
#: document, and `DIAGNOSIS.md` opens by saying it is not for reading. It ships
#: because the alternative was worse -- for three releases the only way to use it
#: was `grep` in a checkout, so a painter who installed the wheel did not have it
#: at all. `easel.diagnosis` is what reads it; `easel guide --diagnosis` prints it
#: for the same reason every other document is printable, not because anybody
#: should.
DOCUMENTS = {
    "guide": "PAINTER.md",
    "painting": "PAINTING.md",
    "recipes": "RECIPES.md",
    "reference": "REFERENCE.md",
    "calibration": "CALIBRATION.md",
    "diagnosis": "DIAGNOSIS.md",
}

#: The heading of the section the guide means to be read on its own: the whole
#: workflow in under a thousand words, and enough to start. It ends where the next
#: `##` heading begins.
FRONT_PAGE = "## The first hour"

#: A hard ceiling on `PAINTER.md`, asserted by `tests/test_guide.py` and printed by
#: `scripts/check_guide_blocks.py`.
#:
#: `LESSONS.md` has carried a no-growth rule since early on -- a finding replaces a
#: rule, becomes a checklist line, or goes elsewhere -- and under it the guide went
#: from 8,600 words to 17,000, because a rule nothing enforces is a preference. The
#: stroke budget works precisely because the engine holds it, so this one is held the
#: same way. The split into `PAINTER.md` / `PAINTING.md` / `RECIPES.md` moved the
#: essay out rather than cutting it, which is what makes a ceiling here affordable:
#: material turned away from this file has somewhere to go.
#:
#: 10,000 rather than the 5,000-6,000 a painter proposed, because that figure was
#: never costed against the contents it asked for -- the order of work, *What you are
#: bad at*, the checklist and the exercises come to about 8,500 words on their own,
#: and reaching 6,000 would mean cutting them, which every other item on the same
#: list forbids. A budget nobody can meet on the day it is written holds nothing.
#:
#: **Lowered to the file's own size in 0.6.0**, which is what a ceiling three
#: thousand words above the text was not: the round moved rule after rule out of
#: here and into something the tool says, and 10,000 stopped binding anything. It is
#: set a little over what the file is, so the next paragraph has to buy its place by
#: taking one out. The round's plan wanted about 5,000, and that is not this: getting
#: there means cutting the workflow, the exercises or *What you are bad at*, each of
#: which a session has defended, and that is a design job with a measurement behind
#: it rather than an edit.
FRONT_PAGE_WORDS = 6_700

#: The same, for the card -- `The first hour`, the section meant to be read alone and
#: the one every painter reads. It had no ceiling until 0.6.0, and it is the page that
#: most wants one: what a painter meets before the first mark is the thing the round
#: measured as too long. `LESSONS.md`'s growth rule applies here twice over, since
#: anything added to the card is added to the file as well.
CARD_WORDS = 1_400

_PACKAGED = Path(__file__).resolve().parent / "docs"
_CHECKOUT = Path(__file__).resolve().parents[2]


def document_path(name: str = "guide") -> Path:
    """Where `name` actually is, installed or in a checkout.

    Raises `KeyError` for a name that is not a document and `FileNotFoundError`
    when the file is missing from both places, which means a broken build rather
    than anything the caller did.
    """
    try:
        filename = DOCUMENTS[name]
    except KeyError:
        known = ", ".join(sorted(DOCUMENTS))
        raise KeyError(f"unknown document {name!r}; there is {known}") from None

    for candidate in (_PACKAGED / filename, _CHECKOUT / filename):
        if candidate.is_file():
            return candidate

    raise FileNotFoundError(
        f"{filename} is in neither {_PACKAGED} nor {_CHECKOUT}. An installed "
        f"package should carry it; see the wheel force-include in pyproject.toml."
    )


def read(name: str = "guide") -> str:
    """The whole document, as text."""
    return document_path(name).read_text(encoding="utf-8")


def headings(name: str, text: str | None = None) -> list[tuple[int, int, str]]:
    """Every heading in a document: `(line number, level, the heading line)`.

    Fenced code blocks are stepped over. Half the passages here end in an example,
    and a Python comment is a line starting with `#` that has nothing to do with the
    document's structure -- so a scanner that does not know about fences reports
    `# mix the shadow first` as a top-level heading and cuts a section in half.

    One scanner rather than one per caller, because `section` and `heading_line`
    disagreeing about what a heading is would show up as a passage that stops in the
    wrong place, which nothing in the suite can see. `text` scans a draft of the
    document instead of the file, which is how `easel.demo` reads a recipe that has
    not been saved yet.
    """
    found: list[tuple[int, int, str]] = []
    fenced = False
    for i, line in enumerate((read(name) if text is None else text).splitlines()):
        text = line.lstrip()
        if text.startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        level = len(text) - len(text.lstrip("#"))
        if level and text[level:level + 1] == " ":
            found.append((i, level, line.rstrip()))
    return found


def _plain(text: str) -> str:
    """A heading with its markdown taken off, for matching a pointer against it."""
    return re.sub(r"[`*]", "", text).strip().casefold()


def heading_line(name: str, prefix: str) -> str:
    """The heading of `name` that `prefix` names, `#`s and all -- what `section` takes.

    `DIAGNOSIS.md` writes its pointers the way a painter would say them aloud --
    ``CALIBRATION.md -> *`block_in`*`` -- with no `#`s, no backticks, and often only
    the front of the heading. `section` wants the line exactly as the document writes
    it. This is the translation between the two, and it is what lets a pointer stay
    readable prose while still resolving to a passage.

    An exact match wins over a longer heading that merely starts the same way;
    failing that, the first in document order, which is the `##` rather than a `###`
    nested under it -- so a pointer that names a section gets the whole section.

    Raises `KeyError` naming the prefix, so a renamed heading is a broken test rather
    than an empty answer. `tests/test_diagnosis.py` holds every pointer to this.
    """
    wanted = _plain(prefix)
    lines = headings(name)
    # The `#`s come off the stripped line rather than by slicing at `level`, so an
    # indented heading -- one nested under a list item, which is legal markdown --
    # does not silently match on its own leading spaces.
    texts = [(_plain(line.lstrip().lstrip("#")), line) for _, _, line in lines]
    for text, line in texts:
        if text == wanted:
            return line
    for text, line in texts:
        if text.startswith(wanted):
            return line
    raise KeyError(
        f"{DOCUMENTS[name]} has no heading starting {prefix!r}. A heading has moved "
        f"or been renamed; fix the pointer that names it, not this."
    )


def section(name: str, heading: str, text: str | None = None) -> str:
    """One section of a document: from `heading` to the next one of its level or above.

    `easel explain <code>` is built on this. A notice's registry row points at the
    heading that holds its measurement, and this is what turns that pointer into the
    passage -- so a reason that leaves the reading path is not deleted, it is
    delivered at the moment it applies. See `easel.notices`.

    `heading` is the heading line exactly as the document writes it, `#`s and all
    (`"### The band across a wedge"`). Matched against a whole line rather than
    anywhere in the text, so a heading quoted in a table or a link is not mistaken
    for the section itself.

    Fenced code blocks are stepped over; `headings` is what does it, and says why.

    Raises `KeyError` for a heading the document does not have, which is what makes
    a renamed heading a broken test rather than an empty answer.

    `text` reads a draft instead of the shipped file, as `headings` does: a word
    budget is checked against the file on disk, which is not always the one the
    package would hand back.
    """
    lines = (read(name) if text is None else text).splitlines(keepends=True)
    level = len(heading) - len(heading.lstrip("#"))
    found = headings(name, text)
    start = next((i for i, _, line in found if line == heading), None)
    if start is None:
        raise KeyError(f"{DOCUMENTS[name]} has no heading {heading!r}")

    end = next((i for i, depth, _ in found if i > start and depth <= level), len(lines))

    body = "".join(lines[start:end]).rstrip()
    # The `---` rule that separates two sections belongs to neither of them.
    if body.endswith("\n---"):
        body = body[: -len("\n---")].rstrip()
    return body + "\n"


def front_page() -> str:
    """`The first hour` on its own: the whole method, and enough to start.

    Falls back to the entire guide if the heading has been renamed, on the
    grounds that too much of the right document beats an empty page.
    """
    try:
        return section("guide", FRONT_PAGE)
    except KeyError:
        return read("guide")


def write(text: str) -> None:
    """Print `text`, without losing it to the console's codec.

    The guide is full of em dashes and arrows, and on Windows a redirected stdout
    still defaults to the locale encoding -- so plain `print` can die of
    UnicodeEncodeError halfway down a document that was fine on the machine it
    was written on. Writing UTF-8 bytes to the underlying buffer sidesteps the
    codec entirely. Captured streams in tests have no `.buffer`, hence the guard.
    """
    stream = getattr(sys.stdout, "buffer", None)
    if stream is None:
        print(text)
        return
    stream.write(text.encode("utf-8"))
    stream.flush()
