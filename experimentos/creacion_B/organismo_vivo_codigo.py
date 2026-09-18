"""organismo_vivo_codigo = experimentos/nivel11_mundo_vivo/organismo_vivo.py (20c0961c79de8825, solo se leyo) + perilla
`desambiguar` (B-5): division tambien por R == 0 bajo retina distinta; la hija nace sin valor en la necesidad
activa y hereda las otras (hereda_nec, como en v14.1). Con desambiguar=0 es organismo_vivo EXACTO (y con
vivo=0, n_nec=1 es organismo_v14 EXACTO, como su origen). El runner corre_codigo.py enciende la perilla por brazo.
Generado por construye_codigo.py. NO editar."""
"""organismo_vivo = organismo/organismo_v14.py (v14.1, feefc88b1fd8d434, TRONCO CONGELADO: aqui solo se LEYO) +
MUNDO VIVO (nivel 11, linea (F) de PLAN.md): DOS necesidades (hambre/sed) y CUATRO estimulos (comida A, veneno B,
agua C, sal D = los cuatro patrones que ya existen), estado interno VECTORIAL con dos muertes posibles, boca que
decide con la NECESIDAD ACTIVA, valor aprendido POR ESTIMULO Y POR NECESIDAD (Wp/Wn/Wps/Wns pasan a matriz
(n_nec, ...)), predictor de dS VECTORIAL y sorpresa POR NECESIDAD.
ANCLA DE IDENTIDAD: con vivo=0 y n_nec=1 (una necesidad, dos estimulos) es organismo_v14 BIT A BIT -- mismo
consumo del rng y MISMAS claves de salida (el dict del mundo vivo se agrega solo si vivo=1).
Arnes: identidad_vivo.py.  Generado por construye_vivo.py. NO editar a mano."""
"""v14.1 = TRONCO desde el 18 sep 2026 (05:55): v14 con eta_s 0.15 y clip_s 10 (bloque A-4: la regla local llega a 1.000 con rasgos dados, 150 exposiciones; examen 8/8 en 101-120 y 121-140, generalizacion 1.000/0.97). v14 (05:00) era: organismo_v13 (cc8b16b492d4d324) + HIJA DISPERSA por relevancia (mask_rel=2,
del_s=del_c=0.25, ema_c=0.05: la hija nace ciega a parte de P) + PUERTA DE FAMILIARIDAD POR EVIDENCIA DEL CODIGO EXACTO
(puerta_pat=5, pat_min=1: familiar si el codigo se mordio >= 5 veces Y tiene >= 1 celda consolidada). Generado por anclas
(experimentos/nivel10_composicion_v14/construye_v14c.py; copia de organismo_v14c_on.py 00e941c861896455). Con mask_rel=0 y
puerta_pat=0 es organismo_v13 EXACTO (identidad 30/30). Examen v3' 8/8 en 121-140, 141-160 y 161-180 (7/8 en 101-120: semilla
117, caso conocido); generalizacion 1.000/0.94-0.95 x3; capacidad N* 51; 3T-k 0.237 con 53 celdas. Gemelo: organismo_v14_rapido.py.
CONGELADO: no se edita. Evidencia: registro/PROPUESTA_v14.md y REGISTRO_etapas_1_2.md.
"""
"""organismo_v14c_on = organismo_v14c.py con mask_rel=2 (hija dispersa; el punto de organismo_v13Don) Y
puerta_pat=5,pat_min=1 (puerta por codigo PATC = evidencia Y >=1 celda consolidada; el punto de
organismo_v13Bn5c) POR DEFECTO -- las DOS perillas ENCENDIDAS. El mismo archivo con las constantes
cambiadas, para que bateria_v14c.py lo examine sin tocar la bateria congelada.
Generado por construye_v14c.py. NO editar."""
"""organismo_v14c = organismo/organismo_v13.py (cc8b16b492d4d324, CONGELADO: solo se leyo) + COMPOSICION
de los dos candidatos a v14 con evidencia completa (registro/PROPUESTA_v14.md): HIJA DISPERSA POR
RELEVANCIA (perilla mask_rel; actua en el NACIMIENTO, nivel7_hija_dispersa/construye_v13D.py) + PUERTA POR
EVIDENCIA DEL CODIGO EXACTO (perilla puerta_pat, PATC; actua en el RUTEO, no en el aprendizaje,
nivel4_puerta_codigo/construye_puerta_codigo.py). Generado por construye_v14c.py. NO editar a mano.
Con mask_rel=0 y puerta_pat=0 es organismo_v13 EXACTO (arnes: identidad_v14c.py)."""
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
# --- MUNDO VIVO (nivel 11): DOS necesidades y CUATRO estimulos = los CUATRO patrones que YA existen.
#     El eje de ENERGIA es exactamente el de v14: EFECTO['comida'][0]==E_VAL['comida'] y
#     EFECTO['veneno'][0]==E_VAL['veneno']; el mapa de recompensa (dS>0->+1, dS<0->-3) reproduce R_VAL.
NEC=('hambre','sed')   # 0 = energia (E), 1 = agua (Ag)
VAL_VIVO={'A':'comida','B':'veneno','C':'agua','D':'sal'}
EFECTO={'comida':(+0.8,0.0),'veneno':(-0.4,0.0),'agua':(0.0,+0.8),'sal':(0.0,-0.4)}   # (dE, dAgua) nominal

def run(seed,T=100000,learn=True,invertir_en=None,nuevo=None,nuevo_en=50000,nuevo_val='veneno',solap_B=None,
        eta=.03,tau_e=.85,alpha=1.2,hambre_boca=2.0,aversion=1.0,costo=.002,nobj=4,log_cada=None,plast=True,theta=0.6,ema=0.02,paso=0.5,solap_AB=None,lam=0.05,memoria_rechazo=20,mu_norm=True,div_signo=True,eta_s=0.15,clip_s=10.0,puerta=3,mask_rel=2,del_s=0.25,del_c=0.25,ema_c=0.05,puerta_pat=5,pat_shuf=0,pat_min=1,vivo=0,n_nec=1,estims=None,costo_a=0.002,A_ini=1.0,val_esc=0,nec_shuf=0,hereda_nec=1,tabla=None,eta_pred=0.0,ema_pred=0.05,clip_e=3.0,k_sorp=0.0,crit_exp=0.5,desambiguar=0):
    if n_nec>1 and not vivo: raise SystemExit('MUNDO VIVO: n_nec>1 exige vivo=1 (la mordida debe tener consecuencia vectorial)')
    rng=np.random.default_rng(seed)
    Wl=rng.uniform(.1,.4,(2,9)); KW=np.zeros((NKMAX,6)); activa=np.zeros(NKMAX,bool); KW[:NK]=rng.uniform(0,1,(NK,6)); activa[:NK]=True
    def code(P):
        v=KW@P; v=np.where(activa,v,-1e9); return set(np.argsort(v)[-K:])
    objetivo_AB=0 if solap_AB is None else solap_AB
    if solap_AB: KW[:solap_AB]=0; KW[:solap_AB,0]=5.0
    cond=lambda: len(code(PAT['A'])&code(PAT['B']))==objetivo_AB and (nuevo is None or solap_B is None or (len(code(PAT[nuevo])&code(PAT['B']))==solap_B and len(code(PAT[nuevo])&code(PAT['A']))==0))
    while not cond(): KW[objetivo_AB:NK]=rng.uniform(0,1,(NK-objetivo_AB,6))
    def kenyon(P): k=np.zeros(NKMAX); k[list(code(P))]=1; return k
    Wp=np.zeros((n_nec,NKMAX)); Wn=np.zeros((n_nec,NKMAX)); err=np.zeros(NKMAX); mu=np.zeros((NKMAX,6)); splits=0; _ndes=0; _des_t=[]; el=np.zeros_like(Wl); tr=np.zeros(9)
    Wps=np.zeros((n_nec,6)); Wns=np.zeros((n_nec,6))   # v13: via LENTA, lineal sobre la retina (inerte si eta_s=0). VIVO: una fila por necesidad
    _na=0; _nm=0   # VIVO: necesidad ACTIVA (manda boca y division) y la que INDEXA la memoria (val_esc -> siempre 0). Con n_nec=1 nunca cambian
    _EF=dict(EFECTO) if tabla is None else dict(tabla)   # VIVO: (dE,dAg) por valencia; `tabla` sirve para el control 'estimulo que no informa'
    _rng_n=np.random.default_rng(seed+900000) if nec_shuf else None   # CONTROL barajado: rng PROPIO (v13s), no toca el del organismo
    Wpe=np.zeros((n_nec,6)); Wke=np.zeros((n_nec,NKMAX)); _sbE=np.zeros(n_nec)   # VIVO: predictor VECTORIAL de dS y SORPRESA POR NECESIDAD (inerte con eta_pred=0)
    _enc={k:0 for k in PAT}; _exp=[{k:None for k in PAT} for _ in range(n_nec)]   # VIVO: exposiciones y EXPOSICIONES HASTA CRITERIO (solo lectura)
    _mnec=[0,0]; _bxor=[[0]*4 for _ in range(n_nec)]; _exor=[[0]*4 for _ in range(n_nec)]   # VIVO: muertes [por energia, por agua] y tabla NECESIDAD x ESTIMULO (solo lectura)
    _IDX={_k2:_i2 for _i2,_k2 in enumerate('ABCD')}
    ncod={}; _ord=[]   # B: evidencia del CODIGO EXACTO (mordidas por codigo) y orden de aparicion
    def _key(_k): return frozenset(np.flatnonzero(_k).tolist())
    def _ev(_k):   # evidencia que LEE la puerta: la propia, o (control) la del codigo vecino en el orden de aparicion
        _q=_key(_k)
        if not pat_shuf: return ncod.get(_q,0)
        if _q not in ncod or len(_ord)<2: return 0
        return ncod[_ord[(_ord.index(_q)+1)%len(_ord)]]
    def _fam(_k,_n=None):   # B: la puerta. puerta_pat>0 -> evidencia del codigo exacto; si no, celdas consolidadas (v13 EXACTO). VIVO: lee la fila de la necesidad
        _w=Wp[_nm if _n is None else _n]-Wn[_nm if _n is None else _n]
        if puerta_pat: return _ev(_k)>=puerta_pat and int((np.abs(_w[_k>0])>0.2).sum())>=pat_min
        return int((np.abs(_w[_k>0])>0.2).sum())>=puerta
    mup=np.zeros((NKMAX,6)); mun=np.zeros((NKMAX,6)); zp=np.zeros(NKMAX); zn=np.zeros(NKMAX)   # D: medias de P condicionadas al signo de R, con normalizador
    def valor(P):   # v13: el valor que usa la boca. Sin puerta: rapida+lenta (un error). Con puerta: la rapida si el patron le es FAMILIAR, si no la lenta
        _k=kenyon(P); _f=float((Wp[_nm]-Wn[_nm])@_k); _s=float((Wps[_nm]-Wns[_nm])@P)
        return _f+_s if puerta is None else (_f if _fam(_k) else _s)   # familiar = >= puerta celdas del codigo con valor consolidado (|W|>0.2, el mismo umbral de v11)
    def _vnec(_n,P,_k):   # VIVO: el valor que la boca usaria para la necesidad _n (mismo ruteo que valor()). SOLO LECTURA
        _f=float((Wp[_n]-Wn[_n])@_k); _s=float((Wps[_n]-Wns[_n])@P)
        return _f+_s if puerta is None else (_f if _fam(_k,_n) else _s)
    pos=0; E=1.0; Ag=A_ini; objs={}; val=(dict(VAL_VIVO) if vivo else {'A':'comida','B':'veneno'})
    err_max=0.0; t_conflicto=None; t_techo=None; n_techo=0   # instrumentacion v8, solo lectura
    _rech={}; _prev_on=-1   # v9: memoria de trabajo de rechazo (posicion -> paso hasta el que no es objetivo)
    sobre={'veneno':[0]*4,'comida':[0]*4}; llegadas={'veneno':[0]*4,'comida':[0]*4}; sin_objetivo=[0]*4   # v9: lectura
    tipos=(list(estims) if estims else ['A','B'])   # VIVO: con dos estimulos, spawn() sortea igual que v14
    if vivo:   # VIVO: una entrada por valencia PRESENTE; con dos estimulos no se agrega ninguna -> los dicts son los de v14
        for _v in ('agua','sal'):
            if _v in [val[_t] for _t in tipos]: sobre[_v]=[0]*4; llegadas[_v]=[0]*4
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
        hambre=np.clip(1-E,0,1)
        if n_nec>1:   # VIVO: deficit por necesidad; manda la ACTIVA (la mas deficitaria). Con n_nec=1 esta rama no existe
            _dfa=np.clip(1-Ag,0,1); _na=1 if _dfa>hambre else 0
            if _na: hambre=_dfa
            if nec_shuf==1: _na=int(_rng_n.integers(n_nec))   # CONTROL 1: la POLITICA se baraja (la tabla de valor SOBREVIVE: cada fila sigue viendo su componente)
            _nm=0 if val_esc else _na   # val_esc=1: UN escalar por celda para todas las necesidades (alternativa a refutar)
        d,k,left=see(contar=True); pat=PAT[k]
        x=np.concatenate([pat*1.2,[1.5 if left else 0,0 if left else 1.5,1.0 if d==0 else 0.]]); noise=.15+.5*hambre
        V=Wl@x; p=1/(1+np.exp(-(V-.8)/noise)); u=p+rng.normal(0,.3,2); m=np.zeros(2)
        if u.max()>.5: m[np.argmax(u)]=1
        tr=tr*.7+x
        if learn: el=el*tau_e+np.outer(m-p,tr)
        pos=(pos+int(m[1]-m[0]))%L; d2,_,_=see(); Rp=.2 if d2<d else 0.
        R=0.
        if pos in objs:
            kk=objs[pos]; kc=kenyon(PAT[kk]); Wb=Wp[_nm]-Wn[_nm]; _wf=float(Wb@kc); _ws=float((Wps[_nm]-Wns[_nm])@PAT[kk])   # v13: las dos vias (VIVO: las de la necesidad activa)
            _wt=_wf+_ws if puerta is None else (_wf if _fam(kc) else _ws)   # v13: valor total (sin puerta: suma; con puerta: la rapida si le es familiar)
            Vb=alpha*_wt+hambre_boca*hambre+.5
            if k_sorp: Vb+=k_sorp*float(_sbE[_na])   # VIVO: la SORPRESA DE LA NECESIDAD ACTIVA en la boca (la dosis de v15, ahora especifica)
            pb=1/(1+np.exp(-Vb/.3)); mordio=rng.random()<pb
            vis[kk][q(t)]+=1
            sobre[val[kk]][q(t)]+=1; llegadas[val[kk]][q(t)]+=int(_prev_on!=pos)
            if vivo and _prev_on!=pos:   # VIVO: EXPOSICIONES (llegadas) y EXPOSICIONES HASTA CRITERIO, por necesidad. SOLO LECTURA
                _enc[kk]+=1; _exor[_na][_IDX[kk]]+=1
                for _n in range(n_nec):
                    _s0=_EF[val[kk]][_n]
                    if _s0 and _exp[_n][kk] is None:
                        _v0=_vnec(_n,PAT[kk],kc)
                        if _v0*_s0>0 and abs(_v0)>=crit_exp: _exp[_n][kk]=_enc[kk]
            if memoria_rechazo and not mordio: _rech[pos]=t+memoria_rechazo   # v9: la boca rechazo -> no es objetivo por un tiempo
            if mordio:
                if vivo:   # VIVO: la mordida tiene consecuencia VECTORIAL -> UN encuentro ensena a TODAS las necesidades
                    _dS=_EF[val[kk]]; _Rv=[(1.0 if _x>0 else (-3.0 if _x<0 else 0.0)) for _x in _dS]
                    if nec_shuf>1: _Rv=[_Rv[_i] for _i in _rng_n.permutation(n_nec)]   # CONTROL 2: se baraja QUE componente ENSENA a cada necesidad; el cuerpo recibe dS intacto
                    R=_Rv[_na]; E=min(E+_dS[0],1.5); Ag=min(Ag+_dS[1],1.5); _bxor[_na][_IDX[kk]]+=1
                else: _dS=(E_VAL[val[kk]],0.0); _Rv=[R_VAL[val[kk]]]; R=R_VAL[val[kk]]; E=min(E+E_VAL[val[kk]],1.5)
                mord[kk][q(t)]+=1
                _ky=_key(kc)
                if _ky not in ncod: _ord.append(_ky)
                ncod[_ky]=ncod.get(_ky,0)+1   # B: evidencia del codigo exacto
                del objs[pos]; spawn()
                _rech.pop(pos,None)   # v9: ese objeto ya no existe
                if learn:
                    if eta_pred:   # VIVO: predictor VECTORIAL de dS (el de allostasis); la SORPRESA es POR NECESIDAD. No toca el rng
                        _dp=Wpe@PAT[kk]+Wke@kc; _ep=np.array(_dS[:n_nec])-_dp
                        Wpe=np.clip(Wpe+eta_pred*np.outer(_ep,PAT[kk]),-clip_e,clip_e); Wke=np.clip(Wke+eta_pred*np.outer(_ep,kc),-clip_e,clip_e)
                        _sbE=(1.-ema_pred)*_sbE+ema_pred*np.abs(_ep)   # causal: la usa la boca del PROXIMO encuentro
                    dlt=R-_wt if puerta is None else R-_wf   # v13: sin puerta UN error compartido; con puerta cada via el suyo
                    if eta_s:   # v13: actualizacion de la via lenta (su tasa, mismo drenaje)
                        _ds=dlt if puerta is None else R-_ws
                        if lam: _mcs=np.minimum(Wps[_nm],Wns[_nm])*(PAT[kk]>0); Wps[_nm]=Wps[_nm]-lam*_mcs; Wns[_nm]=Wns[_nm]-lam*_mcs
                        if _ds>0: Wps[_nm]=np.clip(Wps[_nm]+eta_s*_ds*PAT[kk],0,clip_s)
                        else:     Wns[_nm]=np.clip(Wns[_nm]+eta_s*aversion*(-_ds)*PAT[kk],0,clip_s)
                    if lam: ix=kc>0; mcom=np.minimum(Wp[_nm][ix],Wn[_nm][ix]); Wp[_nm][ix]-=lam*mcom; Wn[_nm][ix]-=lam*mcom   # BUG-01 exp2: decae solo la parte comun
                    _ix=kc>0
                    if dlt>0: _trunca=bool(((Wp[_nm][_ix]+eta*dlt)>3.0).any())
                    else:     _trunca=bool(((Wn[_nm][_ix]+eta*aversion*(-dlt))>3.0).any())
                    if _trunca:
                        n_techo+=1
                        if t_techo is None: t_techo=t
                    if dlt>0: Wp[_nm]=np.clip(Wp[_nm]+eta*dlt*kc,0,3.)
                    else:     Wn[_nm]=np.clip(Wn[_nm]+eta*aversion*(-dlt)*kc,0,3.)
                    if t_conflicto is None and bool((np.minimum(Wp[_nm][_ix],Wn[_nm][_ix])>0).any()): t_conflicto=t
                    if n_nec>1:   # VIVO: las OTRAS necesidades aprenden de SU componente del MISMO bocado (esto es lo que compra el mundo vivo)
                        for _n in range(n_nec):
                            if _n==_nm: continue
                            _Rn=_Rv[_n]; _wfn=float((Wp[_n]-Wn[_n])@kc); _wsn=float((Wps[_n]-Wns[_n])@PAT[kk])
                            _dn=_Rn-(_wfn+_wsn) if puerta is None else _Rn-_wfn
                            if eta_s:
                                _dsn=_dn if puerta is None else _Rn-_wsn
                                if lam: _mn2=np.minimum(Wps[_n],Wns[_n])*(PAT[kk]>0); Wps[_n]=Wps[_n]-lam*_mn2; Wns[_n]=Wns[_n]-lam*_mn2
                                if _dsn>0: Wps[_n]=np.clip(Wps[_n]+eta_s*_dsn*PAT[kk],0,clip_s)
                                else:      Wns[_n]=np.clip(Wns[_n]+eta_s*aversion*(-_dsn)*PAT[kk],0,clip_s)
                            if lam: _mc2=np.minimum(Wp[_n][_ix],Wn[_n][_ix]); Wp[_n][_ix]-=lam*_mc2; Wn[_n][_ix]-=lam*_mc2
                            if _dn>0: Wp[_n]=np.clip(Wp[_n]+eta*_dn*kc,0,3.)
                            else:     Wn[_n]=np.clip(Wn[_n]+eta*aversion*(-_dn)*kc,0,3.)
                    if plast:
                        P=PAT[kk]; idx=np.where(kc>0)[0]; err[idx]=(1-ema)*err[idx]+ema*abs(dlt); mu[idx]=(1-ema)*mu[idx]+ema*P
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
                                if (Wb[c]*R<0 or (desambiguar and R==0)) and abs(float(Wb[c]))>0.2 and float(kj@P)>float(KW[c]@P) and (~activa).any():   # B-5 DESAMBIGUAR: tambien divide cuando una celda consolidada, bajo una retina distinta (kj@P>KW[c]@P), recibe R==0
                                    j=int(np.where(~activa)[0][0]); activa[j]=True; KW[j]=kj
                                    if R>0: Wp[_nm,j]=Wp[_nm,c]; Wn[_nm,j]=0.; Wp[_nm,c]=0.
                                    elif R<0: Wn[_nm,j]=Wn[_nm,c]; Wp[_nm,j]=0.; Wn[_nm,c]=0.
                                    else: Wp[_nm,j]=0.; Wn[_nm,j]=0.; _ndes+=1; _des_t.append((t,kk))   # B-5: con R==0 la hija nace SIN valor en la necesidad activa (las otras se heredan abajo) y la madre conserva el suyo
                                    if n_nec>1 and hereda_nec:   # VIVO: la hija HEREDA el valor de las OTRAS necesidades (la madre lo conserva); la fision es solo de la activa
                                        for _n in range(n_nec):
                                            if _n!=_nm: Wp[_n,j]=Wp[_n,c]; Wn[_n,j]=Wn[_n,c]
                                    mu[j]=P*(float(mu[c].sum())/P.sum()); err[c]=err[j]=0; splits+=1; split_t.append((t,kk))
                                    mup[j]=mup[c].copy(); mun[j]=mun[c].copy(); zp[j]=zp[c]; zn[j]=zn[c]   # D: la hija hereda las medias condicionadas
                            elif err[c]>theta and (~activa).any():
                                j=int(np.where(~activa)[0][0]); activa[j]=True; dist=P-(mu[c]*(P.sum()/max(float(mu[c].sum()),1e-9)) if mu_norm else mu[c])   # v10: mu normalizada a la masa del patron
                                KW[j]=np.clip(KW[c]+paso*dist,0,5); KW[c]=np.clip(KW[c]-paso*dist,0,5)
                                Wp[:,j]=Wp[:,c]; Wn[:,j]=Wn[:,c]; mu[j]=mu[c].copy(); err[c]=err[j]=0; splits+=1; split_t.append((t,kk))
        _prev_on=pos if pos in objs else -1   # v9: para contar llegadas
        E-=costo
        if vivo: Ag-=costo_a   # VIVO: el agua tambien baja sola
        if rng.random()<.003 and objs:
            _dx=list(objs)[int(rng.integers(len(objs)))]; del objs[_dx]; spawn(); _rech.pop(_dx,None)   # v9: olvido
        if learn: Wl=np.clip(Wl+eta*(1+2*hambre)*(max(R,0)+Rp)*el,0,1.5)
        if E<=0 or (vivo and Ag<=0):   # VIVO: DOS muertes posibles (con vivo=0 la segunda es imposible: Ag=A_ini y no baja)
            deaths+=1; _mnec[0 if E<=0 else 1]+=1; E=.6
            if vivo: Ag=.6
            pos=int(rng.integers(L))
        if log_cada and t%log_cada==0: log.append((t,)+tuple(round(valor(PAT[k]),2) for k in 'ABCD'))
    W={k:round(valor(PAT[k]),2) for k in PAT}   # v13: valor total
    W_lenta={k:round(float((Wps[_nm]-Wns[_nm])@PAT[k]),3) for k in PAT}   # v13: lectura de la via lenta sola
    comp={k:(round(float(Wp[_nm]@kenyon(PAT[k])),2),round(float(Wn[_nm]@kenyon(PAT[k])),2)) for k in PAT}
    _ext=(dict(n_nec=n_nec,estims=list(tipos),agua=round(float(Ag),3),muertes_nec=list(_mnec),
               exp_hasta=[dict(_exp[_n]) for _n in range(n_nec)],exposiciones=dict(_enc),
               W_nec=[{_k3:round(_vnec(_n,PAT[_k3],kenyon(PAT[_k3])),2) for _k3 in PAT} for _n in range(n_nec)],
               xor_mord=[list(_bxor[_n]) for _n in range(n_nec)],xor_enc=[list(_exor[_n]) for _n in range(n_nec)],
               sorp_nec=[round(float(_x),4) for _x in _sbE]) if vivo else {})   # VIVO: claves nuevas SOLO si vivo=1 (con vivo=0 el dict es el de v14, clave por clave)
    return dict(desambiguar=desambiguar,des_splits=_ndes,des_t=_des_t,sobre=sobre,llegadas=llegadas,sin_objetivo=sin_objetivo,memoria_rechazo=memoria_rechazo,err_max=err_max,t_conflicto=t_conflicto,t_techo=t_techo,n_techo=n_techo,split_t=split_t,mord=mord,vis=vis,W=W,comp=comp,deaths=deaths,log=log,splits=splits,celdas=int(activa.sum()),puerta_pat=puerta_pat,pat_shuf=pat_shuf,pat_min=pat_min,n_cod=len(ncod),
                solap={'AB':len(code(PAT['A'])&code(PAT['B'])),'nB':len(code(PAT[nuevo])&code(PAT['B'])) if nuevo else None},W_lenta=W_lenta,Wps=[round(float(x),3) for x in Wps[_nm]],Wns=[round(float(x),3) for x in Wns[_nm]],**_ext)
