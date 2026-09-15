"""
organismo_v7i.py = organismo_v7.py (hash 3db0475ef0ea95ce) + INSTRUMENTACION INERTE del error de prediccion.

Que se anade (y por que es inerte):
  (1) err_max / err_max_k : maximo historico de la media movil |error de prediccion| por celda (`err`),
      global y por estimulo. Solo lectura de una variable que ya existia. No toca el RNG.
  (2) La actualizacion de err/mu se saca de dentro del `if plast:` y pasa a ejecutarse SIEMPRE.
      Con plast=True el orden de operaciones es identico (err/mu se actualizaban y despues venia el bucle de split).
      Con plast=False err/mu se calculan pero NO se usan en ningun sitio: no hay splits, no hay lectura de mu,
      y no hay ninguna llamada nueva al RNG. Sirve para medir la trayectoria del error SIN que los splits la trunquen.
  (3) err_split : lista de (t, estimulo, celda, valor de err que disparo la division).
  (4) solap_ini / solap_fin : solapamientos de codigo de TODOS los pares de PAT, antes de entrenar y al final.
      Se calculan fuera del bucle. Inertes.
  (5) devolver_estado=False : si True anade KW/Wp/Wn/activa al dict de salida. No cambia el computo.

Ningun otro cambio. Prueba de equivalencia: equivalencia_v7i.py (6 semillas x 3 escenarios, todos los campos comunes).

--- cabecera original de organismo_v7.py ---
Organismo v7 = v6 + 2L (plasticidad estructural en Kenyon: celda con error de prediccion cronico se divide hacia lo distintivo).
Parametro plast=True/False; solap_AB fuerza solapamiento inicial A&B (None = 0 como en v6).
"""
import numpy as np
L=40; NK=30; NKMAX=90; K=3
PAT={'A':np.array([1,1,0,1,0,0.]),'B':np.array([1,0,1,0,1,0.]),'C':np.array([0,1,1,0,0,1.]),'D':np.array([0,0,1,0,1,1.])}
R_VAL={'comida':1.0,'veneno':-3.0}; E_VAL={'comida':+0.8,'veneno':-0.4}

def run(seed,T=100000,learn=True,invertir_en=None,nuevo=None,nuevo_en=50000,nuevo_val='veneno',solap_B=None,
        eta=.03,tau_e=.85,alpha=1.2,hambre_boca=2.0,aversion=1.0,costo=.002,nobj=4,log_cada=None,plast=True,theta=0.6,ema=0.02,paso=0.5,solap_AB=None,
        devolver_estado=False):
    rng=np.random.default_rng(seed)
    Wl=rng.uniform(.1,.4,(2,9)); KW=np.zeros((NKMAX,6)); activa=np.zeros(NKMAX,bool); KW[:NK]=rng.uniform(0,1,(NK,6)); activa[:NK]=True
    def code(P):
        v=KW@P; v=np.where(activa,v,-1e9); return set(np.argsort(v)[-K:])
    objetivo_AB=0 if solap_AB is None else solap_AB
    if solap_AB: KW[:solap_AB]=0; KW[:solap_AB,0]=5.0
    cond=lambda: len(code(PAT['A'])&code(PAT['B']))==objetivo_AB and (nuevo is None or solap_B is None or (len(code(PAT[nuevo])&code(PAT['B']))==solap_B and len(code(PAT[nuevo])&code(PAT['A']))==0))
    while not cond(): KW[objetivo_AB:NK]=rng.uniform(0,1,(NK-objetivo_AB,6))
    def kenyon(P): k=np.zeros(NKMAX); k[list(code(P))]=1; return k
    # (4) INSTRUMENTACION: solapamientos iniciales de todos los pares. Inerte.
    _ks=sorted(PAT); solap_ini={a+b:len(code(PAT[a])&code(PAT[b])) for i,a in enumerate(_ks) for b in _ks[i+1:]}
    Wp=np.zeros(NKMAX); Wn=np.zeros(NKMAX); err=np.zeros(NKMAX); mu=np.zeros((NKMAX,6)); splits=0; el=np.zeros_like(Wl); tr=np.zeros(9)
    err_max=0.0; err_max_k={k:0.0 for k in PAT}; err_split=[]   # (1)(3) INSTRUMENTACION
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
                    if dlt>0: Wp=np.clip(Wp+eta*dlt*kc,0,3.)
                    else:     Wn=np.clip(Wn+eta*aversion*(-dlt)*kc,0,3.)
                    # (2) err/mu SIEMPRE (con plast=False quedan sin usar). Orden identico al original con plast=True.
                    P=PAT[kk]; idx=np.where(kc>0)[0]; err[idx]=(1-ema)*err[idx]+ema*abs(dlt); mu[idx]=(1-ema)*mu[idx]+ema*P
                    _m=float(err[idx].max())                                  # (1)
                    if _m>err_max: err_max=_m                                 # (1)
                    if _m>err_max_k[kk]: err_max_k[kk]=_m                     # (1)
                    if plast:
                        for c in idx:
                            if err[c]>theta and (~activa).any():
                                err_split.append((t,kk,int(c),float(err[c]))) # (3)
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
    solap_fin={a+b:len(code(PAT[a])&code(PAT[b])) for i,a in enumerate(_ks) for b in _ks[i+1:]}   # (4)
    out=dict(split_t=split_t,mord=mord,vis=vis,W=W,comp=comp,deaths=deaths,log=log,splits=splits,celdas=int(activa.sum()),
                solap={'AB':len(code(PAT['A'])&code(PAT['B'])),'nB':len(code(PAT[nuevo])&code(PAT['B'])) if nuevo else None})
    out.update(err_max=err_max,err_max_k=err_max_k,err_split=err_split,solap_ini=solap_ini,solap_fin=solap_fin)  # (1)(3)(4)
    if devolver_estado: out.update(KW=KW.copy(),Wp=Wp.copy(),Wn=Wn.copy(),activa=activa.copy())                  # (5)
    return out
