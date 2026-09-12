"""The guide against the package that is supposed to carry it.

`PAINTER.md` is the deliverable, and for two releases the wheel did not contain
it: a session that installed from PyPI got the brush and none of the method. The
fix has two halves that live in different files and cannot see each other -- a
force-include table in pyproject.toml, and `easel.guide` reading what it produces
-- so the drift between them is what these tests are for. A missing document is
not an exception anyone will see at the right time; it is a painter, months from
now, told to read a file that is not there.
"""

from __future__ import annotations

import tomllib
from pathlib import Path

import pytest

from easel import guide
from easel.cli import main

ROOT = Path(__file__).resolve().parents[1]
WHEEL_INCLUDES = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))[
    "tool"]["hatch"]["build"]["targets"]["wheel"]["force-include"]


@pytest.mark.parametrize("name", sorted(guide.DOCUMENTS))
def test_every_document_resolves(name: str) -> None:
    path = guide.document_path(name)
    assert path.is_file()
    assert path.name == guide.DOCUMENTS[name]


def test_the_build_ships_exactly_the_documents_the_code_looks_for() -> None:
    """The half of this that is not Python. Add a document to `DOCUMENTS` without
    adding it here and it resolves in a checkout, where the tests run, and is
    missing from every install -- which is precisely the bug this replaced."""
    shipped = {Path(src).name for src in WHEEL_INCLUDES}
    assert shipped == set(guide.DOCUMENTS.values())


@pytest.mark.parametrize("source, target", sorted(WHEEL_INCLUDES.items()))
def test_each_shipped_document_lands_where_the_code_looks(source: str, target: str) -> None:
    assert (ROOT / source).is_file()
    assert target == f"easel/docs/{source}"


def test_the_front_page_is_the_first_hour_and_stops_there() -> None:
    page = guide.front_page()
    assert page.startswith(guide.FRONT_PAGE)
    # One `##` heading, its own: the section ends where the next one starts.
    assert [ln for ln in page.splitlines() if ln.startswith("## ")] == [guide.FRONT_PAGE]
    assert len(page.split()) < len(guide.read("guide").split())


def test_the_front_page_carries_the_one_habit() -> None:
    """If the front page ever stops saying this, it has stopped being the method."""
    assert "Look every 5 to 15 strokes" in guide.front_page()


def test_an_unknown_document_says_what_there_is() -> None:
    with pytest.raises(KeyError) as excinfo:
        guide.document_path("nonsense")
    assert "reference" in str(excinfo.value)


@pytest.mark.parametrize("argv", [
    ["guide"],
    ["guide", "--full"],
    ["guide", "--reference"],
    ["guide", "--calibration"],
    ["guide", "--path"],
])
def test_the_command_runs_and_prints_something(argv: list[str], capsys) -> None:
    assert main(argv) == 0
    assert capsys.readouterr().out.strip()


def test_the_command_prints_less_by_default_than_with_full(capsys) -> None:
    main(["guide"])
    first_page = capsys.readouterr().out
    main(["guide", "--full"])
    whole = capsys.readouterr().out
    assert 0 < len(first_page) < len(whole)


def test_path_prints_a_path_rather_than_the_document(capsys) -> None:
    main(["guide", "--path"])
    out = capsys.readouterr().out.strip()
    assert Path(out).is_file()
    assert "\n" not in out
