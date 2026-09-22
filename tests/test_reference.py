"""`REFERENCE.md` against the engine it describes.

A reference is a promise that a number in it is the number in the code. The guide can
be a little out of date and still teach the right habit; a reference that is out of
date is worse than no reference, because it is read *instead of* looking. Nothing here
judges the prose -- it checks the facts that can drift on their own: the brush table,
the defaults, every name a painter can say, and every flag the shell takes.

The one measurement in the repo that a test can make is this one. Everything else worth
knowing about the engine was found by looking at a picture.
"""

from __future__ import annotations

import re
import warnings
from dataclasses import fields
from pathlib import Path

import pytest

from easel import Region, Session
from easel.brush import BRUSHES, Brush
from easel.canvas import GROUNDS
from easel.cli import build_parser
from easel.history import History
from easel.palette import PIGMENTS
from easel.prepare import LEVELS
from easel.regions import REGION_NAMES
from easel.stroke import PRESSURE_PROFILES
from easel.texture import TEXTURES

REFERENCE = Path(__file__).resolve().parents[1] / "REFERENCE.md"
TEXT = REFERENCE.read_text(encoding="utf-8")

#: Pigment names that are short forms of another entry rather than paint of their own.
ALIASES = ("white", "yellow", "ochre", "red", "blue", "umber", "sienna")


def _number(cell: str) -> float:
    return float(cell.strip().strip("`"))


@pytest.mark.parametrize("name", sorted(BRUSHES))
def test_the_brush_table_is_the_brush(name):
    """Every row of it, against the preset it names."""
    rows = [ln for ln in TEXT.splitlines() if ln.startswith(f"| `{name}` |")]
    assert len(rows) == 1, f"REFERENCE.md has {len(rows)} rows for {name}"
    cells = rows[0].split("|")
    b = BRUSHES[name]
    got = [_number(c) for c in cells[3:8]]
    assert got == [b.size, b.opacity, b.hardness, b.load, b.load_falloff]


@pytest.mark.parametrize(
    "field",
    ["spacing", "jitter", "size_jitter", "angle", "aspect", "wetness",
     "thickness_gain", "smudge", "texture_sensitivity", "bristle_count",
     "bristle_pitch", "bristle_seed", "tip_wobble"],
)
def test_every_other_brush_default_is_listed_as_it_stands(field):
    """Read back as a number, not as a string: `0` and `0.0` are the same default, and
    a test that says otherwise is a test about typography."""
    default = {f.name: f.default for f in fields(Brush)}[field]
    found = re.search(rf"`{field} ([\d.]+)`", TEXT)
    assert found, f"REFERENCE.md does not list a default for {field}"
    assert float(found.group(1)) == pytest.approx(float(default))


@pytest.mark.parametrize("name", REGION_NAMES)
def test_every_region_a_painter_can_say_is_named(name):
    assert re.search(rf"\b{re.escape(name)}\b", TEXT)


@pytest.mark.parametrize("name", sorted(GROUNDS))
def test_every_ground_is_named(name):
    assert name in TEXT


@pytest.mark.parametrize("name", TEXTURES)
def test_every_texture_is_named(name):
    assert name in TEXT


@pytest.mark.parametrize("name", PRESSURE_PROFILES)
def test_every_pressure_profile_is_named(name):
    assert f'"{name}"' in TEXT


@pytest.mark.parametrize("name", sorted(set(PIGMENTS) - set(ALIASES)))
def test_every_pigment_is_named(name):
    assert name in TEXT


def test_the_short_names_are_named_as_short_names():
    """Seven of the eighteen entries are the same paint under another name, and a
    painter counting the box off this page should not come out with eighteen."""
    for alias in ALIASES:
        assert f"`{alias}`" in TEXT
    assert len(set(PIGMENTS) - set(ALIASES)) == 11
    assert "Eleven pigments" in TEXT


@pytest.mark.parametrize("level", sorted(LEVELS))
def test_every_prepare_level_is_named(level):
    assert f'"{level}"' in TEXT or f"`{level}`" in TEXT
    assert str(LEVELS[level]) in TEXT


def test_the_signature_allowance_is_the_one_the_log_grants():
    assert f"first {History.SIGNATURE_ALLOWANCE}" in TEXT or "first five" in TEXT
    assert History.SIGNATURE_ALLOWANCE == 5, "the reference says five in words"


def _budget_columns() -> tuple[str, str]:
    """The free column and the charged column of the budget table, as two strings."""
    table = TEXT.split("## What counts against the budget")[1].split("\n\n")[1]
    free, charged = [], []
    for row in table.splitlines()[2:]:                      # past the header and rule
        cells = row.split("|")
        free.append(cells[1])
        charged.append(cells[2])
    return " ".join(free), " ".join(charged)


@pytest.mark.parametrize("kind", [k for k in History.UNPAINTED_KINDS if k != "look"])
def test_what_the_log_does_not_charge_for_is_in_the_free_column(kind):
    """`look` is the exception: it is a record kind, not a call a painter makes."""
    free, charged = _budget_columns()
    assert f"`{kind}" in free and f"`{kind}" not in charged


@pytest.mark.parametrize(
    "verb", ["stroke", "dab", "smudge", "glaze", "block_in", "sweep", "scumble", "cover"])
def test_every_verb_that_lays_paint_is_in_the_charged_column(verb):
    """Including `smudge` and `glaze`, which a painter reaches for believing otherwise."""
    free, charged = _budget_columns()
    assert f"`{verb}" in charged and f"`{verb}" not in free


def _cli_options() -> set[str]:
    """Every long option the shell takes, whichever subcommand takes it."""
    out: set[str] = set()
    parser = build_parser()
    for action in parser._actions:
        for choice in getattr(action, "choices", None) or {}:
            sub = action.choices[choice]
            out.update(o for a in sub._actions for o in a.option_strings)
    return out


@pytest.mark.parametrize("flag", sorted(set(re.findall(r"--[a-z][a-z-]+", TEXT))))
def test_every_flag_the_reference_prints_is_a_flag(flag):
    assert flag in _cli_options()


# -- the signature lines, against the signatures ------------------------------------------
#
# `look(marks=)` and `look(impasto=)` shipped in 0.4.0 and were named in none of the
# five documents: this page's signature line listed eight of the ten parameters and
# stopped. A painter placed six landmarks, judged the picture through fifty-two looks
# with their labels drawn over it, and never found the way to turn them off -- having
# found `unguide()` for the scaffolding, because that one *is* named. That was the
# second of its kind, and the first fix, a sentence, did not generalise: these lines
# are hand-maintained, and one had been wrong since the parameter shipped.
#
# So the page's own claim is the test. It says it checks *every name a painter can
# say*, and a parameter is the kind of name a painter types. Two checks, because the
# page names a parameter in two ways and each misses what the other catches: the
# spelled-out calls have to be complete where they stand, and every call anywhere on
# the page has to have all of its parameters somewhere in the page's code.

def _documented_calls() -> list[tuple[str, object]]:
    """Every public call the page is answerable for, as (label, function).

    Everything on :class:`Session` and :class:`Palette` that does not start with an
    underscore, plus the shape and place constructors and ``Session(...)`` itself --
    not only the calls the page happens to have written out. That is the page's own
    claim, and it means **a new public parameter fails this file until it is
    documented**, which is the point: the one that raised it had shipped a release
    earlier and nobody noticed.
    """
    import easel
    from easel.palette import Palette
    from easel.session import Session

    out = [("Session", Session.__init__)]
    for prefix, owner in (("s.", Session), ("p.", Palette)):
        for name in dir(owner):
            fn = getattr(owner, name, None)
            if not name.startswith("_") and callable(fn):
                out.append((f"{prefix}{name}", fn))
    for name in ("polygon", "ellipse", "blob", "hull", "ribbon", "union",
                 "cell", "span", "region", "horizon", "between", "thirds", "golden"):
        out.append((name, getattr(easel, name)))
    return out


def _optional(fn) -> list[str]:
    """The parameters a painter passes by name: the ones with a default.

    A required argument is shown by example instead -- `s.export("painting.png")` --
    so asking for its name back would be asking the page to write Python twice.
    """
    import inspect

    try:
        params = inspect.signature(fn).parameters.values()
    except (TypeError, ValueError):  # pragma: no cover - a builtin sneaking in
        return []
    return [p.name for p in params
            if p.name != "self"
            and p.default is not inspect.Parameter.empty
            and p.kind is not inspect.Parameter.VAR_KEYWORD]


#: The page's code and nothing else: every fenced block, plus every inline span. A
#: parameter has to be named *as code* -- `path`, `name`, `size` and `note` are all
#: ordinary English, and prose that happens to contain one is not documentation of it.
CODE = "\n".join(re.findall(r"```[a-z]*\n(.*?)```", TEXT, re.S)
                  + re.findall(r"`([^`\n]+)`", TEXT))

CALLS = _documented_calls()


@pytest.mark.parametrize("label,fn", CALLS, ids=[c[0] for c in CALLS])
def test_every_parameter_a_painter_can_name_is_somewhere_on_the_page(label, fn):
    """The whole page is the scope here: `sweep` takes twelve optional arguments and
    the page spells them out in a table under the verb rather than on one line."""
    missing = [p for p in _optional(fn)
               if not re.search(rf"(?<![\w.]){re.escape(p)}\b", CODE)]
    assert not missing, (
        f"REFERENCE.md never names {', '.join(missing)}, which {label} takes. "
        f"A parameter nobody can find is a parameter nobody has."
    )


def _spelled_out() -> list[tuple[str, object, str]]:
    """The calls the page writes out as a signature, as (label, fn, the call itself).

    The scope is the call and nothing around it -- its own line, the lines it is
    continued onto, and the comment on the end of them. Anything wider does not
    hold: the *Looking* block alone spells out fifteen calls, and `export`'s
    `impasto=` four lines down was enough to make the missing one on `look` read as
    documented.
    """
    known = dict(_documented_calls())
    found: dict[str, tuple] = {}
    for chunk in TEXT.split("```python")[1:]:
        lines = chunk.partition("```")[0].splitlines()
        for i, line in enumerate(lines):
            head = line.strip()
            label = head.split("(")[0]
            if label not in known or "(" not in head:
                continue
            if "=" not in head.split("(", 1)[1]:
                # Not a signature: a call written out as an example takes its
                # arguments positionally, and has nothing to be complete about.
                continue
            call = [line]
            while "".join(call).count("(") > "".join(call).count(")"):
                i += 1
                if i >= len(lines):
                    break
                call.append(lines[i])
            found.setdefault(label, (label, known[label], "\n".join(call)))
    return sorted(found.values(), key=lambda row: row[0])


SPELLED = _spelled_out()


def test_the_page_still_spells_out_the_calls_this_is_about():
    """A guard on the guard: a scrape that stops finding lines passes by finding
    nothing to check."""
    names = {label for label, _, _ in SPELLED}
    assert {"s.look", "s.compare", "s.prepare", "p.at_value", "ellipse"} <= names
    assert len(SPELLED) >= 12, sorted(names)


@pytest.mark.parametrize("label,fn,call", SPELLED, ids=[c[0] for c in SPELLED])
def test_a_spelled_out_signature_names_all_of_it(label, fn, call):
    """`look(impasto=)` is the case the check above misses: `impasto` *is* named on
    the page, on `export`'s line, and was missing from the one call a painter reads
    to find out what looking can do."""
    missing = [p for p in _optional(fn)
               if not re.search(rf"(?<![\w.]){re.escape(p)}\b", call)]
    assert not missing, (
        f"REFERENCE.md writes {label} out in full and leaves out "
        f"{', '.join(missing)}:\n{call}"
    )


# -- the verb x hold matrix ------------------------------------------------------------
def _hold_matrix() -> list[tuple[str, str, str, str]]:
    """*Which verb takes which hold*, as rows of (verb, clip, solid, edge)."""
    rows = []
    for line in TEXT.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 4 and re.fullmatch(r"`\w+\(\)`", cells[0]) and cells[1] in (
                "yes", "no"):
            rows.append((cells[0].strip("`").removesuffix("()"), *cells[1:]))
    return rows


MATRIX = _hold_matrix()


def test_the_matrix_still_has_every_verb_that_lays_paint():
    """A guard on the guard: a scrape that stops finding rows passes by finding none."""
    assert {verb for verb, _, _, _ in MATRIX} == {
        "stroke", "dab", "smudge", "glaze", "block_in", "sweep", "scumble", "cover"}


def _call(s, verb: str, **kw):
    """One of each verb, as small as it can be, with ``kw`` on the end of it."""
    place = Region(0.2, 0.2, 0.8, 0.6, name="place")
    path = [(0.2, 0.3), (0.8, 0.35)]
    if verb == "stroke":
        return s.stroke(path, "flat", "burnt_umber", size=0.05, **kw)
    if verb == "dab":
        return s.dab(0.5, 0.5, "round_hard", "burnt_umber", size=0.05, **kw)
    if verb == "smudge":
        return s.smudge(path, **kw)
    if verb == "glaze":
        return s.glaze(path, "burnt_umber", **kw)
    if verb == "block_in":
        return s.block_in(place, "flat", "burnt_umber", size=0.05, **kw)
    if verb == "sweep":
        return s.sweep(path, "flat", "burnt_umber", into="down", depth=0.1,
                       size=0.05, **kw)
    if verb == "scumble":
        return s.scumble(place, "burnt_umber", "titanium_white", 4, size=0.05, **kw)
    return s.cover(place, "burnt_umber", size=0.05, **kw)


@pytest.mark.parametrize("verb,clip,solid,edge", MATRIX,
                         ids=[row[0] for row in MATRIX])
def test_the_hold_matrix_is_what_the_verbs_take(tmp_path, verb, clip, solid, edge):
    """Every cell of it, against the call it names -- by making the call rather than by
    reading the signature, because three of these verbs take their holds through
    ``**kw`` and a signature does not show that.

    This is the row that drifted: ``clip=`` was documented as *`stroke`, `glaze`* and
    was a named argument of ``stroke`` alone, so four verbs answered a question about
    where their paint may land with *`clip=` is not a brush field*.
    """
    s = Session(160, 120, seed=4, timelapse=False, out_dir=tmp_path).scratch(
        count_only=True)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        if clip == "yes":
            _call(s, verb, clip=Region(0.0, 0.0, 0.5, 1.0))
        else:
            with pytest.raises(TypeError):
                _call(s, verb, clip=Region(0.0, 0.0, 0.5, 1.0))
        if solid == "yes":
            _call(s, verb, solid=True)
        else:
            with pytest.raises(TypeError):
                _call(s, verb, solid=True)
        if "`" in edge:                       # the cell names the values it takes
            for value in re.findall(r"`(\w+)`", edge):
                _call(s, verb, edge=value)
            with pytest.raises(ValueError):
                _call(s, verb, edge="nonsense")
        elif edge == "—":
            with pytest.raises(TypeError):
                _call(s, verb, edge="hard")


# -- the extents behind the region names -----------------------------------------------
def test_the_places_table_is_the_places():
    """`region("bottom")` is a **ninth** -- x 0.333-0.667, y 0.667-1.000 -- because the
    nine are cells of a 3x3, and a painter reached for it meaning the foreground band,
    blocked one in, and got the middle of one. The page listed the names and none of
    their extents, so there was nowhere to find that out short of printing one."""
    from easel.regions import _NAMED

    rows = {}
    for line in TEXT.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 3 and re.fullmatch(r"`[a-z-]+`", cells[0]) and all(
                re.fullmatch(r"`\d\.\d+`-`\d\.\d+`", c) for c in cells[1:]):
            x0, x1 = (float(v) for v in re.findall(r"\d\.\d+", cells[1]))
            y0, y1 = (float(v) for v in re.findall(r"\d\.\d+", cells[2]))
            rows[cells[0].strip("`")] = (x0, y0, x1, y1)
    assert set(rows) == set(_NAMED), "REFERENCE.md lists a region the engine has not"
    for name, box in rows.items():
        assert box == pytest.approx(_NAMED[name], abs=0.001), name


@pytest.mark.parametrize("name", ["undo", "log", "replay"])
def test_the_calls_that_count_records_say_records(name):
    """`undo`'s own docstring said *scrape back n strokes* and `log(last=)` said
    nothing at all, while `replay(upto=)` said records: all three count log entries,
    and a dry or a pencil line is one of those and is free. A painter asked which,
    because the three answers did not agree."""
    from easel.session import Session

    doc = getattr(Session, name).__doc__ or ""
    assert "record" in doc.lower(), f"Session.{name} does not say what it counts"


def test_the_shell_says_records_for_undo_too():
    """The docstrings came to agree and the shell did not: `easel undo`'s help still
    said *scrape back N strokes*, a fourth answer to the question the three
    docstrings were fixed to answer once."""
    sub = next(a for a in build_parser()._actions if hasattr(a, "choices") and a.choices)
    said = {c.dest: c.help for c in sub._choices_actions}
    assert "record" in said["undo"]
