"""
Organismo v4 — engranes en su sitio.
 - Retina 6px (patrón del objeto más cercano) + dirección (2) + "estoy encima" (1) + hambre (1).
 - Locomoción: 2 motores con inhibición mutua, camino directo, R-STDP con error de predicción.
 - Boca: circuito aparte, decide morder solo estando encima. Sin sesgo global aprendible:
   el hambre empuja a morder; el miedo solo puede aprender "ESTE patrón no".
 - Muerte: la energía se reinicia, la memoria casi no se toca (el que muere es el cuerpo).
"""
import numpy as np
L=40
PA=np.array([1,1,0,1,0,0.]); PB=np.array([1,0,1,0,1,0.])
def run(seed,T=100000,eta=.03,tau_e=.85,hambre_boca=2.0,aversion=1.0,olvido_muerte=.0,learn=True,nobj=4,costo=.002,invertir_en=None):
    rng=np.random.default_rng(seed)
    Wl=rng.uniform(.1,.4,(2,9)); NK=30; KW=rng.uniform(0,1,(NK,6)); Wb=np.zeros(NK)   # cuerpo fungiforme
    def kenyon(pat):
        v=KW@pat; k=np.zeros(NK); k[np.argsort(v)[-3:]]=1; return k
    el=np.zeros_like(Wl); tr=np.zeros(9); pos=0; E=1.0; Rbar=0.0; objs={}
    def spawn():
        while len(objs)<nobj:
            x=int(rng.integers(L))
            if x not in objs: objs[x]='A' if rng.random()<.5 else 'B'
    spawn(); ateA=[]; ateB=[]; deaths=0; mordidas=0
    def see():
        best=None
        for x,k in objs.items():
            dl=(pos-x)%L; dr=(x-pos)%L; d=min(dl,dr)
            if best is None or d<best[0]: best=(d,k,dl<dr)
        d,k,left=best; pat=PA if k=='A' else PB
        return pat,d,left
    comida='A'; pre=[]; tA=None; tB=None; wbq=[]; hB=[]; mordB=[0,0,0,0]
    for t in range(T):
        if invertir_en is not None and t==invertir_en: comida='B'; pre=[Wb@kenyon(PA),Wb@kenyon(PB)]
        hambre=np.clip(1-E,0,1)
        pat,d,left=see()
        x=np.concatenate([pat*1.2,[1.5 if left else 0,0 if left else 1.5,1.0 if d==0 else 0.0]])
        noise=.15+.5*hambre
        # --- patas ---
        V=Wl@x; p=1/(1+np.exp(-(V-.8)/noise))
        u=p+rng.normal(0,.3,2); m=np.zeros(2)
        if u.max()>.5: m[np.argmax(u)]=1
        tr=tr*.7+x
        if learn: el=el*tau_e+np.outer(m-p,tr)
        dprev=d; pos=(pos+int(m[1]-m[0]))%L
        _,d2,_=see(); Rpatas=0.2 if d2<dprev else 0.0
        # --- boca ---
        R=0.0; mordio=0; pb=0.0
        if pos in objs:
            kc=kenyon(pat); Vb=Wb@kc+hambre_boca*hambre+0.5                       # sesgo fijo: la boca quiere
            pb=1/(1+np.exp(-Vb/.3)); mordio=float(rng.random()<pb); mordidas+=mordio
            if mordio:
                if objs[pos]=='B':
                    mordB[min(t//(T//4),3)]+=1
                    if t>=(invertir_en or T) and len(hB)<3: hB.append(round(float(hambre),2))
                if objs[pos]==comida: R=1.0; E=min(E+.8,1.5); ateA.append(t)
                else: R=-3.0; E-=.4; ateB.append(t)
                del objs[pos]; spawn()
            elif learn:                                            # no mordió: no aprende de eso
                pass
        E-=costo
        if rng.random()<0.003 and objs:                       # el mundo fluye: algo se pudre y algo nace
            del objs[list(objs)[int(rng.integers(len(objs)))]]; spawn()
        # --- aprendizaje ---
        delta=R-Rbar; Rbar=.99*Rbar+.01*R
        if learn:
            if pos not in objs or True:
                Wl=np.clip(Wl+eta*(1+2*hambre)*(max(delta,0)+Rpatas)*el,0,1.5)
            if mordio:                                             # sabor -> consecuencia, específico al patrón
                g=eta*(aversion if R<0 else 1.0)*delta
                Wb=np.clip(Wb+g*kc,-3.0,3.0)
        if invertir_en is not None and t>invertir_en and t%200==0:
            wa=Wb@kenyon(PA); wb=Wb@kenyon(PB)
            if tA is None and wa<0: tA=t-invertir_en
            if tB is None and wb>pre[1]/2: tB=t-invertir_en
        if (t+1)%(T//4)==0: wbq.append(round(float(Wb@kenyon(PB)),2))
        if E<=0:
            deaths+=1; E=.6; pos=int(rng.integers(L))
            Wl=(1-olvido_muerte)*Wl+olvido_muerte*rng.uniform(.1,.4,(2,9)); Wb*=(1-olvido_muerte)
    a=np.array(ateA); b=np.array(ateB); q=T//4
    f=lambda arr,i:((arr>=i*q)&(arr<(i+1)*q)).sum()
    return [(f(a,i),f(b,i)) for i in range(4)],deaths,np.array([Wb@kenyon(PA),Wb@kenyon(PB)]),pre,tA,tB,wbq,hB,mordB
if False:
    for learn in (True,False):
        print("=== "+("APRENDE" if learn else "azar"))
        for s in (1,2,3,4,5,6):
            qs,d,Wb=run(s,learn=learn)
            tot=sum(a for a,_ in qs),sum(b for _,b in qs)
            print(f"  seed {s}: comida/veneno por cuarto: "+"  ".join(f"{a:3d}/{b:3d}" for a,b in qs)+f"  ratio final={qs[3][0]/max(qs[3][1],1):5.1f} muertes {d:3d}  Wb·A={Wb[0]:+.2f} Wb·B={Wb[1]:+.2f}")
