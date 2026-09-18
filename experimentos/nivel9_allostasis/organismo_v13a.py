"""organismo_v13a = organismo/organismo_v13.py (cc8b16b492d4d324, TRONCO) + MODELO DE SI MISMO minimo:
un predictor lineal de la energia que rinde el bocado (dE_pred = Wpe@retina + Wke@kenyon, regla delta a tasa eta_pred)
y la SORPRESA |dE - dE_pred| como senal interna que modula la tasa de la via RAPIDA: eta_ef = eta*(1 + k_sorpresa*sorpresa).
El predictor NO entra en valor() ni en la decision de la boca y NO consume el RNG del organismo: por eso con
eta_pred>0 y k_sorpresa=0 la conducta es la de v13 bit a bit (SOLO MIDE). Con eta_pred=0 y k_sorpresa=0 es v13 EXACTO.
Control RUIDO (sorpresa_barajada=True): misma magnitud de modulacion, barajada en el tiempo con RNG propio.
Salidas nuevas: sorpresa_media/error_pred/eta_media/bocados por cuarto, sorpresa_pre/post y eta_pre/post en ventana
fina, t_ext_B, mord_post, deaths_post, W_pred.
Preregistro: experimentos/nivel9_allostasis/PREREGISTRO_allostasis.md. Generado por construye_allostasis.py. NO editar.
RAMA exploratoria del bloque 6: no es tronco ni candidato a tronco.
"""
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
        eta=.03,tau_e=.85,alpha=1.2,hambre_boca=2.0,aversion=1.0,costo=.002,nobj=4,log_cada=None,plast=True,theta=0.6,ema=0.02,paso=0.5,solap_AB=None,lam=0.05,memoria_rechazo=20,mu_norm=True,div_signo=True,eta_s=0.015,clip_s=3.0,puerta=3,eta_pred=0.0,k_sorpresa=0.0,clip_e=3.0,buf_sorpresa=20,sorpresa_barajada=False,vent_sorpresa=2000):
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
    Wpe=np.zeros(6); Wke=np.zeros(NKMAX)   # v13a: PREDICTOR de dE (modelo de si mismo). Inerte si eta_pred=0: no entra en valor() ni en la boca
    _sq=[0.]*4; _eq=[0.]*4; _npq=[0]*4; _nq=[0]*4; _etaq=[0.]*4   # v13a: por cuarto — |e|, e con signo, bocados con predictor, bocados, factor eta_ef/eta
    _vs=[0.,0.]; _ve=[0.,0.]; _vn=[0,0]   # v13a: ventana fina de vent_sorpresa pasos antes/despues de la inversion
    _buf=[]; _rng_s=np.random.default_rng(seed+900000) if sorpresa_barajada else None   # v13a: control RUIDO, RNG PROPIO (no toca el del organismo)
    t_ext_B=None; mord_post={'comida':0,'veneno':0}; deaths_post=0   # v13a: medidas tras la inversion (M1, M2)
    def valor(P):   # v13: el valor que usa la boca. Sin puerta: rapida+lenta (un error). Con puerta: la rapida si el patron le es FAMILIAR, si no la lenta
        _k=kenyon(P); _f=float((Wp-Wn)@_k); _s=float((Wps-Wns)@P)
        return _f+_s if puerta is None else (_f if int((np.abs((Wp-Wn)[_k>0])>0.2).sum())>=puerta else _s)   # familiar = >= puerta celdas del codigo con valor consolidado (|W|>0.2, el mismo umbral de v11)
    pos=0; E=1.0; objs={}; val={'A':'comida','B':'veneno'}
    err_max=0.0; t_conflicto=None; t_techo=None; n_techo=0   # instrumentacion v8, solo lectura
    _rech={}; _prev_on=-1   # v9: memoria de trabajo de rechazo (posicion -> paso hasta el que no es objetivo)
    sobre={'veneno':[0]*4,'comida':[0]*4}; llegadas={'veneno':[0]*4,'comida':[0]*4}; sin_objetivo=[0]*4   # v9: lectura
    tipos=['A','B']
    def spawn():
        while len(objs)<nobj:
            x=int(rng.integers(L))
            if x not in objs: objs[x]=tipos[int(rng.integers(len(tipos)))]
    spawn()
    q=lambda t:min(t//(T//4),3)
    split_t=[]; mord={k:[0]*4 for k in PAT}; vis={k:[0]*4 for k in PAT}; deaths=0; log=[]
    def see(contar=False):
        best=None
        for x,k in objs.items():
            if memoria_rechazo and _rech.get(x,-1)>t: continue   # v9: rechazado hace poco, no es objetivo
            dl=(pos-x)%L; dr=(x-pos)%L; d=min(dl,dr)
            if best is None or d<best[0]: best=(d,k,dl<dr)
        if best is None:   # v9: todo filtrado -> regla original (fallback)
            if contar: sin_objetivo[q(t)]+=1
            for x,k in objs.items():
                dl=(pos-x)%L; dr=(x-pos)%L; d=min(dl,dr)
                if best is None or d<best[0]: best=(d,k,dl<dr)
        return best
    for t in range(T):
        if invertir_en is not None and t==invertir_en: val={'A':'veneno','B':'comida'}
        if nuevo is not None and t==nuevo_en: tipos.append(nuevo); val[nuevo]=nuevo_val
        hambre=np.clip(1-E,0,1); d,k,left=see(contar=True); pat=PAT[k]
        x=np.concatenate([pat*1.2,[1.5 if left else 0,0 if left else 1.5,1.0 if d==0 else 0.]]); noise=.15+.5*hambre
        V=Wl@x; p=1/(1+np.exp(-(V-.8)/noise)); u=p+rng.normal(0,.3,2); m=np.zeros(2)
        if u.max()>.5: m[np.argmax(u)]=1
        tr=tr*.7+x
        if learn: el=el*tau_e+np.outer(m-p,tr)
        pos=(pos+int(m[1]-m[0]))%L; d2,_,_=see(); Rp=.2 if d2<d else 0.
        R=0.
        if pos in objs:
            kk=objs[pos]; kc=kenyon(PAT[kk]); Wb=Wp-Wn; _wf=float(Wb@kc); _ws=float((Wps-Wns)@PAT[kk])   # v13: las dos vias
            _wt=_wf+_ws if puerta is None else (_wf if int((np.abs(Wb[kc>0])>0.2).sum())>=puerta else _ws)   # v13: valor total (sin puerta: suma; con puerta: la rapida si le es familiar)
            Vb=alpha*_wt+hambre_boca*hambre+.5; pb=1/(1+np.exp(-Vb/.3)); mordio=rng.random()<pb
            vis[kk][q(t)]+=1
            sobre[val[kk]][q(t)]+=1; llegadas[val[kk]][q(t)]+=int(_prev_on!=pos)
            if memoria_rechazo and not mordio: _rech[pos]=t+memoria_rechazo   # v9: la boca rechazo -> no es objetivo por un tiempo
            if mordio:
                R=R_VAL[val[kk]]; E=min(E+E_VAL[val[kk]],1.5); mord[kk][q(t)]+=1
                if invertir_en is not None and t>=invertir_en: mord_post[val[kk]]+=1   # v13a: M2, bocados tras la inversion
                del objs[pos]; spawn()
                _rech.pop(pos,None)   # v9: ese objeto ya no existe
                if learn:
                    _sr=0.; _sr0=0.   # v13a: sorpresa emitida (la que modula) y sorpresa real (la que se mide)
                    if eta_pred:   # v13a: predice la energia que rinde el bocado y aprende de SU error (regla delta, tasa propia)
                        _dEp=float(Wpe@PAT[kk])+float(Wke@kc); _ee=E_VAL[val[kk]]-_dEp; _sr0=abs(_ee); _sr=_sr0
                        Wpe=np.clip(Wpe+eta_pred*_ee*PAT[kk],-clip_e,clip_e); Wke=np.clip(Wke+eta_pred*_ee*kc,-clip_e,clip_e)
                        _sq[q(t)]+=_sr0; _eq[q(t)]+=_ee; _npq[q(t)]+=1
                        if _rng_s is not None:   # RUIDO: misma magnitud, barajada en el tiempo (ventana de buf_sorpresa bocados)
                            _buf.append(_sr)
                            if len(_buf)>buf_sorpresa: _sr=float(_buf.pop(int(_rng_s.integers(len(_buf)))))
                    _eta=eta*(1.+k_sorpresa*_sr) if k_sorpresa else eta   # v13a: eta_ef = eta*(1+k_sorpresa*sorpresa); con k_sorpresa=0 es eta EXACTO
                    _nq[q(t)]+=1; _etaq[q(t)]+=_eta/eta
                    if vent_sorpresa and invertir_en is not None and invertir_en-vent_sorpresa<=t<invertir_en+vent_sorpresa:
                        _w=0 if t<invertir_en else 1; _vs[_w]+=_sr0; _ve[_w]+=_eta/eta; _vn[_w]+=1   # v13a: guarda G-b (misma eta media) y P3
                    dlt=R-_wt if puerta is None else R-_wf   # v13: sin puerta UN error compartido; con puerta cada via el suyo
                    if eta_s:   # v13: actualizacion de la via lenta (su tasa, mismo drenaje)
                        _ds=dlt if puerta is None else R-_ws
                        if lam: _mcs=np.minimum(Wps,Wns)*(PAT[kk]>0); Wps=Wps-lam*_mcs; Wns=Wns-lam*_mcs
                        if _ds>0: Wps=np.clip(Wps+eta_s*_ds*PAT[kk],0,clip_s)
                        else:     Wns=np.clip(Wns+eta_s*aversion*(-_ds)*PAT[kk],0,clip_s)
                    if lam: ix=kc>0; mcom=np.minimum(Wp[ix],Wn[ix]); Wp[ix]-=lam*mcom; Wn[ix]-=lam*mcom   # BUG-01 exp2: decae solo la parte comun
                    _ix=kc>0
                    if dlt>0: _trunca=bool(((Wp[_ix]+_eta*dlt)>3.0).any())
                    else:     _trunca=bool(((Wn[_ix]+_eta*aversion*(-dlt))>3.0).any())
                    if _trunca:
                        n_techo+=1
                        if t_techo is None: t_techo=t
                    if dlt>0: Wp=np.clip(Wp+_eta*dlt*kc,0,3.)
                    else:     Wn=np.clip(Wn+_eta*aversion*(-dlt)*kc,0,3.)
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
        if invertir_en is not None and t>=invertir_en and t_ext_B is None and valor(PAT['B'])>=0: t_ext_B=t   # v13a: M1, mismo criterio que mundo_social.py (lineas 156-157). No consume RNG
        _prev_on=pos if pos in objs else -1   # v9: para contar llegadas
        E-=costo
        if rng.random()<.003 and objs:
            _dx=list(objs)[int(rng.integers(len(objs)))]; del objs[_dx]; spawn(); _rech.pop(_dx,None)   # v9: olvido
        if learn: Wl=np.clip(Wl+eta*(1+2*hambre)*(max(R,0)+Rp)*el,0,1.5)
        if E<=0:
            deaths+=1; E=.6; pos=int(rng.integers(L))
            if invertir_en is not None and t>=invertir_en: deaths_post+=1   # v13a
        if log_cada and t%log_cada==0: log.append((t,)+tuple(round(valor(PAT[k]),2) for k in 'ABCD'))
    W={k:round(valor(PAT[k]),2) for k in PAT}   # v13: valor total
    W_lenta={k:round(float((Wps-Wns)@PAT[k]),3) for k in PAT}   # v13: lectura de la via lenta sola
    comp={k:(round(float(Wp@kenyon(PAT[k])),2),round(float(Wn@kenyon(PAT[k])),2)) for k in PAT}
    return dict(sobre=sobre,llegadas=llegadas,sin_objetivo=sin_objetivo,memoria_rechazo=memoria_rechazo,err_max=err_max,t_conflicto=t_conflicto,t_techo=t_techo,n_techo=n_techo,split_t=split_t,mord=mord,vis=vis,W=W,comp=comp,deaths=deaths,log=log,splits=splits,celdas=int(activa.sum()),
                solap={'AB':len(code(PAT['A'])&code(PAT['B'])),'nB':len(code(PAT[nuevo])&code(PAT['B'])) if nuevo else None},W_lenta=W_lenta,Wps=[round(float(x),3) for x in Wps],Wns=[round(float(x),3) for x in Wns],
                sorpresa_media=[round(_sq[i]/_npq[i],4) if (eta_pred and _npq[i]) else None for i in range(4)],
                error_pred=[round(_eq[i]/_npq[i],4) if (eta_pred and _npq[i]) else None for i in range(4)],
                eta_media=[round(_etaq[i]/_nq[i],4) if _nq[i] else None for i in range(4)],bocados=list(_nq),
                sorpresa_pre=(round(_vs[0]/_vn[0],4) if (eta_pred and _vn[0]) else None),sorpresa_post=(round(_vs[1]/_vn[1],4) if (eta_pred and _vn[1]) else None),
                eta_pre=(round(_ve[0]/_vn[0],4) if _vn[0] else None),eta_post=(round(_ve[1]/_vn[1],4) if _vn[1] else None),n_pre=_vn[0],n_post=_vn[1],
                t_ext_B=t_ext_B,mord_post=mord_post,deaths_post=deaths_post,
                W_pred=({k:round(float(Wpe@PAT[k])+float(Wke@kenyon(PAT[k])),3) for k in PAT} if eta_pred else None),Wpe=[round(float(x),3) for x in Wpe])
