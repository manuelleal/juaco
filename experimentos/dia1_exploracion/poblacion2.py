import numpy as np, time
L=40; NK=30
PA=np.array([1,1,0,1,0,0.]); PB=np.array([1,0,1,0,1,0.])
KW=np.random.default_rng(999).uniform(0,1,(NK,6))          # expansión común a la especie
def kenyon(pat):
    v=KW@pat; k=np.zeros(NK); k[np.argsort(v)[-3:]]=1; return k
GRUPOS={'base':dict(eta=.03,hambre_boca=2.0,aversion=3.0),
        'lento':dict(eta=.01,hambre_boca=2.0,aversion=3.0),
        'valiente':dict(eta=.03,hambre_boca=4.0,aversion=1.5),
        'miedoso':dict(eta=.03,hambre_boca=1.0,aversion=8.0)}
class Org:
    def __init__(s,rng,g):
        s.rng=rng; s.g=g; s.p=GRUPOS[g]; s.Wl=rng.uniform(.1,.4,(2,9)); s.Wb=np.zeros(NK)
        s.el=np.zeros_like(s.Wl); s.tr=np.zeros(9); s.pos=0; s.E=1.0; s.Rbar=0; s.objs={}; s.spawn(); s.reset()
    def reset(s): s.A=s.B=s.muertes=0
    def spawn(s):
        while len(s.objs)<6:
            x=int(s.rng.integers(L))
            if x not in s.objs: s.objs[x]='A' if s.rng.random()<.5 else 'B'
    def see(s):
        best=None
        for x,k in s.objs.items():
            dl=(s.pos-x)%L; dr=(x-s.pos)%L; d=min(dl,dr)
            if best is None or d<best[0]: best=(d,k,dl<dr)
        d,k,left=best; return (PA if k=='A' else PB),d,left
    def step(s):
        rng=s.rng; hambre=np.clip(1-s.E,0,1); pat,d,left=s.see()
        x=np.concatenate([pat*1.2,[1.5 if left else 0,0 if left else 1.5,1.0 if d==0 else 0.]]); noise=.15+.5*hambre
        V=s.Wl@x; p=1/(1+np.exp(-(V-.8)/noise)); u=p+rng.normal(0,.3,2); m=np.zeros(2)
        if u.max()>.5: m[np.argmax(u)]=1
        s.tr=s.tr*.7+x; s.el=s.el*.85+np.outer(m-p,s.tr)
        s.pos=(s.pos+int(m[1]-m[0]))%L; _,d2,_=s.see(); Rp=.2 if d2<d else 0.
        R=0.; mordio=0; pb=0.; kc=None
        if s.pos in s.objs:
            kc=kenyon(pat); Vb=s.Wb@kc+s.p['hambre_boca']*hambre+.5; pb=1/(1+np.exp(-Vb/.3)); mordio=float(rng.random()<pb)
            if mordio:
                if s.objs[s.pos]=='A': R=1.; s.E=min(s.E+.8,1.5); s.A+=1
                else: R=-3.; s.E-=.4; s.B+=1
                del s.objs[s.pos]; s.spawn()
        s.E-=.002
        if rng.random()<.003 and s.objs: del s.objs[list(s.objs)[int(rng.integers(len(s.objs)))]]; s.spawn()
        delta=R-s.Rbar; s.Rbar=.99*s.Rbar+.01*R; eta=s.p['eta']
        s.Wl=np.clip(s.Wl+eta*(1+2*hambre)*(max(delta,0)+Rp)*s.el,0,1.5)
        if mordio: s.Wb=np.clip(s.Wb+eta*(s.p['aversion'] if R<0 else 1.)*(mordio-pb)*delta*kc,-3,3)
        if s.E<=0: s.muertes+=1; s.E=.6; s.pos=int(rng.integers(L))
    def score(s): return s.A-3*s.B-2*s.muertes
    def recibir(s,o,mix=.3): s.Wl=(1-mix)*s.Wl+mix*o.Wl; s.Wb=(1-mix)*s.Wb+mix*o.Wb
    def renacer(s): s.Wl=s.rng.uniform(.1,.4,(2,9)); s.Wb=np.zeros(NK); s.E=1.

def experimento(seed,compartir,seleccion,por_grupo=5,epocas=16,pasos=5000):
    pob=[Org(np.random.default_rng(seed*1000+i),g) for i,g in enumerate([g for g in GRUPOS for _ in range(por_grupo)])]
    prev=None; out=[]
    for ep in range(epocas):
        for a in pob: a.reset()
        for t in range(pasos):
            for a in pob: a.step()
        sc=np.array([a.score() for a in pob]); A=np.array([a.A for a in pob]); B=np.array([a.B for a in pob]); D=np.array([a.muertes for a in pob])
        med=np.median(sc); mejor=pob[int(np.argmax(sc))]; exito=prev is None or med>=prev
        pg={g:(np.mean([a.A for a in pob if a.g==g]),np.mean([a.B for a in pob if a.g==g]),np.mean([a.muertes for a in pob if a.g==g])) for g in GRUPOS}
        out.append((ep,med,A.mean(),B.mean(),D.mean(),mejor.g,exito,pg))
        if compartir:
            for a in pob:
                if a is not mejor and a.score()<mejor.score(): a.recibir(mejor)
        if seleccion and not exito:
            for i in np.argsort(sc)[:len(pob)//2]: pob[i].renacer()
        prev=med
    return out
if __name__=="__main__":
    t0=time.time()
    for nombre,c,s in (("POBLACIÓN: comparte + selección",True,True),("CONTROL: cada uno solo",False,False)):
        print("\n=== "+nombre)
        for ep,med,A,B,D,mg,ex,pg in experimento(1,c,s):
            if ep%3==0 or ep==15:
                gs="  ".join(f"{g}:{a:.0f}/{b:.0f}/{d:.0f}" for g,(a,b,d) in pg.items())
                print(f" ep{ep:2d} mediana={med:6.1f} comida={A:5.1f} veneno={B:4.1f} muertes={D:4.1f} mejor={mg:8s} {'viven' if ex else 'MUERE ½'} | {gs}")
    print(f"\n{time.time()-t0:.0f}s")
