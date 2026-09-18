"""mundo_mapa = organismo_v13.py (cc8b16b492d4d324) + vision limitada r_vis + sitios fijos con regeneracion + tabla M
(posicion -> ultimo patron visto) con simulacion hacia adelante + prueba de teletransporte. Generado por construye_mapa.py.
NO editar. Con r_vis=None, sitios=None, usa_M=False, prueba=None es organismo_v13 exacto (identidad obligatoria)."""
"""
Organismo v13 — CANDIDATO A TRONCO (congelable solo si pasa PREREGISTRO_tronco_v13.md): v11 + VIA LENTA lineal
sobre la retina + PUERTA de familiaridad. Punto confirmado en semillas 61-80: eta_s=0.015, puerta=3
(datos v13_dos_vias_20260917_160541: retencion 20/20, acierto en patrones nunca vistos 0.850, E1/E2/E2L 20/20).

Dos vias con UN solo error (esquema CLS minimo): la rapida es v11 sin tocar (Kenyon + division por conflicto de
signo); la lenta es una lectura lineal directa de los 6 pixeles con dos canales Wps/Wns (>=0, tope clip_s) a tasa
eta_s < eta, con el mismo drenaje de la parte comun. Cada via aprende de SU error. La boca consulta la rapida solo
si el patron le es FAMILIAR (>= puerta de las 3 celdas de su codigo con |Wp-Wn|>0.2, el umbral de v11); si no,
consulta la lenta, que aprende la regla y no los casos. Con eta_s=0 y puerta=None es v11 EXACTO.
Linaje: ... -> v9 (d3b72fb8819fbe8e) -> v10 (219d5033fe15b5b9, instrumento) -> v11 (f69e24063be1b194) -> v13.
Generado por experimentos/v13_dos_vias/construye_v13_tronco.py (a partir del genoma explorado). NO editar a mano.
"""
import numpy as np
L=40; NK=30; NKMAX=90; K=3
PAT={'A':np.array([1,1,0,1,0,0.]),'B':np.array([1,0,1,0,1,0.]),'C':np.array([0,1,1,0,0,1.]),'D':np.array([0,0,1,0,1,1.])}
R_VAL={'comida':1.0,'veneno':-3.0}; E_VAL={'comida':+0.8,'veneno':-0.4}

def run(seed,T=100000,learn=True,invertir_en=None,nuevo=None,nuevo_en=50000,nuevo_val='veneno',solap_B=None,
        eta=.03,tau_e=.85,alpha=1.2,hambre_boca=2.0,aversion=1.0,costo=.002,nobj=4,log_cada=None,plast=True,theta=0.6,ema=0.02,paso=0.5,solap_AB=None,lam=0.05,memoria_rechazo=20,mu_norm=True,div_signo=True,eta_s=0.015,clip_s=3.0,puerta=3,
        r_vis=None,sitios=None,regen=50,usa_M=False,escribe_M=True,gamma_M=0.6,H_M=20,disc_M=0.9,prueba=None):   # mapa
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
    Wps=np.zeros(6); Wns=np.zeros(6)   # v13: via LENTA, lineal sobre la retina (inerte si eta_s=0)
    _Mpat=np.zeros((L,6)); _Mset=np.zeros(L,bool); _VACIO=np.zeros(6)   # mapa: tabla posicion -> ultimo patron visto
    def valor(P):   # v13: el valor que usa la boca. Sin puerta: rapida+lenta (un error). Con puerta: la rapida si el patron le es FAMILIAR, si no la lenta
        _k=kenyon(P); _f=float((Wp-Wn)@_k); _s=float((Wps-Wns)@P)
        return _f+_s if puerta is None else (_f if int((np.abs((Wp-Wn)[_k>0])>0.2).sum())>=puerta else _s)   # familiar = >= puerta celdas del codigo con valor consolidado (|W|>0.2, el mismo umbral de v11)
    pos=0; E=1.0; objs={}; val={'A':'comida','B':'veneno'}
    err_max=0.0; t_conflicto=None; t_techo=None; n_techo=0   # instrumentacion v8, solo lectura
    _rech={}; _prev_on=-1   # v9: memoria de trabajo de rechazo (posicion -> paso hasta el que no es objetivo)
    sobre={'veneno':[0]*4,'comida':[0]*4}; llegadas={'veneno':[0]*4,'comida':[0]*4}; sin_objetivo=[0]*4   # v9: lectura
    tipos=['A','B']
    _SIT={}; _pend={}   # mapa: sitio -> tipo fijo; sitio -> paso en que reaparece
    if sitios is not None:
        _F0=int(rng.integers(L)); _SIT={(_F0+i*(L//len(sitios)))%L:kk for i,kk in enumerate(sitios)}
    def spawn():
        if sitios is not None:   # mapa: los objetos viven en sitios fijos
            for x,kk in _SIT.items():
                if x not in objs and x not in _pend: objs[x]=kk
            return
        while len(objs)<nobj:
            x=int(rng.integers(L))
            if x not in objs: objs[x]=tipos[int(rng.integers(len(tipos)))]
    spawn()
    def _sesgo_M():   # mapa: con la retina vacia, valor recordado por direccion, descontado por distancia
        _bi=sum(disc_M**h*valor(_Mpat[(pos-h)%L]) for h in range(1,H_M+1) if _Mset[(pos-h)%L])
        _bd=sum(disc_M**h*valor(_Mpat[(pos+h)%L]) for h in range(1,H_M+1) if _Mset[(pos+h)%L])
        return gamma_M*np.array([_bi,_bd])
    q=lambda t:min(t//(T//4),3)
    split_t=[]; mord={k:[0]*4 for k in PAT}; vis={k:[0]*4 for k in PAT}; deaths=0; log=[]
    def see(contar=False):
        best=None
        for x,k in objs.items():
            if memoria_rechazo and _rech.get(x,-1)>t: continue   # v9: rechazado hace poco, no es objetivo
            if r_vis is not None and min((pos-x)%L,(x-pos)%L)>r_vis: continue   # mapa: fuera de la vista
            dl=(pos-x)%L; dr=(x-pos)%L; d=min(dl,dr)
            if best is None or d<best[0]: best=(d,k,dl<dr)
        if best is None:   # v9: todo filtrado -> regla original (fallback)
            if contar: sin_objetivo[q(t)]+=1
            for x,k in objs.items():
                if r_vis is not None and min((pos-x)%L,(x-pos)%L)>r_vis: continue   # mapa: fuera de la vista
                dl=(pos-x)%L; dr=(x-pos)%L; d=min(dl,dr)
                if best is None or d<best[0]: best=(d,k,dl<dr)
        return best if best is not None else (None,'vacio',None)   # mapa: nada a la vista
    for t in range(T):
        if _pend:   # mapa: reaparecen en su sitio los objetos maduros
            _mad=[x for x,tt in _pend.items() if tt<=t]
            if _mad:
                for x in _mad: del _pend[x]
                spawn()
        if invertir_en is not None and t==invertir_en: val={'A':'veneno','B':'comida'}
        if nuevo is not None and t==nuevo_en: tipos.append(nuevo); val[nuevo]=nuevo_val
        hambre=np.clip(1-E,0,1); d,k,left=see(contar=True); pat=PAT[k] if k!='vacio' else _VACIO
        x=np.concatenate([pat*1.2,[1.5 if left else 0,1.5 if left is False else 0,1.0 if d==0 else 0.]]); noise=.15+.5*hambre
        V=Wl@x; p=1/(1+np.exp(-(V-.8)/noise)); u=p+rng.normal(0,.3,2); m=np.zeros(2)
        if usa_M and k=='vacio': u=u+_sesgo_M()   # mapa: solo desempata sin senal directa
        if u.max()>.5: m[np.argmax(u)]=1
        tr=tr*.7+x
        if learn: el=el*tau_e+np.outer(m-p,tr)
        pos=(pos+int(m[1]-m[0]))%L; d2,_,_=see(); Rp=.2 if (d is not None and d2 is not None and d2<d) else 0.
        R=0.
        if pos in objs:
            if usa_M and escribe_M: _Mpat[pos]=PAT[objs[pos]]; _Mset[pos]=True   # mapa: recuerda lo que vio aqui
            kk=objs[pos]; kc=kenyon(PAT[kk]); Wb=Wp-Wn; _wf=float(Wb@kc); _ws=float((Wps-Wns)@PAT[kk])   # v13: las dos vias
            _wt=_wf+_ws if puerta is None else (_wf if int((np.abs(Wb[kc>0])>0.2).sum())>=puerta else _ws)   # v13: valor total (sin puerta: suma; con puerta: la rapida si le es familiar)
            Vb=alpha*_wt+hambre_boca*hambre+.5; pb=1/(1+np.exp(-Vb/.3)); mordio=rng.random()<pb
            vis[kk][q(t)]+=1
            sobre[val[kk]][q(t)]+=1; llegadas[val[kk]][q(t)]+=int(_prev_on!=pos)
            if memoria_rechazo and not mordio: _rech[pos]=t+memoria_rechazo   # v9: la boca rechazo -> no es objetivo por un tiempo
            if mordio:
                R=R_VAL[val[kk]]; E=min(E+E_VAL[val[kk]],1.5); mord[kk][q(t)]+=1
                if sitios is not None: _pend[pos]=t+regen   # mapa: reaparece en su sitio
                del objs[pos]; spawn()
                _rech.pop(pos,None)   # v9: ese objeto ya no existe
                if learn:
                    dlt=R-_wt if puerta is None else R-_wf   # v13: sin puerta UN error compartido; con puerta cada via el suyo
                    if eta_s:   # v13: actualizacion de la via lenta (su tasa, mismo drenaje)
                        _ds=dlt if puerta is None else R-_ws
                        if lam: _mcs=np.minimum(Wps,Wns)*(PAT[kk]>0); Wps=Wps-lam*_mcs; Wns=Wns-lam*_mcs
                        if _ds>0: Wps=np.clip(Wps+eta_s*_ds*PAT[kk],0,clip_s)
                        else:     Wns=np.clip(Wns+eta_s*aversion*(-_ds)*PAT[kk],0,clip_s)
                    if lam: ix=kc>0; mcom=np.minimum(Wp[ix],Wn[ix]); Wp[ix]-=lam*mcom; Wn[ix]-=lam*mcom   # BUG-01 exp2: decae solo la parte comun
                    _ix=kc>0
                    if dlt>0: _trunca=bool(((Wp[_ix]+eta*dlt)>3.0).any())
                    else:     _trunca=bool(((Wn[_ix]+eta*aversion*(-dlt))>3.0).any())
                    if _trunca:
                        n_techo+=1
                        if t_techo is None: t_techo=t
                    if dlt>0: Wp=np.clip(Wp+eta*dlt*kc,0,3.)
                    else:     Wn=np.clip(Wn+eta*aversion*(-dlt)*kc,0,3.)
                    if t_conflicto is None and bool((np.minimum(Wp[_ix],Wn[_ix])>0).any()): t_conflicto=t
                    if plast:
                        P=PAT[kk]; idx=np.where(kc>0)[0]; err[idx]=(1-ema)*err[idx]+ema*abs(dlt); mu[idx]=(1-ema)*mu[idx]+ema*P
                        err_max=max(err_max,float(err[idx].max()))
                        for c in idx:
                            if div_signo:   # v11 (JUACO-EVO gen1/llm_2): divide por CONFLICTO DE SIGNO, hija ciega fuera de P, madre fija, fision del valor
                                dist=P-(mu[c]*(P.sum()/max(float(mu[c].sum()),1e-9)) if mu_norm else mu[c])
                                kj=np.clip(KW[c]*(1-0.05)+paso*dist,0,5)*(P>0)
                                if Wb[c]*R<0 and abs(float(Wb[c]))>0.2 and float(kj@P)>float(KW[c]@P) and (~activa).any():
                                    j=int(np.where(~activa)[0][0]); activa[j]=True; KW[j]=kj
                                    if R>0: Wp[j]=Wp[c]; Wn[j]=0.; Wp[c]=0.
                                    else:   Wn[j]=Wn[c]; Wp[j]=0.; Wn[c]=0.
                                    mu[j]=P*(float(mu[c].sum())/P.sum()); err[c]=err[j]=0; splits+=1; split_t.append((t,kk))
                            elif err[c]>theta and (~activa).any():
                                j=int(np.where(~activa)[0][0]); activa[j]=True; dist=P-(mu[c]*(P.sum()/max(float(mu[c].sum()),1e-9)) if mu_norm else mu[c])   # v10: mu normalizada a la masa del patron
                                KW[j]=np.clip(KW[c]+paso*dist,0,5); KW[c]=np.clip(KW[c]-paso*dist,0,5)
                                Wp[j]=Wp[c]; Wn[j]=Wn[c]; mu[j]=mu[c].copy(); err[c]=err[j]=0; splits+=1; split_t.append((t,kk))
        _prev_on=pos if pos in objs else -1   # v9: para contar llegadas
        E-=costo
        if rng.random()<.003 and objs:
            _dx=list(objs)[int(rng.integers(len(objs)))]
            if sitios is not None: _pend[_dx]=t+regen   # mapa
            del objs[_dx]; spawn(); _rech.pop(_dx,None)   # v9: olvido
        if learn: Wl=np.clip(Wl+eta*(1+2*hambre)*(max(R,0)+Rp)*el,0,1.5)
        if E<=0: deaths+=1; E=.6; pos=int(rng.integers(L))
        if log_cada and t%log_cada==0: log.append((t,)+tuple(round(valor(PAT[k]),2) for k in 'ABCD'))
    _tel=None
    if prueba is not None:   # mapa: prueba de teletransporte, sin aprendizaje
        _Fs=[x for x,kk in _SIT.items() if val[kk]=='comida']; _F=_Fs[0] if _Fs else int(rng.integers(L))
        if prueba.get('barajar'):
            _pi=rng.permutation(NKMAX); Wp=Wp[_pi]; Wn=Wn[_pi]; _pj=rng.permutation(6); Wps=Wps[_pj]; Wns=Wns[_pj]
        if prueba.get('invertir'): Wp,Wn=Wn,Wp; Wps,Wns=Wns,Wps   # control decisivo: el valor con el signo cambiado (la puerta no cambia)
        _ac=[]; _nn=0; _ciego=0; _pasos=[]
        for i in range(prueba.get('n_tel',40)):
            _dn=int(rng.integers(r_vis+1,13)); _lado=-1 if i%2==0 else 1   # la comida queda a _dn casillas hacia _lado
            pos=(_F-_lado*_dn)%L; E=prueba.get('E_test',0.3); tr=np.zeros(9); _rech.clear()
            for x in list(_pend): del _pend[x]
            spawn(); _dir=0
            for _s in range(prueba.get('max_pasos',30)):
                hambre=np.clip(1-E,0,1); d,k,left=see(); pat=PAT[k] if k!='vacio' else _VACIO
                if _s==0 and k=='vacio': _ciego+=1
                x=np.concatenate([pat*1.2,[1.5 if left else 0,1.5 if left is False else 0,1.0 if d==0 else 0.]]); noise=.15+.5*hambre
                V=Wl@x; p=1/(1+np.exp(-(V-.8)/noise)); u=p+rng.normal(0,.3,2); m=np.zeros(2)
                if usa_M and k=='vacio': u=u+_sesgo_M()
                if u.max()>.5: m[np.argmax(u)]=1
                if m.any(): _dir=int(m[1]-m[0]); break
            _pasos.append(_s+1)
            if _dir==0: _nn+=1
            else: _ac.append(int(_dir==_lado))
        _tel=dict(acierto=(round(sum(_ac)/len(_ac),3) if _ac else None),n=len(_ac),sin_mover=_nn,ciego_al_llegar=_ciego,
                  pasos_medio=round(sum(_pasos)/len(_pasos),2),F=_F,sitios={int(x):kk for x,kk in _SIT.items()})
    W={k:round(valor(PAT[k]),2) for k in PAT}   # v13: valor total
    W_lenta={k:round(float((Wps-Wns)@PAT[k]),3) for k in PAT}   # v13: lectura de la via lenta sola
    comp={k:(round(float(Wp@kenyon(PAT[k])),2),round(float(Wn@kenyon(PAT[k])),2)) for k in PAT}
    return dict(sobre=sobre,llegadas=llegadas,sin_objetivo=sin_objetivo,memoria_rechazo=memoria_rechazo,err_max=err_max,t_conflicto=t_conflicto,t_techo=t_techo,n_techo=n_techo,split_t=split_t,mord=mord,vis=vis,W=W,comp=comp,deaths=deaths,log=log,splits=splits,celdas=int(activa.sum()),
                solap={'AB':len(code(PAT['A'])&code(PAT['B'])),'nB':len(code(PAT[nuevo])&code(PAT['B'])) if nuevo else None},W_lenta=W_lenta,Wps=[round(float(x),3) for x in Wps],Wns=[round(float(x),3) for x in Wns],
                tel=_tel,M_llenas=int(_Mset.sum()))   # mapa
