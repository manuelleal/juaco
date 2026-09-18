"""organismo_g3 = organismo_v13q5.py (fae9c32b146fdbb4) + perilla `memoria` (MINI-EQUIPO 3 de la sala de enjambre;
mecanismo M3 -- MEMORIA DE UN GOLPE POR COMBINACION): cada una de las 15 celdas de DOS canales (todos los
pares de los 6 pixeles binarios de la retina) escribe, DE UN GOLPE en la primera mordida que ve esa
combinacion de 2 bits, el valor R que recibio (BTSP, Bittner et al. 2017; Milstein et al. 2024; OnlineHD,
Hernandez-Cano et al. 2021); sin repeticion, sin gradiente, sin tasa de aprendizaje. Gana y lee la boca la
celda de MENOR error propio (media movil de (R-prediccion)^2); una combinacion nunca vista se ABSTIENE
devolviendo 0.0. `memoria='combi'` promedia con `mem_alfa` tras la primera escritura; `memoria='combi1'`
se queda con el PRIMER valor, para siempre (binario literal, Milstein 2024).
Generado por experimentos/enjambre/grupo3/construye_grupo3.py. NO editar a mano.
Con memoria=None es organismo_v13q5.py EXACTO (identidad obligatoria: identidad_g3.py)."""
"""organismo_v13q5 = organismo_v13q4.py (3cc732dd2b2519cd) + perilla `lab` (registro del flujo de encuentros de la via
lenta: (t, patron, R, residuo) por mordida, y el paso de la sonda). Sirve para el CONTROL POSITIVO: repetir
ESE flujo fuera del organismo con minimos cuadrados exactos, gradiente o retropropagacion.
Generado por experimentos/creacion_A/construye_v13q5.py. NO editar a mano.
Con lab=False es organismo_v13q4 EXACTO (y con seleccion=None, organismo_v13q3 exacto)."""
"""organismo_v13q4 = organismo_v13q3.py (aaebe073308a40c2) + perilla `seleccion` (A-1 ii del CREADOR A):
cascade-correlation local sobre los rasgos conjuntivos de la via lenta. Knobs: seleccion=None|'wta',
sel_theta, sel_rho, sel_cupo, sel_calienta, sel_estad='cond'|'cov'.
Generado por experimentos/creacion_A/construye_v13q4.py. NO editar a mano.
Con seleccion=None es organismo_v13q3 EXACTO (identidad obligatoria: identidad_v13q4.py)."""
"""organismo_v13q3 = organismo_v13q.py (0b59eb03858df3a8) + regla fusionada del trio XOR (bloque 3d) +
lecturas oraculo del bloque 3e. Knobs: regla_lenta='dos_canales'|'delta_signo', constante=False|True,
lam_lenta (decaimiento por actualizacion), lectura=...|'oraculo01'|'oraculo01_ruido'.
Generado por construye_xor_3d.py. NO editar. Con regla_lenta='dos_canales' y constante=False es organismo_v13q
exacto en todas las claves del original (identidad obligatoria, ETAPA 1 de corre_xor_3d.py)."""
"""organismo_v13q = organismo_v13g.py (2a80e125f8593bf2) + knob lectura de la via lenta (lineal | cuadratica | random15).
Generado por construye_xor.py. NO editar. Con lectura='lineal' es organismo_v13g exacto (identidad obligatoria)."""
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
        eta=.03,tau_e=.85,alpha=1.2,hambre_boca=2.0,aversion=1.0,costo=.002,nobj=4,log_cada=None,plast=True,theta=0.6,ema=0.02,paso=0.5,solap_AB=None,lam=0.05,memoria_rechazo=20,mu_norm=True,div_signo=True,eta_s=0.0,clip_s=3.0,puerta=None,mundo='AB',regla='px0',fase2_en=None,sonda_final=False,lectura='lineal',regla_lenta='dos_canales',constante=False,lam_lenta=0.002,seleccion=None,sel_theta=0.6,sel_rho=0.05,sel_cupo=1,sel_calienta=0,sel_estad='cond',lab=False,memoria=None,mem_alfa=0.3,mem_rho=0.02):   # xor: lectura de la via lenta; 3d: regla de la via lenta, termino constante y decaimiento; creacion_A A-1(ii): seleccion de rasgos conjuntivos por competencia
    if regla_lenta not in ('dos_canales','delta_signo'): raise ValueError(f"regla_lenta={regla_lenta!r}")   # 3d: un knob mal escrito NO puede caer en silencio al brazo original
    if lectura not in ('lineal','cuadratica','random15','oraculo01','oraculo01_ruido'): raise ValueError(f"lectura={lectura!r}")   # 3e: idem para la lectura
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
    _NF=(6 if lectura=='lineal' else 3 if lectura in ('oraculo01','oraculo01_ruido') else 21)+(1 if constante else 0)   # xor: lineal = 6 px; cuadratica = 6 px + 15 productos; random15 = 6 px + 15 bits al azar; 3e: oraculo = 3 rasgos; 3d: +1 si constante
    Wps=np.zeros(_NF); Wns=np.zeros(_NF)   # v13: via LENTA sobre phi(P) (con lectura='lineal' es v13g exacto)
    if memoria not in (None,'combi','combi1'): raise ValueError(f"memoria={memoria!r}")   # M3: perilla mal escrita no cae en silencio
    _PAR=[(i,j) for i in range(6) for j in range(i+1,6)]   # M3: las 15 celdas de dos canales (pares de pixeles binarios)
    _MM=np.zeros((15,4))   # M3: valor escrito por celda x combinacion (P_i,P_j) in 00,01,10,11
    _MN=np.zeros((15,4))   # M3: veces visitada esa celda x combinacion (0 = abstencion explicita)
    _ME=np.full(15,1e9)   # M3: error propio de cada celda (media movil de (R-prediccion)^2); gana la de menor error
    _MG=0   # M3: celda ganadora vigente (indice en _PAR); la que lee la boca
    Ws=np.zeros(_NF)   # 3d: vector con signo de la via lenta; solo se mueve/lee si regla_lenta=='delta_signo'
    if seleccion not in (None,'wta'): raise ValueError(f"seleccion={seleccion!r}")   # creacion_A: un knob mal escrito NO puede caer en silencio al brazo original
    if sel_estad not in ('cond','cov'): raise ValueError(f"sel_estad={sel_estad!r}")
    _ev5=[]   # creacion_A (control positivo): (t, patron, R) de cada actualizacion de la via lenta; solo se graba si lab=True
    _e4=np.zeros(_NF); _ab4=np.ones(_NF,bool); _cand4=np.zeros(_NF,bool); _abre4=[]; _nsel4=0   # creacion_A A-1(ii): elegibilidad, bit de abierto, mascara de candidatos, historia de aperturas, contador de mordidas
    if seleccion is not None:
        _npx4=2 if lectura in ('oraculo01','oraculo01_ruido') else 6   # elementales: los pixeles (P0,P1 en el oraculo)
        _ncj4=0 if lectura=='lineal' else (1 if lectura in ('oraculo01','oraculo01_ruido') else 15)   # candidatos: los productos (o los 15 bits de random15, como control)
        _cand4[_npx4:_npx4+_ncj4]=True; _ab4=~_cand4   # elementales y constante ABIERTOS; conjuntivos CERRADOS
    _IJ=[(i,j) for i in range(6) for j in range(i+1,6)]
    _R15={}
    if lectura=='random15':
        _rr=np.random.default_rng(seed+900000)   # RNG propio: no toca el del organismo
        for _n in range(64):
            _Pb=tuple(float((_n>>(5-_j))&1) for _j in range(6)); _R15[_Pb]=_rr.integers(0,2,15).astype(float)
    def phi(P):   # 3d: constante=True anade 1 entrada fija en 1.0 al final (phi' de C). Con constante=False devuelve exactamente lo de antes
        if lectura=='lineal': _b=P
        elif lectura=='cuadratica': _b=np.concatenate([P,[P[i]*P[j] for i,j in _IJ]])
        elif lectura=='oraculo01': _b=np.array([P[0],P[1],P[0]*P[1]])   # 3e: la base EXACTA de xor01 (3 rasgos)
        elif lectura=='oraculo01_ruido': _b=np.array([P[0],P[1],P[2]*P[3]])   # 3e: control, mismo tamano, el producto equivocado
        else: _b=np.concatenate([P,_R15[tuple(float(v) for v in P)]])
        return np.concatenate([_b,[1.0]]) if constante else _b
    def lenta(P):   # 3d: lectura de la via lenta sola segun regla_lenta ('dos_canales' = la formula original, exacta)
        if memoria is not None: _i,_j=_PAR[_MG]; _c=int(P[_i])*2+int(P[_j]); return float(_MM[_MG,_c]) if _MN[_MG,_c]>0 else 0.0   # M3: lectura de la celda ganadora, abstencion explicita
        _ph=phi(P); return float(Ws@_ph) if regla_lenta=='delta_signo' else float((Wps-Wns)@_ph)
    def _wvec():   # 3d: vector con signo VIGENTE de la via lenta (mecanismo: marginales y producto en la sonda)
        return Ws if regla_lenta=='delta_signo' else (Wps-Wns)
    def valor(P):   # v13: el valor que usa la boca. Sin puerta: rapida+lenta (un error). Con puerta: la rapida si el patron le es FAMILIAR, si no la lenta
        _k=kenyon(P); _f=float((Wp-Wn)@_k); _s=lenta(P)
        return _f+_s if puerta is None else (_f if int((np.abs((Wp-Wn)[_k>0])>0.2).sum())>=puerta else _s)   # familiar = >= puerta celdas del codigo con valor consolidado (|W|>0.2, el mismo umbral de v11)
    pos=0; E=1.0; objs={}; val={'A':'comida','B':'veneno'} if mundo=='AB' else dict(val_regla)
    err_max=0.0; t_conflicto=None; t_techo=None; n_techo=0   # instrumentacion v8, solo lectura
    _rech={}; _prev_on=-1   # v9: memoria de trabajo de rechazo (posicion -> paso hasta el que no es objetivo)
    sobre={'veneno':[0]*4,'comida':[0]*4}; llegadas={'veneno':[0]*4,'comida':[0]*4}; sin_objetivo=[0]*4   # v9: lectura
    tipos=['A','B'] if mundo=='AB' else list(tren)
    W_apriori=None; codigos_f2=None; primer={}   # v13g: sonda y primer encuentro (lectura)
    W_lenta_apriori=None; familiar_apriori=None   # 3b
    Ws_apriori=None   # 3d: el vector con signo vigente EN LA SONDA (los del return son los del final de T)
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
            W_lenta_apriori={_k:lenta(P_[_k]) for _k in P_}   # 3b: la via lenta sola (3d: Ws@phi' si delta_signo)
            Ws_apriori=[float(_x) for _x in _wvec()]   # 3d: lectura pura, no cambia ningun numero
            familiar_apriori={_k:(bool(int((np.abs((Wp-Wn)[kenyon(P_[_k])>0])>0.2).sum())>=puerta) if puerta is not None else False) for _k in P_}   # 3b: ¿la puerta lee la rapida?
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
            kk=objs[pos]; kc=kenyon(P_[kk]); Wb=Wp-Wn; _wf=float(Wb@kc); _ws=lenta(P_[kk])   # v13: las dos vias (xor: phi; 3d: segun regla_lenta)
            _wt=_wf+_ws if puerta is None else (_wf if int((np.abs(Wb[kc>0])>0.2).sum())>=puerta else _ws)   # v13: valor total (sin puerta: suma; con puerta: la rapida si le es familiar)
            Vb=alpha*_wt+hambre_boca*hambre+.5; pb=1/(1+np.exp(-Vb/.3)); mordio=rng.random()<pb
            vis[kk][q(t)]+=1
            sobre[val[kk]][q(t)]+=1; llegadas[val[kk]][q(t)]+=int(_prev_on!=pos)
            if kk in primer and primer[kk] is None: primer[kk]=dict(t=t,W=_wt,pb=float(pb),hambre=float(hambre),mordio=bool(mordio))   # v13g
            if memoria_rechazo and not mordio: _rech[pos]=t+memoria_rechazo   # v9: la boca rechazo -> no es objetivo por un tiempo
            if mordio:
                R=R_VAL[val[kk]]; E=min(E+E_VAL[val[kk]],1.5); mord[kk][q(t)]+=1
                del objs[pos]; spawn()
                _rech.pop(pos,None)   # v9: ese objeto ya no existe
                if learn:
                    dlt=R-_wt if puerta is None else R-_wf   # v13: sin puerta UN error compartido; con puerta cada via el suyo
                    if eta_s:   # v13: actualizacion de la via lenta (su tasa, mismo drenaje)
                        _ds=dlt if puerta is None else R-_ws
                        if lab: _ev5.append((int(t),kk,float(R),float(_ds)))   # creacion_A: LECTURA pura (no cambia ningun numero)
                        if memoria is not None:   # M3: memoria de un golpe por combinacion (BTSP; Milstein 2024; OnlineHD): las 15 celdas escriben en cada mordida, ninguna tasa
                            for _c5m in range(15):
                                _i5m,_j5m=_PAR[_c5m]; _dir5m=int(P_[kk][_i5m])*2+int(P_[kk][_j5m])
                                _p5m=float(_MM[_c5m,_dir5m]) if _MN[_c5m,_dir5m]>0 else 0.0
                                _d5m=R-_p5m; _prim5m=bool(_MN[_c5m].sum()==0)   # primera vez que ESTA celda ve cualquier combinacion
                                _ME[_c5m]=(_d5m*_d5m) if _prim5m else (1-mem_rho)*_ME[_c5m]+mem_rho*(_d5m*_d5m)
                                if _MN[_c5m,_dir5m]==0: _MM[_c5m,_dir5m]=R   # DE UN GOLPE: la primera vez que se ve ESA combinacion
                                elif memoria=='combi': _MM[_c5m,_dir5m]+=mem_alfa*(R-_MM[_c5m,_dir5m])   # 'combi1': no hace nada (binario literal, Milstein 2024)
                                _MN[_c5m,_dir5m]+=1
                            _MG=int(np.argmin(_ME))
                        elif seleccion is not None:   # creacion_A A-1(ii): elegibilidad por rasgo, competencia entre candidatos, y la via lenta aprende SOLO lo abierto
                            _ph4=phi(P_[kk]); _act4=_ph4>0; _nsel4+=1
                            if sel_estad=='cond': _e4[_act4]=(1-sel_rho)*_e4[_act4]+sel_rho*_ds   # media movil del residuo BAJO el rasgo
                            else:                 _e4=(1-sel_rho)*_e4+sel_rho*(_ds*_ph4)          # correlacion acumulada (cascade-correlation)
                            if _nsel4>=sel_calienta and int((_ab4&_cand4).sum())<sel_cupo:
                                _c4=_cand4&~_ab4
                                if _c4.any():
                                    _j4=int(np.argmax(np.where(_c4,np.abs(_e4),-1.0)))
                                    if abs(float(_e4[_j4]))>sel_theta: _ab4[_j4]=True; _abre4.append((int(t),int(_j4),round(float(_e4[_j4]),4),int(_nsel4)))
                            _phm4=_ph4*_ab4   # los cerrados no reciben error y quedan en 0
                            if regla_lenta=='delta_signo':
                                Ws=np.clip(Ws*(1-lam_lenta)+eta_s*_ds*_phm4,-clip_s,clip_s)
                            else:
                                if lam: _mcs=np.minimum(Wps,Wns)*(_phm4>0); Wps=Wps-lam*_mcs; Wns=Wns-lam*_mcs
                                if _ds>0: Wps=np.clip(Wps+eta_s*_ds*_phm4,0,clip_s)
                                else:     Wns=np.clip(Wns+eta_s*aversion*(-_ds)*_phm4,0,clip_s)
                        elif regla_lenta=='delta_signo':   # 3d (A+B+C): UN vector con signo, decaimiento multiplicativo de TODO el vector, tope simetrico. Sin aversion (todas las corridas de 3d usan aversion=1.0)
                            Ws=np.clip(Ws*(1-lam_lenta)+eta_s*_ds*phi(P_[kk]),-clip_s,clip_s)
                        else:   # 'dos_canales': la regla original de v13/v13q, sin tocar (identidad obligatoria)
                            if lam: _mcs=np.minimum(Wps,Wns)*(phi(P_[kk])>0); Wps=Wps-lam*_mcs; Wns=Wns-lam*_mcs
                            if _ds>0: Wps=np.clip(Wps+eta_s*_ds*phi(P_[kk]),0,clip_s)
                            else:     Wns=np.clip(Wns+eta_s*aversion*(-_ds)*phi(P_[kk]),0,clip_s)
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
    W_lenta={k:round(lenta(P_[k]),3) for k in P_}   # v13: lectura de la via lenta sola (xor: phi; 3d: segun regla_lenta)
    comp={k:(round(float(Wp@kenyon(P_[k])),2),round(float(Wn@kenyon(P_[k])),2)) for k in P_}
    return dict(lab=lab,lenta_eventos=_ev5,mem_ganadora=list(_PAR[_MG]),mem_tabla=[[round(float(x),3) for x in f] for f in _MM],mem_vistas=int((_MN>0).sum()),fase2_en=fase2_en,seleccion=seleccion,sel_estad=sel_estad,sel_theta=sel_theta,sel_rho=sel_rho,sel_cupo=sel_cupo,
                sel_abre=_abre4,sel_abiertos=[int(_i) for _i in np.where(_ab4&_cand4)[0]],
                sel_e=[round(float(_x),4) for _x in _e4],sel_n=int(_nsel4),sobre=sobre,llegadas=llegadas,sin_objetivo=sin_objetivo,memoria_rechazo=memoria_rechazo,err_max=err_max,t_conflicto=t_conflicto,t_techo=t_techo,n_techo=n_techo,split_t=split_t,mord=mord,vis=vis,W=W,comp=comp,deaths=deaths,log=log,splits=splits,celdas=int(activa.sum()),
                solap=None if mundo!='AB' else {'AB':len(code(P_['A'])&code(P_['B'])),'nB':len(code(P_[nuevo])&code(P_['B'])) if nuevo else None},W_lenta=W_lenta,Wps=[round(float(x),3) for x in Wps],Wns=[round(float(x),3) for x in Wns],Ws=[round(float(x),3) for x in Ws],Ws_apriori=Ws_apriori,regla_lenta=regla_lenta,constante=constante,lam_lenta=lam_lenta,mundo=mundo,regla=regla,tren=tren,test=test,W_apriori=W_apriori,W_lenta_apriori=W_lenta_apriori,familiar_apriori=familiar_apriori,codigos_f2=codigos_f2,primer=primer,W_final=({_k:valor(P_[_k]) for _k in P_} if mundo!='AB' else None),sonda=_sonda,codigos_fin=_cod_fin)
