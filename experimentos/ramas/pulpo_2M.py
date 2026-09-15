"""2M — pulpo: dos evaluadores semiautónomos (brazos) con energía compartida vs un evaluador central. 6 estímulos."""
import numpy as np
L=40; K=3
def patrones(rng,n=6):
    P=[]
    while len(P)<n:
        p=np.zeros(6); p[rng.choice(6,3,replace=False)]=1
        if not any(np.array_equal(p,q) for q in P): P.append(p)
    return P
class Brazo:
    def __init__(s,rng,NK):
        s.NK=NK; s.KW=rng.uniform(0,1,(NK,6)); s.Wp=np.zeros(NK); s.Wn=np.zeros(NK)
    def code(s,P): k=np.zeros(s.NK); k[np.argsort(s.KW@P)[-K:]]=1; return k
    def valor(s,P): return (s.Wp-s.Wn)@s.code(P)
    def aprende(s,P,R,eta=.03):
        kc=s.code(P); dlt=R-(s.Wp-s.Wn)@kc
        if dlt>0: s.Wp=np.clip(s.Wp+eta*dlt*kc,0,3.)
        else:     s.Wn=np.clip(s.Wn+eta*(-dlt)*kc,0,3.)
def run(seed,T=100000,brazos=2,NK_total=60,nobj=6,alpha=1.2,costo=.002):
    rng=np.random.default_rng(seed); PAT=patrones(rng); VAL=['comida']*3+['veneno']*3
    R_VAL={'comida':1.0,'veneno':-3.0}; E_VAL={'comida':+0.8,'veneno':-0.4}
    B=[Brazo(rng,NK_total//brazos) for _ in range(brazos)]
    Wl=rng.uniform(.1,.4,(2,9)); el=np.zeros_like(Wl); tr=np.zeros(9)
    pos=0; E=1.0; objs={}; deaths=0; uso=np.zeros((brazos,6),int)
    def spawn():
        while len(objs)<nobj:
            x=int(rng.integers(L))
            if x not in objs: objs[x]=int(rng.integers(6))
    spawn()
    def see():
        best=None
        for x,k in objs.items():
            dl=(pos-x)%L; dr=(x-pos)%L; d=min(dl,dr)
            if best is None or d<best[0]: best=(d,k,dl<dr)
        return best
    q=lambda t:min(t//(T//4),3); ven=[0]*4; com=[0]*4; err_t=[]
    for t in range(T):
        hambre=np.clip(1-E,0,1); d,k,left=see(); pat=PAT[k]
        x=np.concatenate([pat*1.2,[1.5 if left else 0,0 if left else 1.5,1.0 if d==0 else 0.]]); noise=.15+.5*hambre
        V=Wl@x; p=1/(1+np.exp(-(V-.8)/noise)); u=p+rng.normal(0,.3,2); m=np.zeros(2)
        if u.max()>.5: m[np.argmax(u)]=1
        tr=tr*.7+x; el=el*.85+np.outer(m-p,tr)
        pos=(pos+int(m[1]-m[0]))%L; d2,_,_=see(); Rp=.2 if d2<d else 0.; R=0.
        if pos in objs:
            kk=objs[pos]; P=PAT[kk]
            vals=[b.valor(P) for b in B]; i=int(np.argmax(np.abs(vals))) if brazos>1 else 0   # el centro: actúa el brazo más seguro
            Vb=alpha*vals[i]+2.0*hambre+.5; pb=1/(1+np.exp(-Vb/.3))
            if rng.random()<pb:
                R=R_VAL[VAL[kk]]; E=min(E+E_VAL[VAL[kk]],1.5); del objs[pos]; spawn()
                (ven if VAL[kk]=='veneno' else com)[q(t)]+=1; uso[i,kk]+=1
                B[i].aprende(P,R)          # solo aprende el brazo que actuó
        E-=costo
        if rng.random()<.003 and objs: del objs[list(objs)[int(rng.integers(len(objs)))]]; spawn()
        Wl=np.clip(Wl+eta_l(hambre)*(max(R,0)+Rp)*el,0,1.5) if False else np.clip(Wl+.03*(1+2*hambre)*(max(R,0)+Rp)*el,0,1.5)
        if E<=0: deaths+=1; E=.6; pos=int(rng.integers(L))
        if t%10000==0:
            # error de valor del sistema: para cada estímulo, valor del brazo que actuaría vs valor real
            e=np.mean([abs(max([b.valor(PAT[j]) for b in B],key=abs)-R_VAL[VAL[j]]) for j in range(6)]); err_t.append(round(float(e),2))
    # especialización: fracción de estímulos donde un brazo hizo >80% de las mordidas
    esp=np.mean([(uso[:,j].max()/max(uso[:,j].sum(),1))>.8 for j in range(6)]) if brazos>1 else None
    return dict(ven=ven,com=com,deaths=deaths,err_t=err_t,esp=esp,uso=uso)
if __name__=="__main__":
    for nombre,br in (("CENTRAL 1 evaluador × 60 celdas",1),("PULPO 2 brazos × 30 celdas",2),("PULPO 3 brazos × 20 celdas",3)):
        print(f"\n=== {nombre}")
        print("seed | veneno por cuarto | comida por cuarto | muertes | error de valor cada 10k pasos               | especialización")
        V=[];D=[];Ef=[]
        for s in range(1,9):
            r=run(s,brazos=br)
            V.append(r['ven'][3]); D.append(r['deaths']); Ef.append(r['err_t'][-1])
            print(f" {s:3d} | {' '.join(f'{v:3d}' for v in r['ven'])}   | {' '.join(f'{v:3d}' for v in r['com'])}   | {r['deaths']:4d}    | {' '.join(f'{e:4.2f}' for e in r['err_t'])} | {'' if r['esp'] is None else f'{100*r[chr(101)+chr(115)+chr(112)]:.0f}% de estímulos con brazo dueño'}")
        print(f"   mediana veneno Q4 {np.median(V):.0f} | muertes {np.median(D):.0f} | error de valor final {np.median(Ef):.2f}")
