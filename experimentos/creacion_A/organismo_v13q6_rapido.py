"""
organismo_v13q6 RAPIDO — gemelo COMPILADO (numba) de experimentos/creacion_A/organismo_v13q6.py (b37aa8124c89cc5f).
Arnes: identidad_v13q6_rapido.py (regla 9 de registro/EQUIPO.md: si no da 100 %, este archivo no confirma nada).

NO contiene ningun bucle propio: DELEGA el nucleo compilado en organismo_v13q5_rapido._bucle, el gemelo de
organismo_v13q5 (fae9c32b146fdbb4) ya validado 239/239 contra el original interpretado. Lo unico que cambia entre
v13q5 y v13q6 vive en la capa de Python — la particion del mundo de regla —, asi que el kernel es LITERALMENTE el
mismo objeto compilado.

Por que delegar y no copiar el bucle (mismo criterio que organismo/organismo_v14_rapido.py):
  - IDENTIDAD: no hay dos copias del kernel que puedan divergir.
  - MISMA CACHE NUMBA: se reutiliza la de organismo_v13q5_rapido (__pycache__/*.nbi/*.nbc de ese modulo); una copia
    generaria un segundo juego de caches y una segunda compilacion de ~25 s.
  - Las guardias heredadas (log_cada no compilado, invertir_en solo en 'AB', `nuevo` antes de `invertir_en`) y los
    mensajes de error siguen valiendo tal cual.

Que anade v13q6 sobre v13q5 — las CINCO anclas de construye_v13q6.py, aplicadas aqui una a una sobre el wrapper de
Python de organismo_v13q5_rapido.py (todo lo demas es ese archivo, linea por linea):
  1. `def split_regla(seed, regla, ntr_ovr=None)`                       (firma de split_regla)
  2. `if ntr_ovr is not None: ntr = (int(ntr_ovr[0]), int(ntr_ovr[1]))` DESPUES de las ramas, antes de `food = ...`
  3. `... ,lab=False,ntr=None):`                                        (firma de run)
  4. `split_regla(seed,regla,ntr)` dentro de run                        (la llamada)
  5. `return dict(ntr=ntr,lab=lab,...)`                                 (constancia del ntr pedido)
Con `ntr=None` (por defecto) es organismo_v13q5_rapido EXACTO en todas SUS claves (identidad obligatoria, ETAPA 1
del arnes), y el unico anadido al return es la clave `ntr`.

AVISO heredado del constructor (trampa 3 de EQUIPO.md): mover `ntr` cambia el MUNDO, no la regla. Al subir el tren
baja el test. Con valores grandes el test puede quedarse con una sola clase o casi vacio (p. ej. xor01 tiene 12
comida y 8 veneno entre los 20 patrones de 3 px, asi que ntr=(11,9) deja el test en 1 patron y ntr=(14,6) en 2, los
dos de veneno). El gemelo reproduce eso EXACTAMENTE, como debe; interpretarlo es del preregistro, no del gemelo.

Restricciones (heredadas, el original manda): log_cada debe ser None; invertir_en solo con mundo='AB'; `nuevo` antes
de `invertir_en` no se admite.
"""
import os
import sys

import numpy as np

try:
    import organismo_v13q5_rapido as _G          # el gemelo YA VALIDADO: de aqui sale el nucleo compilado
except ImportError:                              # el directorio propio no estaba en sys.path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))   # al FINAL: no puede tapar a organismo/ (ERR-28)
    import organismo_v13q5_rapido as _G

# el mismo mundo y las mismas constantes que organismo_v13q6.py / organismo_v13q5_rapido.py
L = _G.L; NK = _G.NK; NKMAX = _G.NKMAX; K = _G.K
PAT = _G.PAT; R_VAL = _G.R_VAL; E_VAL = _G.E_VAL
patrones_regla = _G.patrones_regla               # v9g: los C(6,3)=20 patrones de 6 px con 3 px activos
_bucle = _G._bucle                               # NUCLEO COMPILADO (njit, cache=True) — no se recompila nada aqui


def split_regla(seed, regla, ntr_ovr=None):   # creacion_A A-6: `ntr_ovr` sobreescribe el tamano del tren (None = el de siempre)
    """v9g: valencias por regla y particion train/test con RNG propios (no tocan el RNG del organismo). (identico)"""
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
    if ntr_ovr is not None: ntr = (int(ntr_ovr[0]), int(ntr_ovr[1]))   # creacion_A A-6: DESPUES de las ramas, para que no lo pisen
    food = [k for k in nombres if vr[k] == 'comida']; pois = [k for k in nombres if vr[k] == 'veneno']
    r = np.random.default_rng(10000 + seed); fi = r.permutation(len(food)); pi = r.permutation(len(pois))
    food = [food[i] for i in fi]; pois = [pois[i] for i in pi]
    tren = sorted(food[:ntr[0]] + pois[:ntr[1]]); test = sorted(food[ntr[0]:] + pois[ntr[1]:])
    return pats, tren, test, vr


def run(seed,T=100000,learn=True,invertir_en=None,nuevo=None,nuevo_en=50000,nuevo_val='veneno',solap_B=None,
        eta=.03,tau_e=.85,alpha=1.2,hambre_boca=2.0,aversion=1.0,costo=.002,nobj=4,log_cada=None,plast=True,theta=0.6,ema=0.02,paso=0.5,solap_AB=None,lam=0.05,memoria_rechazo=20,mu_norm=True,div_signo=True,eta_s=0.0,clip_s=3.0,puerta=None,mundo='AB',regla='px0',fase2_en=None,sonda_final=False,lectura='lineal',regla_lenta='dos_canales',constante=False,lam_lenta=0.002,seleccion=None,sel_theta=0.6,sel_rho=0.05,sel_cupo=1,sel_calienta=0,sel_estad='cond',lab=False,ntr=None):
    if log_cada:
        raise ValueError("organismo_v13q6_rapido: log_cada no esta compilado; usa organismo_v13q6 para eso")
    if regla_lenta not in ('dos_canales','delta_signo'): raise ValueError(f"regla_lenta={regla_lenta!r}")   # 3d: un knob mal escrito NO puede caer en silencio al brazo original
    if lectura not in ('lineal','cuadratica','random15','oraculo01','oraculo01_ruido'): raise ValueError(f"lectura={lectura!r}")   # 3e: idem para la lectura
    if mundo=='AB': P_=PAT; tren=['A','B']; test=[]   # v13g: con 'AB' es v13 exacto
    else: P_,tren,test,val_regla=split_regla(seed,regla,ntr); fase2_en=T//2 if fase2_en is None else fase2_en   # creacion_A A-6
    rng=np.random.default_rng(seed)
    # --- inicializacion: EXACTAMENTE las lineas del original (mismo flujo de azar) ---
    Wl=rng.uniform(.1,.4,(2,9)); KW=np.zeros((NKMAX,6)); activa=np.zeros(NKMAX,bool); KW[:NK]=rng.uniform(0,1,(NK,6)); activa[:NK]=True
    def code(P):
        v=KW@P; v=np.where(activa,v,-1e9); return set(np.argsort(v)[-K:])
    objetivo_AB=0 if solap_AB is None else solap_AB
    if solap_AB: KW[:solap_AB]=0; KW[:solap_AB,0]=5.0
    cond=lambda: len(code(P_['A'])&code(P_['B']))==objetivo_AB and (nuevo is None or solap_B is None or (len(code(P_[nuevo])&code(P_['B']))==solap_B and len(code(P_[nuevo])&code(P_['A']))==0))
    while mundo=='AB' and not cond(): KW[objetivo_AB:NK]=rng.uniform(0,1,(NK-objetivo_AB,6))
    _NF=(6 if lectura=='lineal' else 3 if lectura in ('oraculo01','oraculo01_ruido') else 21)+(1 if constante else 0)   # xor: lineal = 6 px; cuadratica = 6 px + 15 productos; random15 = 6 px + 15 bits al azar; 3e: oraculo = 3 rasgos; 3d: +1 si constante
    if seleccion not in (None,'wta'): raise ValueError(f"seleccion={seleccion!r}")   # creacion_A: un knob mal escrito NO puede caer en silencio al brazo original
    if sel_estad not in ('cond','cov'): raise ValueError(f"sel_estad={sel_estad!r}")
    _e4=np.zeros(_NF); _ab4=np.ones(_NF,bool); _cand4=np.zeros(_NF,bool)   # creacion_A A-1(ii): elegibilidad, bit de abierto, mascara de candidatos
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
    def phi(P):   # 3d: constante=True anade 1 entrada fija en 1.0 al final (phi' de C)
        if lectura=='lineal': _b=P
        elif lectura=='cuadratica': _b=np.concatenate([P,[P[i]*P[j] for i,j in _IJ]])
        elif lectura=='oraculo01': _b=np.array([P[0],P[1],P[0]*P[1]])   # 3e: la base EXACTA de xor01 (3 rasgos)
        elif lectura=='oraculo01_ruido': _b=np.array([P[0],P[1],P[2]*P[3]])   # 3e: control, mismo tamano, el producto equivocado
        else: _b=np.concatenate([P,_R15[tuple(float(v) for v in P)]])
        return np.concatenate([_b,[1.0]]) if constante else _b
    # --- lo que el bucle compilado necesita como arrays ---
    NOMS=list(P_)                                                  # orden de insercion del dict del original
    IDX={k:i for i,k in enumerate(NOMS)}; npat=len(NOMS)
    PATM=np.array([P_[k] for k in NOMS], float)
    PHIM=np.array([np.asarray(phi(P_[k]), float) for k in NOMS], float)   # phi es fija por patron (con la constante ya dentro)
    assert PHIM.shape[1]==_NF
    val={'A':'comida','B':'veneno'} if mundo=='AB' else dict(val_regla)
    valc=np.zeros(npat,np.int64)
    for k,v in val.items(): valc[IDX[k]] = 1 if v=='comida' else -1
    tipos=np.zeros(npat+2,np.int64)
    for i,k in enumerate(tren): tipos[i]=IDX[k]
    ntipos0=len(tren)
    test_idx=np.array([IDX[k] for k in test],np.int64) if test else np.zeros(0,np.int64)
    if invertir_en is not None and mundo != 'AB':
        raise ValueError("el original solo invierte en mundo='AB' (val se reemplaza por {'A','B'} y el mundo de regla revienta)")
    if invertir_en is not None and nuevo is not None and nuevo_en < invertir_en:
        raise ValueError("el original no admite nuevo antes de invertir (val se reemplaza)")
    _nevmax=int(T) if lab else 0                                   # v13q5: cota dura (una actualizacion de la via lenta por paso, como mucho)
    ev_t=np.zeros(_nevmax,np.int64); ev_k=np.zeros(_nevmax,np.int64); ev_R=np.zeros(_nevmax); ev_ds=np.zeros(_nevmax)
    (Wp, Wn, Wps, Wns, Ws, KW, activa, splits, st_t, st_k, mord, vis, sobre, llegadas, sin_objetivo, deaths, err_max,
     t_conflicto, t_techo, n_techo, _Wp2, _Wn2, _Wps2, _Wns2, _Ws2, _KW2, _act2, f2_ok, pr_set, pr_t, pr_W, pr_pb, pr_h, pr_m,
     _e4, _ab4, ab_t, ab_j, ab_e, ab_n, _nsel4, _nev) = _bucle(
        rng, int(T), bool(learn), -1 if invertir_en is None else int(invertir_en),
        IDX.get('A', -1), IDX.get('B', -1), -1 if nuevo is None else IDX[nuevo], int(nuevo_en),
        1 if nuevo_val == 'comida' else -1, bool(mundo != 'AB'), -1 if fase2_en is None else int(fase2_en), test_idx,
        float(eta), float(tau_e), float(alpha), float(hambre_boca), float(aversion), float(costo), int(nobj),
        bool(plast), float(theta), float(ema), float(paso), float(lam), int(memoria_rechazo), bool(mu_norm),
        bool(div_signo), float(eta_s), float(clip_s), -1 if puerta is None else int(puerta),
        Wl, KW, activa, PATM, PHIM, valc, tipos, int(ntipos0),
        bool(regla_lenta == 'delta_signo'), float(lam_lenta), bool(seleccion is not None), bool(sel_estad == 'cov'),
        float(sel_theta), float(sel_rho), int(sel_cupo), int(sel_calienta), _cand4, _ab4,
        bool(lab), ev_t, ev_k, ev_R, ev_ds)
    # --- lecturas de cierre: EXACTAMENTE el codigo del original ---
    def kenyon(P): k=np.zeros(NKMAX); k[list(code(P))]=1; return k
    def lenta(P):   # 3d: lectura de la via lenta sola segun regla_lenta ('dos_canales' = la formula original, exacta)
        _ph=phi(P); return float(Ws@_ph) if regla_lenta=='delta_signo' else float((Wps-Wns)@_ph)
    def valor(P):   # v13: el valor que usa la boca
        _k=kenyon(P); _f=float((Wp-Wn)@_k); _s=lenta(P)
        return _f+_s if puerta is None else (_f if int((np.abs((Wp-Wn)[_k>0])>0.2).sum())>=puerta else _s)
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
    # --- la sonda de fase2_en, sobre la FOTO que saco el bucle. Alcance propio para no tapar el code/valor/lenta de
    #     cierre: dentro son EXACTAMENTE las lineas del original, con el estado del instante t==fase2_en ---
    def _sonda_f2():
        Wp, Wn, Wps, Wns, Ws, KW, activa = _Wp2, _Wn2, _Wps2, _Wns2, _Ws2, _KW2, _act2
        def code(P):
            v=KW@P; v=np.where(activa,v,-1e9); return set(np.argsort(v)[-K:])
        def kenyon(P): k=np.zeros(NKMAX); k[list(code(P))]=1; return k
        def lenta(P):
            _ph=phi(P); return float(Ws@_ph) if regla_lenta=='delta_signo' else float((Wps-Wns)@_ph)
        def _wvec():   # 3d: vector con signo VIGENTE de la via lenta
            return Ws if regla_lenta=='delta_signo' else (Wps-Wns)
        def valor(P):
            _k=kenyon(P); _f=float((Wp-Wn)@_k); _s=lenta(P)
            return _f+_s if puerta is None else (_f if int((np.abs((Wp-Wn)[_k>0])>0.2).sum())>=puerta else _s)
        return ({_k:valor(P_[_k]) for _k in P_},
                {_k:lenta(P_[_k]) for _k in P_},   # 3b: la via lenta sola (3d: Ws@phi' si delta_signo)
                [float(_x) for _x in _wvec()],     # 3d: Ws_apriori
                {_k:(bool(int((np.abs((Wp-Wn)[kenyon(P_[_k])>0])>0.2).sum())>=puerta) if puerta is not None else False) for _k in P_},   # 3b: ¿la puerta lee la rapida?
                {_k:sorted(int(_i) for _i in code(P_[_k])) for _k in P_})
    W_apriori=W_lenta_apriori=familiar_apriori=codigos_f2=None; Ws_apriori=None   # v13g/3b/3d
    if f2_ok: W_apriori, W_lenta_apriori, Ws_apriori, familiar_apriori, codigos_f2 = _sonda_f2()
    primer={} if not f2_ok else {k:(dict(t=int(pr_t[IDX[k]]),W=float(pr_W[IDX[k]]),pb=float(pr_pb[IDX[k]]),
                                        hambre=float(pr_h[IDX[k]]),mordio=bool(pr_m[IDX[k]])) if pr_set[IDX[k]] else None)
                                  for k in test}
    _abre4=[(int(ab_t[_i]),int(ab_j[_i]),round(float(ab_e[_i]),4),int(ab_n[_i])) for _i in range(len(ab_t))]   # A-1(ii)
    _ev5=[(int(ev_t[_i]),NOMS[int(ev_k[_i])],float(ev_R[_i]),float(ev_ds[_i])) for _i in range(int(_nev))]     # v13q5: `lab`
    return dict(ntr=ntr,lab=lab,lenta_eventos=_ev5,fase2_en=fase2_en,seleccion=seleccion,sel_estad=sel_estad,sel_theta=sel_theta,sel_rho=sel_rho,sel_cupo=sel_cupo,
                sel_abre=_abre4,sel_abiertos=[int(_i) for _i in np.where(_ab4&_cand4)[0]],
                sel_e=[round(float(_x),4) for _x in _e4],sel_n=int(_nsel4),
                sobre={'veneno':[int(v) for v in sobre[0]],'comida':[int(v) for v in sobre[1]]},
                llegadas={'veneno':[int(v) for v in llegadas[0]],'comida':[int(v) for v in llegadas[1]]},
                sin_objetivo=[int(v) for v in sin_objetivo],memoria_rechazo=memoria_rechazo,err_max=float(err_max),
                t_conflicto=None if t_conflicto<0 else int(t_conflicto),t_techo=None if t_techo<0 else int(t_techo),n_techo=int(n_techo),
                split_t=[(int(a),NOMS[int(b)]) for a,b in zip(st_t,st_k)],
                mord={k:[int(v) for v in mord[IDX[k]]] for k in P_},vis={k:[int(v) for v in vis[IDX[k]]] for k in P_},
                W=W,comp=comp,deaths=int(deaths),log=[],splits=int(splits),celdas=int(activa.sum()),
                solap=None if mundo!='AB' else {'AB':len(code(P_['A'])&code(P_['B'])),'nB':len(code(P_[nuevo])&code(P_['B'])) if nuevo else None},
                W_lenta=W_lenta,Wps=[round(float(x),3) for x in Wps],Wns=[round(float(x),3) for x in Wns],
                Ws=[round(float(x),3) for x in Ws],Ws_apriori=Ws_apriori,regla_lenta=regla_lenta,constante=constante,lam_lenta=lam_lenta,
                mundo=mundo,regla=regla,tren=tren,test=test,W_apriori=W_apriori,W_lenta_apriori=W_lenta_apriori,familiar_apriori=familiar_apriori,codigos_f2=codigos_f2,primer=primer,
                W_final=({_k:valor(P_[_k]) for _k in P_} if mundo!='AB' else None),sonda=_sonda,codigos_fin=_cod_fin)
