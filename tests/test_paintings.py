"""`PAINTINGS.md` against the paintings it claims to list.

The page says *one section below per directory under `paintings/`*, and it says that
instead of counting them on purpose: adding a painting should be adding a directory and
writing a section, not correcting a number in eight other sentences. Before this, the
count was baked into the summary line, the decide-first rule, a heading, the agreement
argument, the unfinished list and two entries in *Further*, and every one of them would
have quietly become wrong.

A promise like that is only worth something if it cannot stop being true without
somebody noticing. A painting committed with no section is invisible on the one page
that exists to show what the engine has painted, and a section pointing at a file that
was never committed is a broken image on the project's shop window -- neither is an
error anyone hits at the moment they cause it.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "PAINTINGS.md"
PAINTINGS = ROOT / "paintings"

DIRECTORIES = sorted(p.name for p in PAINTINGS.iterdir() if p.is_dir())

# What a painting's directory owes the page, and the page owes the reader.
LINKED = ("painting.png", "painting.gif", "NOTES.md")


@pytest.mark.parametrize("name", DIRECTORIES)
@pytest.mark.parametrize("filename", LINKED)
def test_every_painting_directory_carries_what_the_page_links_to(
    name: str, filename: str
) -> None:
    assert (PAINTINGS / name / filename).is_file(), (
        f"paintings/{name}/ has no {filename}. PAINTINGS.md links to one for every "
        f"painting; without it the page shows a broken image or a dead link."
    )


@pytest.mark.parametrize("name", DIRECTORIES)
def test_every_painting_has_a_section_on_the_page(name: str) -> None:
    text = PAGE.read_text(encoding="utf-8")
    for filename in LINKED:
        assert f"paintings/{name}/{filename}" in text, (
            f"paintings/{name}/ is committed but PAINTINGS.md does not link to its "
            f"{filename}. The page promises one section per directory under "
            f"paintings/ -- add the section, or the painting is invisible on it."
        )


def test_the_page_links_to_no_painting_that_is_not_there() -> None:
    """The other direction, which is the one that shows up as a broken image."""
    text = PAGE.read_text(encoding="utf-8")
    linked = {m for m in re.findall(r"paintings/([A-Za-z0-9_\-]+)/", text)}
    missing = sorted(name for name in linked if not (PAINTINGS / name).is_dir())
    assert not missing, f"PAINTINGS.md links to directories that do not exist: {missing}"


@pytest.mark.parametrize(
    "phrase",
    ["Three pictures", "all three", "All three", "these three paintings",
     "None of the three", "the three agree"],
)
def test_the_page_does_not_count_its_paintings(phrase: str) -> None:
    """A regression guard rather than a theorem: these are the exact constructions the
    page used before, each of which had to be rewritten to add a fourth painting. The
    rule is that the prose describes the collection without sizing it -- *every picture
    here*, *none of them*, *several painters* -- so that the next one costs a directory
    and a section and nothing else."""
    text = PAGE.read_text(encoding="utf-8")
    assert phrase not in text, (
        f"PAINTINGS.md counts its paintings again ({phrase!r}). Say it without the "
        f"number, so adding the next painting does not mean correcting this sentence."
    )
