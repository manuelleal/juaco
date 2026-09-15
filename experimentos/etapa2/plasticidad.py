"""2L — plasticidad estructural en Kenyon: una celda con error de predicción crónico se divide."""
import numpy as np
L=40; NK=30; NKMAX=90; K=3
PAT={'A':np.array([1,1,0,1,0,0.]),'B':np.array([1,0,1,0,1,0.])}
R_VAL={'comida':1.0,'veneno':-3.0}; E_VAL={'comida':+0.8,'veneno':-0.4}
def run(seed,T=100000,solap=2,plast=True,theta=0.6,ema=0.02,paso=0.5,eta=.03,alpha=1.2,costo=.002,nobj=4):
    rng=np.random.default_rng(seed)
    Wl=rng.uniform(.1,.4,(2,9)); KW=np.zeros((NKMAX,6)); activa=np.zeros(NKMAX,bool)
    KW[:NK]=rng.uniform(0,1,(NK,6)); activa[:NK]=True
    # forzar solapamiento: 'solap' celdas dominadas por el píxel compartido (px 0)
    KW[:solap]=0; KW[:solap,0]=5.0
    def code(P):
        v=KW@P; v[~activa]=-1e9; return set(np.argsort(v)[-K:])
    while len(code(PAT['A'])&code(PAT['B']))!=solap:
        KW[solap:NK]=rng.uniform(0,1,(NK-solap,6))
    def kenyon(P): k=np.zeros(NKMAX); k[list(code(P))]=1; return k
    Wp=np.zeros(NKMAX); Wn=np.zeros(NKMAX); err=np.zeros(NKMAX); el=np.zeros_like(Wl); tr=np.zeros(9)
    pos=0; E=1.0; objs={}; val={'A':'comida','B':'veneno'}; tipos=['A','B']; splits=0; deaths=0; log=[]
    def spawn():
        while len(objs)<nobj:
            x=int(rng.integers(L))
            if x not in objs: objs[x]=tipos[int(rng.integers(2))]
    spawn()
    def see():
        best=None
        for x,k in objs.items():
            dl=(pos-x)%L; dr=(x-pos)%L; d=min(dl,dr)
            if best is None or d<best[0]: best=(d,k,dl<dr)
        return best
    mord={'A':0,'B':0}
    for t in range(T):
        hambre=np.clip(1-E,0,1); d,k,left=see(); pat=PAT[k]
        x=np.concatenate([pat*1.2,[1.5 if left else 0,0 if left else 1.5,1.0 if d==0 else 0.]]); noise=.15+.5*hambre
        V=Wl@x; p=1/(1+np.exp(-(V-.8)/noise)); u=p+rng.normal(0,.3,2); m=np.zeros(2)
        if u.max()>.5: m[np.argmax(u)]=1
        tr=tr*.7+x; el=el*.85+np.outer(m-p,tr)
        pos=(pos+int(m[1]-m[0]))%L; d2,_,_=see(); Rp=.2 if d2<d else 0.; R=0.
        if pos in objs:
            kk=objs[pos]; P=PAT[kk]; kc=kenyon(P); Wb=Wp-Wn
            Vb=alpha*(Wb@kc)+2.0*hambre+.5; pb=1/(1+np.exp(-Vb/.3))
            if rng.random()<pb:
                R=R_VAL[val[kk]]; E=min(E+E_VAL[val[kk]],1.5); mord[kk]+=1; del objs[pos]; spawn()
                dlt=R-Wb@kc
                if dlt>0: Wp=np.clip(Wp+eta*dlt*kc,0,3.)
                else:     Wn=np.clip(Wn+eta*(-dlt)*kc,0,3.)
                if plast:
                    idx=np.where(kc>0)[0]; err[idx]=(1-ema)*err[idx]+ema*abs(dlt)
                    for c in idx:
                        if err[c]>theta and (~activa).any():
                            j=int(np.where(~activa)[0][0]); activa[j]=True
                            KW[j]=np.clip(KW[c]+paso*(P-KW[c]),0,5); KW[c]=np.clip(KW[c]-paso*(P-KW[c]),0,5)   # hija hacia el patrón, madre lejos
                            Wp[j]=Wp[c]; Wn[j]=Wn[c]; err[c]=err[j]=0; splits+=1
        E-=costo
        if rng.random()<.003 and objs: del objs[list(objs)[int(rng.integers(len(objs)))]]; spawn()
        Wl=np.clip(Wl+eta*(1+2*hambre)*(max(R,0)+Rp)*el,0,1.5)
        if E<=0: deaths+=1; E=.6; pos=int(rng.integers(L))
        if t%25000==0 or t==T-1: log.append((t,len(code(PAT['A'])&code(PAT['B'])),round(float((Wp-Wn)@kenyon(PAT['A'])),2),round(float((Wp-Wn)@kenyon(PAT['B'])),2)))
    return dict(log=log,splits=splits,deaths=deaths,mord=mord,celdas=int(activa.sum()),
                WA=round(float((Wp-Wn)@kenyon(PAT['A'])),2),WB=round(float((Wp-Wn)@kenyon(PAT['B'])),2),ov=len(code(PAT['A'])&code(PAT['B'])))
if __name__=="__main__":
    for solap in (2,3):
        for plast in (False,True):
            print(f"\n=== A∩B forzado = {solap}   plasticidad {'ON' if plast else 'OFF'}")
            print("seed | solapamiento t=0 25k 50k 75k fin | W_A fin | W_B fin | divisiones | celdas | veneno | muertes")
            for s in range(1,9):
                r=run(s,solap=solap,plast=plast)
                ovs=" ".join(str(x[1]) for x in r['log'])
                print(f" {s:3d} | {ovs:28s} | {r['WA']:+6.2f} | {r['WB']:+6.2f} | {r['splits']:4d}       | {r['celdas']:3d}    | {r['mord']['B']:4d}   | {r['deaths']}")
