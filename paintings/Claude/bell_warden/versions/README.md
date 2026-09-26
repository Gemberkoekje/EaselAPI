# The versions that were rehearsed and thrown away

The painter rehearsed nineteen times and committed seven passes, and each committed script
is the last version of its pass: every earlier one was rewritten in place. The ones this
round needs are recovered here — the first drawing, the five versions of the subject's
pass before the committed one, the three of the details pass, and the drawing check the
painter judged its second drawing on — **from the painting session's transcript**: every file the painter
wrote, edited, or rewrote with a script in the painting's folder, replayed in order. The
replay ends byte for byte on the folder the painter left, and every one of the session
file's 27 saved reports comes back word for word when the version that printed it is run
on the canvas it opened on. The one rehearsal that raised, on `at_value(..., 0.13)`, raises
again. The other eleven rehearsals — the room's four, the plinth's four, the finish's two
and the glow's one — are not filed; the transcript holds them the same way.

| File | Marks | What the painter was after | What it read as |
|---|---|---|---|
| `p04_v1_cat.py`, with `prelude_cat.py` | 85 | the silhouette in shade, the near wing mid, the planes of light laid on it | a cat: two symmetric peaks are ears, and the light sits on the dark as patches ([`subject_cat.png`](../evidence/subject_cat.png)) |
| `p04_v2_piebald.py` | 98 | the redrawn profile: the wing, the body in shade, then the lit planes | a piebald: the planes are islands ([`subject_piebald.png`](../evidence/subject_piebald.png)) |
| `p04_v3_arch.py` | 113 | a warmer body, one continuous lit side joined to the shade | an arch: a lit band wrapped round a hollow ([`subject_arch.png`](../evidence/subject_arch.png)) |
| `p04_v4_rim.py` | 101 | the lit rim from two copies of the silhouette, one shifted toward the light and one away from it | a flat cut-out, sawtoothed along the rim |
| `p04_v5_bars.py` | 101 | the committed structure: the silhouette in the light, then the mid and the shade from copies shifted away from it | right, and told *a stack of bars*: its three layers ran along one axis, which the committed pass varies |
| `p05_v1.py` | 22 | the ember, the claws, the brow, the maw, a horn, dry brush | a rabbit's head or a goat's; claws too small to grip; a floating maw |
| `p05_v2.py` | 67 | a core shadow, a far horn, a wedge of a maw, larger claws, lights along the edges that face the lamp | the head's top at `0.52` on the `lightest:` line, where its plane was mixed at `0.64` — taken for paint dragged by the wet shade |
| `p05_v3.py` | 68 | `p05_v2.py` with an `s.dry()` before the head and another before the lights, and a film on the plinth's front | the head's top still at `0.52` — put down, then, to the eye inside the place; committed with its lights' tips wobbled |

The last two columns are the painter's own account of each version, from its session, in
the filer's words.

**Each rehearses on the canvas it was rehearsed on**, from the painting's own folder:

```bash
easel new bell.easel --size 1024x768 --texture linen --ground umber_wash --seed 11 --budget 300
easel run bell.easel p01_draw.py p02_room.py p03_plinth.py
easel run bell.easel versions/p04_v1_cat.py --rehearse --prelude versions/prelude_cat.py
easel run bell.easel p01_draw.py
easel run bell.easel versions/p04_v2_piebald.py --rehearse    # and v3, v4, v5
easel run bell.easel p04_gargoyle.py
easel run bell.easel versions/p05_v2.py --rehearse            # and v1, v3
```

Run so on the checkout at `v0.7.0` on 2026-09-26, each prints the block the painter's file
saved for it, word for word. `prelude_cat.py` is the prelude as it stood from the room's
commit through the cat: the room and the plinth as they are now, and the first typed
silhouette — 32 points and a tail, its lit planes named `face lit`, `wing edge lit`,
`chest lit`, `shoulder lit` and `haunch lit`. Every later version ran on the painting's own
prelude, which is why the cat's report calls the lightest place *face lit* and every later
one *head top*: the plan's place was renamed with the drawing.

**The first drawing.** [`p01_v1_union.py`](p01_v1_union.py), with
[`prelude_union.py`](prelude_union.py), is the drawing pass as it was first run, before
any paint: guides only, and a creature that is a `union()` of eight ellipses and ribbons
— a head, a muzzle, a torso, two wings, a haunch, a hind foot and an arm. On a fresh
canvas,

```bash
easel new bell.easel --size 1024x768 --texture linen --ground umber_wash --seed 11 --budget 300
easel run bell.easel versions/p01_v1_union.py --prelude versions/prelude_union.py
```

it redraws [`drawing_first.png`](../evidence/drawing_first.png) to the pixel and prints
the file's first report, `plan-pairs` and all. The painter's verdict on it is its notes'
first line: *a box with a spiky blob on it*.

**The drawing check.** [`drawing_check.py`](drawing_check.py) is the throwaway canvas the
painter judged its second drawing on, verbatim: a light ground, and each shape's `.closed`
in pencil with `smooth=False`. It reads `prelude.py` from the folder it runs in, and the
prelude it read then is [`prelude_drawing.py`](prelude_drawing.py) — the silhouette before
its last three fixes: the horn curved back, the belly lowered, the wing's scallops
deepened. Copied beside it as `prelude.py`, the script redraws
[`drawing_check_corners.png`](../evidence/drawing_check_corners.png) to the pixel; with
`smooth=False` taken off and the planes' pressure at `0.4` rather than `0.35`, it redraws
[`drawing_check_smooth.png`](../evidence/drawing_check_smooth.png), the pot.
