"""Nivel 6, peldano siguiente: DOS METAS Y RODEO. Ejecuta PREREGISTRO_rodeo.md.
REGLA 10: log desde el arranque. REGLA 11: lista los python vivos antes de abrir el Pool.
Identidad (etapa 1, se para si falla): mundo_mapa_rodeo == mundo_mapa en los SEIS brazos de corre_mapa.py, semillas 1-3
(18 comparaciones, todas las claves); y con las perillas apagadas == organismo_v13, 3 semillas x 3 escenarios (9).
Uso:  python experimentos/nivel6_rodeo/corre_rodeo.py [--desde N]      (por defecto semillas 41-60, Pool: SOLO el coordinador)
      python experimentos/nivel6_rodeo/corre_rodeo.py --humo           (un proceso: identidad 1 semilla + MAPA en 41 y 42)
"""
import sys, os, json, time, hashlib, platform, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
MAPA_DIR = os.path.join(RAIZ, 'experimentos', 'nivel6_mapa')
sys.path[:0] = [AQUI, MAPA_DIR, os.path.join(RAIZ, 'organismo')]
_desde = int(sys.argv[sys.argv.index('--desde') + 1]) if '--desde' in sys.argv else 41
SEEDS = list(range(_desde, _desde + 20))
HUMO = '--humo' in sys.argv

T = 100000
MUNDO = dict(T=T, r_vis=3, sitios=('A', 'B', 'A'))
PRUEBA = dict(modo='rodeo', n_tel=40, E_test=0.3, max_pasos=60, g1=5, g2=20, dps=(4, 5, 6, 7), aas=(4, 5, 6, 7))
BRAZOS = {                                                                   # preregistro seccion 3
    'MAPA':      dict(usa_M=True, prueba=dict(PRUEBA)),
    'SINMAPA':   dict(usa_M=False, prueba=dict(PRUEBA)),
    'INVERTIDO': dict(usa_M=True, prueba=dict(PRUEBA, invertir=True)),
    'CONGELADA': dict(usa_M=True, escribe_M=False, prueba=dict(PRUEBA)),
}
# Identidad: los seis brazos de corre_mapa.py, tal cual (mundo del mapa, prueba del mapa).
MUNDO_MAPA = dict(T=T, r_vis=3, sitios=('A', 'B'))
PRUEBA_MAPA = dict(n_tel=40, E_test=0.3, max_pasos=30)
BRAZOS_MAPA = {
    'MAPA':      dict(usa_M=True, prueba=dict(PRUEBA_MAPA)),
    'SINMAPA':   dict(usa_M=False, prueba=dict(PRUEBA_MAPA)),
    'CONGELADA': dict(usa_M=True, escribe_M=False, prueba=dict(PRUEBA_MAPA)),
    'BARAJADO':  dict(usa_M=True, prueba=dict(PRUEBA_MAPA, barajar=True)),
    'SINCOMIDA': dict(usa_M=True, prueba=dict(PRUEBA_MAPA), sitios=('B', 'B')),
    'INVERTIDO': dict(usa_M=True, prueba=dict(PRUEBA_MAPA, invertir=True)),
}
IDENT_V13 = [dict(), dict(invertir_en=50000), dict(nuevo='C')]
UMBRAL_V0 = -0.308   # preregistro 5: rodea en las cuatro distancias si v_B < -0.308 * v_A (el caso dp=4)
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


def tarea(args):
    tipo = args[0]
    if tipo == 'IM':   # identidad contra mundo_mapa en un brazo de corre_mapa
        _, brazo, seed, t_id = args
        import mundo_mapa as a_, mundo_mapa_rodeo as b_
        kw = dict(MUNDO_MAPA); kw.update(BRAZOS_MAPA[brazo]); kw['T'] = t_id
        a, b = a_.run(seed, **kw), b_.run(seed, **kw)
        dif = [kk for kk in a if N(a[kk]) != N(b[kk])] + [kk for kk in b if kk not in a]
        return dict(tipo=tipo, esc=f'mapa:{brazo}', seed=seed, identico=not dif, difieren=dif)
    if tipo == 'IV':   # identidad con las perillas apagadas contra el tronco
        _, i, seed, t_id = args
        import organismo_v13 as a_, mundo_mapa_rodeo as b_
        kw = dict(IDENT_V13[i]); kw['T'] = t_id
        a, b = a_.run(seed, **kw), b_.run(seed, **kw)
        # v13 no tiene las dos claves que ya anadia mundo_mapa; el resto tiene que ser identico y no puede haber mas.
        dif = [kk for kk in a if N(a[kk]) != N(b[kk])] + [kk for kk in b if kk not in a and kk not in ('tel', 'M_llenas')]
        if b.get('tel') is not None or b.get('M_llenas') != 0: dif.append('perillas_no_apagadas')
        return dict(tipo=tipo, esc=f'v13:{i}', seed=seed, identico=not dif, difieren=dif)
    _, brazo, seed = args
    import mundo_mapa_rodeo as m
    kw = dict(MUNDO); kw.update(BRAZOS[brazo])
    r = m.run(seed, **kw)
    return dict(tipo='T', brazo=brazo, seed=seed, tel=r['tel'], M_llenas=r['M_llenas'], W=r['W'], deaths=r['deaths'],
                mord=r['mord'], splits=r['splits'], celdas=r['celdas'])


def G(r, k, alt=None):
    """Guardia None: la prueba pudo no dar ningun caso valido (todos 'sin mover')."""
    t = r.get('tel') if isinstance(r, dict) else None
    if not t:
        return alt
    v = t.get(k)
    return alt if v is None else v


def med(xs):
    xs = [x for x in xs if x is not None]
    if not xs:
        return (None, None, None)
    return float(np.median(xs)), float(min(xs)), float(max(xs))


def F(x, n=3):
    """Guardia None tambien al imprimir: que el analisis no reviente despues de 80 corridas."""
    return 'na' if x is None else f"{x:.{n}f}"


def resume(b, g):
    r1 = [G(r, 'R1', 0.5) for r in g]; r2 = [G(r, 'R2', 0.5) for r in g]
    M = lambda k, alt=0: med([G(r, k, alt) for r in g])[0]
    m1, mn1, mx1 = med(r1)
    return (f"   {b:9s} R1 {F(m1)} [{F(mn1,2)},{F(mx1,2)}] (>0.70 en {sum(x > 0.70 for x in r1)}/{len(r1)})  R2 {F(med(r2)[0])}"
            f"  llega_limpio {F(M('llega_limpio', 0.0))}  sin_mover {F(M('sin_mover'),0)}/40"
            f"  ciego {F(M('ciego_al_llegar'),0)}/40  pisa {F(M('pisa_total'),0)}"
            f"  M_llenas {F(med([r['M_llenas'] for r in g])[0],0)}  v_A {F(M('v_A', 0.0),2)}"
            f"  v_B {F(M('v_B', 0.0),2)}  mec_rodeo {F(M('mec_rodeo', 0.0),2)}"
            f"  muertes {F(med([r['deaths'] for r in g])[0],0)}")


def humo():
    """Humo de un proceso (regla 3): identidad en 1 semilla + MAPA con la prueba de rodeo en 41 (or=+1) y 42 (espejo)."""
    log("HUMO de un proceso (sin Pool). Identidad 1 semilla (T=10000) + 2 corridas MAPA de 100000.")
    log(f"sha mundo_mapa {h16(os.path.join(MAPA_DIR,'mundo_mapa.py'))}  mundo_mapa_rodeo {h16(os.path.join(AQUI,'mundo_mapa_rodeo.py'))}")
    rc = [tarea(('IM', b, 1, 10000)) for b in BRAZOS_MAPA] + [tarea(('IV', i, 1, 10000)) for i in range(len(IDENT_V13))]
    for x in rc:
        if not x['identico']: log(f"   DIFIERE {x['esc']} s{x['seed']}: {x['difieren']}")
    log(f"   identidad (6 brazos de corre_mapa + 3 escenarios de v13, semilla 1): {sum(x['identico'] for x in rc)}/{len(rc)}")
    for s in (41, 42):
        t0 = time.time(); r = tarea(('T', 'MAPA', s)); t = r['tel']
        log(f"   MAPA s{s} ({time.time()-t0:.1f}s) orientacion {t['orientacion']} sitios {t['sitios']} g {t['g']}")
        log(f"      R1 {t['R1']} (n {t['n_rodeo']})  R2 {t['R2']} (n {t['n_atajo']})  llega_limpio {t['llega_limpio']}  llega {t['llega']}"
            f"  come F1/F2 {t['come_F1']}/{t['come_F2']}  pisa {t['pisa_total']}  sin_mover {t['sin_mover']}  ciego {t['ciego_al_llegar']}/40")
        log(f"      v_A {t['v_A']}  v_B {t['v_B']}  V0 (v_B < {UMBRAL_V0}*v_A) {'OK' if t['v_B'] < UMBRAL_V0*t['v_A'] else 'NO'}"
            f"  mec_rodeo {t['mec_rodeo']}  mec_atajo {t['mec_atajo']}  M_llenas {r['M_llenas']}  W {r['W']}  muertes {r['deaths']}")
    log("HUMO hecho. Los numeros son de UNA semilla por orientacion: no son el resultado, y nada se recalibra con ellos.")


if __name__ == '__main__':
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f"rodeo_{'humo' if HUMO else f's{SEEDS[0]}-{SEEDS[-1]}'}_{stamp}.log"), 'w', encoding='utf-8', newline='\n')
    if HUMO:
        humo(); _log['f'].close(); sys.exit(0)
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    pre = os.path.join(AQUI, 'PREREGISTRO_rodeo.md')
    log(f"ARRANQUE nivel 6 (dos metas y rodeo) sobre v13. brazos {list(BRAZOS)}, semillas {SEEDS[0]}-{SEEDS[-1]}. Pool({N_PARALELO}).")
    log(f"sha preregistro {h16(pre)}  script {h16(os.path.abspath(__file__))}  mundo_mapa_rodeo {h16(os.path.join(AQUI, 'mundo_mapa_rodeo.py'))}"
        f"  mundo_mapa {h16(os.path.join(MAPA_DIR, 'mundo_mapa.py'))}  v13 {h16(os.path.join(RAIZ, 'organismo', 'organismo_v13.py'))}")
    try:
        ps = subprocess.run(['powershell', '-NoProfile', '-Command',
                             "Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*' } | ForEach-Object { \"$($_.ProcessId) $($_.CommandLine)\" }"],
                            capture_output=True, text=True, timeout=60).stdout.strip().splitlines()
    except Exception as e:
        ps = [f"(no se pudo listar: {e})"]
    log(f"REGLA 11 — procesos python vivos ({len(ps)}), este es pid {os.getpid()}")
    V = {}
    with mp.Pool(N_PARALELO) as pool:
        ctrl = [('IM', b, s, T) for b in BRAZOS_MAPA for s in (1, 2, 3)] + [('IV', i, s, T) for i in range(len(IDENT_V13)) for s in (1, 2, 3)]
        log(f"ETAPA 1/3 — identidad: {len(ctrl)} comparaciones (18 contra mundo_mapa, 9 contra organismo_v13)...")
        rc = pool.map(tarea, ctrl, chunksize=1)
        log(f"  identicos: {sum(x['identico'] for x in rc)}/{len(rc)}")
        for x in rc:
            if not x['identico']: log(f"      DIFIERE {x['esc']} s{x['seed']}: {x['difieren']}")
        V['IDENTIDAD'] = all(x['identico'] for x in rc)
        if not V['IDENTIDAD']:
            log("*** IDENTIDAD FALLIDA: se para."); sys.exit(1)
        tr = [('T', b, s) for b in BRAZOS for s in SEEDS]
        log(f"ETAPA 2/3 — {len(tr)} corridas...")
        res = []
        for i, r in enumerate(pool.imap_unordered(tarea, tr, chunksize=1), 1):
            res.append(r)
            if i % 20 == 0 or i == len(tr):
                log(f"          {i}/{len(tr)}")
    log("ETAPA 3/3 — analisis.")
    por = {b: {r['seed']: r for r in res if r['brazo'] == b} for b in BRAZOS}
    for b in BRAZOS:
        log(resume(b, [por[b][s] for s in SEEDS]))
    mapa, sinm, inv, cong = (por[b] for b in ('MAPA', 'SINMAPA', 'INVERTIDO', 'CONGELADA'))
    r1m = [G(mapa[s], 'R1', 0.5) for s in SEEDS]
    par = sum(G(mapa[s], 'R1', 0.5) > G(sinm[s], 'R1', 0.5) for s in SEEDS)
    R1 = med(r1m)[0] >= 0.70 and par >= 15
    R2 = med([G(mapa[s], 'R2', 0.5) for s in SEEDS])[0] >= 0.70
    R3 = med([G(inv[s], 'R1', 0.5) for s in SEEDS])[0] <= 0.35
    R4 = med([G(mapa[s], 'llega_limpio', 0.0) for s in SEEDS])[0] >= 0.60
    v0n = sum(1 for s in SEEDS if G(mapa[s], 'v_B', 0.0) < UMBRAL_V0 * G(mapa[s], 'v_A', 0.0))
    V0 = v0n >= 18
    V1 = all(mapa[s]['M_llenas'] == 3 and inv[s]['M_llenas'] == 3 and cong[s]['M_llenas'] == 0 for s in SEEDS)
    V2 = all(G(por[b][s], 'ciego_al_llegar', 0) == 40 for b in BRAZOS for s in SEEDS)
    V3 = all(N(sinm[s]['tel']) == N(cong[s]['tel']) for s in SEEDS)
    V.update(R1=R1, R1_pareado=par, R2=R2, R3=R3, R4=R4, V0=V0, V0_n=v0n, V1=V1, V2=V2, V3=V3,
             RODEA=bool(R1 and R2 and R3 and R4))
    log(f"   R1 rodeo>=.70 y pareado>=15/20: {'OK' if R1 else 'NO'} (pareado {par}/20) | R2 atajo>=.70 {'OK' if R2 else 'NO'}"
        f" | R3 INVERTIDO<=.35 {'OK' if R3 else 'NO'} | R4 llega limpio>=.60 {'OK' if R4 else 'NO'}")
    log(f"   validez: V0 v_B<{UMBRAL_V0}*v_A en {v0n}/20 {'OK' if V0 else 'NO'} | V1 M_llenas {'OK' if V1 else 'NO'}"
        f" | V2 ciego 40/40 {'OK' if V2 else 'NO'} | V3 SINMAPA==CONGELADA {'OK' if V3 else 'NO'}")
    log(f"VEREDICTO rodeo: {'ELIGE entre dos metas recordadas y se desvia por el lado largo' if V['RODEA'] else 'NO (refutado o control caido)'}"
        f"{'' if (V0 and V1 and V2 and V3) else '  *** OJO: validez caida, no se interpreta'}")
    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), semillas=SEEDS, mundo=MUNDO, prueba=PRUEBA, brazos=BRAZOS,
                veredictos=V, identidades=rc, procesos_python=ps, sha_preregistro=h16(pre),
                sha_script=h16(os.path.abspath(__file__)), sha_mundo=h16(os.path.join(AQUI, 'mundo_mapa_rodeo.py')),
                sha_origen=h16(os.path.join(MAPA_DIR, 'mundo_mapa.py')), python=platform.python_version(), numpy=np.__version__)
    dj = os.path.join(RAIZ, 'datos', f'rodeo_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.json')
    json.dump(dict(meta=meta, corridas=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
