# Quiet harbour at dusk

_To understand this, start by reading `painting.png`, then `prelude.py`, then `pass1_draw.py`._

Painted with easel-paint 0.5.0. Session `painting.easel`, 1024×768, linen, cool_grey ground, seed 11, budget 300.

## Why this subject

Dusk flattens the water into one colour, so the painting is mostly edges and light, not detail. That reason is still in the picture: the harbour is a single muted sheet, the boats and pier are silhouettes against the afterglow, and there is almost nothing to name once you have said “edge” and “light”.

## Plan, before the first mark

- Values: silhouettes **0.14–0.20** · water sheet **0.40** (near **0.34**, sheet **0.48** so they merge) · afterglow **0.70** (core **0.78**). Upper sky **0.28**.
- Three bands — sky, water, near water — crossed by the pier (receding toward the light) and two masts.
- Budget **300**. Planned split: ~80 masses and atmosphere, ~100 subject (silhouettes and the sheet of light), ~100 last-third surroundings, ~20 accents.
- Planned subject share ~33% on the boats/pier once they were in; the real subject is the flattened water, which is most of the field.
- Back to front: sky, water, headland, boats, pier, accents.
- Projection written before the drawing: VP at (0.28, 0.38), F=0.90, eye 1.80 m, so the pier and hulls land in metres rather than guessed canvas points.

## What changed while painting

1. **The first sky mass was mixed too close to the water** (`dusk_mid` 0.38 against water 0.40). Replaced with `dusk_high` 0.28 so the block-in already separated.
2. **A downward glaze of afterglow on the water read as a searchlight.** That is the opposite of a flattened sheet. Dropped; one faint horizontal glaze stays.
3. **The pier’s long side-face was a black triangle that owned the picture.** Deck only, plus three pilings. The near fascia was a box and was dropped too.
4. **The dinghy failed three times** (polygons, then stacked rims, then three strokes). The fault was the drawing — a foreshortened hull laid as a diagram. Dropped. Two boats and the pier are enough edges.
5. **Smudge along the horizon dragged the afterglow into the headland** as a white thumbprint. All smudges came out. The right horizon is lost because the values already sit 0.02 apart, once the graphite line is erased.
6. **Small loaded bristle “paint-across” marks printed combs and speckles.** Lost edges that need paint use a larger brush or they are left alone.
7. Stopped with **132 of 300** strokes. Further marks on the pier and the sky were making the picture worse; the remaining budget belongs to the pier’s flatness, and two treatments of that passage had already failed.

## Closing checklist

- Greyscale: clear light (afterglow), mid (water), dark (boats, pier, headland). Yes.
- Edges: hard on the hulls, soft in the sky joins, lost along the right horizon. Yes.
- Ground showing: **0.00%**. The graded fields were laid solid; the `density=0.8` breather in pass 2 was buried. Accepted, and recorded.
- Highlights: the afterglow, one catch on the nearer hull, a whisper on the far gunwale. Few.
- Mechanical: the pier is still a receding plane of one colour — the weakest passage. The masts fade and lean a little.
- Lightest mass is the afterglow, as planned.
- Back to front: yes. Nothing standing on a mass was buried by a later correction.
- Pencil: erased in pass 5.
- Subject share: **26 of 134 marks (19%)** tagged `subject` (the boats). Against 33% planned. Counting the water and the light as the subject, the share is most of the picture — that is the point of this one.
- Weakest passage: the pier, a flat brown wedge. The leftover strokes would go there.
- Why this subject: still in it. The water is one colour. The rest is edges and the remaining light.

## Signature

Two short liner marks, lower left, in `water_near`, `note="signature"`. Close in value to the near water; a small ripple, not a name.

## File map

- `painting.png` / `painting.gif` — the painting and its time-lapse
- `painting.easel` — session (1024×768, linen, cool_grey, seed 11, budget 300)
- `prelude.py` — mixtures via `at_value`, projection `P()`, landmarks, named masses
- `pass1_draw.py` — graphite (free)
- `pass2_masses.py` — three big bristle masses at `density=0.8`
- `pass3_fields.py` — graded sky, flattened water, afterglow as lit air, headland
- `pass4_boats.py` — silhouettes, masts, pier deck, pilings
- `pass5_finish.py` — erase the drawing, quiet the fields, last light, sign, export
- `pass6_repair.py` — one stroke over a hole in the near water
- `out/` — rehearsals and compares

## Rebuild

```powershell
python -m easel new painting.easel --size 1024x768 --texture linen --ground cool_grey --seed 11 --budget 300 --out-dir out --force
python -m easel run painting.easel pass1_draw.py
python -m easel run painting.easel pass2_masses.py
python -m easel run painting.easel pass3_fields.py
python -m easel run painting.easel pass4_boats.py
python -m easel run painting.easel pass5_finish.py
python -m easel run painting.easel pass6_repair.py
python -m easel timelapse painting.easel painting.gif --every 2
```
