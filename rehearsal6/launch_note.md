# How REHEARSAL6 was run

The brief's *Definition of done*, run end to end for the second time (REHEARSAL4 was
the first). Two fresh sessions, launched in parallel, each given the text below and
nothing else. Neither had read `NOTES.md`, `REVIEW.md`, `painting-api-brief.md`,
`README.md`, `M7.md`, `ENGINE_CHANGES.md`, any earlier rehearsal, or any file under
`src/`, `tests/`, `scripts/` or `examples/`. Both were told to keep a running list of
every moment they wanted to open the source.

**The mechanism differs from REHEARSAL4 and the difference is stated rather than
buried.** REHEARSAL4's painters were separate Claude Code sessions on the author's
machine. REHEARSAL6's are fresh contexts launched from the author's session into the
same container: each begins with the prompt below and no other history, but "do not
open the source" is honoured by the painter rather than enforced by a sandbox — as it
was in every earlier run.

The engine's author (the launching session) read the brief and the notes, did not
paint, did not edit a painting script, and did not look at the unprompted paintings
before handing them to the human.

| Run | Reference | Stage |
|---|---|---|
| `rehearsal6/pass/` | `/home/user/refs/Level1.jpg`, a mug on a table | **The pass** — the copy, then the two unprompted paintings |
| `rehearsal6/sitter/` | `/home/user/refs/Level3.jpg`, the sitter | **Reach** — how far the tools get on a face |

Both references are byte-identical to REHEARSAL4's (`md5 2372e530…` and `237232…`),
so the two runs are on the same photographs.

Everything measured afterwards was re-measured from the exported PNGs and the saved
sessions by `rehearsal6/verify_done.py`, which imports REHEARSAL4's checks rather than
re-implementing them, not taken from the painters' reports.

---

## The prompt the `pass` session was given

> You are a painter. You have an engine called Easel and a guide written for you.
>
> **Read `/home/user/EaselAPI/PAINTER.md` first, all of it, before you write a line of
> code.** `/home/user/EaselAPI/CALIBRATION.md` beside it holds the measured numbers
> behind its rules; read it if you want them. Those two files are the only
> documentation you may open.
>
> **Do not open any other file in this repository.** Not `README.md`, not `NOTES.md`,
> not `REVIEW.md`, not `M7.md`, not `painting-api-brief.md`, not `ENGINE_CHANGES.md`,
> not anything under `src/`, `tests/`, `scripts/`, `examples/`, `m7/`, `m8/`, `m8b/`,
> `engine_changes/`, `rehearsal/`, `rehearsal2/`, `rehearsal3/`, `rehearsal4/`,
> `rehearsal5/`, and nothing in `rehearsal6/` outside your own directory. Do not read
> the installed package. Do not use `help()`, `inspect`, `dir()`, or read a docstring
> or a signature. If the guide does not say how something works, find out by writing
> code and looking at the picture — that is the point of the exercise. **Do not modify
> any source file.**
>
> Keep a running list of every moment you wanted to open the source, and what you
> wanted to know. That list is a result.
>
> Work in `/home/user/EaselAPI/rehearsal6/pass/`. `cd` there first and keep everything
> you write inside it. Python is `/home/user/EaselAPI/.venv/bin/python`; the CLI is
> `/home/user/EaselAPI/.venv/bin/easel`, or `…/python -m easel` if you prefer. Paint in
> increments from scripts run with `easel run`, so you can look between passes. **Look
> at the PNGs you produce** — open them with your image tool, that is the job.
>
> ### Stage 1 — the copy
>
> The reference photograph is `/home/user/refs/Level1.jpg`. Paint a copy of it, in a
> session called `copy.easel`.
>
> - **Under 300 strokes.** `s.stroke_count` is the number that counts. Pencil lines
>   and rehearsals are free.
> - **The pencil is your own.** Do not call `sketch(reference)` — that is a different,
>   assisted mode and is not what is being measured here. Draw your own underdrawing
>   with `pencil()` if you want one.
> - The criterion you are being judged on, besides a human recognising the object:
>   `compare()` reports **no cell on the object** more than `0.10` from the
>   reference's value.
> - **Your last ten strokes may not be value corrections.** Spend them on the picture.
>   The log carries the order, and your `LOG.md` will be asked what those ten were for.
> - Before you pay for an expensive mark, try it with `preview()` or `rehearse()`.
>   **Keep every mark you tried and then rejected**, with the look that caught it —
>   you will be asked to point at them.
> - Export the final painting as `copy_final.png` and a time-lapse as
>   `copy_timelapse.gif`.
>
> ### Stage 2 — two paintings with no prompt
>
> When the copy is done, paint **two** more pictures, in sessions called `own1.easel`
> and `own2.easel`. There is no reference for either.
>
> - **The first is genuinely unprompted.** No constraint of any kind: subject, palette,
>   size, everything is yours.
> - **The second must differ from the first in compositional structure.** That is the
>   only constraint on it. Nothing is said about its subject, its palette, or what its
>   marks should do — working out how to make it structurally different is yours.
> - Export each as `own1_final.png` / `own2_final.png` with
>   `own1_timelapse.gif` / `own2_timelapse.gif`.
>
> ### Finally
>
> Write `LOG.md` in your directory, in your own words: what you did, what the guide
> got right, what it got wrong or left out, the marks you rejected and why, your
> stroke counts, what your last ten strokes on the copy were for, your honest opinion
> of each painting including its flaws, and the list of moments you wanted the source.
> Be blunt. A flattering log is a useless one.

## The prompt the `sitter` session was given

The same, with Stage 2 removed, the directory `rehearsal6/sitter/` and Stage 1 pointed
at `/home/user/refs/Level3.jpg`, plus:

> This photograph is a portrait of a person in a dim room. The question this run
> answers is not the value criterion — it is **how far the tools reach**: is the
> painting recognisable as *this person*, and which features got there? Say so
> plainly at the top of your log, including the ones that defeated you.

## What was not in either prompt

The signature, and every quantity the probes measure. See `PREREGISTERED.md`.
