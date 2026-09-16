"""Prueba de COSTE del arreglo de BUG-01 con el techo MORDIENDO contra el objetivo.

Ejecuta PREREGISTRO_coste_techo.md (sha e0e2709f71dff15f). No decide nada que no este escrito alli.
Organismos: organismo_v7h.py y organismo_caph.py, generados por construye_coste_techo.py.

REGLA 10: linea de progreso por etapa con marca de tiempo, log a archivo DESDE EL ARRANQUE
(datos/coste_techo_<fecha>.log, seguible con tail -f).

Precisiones de implementacion escritas ANTES de correr (el preregistro no las fijaba al detalle):
- M_max (C5) se calcula por semilla: maximo, sobre los checkpoints de la corrida, del numero de estimulos vivos
  con |W-R| <= 0.3. Es la version por semilla de parte2g_techo_estricto.py.
- "Fases cuyo ultimo paso es < t_techo" (S0): la fase p (0-indexada) ocupa [p*50000, (p+1)*50000); se compara si
  (p+1)*50000 - 1 < t_techo(control). Sin truncacion en el control se comparan ademas los totales.
- W de fase en S0 se compara redondeado a 2 decimales; en C0, W de checkpoint ya viene a 3 decimales de foto().
- C3 usa el checkpoint final (t=T) con |W| < 0.0005, es decir W == 0.000 a 3 decimales.

Uso:  python experimentos/bug01/corre_coste_techo.py [semillas]
"""
import sys, os, json, time, hashlib, platform, csv, subprocess, statistics as st
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
CAPDIR = os.path.join(RAIZ, 'experimentos', 'ramas', '2Kbis_capacidad')
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo'), CAPDIR]

LAM = 0.05
S_CADA, S_T = 50000, 350000                    # bloque S: 7 fases
NF = S_T // S_CADA
UMBRAL_SEM = 15                                # >=15/20, fijado en el preregistro
N_PARALELO = 14

ESC_V7 = {'BUG': dict(plast=False, solap_AB=3), 'E1': dict(), 'E2': dict(invertir_en=50000),
          'E2I': dict(nuevo='C'), 'E2J': dict(nuevo='D', nuevo_val='comida', solap_B=1),
          'E2K': dict(nuevo='D', nuevo_val='comida', solap_B=2), 'E2L': dict(solap_AB=3)}
PLAN0 = [(0, 'A', 'comida'), (0, 'B', 'veneno')]
ESC_CAP = {'E1': dict(plan=PLAN0), 'C_veneno_50k': dict(plan=PLAN0 + [(50000, 'C', 'veneno')]),
           'D_comida_50k': dict(plan=PLAN0 + [(50000, 'D', 'comida')])}
CONDS_C = [('C_T20', True, 20000), ('C_T60', True, 60000), ('C_F20', False, 20000)]
PRINCIPALES = ['S_F', 'S_T', 'C_T20']

_log = {'f': None, 't0': None}


def log(msg):
    """REGLA 10: marca de tiempo, a pantalla y a archivo, con flush + fsync."""
    dt = time.time() - _log['t0']
    linea = f"[{time.strftime('%H:%M:%S')} +{dt:7.1f}s] {msg}"
    print(linea, flush=True)
    if _log['f']:
        _log['f'].write(linea + "\n")
        _log['f'].flush()
        os.fsync(_log['f'].fileno())


def J(x):
    return json.dumps(x, sort_keys=True, default=str)


# ---------------------------------------------------------------------------------------------
# tareas
# ---------------------------------------------------------------------------------------------
def tarea_control(args):
    cual, esc, seed, plast = args
    if cual == 'a':                                   # v7h(lam=0) vs organismo_v7
        import organismo_v7 as base, organismo_v7h as var
        kw = ESC_V7[esc]; a, b = base.run(seed, **kw), var.run(seed, lam=0.0, **kw)
        dif = [k for k in a if a[k] != b[k]]
    elif cual == 'b':                                 # v7h(lam=0.05) vs v7e(lam=0.05)
        import organismo_v7e as base, organismo_v7h as var
        kw = ESC_V7[esc]; a, b = base.run(seed, lam=LAM, **kw), var.run(seed, lam=LAM, **kw)
        dif = [k for k in a if a[k] != b[k]]
    else:                                             # caph(lam=0) vs organismo_cap
        import organismo_cap as base, organismo_caph as var, parte2_capacidad as P
        if esc == 'corto6':
            kw = dict(T=P.T_de(20000, 6), plan=P.plan_de(20000, 6), pats=P.PATS, chk=P.chks(20000, 6))
        else:
            kw = ESC_CAP[esc]
        a, b = base.run(seed, plast=plast, **kw), var.run(seed, plast=plast, lam=0.0, **kw)
        dif = [k for k in a if J(a[k]) != J(b[k])]
    return dict(cual=cual, esc=esc, seed=seed, plast=plast, identico=not dif, difieren=dif)


def tarea_S(args):
    plast, lam, seed = args
    import organismo_v7h as o
    r = o.run(seed, T=S_T, invertir_cada=S_CADA, plast=plast, lam=lam)
    return dict(bloque='S', cond='S_T' if plast else 'S_F', plast=plast, lam=lam, seed=seed,
                fases=r['fases'], dfase=r['dfase'], t_techo=r['t_techo'], techo_primero=r['techo_primero'],
                n_techo=r['n_techo'], mv_tot=r['mv_tot'], mc_tot=r['mc_tot'], deaths=r['deaths'],
                splits=r['splits'], celdas=r['celdas'], err_max=round(r['err_max'], 4), W=r['W'], comp=r['comp'])


def tarea_C(args):
    cond, plast, pt, lam, seed = args
    import organismo_caph as o, parte2_capacidad as P
    r = o.run(seed, T=P.T_de(pt), plan=P.plan_de(pt), pats=P.PATS, chk=P.chks(pt), plast=plast, lam=lam)
    for h in r['hist']:
        h['dev'] = {k: round(abs(v - P.R[k]), 3) for k, v in h['W'].items()}
    return dict(bloque='C', cond=cond, plast=plast, paso_t=pt, lam=lam, seed=seed, hist=r['hist'],
                t_techo=r['t_techo'], techo_primero=r['techo_primero'], n_techo=r['n_techo'],
                mv_tot=r['mv_tot'], mc_tot=r['mc_tot'], deaths=r['deaths'], celdas=r['celdas'],
                splits=r['splits'], t_agot=r['t_agot'], err_max=round(r['err_max'], 4))


# ---------------------------------------------------------------------------------------------
# analisis
# ---------------------------------------------------------------------------------------------
def med(xs):
    xs = [x for x in xs if x is not None]
    return (float(np.median(xs)), float(np.min(xs)), float(np.max(xs))) if xs else (None, None, None)


def fmt(t, d=2):
    return "sin datos" if t[0] is None else f"{t[0]:+.{d}f} [{t[1]:+.{d}f}, {t[2]:+.{d}f}]"


def fase_igual(rc, rf, p):
    for k in ('A', 'B'):
        fc, ff = rc['fases'][k], rf['fases'][k]
        for campo in ('mord', 'vis', 'mv', 'mc', 'n'):
            if fc[campo][p] != ff[campo][p]:
                return False
        if round(fc['W'][p], 2) != round(ff['W'][p], 2):
            return False
    return rc['dfase'][p] == rf['dfase'][p]


def techo_n(hist):
    import parte2_capacidad as P
    return P.techo(hist)


def m_max(hist):
    return max(sum(1 for v in h['dev'].values() if v <= 0.3) for h in hist)


def hist_sorted(r):
    return sorted(r['hist'], key=lambda h: h['t'])


if __name__ == '__main__':
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    argv = sys.argv[1:]
    SALIDA = os.path.join(RAIZ, 'datos')
    if '--salida' in argv:                            # solo para ensayos: escribe fuera de datos/
        i = argv.index('--salida'); SALIDA = argv[i + 1]; del argv[i:i + 2]
    S = int(argv[0]) if argv else 20
    seeds = list(range(1, S + 1))
    stamp = time.strftime('%Y%m%d_%H%M%S')
    h16 = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]

    _log['t0'] = time.time()
    _log['f'] = open(os.path.join(SALIDA, f'coste_techo_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    log(f"ARRANQUE. prueba de coste con el techo mordiendo, {S} semillas, lam={LAM}, Pool({N_PARALELO}).")
    log(f"log -> datos/coste_techo_{stamp}.log   (regla 10: se escribe desde ya)")
    log(f"sha preregistro {h16(os.path.join(AQUI, 'PREREGISTRO_coste_techo.md'))}  script {h16(os.path.abspath(__file__))}"
        f"  v7h {h16(os.path.join(AQUI, 'organismo_v7h.py'))}  caph {h16(os.path.join(AQUI, 'organismo_caph.py'))}")

    # REGLA 11: procesos Python vivos antes de lanzar
    try:
        ps = subprocess.run(['powershell', '-NoProfile', '-Command',
                             "Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*' } | "
                             "ForEach-Object { \"$($_.ProcessId) $($_.CommandLine)\" }"],
                            capture_output=True, text=True, timeout=60).stdout.strip().splitlines()
    except Exception as e:
        ps = [f"(no se pudo listar: {e})"]
    log(f"REGLA 11 — procesos python vivos al arrancar ({len(ps)}), este script es pid {os.getpid()}:")
    for linea in ps:
        log(f"    {linea[:160]}")

    res_ctrl, res_S, res_C = [], [], []
    with mp.Pool(N_PARALELO) as pool:
        # ---------- ETAPA 1: CONTROL 1 ----------
        trabajos = ([('a', e, s, None) for e in ESC_V7 for s in range(1, 7)]
                    + [('b', e, s, None) for e in ESC_V7 for s in range(1, 7)]
                    + [('c', e, s, p) for e in ESC_CAP for s in range(1, 7) for p in (False, True)]
                    + [('c', 'corto6', s, p) for s in range(1, 4) for p in (False, True)])
        log(f"ETAPA 1/5 — control de inercia de los instrumentos ({len(trabajos)} comparaciones)...")
        for i, r in enumerate(pool.imap_unordered(tarea_control, trabajos, chunksize=1), 1):
            res_ctrl.append(r)
            if i % 20 == 0 or i == len(trabajos):
                log(f"          control {i}/{len(trabajos)}  ({sum(c['identico'] for c in res_ctrl)} identicos)")
        ok_ctrl = {}
        for cual, nombre in (('a', 'v7h(lam=0) vs v7'), ('b', 'v7h(lam=0.05) vs v7e(lam=0.05)'),
                             ('c', 'caph(lam=0) vs cap')):
            g = [c for c in res_ctrl if c['cual'] == cual]
            ok_ctrl[cual] = all(c['identico'] for c in g)
            log(f"  {nombre:34s}: {sum(c['identico'] for c in g)}/{len(g)} -> {'OK' if ok_ctrl[cual] else 'FALLA'}")
            for c in g:
                if not c['identico']:
                    log(f"      DIFIERE {c['esc']} semilla {c['seed']} plast={c['plast']}: {c['difieren']}")
        if not all(ok_ctrl.values()):
            log("*** CONTROL 1 FALLIDO. Los instrumentos no son el mismo organismo. No se corre nada mas.")
            sys.exit(1)

        # ---------- ETAPAS 2 y 3: BLOQUES S y C (en un solo pool, largas primero) ----------
        tS = [(p, l, s) for p in (False, True) for l in (0.0, LAM) for s in seeds]
        tC = [(c, p, pt, l, s) for (c, p, pt) in CONDS_C for l in (0.0, LAM) for s in seeds]
        tC.sort(key=lambda a: -a[2])
        log(f"ETAPA 2/5 — bloque S: {len(tS)} corridas a T={S_T} (inversion cada {S_CADA}).")
        log(f"ETAPA 3/5 — bloque C: {len(tC)} corridas (2K-bis Parte 2; paso_t 60000 primero). Se lanzan juntas.")
        todo = [('C', a) for a in tC] + [('S', a) for a in tS]
        n_tot = len(todo)
        asyncs = [(b, pool.apply_async(tarea_C if b == 'C' else tarea_S, (a,))) for b, a in todo]
        hechos = 0; ultimo = 0
        while hechos < n_tot:
            hechos = sum(1 for _, ar in asyncs if ar.ready())
            if hechos - ultimo >= 20 or hechos == n_tot:
                nS = sum(1 for b, ar in asyncs if b == 'S' and ar.ready())
                log(f"          corridas {hechos}/{n_tot}  (S {nS}/{len(tS)}, C {hechos-nS}/{len(tC)})")
                ultimo = hechos
            if hechos < n_tot:
                time.sleep(2)
        for b, ar in asyncs:
            (res_S if b == 'S' else res_C).append(ar.get())

    # Volcado crudo ANTES del analisis: un fallo del codigo de analisis no se lleva las corridas.
    dcrudo = os.path.join(SALIDA, f'coste_techo_{stamp}_crudo.json')
    json.dump(dict(control_inercia=res_ctrl, bloque_S=res_S, bloque_C=res_C, procesos_python_al_arrancar=ps),
              open(dcrudo, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"crudo -> {os.path.basename(dcrudo)}  sha256_16 = {h16(dcrudo)}  (escrito antes del analisis)")

    # ---------- ETAPA 4: ANALISIS ----------
    log("ETAPA 4/5 — analisis.")
    V = {}

    def par(res, cond, seed):
        c = next(r for r in res if r['cond'] == cond and r['seed'] == seed and r['lam'] == 0.0)
        f = next(r for r in res if r['cond'] == cond and r['seed'] == seed and r['lam'] == LAM)
        return c, f

    # ===== BLOQUE S =====
    log(""); log("=" * 96); log("BLOQUE S — inversiones seriadas, 7 fases de 50k"); log("=" * 96)
    S0 = True
    for cond in ('S_F', 'S_T'):
        ok = 0; det = []
        for s in seeds:
            rc, rf = par(res_S, cond, s)
            tt = rc['t_techo']
            fases_cmp = [p for p in range(NF) if tt is None or (p + 1) * S_CADA - 1 < tt]
            iguales = all(fase_igual(rc, rf, p) for p in fases_cmp)
            if tt is None:
                iguales &= (rc['deaths'] == rf['deaths'] and rc['splits'] == rf['splits'] and rc['W'] == rf['W'])
            ok += iguales
            if not iguales:
                det.append((s, tt, [p + 1 for p in fases_cmp if not fase_igual(rc, rf, p)]))
        S0 &= ok == S
        log(f"  S0 {cond}: identico antes de la primera truncacion del control en {ok}/{S}")
        for d in det:
            log(f"      DIFIERE semilla {d[0]}: t_techo(control)={d[1]}, fases distintas {d[2]}")
    log(f"  S0 [exacta, decide la lectura]: {'SOSTENIDA' if S0 else 'REFUTADA'}")
    V['S0'] = S0

    for cond in ('S_F', 'S_T'):
        for lam in (0.0, LAM):
            g = [r for r in res_S if r['cond'] == cond and r['lam'] == lam]
            tts = [r['t_techo'] for r in g]
            prim = {}
            for r in g:
                key = 'ninguna' if r['techo_primero'] is None else f"{r['techo_primero'][0]}-{r['techo_primero'][1]}-fase{r['techo_primero'][2]+1}"
                prim[key] = prim.get(key, 0) + 1
            log(f"  {cond} lam={lam}: truncan {sum(t is not None for t in tts)}/{S}; primera: {prim}; "
                f"muertes {fmt(med([r['deaths'] for r in g]),0)}; veneno {fmt(med([r['mv_tot'] for r in g]),0)}; "
                f"splits {fmt(med([r['splits'] for r in g]),0)}")
            for k in ('A', 'B'):
                ws = [fmt(med([r['fases'][k]['W'][p] for r in g])) for p in range(NF)]
                ns = [med([r['fases'][k]['n'][p] for r in g])[0] for p in range(NF)]
                cens = [sum(r['fases'][k]['n'][p] is None for r in g) for p in range(NF)]
                log(f"      W_{k} por fase: " + " | ".join(ws))
                log(f"      n_{k} mediana por fase: {ns}   censuradas: {cens}")

    gFc = sorted([r for r in res_S if r['cond'] == 'S_F' and r['lam'] == 0.0], key=lambda r: r['seed'])
    gFf = sorted([r for r in res_S if r['cond'] == 'S_F' and r['lam'] == LAM], key=lambda r: r['seed'])
    S1a = sum(r['t_techo'] is None or r['t_techo'] >= 4 * S_CADA for r in gFc) == S
    S1b = sum(r['techo_primero'] is not None and r['techo_primero'][0] == 'B' and r['techo_primero'][2] == 4
              for r in gFc) >= UMBRAL_SEM
    wb5 = med([r['fases']['B']['W'][4] for r in gFc])[0]
    S1c = wb5 is not None and -1.5 <= wb5 <= -0.7
    S1d = sum(abs(r['fases']['A']['W'][NF-1]) <= 0.3 and abs(r['fases']['B']['W'][NF-1]) <= 0.3 for r in gFc) >= UMBRAL_SEM
    S2 = (sum(r['t_techo'] is None for r in gFf) == S and
          sum(abs(r['fases']['A']['W'][NF-1] - 1) < 0.15 and abs(r['fases']['B']['W'][NF-1] + 3) < 0.3 for r in gFf) >= UMBRAL_SEM)
    S3f = (sum(r['fases']['B']['n'][0] == 19 for r in gFf) == S and
           all(sum(r['fases']['B']['n'][p] is not None and 21 <= r['fases']['B']['n'][p] <= 23 for r in gFf) >= UMBRAL_SEM
               for p in (2, 4, 6)))
    S3c = (sum(c['fases']['B']['n'][2] == f['fases']['B']['n'][2] for c, f in zip(gFc, gFf)) == S and
           sum(r['fases']['B']['n'][4] is None for r in gFc) >= UMBRAL_SEM)
    log("")
    log(f"  S1a cero truncaciones en fases 1-4 (control, plast=F), 20/20 : {'SOSTENIDA' if S1a else 'REFUTADA'}")
    log(f"  S1b primera truncacion = B en fase 5, >=15/20                 : {'SOSTENIDA' if S1b else 'REFUTADA'}")
    log(f"  S1c mediana W_B fin fase 5 en [-1.5,-0.7]  ({wb5})            : {'SOSTENIDA' if S1c else 'REFUTADA'}")
    log(f"  S1d |W_A|,|W_B|<=0.3 al final (BUG-01 temporal), >=15/20      : {'SOSTENIDA' if S1d else 'REFUTADA'}")
    log(f"  S2  arreglo plast=F: 0 truncaciones y valores E1 al final     : {'SOSTENIDA' if S2 else 'REFUTADA'}")
    log(f"  S3  arreglo: n1=19 y n3,n5,n7 en [21,23]                      : {'SOSTENIDA' if S3f else 'REFUTADA'}")
    log(f"  S3  control: n3 = arreglo 20/20 y n5 censurada >=15/20        : {'SOSTENIDA' if S3c else 'REFUTADA'}")
    V.update(S1a=S1a, S1b=S1b, S1c=S1c, S1d=S1d, S2=S2, S3_arreglo=S3f, S3_control=S3c)

    # ===== BLOQUE C =====
    log(""); log("=" * 96); log("BLOQUE C — capacidad 2K-bis Parte 2"); log("=" * 96)
    C0 = True; C1 = True; resumen_C = {}
    for cond, plast, pt in CONDS_C:
        ok0 = 0; difN = []; viol1 = []; Nc = []; Nf = []; Mc = []; Mf = []
        for s in seeds:
            rc, rf = par(res_C, cond, s)
            tt = rc['t_techo']
            hc, hf = hist_sorted(rc), hist_sorted(rf)
            iguales = True
            for a, b in zip(hc, hf):
                if tt is not None and a['t'] > tt:
                    break
                for campo in ('W', 'celdas', 'splits', 'mord_ac', 'vis_ac'):
                    if J(a[campo]) != J(b[campo]):
                        iguales = False
            ok0 += iguales
            nc, nf = techo_n(rc['hist']), techo_n(rf['hist'])
            Nc.append(nc); Nf.append(nf); Mc.append(m_max(rc['hist'])); Mf.append(m_max(rf['hist']))
            if nc != nf:
                n0 = min(nc, nf); t_chk = n0 * pt
                difN.append((s, nc, nf, tt, t_chk))
                if tt is None or not tt < t_chk:
                    viol1.append(s)
        C0 &= ok0 == S; C1 &= not viol1
        g = {l: [r for r in res_C if r['cond'] == cond and r['lam'] == l] for l in (0.0, LAM)}
        ceros = {l: sum(1 for r in g[l] for v in hist_sorted(r)[-1]['W'].values() if abs(v) < 0.0005) for l in g}
        totv = {l: sum(len(hist_sorted(r)[-1]['W']) for r in g[l]) for l in g}
        agot = {l: sum(r['t_agot'] is not None for r in g[l]) for l in g}
        trunc = {l: sum(r['t_techo'] is not None for r in g[l]) for l in g}
        igualesN = sum(a == b for a, b in zip(Nc, Nf))
        mmax_ok = sum(b >= a for a, b in zip(Mc, Mf))
        resumen_C[cond] = dict(C0=ok0, N_iguales=igualesN, N_control=med(Nc), N_arreglo=med(Nf), difN=difN,
                               C1_violaciones=viol1, ceros=ceros, total_valores=totv, agotan=agot, truncan=trunc,
                               Mmax_arreglo_ge=mmax_ok, Mmax_control=med(Mc), Mmax_arreglo=med(Mf))
        log(f"  {cond}: C0 identico antes de la truncacion {ok0}/{S}; truncan control {trunc[0.0]}/{S}, arreglo {trunc[LAM]}/{S}")
        log(f"      t_techo control {fmt(med([r['t_techo'] for r in g[0.0]]),0)}")
        log(f"      N* control {fmt(med(Nc),1)}  arreglo {fmt(med(Nf),1)}  iguales {igualesN}/{S}  difieren: {difN}")
        log(f"      C1 violaciones: {viol1 or 'ninguna'}")
        log(f"      W==0.000 al final: control {ceros[0.0]}/{totv[0.0]}  arreglo {ceros[LAM]}/{totv[LAM]}")
        log(f"      agotan 90 celdas: control {agot[0.0]}/{S}  arreglo {agot[LAM]}/{S}")
        log(f"      M_max control {fmt(med(Mc),1)}  arreglo {fmt(med(Mf),1)}  arreglo>=control {mmax_ok}/{S}")
        log(f"      muertes control {fmt(med([r['deaths'] for r in g[0.0]]),0)}  arreglo {fmt(med([r['deaths'] for r in g[LAM]]),0)}")
    rp = resumen_C['C_T20']
    C2 = rp['N_iguales'] >= 18
    C3 = rp['ceros'][0.0] >= 0.70 * rp['total_valores'][0.0] and rp['ceros'][LAM] <= 0.05 * rp['total_valores'][LAM]
    C4 = rp['agotan'][0.0] >= 18 and rp['agotan'][LAM] <= 10
    C5 = rp['Mmax_arreglo_ge'] >= UMBRAL_SEM
    log("")
    log(f"  C0 [exacta] identico antes de la primera truncacion, todas las condiciones : {'SOSTENIDA' if C0 else 'REFUTADA'}")
    log(f"  C1 [derivada] N* solo difiere si la truncacion precede al checkpoint n0+1    : {'SOSTENIDA' if C1 else 'REFUTADA'}")
    log(f"  C2 [ext] N* igual >=18/20 (C_T20)                                             : {'SOSTENIDA' if C2 else 'REFUTADA'}")
    log(f"  C3 [ext] W=0 exacto control >=70%, arreglo <=5% (C_T20)                        : {'SOSTENIDA' if C3 else 'REFUTADA'}")
    log(f"  C4 [ext] agotamiento control >=18/20, arreglo <=10/20 (C_T20)                  : {'SOSTENIDA' if C4 else 'REFUTADA'}")
    log(f"  C5 M_max arreglo >= control en >=15/20 (C_T20)                                 : {'SOSTENIDA' if C5 else 'REFUTADA'}")
    V.update(C0=C0, C1=C1, C2=C2, C3=C3, C4=C4, C5=C5)

    # ===== COSTE =====
    log(""); log("=" * 96); log("CRITERIO DE COSTE — pareado por semilla, arreglo - control"); log("=" * 96)
    coste = {}
    for cond in PRINCIPALES + ['C_T60', 'C_F20']:
        res = res_S if cond.startswith('S') else res_C
        pares = [par(res, cond, s) for s in seeds]
        valida = sum(c['t_techo'] is not None for c, _ in pares) >= UMBRAL_SEM
        fila = dict(valida=valida)
        for M, campo in (('M1_muertes', 'deaths'), ('M2_veneno', 'mv_tot'), ('M3_comida', 'mc_tot')):
            d = [f[campo] - c[campo] for c, f in pares]
            peor = sum(x > 0 for x in d); mejor = sum(x < 0 for x in d); md = float(np.median(d))
            fila[M] = dict(peor=peor, mejor=mejor, mediana=md, rango=(min(d), max(d)),
                           COSTE=(peor >= UMBRAL_SEM and md > 0))
        coste[cond] = fila
        voto = cond in PRINCIPALES
        log(f"  {cond} {'(principal)' if voto else '(sin voto)  '} control trunca en >=15/20: "
            f"{'SI' if valida else 'NO -> NULA'}")
        for M in ('M1_muertes', 'M2_veneno', 'M3_comida'):
            x = fila[M]
            log(f"      {M:11s} arreglo peor {x['peor']:2d}/{S}, mejor {x['mejor']:2d}/{S}, mediana dif {x['mediana']:+8.1f} "
                f"rango [{x['rango'][0]:+d}, {x['rango'][1]:+d}]" + (f"  COSTE={x['COSTE']}" if M != 'M3_comida' else "  (sin voto)"))
    nulas = [c for c in PRINCIPALES if not coste[c]['valida']]
    con_coste = [c for c in PRINCIPALES if coste[c]['M1_muertes']['COSTE'] or coste[c]['M2_veneno']['COSTE']]
    PASA = bool(S0 and C0 and not nulas and not con_coste)
    log("")
    log(f"  condiciones principales NULAS: {nulas or 'ninguna'}")
    log(f"  condiciones principales con COSTE: {con_coste or 'ninguna'}")
    if not (S0 and C0):
        log("  *** S0 o C0 REFUTADA: por el preregistro sec. 7, se para. Lo de arriba NO se lee.")
    log(f"  PRUEBA DE COSTE: {'PASA' if PASA else 'NO PASA'}")
    V.update(nulas=nulas, con_coste=con_coste, PASA=PASA)

    # ---------- ETAPA 5: ESCRITURA ----------
    log("ETAPA 5/5 — escritura de datos.")
    meta = dict(experimento='BUG01_coste_techo', fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), n_semillas=S, lam=LAM,
                S=dict(T=S_T, invertir_cada=S_CADA, fases=NF), C=[dict(cond=c, plast=p, paso_t=pt) for c, p, pt in CONDS_C],
                principales=PRINCIPALES, umbral_semillas=UMBRAL_SEM, paralelo=N_PARALELO,
                sha_preregistro=h16(os.path.join(AQUI, 'PREREGISTRO_coste_techo.md')),
                sha_script=h16(os.path.abspath(__file__)),
                sha_constructor=h16(os.path.join(AQUI, 'construye_coste_techo.py')),
                sha_organismo_v7h=h16(os.path.join(AQUI, 'organismo_v7h.py')),
                sha_organismo_caph=h16(os.path.join(AQUI, 'organismo_caph.py')),
                sha_organismo_v7e=h16(os.path.join(AQUI, 'organismo_v7e.py')),
                sha_organismo_v7=h16(os.path.join(RAIZ, 'organismo', 'organismo_v7.py')),
                sha_organismo_cap=h16(os.path.join(CAPDIR, 'organismo_cap.py')),
                sha_parte2_capacidad=h16(os.path.join(CAPDIR, 'parte2_capacidad.py')),
                python=platform.python_version(), numpy=np.__version__, plataforma=platform.platform(),
                procesos_python_al_arrancar=ps, veredictos=V, coste=coste, resumen_C=resumen_C)
    djson = os.path.join(SALIDA, f'coste_techo_{stamp}.json')
    json.dump(dict(meta=meta, control_inercia=res_ctrl, bloque_S=res_S, bloque_C=res_C),
              open(djson, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
    dcsv = os.path.join(SALIDA, f'coste_techo_{stamp}.csv')
    cols = ['bloque', 'cond', 'plast', 'paso_t', 'lam', 'seed', 't_techo', 'techo_primero', 'n_techo', 'deaths',
            'mv_tot', 'mc_tot', 'splits', 'celdas', 't_agot', 'err_max', 'Nstar', 'Mmax', 'W_A_fin', 'W_B_fin']
    with open(dcsv, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction='ignore'); w.writeheader()
        for r in sorted(res_S + res_C, key=lambda r: (r['bloque'], r['cond'], r['lam'], r['seed'])):
            fila = {k: r.get(k) for k in cols}
            if r['bloque'] == 'C':
                fila.update(Nstar=techo_n(r['hist']), Mmax=m_max(r['hist']))
            else:
                fila.update(W_A_fin=round(r['fases']['A']['W'][NF-1], 4), W_B_fin=round(r['fases']['B']['W'][NF-1], 4))
            w.writerow({k: ('' if v is None else v) for k, v in fila.items()})
    log(f"datos -> {os.path.basename(djson)}  sha256_16 = {h16(djson)}")
    log(f"         {os.path.basename(dcsv)}  sha256_16 = {h16(dcsv)}")
    log("")
    log(f"VEREDICTO coste_techo: " + " ".join(f"{k}={v}" for k, v in V.items()))
    log("Pega en el registro: fecha, veredictos y hashes de arriba (regla 7).")
    _log['f'].close()
