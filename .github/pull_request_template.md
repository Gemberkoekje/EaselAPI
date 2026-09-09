## Summary

<!-- What changed and why. Link an issue if there is one. -->

## Test plan

- [ ] `pytest -q` passes
- [ ] `ruff check src tests scripts examples` passes
- [ ] No golden image moved, or it moved on purpose (see below)
- [ ] `python scripts/make_brush_sampler.py` regenerated and looked at, if the change
      touches brushes, colour, or canvas texture -- `samples/brushes.png` is this
      project's primary test artefact, and looking at it catches what the test suite
      cannot

<!--
If a case in `tests/test_golden.py` fails:
  1. Open `tests/golden/<case>.actual.png` beside the stored `<case>.png` and look at both.
  2. Only once the new marks are decided to be better: `python scripts/make_golden.py <case>`,
     then commit the updated PNG(s) and `tests/golden/hashes.json`.
A golden regenerated without looking records that a mark changed and asserts that nobody
minded, which is worse than having no golden at all -- see REVIEW.md.
-->

## Notes for the reviewer

<!-- Anything not obvious from the diff: alternatives tried and rejected, a design
     tradeoff deliberately left open, what this does not attempt to fix. See REVIEW.md's
     "Open, with evidence" entries for the tone this project uses for that. -->
