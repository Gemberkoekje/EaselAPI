"""REHEARSAL5 against REHEARSAL4, on the five questions the guide changes targeted.

`REHEARSAL4.md`'s *What to do next* fixed these before this run was launched, and none
of them were told to the painter:

1. Does the dark stay inside the thing containing it?   (was 17.5% escaped)
2. Does a later mass stop burying finished work?        (was 117.7% of standing detail)
3. Is the background still a grid of square patches?    (axis-aligned edge share)
4. Does the painter judge a mark before paying for it?  (was 1 preview, 0 rehearse)
5. Does the value criterion still hold?                 (was 0 of 64 out, by 0.0015)

Every probe here is REHEARSAL4's own code, imported by path rather than copied, so the
two runs are measured by the same instrument and the numbers can be put side by side.
Nothing in this file re-implements a measurement.

Run from the repo root:  python rehearsal5/compare_runs.py
"""
from __future__ import annotations

import importlib.util
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
R4 = f"{ROOT}/rehearsal4"


def _load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


notes = _load("probe_human_notes", f"{R4}/probe_human_notes.py")
verify = _load("verify_done", f"{R4}/verify_done.py")
axis = _load("probe_axis_alignment", f"{ROOT}/rehearsal3/probe_axis_alignment.py")

#: Both painters' copies. `containment` and `axis_share` take a path as given;
#: `verify.check` prefixes with rehearsal4's own directory, so that one gets a
#: relative form derived here rather than written out twice.
RUNS = [
    ("REHEARSAL4", f"{R4}/pass/copy_final.png", f"{R4}/pass/copy.easel",
     f"{R4}/pass/out"),
    ("REHEARSAL5", f"{HERE}/pass/copy_final.png", f"{HERE}/pass/copy.easel",
     f"{HERE}/pass/out"),
]
REFERENCE = "C:/temp/Level1.jpg"


def relative_to_r4(png: str) -> str:
    """The form `verify.check` wants: a path relative to rehearsal4/."""
    return os.path.relpath(png, R4).replace("\\", "/")


def strokes(easel_path: str) -> tuple[int, str, dict]:
    if not os.path.exists(easel_path):
        return (-1, "missing", {})
    with np.load(easel_path, allow_pickle=False) as z:
        meta = json.loads(str(z["meta"]))
        log = json.loads(str(z["log"]))
    kinds: dict[str, int] = {}
    for record in log:
        kinds[record["kind"]] = kinds.get(record["kind"], 0) + 1
    assisted = meta.get("assisted", None)
    mark = "none" if assisted == [] else ("(no field)" if assisted is None
                                          else f"USED {len(assisted)}")
    # The signature is free up to the guide's allowance; see verify_done.py.
    signed = sum(1 for r in log if "signature" in str(r.get("note", "")).lower())
    if signed:
        kinds["signature"] = signed
    return (meta["stroke_count"] - min(signed, verify.SIGNATURE_ALLOWANCE), mark, kinds)


def planning(out_dir: str) -> tuple[int, int]:
    names = os.listdir(out_dir) if os.path.isdir(out_dir) else []
    return (sum(1 for n in names if n.startswith("preview")),
            sum(1 for n in names if n.startswith("rehearse")))


if __name__ == "__main__":
    print("REHEARSAL5 vs REHEARSAL4 - the five questions the guide changes targeted.")
    print("Same reference, same protocol, same probes. Nothing below was told to the")
    print("painter.\n")

    print("== Stroke count, and the pencil ==")
    for label, _, easel_path, _ in RUNS:
        count, assisted, kinds = strokes(easel_path)
        if count < 0:
            print(f"  {label}  (no session file yet)")
            continue
        breakdown = ", ".join(f"{k} {v}" for k, v in sorted(kinds.items()))
        print(f"  {label}  {count:>3} strokes / 300   sketch(reference): {assisted}"
              f"   [{breakdown}]")

    print("\n== 1. Did the dark stay inside the thing containing it? ==")
    for label, painting, _, _ in RUNS:
        notes.containment(painting, REFERENCE, label)

    print("\n== 2. Did a later mass bury finished work? ==")
    for label, _, easel_path, _ in RUNS:
        notes.overpainting(easel_path, label)

    print("\n== 3. Is the picture still a grid of square patches? ==")
    print("  (share of strong edges within 10 deg of an axis; the photograph is 22.8%)")
    for label, painting, _, _ in RUNS:
        if os.path.exists(painting):
            print(f"  {label}  {axis.axis_share(painting):5.1f} %")
        else:
            print(f"  {label}  (missing)")

    print("\n== 4. Were marks judged before they were paid for? ==")
    for label, _, _, out_dir in RUNS:
        previews, rehearsals = planning(out_dir)
        verdict = ("used both" if previews and rehearsals
                   else "NEITHER" if not previews and not rehearsals
                   else "one of the two only")
        print(f"  {label}  preview {previews:>2}   rehearse {rehearsals:>2}   {verdict}")

    print("\n== 5. Does the value criterion hold? ==")
    for label, painting, _, _ in RUNS:
        verify.check(relative_to_r4(painting), REFERENCE, verify.MUG_CELLS,
                     f"{label} - cells on the object")
