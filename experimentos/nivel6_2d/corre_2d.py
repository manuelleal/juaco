"""Nivel 6 en 2D: RODEO VERDADERO, HORIZONTE 2, SECUENCIA A->B y RODEO FALSO. Ejecuta PREREGISTRO_2d.md.
REGLA 10: log desde el arranque (con fsync). REGLA 11: lista los python vivos antes de abrir el Pool.
Pool SOLO bajo __main__ y SOLO el coordinador (regla 3). Pool(14): no hay razon de memoria para bajarlo
(cada worker sostiene KW 90x6, M 221x6 y una docena de vectores: < 50 MB por proceso).

ETAPA 1 (identidad, se para con sys.exit(1) si no es 100 %): mundo_2d con alto=1 == mundo_mapa (2 configuraciones),
con modo='rodeo' == mundo_mapa_rodeo (1) y con las perillas apagadas == organismo_v13 (1); 2 semillas, T=20000.
El arnes completo (60 comparaciones, 4 rejillas) es experimentos/nivel6_2d/identidad_2d.py.

ETAPA 2: 4 mundos x 6 brazos x 20 semillas. ETAPA 3: criterios del PREREGISTRO_2d.md seccion 5, tal cual.

Uso:  python experimentos/nivel6_2d/corre_2d.py [--desde 21] [--mundos T1 T4 T3 T2]   (replica: --desde 41)
      python experimentos/nivel6_2d/corre_2d.py --humo [--mundos T1]                  (un proceso, 1 semilla, T corto)
"""
import sys, os, json, time, hashlib, platform, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
MAPA_DIR = os.path.join(RAIZ, 'experimentos', 'nivel6_mapa')
RODEO_DIR = os.path.join(RAIZ, 'experimentos', 'nivel6_rodeo')
sys.path[:0] = [AQUI, MAPA_DIR, RODEO_DIR, os.path.join(RAIZ, 'organismo')]


def _lista(flag):
    if flag not in sys.argv: return None
    out = []
    for a in sys.argv[sys.argv.index(flag) + 1:]:
        if a.startswith('--'): break
        out += [x for x in a.replace(',', ' ').split() if x]
    return out or None


_desde = int(sys.argv[sys.argv.index('--desde') + 1]) if '--desde' in sys.argv else 21
SEEDS = list(range(_desde, _desde + 20))
HUMO = '--humo' in sys.argv

T = 100000
ANCHO, ALTO, R_VIS, N_TEL = 17, 13, 3, 40
NOM = {0: '-x', 1: '+x', 2: '-y', 3: '+y'}
N_PARALELO = 14
# Ventana de validez V-T2 (preregistro 5): H1 falla si 0.9^4*v_A < 0.9^7*|v_B| (r > 1.37) y H2 acierta si
# 2*0.9^4*v_A > 0.9^7*|v_B| (r < 2.74). Los dos umbrales salen de la geometria, no de los datos.
VT2_LO, VT2_HI = 1.37, 2.74

# Mundos y pruebas: PREREGISTRO_2d.md seccion 2 (coordenadas relativas al origen azaroso; espejo en semillas pares).
MUNDOS = {
    'T1': dict(et='rodeo', nombre='M1 barrera   rodeo VERDADERO',
               sitios=('A', 'B', 'B', 'B', 'B'), xy=((0, 0), (2, -2), (2, -1), (2, 0), (2, 1)),
               casos=({'et': 'rodeo', 'S': (6, 0), 'ok': (0, 3)},), max_pasos=60),
    'T4': dict(et='falso', nombre='M2 sombra    rodeo FALSO',
               sitios=('A', 'B', 'B', 'A'), xy=((0, 0), (2, 0), (3, 0), (-4, -4)),
               casos=({'et': 'falso', 'S': (-4, 0), 'ok': (1,)},), max_pasos=60),
    'T2': dict(et='h2', nombre='M3 flanco    HORIZONTE 2',
               sitios=('A', 'B', 'B', 'B'), xy=((4, 0), (1, 6), (0, 5), (0, -5)),
               casos=({'et': 'h2', 'S': (0, 0), 'ok': (1,)},), max_pasos=60),
    'T3': dict(et='sec', nombre='M4 secuencia A->B',
               # B a 6 de A (> r_vis): al comerse A tiene que quedarse CIEGO, o la prueba mide las patas y no la tabla M
               sitios=('A', 'A', 'B'), xy=((0, 0), (0, 6), (-4, 4)),
               casos=({'et': 'sec', 'S': (-4, 0), 'ok': (1,), 'consume': True},), max_pasos=80),
}
ORDEN = ['T1', 'T4', 'T3', 'T2']          # preregistro 8: orden por si hay que recortar
PEDIDOS = [m for m in (_lista('--mundos') or ORDEN) if m in MUNDOS] or ORDEN
BRAZOS = {                                 # preregistro seccion 4
    'MAPA':      dict(usa_M=True),
    'MAPA_h2':   dict(usa_M=True, _p=dict(h2=True)),                 # en T3 se sustituye por MAPA_borra
    'SINMAPA':   dict(usa_M=False),
    'CONGELADA': dict(usa_M=True, escribe_M=False),
    'INVERTIDO': dict(usa_M=True, _p=dict(invertir=True)),
    'BARAJADO':  dict(usa_M=True, _p=dict(barajar=True)),
}
BRAZO_T3 = {'MAPA_borra': dict(usa_M=True, _p=dict(borra_M=True))}
brazos_de = lambda mu: ({k: v for k, v in BRAZOS.items() if k != 'MAPA_h2'} | BRAZO_T3) if mu == 'T3' else dict(BRAZOS)
# Identidad interna (etapa 1): 2 configuraciones contra mundo_mapa, 1 contra mundo_mapa_rodeo, 1 contra organismo_v13.
MUNDO_MAPA = dict(r_vis=3, sitios=('A', 'B'))
PRUEBA_MAPA = dict(n_tel=40, E_test=0.3, max_pasos=30)
IDENT_MAPA = {'mapa:MAPA':    dict(MUNDO_MAPA, usa_M=True, prueba=dict(PRUEBA_MAPA)),
              'mapa:SINMAPA': dict(MUNDO_MAPA, usa_M=False, prueba=dict(PRUEBA_MAPA))}
IDENT_ROD = {'rodeo': dict(r_vis=3, sitios=('A', 'B', 'A'), usa_M=True,
                           prueba=dict(modo='rodeo', n_tel=40, E_test=0.3, max_pasos=60, g1=5, g2=20))}
IDENT_V13 = {'v13:apagadas': dict()}
T_ID = 20000
_log = {'f': None, 't0': time.time()}


def log(msg=""):
    linea = f"[{time.strftime('%H:%M:%S')} +{time.time()-_log['t0']:7.1f}s] {msg}"
    print(linea, flush=True)
    if _log['f']:
        _log['f'].write(linea + "\n"); _log['f'].flush(); os.fsync(_log['f'].fileno())


def N(x):
    return json.loads(json.dumps(x, default=str))


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def kw_de(mu, brazo, t=T):
    m = MUNDOS[mu]; br = dict(brazos_de(mu)[brazo]); pex = br.pop('_p', {})
    prueba = dict(modo='2d', xy=m['xy'], casos=m['casos'], n_tel=N_TEL, max_pasos=m['max_pasos'], E_test=0.3, **pex)
    return dict(T=t, ancho=ANCHO, alto=ALTO, r_vis=R_VIS, sitios=m['sitios'], regen=50, prueba=prueba, **br)


def tarea(args):
    tipo = args[0]
    if tipo in ('IM', 'IR', 'IV'):                     # etapa 1: identidad (el ancla del instrumento)
        _, nombre, seed, t_id = args
        import mundo_2d as b_
        if tipo == 'IM':
            import mundo_mapa as a_; kw = dict(IDENT_MAPA[nombre])
        elif tipo == 'IR':
            import mundo_mapa_rodeo as a_; kw = dict(IDENT_ROD[nombre])
        else:
            import organismo_v13 as a_; kw = dict(IDENT_V13[nombre])
        kw['T'] = t_id
        a, b = a_.run(seed, **kw), b_.run(seed, **kw)
        extra = ('tel', 'M_llenas') if tipo == 'IV' else ()
        dif = [k for k in a if N(a[k]) != N(b[k])] + [k for k in b if k not in a and k not in extra]
        if tipo == 'IV' and (b.get('tel') is not None or b.get('M_llenas') != 0): dif.append('perillas_no_apagadas')
        return dict(tipo=tipo, esc=nombre, seed=seed, identico=not dif, difieren=dif)
    _, mu, brazo, seed, t = args
    import mundo_2d as m
    r = m.run(seed, **kw_de(mu, brazo, t))
    return dict(tipo='T', mundo=mu, brazo=brazo, seed=seed, tel=r['tel'], M_llenas=r['M_llenas'], W=r['W'],
                deaths=r['deaths'], mord=r['mord'], splits=r['splits'], celdas=r['celdas'])


# ---------- lecturas de una corrida (todas se calculan sobre los episodios crudos: 'casos') ----------
mir = lambda a, o: a if o > 0 else a ^ 1          # espejo de la semilla: 0<->1 y 2<->3


def CAS(r):
    t = r.get('tel') if isinstance(r, dict) else None
    return (t.get('casos') or []) if t else []


def K(r, k, et=None, alt=None):
    t = r.get('tel') if isinstance(r, dict) else None
    if not t: return alt
    v = t.get(k)
    if isinstance(v, dict): v = v.get(et if et else (list(v) or [None])[0])
    return alt if v is None else v


def ori(r):
    return K(r, 'orientacion', alt=1)


def frac_primer(r, a_canon):
    cs = CAS(r); o = ori(r)
    if not cs: return None
    return sum(c['primer'] == mir(a_canon, o) for c in cs) / len(cs)


def razon_primer(r, a1, a2):
    """Reparto entre dos opciones equivalentes (T4): n(a1)/(n(a1)+n(a2)); None si nunca elige ninguna."""
    cs = CAS(r); o = ori(r)
    n1 = sum(c['primer'] == mir(a1, o) for c in cs); n2 = sum(c['primer'] == mir(a2, o) for c in cs)
    return None if (n1 + n2) == 0 else n1 / (n1 + n2)


def frac_B(r, a_mas, a_menos):
    """Lectura de MECANISMO: fraccion de episodios con B[a_mas] > B[a_menos] (T1c, el flanco barato)."""
    cs = [c for c in CAS(r) if c.get('B1')]; o = ori(r)
    if not cs: return None
    return sum(c['B1'][mir(a_mas, o)] > c['B1'][mir(a_menos, o)] for c in cs) / len(cs)


def sigue(r, cual='mec1', solo_discrepantes=True):
    """Fraccion de episodios (donde mec1 != mec2, si se pide) en que el primer paso es el que predice ese mecanismo."""
    cs = [c for c in CAS(r) if c.get(cual) is not None and c['primer'] >= 0]
    if solo_discrepantes: cs = [c for c in cs if c.get('mec1') != c.get('mec2')]
    return None if not cs else sum(c['primer'] == c[cual] for c in cs) / len(cs)


def n_discrepa(r):
    return sum(1 for c in CAS(r) if c.get('mec1') is not None and c.get('mec1') != c.get('mec2'))


def conducta(r):
    """tel sin los registros de MECANISMO: con usa_M=False el sesgo ni se calcula, asi que esas claves no existen
    en SINMAPA. C2 compara la CONDUCTA bit a bit (primer paso, llegadas, pisadas, pasos, ciego, sin_mover)."""
    t = dict(r.get('tel') or {})
    for k in ('mec1', 'mec2', 'sigue_mec1', 'h2', 'borra_M'): t.pop(k, None)
    t['casos'] = [{k: v for k, v in c.items() if k not in ('mec1', 'mec2', 'B1', 'B2')} for c in (t.get('casos') or [])]
    return N(t)


def med(xs):
    xs = [x for x in xs if x is not None]
    return (None, None, None) if not xs else (float(np.median(xs)), float(min(xs)), float(max(xs)))


def F(x, n=3):
    return 'na' if x is None else f"{x:.{n}f}"


def resume(mu, b, g):
    et = MUNDOS[mu]['et']
    M = lambda k, alt=None: med([K(r, k, et, alt) for r in g])[0]
    R, mn, mx = med([K(r, 'R', et) for r in g])
    return (f"   {b:11s} R {F(R)} [{F(mn,2)},{F(mx,2)}]  llega {F(M('llega'))}  limpio {F(M('llega_limpio'))}"
            f"  come2 {F(M('come2'))}  pisa {F(M('pisa'))}  sigue_mec1 {F(M('sigue_mec1'))}"
            f"  sin_mover {F(M('sin_mover'),0)}/{N_TEL}  ciego {F(M('ciego_al_llegar'),0)}/{N_TEL}"
            f"  M {F(med([r['M_llenas'] for r in g])[0],0)}  v_A {F(M('v_A'),2)}  v_B {F(M('v_B'),2)}"
            f"  muertes {F(med([r['deaths'] for r in g])[0],0)}")


def humo():
    """Humo de un proceso (regla 3): identidad con 1 semilla y T corto + una corrida MAPA corta por mundo pedido."""
    log(f"HUMO de un proceso (sin Pool). Mundos {PEDIDOS}. Identidad 1 semilla T=5000 + 1 corrida MAPA T=20000 por mundo.")
    log(f"sha mundo_2d {h16(os.path.join(AQUI,'mundo_2d.py'))}  mundo_mapa {h16(os.path.join(MAPA_DIR,'mundo_mapa.py'))}"
        f"  mundo_mapa_rodeo {h16(os.path.join(RODEO_DIR,'mundo_mapa_rodeo.py'))}  v13 {h16(os.path.join(RAIZ,'organismo','organismo_v13.py'))}")
    rc = ([tarea(('IM', k, 1, 5000)) for k in IDENT_MAPA] + [tarea(('IR', k, 1, 5000)) for k in IDENT_ROD]
          + [tarea(('IV', k, 1, 5000)) for k in IDENT_V13])
    for x in rc:
        if not x['identico']: log(f"   DIFIERE {x['esc']} s{x['seed']}: {x['difieren']}")
    log(f"   identidad (mundo_mapa x2, rodeo, v13; semilla 1): {sum(x['identico'] for x in rc)}/{len(rc)}")
    for mu in PEDIDOS:
        et = MUNDOS[mu]['et']
        t0 = time.time(); r = tarea(('T', mu, 'MAPA', SEEDS[0], 20000)); t = r['tel']
        log(f"   {mu} {MUNDOS[mu]['nombre']}  s{SEEDS[0]} ({time.time()-t0:.1f}s)  rejilla {t['rejilla']}"
            f"  orientacion {t['orientacion']}  sitios {t['sitios']}")
        log(f"      R {t['R'][et]} (n {t['n'][et]})  llega {t['llega'][et]}  limpio {t['llega_limpio'][et]}"
            f"  come2 {t['come2'][et]}  pisa {t['pisa'][et]}  pasos {t['pasos'][et]}"
            f"  sigue_mec1 {t['sigue_mec1'][et]}  sin_mover {t['sin_mover']}  ciego {t['ciego_al_llegar']}/{N_TEL}")
        vA, vB = t['v_A'], t['v_B']; rr = (abs(vB) / vA) if vA > 0 else None
        log(f"      v_A {vA}  v_B {vB}  r {F(rr,2)}  V-T2 ({VT2_LO}<r<{VT2_HI}) {'dentro' if (rr and VT2_LO < rr < VT2_HI) else 'fuera'}"
            f"  M_llenas {r['M_llenas']}/{len(MUNDOS[mu]['xy'])}  W {r['W']}  muertes {r['deaths']}"
            f"  mec1!=mec2 en {n_discrepa(r)}/{N_TEL}")
        log(f"      primer paso {{{', '.join(f'{NOM[a]}:{F(frac_primer(r,a),2)}' for a in range(4))}}}   B1(ep0) {CAS(r)[0]['B1']}")
    log("HUMO hecho. Son 1 semilla y T=20000 (el bloque va a 100000): no son el resultado y nada se recalibra con ellos.")


if __name__ == '__main__':
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f"2d_{'humo' if HUMO else f's{SEEDS[0]}-{SEEDS[-1]}'}_{stamp}.log"),
                     'w', encoding='utf-8', newline='\n')
    if HUMO:
        humo(); _log['f'].close(); sys.exit(0)
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    pre = os.path.join(AQUI, 'PREREGISTRO_2d.md')
    SHAS = dict(preregistro=h16(pre), script=h16(os.path.abspath(__file__)),
                instrumento=h16(os.path.join(AQUI, 'mundo_2d.py')),
                constructor=h16(os.path.join(AQUI, 'construye_2d.py')),
                origen_rodeo=h16(os.path.join(RODEO_DIR, 'mundo_mapa_rodeo.py')),
                origen_mapa=h16(os.path.join(MAPA_DIR, 'mundo_mapa.py')),
                tronco_v13=h16(os.path.join(RAIZ, 'organismo', 'organismo_v13.py')))
    log(f"ARRANQUE nivel 6 en 2D sobre v13. Mundos {PEDIDOS}, semillas {SEEDS[0]}-{SEEDS[-1]}, rejilla {ANCHO}x{ALTO}, Pool({N_PARALELO}).")
    log("   " + "  ".join(f"sha {k} {v}" for k, v in SHAS.items()))
    try:
        ps = subprocess.run(['powershell', '-NoProfile', '-Command',
                             "Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*' } | ForEach-Object { \"$($_.ProcessId) $($_.CommandLine)\" }"],
                            capture_output=True, text=True, timeout=60).stdout.strip().splitlines()
    except Exception as e:
        ps = [f"(no se pudo listar: {e})"]
    log(f"REGLA 11 — procesos python vivos ({len(ps)}), este es pid {os.getpid()}")
    V = {}
    with mp.Pool(N_PARALELO) as pool:
        ctrl = ([('IM', k, s, T_ID) for k in IDENT_MAPA for s in (1, 2)] +
                [('IR', k, s, T_ID) for k in IDENT_ROD for s in (1, 2)] +
                [('IV', k, s, T_ID) for k in IDENT_V13 for s in (1, 2)])
        log(f"ETAPA 1/3 — identidad: {len(ctrl)} comparaciones (alto=1 contra mundo_mapa, modo=rodeo contra mundo_mapa_rodeo, apagadas contra v13)...")
        rc = pool.map(tarea, ctrl, chunksize=1)
        log(f"  identicas: {sum(x['identico'] for x in rc)}/{len(rc)}")
        for x in rc:
            if not x['identico']: log(f"      DIFIERE {x['esc']} s{x['seed']}: {x['difieren']}")
        V['IDENTIDAD'] = all(x['identico'] for x in rc)
        if not V['IDENTIDAD']:
            log("*** IDENTIDAD FALLIDA: se para (el instrumento no es el anillo con alto=1)."); _log['f'].close(); sys.exit(1)
        tr = [('T', mu, b, s, T) for mu in PEDIDOS for b in brazos_de(mu) for s in SEEDS]
        log(f"ETAPA 2/3 — {len(tr)} corridas de {T} pasos...")
        res = []
        for i, r in enumerate(pool.imap_unordered(tarea, tr, chunksize=1), 1):
            res.append(r)
            if i % 20 == 0 or i == len(tr): log(f"          {i}/{len(tr)}")
    dj = os.path.join(RAIZ, 'datos', f'2d_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.json')
    json.dump(dict(meta=dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), semillas=SEEDS, mundos=PEDIDOS, shas=SHAS,
                             crudo=True), corridas=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"   seguro: corridas crudas ya guardadas en {os.path.basename(dj)} (se reescribe con los veredictos al final)")
    log("ETAPA 3/3 — analisis (criterios del PREREGISTRO_2d.md seccion 5, tal cual).")
    POR = {mu: {b: {r['seed']: r for r in res if r['mundo'] == mu and r['brazo'] == b} for b in brazos_de(mu)} for mu in PEDIDOS}
    for mu in PEDIDOS:
        log(f"  {mu} — {MUNDOS[mu]['nombre']}")
        for b in brazos_de(mu):
            log(resume(mu, b, [POR[mu][b][s] for s in SEEDS]))
    P, det = {}, {}
    # ---- P1 rodeo verdadero (T1) ----
    if 'T1' in PEDIDOS:
        mp_, sn = POR['T1']['MAPA'], POR['T1']['SINMAPA']
        r1 = [K(mp_[s], 'R', 'rodeo') for s in SEEDS]; r1s = [K(sn[s], 'R', 'rodeo') for s in SEEDS]
        par = sum(1 for a, b in zip(r1, r1s) if a is not None and b is not None and a > b)
        t1b = [frac_primer(mp_[s], 1) for s in SEEDS]; t1c = [frac_B(mp_[s], 3, 2) for s in SEEDS]
        P['P1'] = bool(med(r1)[0] is not None and med(r1)[0] >= 0.50 and par >= 15)
        det['P1'] = dict(R1=med(r1)[0], R1_sinmapa=med(r1s)[0], pareado=par, T1b_alejarse=med(t1b)[0], T1c_flanco=med(t1c)[0],
                         refutado_se_aleja=bool(med(r1)[0] is not None and med(r1)[0] <= 0.20 and (med(t1b)[0] or 0) >= 0.80))
        log(f"   P1 rodeo verdadero: R1 {F(med(r1)[0])} (SINMAPA {F(med(r1s)[0])}, pareado {par}/20) -> {'OK' if P['P1'] else 'NO'}"
            f" | alejarse {F(med(t1b)[0])} | flanco barato (mecanismo) {F(med(t1c)[0])}"
            f"{'  *** REFUTADO en la forma predicha: no rodea, se aleja' if det['P1']['refutado_se_aleja'] else ''}")
    # ---- P2 horizonte 2 (T2), con la ventana V-T2 por semilla ----
    if 'T2' in PEDIDOS:
        m1, m2 = POR['T2']['MAPA'], POR['T2']['MAPA_h2']
        rs = {}
        for s in SEEDS:
            vA, vB = K(m1[s], 'v_A'), K(m1[s], 'v_B')
            rs[s] = (abs(vB) / vA) if (vA and vA > 0 and vB is not None) else None
        val = [s for s in SEEDS if rs[s] is not None and VT2_LO < rs[s] < VT2_HI]
        dif = {s: (None if (K(m2[s], 'R', 'h2') is None or K(m1[s], 'R', 'h2') is None)
                   else K(m2[s], 'R', 'h2') - K(m1[s], 'R', 'h2')) for s in SEEDS}
        gana = sum(1 for s in val if dif[s] is not None and dif[s] >= 0.15)
        sg1 = med([sigue(m1[s], 'mec1') for s in val])[0]; sg2 = med([sigue(m2[s], 'mec2') for s in val])[0]
        VT2 = len(val) >= 8
        P['P2'] = bool(VT2 and val and gana / len(val) >= 0.75 and (sg1 or 0) >= 0.70 and (sg2 or 0) >= 0.70)
        det['P2'] = dict(validas=val, n_validas=len(val), r_por_semilla={s: rs[s] for s in SEEDS}, V_T2=bool(VT2),
                         dif_validas=med([dif[s] for s in val])[0], dif_todas=med([dif[s] for s in SEEDS])[0],
                         gana_015=gana, sigue_mec1=sg1, sigue_mec2=sg2,
                         R2_mapa_validas=med([K(m1[s], 'R', 'h2') for s in val])[0],
                         R2_h2_validas=med([K(m2[s], 'R', 'h2') for s in val])[0],
                         R2_mapa_todas=med([K(m1[s], 'R', 'h2') for s in SEEDS])[0],
                         R2_h2_todas=med([K(m2[s], 'R', 'h2') for s in SEEDS])[0])
        log(f"   P2 horizonte 2: validas {len(val)}/20 (V-T2 {VT2_LO}<r<{VT2_HI}) {'OK' if VT2 else 'NO (no discrimina)'}"
            f" | subconjunto valido R2 {F(det['P2']['R2_mapa_validas'])} -> {F(det['P2']['R2_h2_validas'])}"
            f" (dif {F(det['P2']['dif_validas'])}, >=0.15 en {gana}/{len(val) if val else 0})"
            f" | sigue mec1 {F(sg1)} / mec2 {F(sg2)} -> {'OK' if P['P2'] else 'NO'}")
        log(f"      conjunto completo (se reporta al lado): R2 {F(det['P2']['R2_mapa_todas'])} -> {F(det['P2']['R2_h2_todas'])}"
            f"  dif {F(det['P2']['dif_todas'])}")
    # ---- P3 secuencia A->B (T3) ----
    if 'T3' in PEDIDOS:
        mp3, bo = POR['T3']['MAPA'], POR['T3']['MAPA_borra']
        c_m = [K(mp3[s], 'come2', 'sec') for s in SEEDS]; c_b = [K(bo[s], 'come2', 'sec') for s in SEEDS]
        par3 = sum(1 for a, b in zip(c_b, c_m) if a is not None and b is not None and a > b)
        P['P3'] = bool(med(c_b)[0] is not None and med(c_b)[0] >= 0.50 and (med(c_m)[0] or 0) <= 0.20 and par3 >= 15)
        det['P3'] = dict(come2_mapa=med(c_m)[0], come2_borra=med(c_b)[0], pareado=par3,
                         llega_mapa=med([K(mp3[s], 'llega', 'sec') for s in SEEDS])[0],
                         llega_borra=med([K(bo[s], 'llega', 'sec') for s in SEEDS])[0])
        log(f"   P3 secuencia: come2 MAPA {F(med(c_m)[0])} -> borra_M {F(med(c_b)[0])} (pareado {par3}/20)"
            f" | llega_A {F(det['P3']['llega_mapa'])} / {F(det['P3']['llega_borra'])} -> {'OK' if P['P3'] else 'NO'}")
    # ---- P4 rodeo falso (T4) ----
    if 'T4' in PEDIDOS:
        m4 = POR['T4']['MAPA']
        r4 = [razon_primer(m4[s], 1, 2) for s in SEEDS]
        P['P4'] = bool(med(r4)[0] is not None and med(r4)[0] <= 0.25)
        det['P4'] = dict(R4=med(r4)[0], indiferente=bool(med(r4)[0] is not None and 0.40 <= med(r4)[0] <= 0.60),
                         R4_sinmapa=med([razon_primer(POR['T4']['SINMAPA'][s], 1, 2) for s in SEEDS])[0])
        log(f"   P4 rodeo falso: R4 {F(med(r4)[0])} (SINMAPA {F(det['P4']['R4_sinmapa'])}, indiferente = 0.50) -> {'OK' if P['P4'] else 'NO'}"
            f"{'  *** refutado: no hay desvio sin motivo' if det['P4']['indiferente'] else ''}")
    # ---- controles y validez ----
    c1a = med([frac_primer(POR['T1']['INVERTIDO'][s], 1) for s in SEEDS])[0] if 'T1' in PEDIDOS else None
    c1b = med([razon_primer(POR['T4']['INVERTIDO'][s], 1, 2) for s in SEEDS])[0] if 'T4' in PEDIDOS else None
    C1 = bool((c1a is None or c1a <= 0.25) and (c1b is None or c1b >= 0.60) and not (c1a is None and c1b is None))
    C2 = all(conducta(POR[mu]['SINMAPA'][s]) == conducta(POR[mu]['CONGELADA'][s]) and POR[mu]['CONGELADA'][s]['M_llenas'] == 0
             for mu in PEDIDOS for s in SEEDS)
    C3 = {mu: med([K(POR[mu]['BARAJADO'][s], 'R', MUNDOS[mu]['et']) for s in SEEDS])[0] for mu in PEDIDOS}
    V1 = all(POR[mu][b][s]['M_llenas'] == len(MUNDOS[mu]['xy']) for mu in PEDIDOS for b in ('MAPA', 'INVERTIDO') for s in SEEDS)
    V2 = all(K(POR[mu][b][s], 'ciego_al_llegar', alt=0) == N_TEL for mu in PEDIDOS for b in brazos_de(mu) for s in SEEDS)
    V3 = all(K(POR[mu][b][s], 'sin_mover', alt=99) <= 2 for mu in PEDIDOS for b in brazos_de(mu) for s in SEEDS)
    v4n = {mu: sum(1 for s in SEEDS if (K(POR[mu]['MAPA'][s], 'v_A') or 0) > 0 and (K(POR[mu]['MAPA'][s], 'v_B') or 0) < 0) for mu in PEDIDOS}
    V4 = all(n >= 18 for n in v4n.values())
    V.update(P); V.update(C1=C1, C1_invertido_T1b=c1a, C1_invertido_R4=c1b, C2=bool(C2), C3_barajado=C3,
                          V1=bool(V1), V2=bool(V2), V3=bool(V3), V4=bool(V4), V4_n=v4n, detalle=det,
                          RODEA_2D=bool(all(P.get(k, False) for k in ('P1', 'P2', 'P3', 'P4'))))
    log(f"   C1 INVERTIDO decisivo (T1b<=0.25 {F(c1a)} y R4>=0.60 {F(c1b)}): {'OK' if C1 else 'NO'}"
        f" | C2 CONGELADA==SINMAPA en conducta y M_llenas=0: {'OK' if C2 else 'NO'}"
        f" | C3 BARAJADO (se reporta): {{{', '.join(f'{k}:{F(v)}' for k, v in C3.items())}}}")
    log(f"   validez: V1 M_llenas {'OK' if V1 else 'NO'} | V2 ciego {N_TEL}/{N_TEL} {'OK' if V2 else 'NO'}"
        f" | V3 sin_mover<=2 {'OK' if V3 else 'NO'} | V4 v_A>0 y v_B<0 en >=18/20 {v4n} {'OK' if V4 else 'NO'}")
    valido = C1 and C2 and V1 and V2 and V3 and V4
    if V['RODEA_2D']:
        ver = "RODEA_2D: rodea el veneno recordado, gana con horizonte 2, encadena A->B y no se desvia sin motivo"
    elif det.get('P1', {}).get('refutado_se_aleja'):
        ver = ("REFUTADO en la forma predicha: con el veneno recordado entre el y la comida NO RODEA, SE ALEJA; "
               "el mecanismo distingue el flanco barato y no lo usa")
    else:
        ver = "NO (algun criterio cayo fuera de la forma predicha): ver P1-P4 arriba, no se declara nada"
    log(f"VEREDICTO 2D: {ver}{'' if valido else '  *** OJO: control o validez caidos, NO SE INTERPRETA'}")
    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), semillas=SEEDS, mundos=PEDIDOS, rejilla=[ANCHO, ALTO],
                r_vis=R_VIS, T=T, n_tel=N_TEL, ventana_VT2=[VT2_LO, VT2_HI], definicion_mundos=MUNDOS,
                brazos={mu: list(brazos_de(mu)) for mu in PEDIDOS}, veredictos=V, identidades=rc, procesos_python=ps,
                shas=SHAS, python=platform.python_version(), numpy=np.__version__)
    json.dump(dict(meta=meta, corridas=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
