"""organismo_familias_b2 = experimentos/nivel12_mundo_familias/organismo_familias.py (b9dd561a0cf056b8,
identidad 43/43; que a su vez es el TRONCO organismo/organismo_v14.py, v14.1, feefc88b1fd8d434) + TRES PERILLAS
DEL MUNDO/REGISTRO para el BLOQUE 2 (capacidad directa): `vira` (una variante -- y solo ella -- cambia de
consecuencia en `cambio`), `exc_evita` (las excepciones no ocupan la variante retenida) y `reg_b2` (registro de la
CONDUCTA de la boca en la primera exposicion y de la separacion tras el cambio).
NO hay organo nuevo: el organismo sigue siendo v14.1 tal cual.
ANCLA DE IDENTIDAD: con vira=0, exc_evita=-1, reg_b2=0 es organismo_familias BIT A BIT (mismas claves, mismo rng);
y por herencia, con mundo='AB', organismo_v14 bit a bit.  Arnes: identidad_familias_b2.py.
Generado por construye_familias_b2.py. NO editar a mano."""
"""organismo_familias = organismo/organismo_v14.py (v14.1, feefc88b1fd8d434, TRONCO CONGELADO: aqui solo se LEYO)
+ B-5 (anclas literales de experimentos/creacion_B/construye_codigo.py, f94aa0a2f714c28d)
+ MUNDO DE FAMILIAS (bloque 1, nivel 12): retina D = 9 forma + 3 variable, F tokens de peso 3, V variantes por token,
excepciones dentro de la familia, deriva de la variante presente, cambio de una familia en T/2, RENOVACION SIMETRICA
(lo rechazado desaparece igual que lo mordido) y valencia NEUTRA opcional (n_neu: R == 0).
NO hay organo nuevo: el organismo es v14.1 tal cual; lo unico nuevo es el mundo (y B-5, reparacion ya medida).
ANCLA DE IDENTIDAD: con mundo='AB' es organismo_v14 BIT A BIT -- mismo consumo del rng y MISMAS claves de salida
(el dict del mundo de familias se agrega solo si mundo!='AB'); con mundo='AB' y desambiguar=1 es
experimentos/creacion_B/organismo_v14_codigo_on.py bit a bit.
Arnes: identidad_familias.py.  Generado por construye_familias.py. NO editar a mano."""
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

# ============================= MUNDO DE FAMILIAS (bloque 1, nivel 12) =============================
R_VAL['nada']=0.0; E_VAL['nada']=0.0   # FAMILIAS: valencia NEUTRA (R==0): el estimulo que NO informa. Con mundo='AB' nunca se usa.

def _familias(seed,D,n_var,F,V,n_exc,fam_val,n_neu,exc_evita=-1,vira=0):
    """Construye el mundo con un rng PROPIO (default_rng(SEMILLA_MUNDO+seed) dentro de escala_codigo.catalogo):
    NUNCA toca el rng del organismo, asi que con mundo='AB' el flujo aleatorio es el de v14.1 bit a bit.
    El CATALOGO no se reimplementa: es escala_codigo.catalogo (bloque 0), asi que el mundo de la semilla s es EL
    MISMO sobre el que el bloque 0 calculo el alias (PREREGISTRO_bloque1_familias.md 2.1 y 2.6)."""
    import escala_codigo as _EC                      # import perezoso: con mundo='AB' esta linea NUNCA se ejecuta
    _P,_fm,_ev,_rz,_Vef = _EC.catalogo(D,F,V,seed)
    if _Vef!=V: raise SystemExit(f'FAMILIAS: escala_codigo.catalogo degrado V de {V} a {_Vef} (D={D}). Abortado.')
    nom=[]; PAT={}; fam={}; var={}
    for _i in range(_P.shape[0]):
        _k=int(_fm[_i]); _n=('T%d'%_k) if not bool(_ev[_i]) else ('T%dv%d'%(_k,_i-int(_rz[_i])-1))
        nom.append(_n); PAT[_n]=_P[_i].astype(float); fam[_n]=_k; var[_n]=(-1 if not bool(_ev[_i]) else _i-int(_rz[_i])-1)
    g=np.random.default_rng(_EC.SEMILLA_MUNDO+seed+777)   # rng PROPIO para valencias y excepciones (el catalogo ya uso el suyo)
    base={_k:('comida' if _k%2==0 else 'veneno') for _k in range(F)}
    for _k in range(F-int(n_neu),F): base[_k]='nada'                    # FAMILIAS: los ultimos n_neu tokens NO informan
    val={_n:(base[(fam[_n]+1)%F] if (fam_val=='barajado' and var[_n]>=0) else base[fam[_n]]) for _n in PAT}
    # exc_win: UNA variante candidata por token, en orden de token (decision ESTRUCTURAL declarada, no un desempate).
    # Se sortea SIEMPRE -- tambien con n_exc=0 -- para que `lineal` tenga LA MISMA ventana de medida que `excepciones`.
    if int(exc_evita)<0: exc_win=['T%dv%d'%(_k,int(g.integers(V))) for _k in range(F)]
    else:   # B2: la variante RETENIDA por la deriva no puede ser ademas excepcion. UN entero del rng por token, igual que arriba.
        _al=[_v for _v in range(V) if _v!=int(exc_evita)]
        exc_win=['T%dv%d'%(_k,_al[int(g.integers(len(_al)))]) for _k in range(F)]
    if fam_val=='azar':   # la permutacion de `azar` va LA ULTIMA: asi tokens y exc_win son identicos en los 4 mundos
        _nn=sorted(PAT); _et=['comida']*(len(_nn)//2)+['veneno']*(len(_nn)-len(_nn)//2)
        _pm=g.permutation(len(_nn)).tolist()
        for _i,_n in enumerate(_nn): val[_n]=_et[_pm[_i]]
        for _k in range(F-int(n_neu),F):
            for _n in PAT:
                if fam[_n]==_k: val[_n]='nada'
    _op={'comida':'veneno','veneno':'comida','nada':'veneno'}
    exc=[_n for _n in exc_win[:max(int(n_exc),0)]]
    for _n in exc: val[_n]=_op[val[_n]]
    herm={_e:sorted(set(['T%d'%fam[_e]]+['T%dv%d'%(fam[_e],_v) for _v in range(V)])-{_e}) for _e in exc_win}
    pres=[['T%d'%_k for _k in range(F)]+['T%dv%d'%(_k,_i) for _k in range(F)] for _i in range(V)]
    if int(vira)>0:     _vp={_n:_op[val[_n]] for _n in exc_win[:int(vira)]}          # B2 SAL ROSA: cambia la variante, NO sus hermanas
    elif int(vira)<0:   _vp={}                                                          # B2 gemelo de control: en `cambio` no cambia NADA
    else:               _vp={_n:_op[val[_n]] for _n in PAT if fam[_n]==0 and _n not in exc}   # CAMBIO: la familia 0 invierte; su excepcion NO
    val_post=_vp
    return dict(PAT=PAT,fam=fam,var=var,val=val,exc=exc,exc_win=exc_win,herm=herm,pres=pres,val_post=val_post,viradas=list(exc_win[:abs(int(vira))]),
                nombres=nom,forma=D-n_var)

def run(seed,T=100000,learn=True,invertir_en=None,nuevo=None,nuevo_en=50000,nuevo_val='veneno',solap_B=None,
        eta=.03,tau_e=.85,alpha=1.2,hambre_boca=2.0,aversion=1.0,costo=.002,nobj=4,log_cada=None,plast=True,theta=0.6,ema=0.02,paso=0.5,solap_AB=None,lam=0.05,memoria_rechazo=20,mu_norm=True,div_signo=True,eta_s=0.15,clip_s=10.0,puerta=3,mask_rel=2,del_s=0.25,del_c=0.25,ema_c=0.05,puerta_pat=5,pat_shuf=0,pat_min=1,desambiguar=0,mundo='AB',pats=PAT,nk=NK,nkmax=NKMAX,ktop=K,largo=L,fam_D=12,fam_nvar=3,fam_F=8,fam_V=3,n_exc=4,n_neu=0,fam_val='familia',deriva=5000,cambio=None,renov=0.0,vent=10000,crit_exp=0.5,vira=0,exc_evita=-1,reg_b2=0):
    rng=np.random.default_rng(seed)
    PAT=pats; NK=nk; NKMAX=nkmax; K=ktop; L=largo   # FAMILIAS: sombra INERTE (los defaults SON las constantes del modulo)
    _MF=(mundo!='AB')   # FAMILIAS: con mundo='AB' NINGUNA linea nueva se ejecuta -> v14.1 BIT A BIT
    _FA=_familias(seed,fam_D,fam_nvar,fam_F,fam_V,n_exc,fam_val,n_neu,exc_evita,vira) if _MF else None   # rng PROPIO: no toca el del organismo
    if _MF: PAT=_FA['PAT']
    _D=len(next(iter(PAT.values())))   # FAMILIAS: tamano de la retina (6 con los patrones del tronco -> v14.1 exacto)
    Wl=rng.uniform(.1,.4,(2,_D+3)); KW=np.zeros((NKMAX,_D)); activa=np.zeros(NKMAX,bool); KW[:NK]=rng.uniform(0,1,(NK,_D)); activa[:NK]=True
    def code(P):
        v=KW@P; v=np.where(activa,v,-1e9); return set(np.argsort(v)[-K:])
    objetivo_AB=0 if solap_AB is None else solap_AB
    if solap_AB: KW[:solap_AB]=0; KW[:solap_AB,0]=5.0
    cond=(lambda: True) if _MF else (lambda: len(code(PAT['A'])&code(PAT['B']))==objetivo_AB and (nuevo is None or solap_B is None or (len(code(PAT[nuevo])&code(PAT['B']))==solap_B and len(code(PAT[nuevo])&code(PAT['A']))==0)))   # FAMILIAS: el rechazo del tronco solo restringe A y B, que no existen aqui (misma decision que escala_codigo.kw_del_tronco)
    while not cond(): KW[objetivo_AB:NK]=rng.uniform(0,1,(NK-objetivo_AB,_D))
    _cod0=({_a:sorted(code(PAT[_a])) for _a in sorted(PAT)} if _MF else None)   # FAMILIAS: el codigo INICIAL (antes de la primera fision), para cruzarlo con escala_codigo (bloque 0)
    def kenyon(P): k=np.zeros(NKMAX); k[list(code(P))]=1; return k
    Wp=np.zeros(NKMAX); Wn=np.zeros(NKMAX); err=np.zeros(NKMAX); mu=np.zeros((NKMAX,_D)); splits=0; _ndes=0; _des_t=[]; el=np.zeros_like(Wl); tr=np.zeros(_D+3)
    Wps=np.zeros(_D); Wns=np.zeros(_D)   # v13: via LENTA, lineal sobre la retina (inerte si eta_s=0)
    _ipa=-1; _tcam=(T//2 if cambio is None else cambio)   # FAMILIAS: deriva vigente y paso del cambio de familia
    _enc={}; _exp={}; _ult={}; _prim={}; _rut=[0,0]; _texc={}; _col=0; _omi=0; _nren=0; _fv=[[],[],[],[]]
    _pb2={}; _sep={}; _en2={}; _vir=(set(_FA['viradas']) if _MF else set())   # B2: registro (reg_b2). Dicts vacios: no consumen rng ni cambian ninguna decision.
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
    mup=np.zeros((NKMAX,_D)); mun=np.zeros((NKMAX,_D)); zp=np.zeros(NKMAX); zn=np.zeros(NKMAX)   # D: medias de P condicionadas al signo de R, con normalizador
    def valor(P):   # v13: el valor que usa la boca. Sin puerta: rapida+lenta (un error). Con puerta: la rapida si el patron le es FAMILIAR, si no la lenta
        _k=kenyon(P); _f=float((Wp-Wn)@_k); _s=float((Wps-Wns)@P)
        return _f+_s if puerta is None else (_f if _fam(_k) else _s)   # familiar = >= puerta celdas del codigo con valor consolidado (|W|>0.2, el mismo umbral de v11)
    pos=0; E=1.0; objs={}; val=(dict(_FA['val']) if _MF else {'A':'comida','B':'veneno'})
    err_max=0.0; t_conflicto=None; t_techo=None; n_techo=0   # instrumentacion v8, solo lectura
    _rech={}; _prev_on=-1   # v9: memoria de trabajo de rechazo (posicion -> paso hasta el que no es objetivo)
    sobre={'veneno':[0]*4,'comida':[0]*4}; llegadas={'veneno':[0]*4,'comida':[0]*4}; sin_objetivo=[0]*4   # v9: lectura
    if _MF: sobre['nada']=[0]*4; llegadas['nada']=[0]*4   # FAMILIAS: valencia NEUTRA (solo lectura)
    tipos=(list(_FA['pres'][0]) if _MF else ['A','B'])   # FAMILIAS: los F tokens + UNA variante por token
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
        if _MF:   # FAMILIAS: deriva de la variante presente (SIN sorteo), cambio de UNA familia y muestreo del anillo
            _ip=(t//deriva)%fam_V
            if _ip!=_ipa:
                _ipa=_ip
                for _x in list(objs):
                    if _FA['var'][objs[_x]]>=0: objs[_x]='T%dv%d'%(_FA['fam'][objs[_x]],_ip)   # los objetos de la variante que sale pasan a la que entra
                tipos[:]=list(_FA['pres'][_ip])   # len(tipos) NO cambia nunca: el sorteo de spawn() es el mismo
            if t==_tcam:
                for _n2,_v2 in _FA['val_post'].items(): val[_n2]=_v2   # la excepcion de T0 conserva su valencia ABSOLUTA
            if t%1000==0 and objs: _fv[q(t)].append(sum(1 for _y in objs.values() if val[_y]=='veneno')/len(objs))
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
            _wt=_wf+_ws if puerta is None else (_wf if _fam(kc) else _ws)   # v13: valor total (sin puerta: suma; con puerta: la rapida si le es familiar)
            Vb=alpha*_wt+hambre_boca*hambre+.5; pb=1/(1+np.exp(-Vb/.3)); mordio=rng.random()<pb
            vis[kk][q(t)]+=1
            sobre[val[kk]][q(t)]+=1; llegadas[val[kk]][q(t)]+=int(_prev_on!=pos)
            if _MF and _prev_on!=pos:   # FAMILIAS: EXPOSICIONES por patron, exp_asoc, ruta, primera y ULTIMA visita (SOLO LECTURA)
                _enc[kk]=_enc.get(kk,0)+1; _rut[0 if _fam(kc) else 1]+=1
                _o0=(1.0 if val[kk]=='comida' else (-1.0 if val[kk]=='veneno' else 0.0))
                if kk not in _prim: _prim[kk]=[t,round(float(_wt),3),_o0]
                if _o0 and kk not in _exp and _wt*_o0>0 and abs(_wt)>=crit_exp: _exp[kk]=_enc[kk]
                _ult[kk]=[t,round(float(_wt),3),_o0]
                if reg_b2:   # B2: CONDUCTA de la boca (nunca pesos: ERR-44). `mordio` ya esta decidido arriba; `valor` no consume rng.
                    if kk not in _pb2: _pb2[kk]=[t,round(float(_wt),3),_o0,int(bool(_fam(kc))),int(bool(mordio)),round(float(hambre),3),round(float(_ws),3),round(float(_wf),3)]
                    if t>=_tcam:
                        _en2[kk]=_en2.get(kk,0)+1
                        if kk in _vir and kk not in _sep and _o0 and _wt*_o0>0 and abs(_wt)>=crit_exp:
                            _vh=[float(valor(PAT[_h])) for _h in _FA['herm'][kk]]   # SEPARACION: signo distinto al de >= 2 de sus 3 hermanas
                            if sum(1 for _z in _vh if _z*_wt<=0)>=2: _sep[kk]=_en2[kk]
            if memoria_rechazo and not mordio: _rech[pos]=t+memoria_rechazo   # v9: la boca rechazo -> no es objetivo por un tiempo
            if _MF and not mordio and val[kk]=='comida' and any(_t3<t<=_t3+vent and kk in _FA['herm'][_e3] for _e3,_t3 in _texc.items()): _omi+=1   # FAMILIAS: OMISION (hermano comestible rechazado en ventana abierta)
            if renov and not mordio and (renov>=1.0 or rng.random()<renov):   # RENOVACION SIMETRICA (DIAG_mundo bloqueo 3): lo rechazado tambien desaparece
                _nren+=1; del objs[pos]; spawn(); _rech.pop(pos,None)
            if mordio:
                R=R_VAL[val[kk]]; E=min(E+E_VAL[val[kk]],1.5); mord[kk][q(t)]+=1
                if _MF:   # FAMILIAS: la ventana la abre la PRIMERA mordida del estimulo de exc_win, exista o no la excepcion (asi `lineal` tiene la MISMA ventana)
                    if kk in _FA['herm'] and kk not in _texc: _texc[kk]=t
                    if val[kk]=='veneno':
                        for _e3,_t3 in _texc.items():
                            if _t3<t<=_t3+vent and kk in _FA['herm'][_e3]: _col+=1; break
                _ky=_key(kc)
                if _ky not in ncod: _ord.append(_ky)
                ncod[_ky]=ncod.get(_ky,0)+1   # B: evidencia del codigo exacto
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
                                    if R>0: Wp[j]=Wp[c]; Wn[j]=0.; Wp[c]=0.
                                    elif R<0: Wn[j]=Wn[c]; Wp[j]=0.; Wn[c]=0.
                                    else: Wp[j]=0.; Wn[j]=0.; _ndes+=1; _des_t.append((t,kk))   # B-5: con R==0 la hija nace SIN valor (no hay signo nuevo que llevarse) y la madre conserva el suyo
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
        if log_cada and t%log_cada==0: log.append((t,)+tuple(round(valor(PAT[k]),2) for k in (sorted(PAT) if _MF else 'ABCD')))
    W={k:round(valor(PAT[k]),2) for k in PAT}   # v13: valor total
    W_lenta={k:round(float((Wps-Wns)@PAT[k]),3) for k in PAT}   # v13: lectura de la via lenta sola
    comp={k:(round(float(Wp@kenyon(PAT[k])),2),round(float(Wn@kenyon(PAT[k])),2)) for k in PAT}
    _wv=([round(float(abs(Wps[_i]-Wns[_i])),3) for _i in range(_D-fam_nvar,_D)] if _MF else [])
    _ext=(dict(mundo=mundo,
               fam=dict(D=_D,n_var=fam_nvar,F=fam_F,V=fam_V,n_exc=n_exc,n_neu=n_neu,fam_val=fam_val,deriva=deriva,
                        cambio=_tcam,renov=renov,vent=vent,crit_exp=crit_exp,nobj=nobj,L=L,NK=NK,NKMAX=NKMAX,K=K),
               val_mundo=dict(_FA['val']),exc=list(_FA['exc']),exc_win=list(_FA['exc_win']),
               herm={_a:list(_b) for _a,_b in _FA['herm'].items()},
               cod0=dict(_cod0),cod_fin={_a:sorted(code(PAT[_a])) for _a in sorted(PAT)},
               exposiciones=dict(_enc),exp_asoc=dict(_exp),primera=dict(_prim),ultima=dict(_ult),
               ruta=list(_rut),colateral=_col,omision=_omi,colateral_tot=_col+_omi,t_exc=dict(_texc),
               w_var=_wv,w_var_med=(round(float(np.median(_wv)),3) if _wv else None),renovados=_nren,
               frac_veneno=[(round(float(np.mean(_x)),3) if _x else None) for _x in _fv],
               frac_regalo=round(0.6*deaths/max(T*costo,1e-9),4)) if _MF else {})   # FAMILIAS: claves nuevas SOLO si mundo!='AB'
    if _MF and reg_b2: _ext.update(reg_b2=1,vira=int(vira),exc_evita=int(exc_evita),cambio_b2=_tcam,log_cada=log_cada,viradas=list(_FA['viradas']),val_post=dict(_FA['val_post']),primera_b2=dict(_pb2),sep_exp=dict(_sep),enc_post=dict(_en2))   # B2: claves nuevas SOLO con reg_b2=1 (identidad)
    return dict(desambiguar=desambiguar,des_splits=_ndes,des_t=_des_t,sobre=sobre,llegadas=llegadas,sin_objetivo=sin_objetivo,memoria_rechazo=memoria_rechazo,err_max=err_max,t_conflicto=t_conflicto,t_techo=t_techo,n_techo=n_techo,split_t=split_t,mord=mord,vis=vis,W=W,comp=comp,deaths=deaths,log=log,splits=splits,celdas=int(activa.sum()),puerta_pat=puerta_pat,pat_shuf=pat_shuf,pat_min=pat_min,n_cod=len(ncod),
                solap=({'AB':None,'nB':None} if _MF else {'AB':len(code(PAT['A'])&code(PAT['B'])),'nB':len(code(PAT[nuevo])&code(PAT['B'])) if nuevo else None}),W_lenta=W_lenta,Wps=[round(float(x),3) for x in Wps],Wns=[round(float(x),3) for x in Wns],**_ext)
