# Tidal Sky — painter's notes

A golden-hour coastal scene painted with `easel-paint` (the `easel` module).

**Why this subject:** the whole picture is one light — a low sun's amber/coral
reflection running unbroken from sky to water — and the boat is the one dark thing
standing in it.

## Files

- `tidal-sky.easel` — the session (1024x768, linen, toned_grey, seed 7, budget 300)
- `prelude.py` — mixtures (mixed to *values* via `at_value`, not ratios), landmarks
  (`sun`, `bow`, `stern`), and the masses as named functions (repair = re-run the stack)
- `pass1_draw.py` — graphite drawing: horizon at y=0.52, boat hull, sun circle. Free.
- `pass2_masses.py` — two big bristle block-ins at `density=0.8`, then a values look.
- `pass3_fields.py` — the graded fields (scumble ramps per the *graded field* recipe,
  `load=1.0, load_falloff=0.0`, `size` left off), clouds, sun halo (three glazes of
  lit air, mixed close to the sampled field), sun disc (`dab` + `press=3`), and the
  glitter path.
- `pass4_boat.py` — the hull (`block_in`, `edge="hard"`, axis direction), broken
  reflection strokes, one broken catch-light along the near edge.
- `pass5_finish.py` — two starved diagonal swell lines (breaks the comb), right half
  of the horizon lost (one smudge + paint across), boat waterline half-lost, two
  sparks (`tip_wobble=0.7`), signature, export.
- `painting.png` / `painting.gif` — the painting and its time-lapse.

## Key decisions and gotchas

- The first glitter path was vertical tilted `flat` strokes and read as floating
  rectangles (the tool's own chisel shape). The fix: horizontal broken flashes,
  shorter and fainter toward the viewer.
- `s.timelapse_gif()` fails on a rehearsal copy (`--rehearse` records no frames), so
  it was run via `easel timelapse` after committing the pass.
- The standing warnings (horizontal-bar comb, 0.00% bare ground) were accepted: a calm
  sea at golden hour *is* horizontal, and a full sky/water field leaves no ground to
  show — the `density=0.8` breather layer in pass 2 was the deliberately painted one.
- 68 of 300 strokes spent. The subject's share stayed small on purpose: the picture's
  subject is the light, not the boat.

## To rebuild from scratch

```bash
easel new tidal-sky.easel --size 1024x768 --texture linen --ground toned_grey --seed 7 --budget 300
easel run tidal-sky.easel pass1_draw.py
easel run tidal-sky.easel pass2_masses.py
easel run tidal-sky.easel pass3_fields.py
easel run tidal-sky.easel pass4_boat.py
easel run tidal-sky.easel pass5_finish.py
easel timelapse tidal-sky.easel painting.gif
```
