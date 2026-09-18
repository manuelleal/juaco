"""Nivel 8, bloque metaplasticidad (A-2 del creador A): mundo largo con la via rapida ganada por
g_c = 1/(1+beta_m*m_c), m_c = min(Wp,Wn) = masa de conflicto YA presente en el tronco (A3). Ejecuta
PREREGISTRO_metaplasticidad.md. Copia adaptada de experimentos/nivel8_mundo_largo/corre_mundo_largo.py (no se
edita ese archivo; solo se copia su logica de pool_de/sitios_de/recuperacion). REGLA 10: log desde el arranque
con fsync. REGLA 3: Pool solo bajo if __name__=='__main__'; --humo corre 1 solo proceso, sin Pool.
Identidad (dentro del runner, antes de la serie): mundo_largo_A.run(seed, beta_m=None, **kw) ==
mundo_largo.run(seed, **kw), semillas 1-3, T=20000, todas las claves.

Uso:  python experimentos/nivel8_metaplasticidad/corre_metaplasticidad.py [--desde N]
      python experimentos/nivel8_metaplasticidad/corre_metaplasticidad.py --humo
"""
import sys, os, json, time, hashlib, platform, subprocess, itertools
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
LARGO = os.path.join(RAIZ, 'experimentos', 'nivel8_mundo_largo')          # origen: mundo_largo.py (no se edita)
CREACION_A = os.path.join(RAIZ, 'experimentos', 'creacion_A')             # instrumento: mundo_largo_A.py
sys.path[:0] = [AQUI, CREACION_A, LARGO]

_HUMO = '--humo' in sys.argv
_desde = int(sys.argv[sys.argv.index('--desde') + 1]) if '--desde' in sys.argv else 41
SEEDS = list(range(_desde, _desde + 20))
T = 200000; T_NUEVO = 4000; T_INV = 100000
BRAZOS = {
    'BASE': dict(beta_m=None),
    'B10':  dict(beta_m=10),
    'B50':  dict(beta_m=50),
}
N_PARALELO = 14
_log = {'f': None, 't0': time.time()}


def log(msg=""):
    linea = f"[{time.strftime('%H:%M:%S')} +{time.time()-_log['t0']:7.1f}s] {msg}"
    print(linea, flush=True)
    if _log['f']:
        _log['f'].write(linea + "\n"); _log['f'].flush(); os.fsync(_log['f'].fileno())


def N(x):
    """Normalizacion de otros runners (corre_mundo_largo.py, mini_prueba_A_largo.py): listas/dicts/np -> basicos."""
    return json.loads(json.dumps(x, default=str))


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def pool_de(seed):
    """50 patrones (peso 2, 3 y 4 sobre 6 px), valencias al azar 25/25 con RNG propio. Nombres = cadena de bits.
    Copiado sin cambios de corre_mundo_largo.py (funcion del MUNDO, no del organismo; no depende de beta_m)."""
    pats = []
    for w in (2, 3, 4):
        for combo in itertools.combinations(range(6), w):
            v = np.zeros(6); v[list(combo)] = 1.
            pats.append((''.join('1' if v[j] else '0' for j in range(6)), v))
    r0 = np.random.default_rng(30000 + seed); perm = r0.permutation(len(pats))
    com = set(pats[i][0] for i in perm[:25])
    return [(n, v, 'comida' if n in com else 'veneno') for n, v in pats]


def sitios_de(pool, seed):
    """4 patrones iniciales (2 comida, 2 veneno) de PESO 3, cada uno en dos sitios, intercalados.
    Copiado sin cambios de corre_mundo_largo.py."""
    r1 = np.random.default_rng(40000 + seed)
    f = [n for n, v, vl in pool if vl == 'comida' and n.count('1') == 3]; p = [n for n, v, vl in pool if vl == 'veneno' and n.count('1') == 3]
    f = [f[i] for i in r1.permutation(len(f))[:2]]; p = [p[i] for i in r1.permutation(len(p))[:2]]
    return (f[0], p[0], f[1], p[1], f[0], p[0], f[1], p[1])


def recuperacion(cb, db):
    """Copiado sin cambios de corre_mundo_largo.py. Usa T/T_INV GLOBALES (200000/100000): a T=20000 (--humo /
    identidad) 'pre' y 'rec' no son interpretables (b0=T_INV//1000=100 cae fuera del rango de cb/db, que solo
    tienen T//1000+1 bins) -- es un artefacto esperado de correr a T corto, no un bug; ver informe de entrega."""
    pre = float(np.mean(cb[80:100])); b0 = T_INV // 1000
    rec = None
    for b in range(b0, len(cb) - 3):
        if np.mean(cb[b:b + 3]) >= 0.8 * pre: rec = (b - b0) * 1000; break
    return dict(pre=round(pre, 2), rec=rec if rec is not None else T - T_INV, muertes_20k=int(sum(db[b0:b0 + 20])), rec_hallada=rec is not None)


def med(xs):
    xs = [x for x in xs if x is not None]
    return float(np.median(xs)), float(min(xs)), float(max(xs))


def identidad(T_id=20000):
    """ETAPA DE IDENTIDAD (parrafo 3 del preregistro): mundo_largo_A(beta_m=None) == mundo_largo, semillas 1-3,
    T=20000, en la config real de la serie (pool+sitios+T_nuevo+r_vis, usa_M=False). Secuencial, sin Pool (vale
    tanto para --humo como para la serie completa, que la corre ANTES de abrir el Pool)."""
    import mundo_largo as ORIG
    import mundo_largo_A as NUEVO
    malas = []; detalle = []
    for seed in (1, 2, 3):
        pool = pool_de(seed)
        kw = dict(T=T_id, r_vis=3, sitios=sitios_de(pool, seed), pool=pool, T_nuevo=T_NUEVO,
                  invertir_largo=(T_INV if T_id >= T_INV else None), usa_M=False)
        a = ORIG.run(seed, **kw)
        b = NUEVO.run(seed, beta_m=None, **kw)
        dif = [k for k in a if N(a[k]) != N(b[k])]   # itera sobre las claves del ORIGEN; beta_m/m_stats (solo en b) quedan fuera, por diseno
        detalle.append(dict(seed=seed, identico=not dif, difieren=dif, claves=len(a)))
        log(f"   identidad s{seed} T={T_id}: {'IDENTICO' if not dif else 'DIFIEREN ' + str(dif)} ({len(a)} claves)")
        if dif: malas.append((seed, dif))
    return (not malas), detalle


def tarea(args, T=T):
    """Una corrida (brazo, seed). T por defecto = el T global de la serie (200000); se sobre-escribe explicito
    en --humo (T=20000). Import local de mundo_largo_A: necesario porque Pool usa 'spawn' (regla 9 del EQUIPO)."""
    _, brazo, seed = args
    import mundo_largo_A as m
    pool = pool_de(seed)
    kw = dict(T=T, r_vis=3, sitios=sitios_de(pool, seed), pool=pool, T_nuevo=T_NUEVO,
              invertir_largo=(T_INV if T >= T_INV else None), usa_M=False)
    kw.update(BRAZOS[brazo])
    r = m.run(seed, m_stats=True, **kw)
    cv = r['curva']
    hasta30 = [c[2] for c in cv if c[1] <= 30]; fin = cv[-1] if cv else (None, None, None, None)
    vf = r['val_final']; vs = r['vistos']; W = r['W']
    ok = lambda n: (W[n] > 0) == (vf[n] == 'comida')
    ret_no_inv = float(np.mean([ok(n) for n in vs[4:10]])) if len(vs) >= 10 else None   # nunca invertidos, ausentes
    ret_inv = float(np.mean([ok(n) for n in vs[:4]]))                                    # invertidos en ausencia
    return dict(tipo='T', brazo=brazo, seed=seed, beta_m=BRAZOS[brazo]['beta_m'], curva=cv, n_vistos=len(r['vistos']),
                adq_hasta30=float(np.median(hasta30)) if hasta30 else None, adq_final=fin[2], ret_final=fin[3],
                ret_no_inv=ret_no_inv, ret_inv=ret_inv, W=W, vistos=vs, val_final=vf,
                deaths=r['deaths'], celdas=r['celdas'], splits=r['splits'], m_stats=r['m_stats'],
                **recuperacion(r['comida_bin'], r['muertes_bin']))


def _procesos_vivos():
    """REGLA 11: antes de abrir el Pool, mira los procesos python vivos (igual que corre_mundo_largo.py)."""
    try:
        ps = subprocess.run(['powershell', '-NoProfile', '-Command',
                             "Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*' } | ForEach-Object { \"$($_.ProcessId) $($_.CommandLine)\" }"],
                            capture_output=True, text=True, timeout=60).stdout.strip().splitlines()
    except Exception as e:
        ps = [f"(no se pudo listar: {e})"]
    return ps


if __name__ == '__main__':

    if _HUMO:
        # --humo: 3 semillas, T=20000, UN solo brazo, secuencial, SIN Pool (mini-prueba de un proceso, regla 3).
        HUMO_BRAZO = 'B50'   # ejerce la rama nueva (g_c != 1), no solo la identidad
        t0 = time.time()
        log(f"=== HUMO (1 proceso, sin Pool) === identidad s1-3 T=20000, luego 3 corridas brazo {HUMO_BRAZO} T=20000")
        ok, detalle = identidad(T_id=20000)
        log(f"identidad: {'OK' if ok else 'FALLA'} {sum(d['identico'] for d in detalle)}/3")
        if not ok:
            log("VEREDICTO: INSTRUMENTO SOSPECHOSO (identidad no 3/3 en humo)")
            sys.exit(1)
        for seed in (1, 2, 3):
            ts = time.time()
            r = tarea(('T', HUMO_BRAZO, seed), T=20000)
            dt = time.time() - ts
            log(f"  s{seed} brazo={HUMO_BRAZO}  ret_no_inv={r['ret_no_inv']}  ret_inv={r['ret_inv']:.3f}  adq_final={r['adq_final']}"
                f"  rec={r['rec']} (no interpretable a T=20000, ver docstring de recuperacion())  deaths={r['deaths']}"
                f"  celdas={r['celdas']}  splits={r['splits']}  m_max={r['m_stats']['max']:.4f}  ({dt:.2f}s)")
        log(f"HUMO fin, total {time.time()-t0:.1f}s. Serie completa NO se corrio (regla del --humo).")
        sys.exit(0)

    # ---- serie completa (60 corridas, T=200000, Pool(14)) ----
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    stamp = time.strftime('%Y%m%d_%H%M%S')
    os.makedirs(os.path.join(RAIZ, 'datos'), exist_ok=True)
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'metaplasticidad_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    pre = os.path.join(AQUI, 'PREREGISTRO_metaplasticidad.md')
    inst = os.path.join(CREACION_A, 'mundo_largo_A.py'); orig = os.path.join(LARGO, 'mundo_largo.py'); construye = os.path.join(CREACION_A, 'construye_largo_A.py')
    log(f"ARRANQUE metaplasticidad (nivel 8, A-2). brazos {list(BRAZOS)}, semillas {SEEDS[0]}-{SEEDS[-1]}, T={T}, T_nuevo={T_NUEVO}, inversion en {T_INV}. Pool({N_PARALELO}).")
    log(f"sha preregistro {h16(pre)}  script {h16(os.path.abspath(__file__))}  instrumento mundo_largo_A {h16(inst)}  origen mundo_largo {h16(orig)}  construye_largo_A {h16(construye)}")
    ps = _procesos_vivos()
    log(f"REGLA 11 -- procesos python vivos ({len(ps)}), este es pid {os.getpid()}")

    log("ETAPA 1/3 -- identidad mundo_largo_A(beta_m=None) == mundo_largo, s1-3, T=20000 (secuencial, sin Pool)...")
    id_ok, id_detalle = identidad(T_id=20000)
    log(f"  identicos: {sum(d['identico'] for d in id_detalle)}/3")
    for d in id_detalle:
        if not d['identico']: log(f"      DIFIERE s{d['seed']}: {d['difieren']}")
    if not id_ok:
        log("VEREDICTO metaplasticidad: INSTRUMENTO SOSPECHOSO (identidad no 3/3). Se para, la serie NO se corre.")
        _log['f'].close(); sys.exit(1)

    with mp.Pool(N_PARALELO) as pool:
        tr = [('T', b, s) for b in BRAZOS for s in SEEDS]
        log(f"ETAPA 2/3 -- {len(tr)} corridas...")
        res = []
        for i, r in enumerate(pool.imap_unordered(tarea, tr, chunksize=1), 1):
            res.append(r)
            if i % 10 == 0 or i == len(tr):
                log(f"          {i}/{len(tr)}")

    log("ETAPA 3/3 -- analisis.")
    G = lambda b: {r['seed']: r for r in res if r['brazo'] == b}
    base, b10, b50 = (G(b) for b in ('BASE', 'B10', 'B50'))
    for b in BRAZOS:
        g = G(b)
        log(f"   {b:5s} ret_no_inv {med([g[s]['ret_no_inv'] for s in SEEDS])[0]:.3f}  ret_inv {med([g[s]['ret_inv'] for s in SEEDS])[0]:.3f}"
            f"  adq_final {med([g[s]['adq_final'] for s in SEEDS])[0]:.3f}  rec {med([g[s]['rec'] for s in SEEDS])[0]:.0f}"
            f"  muertes {med([g[s]['deaths'] for s in SEEDS])[0]:.0f}  celdas {med([g[s]['celdas'] for s in SEEDS])[0]:.0f}  splits {med([g[s]['splits'] for s in SEEDS])[0]:.0f}")

    m_ret_no_inv = {b: med([G(b)[s]['ret_no_inv'] for s in SEEDS])[0] for b in BRAZOS}
    m_ret_inv    = {b: med([G(b)[s]['ret_inv']    for s in SEEDS])[0] for b in BRAZOS}
    m_adq_final  = {b: med([G(b)[s]['adq_final']  for s in SEEDS])[0] for b in BRAZOS}
    m_rec        = {b: med([G(b)[s]['rec']        for s in SEEDS])[0] for b in BRAZOS}
    m_deaths     = {b: med([G(b)[s]['deaths']     for s in SEEDS])[0] for b in BRAZOS}

    def _pareado(x, y):
        return sum((x[s]['ret_no_inv'] is not None and y[s]['ret_no_inv'] is not None and x[s]['ret_no_inv'] > y[s]['ret_no_inv']) for s in SEEDS)
    par_b50 = _pareado(b50, base); par_b10 = _pareado(b10, base)

    # -- criterios EXACTAMENTE como quedan escritos en PREREGISTRO_metaplasticidad.md SS6-8 --
    P1_mediana = m_ret_no_inv['B50'] >= 0.80
    P1 = P1_mediana and (par_b50 >= 14)
    P2 = m_adq_final['B50'] >= m_adq_final['BASE'] - 0.05
    P3 = m_rec['B50'] <= m_rec['BASE']
    B10_igual_B50 = (m_ret_no_inv['B10'] >= 0.80) and (par_b10 >= 14)
    P4 = not B10_igual_B50
    C1 = m_deaths['B50'] <= 1.5 * m_deaths['BASE']
    C2 = m_ret_inv['B50'] >= m_ret_inv['BASE'] - 0.05
    CONFIRMA = P1 and P2 and P3 and P4 and C1 and C2
    VEREDICTO = 'CONFIRMA' if CONFIRMA else 'REFUTA'

    log(f"   P1 B50 ret_no_inv mediana {m_ret_no_inv['B50']:.3f} (>=0.80 {'OK' if P1_mediana else 'NO'}), pareado>BASE {par_b50}/20 (>=14 {'OK' if par_b50>=14 else 'NO'}) -> P1 {'OK' if P1 else 'NO'}")
    log(f"   P2 adq_final BASE {m_adq_final['BASE']:.3f} B50 {m_adq_final['B50']:.3f} (no cae >0.05: {'OK' if P2 else 'NO'})")
    log(f"   P3 rec BASE {m_rec['BASE']:.0f} B50 {m_rec['B50']:.0f} (no empeora: {'OK' if P3 else 'NO'})")
    log(f"   P4 B10 ret_no_inv mediana {m_ret_no_inv['B10']:.3f}, pareado>BASE {par_b10}/20 -> {'IGUALA A B50 => RUIDO' if B10_igual_B50 else 'B10~=BASE OK'} -> P4 {'OK' if P4 else 'NO'}")
    log(f"   C1 muertes BASE {m_deaths['BASE']:.0f} B50 {m_deaths['B50']:.0f} (limite {1.5*m_deaths['BASE']:.0f}) -> {'OK' if C1 else 'NO'}")
    log(f"   C2 ret_inv BASE {m_ret_inv['BASE']:.3f} B50 {m_ret_inv['B50']:.3f} (no cae >0.05: {'OK' if C2 else 'NO'})")
    log(f"VEREDICTO metaplasticidad: {VEREDICTO}  (P1 {'OK' if P1 else 'NO'} P2 {'OK' if P2 else 'NO'} P3 {'OK' if P3 else 'NO'} P4 {'OK' if P4 else 'NO'} C1 {'OK' if C1 else 'NO'} C2 {'OK' if C2 else 'NO'})")

    V = dict(IDENTIDAD=id_ok, P1_mediana=P1_mediana, P1_pareado=par_b50, P1=P1, P2=P2, P3=P3,
              B10_igual_B50=B10_igual_B50, P4=P4, C1=C1, C2=C2, VEREDICTO=VEREDICTO,
              medianas=dict(ret_no_inv=m_ret_no_inv, ret_inv=m_ret_inv, adq_final=m_adq_final, rec=m_rec, deaths=m_deaths),
              pareado_b50_sobre_base=par_b50, pareado_b10_sobre_base=par_b10)

    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), semillas=SEEDS, T=T, T_nuevo=T_NUEVO, T_inv=T_INV, brazos=BRAZOS,
                veredictos=V, identidad_detalle=id_detalle, procesos_python=ps,
                sha_preregistro=h16(pre), sha_script=h16(os.path.abspath(__file__)), sha_instrumento=h16(inst),
                sha_origen=h16(orig), sha_construye_A=h16(construye),
                python=platform.python_version(), numpy=np.__version__)
    dj = os.path.join(RAIZ, 'datos', f'metaplasticidad_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.json')
    json.dump(dict(meta=meta, corridas=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
