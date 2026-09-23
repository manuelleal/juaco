"""FANIN (nivel 7) — runner del bloque. Ejecuta PREREGISTRO_fanin.md. REGLA 10: log desde el arranque.

Cambio UNICO: entradas por celda de la expansion Kenyon, brazos F6 (tronco), F3, F2. Mismas semillas pareadas.
Instrumento: organismo_v142g_fanin.py (identidad 23/23 con fanin=6, identidad_fanin_salida.txt), kwargs del tronco
LEIDOS de la entrada 'organismo_v142' de organismo/bateria_generaliza_v142.py (congelada; regla 14) + fanin + diag.

Tareas por (brazo, semilla), T = 200 000, sonda a priori en T/2 (antes de ver los de test):
  mundo 'rejilla' (63 patrones, particion POR VARIANTES dentro de cada fila, todas las filas vistas):
      conj (a AND b), np (patron negativo A+ B+ AB-), xor (a XOR b), par3 (paridad de a,b,c), px0 (control lineal),
      azar (control de fuga)
  mundo 'regla' = ETAPA 3 del repo (20 patrones de peso 3; bateria_generaliza): px0, azar (G1/G2/K con los umbrales
      de la bateria) + xor01 (la XOR historica del repo, secundaria)
Serie completa (NO se corre sin el coordinador): Pool(--pool N) sobre las tareas; despues, en serie y por brazo, el
examen v3' (bateria_v142_fanin.py) y la bateria de generalizacion copiada (bateria_generaliza_v142_fanin.py).

Uso:  python experimentos/nivel07_fanin_expansion/corre_fanin.py --humo          (UN proceso: 3 brazos x 2 semillas, T=20000)
      python experimentos/nivel07_fanin_expansion/corre_fanin.py --pool 6        (la serie: semillas 6001-6020)
      [--desde N] [--sin_baterias]
"""
import sys, os, json, time, hashlib, platform, importlib, subprocess, math
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORG = os.path.join(RAIZ, 'organismo')
sys.path[:0] = [AQUI, ORG]

HUMO = '--humo' in sys.argv
POOL = int(sys.argv[sys.argv.index('--pool') + 1]) if '--pool' in sys.argv else None
DESDE = int(sys.argv[sys.argv.index('--desde') + 1]) if '--desde' in sys.argv else (6001 if HUMO else 6021)   # serie 6021-6040; 6001-6020 quemadas (humo/exploracion); replica 6041-6060
SEEDS = [DESDE, DESDE + 1] if HUMO else list(range(DESDE, DESDE + 20))
T = 20000 if HUMO else 200000
BRAZOS = {'F6': 6, 'F3': 3, 'F2': 2}
REJILLA = ['conj', 'np', 'xor', 'par3', 'px0', 'azar']
ETAPA3 = ['px0', 'azar', 'xor01']
PRUEBAS = ['np', 'xor', 'par3', 'conj']          # las cuatro pedidas por el director
MEJORA = ['np', 'xor', 'par3']                   # familia de "mejora" (Holm): 3 pruebas x 2 brazos = 6
MARGEN = 0.05; MIN_SEM = 15                       # PREREGISTRO_fanin.md §6
VALIDEZ = 0.30                                    # puerta de validez: fraccion de nunca vistos por la via rapida en la sonda
POOL_SEM = 10                                     # puerta de pool: lleno antes de T/2 en >= 10/20 semillas
NKMAX = 90
_log = {'f': None, 't0': time.time()}


def log(msg=""):
    linea = f"[{time.strftime('%H:%M:%S')} +{time.time()-_log['t0']:7.1f}s] {msg}"
    print(linea, flush=True)
    if _log['f']:
        _log['f'].write(linea + "\n"); _log['f'].flush(); os.fsync(_log['f'].fileno())


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def KW_TRONCO():
    bg = importlib.import_module('bateria_generaliza_v142')   # CONGELADA: solo se lee la entrada del tronco (regla 14)
    return dict(bg.INSTRUMENTOS['organismo_v142'][1])


def bal(W, test, vr):
    """acierto de signo BALANCEADO (media de comida y veneno; valor 0 exacto = 0.5), la formula de bateria_generaliza."""
    if W is None:
        return None
    f = [1.0 if W[k] > 0 else (0.5 if W[k] == 0 else 0.0) for k in test if vr[k] == 'comida']
    p = [1.0 if W[k] < 0 else (0.5 if W[k] == 0 else 0.0) for k in test if vr[k] == 'veneno']
    return 0.5 * float(np.mean(f)) + 0.5 * float(np.mean(p)) if f and p else None


def tarea(args):
    brazo, mundo, regla, seed, T_, kw = args
    g = importlib.import_module('organismo_v142g_fanin')
    t0 = time.time()
    r = g.run(seed, T=T_, mundo=mundo, regla=regla, fanin=BRAZOS[brazo], diag=True, **kw)
    dt = time.time() - t0
    if mundo == 'rejilla':
        _, _, rel, fila, vr = g.info_rejilla(seed, regla)
    else:
        vr = g.split_regla(seed, regla)[3]; fila = {k: '' for k in vr}; rel = None
    test = r['test']; D = r['diag_fanin']
    pf = [r['primer'][k]['pb'] for k in test if r['primer'][k] is not None and vr[k] == 'comida']
    pp = [1 - r['primer'][k]['pb'] for k in test if r['primer'][k] is not None and vr[k] == 'veneno']
    por_fila = {}
    for f in sorted(set(fila[k] for k in test)):
        ks = [k for k in test if fila[k] == f]
        s = [(1.0 if (r['W_apriori'][k] > 0) == (vr[k] == 'comida') and r['W_apriori'][k] != 0 else (0.5 if r['W_apriori'][k] == 0 else 0.0)) for k in ks]
        por_fila[f] = round(float(np.mean(s)), 4)
    acc = bal(r['W_apriori'], test, vr)
    E = D['encuentros']; tren = r['tren']
    t_lleno = r['split_t'][NKMAX - 30 - 1][0] if r['splits'] >= NKMAX - 30 else None   # celdas == 30 + splits (identidad 4a')
    return dict(rapida_sonda_test=float(np.mean([D['familiar_apriori'][k] for k in test])),
                rapida_sonda_tren=float(np.mean([D['familiar_apriori'][k] for k in tren])),
                rapida_enc_test=(E['rap_test'] / E['enc_test'] if E['enc_test'] else None),
                rapida_enc_tren2=(E['rap_tren2'] / E['enc_tren2'] if E['enc_tren2'] else None), encuentros=E,
                pool_final=r['celdas'], t_lleno=t_lleno, lleno_antes_T2=(t_lleno is not None and t_lleno < T_ // 2),brazo=brazo, fanin=BRAZOS[brazo], mundo=mundo, regla=regla, seed=seed, T=T_, seg=round(dt, 2), rel=rel,
                acc=acc, J=(None if acc is None else 2 * acc - 1),
                acc_rapida=bal(D['W_rapida_apriori'], test, vr), acc_lenta=bal(D['W_lenta_apriori'], test, vr),
                familiar_test=float(np.mean([D['familiar_apriori'][k] for k in test])),
                alias_test=float(np.mean([D['alias_test'][k] for k in test])),
                ba=(0.5 * float(np.mean(pf)) + 0.5 * float(np.mean(pp))) if (pf and pp) else None,
                cobertura_primer=sum(v is not None for v in r['primer'].values()), n_test=len(test), n_tren=len(r['tren']),
                por_fila=por_fila, splits=r['splits'], celdas=r['celdas'], deaths=r['deaths'],
                cobertura=D['cobertura'], empates=dict(llamadas=D['llamadas'], empates=D['empates'], empates_cero=D['empates_cero'],
                                                       frac=D['empates'] / max(D['llamadas'], 1)),
                foto_ini=D['ini'], foto_sonda=D['sonda'], foto_fin=D['fin'])


# ------------------------------------------------------------------ estadistica preregistrada
def signo_p(k, n):
    """P(X >= k) con X ~ Bin(n, 1/2): prueba de signo exacta, una cola (empates excluidos de n)."""
    return sum(math.comb(n, i) for i in range(k, n + 1)) / 2 ** n if n else 1.0


def pareado(a, b):
    """a, b: dict semilla -> valor. Devuelve mediana de (a-b), # a>b, # a<b, # empates, p una cola (a>b) y (a<b)."""
    ss = sorted(s for s in a if s in b and a[s] is not None and b[s] is not None)
    d = [a[s] - b[s] for s in ss]
    up = sum(x > 0 for x in d); dn = sum(x < 0 for x in d); n = up + dn
    return dict(n=len(ss), med=float(np.median(d)) if d else None, sube=up, baja=dn, empata=len(ss) - n,
                p_sube=signo_p(up, n), p_baja=signo_p(dn, n))


def holm(ps):
    """ps: dict nombre -> p. Devuelve dict nombre -> p ajustada de Holm (monotona)."""
    orden = sorted(ps, key=lambda k: ps[k]); m = len(orden); out = {}; acum = 0.0
    for i, k in enumerate(orden):
        acum = max(acum, min(1.0, (m - i) * ps[k])); out[k] = acum
    return out


def med(xs):
    xs = [x for x in xs if x is not None]
    return (float(np.median(xs)), float(min(xs)), float(max(xs))) if xs else (None, None, None)


def f3(x):
    return '  n/a' if x is None else f"{x:.3f}"


def resumen(res, seeds):
    V = {}
    G = lambda b, m, rg, campo: {r['seed']: r[campo] for r in res if r['brazo'] == b and r['mundo'] == m and r['regla'] == rg}
    log()
    log("=== ACIERTO EN NUNCA VISTOS (sonda a priori, valor total, balanceado; mediana [min, max]) ===")
    log(f"{'mundo':8s} {'regla':6s} " + " ".join(f"{b:>22s}" for b in BRAZOS) + "   | via rapida sola (F6/F3/F2) | via lenta sola | familiar test | alias test")
    for m, rgs in (('rejilla', REJILLA), ('regla', ETAPA3)):
        for rg in rgs:
            c = [med(list(G(b, m, rg, 'acc').values())) for b in BRAZOS]
            ra = [med(list(G(b, m, rg, 'acc_rapida').values()))[0] for b in BRAZOS]
            le = [med(list(G(b, m, rg, 'acc_lenta').values()))[0] for b in BRAZOS]
            fa = [med(list(G(b, m, rg, 'familiar_test').values()))[0] for b in BRAZOS]
            al = [med(list(G(b, m, rg, 'alias_test').values()))[0] for b in BRAZOS]
            log(f"{m:8s} {rg:6s} " + " ".join(f"{f3(x[0])} [{f3(x[1])},{f3(x[2])}]" for x in c)
                + f"   | {'/'.join(f3(x) for x in ra)} | {'/'.join(f3(x) for x in le)} | {'/'.join(f3(x) for x in fa)} | {'/'.join(f3(x) for x in al)}")
    log()
    log("=== DIAGNOSTICOS POR BRAZO (medianas sobre todas las tareas del brazo) ===")
    for m in ('rejilla', 'regla'):
        for b in BRAZOS:
            rr = [r for r in res if r['brazo'] == b and r['mundo'] == m]
            if not rr:
                continue
            q = lambda fn: med([fn(r) for r in rr])[0]
            log(f"  {m:8s} {b}: COBERTURA pixeles leidos {q(lambda r: r['cobertura']['pixeles_leidos']):.0f}/6 (min por semilla "
                f"{min(r['cobertura']['pixeles_leidos'] for r in rr)}), lecturas minimas por pixel {q(lambda r: r['cobertura']['min_lecturas']):.0f}"
                f" | EMPATES en la frontera del ganan-K: {q(lambda r: r['empates']['frac']):.4f} de las llamadas (max {max(r['empates']['frac'] for r in rr):.4f};"
                f" en cero {q(lambda r: r['empates']['empates_cero'] / max(r['empates']['llamadas'], 1)):.4f}), por patron en la sonda {q(lambda r: r['foto_sonda']['empates_frontera']):.3f}")
            log(f"               SOLAPAMIENTO |c(P)&c(Q)|/K en la sonda: todos {q(lambda r: r['foto_sonda']['solap_medio']):.3f}  d=1 {f3(q(lambda r: r['foto_sonda']['solap_d1']))}"
                f"  d=2 {f3(q(lambda r: r['foto_sonda']['solap_d2']))}  (inicio: todos {q(lambda r: r['foto_ini']['solap_medio']):.3f})"
                f" | codigos distintos {q(lambda r: r['foto_sonda']['codigos_distintos'] / r['foto_sonda']['patrones']):.3f} de los patrones"
                f" | CELDAS: usadas {q(lambda r: r['foto_sonda']['frac_usadas']):.3f}, con impulso>0 por patron {q(lambda r: r['foto_sonda']['frac_drive_pos']):.3f},"
                f" activas al final {q(lambda r: r['celdas']):.0f}, fanin efectivo final mediana {q(lambda r: r['foto_fin']['fanin_ef_mediana']):.1f} (max {max(r['foto_fin']['fanin_ef_max'] for r in rr)})")

    # --- PUERTA DE VALIDEZ y PUERTA DE POOL (PREREGISTRO §6b, §6c)
    log()
    log(f"=== VALIDEZ: fraccion de NUNCA VISTOS por la via rapida (sonda a priori; puerta >= {VALIDEZ}) y POOL (lleno antes de T/2 en >= {POOL_SEM}/20) ===")
    log(f"{'mundo':8s} {'regla':6s} {'brazo':5s} {'sonda test':>10s} {'sonda tren':>10s} {'enc test':>9s} {'enc tren':>9s} {'pool fin':>8s} {'t_lleno med':>11s} {'lleno<T/2':>9s}  validez")
    for m, rgs in (('rejilla', REJILLA), ('regla', ETAPA3)):
        for rg in rgs:
            for b in BRAZOS:
                rr = [r for r in res if r['brazo'] == b and r['mundo'] == m and r['regla'] == rg]
                q = lambda k: med([r[k] for r in rr])[0]
                tl = [r['t_lleno'] for r in rr if r['t_lleno'] is not None]
                nll = sum(r['lleno_antes_T2'] for r in rr)
                val = q('rapida_sonda_test') is not None and q('rapida_sonda_test') >= VALIDEZ
                pool_ok = nll < POOL_SEM * len(seeds) / 20
                V[f'validez_{m}_{rg}_{b}'] = dict(valido=bool(val), pool_ok=bool(pool_ok), rapida_sonda_test=q('rapida_sonda_test'),
                                                   rapida_enc_test=q('rapida_enc_test'), lleno_antes_T2=nll, pool_final=q('pool_final'))
                log(f"{m:8s} {rg:6s} {b:5s} {f3(q('rapida_sonda_test')):>10s} {f3(q('rapida_sonda_tren')):>10s} {f3(q('rapida_enc_test')):>9s} {f3(q('rapida_enc_tren2')):>9s}"
                    f" {q('pool_final'):8.0f} {(f'{np.median(tl):.0f}' if tl else 'no llena'):>11s} {nll:>5d}/{len(rr)}  {'VALIDO' if val else 'NO CONCLUYENTE'}{'' if pool_ok else ' + POOL LLENO (mide capacidad)'}")

    # --- ETAPA 3 (bateria_generaliza, umbrales sin tocar) por brazo
    log()
    log("=== ETAPA 3 (bateria_generaliza: G1 px0 >= 0.65, azar en [0.35,0.65], px0>azar >= 70 %; G2 conducta; K cobertura) ===")
    for b in BRAZOS:
        px, az = G(b, 'regla', 'px0', 'acc'), G(b, 'regla', 'azar', 'acc')
        bpx, baz = G(b, 'regla', 'px0', 'ba'), G(b, 'regla', 'azar', 'ba')
        cob = G(b, 'regla', 'px0', 'cobertura_primer')
        S = len(seeds)
        mpx = med(list(px.values()))[0]; maz = med(list(az.values()))[0]
        p1 = sum(px[s] > az[s] for s in seeds if s in px and s in az)
        bp = [x for x in bpx.values() if x is not None]; bz = [x for x in baz.values() if x is not None]
        p2 = sum(1 for s in seeds if bpx.get(s) is not None and baz.get(s) is not None and bpx[s] > baz[s])
        g1 = mpx is not None and mpx >= 0.65 and 0.35 <= maz <= 0.65 and p1 >= 0.7 * S
        g2 = bool(bp) and bool(bz) and np.median(bp) >= 0.55 and 0.42 <= np.median(bz) <= 0.58 and p2 >= 0.7 * S
        k = sum(cob[s] >= 6 for s in cob) >= 0.9 * S
        V[f'E3_{b}'] = dict(G1=bool(g1), G2=bool(g2), K=bool(k), px0=mpx, azar=maz)
        log(f"  {b}: G1 {'PASA' if g1 else 'FALLA'} (px0 {f3(mpx)}, azar {f3(maz)}, px0>azar {p1}/{S})  "
            f"G2 {'PASA' if g2 else 'FALLA'} (px0 {f3(float(np.median(bp)) if bp else None)}, azar {f3(float(np.median(bz)) if bz else None)}, {p2}/{S})  K {'OK' if k else 'FALLA'}")

    # --- comparaciones pareadas preregistradas
    log()
    log(f"=== COMPARACIONES PAREADAS POR SEMILLA (F vs F6; mejora = mediana >= +{MARGEN}, >= {MIN_SEM}/20 suben, Holm p < 0.05; en el humo n = {len(seeds)}: la puerta NO puede pasar) ===")
    fam = {}; filas = {}
    for rg in PRUEBAS:
        for b in ('F3', 'F2'):
            c = pareado(G(b, 'rejilla', rg, 'acc'), G('F6', 'rejilla', rg, 'acc')); filas[(rg, b)] = c
            if rg in MEJORA:
                fam[(rg, b)] = c['p_sube']
    ph = holm({f"{k[0]}|{k[1]}": v for k, v in fam.items()})
    for (rg, b), c in filas.items():
        adj = ph.get(f"{rg}|{b}")
        mejora = c['med'] is not None and c['med'] >= MARGEN and c['sube'] >= MIN_SEM and adj is not None and adj < 0.05
        igual = c['med'] is not None and abs(c['med']) < MARGEN and min(1.0, 2 * min(c['p_sube'], c['p_baja'])) >= 0.05
        vv = V[f'validez_rejilla_{rg}_{b}']; concl = vv['valido'] and vv['pool_ok'] and V[f'validez_rejilla_{rg}_F6']['pool_ok']
        V[f'{rg}_{b}'] = dict(mejora=bool(mejora), no_cambia=bool(igual), concluyente=bool(concl), **c, p_holm=adj)
        log(f"  {rg:5s} {b} vs F6: mediana {c['med']:+.3f}  sube {c['sube']} baja {c['baja']} empata {c['empata']}  p1 {c['p_sube']:.4f}"
            + (f" Holm {adj:.4f}" if adj is not None else " (fuera de la familia de mejora)")
            + f"  -> MEJORA {'SI' if mejora else 'no'}  NO_CAMBIA {'SI' if igual else 'no'}"
            + ("" if concl else "  [NO CONCLUYENTE para el cableado: validez o pool]"))
    # 6d (PROPUESTA, pendiente del coordinador): la misma puerta sobre acc_rapida (via rapida leida directamente); se imprime, no se declara
    fr = {(rg, b): pareado(G(b, 'rejilla', rg, 'acc_rapida'), G('F6', 'rejilla', rg, 'acc_rapida')) for rg in MEJORA for b in ('F3', 'F2')}
    phr = holm({f"{k[0]}|{k[1]}": v['p_sube'] for k, v in fr.items()})
    for (rg, b), c in fr.items():
        m_ = c['med'] is not None and c['med'] >= MARGEN and c['sube'] >= MIN_SEM and phr[f"{rg}|{b}"] < 0.05
        V[f'rapida_{rg}_{b}'] = dict(mejora_secundaria=bool(m_), **c, p_holm=phr[f"{rg}|{b}"])
        log(f"  [6d secundario, sin veredicto] acc_rapida {rg:5s} {b} vs F6: mediana {c['med']:+.3f} sube {c['sube']}/{c['n']} Holm {phr[f'{rg}|{b}']:.4f} -> {'MEJORA' if m_ else 'no'}")
    # media de las cuatro pruebas (prediccion general del director)
    for b in ('F3', 'F2'):
        m4 = lambda bb: {s: float(np.mean([G(bb, 'rejilla', rg, 'acc')[s] for rg in PRUEBAS])) for s in seeds
                         if all(s in G(bb, 'rejilla', rg, 'acc') and G(bb, 'rejilla', rg, 'acc')[s] is not None for rg in PRUEBAS)}
        c = pareado(m4(b), m4('F6'))
        V[f'media4_{b}'] = dict(mejora=bool(c['med'] is not None and c['med'] >= MARGEN and c['sube'] >= MIN_SEM and min(1.0, 2 * c['p_sube']) < 0.05), **c)
        log(f"  media de las 4  {b} vs F6: mediana {c['med']:+.3f}  sube {c['sube']}/{c['n']}  p1 {c['p_sube']:.4f} (Bonferroni x2)  -> MEJORA {'SI' if V[f'media4_{b}']['mejora'] else 'no'}")
    # costo del director: Etapa 3 px0 baja
    for b in ('F3', 'F2'):
        c = pareado(G(b, 'regla', 'px0', 'acc'), G('F6', 'regla', 'px0', 'acc'))
        cae = c['med'] is not None and c['med'] <= -MARGEN and c['baja'] >= MIN_SEM and min(1.0, 2 * c['p_baja']) < 0.05
        sol = pareado({r['seed']: r['foto_sonda']['solap_medio'] for r in res if r['brazo'] == b and r['mundo'] == 'regla' and r['regla'] == 'px0'},
                      {r['seed']: r['foto_sonda']['solap_medio'] for r in res if r['brazo'] == 'F6' and r['mundo'] == 'regla' and r['regla'] == 'px0'})
        V[f'costo_E3_{b}'] = dict(costo_cumple=bool(cae), **c, solap=sol)
        log(f"  COSTO Etapa 3 px0 {b} vs F6: mediana {c['med']:+.3f}  baja {c['baja']}/{c['n']}  p1 {c['p_baja']:.4f} (Bonferroni x2) -> BAJA {'SI' if cae else 'no'}"
            f" | solapamiento en la sonda {b}-F6 mediana {sol['med']:+.3f} (baja {sol['baja']}/{sol['n']})")
    # placebo (regla 15): F6 contra F6 con el emparejamiento de semillas corrido en una
    log()
    log("=== PLACEBO (regla 15): la misma puerta de mejora sobre F6(s) contra F6(s+1 ciclico); debe pasar 0 de 4 ===")
    npl = 0
    for rg in PRUEBAS:
        a = G('F6', 'rejilla', rg, 'acc'); ss = sorted(a)
        b = {ss[i]: a[ss[(i + 1) % len(ss)]] for i in range(len(ss))}
        c = pareado(a, b)
        pasa = c['med'] is not None and c['med'] >= MARGEN and c['sube'] >= MIN_SEM and c['p_sube'] < 0.05
        npl += pasa
        log(f"  {rg:5s}: mediana {c['med']:+.3f} sube {c['sube']}/{c['n']} p1 {c['p_sube']:.4f} -> {'PASA (MAL)' if pasa else 'no pasa (bien)'}")
    V['placebo_pasan'] = npl
    # controles que pueden fallar
    log()
    log("=== CONTROLES QUE PUEDEN FALLAR (en cada brazo) ===")
    for b in BRAZOS:
        px = med(list(G(b, 'rejilla', 'px0', 'acc').values()))[0]; az = med(list(G(b, 'rejilla', 'azar', 'acc').values()))[0]
        ok = px is not None and px >= 0.65 and az is not None and 0.35 <= az <= 0.65
        V[f'control_{b}'] = dict(px0=px, azar=az, ok=bool(ok))
        e3 = V[f'E3_{b}']['G1']; V[f'control_{b}']['E3_px0_G1'] = e3; V[f'control_{b}']['ok'] = bool(ok and e3)
        log(f"  {b}: rejilla px0 {f3(px)} (>= 0.65)  azar {f3(az)} (en [0.35, 0.65])  Etapa 3 G1 (control positivo del tronco) {'PASA' if e3 else 'FALLA'}"
            f"  -> {'OK' if ok and e3 else 'FALLA: el bloque no se lee'}")
    return V


def main():
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    stamp = time.strftime('%Y%m%d_%H%M%S')
    dat = os.path.join(RAIZ, 'datos', 'humo') if HUMO else os.path.join(RAIZ, 'datos')
    os.makedirs(dat, exist_ok=True)
    nombre = f"fanin_{'humo' if HUMO else 's%d-%d' % (SEEDS[0], SEEDS[-1])}_{stamp}"
    _log['f'] = open(os.path.join(dat, nombre + '.log'), 'w', encoding='utf-8', newline='\n')
    if not HUMO and not POOL:
        raise SystemExit('La serie necesita --pool N (lo decide el coordinador). Para el humo: --humo.')
    log(f"=== FANIN — {'HUMO (UN proceso, NO es dato)' if HUMO else 'SERIE'}: brazos {BRAZOS}, semillas {SEEDS[0]}..{SEEDS[-1]}, T={T} ===")
    idf = os.path.join(AQUI, 'identidad_fanin_salida.txt')
    txt = open(idf, encoding='utf-8').read() if os.path.exists(idf) else ''
    ins = h16(os.path.join(AQUI, 'organismo_v142g_fanin.py'))
    if 'TODO IDENTICO' not in txt or f'sha {ins}  organismo_v142g_fanin.py' not in txt:
        raise SystemExit('*** el arnes de identidad no esta en verde para ESTE instrumento: correr identidad_fanin.py primero.')
    log(f"identidad: {txt.strip().splitlines()[-1].split('] ', 1)[1]}  (instrumento {ins})")
    kw = KW_TRONCO()
    log(f"kwargs del tronco (regla 14, leidos de bateria_generaliza_v142 congelada): {kw}")
    shas = {n: h16(os.path.join(AQUI, n)) for n in ('organismo_v142g_fanin.py', 'organismo_v142_fanin.py', 'bateria_v142_fanin.py',
                                                     'bateria_generaliza_v142_fanin.py', 'corre_fanin.py', 'construye_fanin.py')}
    shas['PREREGISTRO_fanin.md'] = h16(os.path.join(AQUI, 'PREREGISTRO_fanin.md')) if os.path.exists(os.path.join(AQUI, 'PREREGISTRO_fanin.md')) else None
    shas['bateria_generaliza_v142.py (congelada)'] = h16(os.path.join(ORG, 'bateria_generaliza_v142.py'))
    for n, s in shas.items():
        log(f"  sha {s}  {n}")
    trabajos = [(b, m, rg, s, T, kw) for s in SEEDS for b in BRAZOS for m, rgs in (('rejilla', REJILLA), ('regla', ETAPA3)) for rg in rgs]
    log(f"ETAPA 1/3 — {len(trabajos)} corridas ({len(BRAZOS)} brazos x {len(REJILLA) + len(ETAPA3)} reglas x {len(SEEDS)} semillas)"
        + (" en UN proceso" if HUMO else f" con Pool({POOL})"))
    res = []; t0 = time.time()
    if HUMO:
        it = map(tarea, trabajos)
        for i, r in enumerate(it, 1):
            res.append(r)
            log(f"   {i:3d}/{len(trabajos)} {r['brazo']} {r['mundo']:7s} {r['regla']:5s} s{r['seed']}  acc {f3(r['acc'])}  rapida {f3(r['acc_rapida'])}"
                f"  rapida(sonda test) {r['rapida_sonda_test']:.2f}  pool {r['pool_final']} lleno {r['t_lleno']}  empates {r['empates']['frac']:.4f}  {r['seg']:.1f}s")
    else:
        with mp.Pool(POOL) as pool:
            for i, r in enumerate(pool.imap_unordered(tarea, trabajos, chunksize=1), 1):
                res.append(r)
                if i % 20 == 0 or i == len(trabajos):
                    log(f"   {i}/{len(trabajos)}")
    pared = time.time() - t0
    log(f"ETAPA 2/3 — resumen ({pared:.0f} s de pared)")
    V = resumen(res, SEEDS)
    # tiempos y estimacion de la serie
    seg_paso = {m: float(np.mean([r['seg'] / r['T'] for r in res if r['mundo'] == m])) for m in ('rejilla', 'regla')}
    seg_paso_b = {b: float(np.mean([r['seg'] / r['T'] for r in res if r['brazo'] == b])) for b in BRAZOS}
    sp = float(np.mean([r['seg'] / r['T'] for r in res]))
    cpu_main = 3 * (len(REJILLA) + len(ETAPA3)) * 20 * 200000 * sp
    cpu_exam = 3 * ((2 * 7 * 6 * 2) + 9 * 20) * 100000 * sp        # examen v3': identidad 84 pares (168 corridas) + 9 etapas x 20
    cpu_gen = 3 * 2 * 20 * 200000 * sp                               # bateria_generaliza copiada: px0/azar x 20
    log()
    log(f"=== TIEMPOS: {sp*1e6:.1f} us/paso de media (rejilla {seg_paso['rejilla']*1e6:.1f}, regla {seg_paso['regla']*1e6:.1f};"
        f" F6 {seg_paso_b['F6']*1e6:.1f}, F3 {seg_paso_b['F3']*1e6:.1f}, F2 {seg_paso_b['F2']*1e6:.1f}) ===")
    log(f"  ESTIMACION de la serie de 20 semillas: tareas {cpu_main/3600:.2f} h de CPU -> Pool(6) ~{cpu_main/6/60:.0f} min;"
        f" examen v3' x3 {cpu_exam/3600:.2f} h -> Pool(6) ~{cpu_exam/6/60:.0f} min; generaliza x3 {cpu_gen/3600:.2f} h -> Pool(6) ~{cpu_gen/6/60:.0f} min;"
        f" TOTAL ~{(cpu_main+cpu_exam+cpu_gen)/6/60:.0f} min de pared con Pool(6) (sin contar colas ni otro Pool en paralelo)")
    dj = os.path.join(dat, nombre + '.json')
    json.dump(dict(meta=dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), humo=HUMO, semillas=SEEDS, T=T, brazos=BRAZOS, kwargs_tronco=kw, sha=shas,
                             margen=MARGEN, min_semillas=MIN_SEM, us_por_paso=sp * 1e6, pared_s=pared, estimacion_min_pool6=(cpu_main + cpu_exam + cpu_gen) / 6 / 60,
                             python=platform.python_version(), numpy=np.__version__, plataforma=platform.platform()),
                   veredictos=V, corridas=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
    log(f"datos -> {os.path.relpath(dj, RAIZ)}  sha256_16 = {h16(dj)}")
    if not HUMO and '--sin_baterias' not in sys.argv:
        log("ETAPA 3/3 — baterias del tronco por brazo (en serie, cada una con su Pool)")
        for b, f in BRAZOS.items():
            for cmd in ([sys.executable, os.path.join(AQUI, 'bateria_v142_fanin.py'), '20', '--desde', str(SEEDS[0]), '--fanin', str(f), '--pool', str(POOL), '--log'],
                        [sys.executable, os.path.join(AQUI, 'bateria_generaliza_v142_fanin.py'), 'organismo_v142_fanin', '20', '--desde', str(SEEDS[0]),
                         '--fanin', str(f), '--pool', str(POOL), '--log']):
                log(f"  {b}: {' '.join(os.path.basename(c) for c in cmd[1:])}")
                p = subprocess.run(cmd, cwd=AQUI, capture_output=True, text=True, encoding='utf-8', errors='replace')
                for l in p.stdout.strip().splitlines()[-4:]:
                    log(f"      {l}")
                if p.returncode:
                    log(f"      *** codigo de salida {p.returncode}: {p.stderr.strip()[-400:]}")
    log("FIN.")
    _log['f'].close()


if __name__ == '__main__':
    main()
