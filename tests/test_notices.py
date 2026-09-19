"""The notice channel, and the three ways it can drift apart from itself.

Before 0.6.0 every call-time warning was a bare ``warnings.warn(str)``: no class, no
code, no collection. A document could promise *the call says so* about a check that had
been deleted, a check could be added that no document mentioned, and nothing would
notice either way -- which is how this repository's prose and its engine drifted apart
twice, both times found by a painter rather than by a test.

So there are three surfaces now, and each pair of them is held against the other here,
in `test_reference.py`'s pattern -- one parametrized case per row rather than one big
assertion, so a failure names the code that broke:

* what `session.py` actually says (every ``_notify`` call in the source),
* :data:`easel.notices.NOTICES`, the registry,
* `REFERENCE.md`'s *What the tool will tell you* table, and the guide headings each
  row points at.

The rest is the channel's own behaviour: that a notice is still a `UserWarning` saying
exactly what it said before, that a pass collects what it was told, that the block
collapses and orders it, and that none of it touches the log -- which is the one thing
here that would move every painting ever made.
"""

from __future__ import annotations

import re
import warnings
from pathlib import Path

import numpy as np
import pytest

from easel import Session, cell, docs, ellipse, notices
from easel.cli import main
from easel.notices import KINDS, NOTICES, EaselWarning, Notice

ROOT = Path(__file__).resolve().parents[1]
SOURCE = sorted((ROOT / "src" / "easel").glob("*.py"))
REFERENCE = (ROOT / "REFERENCE.md").read_text(encoding="utf-8")

#: Every code the engine actually says, read off the calls rather than off the
#: registry -- otherwise the registry would be checked against itself.
SAID = sorted({
    m.group(1)
    for path in SOURCE
    for m in re.finditer(r'_notify\(\s*\n?\s*"([a-z0-9-]+)"', path.read_text(encoding="utf-8"))
})


def make(tmp_path, **kw):
    kw.setdefault("timelapse", False)
    return Session(320, 240, texture="linen", ground="toned_grey", seed=7,
                   out_dir=tmp_path, **kw)


# -- the registry against the engine ---------------------------------------------------
def test_the_engine_says_something() -> None:
    """A guard on the scan above: a regex that matched nothing would make every test
    below pass by being empty."""
    assert len(SAID) >= 20


@pytest.mark.parametrize("code", SAID)
def test_every_code_the_engine_says_is_registered(code) -> None:
    assert code in NOTICES


@pytest.mark.parametrize("code", sorted(NOTICES))
def test_every_registered_code_is_one_the_engine_says(code) -> None:
    """The other direction: a row for a check that was removed is a promise in
    `REFERENCE.md` that nothing behind it can keep."""
    assert code in SAID


def test_nothing_in_the_engine_warns_off_the_channel() -> None:
    """`_notify` is the only place in `src/easel/` allowed to call `warnings.warn`.

    That is what makes the rest of this file mean anything: a check that warned
    directly would have no code, would not be collected, would not reach an MCP
    painter and would not appear in any of the three surfaces held against each other
    above -- and there would be nothing to say so. It is how the channel stays one
    channel as workstreams B to G add to it.
    """
    loose = [
        f"{path.name}:{i + 1}"
        for path in SOURCE
        if path.name != "notices.py"     # the channel itself, which is what it says
        for i, line in enumerate(path.read_text(encoding="utf-8").splitlines())
        if "warnings.warn(" in line and "EaselWarning(" not in line
    ]
    assert not loose, f"warnings.warn off the notice channel: {loose}"


def test_an_unregistered_code_cannot_reach_a_painter(tmp_path) -> None:
    """`_notify` refuses it at the call rather than printing a code that `easel
    explain` cannot answer and `REFERENCE.md` does not list."""
    s = make(tmp_path)
    with pytest.raises(KeyError, match="not a registered notice"):
        s._notify("no-such-rule", "a sentence nobody registered")


# -- the registry against the documents ------------------------------------------------
@pytest.mark.parametrize("code", sorted(NOTICES))
def test_every_registered_code_is_a_row_of_the_reference_table(code) -> None:
    """*What the tool will tell you*, which is the table a painter reads when a pass
    prints a code they have not seen before."""
    rows = [ln for ln in REFERENCE.splitlines() if ln.startswith(f"| `{code}` |")]
    assert len(rows) == 1, f"REFERENCE.md has {len(rows)} rows for {code}"
    cells = [c.strip() for c in rows[0].split("|")]
    spec = NOTICES[code]
    assert cells[2] == spec.kind
    assert docs.DOCUMENTS[spec.document] in cells[4]
    assert spec.heading in cells[4]


@pytest.mark.parametrize("code", sorted(NOTICES))
def test_every_registered_code_points_at_a_passage_that_exists(code) -> None:
    """The one that breaks when the guide is edited rather than when the engine is.
    A heading renamed in `CALIBRATION.md` empties `easel explain` silently; this is
    what makes it loud instead."""
    spec = NOTICES[code]
    passage = docs.section(spec.document, spec.where[1])
    assert passage.startswith(spec.where[1])
    assert len(passage.split()) > 20, f"{code} points at an empty section"


@pytest.mark.parametrize("kind", KINDS)
def test_both_kinds_are_used(kind) -> None:
    """A distinction nothing is on either side of is a distinction that will rot."""
    assert any(spec.kind == kind for spec in NOTICES.values())


@pytest.mark.parametrize("code", sorted(NOTICES))
def test_every_kind_is_one_of_the_two(code) -> None:
    assert NOTICES[code].kind in KINDS


def test_a_document_asking_for_a_code_asks_for_one_that_exists() -> None:
    """Wherever a shipped document tells a painter to run `easel explain <code>`, the
    code has to be real. This is the test that stops the prose and the tool drifting
    apart again: the guide can only promise what the registry carries.

    `REFERENCE.md` names one today. It grows teeth as the guide's own paragraphs
    leave and are replaced by pointers at the checks that carry them, which is what
    this round is for."""
    asked = {
        m.group(1)
        for name in docs.DOCUMENTS
        for m in re.finditer(r"easel explain ([a-z][a-z0-9-]+)", docs.read(name))
    }
    assert asked <= set(NOTICES), f"named in the guide and not registered: {asked - set(NOTICES)}"


# -- what a notice is ------------------------------------------------------------------
def test_a_notice_is_still_a_user_warning_saying_what_it_always_said(tmp_path) -> None:
    """`EaselWarning` subclasses `UserWarning` and `str()` is the message alone, so
    every filter, `pytest.warns` and painter's own `simplefilter` that existed before
    the channel goes on working unchanged."""
    s = make(tmp_path)
    with pytest.warns(UserWarning, match="stops depositing paint") as caught:
        s.block_in(cell("D5"), "flat", "burnt_umber", size=0.001)
    warned = caught[0].message
    assert isinstance(warned, EaselWarning) and isinstance(warned, UserWarning)
    assert warned.code == "chisel-blank"
    assert warned.kind == "fact"
    assert str(warned) == warned.text == s.notices()[0].text


def test_a_pass_keeps_what_it_was_told(tmp_path) -> None:
    s = make(tmp_path)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s.block_in(cell("D5"), "flat", "burnt_umber", size=0.001)
        told = len(s.notices())
        s.smudge([(0.3, 0.5), (0.7, 0.5)], size=0.09)
    assert [n.code for n in s.notices()] == ["chisel-blank", "smudge-wide"]
    assert [n.code for n in s.notices(since=told)] == ["smudge-wide"]


def test_a_rehearsal_says_what_it_says_about_the_copy(tmp_path) -> None:
    """`rehearse` lays the plan on a throwaway copy, and a notice that landed there
    would be thrown away with it -- which through the MCP server, where the returned
    text is the only channel there is, meant not being told at all."""
    s = make(tmp_path)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s.rehearse([{"shape": ellipse(cell("D5"), 0.10, 0.10), "brush": "flat",
                     "color": "burnt_umber", "size": 0.001}])
    assert "chisel-blank" in [n.code for n in s.notices()]


def test_a_price_walk_says_what_it_found(tmp_path) -> None:
    """A quote that comes back four times what was budgeted should say why, and the
    walk that works it out happens on a copy too."""
    s = make(tmp_path)
    tall = ellipse(cell("D5"), 0.03, 0.30)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s.cost({"shape": tall, "brush": "flat", "color": "burnt_umber", "size": 0.01})
    assert "direction-default" in [n.code for n in s.notices()]


# -- the block that gets printed -------------------------------------------------------
def test_identical_codes_collapse_with_a_count() -> None:
    """Nine masses with `direction` left off is one thing said nine times. Printing it
    nine times is `LESSONS.md`'s seventh rule broken by the channel rather than by a
    check."""
    said = [Notice("chisel-blank", "first"), Notice("chisel-blank", "second"),
            Notice("chisel-blank", "third")]
    lines = notices.lines(said)
    assert len(lines) == 1
    assert "(3 calls)" in lines[0]
    # The first of them, because it is the one whose numbers can be gone and looked at.
    assert "first" in lines[0] and "second" not in lines[0]


def test_facts_come_before_habits() -> None:
    said = [Notice("smudge-wide", "a habit"), Notice("chisel-blank", "a fact")]
    assert [n.code for n, _ in notices.collapse(said)] == ["chisel-blank", "smudge-wide"]


def test_the_block_says_nothing_when_there_is_nothing_to_say() -> None:
    """An empty heading over an empty list reads as a missing sentence."""
    assert notices.block([]) == ""
    assert notices.block([], "check over this pass: nothing to report") == (
        "check over this pass: nothing to report")


def test_the_block_puts_the_call_before_the_pass() -> None:
    block = notices.block([Notice("chisel-blank", "lands nothing")], "check over this pass")
    assert block.index("at the call") < block.index("check over this pass")


# -- easel explain ---------------------------------------------------------------------
def test_explain_hands_back_the_passage_that_measured_it(tmp_path) -> None:
    text = make(tmp_path).explain("chisel-blank")
    assert "### What a solid mass actually lands at" in text
    assert "CALIBRATION.md" in text
    assert notices.explain("chisel-blank") == text


def test_explain_names_every_code_there_is_when_it_is_asked_for_one_that_is_not() -> None:
    with pytest.raises(KeyError, match="unknown notice"):
        notices.explain("chisel-blanc")


def test_the_shell_explains_a_code(capsys) -> None:
    assert main(["explain", "smudge-wide"]) == 0
    out = capsys.readouterr().out
    assert "## `smudge`" in out and "smudge-wide (habit)" in out


def test_the_shell_lists_them_all_with_no_code(capsys) -> None:
    assert main(["explain"]) == 0
    out = capsys.readouterr().out
    for code in NOTICES:
        assert code in out


# -- delivery: the shell, and the session file -----------------------------------------
def test_easel_run_prints_the_notices_above_the_check(tmp_path, capsys) -> None:
    """One block, once each, on stdout -- and not the unfiltered stderr copy, which
    arrived in the middle of the pass, apart from the check, and once per source line
    rather than once per thing said."""
    path = tmp_path / "p.easel"
    make(tmp_path).save(path)
    script = tmp_path / "pass.py"
    script.write_text(
        's.block_in(cell("D5"), "flat", "burnt_umber", size=0.001)\n'
        's.block_in(cell("E5"), "flat", "burnt_umber", size=0.001)\n',
        encoding="utf-8")

    assert main(["run", str(path), str(script)]) == 0
    caught = capsys.readouterr()
    assert caught.out.count("chisel-blank") == 1
    assert "(2 calls)" in caught.out
    assert caught.out.index("at the call") < caught.out.index("check over this pass")
    assert "chisel-blank" not in caught.err


def test_a_pass_that_raised_still_says_what_it_was_told(tmp_path, capsys) -> None:
    """The notices go out with the error, because there is no check to put them
    beside -- and a failing pass saying *less* than it did before there was a channel
    would be the channel making things worse."""
    path = tmp_path / "p.easel"
    make(tmp_path).save(path)
    script = tmp_path / "pass.py"
    script.write_text(
        's.block_in(cell("D5"), "flat", "burnt_umber", size=0.001)\n'
        'raise ValueError("stopped here")\n', encoding="utf-8")

    assert main(["run", str(path), str(script)]) == 1
    assert "chisel-blank" in capsys.readouterr().err


def test_a_painters_own_warning_is_not_filtered_with_ours(tmp_path, capsys) -> None:
    """Only `EaselWarning` is taken off stderr. A script's own warning, and every
    library under it, warns exactly as it did before."""
    path = tmp_path / "p.easel"
    make(tmp_path).save(path)
    script = tmp_path / "pass.py"
    script.write_text('import warnings\nwarnings.warn("mine, not the engine\'s")\n',
                      encoding="utf-8")
    with pytest.warns(UserWarning, match="mine, not the engine"):
        assert main(["run", str(path), str(script)]) == 0


def test_the_notices_survive_a_save_and_a_load(tmp_path) -> None:
    """A painting worked from the shell is loaded and saved once per pass, so without
    this the session would forget everything it had ever said between passes."""
    path = tmp_path / "p.easel"
    s = make(tmp_path)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s.block_in(cell("D5"), "flat", "burnt_umber", size=0.001)
    s.save(path)
    assert [(n.code, n.text) for n in Session.load(path).notices()] == \
           [(n.code, n.text) for n in s.notices()]


def _rewrite_meta(path: Path, change) -> None:
    """Edit one `.easel` file's meta in place, the way a differently-versioned Easel
    would have written it. Through an open handle, because `np.savez_compressed`
    appends `.npz` to a path that lacks it -- which quietly leaves the file under
    test untouched and every assertion about it vacuous."""
    import json

    with np.load(path, allow_pickle=False) as data:
        arrays = {k: data[k] for k in data.files}
    meta = json.loads(str(arrays["meta"]))
    change(meta)
    arrays["meta"] = np.array(json.dumps(meta))
    with open(path, "wb") as fh:
        np.savez_compressed(fh, **arrays)


def test_a_file_from_before_the_channel_still_opens(tmp_path) -> None:
    """New keys only, read with `.get`: 0.5.0 wrote no `notices` key and its files
    have to go on loading, which is the same guard that lets a 0.5.0 build open a
    file this one wrote."""
    path = tmp_path / "p.easel"
    s = make(tmp_path)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s.block_in(cell("D5"), "flat", "burnt_umber", size=0.001)
    s.save(path)
    assert Session.load(path).notices()          # the key is being read at all

    _rewrite_meta(path, lambda meta: meta.pop("notices"))
    assert Session.load(path).notices() == []


def test_a_code_this_build_does_not_know_is_dropped_on_load(tmp_path) -> None:
    """A file written by a later Easel: a notice whose registry row is missing has no
    kind to sort by and no passage to explain, so it is left behind rather than
    carried as something that cannot be printed."""
    path = tmp_path / "p.easel"
    make(tmp_path).save(path)
    _rewrite_meta(path, lambda meta: meta.update(
        notices=[["chisel-blank", "a real one"], ["from-0-7-0", "a later one"]]))

    assert [n.code for n in Session.load(path).notices()] == ["chisel-blank"]


# -- rule 8: nothing new may touch the log or the stream -------------------------------
def test_a_notice_leaves_the_log_and_the_stream_exactly_where_they_were(tmp_path) -> None:
    """The whole reason notices live beside `history.records` rather than in it: a
    mark's texture is seeded from its index in the log, so a notice that took one
    would repaint every painting made before it. Same pass, one call warned about and
    one not, and the paint has to land identically."""
    def build(size):
        s = make(tmp_path)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            s.smudge([(0.3, 0.5), (0.7, 0.5)], size=size)
            s.stroke([(0.1, 0.2), (0.9, 0.25)], "bristle", "burnt_umber", size=0.05)
        return s

    quiet, loud = build(0.02), build(0.09)
    assert not quiet.notices() and loud.notices()
    assert len(quiet.history.records) == len(loud.history.records)
    # The smudge itself moves paint differently at the two sizes; the mark *after* it
    # is what has to be untouched, and it is laid on a canvas the smudge did not
    # reach.
    assert np.array_equal(quiet.canvas.rgb[:100], loud.canvas.rgb[:100])
