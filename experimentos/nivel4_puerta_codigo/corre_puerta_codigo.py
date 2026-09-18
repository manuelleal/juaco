"""Nivel 4 — PUERTA DE FAMILIARIDAD POR EVIDENCIA DEL CODIGO EXACTO (propuesta B-2 del creador B).
Ejecuta PREREGISTRO_puerta_codigo.md. Montaje del BLOQUE K identico a experimentos/v13_reverificacion/
corre_reverificacion_v13.py (mundo_grande D=10, 60 estimulos, paso_t 20000 y 60000, semillas 41-60).
REGLA 10: log desde el arranque con fsync. REGLA 11: procesos vivos al log.

Etapa 1 INERCIA (aborta si no es total): capB y v13B con las perillas apagadas == sus originales, todas las claves.
Etapa 2 BLOQUE K: capacidad. Etapa 3 analisis Q1-Q3 y S2. Etapa 4 BLOQUE G: baterias (subprocesos, fuera del Pool).

Uso:  python experimentos/nivel4_puerta_codigo/corre_puerta_codigo.py [--desde 41] [--humo] [--sin-g]
      --humo  = un proceso, sin Pool, 2 semillas, mundo reducido (20 estimulos, paso 4000) y baterias de 2 semillas.
"""
import sys, os, json, time, hashlib, platform, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
# OJO (trampa real, hallada en el humo): experimentos/v13_dos_vias/ tiene SU PROPIO organismo_v13.py
# (88c3574cf9cf38bf) distinto del tronco congelado (cc8b16b492d4d324). `organismo/` va PRIMERO, siempre.
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo'),
                os.path.join(RAIZ, 'experimentos', 'v13_reverificacion'),
                os.path.join(RAIZ, 'experimentos', 'capacidad_grande'),
                os.path.join(RAIZ, 'experimentos', 'v11_evo_division')]
import mundo_grande as G

HUMO = '--humo' in sys.argv
SIN_G = '--sin-g' in sys.argv
_desde = int(sys.argv[sys.argv.index('--desde') + 1]) if '--desde' in sys.argv else 41
SEEDS = list(range(_desde, _desde + (2 if HUMO else 20)))
D_PIX = 10
N_EST = 20 if HUMO else 60
PASOS = (4000,) if HUMO else (20000, 60000)
SEM_BAT = 2 if HUMO else 20
DESDE_BAT = 101
N_PARALELO = 14

BASE = dict(plast=True, lam=0.05, memoria_rechazo=20, mu_norm=True, div_signo=True)
BRAZOS = {
    'v11':     dict(),                                                        # referencia alta de capacidad
    'v13':     dict(eta_s=0.015, puerta=3),                                   # el tronco: referencia baja
    'PAT':     dict(eta_s=0.015, puerta=3, puerta_pat=5),                     # la propuesta
    'PATC':    dict(eta_s=0.015, puerta=3, puerta_pat=5, pat_min=1),          # enmienda 1: evidencia Y una celda consolidada
    'PATSHUF': dict(eta_s=0.015, puerta=3, puerta_pat=5, pat_shuf=1),         # control: contadores barajados
}
NUEVAS = {'puerta_pat', 'pat_shuf', 'pat_min', 'n_cod', 'nofam_est', 'ncod_est'}
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


def tarea(args):
    tipo = args[0]
    if tipo == 'IK':   # capB con perillas apagadas == capD13
        _, n_est, pt, cfg, seed = args
        import organismo_capD13 as a_, organismo_capB as b_
        nom, pats, val, R = G.mundo(D_PIX, n_est)
        kw = dict(T=G.T_de(pt, n_est), plan=G.plan_de(pt, nom, val), pats=pats, chk=G.chks(pt, n_est))
        a = a_.run(seed, **kw, **BASE, **cfg)
        b = b_.run(seed, **kw, **BASE, **cfg, puerta_pat=0, pat_shuf=0, pat_min=0)
        dif = [k for k in a if k not in NUEVAS and N(a[k]) != N(b[k])]
        return dict(tipo=tipo, esc=f"capB n={n_est} {cfg or 'v11'}", seed=seed, identico=not dif, difieren=dif)
    if tipo == 'IV':   # v13B con perillas apagadas == organismo_v13 (congelado)
        _, seed = args
        import organismo_v13 as a_, organismo_v13B as b_
        a = a_.run(seed); b = b_.run(seed, puerta_pat=0, pat_shuf=0, pat_min=0)
        dif = [k for k in a if k not in NUEVAS and N(a[k]) != N(b[k])]
        return dict(tipo=tipo, esc='v13B == organismo_v13', seed=seed, identico=not dif, difieren=dif)
    _, brazo, pt, seed = args
    import organismo_capB as o
    nom, pats, val, R = G.mundo(D_PIX, N_EST)
    r = o.run(seed, T=G.T_de(pt, N_EST), plan=G.plan_de(pt, nom, val), pats=pats, chk=G.chks(pt, N_EST),
              **BASE, **BRAZOS[brazo])
    for h in r['hist']:
        h['dev'] = {k: round(abs(v - R[k]), 3) for k, v in h['W'].items()}
    hist = [dict(t=h['t'], n=h['n'], celdas=h['celdas'], splits=h['splits'], dev=h['dev']) for h in r['hist']]
    nf = r.get('nofam_est', {}); ev = r.get('ncod_est', {})
    mal = sum(1 for k, v in nf.items() if v and ev.get(k, 0) >= 5)   # Q3: mandados a la lenta con evidencia >= n0
    return dict(tipo='K', brazo=brazo, pt=pt, seed=seed, hist=hist, deaths=r['deaths'], t_agot=r['t_agot'],
                splits=r['splits'], celdas=r['celdas'], nofam=int(sum(nf.values())), mal_ruteados=mal,
                n_cod=r.get('n_cod'), W_fin={k: round(float(v), 4) for k, v in r['W'].items()})


def med(xs):
    xs = list(xs)
    return float(np.median(xs)), float(min(xs)), float(max(xs))


if __name__ == '__main__':
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    stamp = time.strftime('%Y%m%d_%H%M%S')
    nom_sal = f'puerta_codigo{"_humo" if HUMO else ""}_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}'
    _log['f'] = open(os.path.join(RAIZ, 'datos', nom_sal + '.log'), 'w', encoding='utf-8', newline='\n')
    pre = os.path.join(AQUI, 'PREREGISTRO_puerta_codigo.md')
    shas = {n_: h16(p) for n_, p in [
        ('preregistro', pre), ('script', os.path.abspath(__file__)),
        ('constructor', os.path.join(AQUI, 'construye_puerta_codigo.py')),
        ('organismo_capB', os.path.join(AQUI, 'organismo_capB.py')),
        ('organismo_v13B', os.path.join(AQUI, 'organismo_v13B.py')),
        ('organismo_v13gB', os.path.join(AQUI, 'organismo_v13gB.py')),
        ('bateria_generaliza_B', os.path.join(AQUI, 'bateria_generaliza_B.py')),
        ('bateria_v13B', os.path.join(AQUI, 'bateria_v13B.py')),
        ('bateria_v13Bc', os.path.join(AQUI, 'bateria_v13Bc.py')),
        ('origen organismo_v13 (congelado)', os.path.join(RAIZ, 'organismo', 'organismo_v13.py')),
        ('origen capD13', os.path.join(RAIZ, 'experimentos', 'v13_reverificacion', 'organismo_capD13.py'))]}
    log(f"ARRANQUE PUERTA POR CODIGO (propuesta B-2). mundo D={D_PIX} n_est={N_EST} pasos={PASOS} "
        f"semillas {SEEDS[0]}-{SEEDS[-1]}, brazos {list(BRAZOS)}. {'HUMO (un proceso, sin Pool)' if HUMO else f'Pool({N_PARALELO})'}")
    log("sha " + "  ".join(f"{k} {v}" for k, v in shas.items()))
    try:
        ps = subprocess.run(['powershell', '-NoProfile', '-Command',
                             "Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*' } | ForEach-Object { \"$($_.ProcessId) $($_.CommandLine)\" }"],
                            capture_output=True, text=True, timeout=60).stdout.strip().splitlines()
    except Exception as e:
        ps = [f"(no se pudo listar: {e})"]
    log(f"REGLA 11 — procesos python vivos ({len(ps)}), este es pid {os.getpid()}")

    ctrl = ([('IK', 12, 3000, dict(eta_s=0.015, puerta=3), SEEDS[0]),
             ('IK', 12, 3000, dict(), SEEDS[0]),
             ('IK', 20, 2000, dict(eta_s=0.015, puerta=2), SEEDS[-1])]
            + [('IV', s) for s in (1, 2, 3)])
    tr = [('K', b, pt, s) for pt in sorted(PASOS, reverse=True) for b in BRAZOS for s in SEEDS]
    V = {}

    def corre(lote, etiqueta, pool):
        log(f"{etiqueta} ({len(lote)})...")
        if pool is None:
            out = []
            for i, x in enumerate(lote, 1):
                out.append(tarea(x))
                if i % 5 == 0 or i == len(lote): log(f"          {i}/{len(lote)}")
            return out
        out = []
        for i, r in enumerate(pool.imap_unordered(tarea, lote, chunksize=1), 1):
            out.append(r)
            if i % 20 == 0 or i == len(lote): log(f"          {i}/{len(lote)}")
        return out

    pool = None if HUMO else mp.Pool(N_PARALELO)
    try:
        rc = corre(ctrl, "ETAPA 1/4 — INERCIA (perillas apagadas == originales)", pool)
        log(f"  identicos: {sum(x['identico'] for x in rc)}/{len(rc)}")
        for x in rc:
            if not x['identico']: log(f"      DIFIERE {x['esc']} s{x['seed']}: {x['difieren'][:6]}")
        V['INERCIA'] = all(x['identico'] for x in rc)
        if not V['INERCIA']:
            log("*** INERCIA FALLIDA: se para (S4 del preregistro)."); _log['f'].close(); sys.exit(1)
        res = corre(tr, f"ETAPA 2/4 — BLOQUE K, capacidad ({len(tr)} corridas largas)", pool)
    finally:
        if pool is not None:
            pool.close(); pool.join()

    log("ETAPA 3/4 — analisis del bloque K (criterios del preregistro, sin recalibrar).")
    GK = lambda b, pt: {r['seed']: r for r in res if r['brazo'] == b and r['pt'] == pt}
    tab = {}
    for pt in sorted(PASOS, reverse=True):
        log(); log(f"  paso_t = {pt}")
        for b in BRAZOS:
            g = GK(b, pt)
            Ns = [G.techo(g[s]['hist']) for s in SEEDS]; Ms = [G.m_max(g[s]['hist']) for s in SEEDS]
            tab[(b, pt)] = dict(N=med(Ns)[0], Nmin=med(Ns)[1], Nmax=med(Ns)[2], M=med(Ms)[0],
                                celdas=med(g[s]['celdas'] for s in SEEDS)[0],
                                splits=med(g[s]['splits'] for s in SEEDS)[0],
                                nofam=med(g[s]['nofam'] for s in SEEDS)[0],
                                mal=med(g[s]['mal_ruteados'] for s in SEEDS)[0],
                                muertes=med(g[s]['deaths'] for s in SEEDS)[0], Ns=Ns)
            t = tab[(b, pt)]
            log(f"   {b:8s} N* {t['N']:.1f} [{t['Nmin']:.0f},{t['Nmax']:.0f}]  M_max {t['M']:.1f}  celdas {t['celdas']:.0f}"
                f"  divisiones {t['splits']:.0f}  a la lenta {t['nofam']:.0f}/{N_EST}  mal ruteados {t['mal']:.0f}"
                f"  muertes {t['muertes']:.0f}")
        for cand in ('PAT', 'PATC'):
            n_q1 = sum(tab[(cand, pt)]['Ns'][i] > tab[('v13', pt)]['Ns'][i] for i in range(len(SEEDS)))
            umb_n = {20000: 45, 60000: 48}.get(pt, 0)
            q1 = tab[(cand, pt)]['N'] >= umb_n and n_q1 >= (1 if HUMO else 15)
            q2 = (abs(tab[(cand, pt)]['celdas'] - tab[('v13', pt)]['celdas']) <= 2 and
                  abs(tab[(cand, pt)]['splits'] - tab[('v13', pt)]['splits']) <= 2)
            q3 = tab[(cand, pt)]['nofam'] <= 2 and tab[(cand, pt)]['mal'] == 0
            n_s2 = sum(tab[(cand, pt)]['Ns'][i] > tab[('PATSHUF', pt)]['Ns'][i] for i in range(len(SEEDS)))
            s2 = not (abs(tab[(cand, pt)]['N'] - tab[('PATSHUF', pt)]['N']) <= 2 and n_s2 < (1 if HUMO else 14))
            V[f'{cand}_{pt}'] = dict(Q1=bool(q1), Q1_n=n_q1, Q1_umbral=umb_n, Q2=bool(q2), Q3=bool(q3),
                                     S2_sobrevive_al_barajado=bool(s2), S2_n=n_s2)
            log(f"   {cand}: Q1 N*>={umb_n} y >v13 en {n_q1}/{len(SEEDS)} {'OK' if q1 else 'NO'} | Q2 celdas/divisiones +-2 {'OK' if q2 else 'NO'}"
                f" | Q3 a la lenta<=2 y 0 mal ruteados {'OK' if q3 else 'NO'} | S2 > PATSHUF en {n_s2}/{len(SEEDS)} {'OK' if s2 else 'CAE'}")

    if not SIN_G:
        log(); log("ETAPA 4/4 — BLOQUE G: generalizacion y retencion (subprocesos secuenciales, fuera del Pool).")
        env = dict(os.environ, PYTHONIOENCODING='utf-8')
        G_OUT = {}
        for etiq, cmd in [
            ('generaliza PAT',  [sys.executable, os.path.join(AQUI, 'bateria_generaliza_B.py'), 'organismo_v13B_n5', str(SEM_BAT), '--desde', str(DESDE_BAT), '--log']),
            ('generaliza PATC', [sys.executable, os.path.join(AQUI, 'bateria_generaliza_B.py'), 'organismo_v13B_n5c', str(SEM_BAT), '--desde', str(DESDE_BAT), '--log']),
            ('retencion PAT',   [sys.executable, os.path.join(AQUI, 'bateria_v13B.py'), str(SEM_BAT), '--desde', str(DESDE_BAT), '--log']),
            ('retencion PATC',  [sys.executable, os.path.join(AQUI, 'bateria_v13Bc.py'), str(SEM_BAT), '--desde', str(DESDE_BAT), '--log']),
        ]:
            log(f"  -> {etiq} ...")
            p = subprocess.run(cmd, capture_output=True, text=True, env=env, cwd=os.path.join(RAIZ, 'organismo'))
            lin = [l.split('] ', 1)[-1].strip() for l in p.stdout.splitlines()
                   if ('PASA' in l or 'FALLA' in l or 'VEREDICTO' in l or '***' in l)]
            G_OUT[etiq] = dict(returncode=p.returncode, lineas=lin)
            for l in lin[-6:]: log(f"     {l}")
            if p.returncode != 0: log(f"     *** codigo {p.returncode}: {p.stderr[-400:]}")
        V['BLOQUE_G'] = G_OUT

    log(); log("VEREDICTO PUERTA_CODIGO — el bloque lo decide S1 (generalizacion) por encima de Q1 (capacidad):")
    log("  " + json.dumps({k: v for k, v in V.items() if k != 'BLOQUE_G'}, ensure_ascii=False)[:1200])
    if HUMO:
        log("(HUMO: 2 semillas, mundo reducido y baterias de 2 semillas — ningun umbral vale; solo prueba el montaje.)")
    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), humo=HUMO, semillas=SEEDS, n_est=N_EST, pasos=list(PASOS),
                brazos=BRAZOS, veredictos=V, identidades=rc, tabla_K={f"{b}_{pt}": v for (b, pt), v in tab.items()},
                shas=shas, procesos_python=ps, python=platform.python_version(), numpy=np.__version__)
    dj = os.path.join(RAIZ, 'datos', nom_sal + '.json')
    json.dump(dict(meta=meta, corridas=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
