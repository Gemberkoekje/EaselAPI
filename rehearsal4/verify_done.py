"""Check the brief's *Definition of done* against the artefacts, not the reports.

The brief asks for:

    A fresh session, given `PAINTER.md` and a reference photo, produces a
    recognizable copy in under 300 strokes without touching source code, then
    produces **two** paintings with no prompt. All exports plus their time-lapses
    exist. [...] the human recognises the object, `compare()` reports no
    **reachable** cell on it more than `0.10` from the reference's value, and the
    painter can point to strokes it rejected in `preview()` or `rehearse()`.

Recognition is the human's call, and the rejected marks are in each `LOG.md`.
Everything else is a number, and every number here is re-measured from the exported
PNGs and the saved sessions. Where a painter's log and this script disagree, this
script wins.

The `unreachable` split stays reported, but since M6b the palette floors at `0.128`
and the criterion is **every cell on the object**. A run that finds more than a
handful out of reach has found something about the reference, not about the palette.

Run from the repo root:  python rehearsal4/verify_done.py
"""
from __future__ import annotations

import json
import os
import re
import subprocess

import numpy as np
from PIL import Image

from easel.measure import compare_images
from easel.palette import Palette

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

THRESHOLD = 0.10
#: The darkest value in the box, asked of the palette rather than hard-coded, so
#: this script cannot go stale against a change to the pigments.
FLOOR = Palette().darkest_value

#: How many marks the guide lets a painter sign with, free of the stroke budget.
#: Marks claiming the exemption must carry `note="signature"`; anything past this
#: many is charged, so the exemption cannot be spent on painting.
SIGNATURE_ALLOWANCE = 5

#: The cells the mug covers in Level1.jpg, read off `_ref_grid_mug.png`. This is
#: REHEARSAL3's list unchanged, so the two runs are directly comparable; cells that
#: are mostly table or cast shadow are excluded, because the criterion says "on the
#: object".
MUG_CELLS = [
    "D2", "E2",
    "D3", "E3", "F3",
    "D4", "E4", "F4",
    "D5", "E5", "F5",
    "D6", "E6",
]
#: The same, plus the cells the mug only clips. Reported alongside so the choice of
#: mask cannot flatter the result.
MUG_CELLS_WIDE = MUG_CELLS + ["C3", "C4", "C5", "F2", "G4"]

#: The sitter's head in Level3.jpg, read off `_ref_grid_sitter.png`: hair on row 2,
#: the face from the brow down through the beard on 3-5.
SITTER_HEAD = ["D2", "E2", "D3", "E3", "D4", "E4", "F4", "D5", "E5"]
#: Head plus the coat mass. The coat is the darkest thing in the photograph, so this
#: is the mask that tests the floor.
SITTER_FIGURE = SITTER_HEAD + [
    "F2", "F3", "F5", "G5",
    "D6", "E6", "F6", "G6",
    "D7", "E7", "F7", "G7",
]


# -- artefacts ------------------------------------------------------------------

REQUIRED = [
    ("pass/copy_final.png", "the copy, mug"),
    ("pass/copy_timelapse.gif", "its time-lapse"),
    ("pass/own1_final.png", "unprompted 1"),
    ("pass/own1_timelapse.gif", "its time-lapse"),
    ("pass/own2_final.png", "unprompted 2"),
    ("pass/own2_timelapse.gif", "its time-lapse"),
    ("sitter/copy_final.png", "the copy, sitter"),
    ("sitter/copy_timelapse.gif", "its time-lapse"),
]


def artefacts() -> bool:
    print("\n== Exports and time-lapses ==")
    ok = True
    for rel, what in REQUIRED:
        path = f"{HERE}/{rel}"
        if os.path.exists(path):
            kb = os.path.getsize(path) / 1024
            print(f"  ok      {rel:<28} {kb:>9,.0f} KB   {what}")
        else:
            ok = False
            print(f"  MISSING {rel:<28} {'':>9}      {what}")
    return ok


# -- stroke counts, straight out of the saved sessions ---------------------------

def sessions() -> None:
    print("\n== Stroke counts (from the .easel files, not the logs) ==")
    print(f"  {'session':<30} {'strokes':>7} {'budget':>7} {'assisted':>9}  kinds")
    for rel in sorted(_find(".easel")):
        path = f"{HERE}/{rel}"
        with np.load(path, allow_pickle=False) as z:
            meta = json.loads(str(z["meta"]))
            log = json.loads(str(z["log"]))
        kinds: dict[str, int] = {}
        for record in log:
            kinds[record["kind"]] = kinds.get(record["kind"], 0) + 1
        # `stroke_count` is what the painter is charged for; pencil and erase are
        # free by design, so they show in the breakdown and not in the number.
        # The signature is free too, up to SIGNATURE_ALLOWANCE marks -- the guide
        # grants it on condition the marks are noted, and this is where that is
        # honoured. Anything past the allowance is charged, so the exemption cannot
        # be used to buy strokes.
        signed = sum(1 for r in log if "signature" in str(r.get("note", "")).lower())
        free = min(signed, SIGNATURE_ALLOWANCE)
        count = meta["stroke_count"] - free
        if signed:
            kinds["signature"] = signed
        budget = "300" if "copy" in rel else "-"
        flag = "" if budget == "-" or count < 300 else "   OVER BUDGET"
        if signed > SIGNATURE_ALLOWANCE:
            flag += f"   SIGNATURE OVER {SIGNATURE_ALLOWANCE} ({signed})"
        # The engine records every assisted call itself, so "the pencil is the
        # painter's own" is checked here rather than taken from a painter's word.
        # A pre-M8b session has no field at all, which is not the same as empty.
        assisted = meta.get("assisted", None)
        mark = "none" if assisted == [] else ("(no field)" if assisted is None
                                              else f"USED {len(assisted)}")
        breakdown = ", ".join(f"{k} {v}" for k, v in sorted(kinds.items()))
        print(f"  {rel:<30} {count:>7} {budget:>7} {mark:>9}  {breakdown}{flag}")


def _find(suffix: str) -> list[str]:
    out = []
    for dirpath, _, names in os.walk(HERE):
        for name in names:
            if name.endswith(suffix):
                out.append(os.path.relpath(os.path.join(dirpath, name), HERE)
                           .replace("\\", "/"))
    return out


# -- the value criterion ---------------------------------------------------------

def check(painting: str, reference: str, cells: list[str], label: str) -> None:
    path = f"{HERE}/{painting}"
    if not os.path.exists(path):
        print(f"\n{label}: missing ({painting})")
        return
    canvas = np.asarray(Image.open(path).convert("RGB"))
    ref = np.asarray(Image.open(reference).convert("RGB"))
    comparison = compare_images(canvas, ref, threshold=THRESHOLD, floor=FLOOR)
    by_label = {c.label: c for c in comparison.cells}

    on_object = [by_label[name] for name in cells if name in by_label]
    out = [c for c in on_object if abs(c.delta) > THRESHOLD]
    unreachable = [c for c in out if c.ref < FLOOR - THRESHOLD]
    real = [c for c in out if c not in unreachable]

    verdict = "PASS" if not out else ("PASS (all out of reach)" if not real else "FAIL")
    print(f"\n{label}   -> {verdict}")
    print(f"  cells on the object      {len(on_object)}")
    print(f"  more than {THRESHOLD:.2f} out       {len(out)}")
    print(f"    of those, unreachable  {len(unreachable)}"
          f"  (reference below the {FLOOR:.3f} floor)")
    print(f"    of those, the painter's {len(real)}")
    for c in sorted(out, key=lambda c: -abs(c.delta)):
        tag = "unreachable" if c in unreachable else "painter's"
        print(f"    {c.label}  ref {c.ref:.2f}  canvas {c.canvas:.2f}  "
              f"{c.delta:+.2f}   {tag}")
    whole = [c for c in comparison.cells if abs(c.delta) > THRESHOLD]
    print(f"  whole picture            {len(whole)} of {len(comparison.cells)} out")


# -- did the painter judge a mark before paying for it? --------------------------

def planning() -> None:
    """Count `preview` and `rehearse` looks per run.

    The pass clause is three things and the third is about *when* a mark is judged:
    "the painter can point to strokes it rejected in `preview()` or `rehearse()`
    **before painting them**". A rejected-marks table full of marks that were painted
    and then painted over does not meet it, however honest the table is -- so this
    counts the tools that judge a mark for free, from the files they write.
    """
    print("\n== Marks judged before they were paid for ==")
    print(f"  {'run':<10} {'preview':>8} {'rehearse':>9}   verdict")
    for run in ("pass", "sitter"):
        out = f"{HERE}/{run}/out"
        names = os.listdir(out) if os.path.isdir(out) else []
        previews = sum(1 for n in names if n.startswith("preview"))
        rehearsals = sum(1 for n in names if n.startswith("rehearse"))
        verdict = ("used both" if previews and rehearsals else
                   "NEITHER - marks were judged only after painting"
                   if not previews and not rehearsals else
                   "one of the two only")
        print(f"  {run:<10} {previews:>8} {rehearsals:>9}   {verdict}")


# -- did the painter reach for shapes? -------------------------------------------

SHAPE_CALLS = ("blob(", "ellipse(", "hull(", "ribbon(", "polygon(", "sweep(")


def shapes() -> None:
    print("\n== Shaped masses (M8) - what the painters' own scripts called ==")
    for run in ("pass", "sitter"):
        counts: dict[str, int] = {}
        scripts = 0
        for dirpath, _, names in os.walk(f"{HERE}/{run}"):
            for name in names:
                if not name.endswith(".py"):
                    continue
                scripts += 1
                text = open(os.path.join(dirpath, name), encoding="utf-8",
                            errors="replace").read()
                for call in SHAPE_CALLS:
                    n = len(re.findall(r"(?<![\w.])" + re.escape(call), text))
                    if n:
                        counts[call[:-1]] = counts.get(call[:-1], 0) + n
        found = ", ".join(f"{k} x{v}" for k, v in sorted(counts.items())) or "none"
        print(f"  {run:<8} {scripts:>3} scripts   {found}")


# -- how square is each picture? -------------------------------------------------

def _axis_probe():
    """REHEARSAL3's edge-angle probe, loaded by path rather than copied.

    The number only means anything next to the numbers it was published with, so
    this run measures with the same code rather than a re-implementation of it.
    """
    import importlib.util  # noqa: PLC0415 - only needed here

    src = f"{ROOT}/rehearsal3/probe_axis_alignment.py"
    spec = importlib.util.spec_from_file_location("probe_axis_alignment", src)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.axis_share


def axes() -> None:
    axis_share = _axis_probe()

    print("\n== Axis alignment (share of strong edges within 10 deg of an axis) ==")
    rows = [
        ("Level1 (the mug photo)", "C:/temp/Level1.jpg"),
        ("pass copy (mug)", f"{HERE}/pass/copy_final.png"),
        ("Level3 (the sitter photo)", "C:/temp/Level3.jpg"),
        ("sitter copy", f"{HERE}/sitter/copy_final.png"),
        ("unprompted 1", f"{HERE}/pass/own1_final.png"),
        ("unprompted 2", f"{HERE}/pass/own2_final.png"),
        ("REHEARSAL3 unprompted", f"{ROOT}/rehearsal3/pass/own_final.png"),
    ]
    width = max(len(n) for n, _ in rows)
    for name, path in rows:
        if not os.path.exists(path):
            print(f"  {name:<{width}}  (missing)")
            continue
        print(f"  {name:<{width}}  {axis_share(path):5.1f} %")


# -- was any source touched? -----------------------------------------------------

def untouched() -> None:
    print("\n== 'without touching source code' ==")
    dirty = subprocess.run(
        ["git", "status", "--porcelain", "--",
         "src", "tests", "scripts", "examples", "PAINTER.md", "CALIBRATION.md"],
        cwd=ROOT, capture_output=True, text=True, check=False).stdout.strip()
    if dirty:
        print("  CHANGED:")
        for line in dirty.splitlines():
            print(f"    {line}")
    else:
        print("  clean: no change to src/, tests/, scripts/, examples/, "
              "PAINTER.md or CALIBRATION.md")


if __name__ == "__main__":
    print("The brief's definition of done, measured from the artefacts.")
    print(f"Palette floor {FLOOR:.3f}; threshold {THRESHOLD:.2f}.")

    artefacts()
    sessions()

    print("\n== The value criterion ==")
    check("pass/copy_final.png", "C:/temp/Level1.jpg", MUG_CELLS,
          "THE PASS - mug, cells on the object")
    check("pass/copy_final.png", "C:/temp/Level1.jpg", MUG_CELLS_WIDE,
          "THE PASS - mug, plus the cells it only clips")
    check("sitter/copy_final.png", "C:/temp/Level3.jpg", SITTER_HEAD,
          "REACH - sitter, the head")
    check("sitter/copy_final.png", "C:/temp/Level3.jpg", SITTER_FIGURE,
          "REACH - sitter, head and coat")

    planning()
    shapes()
    axes()
    untouched()
