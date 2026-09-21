"""What a recipe looks like when it goes wrong, drawn beside it: ``easel demo``.

Finding 19 of the 0.5.0 cohort asked for *small runnable visual comparisons: the
recommended call, what it looks like, the common failure, the smallest fix*, and said
what they were for: *the documentation sometimes compensates for difficult tool
behaviour with additional rules*. A failure described in words is one more rule to
carry; the same failure painted beside the call that does not make it is a picture a
rehearsal can be held against.

A demo is one code block in ``RECIPES.md``, under its recipe's *Goes wrong as*, cut
into sections by three comment lines::

    # the passage: two masses that meet              (optional)
    s.block_in(...)
    # goes wrong: smudge-across
    s.smudge(...)
    # the smallest fix: along the join               (optional)
    s.smudge(...)

The passage is laid first, under every panel. The first panel is the recipe's own
block, on that passage; the second is what goes wrong; the third, when there is one,
is the smallest change that mends the second -- and when there is none, the recipe
itself is the fix.

**What goes wrong names what the tool says about it**: a notice code, as the call
prints it; ``report() says "<words>"`` for a line of the post-pass check, in the
check's own words, because its rules carry no codes -- the notice channel is for what
is said at the call; or ``nothing says so``, for a failure only looking can find,
which is a claim too and is held like the others. Several are joined with ``;``.

:func:`faults` is the invariant ``scripts/check_guide_blocks.py`` holds every demo
to: the failure trips exactly what it names, and the recipe and the fix trip none of
it and say nothing at the call. So a recipe cannot quietly start producing the fault
its own paragraph warns about -- finding 1, a painter who laid *a mass built of
planes* character for character and got the staircase -- and a failure block cannot
quietly stop failing, which would leave a picture of a fault the tool no longer
makes and a line saying the tool catches it.
"""

from __future__ import annotations

import re
import textwrap
import warnings
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
from PIL import Image

from easel import docs
from easel.diagnosis import _words as _content_words
from easel.look import label_sheet, render_look, save_look
from easel.notices import NOTICES, Notice

__all__ = [
    "Demo", "Panel", "Recipe", "answer", "demos", "draw", "faults", "find", "focus",
    "is_demo", "lay", "listing", "notes", "panels", "preamble", "recipes", "sheet", "slug",
]

#: The three comment lines a demo block is cut by, and the one way of naming nothing.
PASSAGE = "# the passage"
GOES_WRONG = "# goes wrong:"
FIX = "# the smallest fix"
NOTHING = "nothing says so"

_BLOCK = re.compile(r"```python\n(.*?)```", re.S)
_REPORT = re.compile(r'^report\(\) says "(?P<words>[^"]+)"$')
_FINDING = "  - "           # how report() prints a finding, as against a standing line
_MOVED = 0.004              # a channel moved further than this was painted: the probes' own
_ENLARGE = 4.0              # a panel is cut to what changed, enlarged at most this much...
_WHOLE = 0.5                # ...unless that is over this share of the canvas already


def preamble(out_dir: str | Path, timelapse: bool = True) -> str:
    """The names the guide's code blocks assume, as the source that binds them.

    Every block in the guide is written as if a painter's session were already open:
    ``s``, a palette with ``dark`` and ``light`` in it, a shape called ``mass``. A
    reader has all of that by the time they reach the block; a block run on its own has
    none of it. This is that context, once: ``scripts/check_guide_blocks.py`` runs
    every block after it and :func:`lay` runs every panel after it, so a block that
    passes the check paints the same picture in the demo.
    """
    return (
        "from easel import Session, Region, region, cell, span, horizon, below, above\n"
        "from easel import blob, ellipse, hull, ribbon, polygon, union\n"
        f"s = Session(400, 300, ground='toned_grey', seed=1, timelapse={bool(timelapse)}, "
        f"out_dir={str(out_dir)!r})\n"
        "p = s.palette\n"
        "s.palette['dark'] = s.palette.mix('ultramarine','burnt_umber',0.45)\n"
        "s.palette['corrected_colour'] = s.palette['dark']\n"
        "s.palette['light'] = s.palette.tint('yellow_ochre', 0.5)\n"
        "s.palette['shadow'] = s.palette['dark']\n"
        "s.palette['mid'] = s.palette['light']\n"
        "s.palette['pale'] = s.palette['light']\n"
        "s.palette['cool'] = s.palette['dark']\n"
        # The lit surface a cast shadow lies on, named the way the guide names it.
        "s.palette['surface'] = s.palette.at_value(s.palette['light'], 0.60)\n"
        "path = [(0.2,0.3),(0.5,0.4),(0.8,0.3)]\n"
        # The guide's landmark blocks assume marks already exist by the time a later
        # block uses s.pt(...), which is true when the guide is read in order.
        "s.mark('top_l', 0.335, 0.315)\n"
        "s.mark('top_r', 0.630, 0.315)\n"
        "s.mark('base', 0.480, 0.715)\n"
        "s.pencil([(0.30, 0.40), (0.50, 0.55)])\n"
        # ...and the same for the plan that preview, rehearse and the paint block share.
        "plan = [{'points': [(0.335, 0.315), (0.40, 0.62)], 'brush': 'liner',\n"
        "         'size': 0.006, 'color': 'light', 'label': 'edge'}]\n"
        # ...and for the masses the guide points at by name once it has built one: a
        # shape to smudge round, a patch to light from the middle, and the bent ribbon
        # the costing blocks weigh against its straight twin.
        "mass = blob(span('D4', 'F6'), 0.22, wobble=0.3, seed=2)\n"
        "patch = ellipse(span('D4', 'F5'))\n"
        "bent = ribbon([(0.20, 0.30), (0.45, 0.62), (0.78, 0.34)], 0.029)\n"
    )


def slug(heading: str) -> str:
    """A heading as its anchor: ``A mark that crosses a boundary`` ->
    ``a-mark-that-crosses-a-boundary``, the way ``RECIPES.md``'s own table links it."""
    kept = re.sub(r"[^a-z0-9 _-]", "", heading.casefold().strip())
    return re.sub(r"\s+", "-", kept)


def is_demo(block: str) -> bool:
    """Whether a code block is a demo rather than a recipe: it has a *goes wrong* line."""
    return any(line.strip().startswith(GOES_WRONG) for line in block.splitlines())


@dataclass(frozen=True)
class Demo:
    """One recipe's demo: the sections of its block, and what the failure names."""

    heading: str
    slug: str
    recipe: str             # the recipe's own first block: the first panel
    passage: str            # laid under every panel; "" for bare ground
    failure: str
    fix: str                # "" when the recipe is the fix
    names: str              # what the failure names, as the block writes it
    codes: tuple[str, ...]  # ...the notice codes among them
    words: tuple[str, ...]  # ...and the report() lines, by words each one contains
    fix_note: str = ""      # what the fix changes, from its comment line

    @property
    def silent(self) -> bool:
        """A failure the tool cannot see, which only looking finds."""
        return not self.codes and not self.words


@dataclass(frozen=True)
class Recipe:
    """One ``##`` section of ``RECIPES.md`` that carries code."""

    heading: str
    slug: str
    blocks: tuple[str, ...]  # every python block, dedented, demos included

    @property
    def recipe(self) -> str:
        """The recipe's own block: its first that is not a demo."""
        return next((b for b in self.blocks if not is_demo(b)), "")

    @property
    def demo(self) -> Demo | None:
        """Its demo, or ``None`` while it has none. A malformed one raises."""
        found = [b for b in self.blocks if is_demo(b)]
        if not found:
            return None
        if len(found) > 1:
            raise ValueError(f"{self.heading!r} has {len(found)} demo blocks; a recipe "
                             f"has one, which shows its commonest failure.")
        return _parse(self, found[0])


def recipes(text: str | None = None) -> list[Recipe]:
    """Every recipe in ``RECIPES.md`` that has code, in the order the file writes them.

    ``text`` reads a draft instead of the shipped file. Read fresh each call: the
    document is a file an editor has open while this is being worked on.
    """
    source = docs.read("recipes") if text is None else text
    lines = source.splitlines(keepends=True)
    found = [(i, line) for i, level, line in docs.headings("recipes", source) if level == 2]
    out: list[Recipe] = []
    for n, (start, line) in enumerate(found):
        end = found[n + 1][0] if n + 1 < len(found) else len(lines)
        blocks = tuple(textwrap.dedent(b) for b in _BLOCK.findall("".join(lines[start:end])))
        if blocks:
            heading = line.lstrip().lstrip("#").strip()
            out.append(Recipe(heading, slug(heading), blocks))
    return out


def demos(text: str | None = None) -> list[Demo]:
    """Every demo there is, parsed -- so a malformed one raises here, naming its recipe."""
    return [d for d in (r.demo for r in recipes(text)) if d is not None]


def _named(names: str, heading: str) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """What a *goes wrong* line names: notice codes, and report() lines by their words."""
    if names == NOTHING:
        return (), ()
    codes: list[str] = []
    words: list[str] = []
    for part in (p.strip() for p in names.split(";")):
        said = _REPORT.match(part)
        if said:
            words.append(said["words"])
        elif part in NOTICES:
            codes.append(part)
        else:
            raise ValueError(
                f"The demo under {heading!r} says it goes wrong as {part!r}, which is "
                f"neither a notice code the engine has, nor report() says \"<words>\", "
                f"nor {NOTHING!r}. `easel explain` lists the codes."
            )
    return tuple(codes), tuple(words)


def _parse(recipe: Recipe, block: str) -> Demo:
    """Cut a demo block into its sections."""
    sections: dict[str, list[str]] = {}
    remarks: dict[str, str] = {}
    names = ""
    current = ""
    for line in block.splitlines():
        text = line.strip()
        for key, marker in (("passage", PASSAGE), ("failure", GOES_WRONG), ("fix", FIX)):
            if text.startswith(marker):
                if key in sections:
                    raise ValueError(f"The demo under {recipe.heading!r} has two "
                                     f"{marker!r} lines.")
                if (key == "passage" and sections
                        or key == "failure" and "fix" in sections
                        or key == "fix" and "failure" not in sections):
                    raise ValueError(f"The demo under {recipe.heading!r} is out of order: "
                                     f"the passage, then what goes wrong, then the fix.")
                sections[key] = []
                rest = text[len(marker):].strip()
                if key == "failure":
                    names = rest
                else:
                    remarks[key] = rest.removeprefix(":").strip()
                current = key
                break
        else:
            if current:
                sections[current].append(line)
            elif text:
                raise ValueError(f"The demo under {recipe.heading!r} has code before its "
                                 f"first section line.")
    if "failure" not in sections or not names:
        raise ValueError(f"The demo under {recipe.heading!r} has no {GOES_WRONG!r} line "
                         f"naming what the tool says about it.")
    codes, words = _named(names, recipe.heading)

    def src(key: str) -> str:
        return "\n".join(sections.get(key, [])).strip("\n") + ("\n" if key in sections else "")

    return Demo(recipe.heading, recipe.slug, recipe.recipe, src("passage"), src("failure"),
                src("fix"), names, codes, words, remarks.get("fix", ""))


# -- painting the panels --------------------------------------------------------------
@dataclass
class Panel:
    """One panel of a demo, and what the tool said while it was laid."""

    label: str
    image: Image.Image | None = None
    said: list[Notice] = field(default_factory=list)          # at this panel's calls
    passage_said: list[Notice] = field(default_factory=list)  # at the passage's
    found: list[str] = field(default_factory=list)            # report()'s findings
    box: tuple[int, int, int, int] | None = None              # where it changed, in px
    error: str = ""

    @property
    def codes(self) -> list[str]:
        """The codes said, once each, in the order first said."""
        return list(dict.fromkeys(n.code for n in self.said))


def lay(passage: str, body: str, out_dir: str | Path, label: str) -> Panel:
    """A fresh session, the preamble, the passage, then ``body``; and what was said.

    Notices are read off the session rather than caught as warnings, so the order and
    the count are the engine's own; the warnings themselves are silenced, since the
    panel says what they said. The check is ``report()`` over ``body`` alone, and the
    panel keeps the box ``body`` changed, which is what :func:`sheet` enlarges.

    No time-lapse: nothing here keeps a frame, and building one after every mark is
    work a panel would throw away.
    """
    panel = Panel(label)
    scope: dict = {}
    opened = said = laid = 0
    before = None
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        try:
            exec(compile(preamble(out_dir, timelapse=False), "<preamble>", "exec"),  # noqa: S102
                 scope)
            opened = len(scope["s"].notices())
            exec(compile(passage, f"<{label}: the passage>", "exec"), scope)  # noqa: S102
            said, laid = len(scope["s"].notices()), len(scope["s"].history.records)
            before = scope["s"].canvas.rgb.copy()
            exec(compile(body, f"<{label}>", "exec"), scope)  # noqa: S102
        except Exception as exc:  # the panel reports it; faults() turns it into a fault
            panel.error = f"{type(exc).__name__}: {exc}"
        s = scope.get("s")
        if s is None:
            return panel
        every = s.notices()
        panel.passage_said = every[opened:said]
        panel.said = every[said:]
        report = s.report(since=laid)
        panel.found = [line[len(_FINDING):] for line in report.splitlines()
                       if line.startswith(_FINDING)]
        if before is not None and before.shape == s.canvas.rgb.shape:
            moved = np.abs(s.canvas.rgb - before).max(axis=2) > _MOVED
            ys, xs = np.nonzero(moved)
            if xs.size:
                panel.box = (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)
        panel.image = render_look(s.canvas, scale=None, sketch=False)
    return panel


def panels(demo: Demo, out_dir: str | Path) -> list[Panel]:
    """The recipe, what goes wrong, and the fix when there is one -- each on the passage."""
    out = [lay(demo.passage, demo.recipe, out_dir, "the recipe"),
           lay(demo.passage, demo.failure, out_dir, "goes wrong")]
    if demo.fix:
        out.append(lay(demo.passage, demo.fix, out_dir, "the smallest fix"))
    return out


def faults(demo: Demo, drawn: list[Panel]) -> list[str]:
    """What is wrong with a demo, as painted: empty when it shows what it says.

    The failure trips exactly what it names -- no code more or fewer, every report()
    line it names and no other -- and the recipe and the fix say nothing at the call
    and trip none of the failure's report() lines. Findings of their own that the
    failure does not name are not faults here: `report()` has rules a recipe can
    trip without being the failure this demo is about, and those are the check's
    business rather than the demo's.
    """
    out = [f"{p.label} raised {p.error}" for p in drawn if p.error]
    if drawn and drawn[0].passage_said:
        out.append(f"the passage says {_codes(drawn[0].passage_said)}: it is laid under "
                   f"every panel, so it must say nothing")
    recipe, failure, *rest = drawn
    said = set(failure.codes)
    if said != set(demo.codes):
        out.append(f"goes wrong names {demo.names!r}, and the calls said "
                   f"{', '.join(failure.codes) or 'nothing'}")
    for line in failure.found:
        if not any(w in line for w in demo.words):
            out.append(f"goes wrong: report() also says {line!r}, which the demo does not "
                       f"name")
    for w in demo.words:
        if not any(w in line for line in failure.found):
            out.append(f"goes wrong names report() {w!r}, and report() does not say it")
    for p in (recipe, *rest):
        if p.said:
            out.append(f"{p.label} says {_codes(p.said)} at the call")
        for w in demo.words:
            if any(w in line for line in p.found):
                out.append(f"{p.label}: report() says {w!r}, which is the failure's")
    return out


def notes(demo: Demo, drawn: list[Panel]) -> list[str]:
    """What ``report()`` says about the recipe and the fix that the failure does not name.

    Not a fault of the demo -- :func:`faults` says why -- but the question
    ``LESSONS.md``'s rule 2 asks of every rule: *what does it say to a painter doing
    the right thing?* A recipe that trips a finding of the post-pass check is either a
    recipe that is wrong or a rule that is, and the guide-block check is the one place
    that asks it of every recipe at once.
    """
    out = []
    for p in drawn:
        if p.label == "goes wrong":
            continue
        out += [f"{p.label}: report() says {line!r}" for line in p.found
                if not any(w in line for w in demo.words)]
    return out


def _codes(notices: list[Notice]) -> str:
    return ", ".join(dict.fromkeys(n.code for n in notices))


def focus(drawn: list[Panel], width: int, height: int) -> tuple[int, int, int, int] | None:
    """The part of the canvas worth enlarging: where any panel changed, padded.

    A demo is about one mark as often as about one mass, and five discs of a 5 px
    brush on a whole canvas are five dots nobody can compare. So every panel is cut to
    the same box -- the union of what each changed, a quarter again round it, grown to
    the canvas's own shape -- and enlarged, at most four times, so a pixel of the
    failure is never blown up into a claim. ``None`` when that box is most of the
    canvas anyway, and the whole canvas is shown.
    """
    boxes = [p.box for p in drawn if p.box]
    if not boxes:
        return None
    x0, y0 = min(b[0] for b in boxes), min(b[1] for b in boxes)
    x1, y1 = max(b[2] for b in boxes), max(b[3] for b in boxes)
    pad = max(16.0, 0.25 * max(x1 - x0, y1 - y0))
    w = max(x1 - x0 + 2 * pad, width / _ENLARGE)
    h = max(y1 - y0 + 2 * pad, height / _ENLARGE)
    if w / h < width / height:
        w = h * width / height
    else:
        h = w * height / width
    w, h = min(w, width), min(h, height)
    if w * h > _WHOLE * width * height:
        return None
    left = min(max(0.0, (x0 + x1 - w) / 2), width - w)
    top = min(max(0.0, (y0 + y1 - h) / 2), height - h)
    return int(left), int(top), int(left + w), int(top + h)


def sheet(demo: Demo, drawn: list[Panel]) -> Image.Image:
    """The panels side by side, each labelled with what it is, cut to :func:`focus`.

    The failure's label is what it names, with a report() line as its quoted words
    alone: a panel is 400 px, and *report() says* twice runs off it.
    """
    named = "; ".join([*demo.codes, *(f'"{w}"' for w in demo.words)]) or NOTHING
    labels = {"the recipe": "the recipe",
              "goes wrong": f"goes wrong: {named}",
              "the smallest fix": "the smallest fix"}
    size = next((p.image.size for p in drawn if p.image is not None), (400, 300))
    box = focus(drawn, *size)
    out = []
    for p in drawn:
        image = p.image or Image.new("RGB", size, (24, 24, 24))
        if box is not None:
            image = image.crop(box).resize(size, Image.LANCZOS)
        out.append((labels.get(p.label, p.label), image))
    return label_sheet(out, columns=len(drawn))


def draw(demo: Demo, out_dir: str | Path = "out",
         path: str | Path | None = None) -> tuple[Path, list[Panel]]:
    """Paint a demo's panels and write the sheet. Returns where it went, and the panels."""
    drawn = panels(demo, out_dir)
    target = Path(path) if path is not None else Path(out_dir) / f"demo-{demo.slug}.png"
    return save_look(sheet(demo, drawn), target), drawn


# -- the command ----------------------------------------------------------------------
def find(words: str, text: str | None = None) -> list[Recipe]:
    """The recipes ``words`` names: by anchor, or by every content word of the heading."""
    every = recipes(text)
    exact = [r for r in every if r.slug == slug(words.replace("-", " "))]
    if exact:
        return exact
    wanted = set(_content_words(words))
    return [r for r in every if wanted and wanted <= set(_content_words(r.heading))]


def listing(text: str | None = None) -> str:
    """Every recipe, and what its demo shows going wrong -- or that it has none yet."""
    rows = []
    for r in recipes(text):
        d = r.demo
        rows.append(f"  {r.slug:52s} {d.names if d else '(no demo yet)'}")
    return ("`easel demo <recipe>` paints a recipe beside what it looks like when it goes "
            "wrong, and the smallest fix.\nName it by its heading -- `easel demo crosses a "
            "boundary` is enough.\n\n" + "\n".join(rows) + "\n")


def answer(words: str, out_dir: str | Path = "out",
           path: str | Path | None = None) -> tuple[str, Path | None]:
    """What ``easel demo <words>`` prints, and the sheet it wrote if it wrote one."""
    if not words.strip():
        return listing(), None
    found = find(words)
    if not found:
        return f"No recipe's heading has all of {words!r} in it.\n\n{listing()}", None
    if len(found) > 1:
        names = "\n".join(f"  {r.slug}" for r in found)
        return f"{words!r} names {len(found)} recipes; say which:\n{names}\n", None
    recipe = found[0]
    demo = recipe.demo
    if demo is None:
        return (f"*{recipe.heading}* has no demo yet: its *Goes wrong as* is still words "
                f"only. `easel guide --recipes` has the recipe.\n"), None
    written, drawn = draw(demo, out_dir, path)
    return _summary(demo, drawn, written), written


def _summary(demo: Demo, drawn: list[Panel], written: Path) -> str:
    """The sheet's path, what each panel was told, the words, and the calls that differ.

    The failure's notices and findings are quoted whole, because they are what a
    painter would read at the call or after the pass: a demo that only named the code
    would be teaching the name of the warning rather than what it says.
    """
    lines = [f"{demo.heading}: {written}", ""]
    for p in drawn:
        if p.error:
            heard = f"raised {p.error}"
        else:
            parts = [f"the call says {c}" for c in p.codes]
            if p.found:
                parts.append(f"report() says {len(p.found)} "
                             f"thing{'s' if len(p.found) != 1 else ''}")
            heard = "; ".join(parts) or "nothing said"
        lines.append(f"  {p.label:17s} {heard}")
    failure = next(p for p in drawn if p.label == "goes wrong")
    told = ([f"{n.code}: {n.text}" for n in failure.said]
            + [f"report(): {line}" for line in failure.found])
    if told:
        lines += ["", "what goes wrong is told:"]
        lines += [textwrap.fill(t, 88, initial_indent="    ", subsequent_indent="    ")
                  for t in dict.fromkeys(told)]
    lines.append("")
    if demo.passage:
        lines += ["the passage, under every panel:", _code(demo.passage)]
    lines += ["goes wrong:", _code(demo.failure)]
    if demo.fix:
        note = f" -- {demo.fix_note}" if demo.fix_note else ""
        lines += [f"the smallest fix{note}:", _code(demo.fix)]
    else:
        lines.append(f"the fix is the recipe itself: *{demo.heading}*, in "
                     f"`easel guide --recipes`.")
    codes = [c for p in drawn for c in p.codes]
    if codes:
        lines += ["", "`easel explain <code>` has the measurement behind "
                  + ", ".join(dict.fromkeys(codes)) + "."]
    return "\n".join(lines).rstrip() + "\n"


def _code(source: str) -> str:
    return textwrap.indent(source.rstrip("\n"), "    ")
