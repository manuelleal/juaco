import numpy as np, time
L=40; H=12; NI=8; NM=3
PA=np.array([1,1,0,1,0,0.]); PB=np.array([1,0,1,0,1,0.])
GRUPOS={ 'base':dict(eta=.02,tau_e=.85,aver=3.0,k=3),
         'lento':dict(eta=.01,tau_e=.95,aver=3.0,k=3),
         'rapido':dict(eta=.05,tau_e=.70,aver=3.0,k=3),
         'miedoso':dict(eta=.02,tau_e=.85,aver=8.0,k=2)}
class Agente:
    def __init__(s,rng,grupo):
        s.rng=rng; s.g=grupo; s.p=GRUPOS[grupo]
        s.W1=rng.uniform(.1,.5,(H,NI)); s.W2=rng.uniform(.1,.5,(NM,H)); s.Wh=rng.uniform(0,.3,NM)
        s.e1=np.zeros_like(s.W1); s.e2=np.zeros_like(s.W2); s.eh=np.zeros(NM)
        s.tr=np.zeros(NI); s.trh=np.zeros(H); s.pos=0; s.E=1.0; s.Rbar=0.0; s.objs={}
        s.spawn(); s.A=0; s.B=0; s.muertes=0
    def spawn(s):
        while len(s.objs)<4:
            x=int(s.rng.integers(L))
            if x not in s.objs: s.objs[x]='A' if s.rng.random()<.5 else 'B'
    def see(s):
        best=None
        for x,k in s.objs.items():
            dl=(s.pos-x)%L; dr=(x-s.pos)%L; d=min(dl,dr)
            if best is None or d<best[0]: best=(d,k,dl<dr)
        d,k,left=best; pat=PA if k=='A' else PB
        return np.concatenate([pat*1.2,[1.5 if left else 0,0 if left else 1.5]])
    def step(s):
        rng=s.rng; hambre=np.clip(1-s.E,0,1); x=s.see(); noise=.15+.6*hambre
        Vh=s.W1@x+rng.normal(0,noise,H); thr=np.sort(Vh)[-s.p['k']]
        ph=1/(1+np.exp(-(Vh-thr)/.2)); h=(Vh>=thr).astype(float)
        V=s.W2@h+s.Wh*hambre; p=1/(1+np.exp(-(V-1.0)/noise))
        u=p+rng.normal(0,.3,NM); m=np.zeros(NM)
        if u.max()>.5: m[np.argmax(u)]=1
        s.tr=s.tr*.7+x; s.trh=s.trh*.7+h; te=s.p['tau_e']
        s.e2=s.e2*te+np.outer(m-p,s.trh); s.e1=s.e1*te+np.outer(h-ph,s.tr)*(s.W2.T@(m-p))[:,None]; s.eh=s.eh*te+(m-p)*hambre
        s.pos=(s.pos+int(m[1]-m[0]))%L; s.E-=.004; R=0.0
        if m[2]==1 and s.pos in s.objs:
            if s.objs[s.pos]=='A': R=1.0; s.E=min(s.E+.8,1.5); s.A+=1
            else: R=-3.0; s.E-=.4; s.B+=1
            del s.objs[s.pos]; s.spawn()
        delta=R-s.Rbar; s.Rbar=.99*s.Rbar+.01*R
        g=s.p['eta']*(1+3*hambre)*delta*(s.p['aver'] if R<0 else 1.0)
        s.W2+=g*s.e2; s.W1+=g*s.e1; s.Wh+=g*s.eh
        if s.E<.3: s.W1*=.999; s.W2*=.999
        s.W1=np.clip(s.W1,0,1.5); s.W2=np.clip(s.W2,0,1.5); s.Wh=np.clip(s.Wh,0,1.5)
        if s.E<=0:
            s.muertes+=1; s.E=1.0; s.pos=int(rng.integers(L))
            s.W1=s.W1*.8+rng.uniform(.1,.5,(H,NI))*.2; s.W2=s.W2*.8+rng.uniform(.1,.5,(NM,H))*.2
    def score(s): return s.A-2*s.B
    def reset_counts(s): s.A=s.B=s.muertes=0
    def recibir(s,otro,mix=.3):
        s.W1=(1-mix)*s.W1+mix*otro.W1; s.W2=(1-mix)*s.W2+mix*otro.W2; s.Wh=(1-mix)*s.Wh+mix*otro.Wh
    def morir_renacer(s):
        r=s.rng; s.W1=s.W1*.5+r.uniform(.1,.5,(H,NI))*.5; s.W2=s.W2*.5+r.uniform(.1,.5,(NM,H))*.5; s.E=1.0

def experimento(seed=0,por_grupo=5,epocas=24,pasos=5000,compartir=True,seleccion=True):
    rng=np.random.default_rng(seed)
    pob=[Agente(np.random.default_rng(seed*1000+i),g) for i,g in enumerate([g for g in GRUPOS for _ in range(por_grupo)])]
    hist=[]; prev=None
    for ep in range(epocas):
        for a in pob: a.reset_counts()
        for t in range(pasos):
            for a in pob: a.step()
        sc=np.array([a.score() for a in pob]); A=np.array([a.A for a in pob]); B=np.array([a.B for a in pob])
        med=np.median(sc); mejor=pob[int(np.argmax(sc))]
        exito = prev is None or med>prev
        por_g={g:(A[[i for i,a in enumerate(pob) if a.g==g]].mean(),B[[i for i,a in enumerate(pob) if a.g==g]].mean()) for g in GRUPOS}
        hist.append((ep,med,A.mean(),B.mean(),mejor.g,exito,por_g))
        if compartir:
            for a in pob:
                if a is not mejor and a.score()<mejor.score(): a.recibir(mejor)
        if seleccion and not exito:
            orden=np.argsort(sc)
            for i in orden[:len(pob)//2]: pob[i].morir_renacer()
        prev=med
    return hist

if __name__=="__main__":
    t0=time.time()
    for nombre,kw in (("POBLACIÓN: comparte + selección",dict()),("CONTROL: solos, sin compartir ni selección",dict(compartir=False,seleccion=False))):
        print("\n=== "+nombre)
        for ep,med,A,B,mg,ex,pg in experimento(**kw):
            if ep%3==0 or ep==23:
                gs="  ".join(f"{g}:{a:.0f}/{b:.0f}" for g,(a,b) in pg.items())
                print(f" ep{ep:2d} mediana={med:6.1f} comida={A:5.1f} veneno={B:5.1f} ratio={A/max(B,1):.2f} mejor={mg:8s} {'viven' if ex else 'MUERE ½'}  | {gs}")
    print(f"\n{time.time()-t0:.0f}s")
