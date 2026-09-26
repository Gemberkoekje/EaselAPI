# The versions that were rehearsed and thrown away

The painter rehearsed 25 times and committed eleven passes, and each committed script is
the last version of its pass: every earlier one was rewritten in place, with the Write and
Edit tools or, twice, a PowerShell `-replace`. The ones this round needs are recovered here
**from the painting session's transcript**: every one of those 53 changes replayed in
order, which ends on the painter's folder in every script. Each of the 36 runs on the
painting's own session, run again on the canvas it opened on, gives the report the file
saved for it word for word, for all 31 that saved one, and the five that saved none raise
again. The rest of the rehearsals are not filed; the transcript holds them the same way.

| File | Marks | What the painter was after | What it read as |
|---|---|---|---|
| `p02_v1.py`, with `prelude_glow1.py` | 40 | the lamp's glow on the wall as an inward scumble | a rusty patch of rings ([`glow_rings.png`](../evidence/glow_rings.png)) |
| `p02_v2.py`, with `prelude_early.py` | 44 | the same, more rings, a more golden colour | a dark rim, like a knot in wood; `inward-comb` fired ([`glow_rim.png`](../evidence/glow_rim.png)) |
| `p02_v4.py`, with `prelude_early.py` | 29 | three soft films mixed close to the wall | a glow too small and faint; widened, the films stayed a faint disc the lantern would hide, and the pool was laid as three soft strokes of paint instead |
| `p03_v1_profiles.py`, with `prelude_early.py` | 135 | the Bell-Warden's structure: each mass in the light, then copies shifted away from the lamp in mid and shade | three profiles stacked in the face like cut paper, and stripes across the kerchief ([`face_profiles.png`](../evidence/face_profiles.png)) |
| `p03_v2_strip.py`, with `prelude_strip.py` | 101 | shadow masses with a half-tone band and a lit plane drawn as polygons, sharing the terminator | the light as a strip along the profile, because the terminator ran beside it ([`face_strip.png`](../evidence/face_strip.png)) |
| `p05_v1.py` | 25 | the face's sockets, eyes, nose, mouth and jaw | the nose's cast shadow, the cheek's hollow and the mark under the eye as smears and a bruise ([`face_marks.png`](../evidence/face_marks.png)) |
| `p06_v1.py` | 22 | knuckles and a thumb laid on the fist, the shawl bunched in it | the disc with knuckles on it — *the fist has failed twice, pointing to a drawing issue rather than shading* — and the next pass redrew it |
| `p08_v1.py` | 20 | the fist taken down into the dark it sits in | a bread roll ([`fist_bun.png`](../evidence/fist_bun.png)) |
| `p09_v1.py` | 22 | cloth bunched round the fist | a bun in a dark cup with a lid — the third miss ([`fist_cup.png`](../evidence/fist_cup.png)) |

The last two columns are the painter's own account of each version, from its session, in
the filer's words. The fist's first failure, a disc, is the committed figure pass, as its
rehearsal showed it ([`fist_disc.png`](../evidence/fist_disc.png)).

**Each rehearses on the canvas it was rehearsed on**, from the painting's own folder:

```bash
easel new wenna.easel --size 768x1024 --texture linen --ground umber_wash --seed 23 --budget 300
easel run wenna.easel versions/p02_v1.py --rehearse --prelude versions/prelude_glow1.py
easel run wenna.easel versions/p02_v2.py --rehearse --prelude versions/prelude_early.py   # and p02_v4
easel run wenna.easel p02_setting.py
easel run wenna.easel versions/p03_v1_profiles.py --rehearse --prelude versions/prelude_early.py
easel run wenna.easel versions/p03_v2_strip.py --rehearse --prelude versions/prelude_strip.py
easel run wenna.easel p03_figure.py p04_lantern.py
easel run wenna.easel versions/p05_v1.py --rehearse
easel run wenna.easel p05_face.py
easel run wenna.easel versions/p06_v1.py --rehearse
easel run wenna.easel p06_hand_cloth.py p07_fist.py
easel run wenna.easel versions/p08_v1.py --rehearse
easel run wenna.easel p08_finish.py
easel run wenna.easel versions/p09_v1.py --rehearse
```

Run so on the checkout at `v0.7.0` on 2026-09-26, each prints the block the painter's file
saved for it, word for word. The preludes differ from the painting's own in what the
painter changed next: `prelude_glow1.py` in the glow's colour alone; `prelude_early.py` in
the kerchief and the face — the kerchief a plain polygon, not yet roughened, and no lit
planes yet; `prelude_strip.py` in where the face's terminator runs — beside the profile,
where the painting's own runs back past the near eye's outer corner.

**The first drawing.** [`p01_v1.py`](p01_v1.py), with
[`prelude_draw1.py`](prelude_draw1.py), is the drawing as it was first run, on the scratch
canvas with a light ground, the head small and the arm raised to hold the lantern. On a
scratch session of its own,

```bash
easel new draft.easel --size 768x1024 --texture smooth --ground warm_white --seed 23 --no-prelude
LOOK=looks/01-drawing-light.png easel run draft.easel versions/p01_v1.py --prelude versions/prelude_draw1.py
```

it redraws [`drawing_first.png`](../evidence/drawing_first.png) to the pixel. The painter's
verdict on it: *the head's too small and the raised arm looks like sticks*.
