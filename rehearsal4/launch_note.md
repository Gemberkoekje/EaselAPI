# How REHEARSAL4 was run

The brief's *Definition of done*, run end to end. Two fresh sessions, launched in
parallel, each given the text below and nothing else. Neither had read `NOTES.md`,
`REVIEW.md`, `painting-api-brief.md`, `README.md`, `M7.md`, any earlier rehearsal, or
any file under `src/`, `tests/`, `scripts/` or `examples/`. Both were told to keep a
running list of every moment they wanted to open the source.

The engine's author (this session) read the brief and the notes and did not paint,
did not edit a painting script, and did not look at the unprompted paintings before
handing them to the human.

| Run | Reference | Stage |
|---|---|---|
| `rehearsal4/pass/` | `C:/temp/Level1.jpg`, a mug on a table | **The pass** — the copy, then the two unprompted paintings |
| `rehearsal4/sitter/` | `C:/temp/Level3.jpg`, the sitter | **Reach** — how far the tools get on a face |

Everything measured afterwards was re-measured from the exported PNGs by
`rehearsal4/verify_done.py`, not taken from the painters' reports.

---

## The prompt the `pass` session was given

> You are a painter. You have an engine called Easel and a guide written for you.
>
> **Read `C:\git\EaselAPI\PAINTER.md` first, all of it, before you write a line of
> code.** `CALIBRATION.md` beside it holds the measured numbers behind its rules; read
> it if you want them. Those two files are the only documentation you may open.
>
> **Do not open any other file in this repository.** Not `README.md`, not `NOTES.md`,
> not `REVIEW.md`, not `M7.md`, not `painting-api-brief.md`, not anything under `src/`,
> `tests/`, `scripts/`, `examples/`, `m7/`, `m8/`, `m8b/`, `rehearsal/`, `rehearsal2/`
> or `rehearsal3/`. Do not read the installed package. Do not use `help()`, `inspect`,
> `dir()`, or read a docstring or a signature. If the guide does not say how something
> works, find out by writing code and looking at the picture — that is the point of the
> exercise. **Do not modify any source file.**
>
> Keep a running list of every moment you wanted to open the source, and what you
> wanted to know. That list is a result.
>
> Work in `C:\git\EaselAPI\rehearsal4\pass\`. Python is `python` on PATH; the CLI is
> `python -m easel`. Paint in increments from scripts run with `easel run`, so you can
> look between passes.
>
> ### Stage 1 — the copy
>
> The reference photograph is `C:/temp/Level1.jpg`. Paint a copy of it.
>
> - **Under 300 strokes.** `s.stroke_count` is the number that counts. Pencil lines
>   and rehearsals are free.
> - **The pencil is your own.** Do not call `sketch(reference)` — that is a different,
>   assisted mode and is not what is being measured here. Draw your own underdrawing
>   with `pencil()` if you want one.
> - The criterion you are being judged on, besides a human recognising the object:
>   `compare()` reports **no cell on the object** more than `0.10` from the
>   reference's value.
> - Before you pay for an expensive mark, try it with `preview()` or `rehearse()`.
>   **Keep every mark you tried and then rejected**, with the look that caught it —
>   you will be asked to point at them.
> - Export the final painting as `copy_final.png` and a time-lapse as
>   `copy_timelapse.gif`.
>
> ### Stage 2 — two paintings with no prompt
>
> When the copy is done, paint **two** more pictures. There is no reference for either.
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
> stroke counts, your honest opinion of each painting including its flaws, and the
> list of moments you wanted the source. Be blunt. A flattering log is a useless one.

## The prompt the `sitter` session was given

The same, with Stage 2 removed and Stage 1 pointed at `C:/temp/Level3.jpg`, plus:

> This photograph is a portrait of a person in a dim room. The question this run
> answers is not the value criterion — it is **how far the tools reach**: is the
> painting recognisable as *this person*, and which features got there? Say so
> plainly at the top of your log, including the ones that defeated you.
