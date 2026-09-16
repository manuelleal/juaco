"""organismo_caph9 = organismo_caph.py (38e259b0175d6375) + memoria de trabajo de rechazo (v9).
Generado por construye_reverificacion.py. NO editar. Con memoria_rechazo=0 es organismo_caph (KK1)."""
"""organismo_caph = organismo_cap.py (dc058e0a43216bf3) + lam (drenaje de la parte comun, linea literal
de organismo_v7e.py) + mordida del techo + mordidas de veneno/comida. Generado por construye_coste_techo.py.
NO editar a mano. Con lam=0 es organismo_cap (control 1 de corre_coste_techo.py).
Preregistro: PREREGISTRO_coste_techo.md (e0e2709f71dff15f)
"""
"""
organismo_cap.py — organismo para la Parte 2 (2K-bis redefinida: capacidad en numero de estimulos).

= organismo_v7.py (3db0475ef0ea95ce) con DOS generalizaciones y cero cambios de mecanismo:
  (a) `pats`: el diccionario de patrones deja de ser fijo (A,B,C,D) y se pasa por argumento.
  (b) `plan`: lista [(t_entrada, nombre, valencia), ...] en vez de (nuevo, nuevo_en, nuevo_val).
      Permite introducir N estimulos de uno en uno. El plan por defecto es [(0,'A','comida'),(0,'B','veneno')],
      identico a v6/v7.
  (c) `chk`: pasos en los que se fotografia el estado (W de cada estimulo, celdas, splits, visitas/mordidas
      del intervalo, solapamientos de codigo). Solo lectura: no toca el RNG ni el estado.

`plast=False` reproduce organismo_v6.py; `plast=True` reproduce organismo_v7.py.
El orden y la forma de TODAS las llamadas al RNG son las de v6/v7 (mismo stream por semilla).
Prueba de equivalencia: equivalencia_cap.py (6 semillas x 3 escenarios x 2 versiones, campos comunes).

NO se fuerza ningun solapamiento salvo el de v6/v7: codigo(primer estimulo) & codigo(segundo) == 0.
Todos los demas solapamientos salen del sorteo y se MIDEN.
"""
import numpy as np
L=40; NK=30; NKMAX=90; K=3
PAT={'A':np.array([1,1,0,1,0,0.]),'B':np.array([1,0,1,0,1,0.]),'C':np.array([0,1,1,0,0,1.]),'D':np.array([0,0,1,0,1,1.])}
R_VAL={'comida':1.0,'veneno':-3.0}; E_VAL={'comida':+0.8,'veneno':-0.4}
PLAN_DEF=[(0,'A','comida'),(0,'B','veneno')]

def run(seed,T=100000,learn=True,plan=None,pats=None,chk=None,
        eta=.03,tau_e=.85,alpha=1.2,hambre_boca=2.0,aversion=1.0,costo=.002,nobj=4,log_cada=None,
        plast=True,theta=0.6,ema=0.02,paso=0.5,lam=0.0,memoria_rechazo=20):
    pats=PAT if pats is None else pats
    plan=PLAN_DEF if plan is None else plan
    nombres=[p[1] for p in plan]; t_entra={p[1]:p[0] for p in plan}
    rng=np.random.default_rng(seed)
    Wl=rng.uniform(.1,.4,(2,9)); KW=np.zeros((NKMAX,6)); activa=np.zeros(NKMAX,bool); KW[:NK]=rng.uniform(0,1,(NK,6)); activa[:NK]=True
    def code(P):
        v=KW@P; v=np.where(activa,v,-1e9); return set(np.argsort(v)[-K:])
    n1,n2=nombres[0],nombres[1]
    cond=lambda: len(code(pats[n1])&code(pats[n2]))==0
    while not cond(): KW[0:NK]=rng.uniform(0,1,(NK,6))
    def kenyon(P): k=np.zeros(NKMAX); k[list(code(P))]=1; return k
    Wp=np.zeros(NKMAX); Wn=np.zeros(NKMAX); err=np.zeros(NKMAX); mu=np.zeros((NKMAX,6)); splits=0; el=np.zeros_like(Wl); tr=np.zeros(9)
    err_max=0.0
    pos=0; E=1.0; objs={}
    tipos=[]; val={}
    entradas={}
    for (te,nm,vl) in plan:
        if te<=0: tipos.append(nm); val[nm]=vl
        else: entradas.setdefault(te,[]).append((nm,vl))
    def spawn():
        while len(objs)<nobj:
            x=int(rng.integers(L))
            if x not in objs: objs[x]=tipos[int(rng.integers(len(tipos)))]
    spawn()
    q=lambda t:min(t//(T//4),3)
    split_t=[]; mord={k:[0]*4 for k in pats}; vis={k:[0]*4 for k in pats}; deaths=0; log=[]
    visc={k:0 for k in pats}; morc={k:0 for k in pats}; visp={k:0 for k in pats}; morp={k:0 for k in pats}
    hist=[]; t_agot=None; chk=set(chk or [])
    t_techo=None; techo_primero=None; n_techo=0; mv_tot=0; mc_tot=0   # <-- prueba de coste (techo)
    _rech={}   # v9: memoria de trabajo de rechazo
    def foto(t):
        vivos=[n for n in tipos]
        Wb=Wp-Wn; cods={n:code(pats[n]) for n in vivos}
        so=[len(cods[a]&cods[b]) for i,a in enumerate(vivos) for b in vivos[i+1:]]
        hist.append(dict(t=int(t),n=len(vivos),celdas=int(activa.sum()),splits=splits,
            W={n:round(float(Wb@kenyon(pats[n])),3) for n in vivos},
            R={n:R_VAL[val[n]] for n in vivos},
            vis_int={n:visc[n]-visp[n] for n in vivos},mord_int={n:morc[n]-morp[n] for n in vivos},
            vis_ac={n:visc[n] for n in vivos},mord_ac={n:morc[n] for n in vivos},
            solap_medio=round(float(np.mean(so)),3) if so else 0.0,solap_max=int(max(so)) if so else 0,
            err_max=round(err_max,4)))
        for n in vivos: visp[n]=visc[n]; morp[n]=morc[n]
    def see():
        best=None
        for x,k in objs.items():
            if memoria_rechazo and _rech.get(x,-1)>t: continue   # v9
            dl=(pos-x)%L; dr=(x-pos)%L; d=min(dl,dr)
            if best is None or d<best[0]: best=(d,k,dl<dr)
        if best is None:   # v9: todo filtrado -> regla original
            for x,k in objs.items():
                dl=(pos-x)%L; dr=(x-pos)%L; d=min(dl,dr)
                if best is None or d<best[0]: best=(d,k,dl<dr)
        return best
    for t in range(T):
        if t in chk: foto(t)
        if t in entradas:
            for (nm,vl) in entradas[t]: tipos.append(nm); val[nm]=vl
        hambre=np.clip(1-E,0,1); d,k,left=see(); pat=pats[k]
        x=np.concatenate([pat*1.2,[1.5 if left else 0,0 if left else 1.5,1.0 if d==0 else 0.]]); noise=.15+.5*hambre
        V=Wl@x; p=1/(1+np.exp(-(V-.8)/noise)); u=p+rng.normal(0,.3,2); m=np.zeros(2)
        if u.max()>.5: m[np.argmax(u)]=1
        tr=tr*.7+x
        if learn: el=el*tau_e+np.outer(m-p,tr)
        pos=(pos+int(m[1]-m[0]))%L; d2,_,_=see(); Rp=.2 if d2<d else 0.
        R=0.
        if pos in objs:
            kk=objs[pos]; kc=kenyon(pats[kk]); Wb=Wp-Wn
            Vb=alpha*(Wb@kc)+hambre_boca*hambre+.5; pb=1/(1+np.exp(-Vb/.3)); mordio=rng.random()<pb
            vis[kk][q(t)]+=1; visc[kk]+=1
            if memoria_rechazo and not mordio: _rech[pos]=t+memoria_rechazo   # v9
            if mordio:
                R=R_VAL[val[kk]]; E=min(E+E_VAL[val[kk]],1.5); mord[kk][q(t)]+=1; morc[kk]+=1
                if val[kk]=='veneno': mv_tot+=1
                else: mc_tot+=1
                del objs[pos]; spawn()
                _rech.pop(pos,None)   # v9
                if learn:
                    dlt=R-Wb@kc
                    if lam: ix=kc>0; mcom=np.minimum(Wp[ix],Wn[ix]); Wp[ix]-=lam*mcom; Wn[ix]-=lam*mcom   # BUG-01 exp2: decae solo la parte comun
                    _ix=kc>0
                    if dlt>0: _trunca=bool(((Wp[_ix]+eta*dlt)>3.0).any())
                    else:     _trunca=bool(((Wn[_ix]+eta*aversion*(-dlt))>3.0).any())
                    if _trunca:
                        n_techo+=1
                        if t_techo is None: t_techo=t; techo_primero=(kk,'Wp' if dlt>0 else 'Wn',t)
                    if dlt>0: Wp=np.clip(Wp+eta*dlt*kc,0,3.)
                    else:     Wn=np.clip(Wn+eta*aversion*(-dlt)*kc,0,3.)
                    P=pats[kk]; idx=np.where(kc>0)[0]; err[idx]=(1-ema)*err[idx]+ema*abs(dlt); mu[idx]=(1-ema)*mu[idx]+ema*P
                    _m=float(err[idx].max())
                    if _m>err_max: err_max=_m
                    if plast:
                        for c in idx:
                            if err[c]>theta and (~activa).any():
                                j=int(np.where(~activa)[0][0]); activa[j]=True; dist=P-mu[c]
                                KW[j]=np.clip(KW[c]+paso*dist,0,5); KW[c]=np.clip(KW[c]-paso*dist,0,5)
                                Wp[j]=Wp[c]; Wn[j]=Wn[c]; mu[j]=mu[c].copy(); err[c]=err[j]=0; splits+=1; split_t.append((t,kk))
                                if t_agot is None and activa.sum()>=NKMAX: t_agot=t
        E-=costo
        if rng.random()<.003 and objs:
            _dx=list(objs)[int(rng.integers(len(objs)))]; del objs[_dx]; spawn(); _rech.pop(_dx,None)   # v9
        if learn: Wl=np.clip(Wl+eta*(1+2*hambre)*(max(R,0)+Rp)*el,0,1.5)
        if E<=0: deaths+=1; E=.6; pos=int(rng.integers(L))
        if log_cada and t%log_cada==0: log.append((t,)+tuple(round(float((Wp-Wn)@kenyon(pats[k])),2) for k in sorted(pats)))
    foto(T)
    W={k:round(float((Wp-Wn)@kenyon(pats[k])),2) for k in pats}
    comp={k:(round(float(Wp@kenyon(pats[k])),2),round(float(Wn@kenyon(pats[k])),2)) for k in pats}
    nv=nombres[2] if len(nombres)>2 else None
    return dict(split_t=split_t,mord=mord,vis=vis,W=W,comp=comp,deaths=deaths,log=log,splits=splits,celdas=int(activa.sum()),
                solap={'AB':len(code(pats[n1])&code(pats[n2])),'nB':len(code(pats[nv])&code(pats[n2])) if nv else None},
                hist=hist,t_agot=t_agot,err_max=err_max,t_entra=t_entra,val=dict(val),t_techo=t_techo,techo_primero=techo_primero,n_techo=n_techo,mv_tot=mv_tot,mc_tot=mc_tot)
