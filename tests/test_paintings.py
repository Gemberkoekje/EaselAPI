"""`PAINTINGS.md` against the paintings it claims to list.

A *painting* is a directory holding a `painting.png` and the rest of what the page
links to. Usually that is a directory directly under `paintings/`; where one subject
has been painted more than once it is `paintings/<subject>/<painter>/`, and the
subject's directory is a container. The page's promise is still one section per
directory — a subject painted twice gets one section with a part for each painter —
but what has to be linked is one set of files per *painting*, which is what the checks
below count.

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

import contextlib
import io
import re
import warnings
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "PAINTINGS.md"
PAINTINGS = ROOT / "paintings"

# What a painting's directory owes the page, and the page owes the reader.
LINKED = ("painting.png", "painting.gif", "NOTES.md")

# What marks a directory as a painting rather than a container. A directory that
# holds one of these owes all of LINKED; a directory that holds none of them is
# either not a painting or is a subject painted more than once, and the paintings
# are one level in.
MARKS = LINKED + ("prelude.py",)


def _paintings(under: Path, depth: int = 2) -> list[str]:
    """Every painting under `paintings/`, as a path relative to it.

    A directory under `paintings/` is a painting if it looks like one, and a
    container to descend into if it does not. One *subject* may have been
    painted more than once -- `paintings/<subject>/<painter>/` -- and every
    painting also sits under the model that painted it --
    `paintings/<model>/<subject>/` -- so a subject one model painted more than
    once nests to `paintings/<model>/<subject>/<painter>/`, two containers
    deep. Before the greenhouse was painted twice this was a flat listing of
    `paintings/*`, and a nested painting was invisible to every check below
    while making the container fail all of them; before the paintings were
    grouped by model this needed one container less than it does now, for the
    same reason.
    """
    found = []
    for d in sorted(p for p in under.iterdir() if p.is_dir()):
        if any((d / m).exists() for m in MARKS):
            found.append(d.relative_to(PAINTINGS).as_posix())
        elif depth:
            found.extend(_paintings(d, depth - 1))
    return found


DIRECTORIES = _paintings(PAINTINGS)


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
    linked = set(re.findall(r"paintings/([A-Za-z0-9_\-]+(?:/[A-Za-z0-9_\-]+)?)/", text))
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


# --------------------------------------------------------------------------------------
# A count-only rehearsal, against the painting whose helpers asked for one
# --------------------------------------------------------------------------------------
# `cost()` prices one `block_in` or one `sweep`; a painter's own helper that calls a
# dozen verbs had no price short of painting it on a copy, and the copy renders every
# dab. One budgeted a row of thirteen pots at about 100 strokes, rehearsed it at 220
# against 142 left, and rebuilt it from strokes at 108 -- three renders of a pass that
# was never going to be laid, three minutes each.
#
# `scratch(count_only=True)` skips the pixel work, and the promise it makes is that the
# count is *exact* rather than an estimate: pass geometry is settled before anything is
# stamped. This is the test the request asked for -- the painting's own scripts, run
# both ways, pass by pass.
#
# The winter greenhouse is the one that raised it, and the one built out of compound
# helpers (`pot`, `foliage`, `stalks`, `boards` in its prelude). Its passes are run
# here on a fresh canvas rather than on the state the one before it left, so a pass
# that needs paint underneath raises the same way in both runs and is skipped: what is
# being held is that counting changes nothing, not that a pass runs out of order.

GREENHOUSE = PAINTINGS / "Claude" / "greenhouse_winter"
PASSES = sorted(GREENHOUSE.glob("p[0-9]*.py"),
                key=lambda p: int(re.match(r"p(\d+)", p.name).group(1)))


def _run_pass(source: str, name: str, out: Path, count_only: bool):
    """One pass of the greenhouse against a fresh canvas, painted or counted."""
    from easel import Session
    from easel.cli import run_scripts

    s = Session(1024, 768, texture="linen", ground="toned_warm_grey", seed=7,
                out_dir=out, timelapse=False, budget=300)
    target = s.scratch(count_only=count_only)
    # From `out`, because a pass is written to be run from beside its own session
    # file: the greenhouse's last one exports to `painting.png` and `painting.gif`
    # by name, and run from here that is the repository's own root.
    with contextlib.chdir(out), contextlib.redirect_stdout(io.StringIO()), \
            warnings.catch_warnings():
        warnings.simplefilter("ignore")
        result = run_scripts(target, [(source, name)],
                             prelude=(GREENHOUSE / "prelude.py").read_text(encoding="utf-8"),
                             prelude_name="prelude.py")
    return result, target


@pytest.mark.parametrize("script", PASSES, ids=lambda p: p.name)
def test_a_counted_pass_logs_what_a_painted_one_logs(script: Path, tmp_path) -> None:
    source = script.read_text(encoding="utf-8")
    painted_result, painted = _run_pass(source, script.name, tmp_path, count_only=False)
    counted_result, counted = _run_pass(source, script.name, tmp_path, count_only=True)

    if painted_result.code != 0:
        # This pass wants the paint an earlier one laid. Both runs are on a fresh
        # canvas, so that is the script asking a question of the canvas, not counting
        # answering one differently.
        pytest.skip(f"{script.name} needs an earlier pass under it")
    assert counted_result.code == 0

    assert counted.history.stroke_count == painted.history.stroke_count
    assert len(counted.history.records) == len(painted.history.records)
    for a, b in zip(painted.history.records, counted.history.records, strict=True):
        assert a.points == b.points, f"{script.name}: a pass moved"
        assert (a.brush, a.kind, a.note) == (b.brush, b.kind, b.note)
        assert a.dabs == b.dabs, f"{script.name}: the dab count moved"
        assert a.params.get("size") == b.params.get("size")
    # It laid no paint: every painted record's paint is nought, and the canvas it
    # borrowed still reads as the bare ground it started from. Graphite is not paint
    # and is still drawn -- it is free against the budget and cheap to lay.
    assert all(r.paint == 0.0 for r in counted.history.records if r.kind != "pencil")
    assert counted.canvas.ground_showing() == 1.0


# --------------------------------------------------------------------------------------
# The cohort probe's corpus, against the paintings there actually are
# --------------------------------------------------------------------------------------
# `scripts/probe_cohort_session.py` replays every committed painting to count how often
# a proposed check would fire, and the share of *passes* it fires on is the number that
# decides whether a rule is built. A painting missing from its corpus is not an error
# anyone hits: the probe runs, prints a table, and the table is quietly about twenty
# paintings instead of twenty-one. This is the same promise `PAINTINGS.md` makes one
# file over -- a painting is added by committing its directory -- held for the probe.


def _corpus():
    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    try:
        import probe_cohort_session
    finally:
        sys.path.remove(str(ROOT / "scripts"))
    return probe_cohort_session


def test_the_cohort_probe_replays_every_painting() -> None:
    probe = _corpus()
    listed = {entry.where for entry in probe.CORPUS}
    missing = sorted(set(DIRECTORIES) - listed)
    assert not missing, (
        f"scripts/probe_cohort_session.py does not replay {missing}. Add a Painting "
        f"entry with its canvas arguments from PAINTINGS.md, or every count the probe "
        f"prints is over a corpus one painting short."
    )
    extra = sorted(listed - set(DIRECTORIES))
    assert not extra, f"the probe's corpus names directories that are not paintings: {extra}"


@pytest.mark.parametrize("name", DIRECTORIES)
def test_every_painting_in_the_corpus_has_passes_to_replay(name: str) -> None:
    probe = _corpus()
    entry = next(e for e in probe.CORPUS if e.where == name)
    assert entry.driver or entry.passes, (
        f"paintings/{name}/ has no pass scripts the probe can find and no driver "
        f"script named. The probe would replay it as nothing at all."
    )
    assert entry.spent > 0, f"paintings/{name}/ has no stroke count to check a rebuild against"
