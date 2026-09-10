from easel import Session
p = Session(200,200,seed=1).palette
def show(n,c): print(f"{n:24s} {p.hex(c)}  v={p.value_of(c):.3f}")
t = p.mix("burnt_sienna","cadmium_red",0.32)
show("terra raw", t)
for r in (0.20,0.35,0.50,0.65):
    show(f"+ochre {r}", p.mix(t,"yellow_ochre",r))
for r in (0.35,0.50,0.65):
    show(f"+ochre{r}+w.18", p.tint(p.mix(t,"yellow_ochre",r),0.18))
    show(f"+ochre{r}+w.30", p.tint(p.mix(t,"yellow_ochre",r),0.30))
show("+cadyellow .30", p.mix(t,"cadmium_yellow",0.30))
show("+cadyellow .45", p.mix(t,"cadmium_yellow",0.45))
show("+cadyel.35+w.12", p.tint(p.mix(t,"cadmium_yellow",0.35),0.12))
show("mid tint .12", p.tint(t,0.12))
show("shadow +ultra .40", p.mix(t,"ultramarine",0.40))
show("shadow +ultra .50", p.mix(t,"ultramarine",0.50))
show("refl", p.mix(p.mix(t,"ultramarine",0.45),"burnt_sienna",0.55))
show("rimhi", p.tint(p.mix(t,"cadmium_yellow",0.45),0.30))
