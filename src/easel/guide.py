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

There are five of them now rather than three. The guide was split by function --
method, reasons, procedures, facts, numbers -- when three painters in a row said
the same two things about it: that it was long, and that its essay was what made
its rules stick. Nothing was cut; it was moved, and `PAINTER.md` is held to
:data:`FRONT_PAGE_WORDS` so that it stays the file a painter can hold in their
head. `LESSONS.md` has the reasoning.
"""

from __future__ import annotations

import sys
from pathlib import Path

#: Document name -> its filename at the repository root. The keys are what
#: `easel guide` accepts. `tests/test_guide.py` checks this against the
#: force-include table in pyproject.toml, which is the half of the arrangement
#: that lives outside Python and would otherwise drift on its own.
DOCUMENTS = {
    "guide": "PAINTER.md",
    "painting": "PAINTING.md",
    "recipes": "RECIPES.md",
    "reference": "REFERENCE.md",
    "calibration": "CALIBRATION.md",
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
FRONT_PAGE_WORDS = 10_000

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


def front_page() -> str:
    """`The first hour` on its own: the whole method, and enough to start.

    Falls back to the entire guide if the heading has been renamed, on the
    grounds that too much of the right document beats an empty page.
    """
    text = read("guide")
    start = text.find(FRONT_PAGE)
    if start == -1:
        return text

    end = text.find("\n## ", start + len(FRONT_PAGE))
    return text[start:] if end == -1 else text[start:end].rstrip() + "\n"


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
