# The two "graded passage laid too narrow" misfires, reconstructed

The painter's verdict said the post-pass check's *graded passage laid too narrow* line
fired twice on marks that were not a graded passage. Neither fire is in the session file
or in the committed passes: **both were printed by rehearsals** (`easel run --rehearse`),
which commit nothing, and both passes were rewritten before they were committed. The
painter rebuilt each from its session transcript and sent them; this directory is that
delivery, with the passes the filed painting already holds referenced rather than copied.

Each folder holds `prelude.py` **as it stood at that moment** -- the headland's is an
earlier prelude than the filed one, without the roughened silhouette, the clips on the
planes, or the `bands` and `ground` declarations; the water's differs from the filed one
in one mixture -- the pass as it was rehearsed, and the painter's own `rehearse.log`.
Re-run on the checkout at `v0.6.0` on 2026-09-23, **each prints the original line exactly**:

```bash
cd headland
easel new lighthouse.easel --size 1024x768 --texture linen --ground burnt_sienna --seed 11 --budget 300
easel run lighthouse.easel ../../p00_draw.py ../../p01_sky.py ../../p02_sea.py
easel run lighthouse.easel 03_headland_v2.py --rehearse
```

```bash
cd water
easel new lighthouse.easel --size 1024x768 --texture linen --ground burnt_sienna --seed 11 --budget 300
easel run lighthouse.easel ../../p00_draw.py ../../p01_sky.py ../../p02_sea.py \
    ../../p03_headland.py ../../p04_tower.py ../../p05_light.py
easel run lighthouse.easel 06_water_v1.py --rehearse
```

`easel run` loads the `prelude.py` beside the session file, so the session has to be
created inside the case's own folder for the prelude of that moment to be the one used.

| Case | The line | What the marks were |
|---|---|---|
| headland (the painter's `rehearse_006`) | 42 marks; *19 marks at stepping colours run parallel 0.020 apart, and the narrowest brush laying them is 0.006 -- 0.3 of that step* | the plane passes of two rock faces, a thin crevice (`round_hard`, 0.006) along their join, and a dry-brush scrape -- no gradient |
| water (the painter's `rehearse_011`) | 19 marks; *7 marks at stepping colours run parallel 0.009 apart, and the narrowest brush laying them is 0.006 -- 0.6 of that step* | eleven glints of a broken reflection, two thin dark ripple marks (0.006, 0.007) and surf -- no gradient either |

In both lines the `0.006` brush is one of the thin dark marks. The rule judges a stack's
step against the *narrowest* brush in it, so one accent laid among wide marks is enough
to make the stack read as a passage laid too narrow. What is done about it is workstream
C of `PLAN-0.7.0.md`.
