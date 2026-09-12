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
    "reference": "REFERENCE.md",
    "calibration": "CALIBRATION.md",
}

#: The heading of the section the guide means to be read on its own. `PAINTER.md`
#: says to read it in two goes; this is the first, and at under a thousand words
#: it is the whole workflow. It ends where the next `##` heading begins.
FRONT_PAGE = "## The first hour"

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
