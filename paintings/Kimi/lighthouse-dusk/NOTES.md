# Lighthouse at Dusk

_To understand this, start by reading `painting.png`, then `prelude.py`, then `pass3_fields.py` and `pass4_lighthouse.py`._

Painted with `easel-paint` 0.5.0. Session: `lighthouse-dusk.easel`, 1024×768, linen texture, `toned_grey` ground, seed 7, budget 420. No reference image was used.

## Why this subject

A lighthouse at dusk lets one small warm lamp hold a whole dark coast together. The picture is mostly deep blue air and water; the warm gold sits only at the horizon, the lamp, and a few broken reflections. That reason is still in the picture: the brightest thing is the lamp, and everything else is arranged around the quiet it makes.

## Plan, before the first mark

- Values: tower/rocks **0.16–0.18**, near sea **0.21**, far sea **0.30**, upper sky **0.20–0.32**, horizon gold **0.58**, lamp glass **0.88**.
- Three horizontal fields — sky, far sea, near sea — crossed by the beam, the point of rock, and the upright tower.
- Budget **420**. Planned split: about half for the graded fields, a third for the lighthouse and rock, the rest for quieting joins and final lights.
- Back to front: sky, horizon glow, sea, distant headland, rock planes, tower, lamp, reflections, signature.

## What changed while painting

1. **The first reflection was built from flat horizontal flashes.** In the committed look they read as small bricks. The pass was rewritten before delivery: the reflection is now five bent, starved `bristle` strokes, built as visible side pieces because the tower and rock interrupt the middle.
2. **A late `cover()` repair was tried and rejected.** It buried the brick reflection, but it also laid a flat blue patch over too much sea and would have stood in front of the tower. The final painting rebuilds the pass instead of keeping that repair.
3. **`sea_near()` still warns that its scumble passes are shorter than the brush.** The warning was accepted: the near water is a shallow foreground band, and the slight bloom keeps it from becoming a ruled sheet.
4. **The standing horizontal-marks warning fired.** It is accepted on purpose: the subject is a horizon, a calm sea, a beam, and a reflection. The crossing marks are the tower, rock edge, beam, and a few clouds.
5. The exported PNG leaves out the landmark labels and guides visible in `pass*_colour.png`; `export()` does not draw marks or guides.

## Closing checklist

- Greyscale: clear light at the lamp and horizon, mid sky/sea, dark tower and rocks. Yes.
- Edges: hard on the tower and gallery, softer in the sky, partly lost along the right horizon. Yes.
- Ground showing: **0.00%**. The first thin masses were later buried by the graded fields; accepted and recorded.
- Highlights: lamp core, gallery rail, a few reflection strokes. Few.
- Mechanical repetition: the main remaining weakness is the stepped edge of the rock and the regular horizon wave. Both are painterly enough to keep, but they are the passages I would spend leftover strokes on.
- Lightest mass: the lamp glass, as planned.
- Back to front: yes. The tower stands on the rock; the rock stands on the sea; the beam sits in the air behind and around the lamp.
- Pencil: erased in `pass5_finish.py`.
- Subject share: **50 of 172 marks (29%)** from Easel's report. Planned around one third.
- Budget: **170 of 420 strokes spent**, 250 left. Stopped because more sea marks were making the picture busier, not better.

## Signature

Two short liner marks at lower left, close in value to the near sea. They read as small tide-lines rather than a name, and both carry `note="signature"`.

## File map

- `painting.png` — finished painting, 1024×768.
- `painting.gif` — Easel time-lapse, 91 frames, looping; the final frame matches the PNG within GIF quantization.
- `lighthouse-dusk.easel` — saved Easel session with palette, history, and frames.
- `prelude.py` — mixtures, landmarks, shapes, and the mass functions used by the passes.
- `pass1_draw.py` — free graphite drawing and guides.
- `pass2_masses.py` — four big bristle masses at low density.
- `pass3_fields.py` — graded sky and sea, clouds, beam glazes, first reflection strokes.
- `pass4_lighthouse.py` — rock planes, tower, gallery, lamp, rails, and first small lights.
- `pass5_finish.py` — erase drawing, quiet glazes, edge work, final lights, signature, export.
- `pass*_colour.png` / `pass*_values.png` — checkpoint looks; the values files are greyscale checks.
- `.venv/` — isolated Python environment used to install and run `easel-paint`.

## Rebuild

From this folder, using the included virtual environment on Windows:

```powershell
.\.venv\Scripts\python.exe -m easel new lighthouse-dusk.easel --size 1024x768 --texture linen --ground toned_grey --seed 7 --budget 420 --out-dir out --force
.\.venv\Scripts\python.exe -m easel run lighthouse-dusk.easel pass1_draw.py pass2_masses.py pass3_fields.py pass4_lighthouse.py pass5_finish.py
.\.venv\Scripts\python.exe -m easel timelapse lighthouse-dusk.easel painting.gif --fps 8 --every 2 --scale 480
```

The committed scripts are the source of truth. If a passage needs changing, change its pass and rebuild from `easel new --force` rather than repainting over the delivered session.
