"""Nivel 7 — HIJA DISPERSA: la hija de v11 nace ciega a parte del patron, no solo fuera de el.
Ejecuta PREREGISTRO_hija_dispersa.md (propuesta B-1 del creador B). El MUNDO no cambia: cambia UNA linea del
nacimiento de la hija. REGLA 10: log desde el arranque con fsync. REGLA 11: procesos vivos al log.

Etapa 1 IDENTIDAD (aborta si no es 3/3): mundo_hija_dispersa con las perillas apagadas == mundo_temporal_k, todas
las claves, en 3 casos. Etapa 2: la serie. Etapa 3: criterios P1-P4 y clausulas R1-R4 tal cual el preregistro.

Uso:  python experimentos/nivel7_hija_dispersa/corre_hija_dispersa.py [--desde 61] [--ks 4,5] [--humo]
      --humo  = un solo proceso, 1 semilla, T=20000, sin Pool (comprobacion de que el montaje corre).
"""
import sys, os, json, time, hashlib, platform, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'experimentos', 'nivel7_3T_k'), os.path.join(RAIZ, 'organismo')]

HUMO = '--humo' in sys.argv
_desde = int(sys.argv[sys.argv.index('--desde') + 1]) if '--desde' in sys.argv else 61
SEEDS = list(range(_desde, _desde + (1 if HUMO else 20)))
KS = [int(v) for v in sys.argv[sys.argv.index('--ks') + 1].split(',')] if '--ks' in sys.argv else [4, 5]
T_SERIE = 20000 if HUMO else 100000
T_IDENT = 20000 if HUMO else 100000
N_PARALELO = 14

V13 = dict(mu_norm=True, div_signo=True, eta_s=0.015, puerta=3)
APAGADO = dict(recic=0, tau_r=0, mask_rel=0, n_cf=1)
# Brazos del preregistro (seccion 2). del_s = del_c = 0.25, fijados ANTES de correr.
BRAZOS = {
    'V13':  dict(mask_rel=0, n_cf=1),                              # control de inercia = el tronco
    'REL':  dict(mask_rel=2, n_cf=1, del_s=0.25, del_c=0.25),      # (a) hija dispersa por relevancia
    'RELD': dict(mask_rel=2, n_cf=4, del_s=0.25, del_c=0.25),      # (a) + division diferida
    'AZAR': dict(mask_rel=4, n_cf=1, del_s=0.25, del_c=0.25),      # (b) control: misma cardinalidad, al azar
    'SLOT': dict(mask_rel=3, n_cf=1, del_s=0.25, del_c=0.25),      # (c) control: slot profundo intercambiado
}
ESC = ['C3', 'C3C']
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


NUEVAS = {'div_bloq', 'n_recic', 'diag', 'recic', 'tau_r', 'mask_rel', 'div_diag', 'n_cf'}


def tarea(args):
    tipo = args[0]
    if tipo == 'I':   # identidad: perillas apagadas == mundo_temporal_k, todas las claves
        _, arm, k, seed = args
        import mundo_temporal_k as a_, mundo_hija_dispersa as b_
        a = a_.run(seed, arm=arm, kprof=k, T=T_IDENT, **V13)
        b = b_.run(seed, arm=arm, kprof=k, T=T_IDENT, **V13, **APAGADO)
        dif = [kk for kk in a if kk not in NUEVAS and N(a[kk]) != N(b[kk])]
        return dict(tipo=tipo, esc=f"{arm} k={k}", seed=seed, identico=not dif, difieren=dif)
    if tipo == 'P4':  # inercia: a k=1, REL == V13 semilla a semilla (todas las claves)
        _, seed = args
        import mundo_hija_dispersa as m
        a = m.run(seed, arm='C3', kprof=1, T=T_SERIE, **V13, **BRAZOS['V13'])
        b = m.run(seed, arm='C3', kprof=1, T=T_SERIE, **V13, **BRAZOS['REL'])
        dif = [kk for kk in a if kk not in NUEVAS and N(a[kk]) != N(b[kk])]
        return dict(tipo=tipo, seed=seed, identico=not dif, difieren=dif)
    _, k, brazo, esc, seed = args
    import mundo_hija_dispersa as m
    r = m.run(seed, arm=esc, kprof=k, T=T_SERIE, **V13, **BRAZOS[brazo])
    lf = r['lift'][3] if r['lift'][3] is not None else 0.0
    return dict(tipo='T', k=k, brazo=brazo, esc=esc, seed=seed, W=r['W'], sep=r['sep'], solap_A=r['solap_A'],
                lift=r['lift'], lift_q4=lf, deaths=r['deaths'], splits=r['splits'], celdas=r['celdas'],
                t_pool=r['t_pool'], div_bloq=r['div_bloq'], Rtot=r['Rtot'], diag=r['diag'])


def med(xs):
    xs = list(xs)
    return float(np.median(xs)), float(min(xs)), float(max(xs))


if __name__ == '__main__':
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    stamp = time.strftime('%Y%m%d_%H%M%S')
    nom = f'hija_dispersa{"_humo" if HUMO else ""}_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}'
    _log['f'] = open(os.path.join(RAIZ, 'datos', nom + '.log'), 'w', encoding='utf-8', newline='\n')
    pre = os.path.join(AQUI, 'PREREGISTRO_hija_dispersa.md')
    inst = os.path.join(AQUI, 'mundo_hija_dispersa.py')
    ctor = os.path.join(AQUI, 'construye_hija_dispersa.py')
    orig = os.path.join(RAIZ, 'experimentos', 'nivel7_3T_k', 'mundo_temporal_k.py')
    log(f"ARRANQUE HIJA DISPERSA (propuesta B-1). k en {KS}, brazos {list(BRAZOS)}, escenarios {ESC}, "
        f"semillas {SEEDS[0]}-{SEEDS[-1]}, T={T_SERIE}. {'HUMO (un proceso, sin Pool)' if HUMO else f'Pool({N_PARALELO})'}")
    log(f"sha preregistro {h16(pre)}  script {h16(os.path.abspath(__file__))}  constructor {h16(ctor)}  "
        f"instrumento {h16(inst)}  origen mundo_temporal_k {h16(orig)}  v13 {h16(os.path.join(RAIZ, 'organismo', 'organismo_v13.py'))}")
    try:
        ps = subprocess.run(['powershell', '-NoProfile', '-Command',
                             "Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*' } | ForEach-Object { \"$($_.ProcessId) $($_.CommandLine)\" }"],
                            capture_output=True, text=True, timeout=60).stdout.strip().splitlines()
    except Exception as e:
        ps = [f"(no se pudo listar: {e})"]
    log(f"REGLA 11 — procesos python vivos ({len(ps)}), este es pid {os.getpid()}")

    ctrl = [('I', 'C3', 1, SEEDS[0]), ('I', 'C3', max(KS), SEEDS[0]), ('I', 'C3C', min(KS), SEEDS[0])]
    tr = [('T', k, b, e, s) for k in KS for b in BRAZOS for e in ESC for s in SEEDS]
    p4 = [('P4', s) for s in SEEDS]
    V = {}

    def corre(lote, etiqueta, pool=None):
        log(f"{etiqueta} ({len(lote)})...")
        if pool is None:
            out = []
            for i, x in enumerate(lote, 1):
                out.append(tarea(x))
                if i % 10 == 0 or i == len(lote): log(f"          {i}/{len(lote)}")
            return out
        out = []
        for i, r in enumerate(pool.imap_unordered(tarea, lote, chunksize=1), 1):
            out.append(r)
            if i % 30 == 0 or i == len(lote): log(f"          {i}/{len(lote)}")
        return out

    pool = None if HUMO else mp.Pool(N_PARALELO)
    try:
        rc = corre(ctrl, "ETAPA 1/3 — IDENTIDAD (perillas apagadas == mundo_temporal_k)", pool)
        log(f"  identicos: {sum(x['identico'] for x in rc)}/{len(rc)}")
        for x in rc:
            if not x['identico']: log(f"      DIFIERE {x['esc']} s{x['seed']}: {x['difieren']}")
        V['IDENTIDAD'] = all(x['identico'] for x in rc)
        if not V['IDENTIDAD']:
            log("*** IDENTIDAD FALLIDA: se para (regla: un instrumento que no es bit a bit no confirma nada).")
            _log['f'].close(); sys.exit(1)
        res = corre(tr, "ETAPA 2/3 — serie", pool)
        rp4 = corre(p4, "ETAPA 2b/3 — P4 (inercia a k=1: REL == V13)", pool)
    finally:
        if pool is not None:
            pool.close(); pool.join()

    log("ETAPA 3/3 — analisis (criterios y clausulas del preregistro, sin recalibrar).")
    G = lambda k, b, e: {r['seed']: r for r in res if r['k'] == k and r['brazo'] == b and r['esc'] == e}
    for k in KS:
        log(); log(f"  k = {k}")
        for b in BRAZOS:
            g = [G(k, b, 'C3')[s] for s in SEEDS]
            log(f"   {b:5s} C3  sep {med(r['sep'] for r in g)[0]:+.2f} [{med(r['sep'] for r in g)[1]:+.2f},{med(r['sep'] for r in g)[2]:+.2f}]"
                f"  lift_q4 {med(r['lift_q4'] for r in g)[0]:+.3f}  solap_A {med(r['solap_A'] for r in g)[0]:.2f}"
                f"  divisiones {med(r['splits'] for r in g)[0]:.0f}  celdas {med(r['celdas'] for r in g)[0]:.0f}"
                f"  muertes {med(r['deaths'] for r in g)[0]:.0f}  Rtot {med(r['Rtot'] for r in g)[0]:+.0f}")
            gc = [G(k, b, 'C3C')[s] for s in SEEDS]
            log(f"   {b:5s} C3C sep {med(r['sep'] for r in gc)[0]:+.2f}  lift_q4 {med(r['lift_q4'] for r in gc)[0]:+.3f}"
                f"  celdas {med(r['celdas'] for r in gc)[0]:.0f}   (control de canal falso)")
        v13 = G(k, 'V13', 'C3'); rel = G(k, 'REL', 'C3'); azar = G(k, 'AZAR', 'C3'); slot = G(k, 'SLOT', 'C3')
        relc = G(k, 'REL', 'C3C')
        f_cel = 0.75 if k == 5 else 0.85
        n_p1 = sum(rel[s]['celdas'] <= f_cel * v13[s]['celdas'] for s in SEEDS)
        p1 = n_p1 >= (1 if HUMO else 18)
        m_lift = med(rel[s]['lift_q4'] for s in SEEDS)[0]
        n_p2 = sum(rel[s]['lift_q4'] > v13[s]['lift_q4'] for s in SEEDS)
        p2 = (m_lift >= 0.18 and n_p2 >= (1 if HUMO else 15)) if k == 5 else None
        m_sep = med(rel[s]['sep'] for s in SEEDS)[0]
        n_p3 = sum(rel[s]['sep'] - relc[s]['sep'] >= 1.0 for s in SEEDS)
        p3 = m_sep >= 2.2 and n_p3 >= (1 if HUMO else 18)
        cfalso = all(med(G(k, b, 'C3C')[s]['sep'] for s in SEEDS)[0] < 1.0 and
                     med(G(k, b, 'C3C')[s]['lift_q4'] for s in SEEDS)[0] < 0.15 for b in BRAZOS)
        n_r3 = sum(rel[s]['lift_q4'] > azar[s]['lift_q4'] for s in SEEDS)
        n_r4 = sum(slot[s]['lift_q4'] > rel[s]['lift_q4'] for s in SEEDS)
        n_azar_p2 = sum(azar[s]['lift_q4'] > v13[s]['lift_q4'] for s in SEEDS)
        azar_p2 = med(azar[s]['lift_q4'] for s in SEEDS)[0] >= 0.18 and n_azar_p2 >= (1 if HUMO else 15)
        umbral = 1 if HUMO else 14
        V[f'k{k}'] = dict(P1=bool(p1), P1_n=n_p1, P2=(None if p2 is None else bool(p2)), P2_n=n_p2, P2_med=m_lift,
                          P3=bool(p3), P3_n=n_p3, P3_sep=m_sep, C3C_ok=bool(cfalso),
                          R3_rel_gt_azar=n_r3, R4_slot_gt_rel=n_r4, AZAR_P2=bool(azar_p2), AZAR_P2_n=n_azar_p2,
                          celdas_v13=med(v13[s]['celdas'] for s in SEEDS)[0],
                          celdas_rel=med(rel[s]['celdas'] for s in SEEDS)[0])
        log(f"   P1 celdas<= {f_cel}xV13 en {n_p1}/{len(SEEDS)} {'OK' if p1 else 'NO'}"
            f" | P2 lift med {m_lift:.3f} (>=0.18) y >V13 en {n_p2}/{len(SEEDS)} {('-' if p2 is None else ('OK' if p2 else 'NO'))}"
            f" | P3 sep med {m_sep:.2f} (>=2.2) y C3-C3C>=1 en {n_p3}/{len(SEEDS)} {'OK' if p3 else 'NO'}"
            f" | canal falso {'OK' if cfalso else 'ARTEFACTO'}")
        log(f"   R3 REL>AZAR en {n_r3}/{len(SEEDS)} (umbral {umbral}) | R4 SLOT>REL en {n_r4}/{len(SEEDS)} (umbral {umbral})"
            f" | AZAR cumple P2: {'si' if azar_p2 else 'no'}")

    k5 = V.get('k5')
    if k5 is not None:
        R1 = not k5['P1']
        R2 = (not k5['P2']) and (not k5['AZAR_P2'])
        R3 = k5['R3_rel_gt_azar'] < (1 if HUMO else 14)
        R4 = k5['R4_slot_gt_rel'] >= (1 if HUMO else 14)
        V['CLAUSULAS'] = dict(R1=bool(R1), R2=bool(R2), R3=bool(R3), R4=bool(R4))
        if R4:      ver = "ERR — ARTEFACTO (SLOT supera a REL): se para y se audita el instrumento"
        elif R1:    ver = "REFUTADA (R1): el ahorro de celdas no replica"
        elif R2:    ver = "SOLO ECONOMIA DE CELDAS (R2): no compone mejor; no toca el tronco"
        elif R3:    ver = "HIJA DISPERSA (R3): lo que actua es la DISPERSION, no la relevancia -> al tronco iria AZAR (memoria cero)"
        else:       ver = "HIJA DISPERSA POR RELEVANCIA: P1-P3 y REL>AZAR"
    else:
        ver = "sin k=5 en esta corrida"
    n_ok4 = sum(x['identico'] for x in rp4)
    V['P4'] = dict(identicos=n_ok4, total=len(rp4), ok=bool(n_ok4 == len(rp4)))
    log(); log(f"P4 (inercia a k=1, REL == V13 semilla a semilla): {n_ok4}/{len(rp4)} {'OK' if n_ok4 == len(rp4) else 'NO'}")
    for x in rp4:
        if not x['identico']: log(f"      DIFIERE s{x['seed']}: {x['difieren'][:8]}")
    log(); log(f"VEREDICTO HIJA_DISPERSA: {ver}")
    if HUMO:
        log("(HUMO: 1 semilla y T=20000 — los umbrales pareados NO valen; esto solo prueba que el montaje corre.)")

    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), humo=HUMO, semillas=SEEDS, ks=KS, T=T_SERIE,
                brazos=BRAZOS, escenarios=ESC, veredictos=V, veredicto=ver, identidades=rc, P4=rp4,
                procesos_python=ps, sha_preregistro=h16(pre), sha_script=h16(os.path.abspath(__file__)),
                sha_constructor=h16(ctor), sha_instrumento=h16(inst), sha_origen=h16(orig),
                python=platform.python_version(), numpy=np.__version__)
    dj = os.path.join(RAIZ, 'datos', nom + '.json')
    json.dump(dict(meta=meta, corridas=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
