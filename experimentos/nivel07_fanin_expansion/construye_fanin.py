"""FANIN (nivel 7, pedido del director 22-sep) — constructor POR ANCLAS de las cuatro copias del bloque.

Cambio UNICO: el numero de ENTRADAS POR CELDA de la expansion Kenyon (`fanin`, defecto 6 = el tronco, donde cada una
de las NK = 30 celdas sorteadas lee los 6 pixeles con pesos U(0,1)). Con fanin < 6 cada celda sorteada lee SOLO
`fanin` pixeles distintos, elegidos al azar con un RNG PROPIO (`default_rng(60000 + seed)`): el rng del organismo NO se
toca y consume exactamente lo mismo que el tronco (los pesos U(0,1) se sortean igual y luego se multiplican por la
mascara). Con fanin = 6 no se crea mascara ni se multiplica nada: es el tronco EXACTO (identidad_fanin.py).
Decisiones declaradas (no son perillas): (1) la mascara vale para las 30 celdas del sorteo inicial y para sus
re-sorteos en el bucle `cond()` del mundo AB (misma mascara, pesos nuevos); (2) las HIJAS nacen con la regla del
tronco sin tocar (su soporte ya lo decide `_rel`, subconjunto de los pixeles encendidos del patron que divide); (3) la
sobre-escritura de `solap_AB` (E2L: 3 celdas que leen solo el pixel 0) queda como en el tronco.
Instrumentacion `diag=False` por defecto (solo lectura, no toca el rng): empates en la frontera del "ganan K",
cobertura de pixeles, solapamiento de codigos, celdas usadas, fanin efectivo, lectura de la via rapida sola y de la
puerta en la sonda a priori.
El instrumento de mundo de regla gana ademas un mundo NUEVO `mundo='rejilla'` (63 patrones no vacios de 6 px) con las
reglas conj / np / xor / par3 / px0 / azar y particion POR VARIANTES dentro de cada fila de la tabla de verdad.

Genera (LEYENDO solo; no toca nada congelado ni ningun original), en esta carpeta:
  organismo_v142_fanin.py              <- organismo/organismo_v142.py              (17528d767fcebaf6, CONGELADO)
  organismo_v142g_fanin.py             <- organismo/organismo_v142g.py             (9e5f566cd6a7a4d2, CONGELADO)
  bateria_v142_fanin.py                <- organismo/bateria_v142.py                (6375d90e531b06e6, CONGELADA)
  bateria_generaliza_v142_fanin.py     <- organismo/bateria_generaliza_v142.py     (e5929942647756a5, CONGELADA)

Uso: python experimentos/nivel07_fanin_expansion/construye_fanin.py      (no corre nada)
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORG = os.path.join(RAIZ, 'organismo')

SHA = {   # tripwire: si un origen cambio, no se escribe nada
    'organismo_v142.py':           '17528d767fcebaf6',
    'organismo_v142g.py':          '9e5f566cd6a7a4d2',
    'bateria_v142.py':             '6375d90e531b06e6',
    'bateria_generaliza_v142.py':  'e5929942647756a5',
}


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def origen(n):
    p = os.path.join(ORG, n)
    s = h16(p)
    if s != SHA[n]:
        raise SystemExit(f'*** ORIGEN {n}: sha {s}, se esperaba {SHA[n]}. No se escribe nada.')
    return open(p, 'rb').read().decode('utf-8')


def sust(t, a, b, n=1, etq=''):
    c = t.count(a)
    if c != n:
        raise SystemExit(f'*** ancla {etq!r} aparece {c} veces, se esperaban {n}. No se escribe nada.')
    return t.replace(a, b)


# ---------------------------------------------------------------- bloques comunes a los dos organismos
KW_INI = "    Wl=rng.uniform(.1,.4,(2,9)); KW=np.zeros((NKMAX,6)); activa=np.zeros(NKMAX,bool); KW[:NK]=rng.uniform(0,1,(NK,6)); activa[:NK]=True\n"
MASCARA = KW_INI + (
    "    _MF=None   # FANIN: con fanin=6 no hay mascara (tronco EXACTO)\n"
    "    if fanin<6:   # FANIN: cada celda sorteada lee SOLO `fanin` pixeles distintos; RNG PROPIO, el rng del organismo no se toca\n"
    "        _rf=np.random.default_rng(60000+seed); _MF=np.zeros((NK,6))\n"
    "        for _c in range(NK): _MF[_c,_rf.choice(6,fanin,replace=False)]=1.\n"
    "        KW[:NK]=KW[:NK]*_MF\n")
CODE_OLD = "    def code(P):\n        v=KW@P; v=np.where(activa,v,-1e9); return set(np.argsort(v)[-K:])\n"
CODE_NEW = ("    _dg={'llamadas':0,'empates':0,'empates_cero':0,'enc_test':0,'rap_test':0,'enc_tren':0,'rap_tren':0,'enc_tren2':0,'rap_tren2':0}   # FANIN diag: empates en la frontera del 'ganan K' (solo lectura)\n"
            "    def code(P):\n        v=KW@P; v=np.where(activa,v,-1e9)\n"
            "        if diag:\n"
            "            _s=np.sort(v); _dg['llamadas']+=1\n"
            "            if _s[-K]==_s[-K-1]: _dg['empates']+=1; _dg['empates_cero']+=int(_s[-K]<=0)\n"
            "        return set(np.argsort(v)[-K:])\n")
KEN = "    def kenyon(P): k=np.zeros(NKMAX); k[list(code(P))]=1; return k\n"


def foto(pats):
    return KEN + (
        "    def _cr(P):   # FANIN diag: el mismo codigo SIN contar empates (solo lectura)\n"
        "        v=KW@P; v=np.where(activa,v,-1e9); return set(np.argsort(v)[-K:])\n"
        "    def _kenr(P): k=np.zeros(NKMAX); k[list(_cr(P))]=1; return k\n"
        "    def _foto(_pats):   # FANIN diag: empates en la frontera, solapamiento, colisiones, celdas usadas (solo lectura)\n"
        "        _ks=list(_pats); _c={k:_cr(_pats[k]) for k in _ks}; _em=0; _em0=0; _vp=[]\n"
        "        for k in _ks:\n"
        "            v=np.where(activa,KW@_pats[k],-1e9); s=np.sort(v); _em+=int(s[-K]==s[-K-1]); _em0+=int(s[-K]==s[-K-1] and s[-K]<=0)\n"
        "            _vp.append(float(((v>0)&activa).sum())/float(activa.sum()))\n"
        "        _pr=[(a,b) for i,a in enumerate(_ks) for b in _ks[i+1:]]\n"
        "        _d=lambda a,b: int(np.abs(_pats[a]-_pats[b]).sum())\n"
        "        _ov=lambda ps: (float(np.mean([len(_c[a]&_c[b])/K for a,b in ps])) if ps else None)\n"
        "        _us=set().union(*_c.values()); _M=(KW[activa]>0)\n"
        "        return dict(empates_frontera=_em/len(_ks),empates_frontera_cero=_em0/len(_ks),solap_medio=_ov(_pr),solap_d1=_ov([p for p in _pr if _d(*p)==1]),\n"
        "                    solap_d2=_ov([p for p in _pr if _d(*p)==2]),colisiones=sum(1 for a,b in _pr if _c[a]==_c[b]),pares=len(_pr),\n"
        "                    codigos_distintos=len(set(frozenset(x) for x in _c.values())),patrones=len(_ks),celdas_usadas=len(_us),\n"
        "                    celdas_activas=int(activa.sum()),frac_usadas=len(_us)/float(activa.sum()),frac_drive_pos=float(np.mean(_vp)),\n"
        "                    fanin_ef_mediana=float(np.median(_M.sum(1))),fanin_ef_max=int(_M.sum(1).max()))\n"
        "    _diag={}\n"
        "    if diag:   # FANIN diag: foto inicial (tras el sorteo y el bucle cond) + cobertura de pixeles por las 30 celdas sorteadas\n"
        "        _lec=(KW[:NK]>0).sum(0); _diag['cobertura']=dict(pixeles_leidos=int((_lec>0).sum()),lecturas_por_pixel=[int(x) for x in _lec],\n"
        f"                                                    min_lecturas=int(_lec.min()),fanin_inicial=[int(x) for x in (KW[:NK]>0).sum(1)]); _diag['ini']=_foto({pats})\n")


def organismo(t, firma_old, firma_new, cond_old, cond_new, pats, cab):
    t = sust(t, firma_old, firma_new, etq='firma')
    t = sust(t, KW_INI, MASCARA, etq='KW inicial')
    t = sust(t, CODE_OLD, CODE_NEW, etq='code')
    t = sust(t, cond_old, cond_new, etq='cond')
    t = sust(t, KEN, foto(pats), etq='kenyon')
    t = sust(t, "    return dict(desambiguar=desambiguar,",
             f"    if diag: _diag.update(fin=_foto({pats}),llamadas=_dg['llamadas'],empates=_dg['empates'],empates_cero=_dg['empates_cero'],encuentros={{_q:_dg[_q] for _q in _dg if _q[:4] in ('enc_','rap_')}})\n"
             "    return dict(fanin=fanin,diag_fanin=(_diag if diag else None),desambiguar=desambiguar,", etq='return')
    return cab + t


REJILLA = '''

def patrones_rejilla():
    """FANIN: los 63 patrones NO vacios de 6 px (el vacio no es estimulo: la retina no ve nada)."""
    pats = {}
    for n in range(1, 64):
        v = np.array([(n >> (5 - j)) & 1 for j in range(6)], float)
        pats[''.join('1' if v[j] else '0' for j in range(6))] = v
    return pats


REGLAS_REJILLA = ('conj', 'np', 'xor', 'par3', 'px0', 'azar')


def info_rejilla(seed, regla):
    """FANIN: pixeles relevantes (sorteados por semilla con RNG propio: sin sitios fijos), fila de la tabla de verdad de
    cada patron y valencia. conj = a AND b; np = patron negativo (A+, B+, AB-: el mundo NO tiene la fila 00);
    xor = a XOR b; par3 = paridad de (a, b, c); px0 = a (control lineal); azar = valencias al azar por patron, mitad y
    mitad (control de fuga; su particion usa las filas de (a, b))."""
    regla = regla.split('@')[0]   # 'xor@8' = xor con tope de 8 variantes por fila (lo aplica split_rejilla)
    rel = [int(x) for x in np.random.default_rng(70000 + seed).permutation(6)[:3]]
    a, b, c = rel
    pats = patrones_rejilla()
    bit = lambda k, i: k[i] == '1'
    if regla == 'np':
        pats = {k: v for k, v in pats.items() if bit(k, a) or bit(k, b)}
    nombres = sorted(pats)
    rp = {'conj': (a, b), 'np': (a, b), 'xor': (a, b), 'par3': (a, b, c), 'px0': (a,), 'azar': (a, b)}[regla]
    fila = {k: ''.join(k[i] for i in rp) for k in nombres}
    if regla == 'conj':
        vr = {k: ('comida' if bit(k, a) and bit(k, b) else 'veneno') for k in nombres}
    elif regla in ('np', 'xor'):
        vr = {k: ('comida' if bit(k, a) != bit(k, b) else 'veneno') for k in nombres}
    elif regla == 'par3':
        vr = {k: ('comida' if (bit(k, a) + bit(k, b) + bit(k, c)) % 2 == 1 else 'veneno') for k in nombres}
    elif regla == 'px0':
        vr = {k: ('comida' if bit(k, a) else 'veneno') for k in nombres}
    elif regla == 'azar':
        pr = np.random.default_rng(80000 + seed).permutation(len(nombres)); com = set(nombres[i] for i in pr[:len(nombres) // 2])
        vr = {k: ('comida' if k in com else 'veneno') for k in nombres}
    else:
        raise ValueError(regla)
    return pats, nombres, rel, fila, vr


def split_rejilla(seed, regla):
    """FANIN: particion POR VARIANTES dentro de cada fila (todas las filas se ven en el tren): en cada fila de la tabla
    de verdad, floor(n/2) variantes al tren y el resto al test, con RNG propio (no toca el rng del organismo)."""
    pats, nombres, rel, fila, vr = info_rejilla(seed, regla)
    tope = int(regla.split('@')[1]) if '@' in regla else None   # FANIN: tope de variantes por fila (se conservan TODAS las filas)
    r = np.random.default_rng(90000 + seed); tren = []; test = []
    for f in sorted(set(fila.values())):
        vs = [k for k in nombres if fila[k] == f]; vs = [vs[i] for i in r.permutation(len(vs))]
        if tope: vs = vs[:tope]
        tren += vs[:len(vs) // 2]; test += vs[len(vs) // 2:]
    if tope: pats = {k: pats[k] for k in tren + test}   # el mundo son solo los patrones elegidos
    return pats, sorted(tren), sorted(test), vr
'''


def main():
    # ---------------- 1. organismo del tronco (mundo AB) ----------------
    t = origen('organismo_v142.py')
    cab = ('"""organismo_v142_fanin = organismo/organismo_v142.py (17528d767fcebaf6, TRONCO v14.2 CONGELADO: solo se leyo)\n'
           '+ perilla `fanin` (entradas por celda de la expansion; defecto 6 = TRONCO EXACTO, sin mascara) + `diag` (solo lectura).\n'
           'Generado POR ANCLAS por experimentos/nivel07_fanin_expansion/construye_fanin.py. NO editar a mano."""\n')
    o1 = organismo(t, "pat_min=1,desambiguar=1):", "pat_min=1,desambiguar=1,fanin=6,diag=False):",
                   "    while not cond(): KW[objetivo_AB:NK]=rng.uniform(0,1,(NK-objetivo_AB,6))\n",
                   "    while not cond(): KW[objetivo_AB:NK]=rng.uniform(0,1,(NK-objetivo_AB,6)) if _MF is None else rng.uniform(0,1,(NK-objetivo_AB,6))*_MF[objetivo_AB:NK]   # FANIN: misma mascara, pesos nuevos\n",
                   'PAT', cab)

    # ---------------- 2. instrumento de mundo de regla (+ mundo rejilla) ----------------
    t = origen('organismo_v142g.py')
    cab = ('"""organismo_v142g_fanin = organismo/organismo_v142g.py (9e5f566cd6a7a4d2, instrumento de mundo de regla del TRONCO\n'
           'v14.2, CONGELADO: solo se leyo) + perilla `fanin` (defecto 6 = EXACTO) + `diag` (solo lectura) + MUNDO NUEVO\n'
           "`mundo='rejilla'` (63 patrones, reglas conj/np/xor/par3/px0/azar, particion por VARIANTES dentro de cada fila).\n"
           "Con mundo='AB' o 'regla' y fanin=6 es organismo_v142g EXACTO (identidad_fanin.py).\n"
           'AVISO (regla 14): sus defectos de via lenta son los de v142g (eta_s=0.0, ...): el runner pasa los kwargs del tronco.\n'
           'Generado POR ANCLAS por experimentos/nivel07_fanin_expansion/construye_fanin.py. NO editar a mano."""\n')
    t = sust(t, "\ndef run(seed,", REJILLA + "\ndef run(seed,", etq='rejilla')
    _WT = "            _wt=_wf+_ws if puerta is None else (_wf if _fam(kc) else _ws)   # v13: valor total (sin puerta: suma; con puerta: la rapida si le es familiar)\n"
    t = sust(t, _WT, _WT + "            if diag and puerta is not None:   # FANIN diag: que via decide en CADA encuentro, nunca vistos (test) y vistos (tren; tren2 = desde T/2)\n"
             "                _rp=int(_fam(kc)); _qq='test' if kk in test else 'tren'; _dg['enc_'+_qq]+=1; _dg['rap_'+_qq]+=_rp\n"
             "                if _qq=='tren' and fase2_en is not None and t>=fase2_en: _dg['enc_tren2']+=1; _dg['rap_tren2']+=_rp\n", etq='encuentro')
    t = sust(t, "    else: P_,tren,test,val_regla=split_regla(seed,regla); fase2_en",
             "    else: P_,tren,test,val_regla=(split_rejilla(seed,regla) if mundo=='rejilla' else split_regla(seed,regla)); fase2_en", etq='split')
    t = sust(t, "            codigos_f2={_k:sorted(int(_i) for _i in code(P_[_k])) for _k in P_}\n",
             "            codigos_f2={_k:sorted(int(_i) for _i in code(P_[_k])) for _k in P_}\n"
             "            if diag:   # FANIN diag: la sonda a priori por partes (solo lectura): via rapida sola, via lenta sola, puerta, alias tren/test\n"
             "                _diag['sonda']=_foto(P_); _diag['W_rapida_apriori']={_k:float((Wp-Wn)@_kenr(P_[_k])) for _k in P_}\n"
             "                _diag['W_lenta_apriori']={_k:float((Wps-Wns)@P_[_k]) for _k in P_}; _diag['familiar_apriori']={_k:bool(_fam(_kenr(P_[_k]))) for _k in P_}\n"
             "                _ctr={frozenset(_cr(P_[_k])) for _k in tren}; _diag['alias_test']={_k:(frozenset(_cr(P_[_k])) in _ctr) for _k in test}\n", etq='sonda')
    o2 = organismo(t, "pat_min=0,desambiguar=1):", "pat_min=0,desambiguar=1,fanin=6,diag=False):",
                   "    while mundo=='AB' and not cond(): KW[objetivo_AB:NK]=rng.uniform(0,1,(NK-objetivo_AB,6))\n",
                   "    while mundo=='AB' and not cond(): KW[objetivo_AB:NK]=rng.uniform(0,1,(NK-objetivo_AB,6)) if _MF is None else rng.uniform(0,1,(NK-objetivo_AB,6))*_MF[objetivo_AB:NK]   # FANIN: misma mascara, pesos nuevos\n",
                   'P_', cab)

    # ---------------- 3. bateria del examen v3' ----------------
    t = origen('bateria_v142.py')
    cab = ('"""bateria_v142_fanin = organismo/bateria_v142.py (6375d90e531b06e6, CONGELADA: solo se leyo) apuntando a\n'
           'organismo_v142_fanin con `--fanin N` (defecto 6). Etapas, CRIT y umbrales del criterio v3\' INTACTOS; la identidad\n'
           '(criterio 5) compara la copia con fanin=6 contra v11/v10 como en el tronco. Cambios: rutas (vive en\n'
           'experimentos/nivel07_fanin_expansion/: organismo_v11/v10 se leen de organismo/, ERR-42), `--pool N` (defecto 6),\n'
           '`--humo` (1 semilla, T=12000, sin Pool, JSON a datos/humo/: regla 14), nombres de salida con el fanin.\n'
           '    python bateria_v142_fanin.py 20 --desde 6001 --fanin 2 --pool 6 --log\n'
           'Generada POR ANCLAS por construye_fanin.py. NO editar a mano."""\n')
    t = sust(t, "_D14 = os.path.dirname(os.path.abspath(__file__))   # tronco: organismo/\n",
             "_D14 = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'organismo')   # FANIN: organismo/ del tronco (v11, v10)\n", etq='_D14')
    t = sust(t, "AQUI = _D14   # tronco: organismo/\n", "AQUI = os.path.dirname(os.path.abspath(__file__))   # FANIN: esta carpeta\n", etq='AQUI')
    t = sust(t, "RAIZ = os.path.dirname(AQUI)   # tronco: organismo/ -> bundle/\n",
             "RAIZ = os.path.dirname(os.path.dirname(AQUI))   # FANIN: experimentos/<carpeta>/ -> raiz\n", etq='RAIZ')
    t = sust(t, "sys.path[:0] = [_D14, AQUI,", "sys.path[:0] = [AQUI, _D14,", etq='path')
    t = sust(t, "N_PARALELO = 14\n",
             "N_PARALELO = int(sys.argv[sys.argv.index('--pool') + 1]) if '--pool' in sys.argv else 6   # FANIN\n"
             "FANIN = int(sys.argv[sys.argv.index('--fanin') + 1]) if '--fanin' in sys.argv else 6   # FANIN\n"
             "HUMO = '--humo' in sys.argv   # FANIN: regla 14, humo que ESCRIBE su JSON\n"
             "T_ETAPA = 12000 if HUMO else 100000   # FANIN: 100000 = defecto del organismo (el examen del tronco)\n\n\n"
             "class _Serie:   # FANIN: el humo corre en UN proceso, sin Pool\n"
             "    def __enter__(self): return self\n"
             "    def __exit__(self, *a): return False\n"
             "    def imap_unordered(self, f, it, chunksize=1): return map(f, it)\n", etq='N_PARALELO')
    t = sust(t, "    cual, esc, seed = args\n", "    cual, esc, seed, _T = args\n", etq='tarea_id args')
    t = sust(t, "import organismo_v142 as v13   # TRONCO v14.2 = v14.1 + B-5 (desambiguar=1 por defecto)",
             "import organismo_v142_fanin as v13   # FANIN: copia por anclas del tronco v14.2 (fanin=6 == tronco)", n=2, etq='import')
    t = sust(t, "        a, b = ref.run(seed, **ESC_ID[esc]), v13.run(seed, eta_s=0.0, puerta=None, **ESC_ID[esc])\n",
             "        a, b = ref.run(seed, T=_T, **ESC_ID[esc]), v13.run(seed, T=_T, eta_s=0.0, puerta=None, **ESC_ID[esc])\n", etq='id v11')
    t = sust(t, "        a, b = ref.run(seed, **ESC_ID[esc]), v13.run(seed, eta_s=0.0, puerta=None, div_signo=False, **ESC_ID[esc])\n",
             "        a, b = ref.run(seed, T=_T, **ESC_ID[esc]), v13.run(seed, T=_T, eta_s=0.0, puerta=None, div_signo=False, **ESC_ID[esc])\n", etq='id v10')
    t = sust(t, "    dif = [k for k in a if a[k] != b[k]]\n", "    dif = [k for k in a if a[k] != b[k]]   # claves de la referencia; la copia agrega fanin/diag_fanin\n", etq='dif')
    t = sust(t, "    etapa, seed = args\n", "    etapa, seed, _fanin, _T = args\n", etq='tarea args')
    t = sust(t, "    r = v13.run(seed, **ETAPAS[etapa])\n", "    r = v13.run(seed, T=_T, fanin=_fanin, **ETAPAS[etapa])\n", etq='tarea run')
    t = sust(t, "if a not in ('--log', '--desde') and sys.argv[i - 1] != '--desde']",
             "if a not in ('--log', '--desde', '--fanin', '--pool', '--humo') and sys.argv[i - 1] not in ('--desde', '--fanin', '--pool')]", etq='argv')
    t = sust(t, "    S = int(argv[0]) if argv else 6\n", "    S = 1 if HUMO else (int(argv[0]) if argv else 6)\n", etq='S')
    t = sust(t, "    if '--log' in sys.argv:\n        _log['f'] = open(os.path.join(RAIZ, 'datos', f'examen_v142_{stamp}.log')",
             "    _DAT = os.path.join(RAIZ, 'datos', 'humo') if HUMO else os.path.join(RAIZ, 'datos'); os.makedirs(_DAT, exist_ok=True)\n"
             "    if '--log' in sys.argv or HUMO:\n        _log['f'] = open(os.path.join(_DAT, f'examen_v142_fanin{FANIN}{\"_humo\" if HUMO else \"\"}_{stamp}.log')", etq='log')
    t = sust(t, "    log(f\"=== Batería v13 — CRITERIO v3, {S} semillas",
             "    log(f\"FANIN = {FANIN}  HUMO = {HUMO}  T = {T_ETAPA}  Pool = {N_PARALELO if not HUMO else 'no (un proceso)'}\")\n"
             "    log(f\"=== Batería v13 — CRITERIO v3, {S} semillas", etq='log fanin')
    t = sust(t, "    with mp.Pool(N_PARALELO) as pool:\n", "    with (_Serie() if HUMO else mp.Pool(N_PARALELO)) as pool:\n", etq='pool')
    t = sust(t, "        trabajos = [(c, e, s) for c in ('v11', 'v10') for e in ESC_ID for s in range(1, 7)]\n",
             "        trabajos = [(c, e, s, T_ETAPA) for c in ('v11', 'v10') for e in ESC_ID for s in range(1, 7)][:1 if HUMO else None]\n", etq='trab id')
    t = sust(t, "        trabajos = [(e, s) for e in ETAPAS for s in seeds]\n",
             "        trabajos = [(e, s, FANIN, T_ETAPA) for e in ETAPAS for s in seeds]\n", etq='trab')
    t = sust(t, "        dj = os.path.join(RAIZ, 'datos', f'examen_v142_{stamp}.json')\n",
             "        dj = os.path.join(_DAT, f'examen_v142_fanin{FANIN}{\"_humo\" if HUMO else \"\"}_{stamp}.json')\n", etq='json')
    t = sust(t, "        meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), semillas=S,",
             "        meta = dict(fanin=FANIN, humo=HUMO, T=T_ETAPA, fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), semillas=S,", etq='meta')
    t = sust(t, "sha_organismo_v13=h16(os.path.join(_D14, 'organismo_v142.py'))",
             "sha_organismo_v13=h16(os.path.join(AQUI, 'organismo_v142_fanin.py'))", etq='sha json')
    t = sust(t, "    log(f\"sha organismo_v13 {h16(os.path.join(_D14, 'organismo_v142.py'))}",
             "    log(f\"sha organismo_v13 {h16(os.path.join(AQUI, 'organismo_v142_fanin.py'))}", etq='sha log')
    t = sust(t, "sha_organismo_v11=h16(os.path.join(AQUI, 'organismo_v11.py')), sha_organismo_v10=h16(os.path.join(AQUI, 'organismo_v10.py'))",
             "sha_organismo_v11=h16(os.path.join(_D14, 'organismo_v11.py')), sha_organismo_v10=h16(os.path.join(_D14, 'organismo_v10.py'))",
             etq='sha v11/v10 (ERR-42, hallado por el humo)')
    b1 = cab + t

    # ---------------- 4. bateria de generalizacion (regresion de la Etapa 3) ----------------
    t = origen('bateria_generaliza_v142.py')
    cab = ('"""bateria_generaliza_v142_fanin = organismo/bateria_generaliza_v142.py (e5929942647756a5, CONGELADA: solo se leyo)\n'
           'con UNA entrada nueva en INSTRUMENTOS (organismo_v142_fanin -> organismo_v142g_fanin) cuyos kwargs son COPIA\n'
           'LITERAL de la entrada organismo_v142 (regla 14; el constructor lo verifica campo a campo), y `fanin` que llega\n'
           'por la tarea (`--fanin N`). Umbrales G1/G2/K sin tocar. `--pool N` (defecto 6), `--humo` (1 semilla, T=40000,\n'
           'sin Pool, JSON a datos/humo/). Vive en experimentos/nivel07_fanin_expansion/ (rutas corregidas, ERR-42).\n'
           '    python bateria_generaliza_v142_fanin.py organismo_v142_fanin 20 --desde 6001 --fanin 2 --pool 6 --log\n'
           'Generada POR ANCLAS por construye_fanin.py. NO editar a mano."""\n')
    t = sust(t, "RAIZ = os.path.dirname(AQUI)\n", "RAIZ = os.path.dirname(os.path.dirname(AQUI))   # FANIN: experimentos/<carpeta>/ -> raiz\n", etq='RAIZ g')
    t = sust(t, "N_PARALELO = 14\n",
             "N_PARALELO = int(sys.argv[sys.argv.index('--pool') + 1]) if '--pool' in sys.argv else 6   # FANIN\n"
             "FANIN = int(sys.argv[sys.argv.index('--fanin') + 1]) if '--fanin' in sys.argv else 6   # FANIN\n"
             "HUMO = '--humo' in sys.argv   # FANIN: regla 14\n"
             "T_REGLA = 40000 if HUMO else 200000   # FANIN: 200000 = la bateria del tronco\n\n\n"
             "class _Serie:   # FANIN: el humo corre en UN proceso, sin Pool\n"
             "    def __enter__(self): return self\n"
             "    def __exit__(self, *a): return False\n"
             "    def imap_unordered(self, f, it, chunksize=1): return map(f, it)\n", etq='N_PARALELO g')
    linea = "    'organismo_v142': ('organismo_v142g', dict(eta_s=0.15, clip_s=10.0, puerta=3, mask_rel=2, del_s=0.25, del_c=0.25, ema_c=0.05, puerta_pat=5, pat_shuf=0, pat_min=1)),"
    if t.count(linea) != 1:
        raise SystemExit('*** la entrada organismo_v142 de INSTRUMENTOS no esta como se esperaba. No se escribe nada.')
    nueva = linea.replace("'organismo_v142': ('organismo_v142g',", "'organismo_v142_fanin': ('organismo_v142g_fanin',")
    kw_tronco = linea.split('dict(', 1)[1]; kw_nueva = nueva.split('dict(', 1)[1]
    assert kw_tronco == kw_nueva, 'regla 14: kwargs distintos'
    t = sust(t, linea, linea + "   # TRONCO v14.2 = v14.1 + B-5: kwargs CAMPO A CAMPO iguales a los de organismo_v14 (regla 14)\n" + nueva, etq='INSTRUMENTOS')
    t = sust(t, "    modulo, regla, seed = args\n", "    modulo, regla, seed, _fanin, _T = args\n", etq='tarea g')
    t = sust(t, "    r = g.run(seed, T=200000, mundo='regla', regla=regla, **kw)\n",
             "    r = g.run(seed, T=_T, mundo='regla', regla=regla, **kw, **({'fanin': _fanin} if modulo == 'organismo_v142_fanin' else {}))\n", etq='run g')
    t = sust(t, "if a not in ('--log', '--desde') and sys.argv[i - 1] != '--desde']",
             "if a not in ('--log', '--desde', '--fanin', '--pool', '--humo') and sys.argv[i - 1] not in ('--desde', '--fanin', '--pool')]", etq='argv g')
    t = sust(t, "    S = int(argv[1]) if len(argv) > 1 else 10\n", "    S = 1 if HUMO else (int(argv[1]) if len(argv) > 1 else 10)\n", etq='S g')
    t = sust(t, "    if '--log' in sys.argv:\n        _log['f'] = open(os.path.join(RAIZ, 'datos', f'regresion_generaliza_{modulo}_{stamp}.log')",
             "    _DAT = os.path.join(RAIZ, 'datos', 'humo') if HUMO else os.path.join(RAIZ, 'datos'); os.makedirs(_DAT, exist_ok=True)\n"
             "    _SUF = f'{FANIN}' + ('_humo' if HUMO else '')\n"
             "    if '--log' in sys.argv or HUMO:\n        _log['f'] = open(os.path.join(_DAT, f'regresion_generaliza_{modulo}{_SUF}_{stamp}.log')", etq='log g')
    t = sust(t, "    log(f\"=== REGRESIÓN DE GENERALIZACIÓN (Etapa 3) — {modulo}",
             "    log(f\"FANIN = {FANIN}  HUMO = {HUMO}  T = {T_REGLA}  Pool = {N_PARALELO if not HUMO else 'no (un proceso)'}\")\n"
             "    log(f\"=== REGRESIÓN DE GENERALIZACIÓN (Etapa 3) — {modulo}", etq='log fanin g')
    t = sust(t, "    _dir = {'organismo_v14g': AQUI,", "    _dir = {'organismo_v142g_fanin': AQUI, 'organismo_v14g': os.path.join(RAIZ, 'organismo'),", etq='_dir')
    t = sust(t, "'organismo_v142g': AQUI,", "'organismo_v142g': os.path.join(RAIZ, 'organismo'),", etq='_dir2')
    t = sust(t, "    trabajos = [(modulo, rg, s) for rg in REGLAS for s in seeds]\n",
             "    trabajos = [(modulo, rg, s, FANIN, T_REGLA) for rg in REGLAS for s in seeds]\n", etq='trab g')
    t = sust(t, "    with mp.Pool(N_PARALELO) as pool:\n", "    with (_Serie() if HUMO else mp.Pool(N_PARALELO)) as pool:\n", etq='pool g')
    t = sust(t, "        dj = os.path.join(RAIZ, 'datos', f'regresion_generaliza_{modulo}_{stamp}.json')\n",
             "        dj = os.path.join(_DAT, f'regresion_generaliza_{modulo}{_SUF}_{stamp}.json')\n", etq='json g')
    t = sust(t, "        json.dump(dict(meta=dict(fecha=", "        json.dump(dict(meta=dict(fanin=FANIN, humo=HUMO, T=T_REGLA, fecha=", etq='meta g')
    b2 = cab + t

    for n, txt in (('organismo_v142_fanin.py', o1), ('organismo_v142g_fanin.py', o2),
                   ('bateria_v142_fanin.py', b1), ('bateria_generaliza_v142_fanin.py', b2)):
        p = os.path.join(AQUI, n)
        open(p, 'w', encoding='utf-8', newline='\n').write(txt)
        print(f'  {h16(p)}  {n}')
    for n, s in SHA.items():
        print(f'  origen {n} {s} (intacto: {h16(os.path.join(ORG, n)) == s})')


if __name__ == '__main__':
    main()
