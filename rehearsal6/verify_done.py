"""The brief's *Definition of done*, measured for REHEARSAL6.

Nothing here re-implements a measurement. `rehearsal4/verify_done.py` already checks
every criterion the brief had when it was written, and it is imported by path and
pointed at this directory, so REHEARSAL4's and REHEARSAL6's numbers come out of the
same instrument and can be put side by side.

What this file adds is the three things the brief gained *after* REHEARSAL4, each of
which exists because a number that could be satisfied by damage was:

**The second number.** `probe_human_notes.py`'s containment -- the share of a mass's
paint that lands where the reference has nothing like it. The brief's reason for it is
that no single mark can improve it and the value number at once.

**The procedural rule.** The last ten charged marks of a copy may not be value
corrections. The log carries the order, so this costs nothing to check; what it cannot
do is read a painter's mind, so it prints the ten and flags the suspicious ones rather
than returning a verdict. The verdict is the write-up's, from the ten marks and the
painter's account of them.

**The signature.** Every finished painting is signed, up to five marks carrying
`note="signature"` and free of the budget. `PAINTER.md` teaches this and neither
prompt mentioned it, so an unsigned painting is a fact about the guide.

The references are REHEARSAL4's committed copies, which the run's own references were
taken from byte for byte (`md5 2372e530...`, `237232...`). Using them rather than a
second copy keeps one photograph in the repository per reference.

Run from the repo root:  python rehearsal6/verify_done.py
"""
from __future__ import annotations

import importlib.util
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
R4 = f"{ROOT}/rehearsal4"

MUG = f"{R4}/pass/ref.jpg"
SITTER = f"{R4}/sitter/ref.jpg"


def _load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


verify = _load("verify_done_r4", f"{R4}/verify_done.py")
notes = _load("probe_human_notes", f"{R4}/probe_human_notes.py")
structure = _load("probe_structure", f"{R4}/probe_structure.py")
axis = _load("probe_axis_alignment", f"{ROOT}/rehearsal3/probe_axis_alignment.py")

#: Everything in REHEARSAL4's checker that resolves a path does it against its own
#: directory. Moving that one name is the whole of pointing it at this run.
verify.HERE = HERE

#: Words that mean a mark was aimed at the value number rather than at the picture.
#: A keyword flag cannot prove intent -- it is a shortlist for the write-up to read,
#: and the ten marks are printed whether they trip it or not.
VALUE_WORDS = ("value", "correct", "fix", "darken", "lighten", "knock down",
               "knockdown", "raise", "lower", "compare", "cell", "delta")


def _session(path: str) -> tuple[dict, list] | None:
    """A session's meta and history, from the `.easel` or from the saved JSON.

    `*.easel` is ignored repository-wide -- a canvas is 15 MB -- so after the run
    `save_logs.py` writes each history out beside the paintings. Preferring the
    `.easel` while it exists and falling back to the JSON means these checks give the
    same answer during the run and from a fresh clone a year later.
    """
    if os.path.exists(path):
        with np.load(path, allow_pickle=False) as z:
            return json.loads(str(z["meta"])), json.loads(str(z["log"]))
    run, name = path.split("/")[-2], os.path.basename(path)[:-6]
    saved = f"{HERE}/sessions/{run}-{name}.json"
    if os.path.exists(saved):
        with open(saved, encoding="utf-8") as handle:
            payload = json.load(handle)
        return payload["meta"], payload["log"]
    return None


def _charged(log: list) -> list:
    """The marks the painter paid for, in order.

    Pencil and erase are free by design and the signature is free by the guide's
    grant, so none of them is one of "the last ten strokes".
    """
    out = []
    for record in log:
        if record["kind"] in ("pencil", "erase", "dry", "mark", "unmark"):
            continue
        if "signature" in str(record.get("note", "")).lower():
            continue
        out.append(record)
    return out


def last_ten(run: str) -> None:
    loaded = _session(f"{HERE}/{run}/copy.easel")
    if loaded is None:
        print(f"\n  {run}: no session for the copy")
        return
    _, log = loaded
    charged = _charged(log)
    tail = charged[-10:]
    print(f"\n  {run} -- the last {len(tail)} charged marks, oldest first")
    flagged = 0
    for record in tail:
        note = str(record.get("note", ""))
        size = record.get("params", {}).get("size")
        hit = [w for w in VALUE_WORDS if w in note.lower()]
        if hit:
            flagged += 1
        mark = f"  <- {'/'.join(hit)}" if hit else ""
        size_text = f"{float(size):.3f}" if size is not None else "  -  "
        print(f"    #{record['index']:<4} {record['kind']:<8} size {size_text}"
              f"   {note[:52]}{mark}")
    verdict = ("clean" if not flagged else
               f"{flagged} of {len(tail)} read as value corrections - see the log")
    print(f"    -> {verdict}")


def signatures() -> None:
    print("\n== Every finished painting is signed ==")
    print("  (up to five marks noted `signature`, free of the budget;")
    print("   neither prompt mentioned it, PAINTER.md:1263 does)")
    found = False
    for run in ("pass", "sitter"):
        for name in ("copy", "own1", "own2"):
            loaded = _session(f"{HERE}/{run}/{name}.easel")
            if loaded is None:
                continue
            found = True
            _, log = loaded
            marks = [r for r in log
                     if "signature" in str(r.get("note", "")).lower()]
            state = (f"{len(marks)} mark(s)" if marks else "UNSIGNED")
            over = ("   OVER THE ALLOWANCE"
                    if len(marks) > verify.SIGNATURE_ALLOWANCE else "")
            print(f"  {run}/{name:<5} {state}{over}")
    if not found:
        print("  (no sessions yet)")


def containment() -> None:
    print("\n== The second number: did the dark stay in the thing containing it? ==")
    print("  (dark paint in the mouth's box that is nowhere near dark in the photo,")
    print(f"   with {notes.SLACK:.0%} of the width of slack for a soft edge)")
    rows = [
        ("REHEARSAL6 pass (mug)", f"{HERE}/pass/copy_final.png"),
        ("REHEARSAL5 pass (mug)", f"{ROOT}/rehearsal5/pass/copy_final.png"),
        ("REHEARSAL4 pass (mug)", f"{R4}/pass/copy_final.png"),
        ("REHEARSAL3 pass (mug)", f"{ROOT}/rehearsal3/pass/copy_final.png"),
    ]
    for label, painting in rows:
        notes.containment(painting, MUG, label)


def buried() -> None:
    print("\n== Did a later mass bury finished work? ==")
    for run in ("pass", "sitter"):
        path = f"{HERE}/{run}/copy.easel"
        if os.path.exists(path):
            notes.overpainting(path, f"rehearsal6/{run}/copy.easel")


def axes() -> None:
    print("\n== Axis alignment (share of strong edges within 10 deg of an axis) ==")
    rows = [
        ("Level1 (the mug photo)", MUG),
        ("REHEARSAL6 pass copy (mug)", f"{HERE}/pass/copy_final.png"),
        ("REHEARSAL5 pass copy (mug)", f"{ROOT}/rehearsal5/pass/copy_final.png"),
        ("REHEARSAL4 pass copy (mug)", f"{R4}/pass/copy_final.png"),
        ("Level3 (the sitter photo)", SITTER),
        ("REHEARSAL6 sitter copy", f"{HERE}/sitter/copy_final.png"),
        ("REHEARSAL4 sitter copy", f"{R4}/sitter/copy_final.png"),
        ("REHEARSAL6 unprompted 1", f"{HERE}/pass/own1_final.png"),
        ("REHEARSAL6 unprompted 2", f"{HERE}/pass/own2_final.png"),
    ]
    width = max(len(n) for n, _ in rows)
    for name, path in rows:
        if not os.path.exists(path):
            print(f"  {name:<{width}}  (missing)")
            continue
        print(f"  {name:<{width}}  {axis.axis_share(path):5.1f} %")


def unprompted_structure() -> None:
    print("\n== The unprompted pair, against PREREGISTERED.md's baseline ==")
    structure.report([
        ("REHEARSAL6 unprompted 1 (free)", f"{HERE}/pass/own1_final.png"),
        ("REHEARSAL6 unprompted 2 (differ)", f"{HERE}/pass/own2_final.png"),
    ])
    print()
    structure.report([
        ("REHEARSAL5 unprompted 1", f"{ROOT}/rehearsal5/unprompted/own1_final.png"),
        ("REHEARSAL5 unprompted 2", f"{ROOT}/rehearsal5/unprompted/own2_final.png"),
        ("REHEARSAL4 unprompted 1", f"{R4}/pass/own1_final.png"),
        ("REHEARSAL4 unprompted 2", f"{R4}/pass/own2_final.png"),
        ("REHEARSAL3 unprompted", f"{ROOT}/rehearsal3/pass/own_final.png"),
    ])


if __name__ == "__main__":
    print("REHEARSAL6 - the brief's definition of done, measured from the artefacts.")
    print(f"Palette floor {verify.FLOOR:.3f}; threshold {verify.THRESHOLD:.2f}.")

    verify.artefacts()
    verify.sessions()

    print("\n== The value criterion ==")
    verify.check("pass/copy_final.png", MUG, verify.MUG_CELLS,
                 "THE PASS - mug, cells on the object")
    verify.check("pass/copy_final.png", MUG, verify.MUG_CELLS_WIDE,
                 "THE PASS - mug, plus the cells it only clips")
    verify.check("sitter/copy_final.png", SITTER, verify.SITTER_HEAD,
                 "REACH - sitter, the head")
    verify.check("sitter/copy_final.png", SITTER, verify.SITTER_FIGURE,
                 "REACH - sitter, head and coat")

    containment()

    print("\n== The procedural rule: the last ten may not be value corrections ==")
    for run in ("pass", "sitter"):
        last_ten(run)

    signatures()
    verify.planning()
    verify.shapes()
    buried()
    axes()
    unprompted_structure()
    verify.untouched()
