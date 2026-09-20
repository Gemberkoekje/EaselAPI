"""The symptom index, answered rather than grepped.

`DIAGNOSIS.md` is the one document in this project that is not meant to be read.
Every row is a description of something wrong on the canvas and a pointer at the
passage that says why; the row carries no content of its own, deliberately, because
a sixth copy of the guide is the failure this repository has already watched twice.
The intended interface was `grep -i rings DIAGNOSIS.md`, and then opening whichever
file the pointer named and finding the heading by hand.

**The one session ever handed the index followed zero pointers in 293 strokes.** It
recognised five rows on sight -- *staircase*, *venetian blind*, *floating discs*,
*searchlight that owns the picture*, *paper cut-out* -- and repaired each from the
remembered description. A recalled row has no measurement attached, which is the
entire difference between the index and its targets: it repaired the chisel
staircase with `edge="clean"` while the row's own target held a cheaper repair at
the other end of the same table. `SUGGESTIONS.md` files that at n=1, and
`LESSONS.md` asked that the file not be changed on one observation.

So the file does not change. What changes is the price of following a pointer, and
this module drops it to nothing: `easel diagnose <words>` matches the words against
the rows and prints **the passage**, not the pointer. There is no step left to skip,
which is a better answer than a row that explains itself -- that row would be the
fourth copy the page refuses.

The other half is that a painter who ran `pip install easel-paint` never had the
index at all. It was not one of the five documents the build shipped, so `grep` was
an instruction that only worked from a checkout. It is the sixth now; see
`easel.docs`.

Matching is deliberately dumb -- overlapping words, a light plural rule, no index
and no model. A painter arrives here with the thing in front of them in their own
words (*concentric rings*, *stringy edge*, *the ground shows through*), and the rows
are written in those words on purpose. When nothing overlaps the answer is the list
of what the index does cover, which is a shorter read than the file.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from easel import docs

__all__ = ["Pointer", "Row", "rows", "match", "answer", "passages", "listing"]

#: A pointer as `DIAGNOSIS.md` writes it: `` `FILE.md` -> *Heading* ``, several to a
#: row, separated by `;`. The heading is a prefix -- a row may name a section without
#: repeating all of it -- and `docs.heading_line` is what resolves one.
#: `tests/test_diagnosis.py` parses the same shape to hold every pointer to a heading
#: that exists; the two regexes are the same rule written twice on purpose, so that a
#: change to the file's format fails the index test rather than silently emptying this.
_POINTER = re.compile(r"`([A-Z]+\.md)`\s*->\s*\*([^*]+)\*")

#: Filename back to the key `easel.docs` knows it by, so a row can name `PAINTER.md`
#: and this can ask for `"guide"`.
_BY_FILENAME = {filename: key for key, filename in docs.DOCUMENTS.items()}

#: Words that carry nothing in a description of a picture. Short enough to read, and
#: it only has to beat the noise from *a*, *the* and *that*, which every row has.
_STOPWORDS = frozenset("""
    a an and any are as at be been but by came come does for from get given goes had
    has have how in into is it its just like make more most no not of off on one only
    or out over run see so some still than that the their them then there they this
    to too up was way were what when where which who why will with you your
""".split())


@dataclass(frozen=True)
class Pointer:
    """One target of one row: a document and the heading in it that holds the reason."""

    #: The filename as the row writes it, e.g. `"CALIBRATION.md"`.
    document: str
    #: The heading as the row writes it, without `#`s and possibly only its front.
    heading: str

    @property
    def key(self) -> str:
        """The name `easel.docs` knows the document by."""
        return _BY_FILENAME[self.document]

    def passage(self) -> str:
        """The section itself. Raises `KeyError` if the heading has moved."""
        return docs.section(self.key, docs.heading_line(self.key, self.heading))


@dataclass(frozen=True)
class Row:
    """One row of the index: what you are looking at, and where the reason is."""

    #: The left column: the description of what is wrong on the canvas.
    symptom: str
    #: The `##` heading the row sits under -- *An edge*, *Colour, value, paint*.
    group: str
    #: The right column, in the order the row writes them.
    pointers: tuple[Pointer, ...]


def _words(text: str) -> list[str]:
    """The content words of a phrase, singular, in order.

    The plural rule is the whole of the stemming, because it is the whole of what a
    painter's own words differ by: they type *ring* and the row says *rings*, or the
    other way round. `-es` comes off after a sibilant so that *passes* meets *pass*,
    and a word ending `-ss` is left alone so that *glass* does not become *glas*.
    Anything cleverer would need a test suite of its own to be worth having.
    """
    out = []
    for word in re.findall(r"[a-z_]+", text.casefold().replace("`", " ")):
        if len(word) > 4 and word.endswith(("ses", "xes", "zes", "ches", "shes")):
            word = word[:-2]
        elif len(word) > 3 and word.endswith("s") and not word.endswith("ss"):
            word = word[:-1]
        if word not in _STOPWORDS and len(word) > 1:
            out.append(word)
    return out


def rows() -> tuple[Row, ...]:
    """Every row of `DIAGNOSIS.md`, in the order the file writes them.

    Read fresh each call rather than cached at import: the document is a file on
    disk, an editor has it open while this is being worked on, and nothing here is
    hot enough for the difference to matter.
    """
    found: list[Row] = []
    group = ""
    for line in docs.read("diagnosis").splitlines():
        text = line.strip()
        if text.startswith("## "):
            group = text[3:].strip()
            continue
        if not text.startswith("|") or text.startswith("|-"):
            continue
        cells = [cell.strip() for cell in text.strip("|").split("|")]
        if len(cells) != 2:
            continue
        pointers = tuple(
            Pointer(document, heading.strip())
            for document, heading in _POINTER.findall(cells[1])
        )
        # No pointer means the header row, which is the only other `|` line there is.
        if pointers:
            found.append(Row(symptom=cells[0], group=group, pointers=pointers))
    return tuple(found)


def match(words: str, limit: int = 5) -> tuple[Row, ...]:
    """The rows that best fit `words`, best first.

    Ranked on how many distinct words of the question the row accounts for, then on
    what share of the row those words are -- so a short precise row beats a long one
    that happens to contain the same term in passing -- then on the order the file
    writes them, which keeps the answer stable.

    With no overlap anywhere in the symptoms, the groups are tried instead: a painter
    who types *gradient* and hits no row should still be handed the gradient section
    rather than nothing.
    """
    wanted = set(_words(words))
    if not wanted:
        return ()

    for field in ("symptom", "group"):
        scored = []
        for order, row in enumerate(rows()):
            have = _words(getattr(row, field))
            hit = wanted & set(have)
            if hit:
                scored.append((len(hit), len(hit) / len(have), -order, row))
        if scored:
            # Keyed on the first three so the `Row` itself is never compared; `-order`
            # is unique, so the sort is total and the answer does not move between runs.
            scored.sort(key=lambda ranked: ranked[:3], reverse=True)
            return tuple(row for *_, row in scored[:limit])
    return ()


def passages(row: Row) -> str:
    """One row's targets, each headed by where it came from.

    A heading that has been renamed out from under a pointer is reported in place and
    the rest of the row still prints, because the painter is already stuck and the
    second pointer may be the one they needed. `tests/test_diagnosis.py` is what
    stops it happening; this is what it looks like if it does.
    """
    out = []
    for pointer in row.pointers:
        try:
            body = pointer.passage()
        except KeyError as gone:
            body = f"[{gone.args[0]}]\n"
        out.append(f"--- {pointer.document}, {pointer.heading}\n\n{body}")
    return "\n".join(out)


def answer(words: str, limit: int = 5) -> str:
    """What `easel diagnose <words>` prints: the best row's passages, in full.

    One row's targets rather than every match's, because the passages are the whole
    point and four of them at once is the reading this index exists to avoid. The
    rest are listed as their own symptoms, which is enough to ask again in better
    words.

    Asked nothing, it answers with the whole index as symptoms -- which is what a
    painter who does not yet know how to say it needs, and is still not the file.
    """
    if not words.strip():
        return listing()

    found = match(words, limit=limit)
    if not found:
        return (
            f"Nothing in the index matches {words!r}. It is written in the words a "
            f"painter uses for what is in front of them, so describe what you can "
            f"see rather than what you think caused it. It covers:\n\n"
            + "\n".join(f"  {group}" for group in _groups())
            + "\n\nAsk with no words at all for every symptom it has.\n"
        )

    best, rest = found[0], found[1:]
    out = [f"{best.symptom}\n  ({best.group})\n", passages(best)]
    if rest:
        out.append(
            "If that was not it, these also matched -- ask again in more of their "
            "words:\n" + "\n".join(f"  * {row.symptom}" for row in rest) + "\n"
        )
    return "\n".join(out)


def _groups() -> tuple[str, ...]:
    """The `##` headings, in file order and without repeats."""
    return tuple(dict.fromkeys(row.group for row in rows()))


def listing(words: str = "") -> str:
    """Every symptom, or every symptom that matches, grouped as the file groups them.

    The triage half of the command: what `grep` gave a painter in a checkout, without
    the checkout and without the pointers, so that the next question can be asked in
    the index's own words.
    """
    found = match(words) if words.strip() else rows()
    if not found:
        return f"Nothing in the index matches {words!r}.\n"
    out = []
    for group in _groups():
        rows_here = [row for row in found if row.group == group]
        if rows_here:
            out.append(group)
            out += [f"  {row.symptom}" for row in rows_here]
            out.append("")
    return "\n".join(out)
