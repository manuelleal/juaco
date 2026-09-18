"""Bloque 2 bis: NOVEDAD DE SITIO contra el canje exploracion/explotacion del mapa, en el mundo largo.
Ejecuta PREREGISTRO_novedad_sitio.md. REGLA 10: log desde el arranque. REGLA 11: lista los python vivos.
Identidad: mundo_largo_n con gamma_N=0 == mundo_largo (todas las claves del original, mundo completo con mapa);
la unica clave nueva permitida en el gemelo es 'nov_diag' (diagnostico, no criterio).
Uso:  python experimentos/nivel8_novedad_sitio/corre_novedad.py [--desde N]   (por defecto semillas 61-80)
"""
import sys, os, json, time, hashlib, platform, subprocess, math
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'experimentos', 'nivel8_mundo_largo'), os.path.join(RAIZ, 'experimentos', 'nivel6_mapa'), os.path.join(RAIZ, 'organismo')]
from corre_mundo_largo import pool_de, sitios_de, recuperacion, T, T_NUEVO, T_INV
_desde = int(sys.argv[sys.argv.index('--desde') + 1]) if '--desde' in sys.argv else 61
SEEDS = list(range(_desde, _desde + 20))
CLAVE_NUEVA = 'nov_diag'   # unica clave que mundo_largo_n anade al dict de mundo_largo
# Preregistro §2: los cuatro primeros son los brazos de CRITERIO; los dos ultimos son de LECTURA (no deciden veredicto).
BRAZOS = {
    'V13':           dict(usa_M=False),
    'MAPA':          dict(usa_M=True),
    'MAPA_NOV':      dict(usa_M=True, gamma_N=0.6, tau_N=4000.0),
    'MAPA_NOV_BAR':  dict(usa_M=True, gamma_N=0.6, tau_N=4000.0, nov_barajada=True),
    'MAPA_NOV_CTE':  dict(usa_M=True, gamma_N=0.6, tau_N=4000.0, nov_cte=True),
    'MAPA_NOV_ALTA': dict(usa_M=True, gamma_N=1.8, tau_N=4000.0),
}
CRITERIO = ('V13', 'MAPA', 'MAPA_NOV', 'MAPA_NOV_BAR')
ALTA = '--alta' in sys.argv   # enmienda 1: serie CONFIRMATORIA de la dosis 1.8 (vista en el brazo exploratorio) en semillas nuevas; mismos criterios
if ALTA:
    SEEDS = list(range(_desde if '--desde' in sys.argv else 81, (_desde if '--desde' in sys.argv else 81) + 20))
    BRAZOS = {'V13': dict(usa_M=False), 'MAPA': dict(usa_M=True),
              'MAPA_NOV': dict(usa_M=True, gamma_N=1.8, tau_N=4000.0), 'MAPA_NOV_BAR': dict(usa_M=True, gamma_N=1.8, tau_N=4000.0, nov_barajada=True),
              'MAPA_NOV_CTE': dict(usa_M=True, gamma_N=1.8, tau_N=4000.0, nov_cte=True)}

N_PARALELO = 14
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


def mundo_kw(seed):
    pool = pool_de(seed)
    return dict(T=T, r_vis=3, sitios=sitios_de(pool, seed), pool=pool, T_nuevo=T_NUEVO, invertir_largo=T_INV)


def visitas_de(r):
    """Lectura del mecanismo: como de repartidas quedan las visitas entre los 8 sitios (no es criterio)."""
    v = [int(x) for x in r.get('nov_diag', {}).get('visitas', {}).values()]
    if not v or sum(v) == 0:
        return dict(vis_total=0, vis_min=0, vis_max=0, eq_visitas=None, H_visitas=None, sitios_pisados=0)
    s = float(sum(v)); ps = [x / s for x in v if x > 0]
    H = -sum(x * math.log(x) for x in ps) / math.log(len(v)) if len(v) > 1 else 0.0
    return dict(vis_total=int(s), vis_min=min(v), vis_max=max(v), eq_visitas=round(min(v) / max(v), 3),
                H_visitas=round(H, 3), sitios_pisados=int(sum(1 for x in v if x > 0)))


def medidas(r, brazo, seed):
    """Las medidas del mundo largo + las dos lecturas nuevas del mecanismo. Tambien la usa el humo de un proceso."""
    cv = r['curva']
    hasta30 = [c[2] for c in cv if c[1] <= 30]; fin = cv[-1] if cv else (None, None, None, None)
    vf = r['val_final']; vs = r['vistos']; W = r['W']
    ok = lambda n: (W[n] > 0) == (vf.get(n) == 'comida')   # OJO: val_final NO trae 'C' ni 'D' (nunca entran al mundo largo) -> .get
    return dict(tipo='T', brazo=brazo, seed=seed, curva=cv, n_vistos=len(vs),
                adq_hasta30=float(np.median(hasta30)) if hasta30 else None, adq_final=fin[2],
                ret_no_inv=float(np.mean([ok(n) for n in vs[4:10]])) if len(vs) >= 10 else None,
                comida_q4=int(sum(r['mord'][k][3] for k in r['mord'] if vf.get(k) == 'comida')),
                sesgo_signo=round(float(np.mean([W[n] > 0 for n in vs])), 3) if vs else None,   # trampa 2: debe rondar 0.5
                deaths=r['deaths'], celdas=r['celdas'], splits=r['splits'], M_llenas=r['M_llenas'],
                **visitas_de(r), **recuperacion(r['comida_bin'], r['muertes_bin']))


def tarea(args):
    tipo = args[0]
    if tipo == 'I':
        _, seed = args
        import mundo_largo as a_, mundo_largo_n as b_
        kw = mundo_kw(seed); kw.update(usa_M=True)   # mundo COMPLETO, con mapa: gamma_N=0 por defecto
        a, b = a_.run(seed, **kw), b_.run(seed, **kw)
        dif = [kk for kk in a if N(a[kk]) != N(b[kk])]
        extra = sorted(set(b) - set(a))
        return dict(tipo=tipo, esc='ident', seed=seed, identico=(not dif) and extra == [CLAVE_NUEVA], difieren=dif, claves_extra=extra)
    _, brazo, seed = args
    import mundo_largo_n as m
    kw = mundo_kw(seed); kw.update(BRAZOS[brazo])
    return medidas(m.run(seed, **kw), brazo, seed)


def med(xs):
    xs = [x for x in xs if x is not None]
    if not xs:
        return (float('nan'),) * 3
    return float(np.median(xs)), float(min(xs)), float(max(xs))


if __name__ == '__main__':
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'novedad{"_alta" if ALTA else ""}_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    pre = os.path.join(AQUI, 'PREREGISTRO_novedad_sitio.md')
    log(f"ARRANQUE bloque 2 bis (NOVEDAD DE SITIO contra el canje del mapa), mundo largo. brazos {list(BRAZOS)}, semillas {SEEDS[0]}-{SEEDS[-1]}, T={T}. Pool({N_PARALELO}).")
    log(f"   criterio: {list(CRITERIO)}; lectura (no deciden): {[b for b in BRAZOS if b not in CRITERIO]}")
    log(f"sha preregistro {h16(pre)}  script {h16(os.path.abspath(__file__))}  constructor {h16(os.path.join(AQUI, 'construye_novedad.py'))}  mundo_largo_n {h16(os.path.join(AQUI, 'mundo_largo_n.py'))}  mundo_largo {h16(os.path.join(RAIZ, 'experimentos', 'nivel8_mundo_largo', 'mundo_largo.py'))}  v13 {h16(os.path.join(RAIZ, 'organismo', 'organismo_v13.py'))}")
    try:
        ps = subprocess.run(['powershell', '-NoProfile', '-Command',
                             "Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*' } | ForEach-Object { \"$($_.ProcessId) $($_.CommandLine)\" }"],
                            capture_output=True, text=True, timeout=60).stdout.strip().splitlines()
    except Exception as e:
        ps = [f"(no se pudo listar: {e})"]
    log(f"REGLA 11 - procesos python vivos ({len(ps)}), este es pid {os.getpid()}")
    V = {}
    with mp.Pool(N_PARALELO) as pool:
        ctrl = [('I', s) for s in (1, 2, 3)]
        log(f"ETAPA 1/3 - identidad gamma_N=0 == mundo_largo, mundo completo con mapa ({len(ctrl)})...")
        rc = pool.map(tarea, ctrl, chunksize=1)
        log(f"  identicos: {sum(x['identico'] for x in rc)}/{len(rc)}")
        for x in rc:
            if not x['identico']: log(f"      DIFIERE {x['esc']} s{x['seed']}: claves {x['difieren']} | extra {x['claves_extra']}")
        V['IDENTIDAD'] = all(x['identico'] for x in rc)
        if not V['IDENTIDAD']:
            log("*** IDENTIDAD FALLIDA: se para."); sys.exit(1)
        tr = [('T', b, s) for b in BRAZOS for s in SEEDS]
        log(f"ETAPA 2/3 - {len(tr)} corridas...")
        res = []
        for i, r in enumerate(pool.imap_unordered(tarea, tr, chunksize=1), 1):
            res.append(r)
            if i % 20 == 0 or i == len(tr):
                log(f"          {i}/{len(tr)}")
    log("ETAPA 3/3 - analisis.")
    GG = {b: {r['seed']: r for r in res if r['brazo'] == b} for b in BRAZOS}
    A = lambda b, s: (GG[b][s]['adq_hasta30'] if (s in GG[b] and GG[b][s]['adq_hasta30'] is not None) else 0.0)
    CQ = lambda b, s: (GG[b][s]['comida_q4'] if s in GG[b] else 0)
    faltan = {b: sorted(s for s in SEEDS if s not in GG[b]) for b in BRAZOS}
    nulos = {b: sum(1 for s in SEEDS if s in GG[b] and GG[b][s]['adq_hasta30'] is None) for b in BRAZOS}
    V.update(corridas_faltantes=faltan, adq_nulos=nulos)
    if any(faltan.values()) or any(nulos.values()):   # una medida vacia se cuenta como 0.0 en A(): que no pase callando
        log(f"   *** OJO: corridas faltantes {faltan} | adq_hasta30 nulos por brazo {nulos}. Los pareados cuentan esas semillas como 0.0.")
    for b in BRAZOS:
        g = list(GG[b].values())
        log(f"   {b:14s} adq(<=30) {med([r['adq_hasta30'] for r in g])[0]:.3f} [{med([r['adq_hasta30'] for r in g])[1]:.2f},{med([r['adq_hasta30'] for r in g])[2]:.2f}]  adq(final) {med([r['adq_final'] for r in g])[0]:.3f}"
            f"  ret_no_inv {med([r['ret_no_inv'] for r in g])[0]:.2f}  comida_q4 {med([r['comida_q4'] for r in g])[0]:.0f}  muertes {med([r['deaths'] for r in g])[0]:.0f}"
            f"  recup {med([r['rec'] for r in g])[0]:.0f}  celdas {med([r['celdas'] for r in g])[0]:.0f}  M_llenas {med([r['M_llenas'] for r in g])[0]:.0f}"
            f"  | visitas {med([r['vis_total'] for r in g])[0]:.0f} eq {med([r['eq_visitas'] for r in g])[0]:.3f} H {med([r['H_visitas'] for r in g])[0]:.3f} pisados {med([r['sitios_pisados'] for r in g])[0]:.0f}"
            f"  | sesgo_signo {med([r['sesgo_signo'] for r in g])[0]:.2f}")
    for b in ('V13', 'MAPA', 'MAPA_NOV'):
        pts = {}
        for r in GG[b].values():
            for t_, nv, a_, p_ in r['curva']: pts.setdefault(nv, []).append(a_)
        log(f"   curva {b}: " + " ".join(f"{nv}:{np.median(v):.2f}" for nv, v in sorted(pts.items()) if nv % 5 == 0 or nv == 50))

    def pareado(b1, b2):
        """> estricto; los empates se reportan SIEMPRE (ERR-17). Desempate preregistrado (preregistro §3), solo si hay empates."""
        gana = sum(A(b1, s) > A(b2, s) for s in SEEDS); emp = sum(A(b1, s) == A(b2, s) for s in SEEDS)
        pier = len(SEEDS) - gana - emp
        directo = gana >= 15
        desemp = (not directo) and emp > 0 and (gana + pier) >= 8 and gana >= 0.75 * (gana + pier)
        return dict(par=f"{b1}>{b2}", gana=gana, empata=emp, pierde=pier, ok=bool(directo or desemp), por_desempate=bool(desemp))

    m_nov = med([A('MAPA_NOV', s) for s in SEEDS])[0]
    nm, nb, bm, nc = pareado('MAPA_NOV', 'MAPA'), pareado('MAPA_NOV', 'MAPA_NOV_BAR'), pareado('MAPA_NOV_BAR', 'MAPA'), pareado('MAPA_NOV', 'MAPA_NOV_CTE')
    P1 = bool(m_nov >= 0.85 and nm['ok'])
    p2n = sum(CQ('MAPA_NOV', s) >= 0.9 * CQ('MAPA', s) for s in SEEDS)
    P2 = bool(p2n >= 15)
    P3 = bool(nb['ok'] and not bm['ok'] and med([A('MAPA_NOV_BAR', s) for s in SEEDS])[0] < 0.85)
    P4 = bool(nc['ok'] and med([A('MAPA_NOV_CTE', s) for s in SEEDS])[0] < 0.85)
    V.update(P1=P1, P2=P2, P3=P3, P4_lectura=P4, P2_n=int(p2n), adq_nov=m_nov, pareados=[nm, nb, bm, nc],
             DEVUELVE_EXPLORACION=bool(P1 and P2 and P3), LIMPIO=bool(P1 and P2 and P3 and P4))
    log(f"   P1 NOV adq {m_nov:.3f} (>=0.85) y >MAPA {nm['gana']}g/{nm['empata']}e/{nm['pierde']}p{' [desempate]' if nm['por_desempate'] else ''} -> {'OK' if P1 else 'NO'}")
    log(f"   P2 comida_q4 >=0.9xMAPA en {p2n}/20 -> {'OK' if P2 else 'NO'}   (referencia informativa 41-60: MAPA 968, V13 837; aqui MAPA {med([CQ('MAPA', s) for s in SEEDS])[0]:.0f}, NOV {med([CQ('MAPA_NOV', s) for s in SEEDS])[0]:.0f})")
    log(f"   P3 NOV>BARAJADA {nb['gana']}g/{nb['empata']}e/{nb['pierde']}p{' [desempate]' if nb['por_desempate'] else ''} y BARAJADA>MAPA {bm['gana']}g/{bm['empata']}e/{bm['pierde']}p (no debe pasar) -> {'OK' if P3 else 'NO'}")
    log(f"   P4 (lectura) NOV>CONSTANTE {nc['gana']}g/{nc['empata']}e/{nc['pierde']}p{' [desempate]' if nc['por_desempate'] else ''} -> {'OK' if P4 else 'NO'}")
    if 'MAPA_NOV_ALTA' in BRAZOS: log(f"   dosis (exploratoria, NO decide): MAPA_NOV_ALTA adq {med([A('MAPA_NOV_ALTA', s) for s in SEEDS])[0]:.3f}  comida_q4 {med([CQ('MAPA_NOV_ALTA', s) for s in SEEDS])[0]:.0f}  muertes {med([r['deaths'] for r in GG['MAPA_NOV_ALTA'].values()])[0]:.0f}")
    log(f"VEREDICTO novedad de sitio: {'DEVUELVE la exploracion sin cobrar la comida' if V['DEVUELVE_EXPLORACION'] else 'NO (refutado o control caido)'}"
        f"{'' if V['LIMPIO'] or not V['DEVUELVE_EXPLORACION'] else ' -- OJO: P4 (control de novedad constante) NO pasa: revisar si es sesgo extra'}")
    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), semillas=SEEDS, T=T, T_nuevo=T_NUEVO, T_inv=T_INV, brazos=BRAZOS, brazos_criterio=list(CRITERIO),
                veredictos=V, identidades=rc, procesos_python=ps, sha_preregistro=h16(pre), sha_script=h16(os.path.abspath(__file__)),
                sha_constructor=h16(os.path.join(AQUI, 'construye_novedad.py')), sha_mundo=h16(os.path.join(AQUI, 'mundo_largo_n.py')),
                sha_mundo_largo=h16(os.path.join(RAIZ, 'experimentos', 'nivel8_mundo_largo', 'mundo_largo.py')),
                python=platform.python_version(), numpy=np.__version__)
    dj = os.path.join(RAIZ, 'datos', f'novedad{"_alta" if ALTA else ""}_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.json')
    json.dump(dict(meta=meta, corridas=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
