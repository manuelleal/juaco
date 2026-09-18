"""Bloque 2 ter: ESCALA DEL RECUERDO (valor recordado saturado) contra el canje exploracion/explotacion del mapa, mundo largo.
Ejecuta PREREGISTRO_escala_mapa.md. REGLA 10: log desde el arranque. REGLA 11: lista los python vivos.
Identidad: mundo_largo_e con sat_M=None, kappa_M=1.0, sat_barajada=False == mundo_largo (todas las claves del original,
mundo completo con mapa); la unica clave nueva permitida en el gemelo es 'esc_diag' (diagnostico, no criterio).
Uso:  python experimentos/nivel8_escala_mapa/corre_escala.py [--desde N]      (por defecto semillas 81-100, Pool(14))
      python experimentos/nivel8_escala_mapa/corre_escala.py --humo [--seed N]  (UN proceso, 3 corridas: identidad + MAPA_SAT)
"""
import sys, os, json, time, hashlib, platform, subprocess, math
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'experimentos', 'nivel8_mundo_largo'), os.path.join(RAIZ, 'experimentos', 'nivel6_mapa'), os.path.join(RAIZ, 'organismo')]
from corre_mundo_largo import pool_de, sitios_de, recuperacion, T, T_NUEVO, T_INV
_desde = int(sys.argv[sys.argv.index('--desde') + 1]) if '--desde' in sys.argv else 81
SEEDS = list(range(_desde, _desde + 20))
CLAVE_NUEVA = 'esc_diag'   # unica clave que mundo_largo_e anade al dict de mundo_largo
# Preregistro §2: los cuatro primeros son los brazos de CRITERIO; el ultimo es de LECTURA (no decide veredicto).
BRAZOS = {
    'V13':          dict(usa_M=False),
    'MAPA':         dict(usa_M=True),
    'MAPA_SAT':     dict(usa_M=True, sat_M=1.0),
    'MAPA_SAT_BAR': dict(usa_M=True, sat_M=1.0, sat_barajada=True),
    'MAPA_ATEN':    dict(usa_M=True, kappa_M=0.5),
}
CRITERIO = ('V13', 'MAPA', 'MAPA_SAT', 'MAPA_SAT_BAR')
# K0 (preregistro §2): con las perillas apagadas el instrumento es mundo_largo bit a bit, y estas semillas ya estan
# medidas en novedad_alta_s81-100_20260917_221523 -> los brazos de referencia deben REPRODUCIRSE EXACTAMENTE.
K0 = {'V13_adq': 0.887, 'MAPA_adq': 0.700, 'MAPA_comida_q4': 971.0}
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
    """Lectura del mecanismo: como de repartidas quedan las pisadas entre los 8 sitios (no es criterio)."""
    v = [int(x) for x in r.get('esc_diag', {}).get('visitas', {}).values()]
    if not v or sum(v) == 0:
        return dict(vis_total=0, vis_min=0, vis_max=0, eq_visitas=None, H_visitas=None, sitios_pisados=0)
    s = float(sum(v)); ps = [x / s for x in v if x > 0]
    H = -sum(x * math.log(x) for x in ps) / math.log(len(v)) if len(v) > 1 else 0.0
    return dict(vis_total=int(s), vis_min=min(v), vis_max=max(v), eq_visitas=round(min(v) / max(v), 3),
                H_visitas=round(H, 3), sitios_pisados=int(sum(1 for x in v if x > 0)))


def medidas(r, brazo, seed):
    """Las medidas del mundo largo + las dos lecturas del mecanismo. Tambien la usa el humo de un proceso."""
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
        import mundo_largo as a_, mundo_largo_e as b_
        kw = mundo_kw(seed); kw.update(usa_M=True)   # mundo COMPLETO, con mapa: perillas de escala apagadas por defecto
        a, b = a_.run(seed, **kw), b_.run(seed, **kw)
        dif = [kk for kk in a if N(a[kk]) != N(b[kk])]
        extra = sorted(set(b) - set(a))
        return dict(tipo=tipo, esc='ident', seed=seed, identico=(not dif) and extra == [CLAVE_NUEVA], difieren=dif, claves_extra=extra)
    _, brazo, seed = args
    import mundo_largo_e as m
    kw = mundo_kw(seed); kw.update(BRAZOS[brazo])
    return medidas(m.run(seed, **kw), brazo, seed)


def med(xs):
    """Guardia: None fuera y lista vacia -> nan (auditoria bloques 2/3, punto 5)."""
    xs = [x for x in xs if x is not None]
    if not xs:
        return (float('nan'),) * 3
    return float(np.median(xs)), float(min(xs)), float(max(xs))


def humo(seed):
    """Humo de UN proceso (regla 3 de EQUIPO.md): 3 corridas de 200000. La corrida de identidad ES el brazo MAPA."""
    import mundo_largo as a_, mundo_largo_e as b_
    kw = mundo_kw(seed); kw.update(usa_M=True)
    log(f"HUMO (un proceso, 3 corridas de T={T}), semilla {seed}, mundo completo con mapa. NADA se ajusta con esto.")
    log(f"sha mundo_largo_e {h16(os.path.join(AQUI, 'mundo_largo_e.py'))}  mundo_largo {h16(os.path.join(RAIZ, 'experimentos', 'nivel8_mundo_largo', 'mundo_largo.py'))}")
    t0 = time.time(); a = a_.run(seed, **kw); ta = time.time() - t0
    log(f"  1/3 mundo_largo (referencia MAPA)            {ta:6.1f}s")
    t0 = time.time(); b = b_.run(seed, **kw); tb = time.time() - t0
    log(f"  2/3 mundo_largo_e perillas apagadas          {tb:6.1f}s")
    dif = [kk for kk in a if N(a[kk]) != N(b[kk])]; extra = sorted(set(b) - set(a))
    ident = (not dif) and extra == [CLAVE_NUEVA]
    log(f"      IDENTIDAD {'OK' if ident else 'FALLA'}  claves que difieren {dif}  claves extra {extra}")
    t0 = time.time(); c = b_.run(seed, **dict(kw, sat_M=1.0)); tc = time.time() - t0
    log(f"  3/3 mundo_largo_e sat_M=1.0 (MAPA_SAT)       {tc:6.1f}s   (+{100*(tc-tb)/tb:.0f}% sobre apagado)")
    for nom, r in (('MAPA', b), ('MAPA_SAT', c)):
        m = medidas(r, nom, seed)
        log(f"   {nom:9s} adq(<=30) {m['adq_hasta30']}  adq(final) {m['adq_final']}  comida_q4 {m['comida_q4']}  muertes {m['deaths']}"
            f"  celdas {m['celdas']}  M_llenas {m['M_llenas']}  sesgo_signo {m['sesgo_signo']}"
            f"  | visitas {m['vis_total']} min/max {m['vis_min']}/{m['vis_max']} eq {m['eq_visitas']} H {m['H_visitas']} pisados {m['sitios_pisados']}")
    log("Una semilla NO es evidencia: el criterio es la mediana de 20 y los dos controles, que aqui no se han corrido.")
    return ident


if __name__ == '__main__':
    stamp = time.strftime('%Y%m%d_%H%M%S')
    if '--humo' in sys.argv:
        s0 = int(sys.argv[sys.argv.index('--seed') + 1]) if '--seed' in sys.argv else 1
        _log['f'] = open(os.path.join(RAIZ, 'datos', f'escala_humo_s{s0}_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
        ok = humo(s0); _log['f'].close(); sys.exit(0 if ok else 1)
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'escala_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    pre = os.path.join(AQUI, 'PREREGISTRO_escala_mapa.md')
    log(f"ARRANQUE bloque 2 ter (ESCALA DEL RECUERDO: valor recordado saturado) contra el canje del mapa, mundo largo. brazos {list(BRAZOS)}, semillas {SEEDS[0]}-{SEEDS[-1]}, T={T}. Pool({N_PARALELO}).")
    log(f"   criterio: {list(CRITERIO)}; lectura (no decide): {[b for b in BRAZOS if b not in CRITERIO]}")
    log(f"sha preregistro {h16(pre)}  script {h16(os.path.abspath(__file__))}  constructor {h16(os.path.join(AQUI, 'construye_escala.py'))}  mundo_largo_e {h16(os.path.join(AQUI, 'mundo_largo_e.py'))}  mundo_largo {h16(os.path.join(RAIZ, 'experimentos', 'nivel8_mundo_largo', 'mundo_largo.py'))}  v13 {h16(os.path.join(RAIZ, 'organismo', 'organismo_v13.py'))}")
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
        log(f"ETAPA 1/3 - identidad perillas apagadas == mundo_largo, mundo completo con mapa ({len(ctrl)})...")
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
        log(f"   {b:13s} adq(<=30) {med([r['adq_hasta30'] for r in g])[0]:.3f} [{med([r['adq_hasta30'] for r in g])[1]:.2f},{med([r['adq_hasta30'] for r in g])[2]:.2f}]  adq(final) {med([r['adq_final'] for r in g])[0]:.3f}"
            f"  ret_no_inv {med([r['ret_no_inv'] for r in g])[0]:.2f}  comida_q4 {med([r['comida_q4'] for r in g])[0]:.0f}  muertes {med([r['deaths'] for r in g])[0]:.0f}"
            f"  recup {med([r['rec'] for r in g])[0]:.0f}  celdas {med([r['celdas'] for r in g])[0]:.0f}  M_llenas {med([r['M_llenas'] for r in g])[0]:.0f}"
            f"  | visitas {med([r['vis_total'] for r in g])[0]:.0f} eq {med([r['eq_visitas'] for r in g])[0]:.3f} H {med([r['H_visitas'] for r in g])[0]:.3f} pisados {med([r['sitios_pisados'] for r in g])[0]:.0f}"
            f"  | sesgo_signo {med([r['sesgo_signo'] for r in g])[0]:.2f}")
    for b in ('V13', 'MAPA', 'MAPA_SAT'):
        pts = {}
        for r in GG[b].values():
            for t_, nv, a_, p_ in r['curva']: pts.setdefault(nv, []).append(a_)
        log(f"   curva {b}: " + " ".join(f"{nv}:{np.median(v):.2f}" for nv, v in sorted(pts.items()) if nv % 5 == 0 or nv == 50))
    # K0: puerta de validez del instrumento (preregistro §2). No es criterio y no se puede recalibrar.
    k0 = dict(V13_adq=med([A('V13', s) for s in SEEDS])[0], MAPA_adq=med([A('MAPA', s) for s in SEEDS])[0],
              MAPA_comida_q4=med([CQ('MAPA', s) for s in SEEDS])[0])
    k0ok = all(abs(k0[k] - K0[k]) < 1e-9 for k in K0)
    V['K0_reproduce'] = bool(k0ok); V['K0_medido'] = k0; V['K0_esperado'] = K0
    log(f"   K0 reproduccion de novedad_alta_s81-100 (V13 {K0['V13_adq']}, MAPA {K0['MAPA_adq']}, comida {K0['MAPA_comida_q4']:.0f}): medido "
        f"V13 {k0['V13_adq']:.3f}, MAPA {k0['MAPA_adq']:.3f}, comida {k0['MAPA_comida_q4']:.0f} -> {'OK' if k0ok else '*** NO: instrumento sospechoso (regla 5)'}")

    def pareado(b1, b2):
        """> estricto; los empates se reportan SIEMPRE (ERR-17). Desempate preregistrado (preregistro §3), solo si hay empates."""
        gana = sum(A(b1, s) > A(b2, s) for s in SEEDS); emp = sum(A(b1, s) == A(b2, s) for s in SEEDS)
        pier = len(SEEDS) - gana - emp
        directo = gana >= 15
        desemp = (not directo) and emp > 0 and (gana + pier) >= 8 and gana >= 0.75 * (gana + pier)
        return dict(par=f"{b1}>{b2}", gana=gana, empata=emp, pierde=pier, ok=bool(directo or desemp), por_desempate=bool(desemp))

    m_sat = med([A('MAPA_SAT', s) for s in SEEDS])[0]
    sm, sb, bm, sa = pareado('MAPA_SAT', 'MAPA'), pareado('MAPA_SAT', 'MAPA_SAT_BAR'), pareado('MAPA_SAT_BAR', 'MAPA'), pareado('MAPA_SAT', 'MAPA_ATEN')
    P1 = bool(m_sat >= 0.85 and sm['ok'])
    p2n = sum(CQ('MAPA_SAT', s) >= 0.9 * CQ('MAPA', s) for s in SEEDS)
    P2 = bool(p2n >= 15)
    P3 = bool(sb['ok'] and not bm['ok'] and med([A('MAPA_SAT_BAR', s) for s in SEEDS])[0] < 0.85)
    P4 = bool(sa['ok'] and med([A('MAPA_ATEN', s) for s in SEEDS])[0] < 0.85)
    V.update(P1=P1, P2=P2, P3=P3, P4_lectura=P4, P2_n=int(p2n), adq_sat=m_sat, pareados=[sm, sb, bm, sa],
             DEVUELVE_EXPLORACION=bool(P1 and P2 and P3), LIMPIO=bool(P1 and P2 and P3 and P4))
    log(f"   P1 SAT adq {m_sat:.3f} (>=0.85) y >MAPA {sm['gana']}g/{sm['empata']}e/{sm['pierde']}p{' [desempate]' if sm['por_desempate'] else ''} -> {'OK' if P1 else 'NO'}")
    log(f"   P2 comida_q4 >=0.9xMAPA en {p2n}/20 -> {'OK' if P2 else 'NO'}   (MAPA {med([CQ('MAPA', s) for s in SEEDS])[0]:.0f}, SAT {med([CQ('MAPA_SAT', s) for s in SEEDS])[0]:.0f}, V13 {med([CQ('V13', s) for s in SEEDS])[0]:.0f})")
    log(f"   P3 SAT>BARAJADA {sb['gana']}g/{sb['empata']}e/{sb['pierde']}p{' [desempate]' if sb['por_desempate'] else ''} y BARAJADA>MAPA {bm['gana']}g/{bm['empata']}e/{bm['pierde']}p (no debe pasar) -> {'OK' if P3 else 'NO'}")
    log(f"   P4 (lectura) SAT>ATENUADO {sa['gana']}g/{sa['empata']}e/{sa['pierde']}p{' [desempate]' if sa['por_desempate'] else ''}, ATENUADO adq {med([A('MAPA_ATEN', s) for s in SEEDS])[0]:.3f} -> {'OK' if P4 else 'NO'}")
    log(f"VEREDICTO escala del recuerdo: {'DEVUELVE la exploracion sin cobrar la comida' if V['DEVUELVE_EXPLORACION'] else 'NO -> por el preregistro §3(a), el canje se registra como ESTRUCTURAL: el mapa cobra exploracion por construccion y v14 no lo lleva'}"
        f"{'' if V['LIMPIO'] or not V['DEVUELVE_EXPLORACION'] else ' -- OJO: P4 (atenuacion uniforme) NO pasa: el efecto puede ser solo menos mapa'}")
    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), semillas=SEEDS, T=T, T_nuevo=T_NUEVO, T_inv=T_INV, brazos=BRAZOS, brazos_criterio=list(CRITERIO),
                veredictos=V, identidades=rc, procesos_python=ps, sha_preregistro=h16(pre), sha_script=h16(os.path.abspath(__file__)),
                sha_constructor=h16(os.path.join(AQUI, 'construye_escala.py')), sha_mundo=h16(os.path.join(AQUI, 'mundo_largo_e.py')),
                sha_mundo_largo=h16(os.path.join(RAIZ, 'experimentos', 'nivel8_mundo_largo', 'mundo_largo.py')),
                python=platform.python_version(), numpy=np.__version__)
    dj = os.path.join(RAIZ, 'datos', f'escala_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.json')
    json.dump(dict(meta=meta, corridas=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
