# When the Windows Come On

_To understand this painting, start with `painting.png`, `painting.gif`, and `paint.py`._

Painted by GPT-6 Astra through OpenCode, 16 September 2026, using easel-paint 0.5.0.

## Intention, before the first mark

I chose a seaside village at dusk because the little warmth of inhabited windows,
carried out into cold water, makes an ordinary harbour feel like a place to come home
to. The red dinghy should feel at rest, held by the same quiet that surrounds it.

This is an invented scene, painted with Easel's brushes. The viewpoint is from just
above the water, looking obliquely along a curving stone quay. The cottages diminish
toward the left; the dinghy is seen from above and along its length, with a narrow
visible interior. A low open horizon on the left balances the village on the right.

## Initial plan

- Canvas: 1440 x 960, linen, muted violet-grey ground `#746d78`, seed 61,
  texture strength 0.72.
- Three main values: sky **0.70**, water **0.39**, village/quay shadow **0.22**.
- Warm window cores may reach **0.90**; they occupy very little area.
- Three large masses: sky, water, the diagonal village/quay. The quay, tower, and
  irregular roofline interrupt the horizontal division. Windows will be clustered,
  unequal, and partly obscured rather than arranged in an even comb.
- Budget: **420 paid brush marks**. Initial allocation: **100** atmosphere and big
  masses, **170** village and boat, **140** surrounding water, quay, and edge work,
  **10** final light accents. Up to five additional signature marks are free in Easel.
- Planned subject share: **40%** for village and dinghy; review the actual count when
  their structure is complete, then bring up their surroundings.
- Back-to-front order: sky, distant coast, sea, village foundation, tower, cottages,
  quay, dinghy interior and hull, water reflections, final light accents.
- Rehearse each painting pass on a scratch canvas, inspect it, then commit. Inspect
  colour and greyscale views between passes. Corrections are made with paint.

## Setup findings

- `python -m pip install easel-paint` found Easel 0.5.0 already installed.
- The console executable is not on PATH; `python -m easel` works.
- Read the installed `PAINTER.md`, `PAINTING.md`, `REFERENCE.md`, and the relevant
  recipes before painting. No reference image is used.
- The nine warm-up exercises are in `process/studies/contact-sheet.png`. They made
  paint load, pigment mixing, the chisel tip, and the importance of explicit sweep
  direction visible before work on the picture.
- Easel exported both the finished PNG and the native brushwork GIF. Every painted
  mark was made with Easel. Pillow assembled the warm-up contact sheet.

## File map

- `painting.png`: finished, signed, 1440 x 960 painting.
- `painting.gif`: Easel's looping brushwork time-lapse, 360 x 240, 78 frames,
  10.08 seconds.
- `NOTES.md`: intention, decisions, pitfalls, and hand-off notes.
- `paint.py`: palette, projected cottages, hand-drawn shapes, 43 separately
  rehearsable passes including the signature, and export commands.
- `warmups.py`: nine small brush and mixing studies.
- `requirements.txt`: the painting engine version.
- `process/painting.easel`: the saved canvas, palette, history, and recorded frames.
- `process/strokes.json`: the full Easel history as readable data.
- `process/00-drawing.png`: the initial graphite composition with a grid.
- `process/*-rehearsal.png`, `process/*-painted.png`: accepted rehearsals and
  committed checkpoints, with companion greyscale views.
- `process/final-values.png`: the final greyscale value check.
- `process/timelapse-contact-sheet.png`: a visual overview of the painting's progress.
- `process/studies/`: the warm-up images and their contact sheet.
- `process/verification-reexport.png`: a fresh export from the saved session,
  verified identical to the delivered PNG.

## Painting observations and final assessment

### What changed while painting

1. **The sky wanted closer mixtures and softer joins.** The first bristle rehearsal
   of the horizon made scalloped bands. Loaded flat passes established the colour
   field; close-valued glazes softened its joins and carried the clouds. The horizon
   mixture was warmed from yellow-beige toward peach by increasing its cadmium red.
2. **The cottage view needed a drawing-level adjustment.** The two closest houses'
   original depths concealed too much of the cream cottage. Their depths were
   shortened in rehearsal, keeping that lit facade visible.
3. **Three holes in the walls were repaired with paint.** `solid=True` prevents paint
   running out, but shaped block-in paths can still wander apart. Three loaded flat
   marks closed those holes before the windows were painted.
4. **Details need the visible part of a surface.** An early plaster rehearsal put
   weathering back over a nearer cottage's side. The accepted pass restricts its
   strokes to the visible facade between the overlapping houses.
5. **The boat was painted as a hollow thing.** Its dark outer mass and far gunwale
   preceded the interior, floorboards, and seats. The nearer red hull and its short
   rim light came afterwards. A thin, slack rope attaches it to the quay.
6. **Reflections were built, then interrupted.** Broad shadow, soft underlying colour,
   unequal warm marks, smaller light marks, and dark-water cuts establish the broken
   vertical paths below the windows. The red boat's reflection was similarly cut
   through with blue water.
7. **The wall needed connected planes.** Four isolated light polygons looked like
   panels attached to the quay. The accepted planes tile the wall's actual face;
   a few stone surfaces and mortar joints supply its character. The rope was then
   repainted in front of those planes.
8. **The last substantial adjustment went to the sky.** Eight close-valued glazes
   quieted the remaining joins before the ten final light accents were placed.

Each paid pass was rehearsed and visually inspected before committing. The files
named `*-rehearsal.png` contain the accepted rehearsal; rejected variants were
replaced during iteration. The saved session retains the actual committed sequence.

### Useful Easel pitfalls from this session

- A small, partly loaded bristle mark readily becomes speckles or a little comb.
  This was particularly conspicuous in clouds and roof lights. Closer colours helped
  the roofs; soft glazes and longer, pressure-shaped round marks served the air and
  water better.
- `scumble()` accepts brush-field overrides, but `clip=` is supported by `stroke()`
  and `glaze()`. Passing `clip=` to `scumble()` raised `TypeError`. The sea's horizon
  was established with a hard-edged mass, with the graded passes positioned below it.
- A wide angled scumble can extend well beyond its named band. That first water
  rehearsal covered part of the sky. The accepted water pass accounts for brush width.
- Yellow-rich glazes over blue water produced greenish blooms. The accepted
  underlying reflection veils stay close to the water's violet-blue; the warm
  reflection strokes carry their own paint over a dried surface.
- Seven short, broad shadow strokes made spoon-shaped islands. A single connected
  reflection mass with a broken lower boundary was a better drawing of the passage.
- A late smudge at the headland pulled a bright thumbprint from the sky. That
  rehearsal was discarded; a close-valued film along the low edge was quieter.
- The engine's native GIF frames are previews. Keep the PNG for viewing the brushwork
  at full canvas resolution.

### Budget and focus

- **408 / 420 paid marks**, plus **3 free signature marks**: 411 painted marks total.
- **172 / 408 paid marks on the village and dinghy: 42.2%**, against 40% planned.
  Easel's report includes the three free signature marks in its share denominator,
  reporting 172 / 411, also rounded to 42%.
- When the boat's structure was complete, the subject occupied **152 / 249 marks
  (61.0%)**. Of the final 159 paid marks, **139** went to sky, water, quay, and edges;
  20 finished the village and boat, including restoring the rope.
- The final ten paid marks are five window cores, three reflected glints, a small
  boat-rim catch, and one cool touch on a bollard.
- Twelve marks remain in reserve. The open water and sky have the quiet I wanted;
  I stopped after the light accents and signature.

### Final look

The light sky, mid-valued water, and dark quay separate in greyscale. The small
window cores are the brightest accents. Roofs and selected building edges are firm;
clouds, distant water, and portions of the quay's reflection soften or disappear.
The limited red, ochre, violet, and blue mixtures keep the picture together.

The result has a simplified, illustrated character. The facades remain quite planar,
and some broad sky banding is still visible. Those are the weakest passages. The
strongest relationship is the little red boat against the cold water, with the
unequal paths of window light reaching toward it.

**Bare ground is only 0.06%**, below the guide's 0.5% threshold. The loaded sky and
sea buried almost all of the toned ground; the visible surface character comes from
worked paint. This is the clearest departure from the initial texture intention.

The reason for choosing the subject survived: the windows feel inhabited, their
warmth travels into the harbour, and the boat is held quietly beside the shore.

### Signature

At lower left, three fine blue marks suggest two little tide lines and a leaning
mast. It repeats the boat and water's motions, stays close to the surrounding value,
and occupies very little space. All three marks carry `note="signature"`.

## Re-export and continue

From this folder, using Python 3.12 or newer:

```powershell
python -m pip install -r requirements.txt
python paint.py report
python paint.py export
```

The saved session and `process/strokes.json` are the authoritative record. The
source contains the accepted recipes, including drawing and palette decisions
revised during rehearsals. To explore a new pass, rehearse it against a copy of
the saved session first.

The initial session was made with `python paint.py sketch`. Numbered passes were
run in the order shown in `STAGES`, each with `--rehearse` before the committed run.
The initial sketch command protects an existing session from replacement.

## Delivery verification

- Opened the final PNG at full resolution and inspected the final greyscale.
- PNG container and pixel data verified: **1440 x 960**, **387,083 bytes**.
- GIF: **360 x 240**, **78 frames**, **10.08 seconds**, loops continuously,
  **1,238,039 bytes**. Every frame decoded successfully; first and last differ.
- The final GIF frame matches the finished painting's thumbnail within GIF palette
  quantization: mean RGB difference **1.288 / 255**.
- Reloading the saved `.easel` file and exporting again produced a **SHA-256
  identical PNG**.
- Easel's final whole-painting report has no brushwork warnings; its separate bare
  ground measurement is discussed above.
- The Python files were formatted with CRLF line endings. Ruff's focused syntax,
  undefined-name, and unused-import checks passed.

PNG SHA-256:

```text
56f110bb5e98194b34b8702db77741d28b94978cbc9169d37ee83104766e57f9
```
