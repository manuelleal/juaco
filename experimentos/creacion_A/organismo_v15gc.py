"""organismo_v15gc = organismo/organismo_v14g.py (1f1318480cd34cde, solo se leyo) + perilla `memoria_pares`.
Con memoria_pares=None es organismo_v14g EXACTO. Generado por construye_v15c.py. NO editar."""
"""organismo_v14g = mundo de regla de v14 (copia de experimentos/nivel10_composicion_v14/organismo_v14gc.py dcca1ab79d86289b).
Perillas apagadas por defecto (== organismo_v13g); bateria_generaliza.py las enciende para organismo_v14.
"""
"""organismo_v14gc = experimentos/v13_dos_vias/organismo_v13g.py (2a80e125f8593bf2) + COMPOSICION
(mask_rel + puerta_pat, ver organismo_v14c.py). Es el instrumento del MUNDO DE REGLA que usa
bateria_generaliza_v14c.py. Generado por construye_v14c.py. NO editar.
Con mask_rel=0 y puerta_pat=0 es organismo_v13g EXACTO."""
"""organismo_v13g = organismo_v13.py + mundo de regla, sonda a priori (valor TOTAL), primer encuentro y sonda final
(mismas anclas que v9g/v11g/v12g). Generado por construye_v13.py. NO editar. Con eta_s=0 es organismo_v11g exacto.
"""
"""
Organismo v13 — CANDIDATO (no es tronco): v11 + VIA LENTA lineal sobre la retina. Preregistro PREREGISTRO_v13.md.

Dos vias con UN solo error (esquema CLS minimo): la rapida es v11 sin tocar (Kenyon + division por conflicto de
signo); la lenta es una lectura lineal directa de los 6 pixeles con dos canales Wps/Wns (>=0, tope clip_s) a tasa
eta_s < eta, con el mismo drenaje de la parte comun. valor(P) = (Wp-Wn)@kenyon(P) + (Wps-Wns)@P; la boca decide
con ese valor y dlt = R - valor entrena a las dos. Con eta_s=0 es v11 EXACTO.
Generado por experimentos/v13_dos_vias/construye_v13.py. NO editar a mano.
"""
import numpy as np
L=40; NK=30; NKMAX=90; K=3
PAT={'A':np.array([1,1,0,1,0,0.]),'B':np.array([1,0,1,0,1,0.]),'C':np.array([0,1,1,0,0,1.]),'D':np.array([0,0,1,0,1,1.])}
R_VAL={'comida':1.0,'veneno':-3.0}; E_VAL={'comida':+0.8,'veneno':-0.4}

import itertools   # v9g


def patrones_regla():
    """v9g: los C(6,3)=20 patrones binarios de 6 px con exactamente 3 px activos."""
    pats = {}
    for combo in itertools.combinations(range(6), 3):
        v = np.zeros(6); v[list(combo)] = 1.
        pats[''.join('1' if v[j] else '0' for j in range(6))] = v
    return pats


def split_regla(seed, regla):
    """v9g: valencias por regla y particion train/test con RNG propios (no tocan el RNG del organismo)."""
    pats = patrones_regla(); nombres = sorted(pats)
    if regla == 'px0':
        vr = {k: ('comida' if k[0] == '1' else 'veneno') for k in nombres}; ntr = (5, 5)
    elif regla == 'xor01':
        vr = {k: ('comida' if k[0] != k[1] else 'veneno') for k in nombres}; ntr = (4, 4)
    elif regla == 'azar':
        r0 = np.random.default_rng(30000 + seed); perm = r0.permutation(len(nombres))
        com = set(nombres[i] for i in perm[:10])
        vr = {k: ('comida' if k in com else 'veneno') for k in nombres}; ntr = (5, 5)
    else:
        raise ValueError(regla)
    food = [k for k in nombres if vr[k] == 'comida']; pois = [k for k in nombres if vr[k] == 'veneno']
    r = np.random.default_rng(10000 + seed); fi = r.permutation(len(food)); pi = r.permutation(len(pois))
    food = [food[i] for i in fi]; pois = [pois[i] for i in pi]
    tren = sorted(food[:ntr[0]] + pois[:ntr[1]]); test = sorted(food[ntr[0]:] + pois[ntr[1]:])
    return pats, tren, test, vr

def run(seed,T=100000,learn=True,invertir_en=None,nuevo=None,nuevo_en=50000,nuevo_val='veneno',solap_B=None,
        eta=.03,tau_e=.85,alpha=1.2,hambre_boca=2.0,aversion=1.0,costo=.002,nobj=4,log_cada=None,plast=True,theta=0.6,ema=0.02,paso=0.5,solap_AB=None,lam=0.05,memoria_rechazo=20,mu_norm=True,div_signo=True,eta_s=0.0,clip_s=3.0,puerta=None,mundo='AB',regla='px0',fase2_en=None,sonda_final=False,mask_rel=0,del_s=0.25,del_c=0.25,ema_c=0.05,puerta_pat=0,pat_shuf=0,pat_min=0,memoria_pares=None,mem_alfa=0.3,mem_rho=0.02):
    if mundo=='AB': P_=PAT; tren=['A','B']; test=[]   # v13g: con 'AB' es v13 exacto
    else: P_,tren,test,val_regla=split_regla(seed,regla); fase2_en=T//2 if fase2_en is None else fase2_en
    rng=np.random.default_rng(seed)
    Wl=rng.uniform(.1,.4,(2,9)); KW=np.zeros((NKMAX,6)); activa=np.zeros(NKMAX,bool); KW[:NK]=rng.uniform(0,1,(NK,6)); activa[:NK]=True
    def code(P):
        v=KW@P; v=np.where(activa,v,-1e9); return set(np.argsort(v)[-K:])
    objetivo_AB=0 if solap_AB is None else solap_AB
    if solap_AB: KW[:solap_AB]=0; KW[:solap_AB,0]=5.0
    cond=lambda: len(code(P_['A'])&code(P_['B']))==objetivo_AB and (nuevo is None or solap_B is None or (len(code(P_[nuevo])&code(P_['B']))==solap_B and len(code(P_[nuevo])&code(P_['A']))==0))
    while mundo=='AB' and not cond(): KW[objetivo_AB:NK]=rng.uniform(0,1,(NK-objetivo_AB,6))
    def kenyon(P): k=np.zeros(NKMAX); k[list(code(P))]=1; return k
    Wp=np.zeros(NKMAX); Wn=np.zeros(NKMAX); err=np.zeros(NKMAX); mu=np.zeros((NKMAX,6)); splits=0; el=np.zeros_like(Wl); tr=np.zeros(9)
    Wps=np.zeros(6); Wns=np.zeros(6)   # v13: via LENTA, lineal sobre la retina (inerte si eta_s=0)
    if memoria_pares not in (None,'combi','combi1'): raise ValueError(f"memoria_pares={memoria_pares!r}")   # v15c: perilla mal escrita no cae en silencio
    _PARv=[(i,j) for i in range(6) for j in range(i+1,6)]   # v15c (M3): las 15 celdas = pares de pixeles
    _MMv=np.zeros((15,4)); _MNv=np.zeros((15,4)); _MEv=np.full(15,1e9); _MGv=0   # v15c: valor, visitas, error propio, ganadora
    def _lenta_v15(P):   # v15c: con la perilla APAGADA es literalmente la lectura de v14
        if memoria_pares is None: return float((Wps-Wns)@P)
        _i,_j=_PARv[_MGv]; _c=int(P[_i])*2+int(P[_j])
        return float(_MMv[_MGv,_c]) if _MNv[_MGv,_c]>0 else 0.0   # abstencion explicita
    ncod={}; _ord=[]   # B: evidencia del CODIGO EXACTO (mordidas por codigo) y orden de aparicion
    def _key(_k): return frozenset(np.flatnonzero(_k).tolist())
    def _ev(_k):   # evidencia que LEE la puerta: la propia, o (control) la del codigo vecino en el orden de aparicion
        _q=_key(_k)
        if not pat_shuf: return ncod.get(_q,0)
        if _q not in ncod or len(_ord)<2: return 0
        return ncod[_ord[(_ord.index(_q)+1)%len(_ord)]]
    def _fam(_k):   # B: la puerta. puerta_pat>0 -> evidencia del codigo exacto; si no, celdas consolidadas (v13 EXACTO)
        if puerta_pat: return _ev(_k)>=puerta_pat and int((np.abs((Wp-Wn)[_k>0])>0.2).sum())>=pat_min
        return int((np.abs((Wp-Wn)[_k>0])>0.2).sum())>=puerta
    mup=np.zeros((NKMAX,6)); mun=np.zeros((NKMAX,6)); zp=np.zeros(NKMAX); zn=np.zeros(NKMAX)   # D: medias de P condicionadas al signo de R, con normalizador
    def valor(P):   # v13: el valor que usa la boca. Sin puerta: rapida+lenta (un error). Con puerta: la rapida si el patron le es FAMILIAR, si no la lenta
        _k=kenyon(P); _f=float((Wp-Wn)@_k); _s=_lenta_v15(P)
        return _f+_s if puerta is None else (_f if _fam(_k) else _s)   # familiar = >= puerta celdas del codigo con valor consolidado (|W|>0.2, el mismo umbral de v11)
    pos=0; E=1.0; objs={}; val={'A':'comida','B':'veneno'} if mundo=='AB' else dict(val_regla)
    err_max=0.0; t_conflicto=None; t_techo=None; n_techo=0   # instrumentacion v8, solo lectura
    _rech={}; _prev_on=-1   # v9: memoria de trabajo de rechazo (posicion -> paso hasta el que no es objetivo)
    sobre={'veneno':[0]*4,'comida':[0]*4}; llegadas={'veneno':[0]*4,'comida':[0]*4}; sin_objetivo=[0]*4   # v9: lectura
    tipos=['A','B'] if mundo=='AB' else list(tren)
    W_apriori=None; codigos_f2=None; primer={}   # v13g: sonda y primer encuentro (lectura)
    def spawn():
        while len(objs)<nobj:
            x=int(rng.integers(L))
            if x not in objs: objs[x]=tipos[int(rng.integers(len(tipos)))]
    spawn()
    q=lambda t:min(t//(T//4),3)
    split_t=[]; mord={k:[0]*4 for k in P_}; vis={k:[0]*4 for k in P_}; deaths=0; log=[]
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
        if mundo!='AB' and t==fase2_en:   # v13g: sonda a priori (valor TOTAL) y entrada de los de test
            W_apriori={_k:valor(P_[_k]) for _k in P_}
            codigos_f2={_k:sorted(int(_i) for _i in code(P_[_k])) for _k in P_}
            tipos.extend(test); primer={_k:None for _k in test}
        hambre=np.clip(1-E,0,1); d,k,left=see(contar=True); pat=P_[k]
        x=np.concatenate([pat*1.2,[1.5 if left else 0,0 if left else 1.5,1.0 if d==0 else 0.]]); noise=.15+.5*hambre
        V=Wl@x; p=1/(1+np.exp(-(V-.8)/noise)); u=p+rng.normal(0,.3,2); m=np.zeros(2)
        if u.max()>.5: m[np.argmax(u)]=1
        tr=tr*.7+x
        if learn: el=el*tau_e+np.outer(m-p,tr)
        pos=(pos+int(m[1]-m[0]))%L; d2,_,_=see(); Rp=.2 if d2<d else 0.
        R=0.
        if pos in objs:
            kk=objs[pos]; kc=kenyon(P_[kk]); Wb=Wp-Wn; _wf=float(Wb@kc); _ws=_lenta_v15(P_[kk])   # v13: las dos vias (v15c: la memoria de pares si la perilla esta encendida)
            _wt=_wf+_ws if puerta is None else (_wf if _fam(kc) else _ws)   # v13: valor total (sin puerta: suma; con puerta: la rapida si le es familiar)
            Vb=alpha*_wt+hambre_boca*hambre+.5; pb=1/(1+np.exp(-Vb/.3)); mordio=rng.random()<pb
            vis[kk][q(t)]+=1
            sobre[val[kk]][q(t)]+=1; llegadas[val[kk]][q(t)]+=int(_prev_on!=pos)
            if kk in primer and primer[kk] is None: primer[kk]=dict(t=t,W=_wt,pb=float(pb),hambre=float(hambre),mordio=bool(mordio))   # v13g
            if memoria_rechazo and not mordio: _rech[pos]=t+memoria_rechazo   # v9: la boca rechazo -> no es objetivo por un tiempo
            if mordio:
                R=R_VAL[val[kk]]; E=min(E+E_VAL[val[kk]],1.5); mord[kk][q(t)]+=1
                _ky=_key(kc)
                if _ky not in ncod: _ord.append(_ky)
                ncod[_ky]=ncod.get(_ky,0)+1   # B: evidencia del codigo exacto
                del objs[pos]; spawn()
                _rech.pop(pos,None)   # v9: ese objeto ya no existe
                if learn:
                    dlt=R-_wt if puerta is None else R-_wf   # v13: sin puerta UN error compartido; con puerta cada via el suyo
                    if eta_s:   # v13: actualizacion de la via lenta (su tasa, mismo drenaje)
                        _ds=dlt if puerta is None else R-_ws
                        if memoria_pares is not None:   # v15c (M3): las 15 celdas escriben; la primera vez, DE UN GOLPE
                            _Pv=P_[kk]
                            for _cv in range(15):
                                _iv,_jv=_PARv[_cv]; _dv=int(_Pv[_iv])*2+int(_Pv[_jv])
                                _pv=float(_MMv[_cv,_dv]) if _MNv[_cv,_dv]>0 else 0.0
                                _erv=R-_pv; _prv=bool(_MNv[_cv].sum()==0)
                                _MEv[_cv]=(_erv*_erv) if _prv else (1-mem_rho)*_MEv[_cv]+mem_rho*(_erv*_erv)
                                if _MNv[_cv,_dv]==0: _MMv[_cv,_dv]=R
                                elif memoria_pares=='combi': _MMv[_cv,_dv]+=mem_alfa*(R-_MMv[_cv,_dv])
                                _MNv[_cv,_dv]+=1
                            _mnv=float(_MEv.min()); _empv=[int(_x) for _x in np.where(_MEv<=_mnv+1e-12)[0]]
                            _MGv=_empv[0] if len(_empv)==1 else int(_empv[int(rng.integers(len(_empv)))])   # desempate al azar; solo consume rng si HAY empate
                        if lam: _mcs=np.minimum(Wps,Wns)*(P_[kk]>0); Wps=Wps-lam*_mcs; Wns=Wns-lam*_mcs
                        if _ds>0: Wps=np.clip(Wps+eta_s*_ds*P_[kk],0,clip_s)
                        else:     Wns=np.clip(Wns+eta_s*aversion*(-_ds)*P_[kk],0,clip_s)
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
                        P=P_[kk]; idx=np.where(kc>0)[0]; err[idx]=(1-ema)*err[idx]+ema*abs(dlt); mu[idx]=(1-ema)*mu[idx]+ema*P
                        if R>0: mup[idx]=(1-ema_c)*mup[idx]+ema_c*P; zp[idx]=(1-ema_c)*zp[idx]+ema_c   # D
                        elif R<0: mun[idx]=(1-ema_c)*mun[idx]+ema_c*P; zn[idx]=(1-ema_c)*zn[idx]+ema_c   # D
                        err_max=max(err_max,float(err[idx].max()))
                        for c in idx:
                            if div_signo:   # v11 (JUACO-EVO gen1/llm_2): divide por CONFLICTO DE SIGNO, hija ciega fuera de P, madre fija, fision del valor
                                dist=P-(mu[c]*(P.sum()/max(float(mu[c].sum()),1e-9)) if mu_norm else mu[c])
                                if mask_rel==2 and zp[c]>1e-6 and zn[c]>1e-6:   # D: HIJA DISPERSA (contexto O discriminador)
                                    _mp=mup[c]/float(zp[c]); _mn=mun[c]/float(zn[c])
                                    _rel=(P>0)&((np.abs(_mp-_mn)>del_s)|(np.minimum(_mp,_mn)>1.0-del_c))
                                else: _rel=(P>0)
                                kj=np.clip(KW[c]*(1-0.05)+paso*dist,0,5)*_rel
                                if Wb[c]*R<0 and abs(float(Wb[c]))>0.2 and float(kj@P)>float(KW[c]@P) and (~activa).any():
                                    j=int(np.where(~activa)[0][0]); activa[j]=True; KW[j]=kj
                                    if R>0: Wp[j]=Wp[c]; Wn[j]=0.; Wp[c]=0.
                                    else:   Wn[j]=Wn[c]; Wp[j]=0.; Wn[c]=0.
                                    mu[j]=P*(float(mu[c].sum())/P.sum()); err[c]=err[j]=0; splits+=1; split_t.append((t,kk))
                                    mup[j]=mup[c].copy(); mun[j]=mun[c].copy(); zp[j]=zp[c]; zn[j]=zn[c]   # D: la hija hereda las medias condicionadas
                            elif err[c]>theta and (~activa).any():
                                j=int(np.where(~activa)[0][0]); activa[j]=True; dist=P-(mu[c]*(P.sum()/max(float(mu[c].sum()),1e-9)) if mu_norm else mu[c])   # v10: mu normalizada a la masa del patron
                                KW[j]=np.clip(KW[c]+paso*dist,0,5); KW[c]=np.clip(KW[c]-paso*dist,0,5)
                                Wp[j]=Wp[c]; Wn[j]=Wn[c]; mu[j]=mu[c].copy(); err[c]=err[j]=0; splits+=1; split_t.append((t,kk))
        _prev_on=pos if pos in objs else -1   # v9: para contar llegadas
        E-=costo
        if rng.random()<.003 and objs:
            _dx=list(objs)[int(rng.integers(len(objs)))]; del objs[_dx]; spawn(); _rech.pop(_dx,None)   # v9: olvido
        if learn: Wl=np.clip(Wl+eta*(1+2*hambre)*(max(R,0)+Rp)*el,0,1.5)
        if E<=0: deaths+=1; E=.6; pos=int(rng.integers(L))
        if log_cada and t%log_cada==0: log.append((t,)+tuple(round(valor(P_[k]),2) for k in 'ABCD'))
    _sonda=None; _cod_fin=None
    if sonda_final:   # v13g: valor TOTAL y codigo de los 64 patrones al final (lectura)
        _sonda={}
        for _n in range(64):
            _P=np.array([(_n>>(5-_j))&1 for _j in range(6)],float); _nm=''.join(str(int(_v)) for _v in _P)
            _sonda[_nm]=dict(W=valor(_P),codigo=sorted(int(_i) for _i in code(_P)))
        _cod_fin={_k:sorted(int(_i) for _i in code(P_[_k])) for _k in P_}
    W={k:round(valor(P_[k]),2) for k in P_}   # v13: valor total
    W_lenta={k:round(float((Wps-Wns)@P_[k]),3) for k in P_}   # v13: lectura de la via lenta sola
    comp={k:(round(float(Wp@kenyon(P_[k])),2),round(float(Wn@kenyon(P_[k])),2)) for k in P_}
    return dict(memoria_pares=memoria_pares,mem_ganadora=(list(_PARv[_MGv]) if memoria_pares is not None else None),mem_tabla=([[float(_x) for _x in _f] for _f in _MMv] if memoria_pares is not None else None),mem_vistas=(int((_MNv>0).sum()) if memoria_pares is not None else None),mem_cobertura=(int((_MNv[_MGv]>0).sum()) if memoria_pares is not None else None),sobre=sobre,llegadas=llegadas,sin_objetivo=sin_objetivo,memoria_rechazo=memoria_rechazo,err_max=err_max,t_conflicto=t_conflicto,t_techo=t_techo,n_techo=n_techo,split_t=split_t,mord=mord,vis=vis,W=W,comp=comp,deaths=deaths,log=log,splits=splits,celdas=int(activa.sum()),puerta_pat=puerta_pat,pat_shuf=pat_shuf,pat_min=pat_min,n_cod=len(ncod),
                solap=None if mundo!='AB' else {'AB':len(code(P_['A'])&code(P_['B'])),'nB':len(code(P_[nuevo])&code(P_['B'])) if nuevo else None},W_lenta=W_lenta,Wps=[round(float(x),3) for x in Wps],Wns=[round(float(x),3) for x in Wns],mundo=mundo,regla=regla,tren=tren,test=test,W_apriori=W_apriori,codigos_f2=codigos_f2,primer=primer,W_final=({_k:valor(P_[_k]) for _k in P_} if mundo!='AB' else None),sonda=_sonda,codigos_fin=_cod_fin)
