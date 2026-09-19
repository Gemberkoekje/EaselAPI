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

import subprocess
import sys
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


def test_the_guide_is_reachable_from_a_bare_import() -> None:
    """Shipping the document is half of it; being findable is the other half.

    Discoverability is the whole job of this module, and it was the one submodule
    `dir(easel)` did not list -- `brush`, `canvas`, `palette` and the rest are bound
    by `__init__.py`, so an agent reading that listing saw the engine and concluded
    there was no method. Absence from a listing is a claim.

    This runs in a subprocess on purpose. Every other test in this file does
    `from easel import guide` at import time, which binds the attribute on the
    package for the rest of the process -- so the same assertion made in-process
    passes whether or not `__init__.py` imports it, which is precisely the bug it
    is here to catch. A session that types `dir(easel)` has imported nothing else.
    """
    probe = (
        "import easel; "
        "assert 'guide' in dir(easel), 'dir(easel) does not list guide'; "
        "assert easel.guide.front_page().strip()"
    )
    done = subprocess.run(
        [sys.executable, "-c", probe], capture_output=True, text=True
    )
    assert done.returncode == 0, done.stderr


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


def test_the_front_page_stays_inside_its_word_budget() -> None:
    """`PAINTER.md` is the file a session is asked to hold in its head.

    `LESSONS.md` has said since early on that a finding never adds a paragraph to
    the guide, and under that rule the guide doubled -- from 8,600 words to 17,000
    -- because nothing enforced it. A stroke budget works because the engine holds
    it; this is the same arrangement for the same reason. Over budget, the fix is
    to move something to `PAINTING.md`, `RECIPES.md`, `REFERENCE.md` or
    `CALIBRATION.md`, not to raise the number.
    """
    words = len(guide.read("guide").split())
    assert words <= guide.FRONT_PAGE_WORDS, (
        f"PAINTER.md is {words} words, over its {guide.FRONT_PAGE_WORDS}-word budget "
        f"by {words - guide.FRONT_PAGE_WORDS}. Move a section out rather than raising this."
    )


def test_the_essay_is_where_the_length_went() -> None:
    """The split was a move, not a cut. If `PAINTING.md` ever becomes a stub, the
    front page's budget has stopped being paid for and started being a deletion."""
    assert len(guide.read("painting").split()) > 5_000


def test_one_home_per_rule(capsys) -> None:
    """`scripts/check_guide_overlap.py`, in the suite, for the reason the word budget is
    in the suite: a rule nothing enforces is a preference.

    Six rules were each stated in full in four to six of the five guide files before the
    restructure, and `SUGGESTIONS.md` has claimed ever since that the checker reports
    zero. It stopped being true without anybody noticing -- the notice channel added
    *a mark's texture is seeded from its place in the log* to `REFERENCE.md`, where
    `PAINTING.md` already had it -- because the script was something a person had to
    remember to run. Over the line, the fix is to say it once and link, not to raise the
    window.
    """
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
    try:
        import check_guide_overlap
    finally:
        sys.path.pop(0)
    assert check_guide_overlap.main([]) == 0, capsys.readouterr().out


@pytest.mark.parametrize("argv", [
    ["guide"],
    ["guide", "--full"],
    ["guide", "--painting"],
    ["guide", "--recipes"],
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


@pytest.mark.parametrize("name", sorted(guide.DOCUMENTS))
def test_a_shipped_document_prints_on_a_cp1252_console(name: str) -> None:
    """`print(easel.docs.read("calibration"))` is the most natural thing a painter does
    with the guide from Python, and on a Windows console it died: **35 characters**
    across the five documents sit outside cp1252 -- a rightwards arrow, a true minus,
    *approximately* and *less-or-equal* -- and 31 of them were in `CALIBRATION.md`.

    The tool itself was never the problem (`easel guide` writes UTF-8 bytes past the
    codec on purpose, and no string in `src/easel/` is non-ASCII); what died was the
    painter's own print. So the documents are held to the narrower codec, and the four
    characters are spelled `->`, `-`, `~` and `<=`.
    """
    text = guide.document_path(name).read_text(encoding="utf-8")
    try:
        text.encode("cp1252")
    except UnicodeEncodeError as bad:
        offender = text[bad.start:bad.end]
        line = text[:bad.start].count("\n") + 1
        pytest.fail(
            f"{guide.DOCUMENTS[name]} line {line} has {offender!r} "
            f"(U+{ord(offender[0]):04X}), which a cp1252 console cannot print."
        )


def test_the_installed_name_is_an_import_name(tmp_path) -> None:
    """The distribution is `easel-paint` and the import the documents teach is `easel`,
    which is one name too many for something met in the first two minutes: a session
    installed the wheel, typed `import easel_paint` because that is what it had just
    installed, and got ModuleNotFoundError. The guess the other way round is worse --
    PyPI carries an unrelated distribution called `easel`.

    So both names are real, and they are the same objects rather than a copy: a name
    added to one is exported by the other the same day.
    """
    import easel
    import easel_paint

    assert easel_paint.Session is easel.Session
    assert set(easel.__all__) <= set(easel_paint.__all__)
    assert easel_paint.__version__ == easel.__version__
    # Submodules too, so `easel_paint.docs.read(...)` is not a narrower thing than
    # the documents describe.
    assert easel_paint.session is easel.session
    assert easel_paint.docs.front_page() == easel.docs.front_page()


def test_the_wheel_ships_both_import_names() -> None:
    """The half of that which is not Python: a package left out of the build table is
    a package that works in a checkout, where the tests run, and is missing from every
    install."""
    packages = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))[
        "tool"]["hatch"]["build"]["targets"]["wheel"]["packages"]
    assert sorted(packages) == ["src/easel", "src/easel_paint"]
    for package in packages:
        assert (ROOT / package / "__init__.py").is_file()
