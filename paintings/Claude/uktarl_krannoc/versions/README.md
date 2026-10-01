# Three versions that were rehearsed and thrown away

The painter rehearsed 26 times and committed 17 passes. Each committed script is the last
version of its pass, because every earlier one was rewritten in place. Three of the earlier
ones carry claims of the verdict, so they are recovered here **from the painting session's
transcript**: the file the painter wrote, and the change to the prelude it ran with. Each
reprints its saved report when run on the canvas it was rehearsed on.

| File | Marks | Saved report | What the painter was after | What it read as |
|---|---|---|---|---|
| `p03_v1_facets.py` | 129 | 6th, from record 25 | the mountain as a mass built of planes: ten facets turned toward the lamp, laid on the stone | *fence posts on a flat violet stage flat*, at 129 strokes ([`mountain_facets.png`](../evidence/mountain_facets.png)) |
| `p06_v1_collar.py` | 85 | 16th, from record 114 | the collar black outside and red within, as two V-shaped masses | the right picture at 85 strokes: the collar alone cost 43 ([`collar_v.png`](../evidence/collar_v.png)) |
| `p08_v2_seam.py` | 7 | 25th, from record 219 | the light behind Uktarl as a pool, with a third stroke wider and fainter on each side | a pool, and a hard vertical seam on each side where its region ended ([`backlight_seam.png`](../evidence/backlight_seam.png)) |

The last two columns are the painter's own account of each version, from its session, in
the filer's words where they are not quoted.

**Each rehearses on the canvas it was rehearsed on**, from the painting's own folder:

```bash
easel new uktarl.easel --size 1024x768 --texture linen --ground "#54443a" --seed 31 --budget 450
easel run uktarl.easel p01_draw.py p02_wall.py
easel run uktarl.easel versions/p03_v1_facets.py --rehearse
easel run uktarl.easel p03_mountain.py p04_lamplight.py p05_floor_tub.py
easel run uktarl.easel versions/p06_v1_collar.py --rehearse
easel run uktarl.easel p06_uktarl_body.py p07_uktarl_head.py
easel run uktarl.easel versions/p08_v2_seam.py look_all.py --rehearse
```

Run so on 2026-10-01, on the checkout whose engine is `v0.8.0`'s, each lays the marks the
painter's rehearsal laid and prints its report word for word, except in three places:

- **The script's name**, in the `dearest:` and `laid at` lines: `p03_v1_facets.py:8` where
  the painter's report says `p03_mountain.py:8`. The line numbers are the painter's.
- **The plan's lines on the mountain's version.** The plan's places moved after that
  rehearsal: the glow's place went from the relief by his hand to the gilding above his
  head, and the mountain's value from `0.30` to `0.22`. So `plan:` and `lightest:` read the
  plan the folder holds now, not the one the painter's report read.
- **One fact at the call on the backlight's version**, `prelude-rebind`. The script binds
  `glow_left` and `glow_right` itself, as the prelude bound them before the painter widened
  them, and the check says that it does. Everything else in that report is the 25th's.

`p06_v1_collar.py` and `p08_v2_seam.py` carry the prelude's old shapes on their eighth and
ninth lines respectively, written as one long line each, so that every other line keeps
the number the painter's report gives it.
