"""
Organismo v7d = v7 + decaimiento local en Wp/Wn (arreglo candidato de BUG-01). lam=0.0 reproduce v7 exactamente.
BUG-01: bajo refuerzo contradictorio sobre un código compartido, Wp y Wn corren los DOS al techo del clip y su
diferencia se anula exactamente, congelando el aprendizaje. El decaimiento es LOCAL (solo celdas del código activo)
y solo en el momento de morder: uno global destruiría el valor de los estímulos no visitados y rompería E2I.
Equilibrio analítico: W* = 3*eta*R/(3*eta+lam).  Preregistro en experimentos/bug01/PREREGISTRO.md.

Organismo v7 = v6 + 2L (plasticidad estructural en Kenyon: celda con error de predicción crónico se divide hacia lo distintivo).
Parámetro plast=True/False; solap_AB fuerza solapamiento inicial A∩B (None = 0 como en v6).

Organismo v6 — consolidación de todo lo aprendido (Etapas 1–2, 2A..2K).
Mecanismos: patas apetitivas/curiosas con R-STDP; boca separada con expansión Kenyon (30 celdas, 3 ganadoras),
canales apetitivo/aversivo separados, error de predicción por estímulo (Rescorla-Wagner), política alpha*valor + 2*hambre + 0.5,
percepción sincronizada (la boca mira lo que pisa), muerte del cuerpo sin olvido, mundo con renovación.
Escenarios: invertir_en (A<->B), nuevo (estímulo C/D en t=nuevo_en con valencia dada y solapamiento forzado con B).
"""
import numpy as np
L=40; NK=30; NKMAX=90; K=3
PAT={'A':np.array([1,1,0,1,0,0.]),'B':np.array([1,0,1,0,1,0.]),'C':np.array([0,1,1,0,0,1.]),'D':np.array([0,0,1,0,1,1.])}
R_VAL={'comida':1.0,'veneno':-3.0}; E_VAL={'comida':+0.8,'veneno':-0.4}

def run(seed,T=100000,learn=True,invertir_en=None,nuevo=None,nuevo_en=50000,nuevo_val='veneno',solap_B=None,
        eta=.03,tau_e=.85,alpha=1.2,hambre_boca=2.0,aversion=1.0,costo=.002,nobj=4,log_cada=None,plast=True,theta=0.6,ema=0.02,paso=0.5,solap_AB=None,lam=0.0):
    rng=np.random.default_rng(seed)
    Wl=rng.uniform(.1,.4,(2,9)); KW=np.zeros((NKMAX,6)); activa=np.zeros(NKMAX,bool); KW[:NK]=rng.uniform(0,1,(NK,6)); activa[:NK]=True
    def code(P):
        v=KW@P; v=np.where(activa,v,-1e9); return set(np.argsort(v)[-K:])
    objetivo_AB=0 if solap_AB is None else solap_AB
    if solap_AB: KW[:solap_AB]=0; KW[:solap_AB,0]=5.0
    cond=lambda: len(code(PAT['A'])&code(PAT['B']))==objetivo_AB and (nuevo is None or solap_B is None or (len(code(PAT[nuevo])&code(PAT['B']))==solap_B and len(code(PAT[nuevo])&code(PAT['A']))==0))
    while not cond(): KW[objetivo_AB:NK]=rng.uniform(0,1,(NK-objetivo_AB,6))
    def kenyon(P): k=np.zeros(NKMAX); k[list(code(P))]=1; return k
    Wp=np.zeros(NKMAX); Wn=np.zeros(NKMAX); err=np.zeros(NKMAX); mu=np.zeros((NKMAX,6)); splits=0; el=np.zeros_like(Wl); tr=np.zeros(9)
    pos=0; E=1.0; objs={}; val={'A':'comida','B':'veneno'}
    tipos=['A','B']
    def spawn():
        while len(objs)<nobj:
            x=int(rng.integers(L))
            if x not in objs: objs[x]=tipos[int(rng.integers(len(tipos)))]
    spawn()
    q=lambda t:min(t//(T//4),3)
    split_t=[]; mord={k:[0]*4 for k in PAT}; vis={k:[0]*4 for k in PAT}; deaths=0; log=[]
    def see():
        best=None
        for x,k in objs.items():
            dl=(pos-x)%L; dr=(x-pos)%L; d=min(dl,dr)
            if best is None or d<best[0]: best=(d,k,dl<dr)
        return best
    for t in range(T):
        if invertir_en is not None and t==invertir_en: val={'A':'veneno','B':'comida'}
        if nuevo is not None and t==nuevo_en: tipos.append(nuevo); val[nuevo]=nuevo_val
        hambre=np.clip(1-E,0,1); d,k,left=see(); pat=PAT[k]
        x=np.concatenate([pat*1.2,[1.5 if left else 0,0 if left else 1.5,1.0 if d==0 else 0.]]); noise=.15+.5*hambre
        V=Wl@x; p=1/(1+np.exp(-(V-.8)/noise)); u=p+rng.normal(0,.3,2); m=np.zeros(2)
        if u.max()>.5: m[np.argmax(u)]=1
        tr=tr*.7+x
        if learn: el=el*tau_e+np.outer(m-p,tr)
        pos=(pos+int(m[1]-m[0]))%L; d2,_,_=see(); Rp=.2 if d2<d else 0.
        R=0.
        if pos in objs:
            kk=objs[pos]; kc=kenyon(PAT[kk]); Wb=Wp-Wn
            Vb=alpha*(Wb@kc)+hambre_boca*hambre+.5; pb=1/(1+np.exp(-Vb/.3)); mordio=rng.random()<pb
            vis[kk][q(t)]+=1
            if mordio:
                R=R_VAL[val[kk]]; E=min(E+E_VAL[val[kk]],1.5); mord[kk][q(t)]+=1
                del objs[pos]; spawn()
                if learn:
                    dlt=R-Wb@kc
                    if lam: ix=kc>0; Wp[ix]*=(1-lam); Wn[ix]*=(1-lam)   # BUG-01: decaimiento local, solo celdas activas
                    if dlt>0: Wp=np.clip(Wp+eta*dlt*kc,0,3.)
                    else:     Wn=np.clip(Wn+eta*aversion*(-dlt)*kc,0,3.)
                    if plast:
                        P=PAT[kk]; idx=np.where(kc>0)[0]; err[idx]=(1-ema)*err[idx]+ema*abs(dlt); mu[idx]=(1-ema)*mu[idx]+ema*P
                        for c in idx:
                            if err[c]>theta and (~activa).any():
                                j=int(np.where(~activa)[0][0]); activa[j]=True; dist=P-mu[c]
                                KW[j]=np.clip(KW[c]+paso*dist,0,5); KW[c]=np.clip(KW[c]-paso*dist,0,5)
                                Wp[j]=Wp[c]; Wn[j]=Wn[c]; mu[j]=mu[c].copy(); err[c]=err[j]=0; splits+=1; split_t.append((t,kk))
        E-=costo
        if rng.random()<.003 and objs: del objs[list(objs)[int(rng.integers(len(objs)))]]; spawn()
        if learn: Wl=np.clip(Wl+eta*(1+2*hambre)*(max(R,0)+Rp)*el,0,1.5)
        if E<=0: deaths+=1; E=.6; pos=int(rng.integers(L))
        if log_cada and t%log_cada==0: log.append((t,)+tuple(round(float((Wp-Wn)@kenyon(PAT[k])),2) for k in 'ABCD'))
    W={k:round(float((Wp-Wn)@kenyon(PAT[k])),2) for k in PAT}
    comp={k:(round(float(Wp@kenyon(PAT[k])),2),round(float(Wn@kenyon(PAT[k])),2)) for k in PAT}
    return dict(split_t=split_t,mord=mord,vis=vis,W=W,comp=comp,deaths=deaths,log=log,splits=splits,celdas=int(activa.sum()),
                solap={'AB':len(code(PAT['A'])&code(PAT['B'])),'nB':len(code(PAT[nuevo])&code(PAT['B'])) if nuevo else None})
