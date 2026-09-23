"""corre_n7.py -- bloque N7-NL (nivel 7, composicion temporal 3T-k EN EL TRONCO v14.2 y con la via lenta normalizada).

Preregistro: experimentos/subida_n7/PREREGISTRO_n7.md (escrito ANTES de la serie). Instrumento: mundo_n7.py
(por anclas desde mundo_composicion_v14.py, construye_n7.py; identidad: identidad_n7.py).

Brazos (todos arm='C3' -- canal de historia visible, plastico -- salvo NC3C):
  T142  el TRONCO v14.2 tal cual (kwargs campo a campo de organismo_v142.run; B-5 encendido)
  N     T142 + norm_lenta=1 (EL CANDIDATO)
  L015  T142 con la via lenta de v14.0 (eta_s 0.015, clip_s 3.0): control que PUEDE GANAR ("basta un paso chico")
  N141  N sin B-5 (desambiguar=0): que aporta B-5 a la composicion
  NAZAR N con la mascara al azar de la misma cardinalidad (mask_rel=4): control que PUEDE GANAR
  NSH   N sin hija dispersa (mask_rel=0)
  NC3C  N con canal FALSO (arm='C3C': la historia que ve es aleatoria; el mundo usa la real)

Uso:
  python experimentos/subida_n7/corre_n7.py --humo                       (1 proceso, semilla 7799, k=2,5,8; JSON en datos/humo/)
  python experimentos/subida_n7/corre_n7.py --desde 7701 --n 20 --pool 6 (serie)
  python experimentos/subida_n7/corre_n7.py --desde 7721 --n 20 --pool 6 (replica)
Opcionales: --ks 1,2,3,4,5,6,7,8   --T 100000   --brazos T142,N,...
"""
import hashlib, inspect, json, os, sys, time
from datetime import datetime

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
if AQUI not in sys.path: sys.path.insert(0, AQUI)
try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass

# ---- kwargs del TRONCO v14.2, CAMPO A CAMPO (regla 14 / ERR-38); identidad_n7.py los compara con organismo_v142.run ----
TRONCO = dict(eta=.03, tau_e=.85, alpha=1.2, hambre_boca=2.0, aversion=1.0, costo=.002, nobj=4,
              theta=0.6, ema=0.02, paso=0.5, lam=0.05, memoria_rechazo=20, mu_norm=True, div_signo=True,
              eta_s=0.15, clip_s=10.0, puerta=3, mask_rel=2, del_s=0.25, del_c=0.25, ema_c=0.05,
              puerta_pat=5, pat_shuf=0, pat_min=1, desambiguar=1)
# parametros SOLO del mundo 3T-k (sin par en el tronco); sus valores reproducen constantes fijas del tronco:
MUNDO = dict(nkmax=90, wclip=3.0, recic=0, tau_r=0, n_cf=1, early=5000)   # NKMAX=90 y techo 3. del tronco

BRAZOS = {
    'T142':  ('C3',  dict()),
    'N':     ('C3',  dict(norm_lenta=1)),
    'L015':  ('C3',  dict(eta_s=0.015, clip_s=3.0)),
    'N141':  ('C3',  dict(norm_lenta=1, desambiguar=0)),
    'NAZAR': ('C3',  dict(norm_lenta=1, mask_rel=4)),
    'NSH':   ('C3',  dict(norm_lenta=1, mask_rel=0)),
    'NC3C':  ('C3C', dict(norm_lenta=1)),
}
# ---- umbrales del PREREGISTRO (3T-k, sin tocar; T2 uniforme 1.5 para todo k) ----
U = dict(T1_solap=1.0, T1_n=15, T2_sep=1.5, T3_lift=0.15, T4_sep=1.0, T4_lift=0.15, T5_dif=1.0, T5_n=15, PAR_n=14)


def _a(flag, d, f=int):
    return f(sys.argv[sys.argv.index(flag) + 1]) if flag in sys.argv else d


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def kw_de(brazo):
    arm, extra = BRAZOS[brazo]
    kw = dict(TRONCO); kw.update(MUNDO); kw.update(extra)
    return arm, kw


def tarea(args):
    brazo, k, seed, T = args
    import mundo_n7 as m
    arm, kw = kw_de(brazo)
    t0 = time.time()
    r = m.run(seed, arm=arm, kprof=k, T=T, **kw)
    lf = r['lift'][3]
    return dict(brazo=brazo, k=k, seed=seed, sep=r['sep'], lift_q4=(lf if lf is not None else 0.0), lift_q4_none=lf is None,
                lift=r['lift'], solap_A=r['solap_A'], celdas=r['celdas'], splits=r['splits'], n_des=r['n_des'],
                deaths=r['deaths'], mordidas=int(sum(r['nbit'])), nbit=r['nbit'], W=r['W'],
                Wps_sum=r['Wps_sum'], Wns_sum=r['Wns_sum'], seg=round(time.time() - t0, 2))


def med(xs):
    xs = sorted(x for x in xs if x is not None)
    if not xs: return None
    n = len(xs); return xs[n // 2] if n % 2 else 0.5 * (xs[n // 2 - 1] + xs[n // 2])


def identidad_rapida():
    """identidad dentro del runner: mundo_n7 con las dos perillas apagadas == mundo_composicion_v14 (1 semilla,
    C3 y C3C, k=3, T=5000) y kwargs del tronco campo a campo. Si falla, no corre nada."""
    sys.path.insert(0, os.path.join(RAIZ, 'experimentos', 'nivel10_composicion_v14'))
    sys.path.insert(0, os.path.join(RAIZ, 'organismo'))
    import mundo_n7 as m, mundo_composicion_v14 as o, organismo_v142 as V142
    nuevas = {'desambiguar', 'norm_lenta', 'n_des', 'Wps_sum', 'Wns_sum'}
    ok = True
    for arm in ('C3', 'C3C'):
        kw = dict(TRONCO); kw.update(MUNDO); kw.pop('desambiguar')
        a = m.run(3, arm=arm, kprof=3, T=5000, desambiguar=0, norm_lenta=0, **kw)
        b = o.run(3, arm=arm, kprof=3, T=5000, **kw)
        a = json.loads(json.dumps({x: y for x, y in a.items() if x not in nuevas}, default=str))
        b = json.loads(json.dumps(b, default=str))
        ok &= (a == b)
    sig = inspect.signature(V142.run).parameters
    dif = [c for c, v in TRONCO.items() if c not in sig or sig[c].default != v]
    ok &= not dif
    ok &= (V142.NKMAX == MUNDO['nkmax'])
    return ok, dif


def criterios(res, ks, S):
    """veredicto por k y por brazo con la letra del preregistro"""
    V = {}
    by = {}
    for r in res: by.setdefault((r['brazo'], r['k']), {})[r['seed']] = r
    for k in ks:
        Vk = {}
        for b in BRAZOS:
            d = by.get((b, k))
            if not d: continue
            ss = sorted(d)
            sep = med([d[s]['sep'] for s in ss]); lf = med([d[s]['lift_q4'] for s in ss])
            t1 = sum(d[s]['solap_A'] <= U['T1_solap'] for s in ss)
            Vk[b] = dict(n=len(ss), sep=sep, lift_q4=lf, T1_n=t1, celdas=med([d[s]['celdas'] for s in ss]),
                         splits=med([d[s]['splits'] for s in ss]), n_des=med([d[s]['n_des'] for s in ss]),
                         muertes=med([d[s]['deaths'] for s in ss]), mordidas=med([d[s]['mordidas'] for s in ss]),
                         lift_none=sum(d[s]['lift_q4_none'] for s in ss),
                         T1=t1 >= min(U['T1_n'], len(ss)) if len(ss) >= 20 else None,
                         T2=sep is not None and sep >= U['T2_sep'], T3=lf is not None and lf >= U['T3_lift'])
        # T4/T5 del candidato contra su canal falso; pareados contra los controles
        if 'N' in Vk and 'NC3C' in Vk:
            dN, dF = by[('N', k)], by[('NC3C', k)]
            comun = sorted(set(dN) & set(dF))
            Vk['N']['T4'] = bool(Vk['NC3C']['sep'] < U['T4_sep'] and Vk['NC3C']['lift_q4'] < U['T4_lift'])
            Vk['N']['T5_n'] = sum(dN[s]['sep'] - dF[s]['sep'] >= U['T5_dif'] for s in comun)
        for c in ('T142', 'L015', 'N141', 'NAZAR', 'NSH'):
            if 'N' in Vk and c in Vk:
                dN, dC = by[('N', k)], by[(c, k)]
                comun = sorted(set(dN) & set(dC))
                Vk['N'][f'lift_N>{c}'] = sum(dN[s]['lift_q4'] > dC[s]['lift_q4'] for s in comun)
                Vk['N'][f'lift_N<{c}'] = sum(dN[s]['lift_q4'] < dC[s]['lift_q4'] for s in comun)
        for b in Vk:
            v = Vk[b]
            v['compone'] = bool(v['T2'] and v['T3'] and (v['T1'] is not False) and (v.get('T4') is not False)
                                and (v.get('T5_n') is None or v['T5_n'] >= min(U['T5_n'], v['n'])))
        V[k] = Vk
    kmax = {}
    for b in BRAZOS:
        km = 0
        for k in sorted(ks):
            if b in V[k] and V[k][b]['compone']: km = k
            else: break
        kmax[b] = km
    return V, kmax


if __name__ == '__main__':
    HUMO = '--humo' in sys.argv
    T = _a('--T', 100000)
    if HUMO:
        SEEDS = [7799]; KS = [2, 5, 8]; POOL = 1
    else:
        d0 = _a('--desde', 7701); SEEDS = list(range(d0, d0 + _a('--n', 20)))
        KS = [int(x) for x in (sys.argv[sys.argv.index('--ks') + 1] if '--ks' in sys.argv else '1,2,3,4,5,6,7,8').split(',')]
        POOL = _a('--pool', 1)
        if POOL > 6: sys.exit('--pool <= 6 (regla del equipo)')
    brz = sys.argv[sys.argv.index('--brazos') + 1].split(',') if '--brazos' in sys.argv else list(BRAZOS)
    stamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    carpeta = os.path.join(AQUI, 'datos', 'humo' if HUMO else '')
    os.makedirs(carpeta, exist_ok=True)
    nombre = f"n7_{'humo' if HUMO else 'serie'}_s{SEEDS[0]}-{SEEDS[-1]}_T{T}_{stamp}"
    shas = {f: h16(os.path.join(AQUI, f)) for f in ('mundo_n7.py', 'corre_n7.py', 'construye_n7.py', 'identidad_n7.py',
                                                     'organismo_v142N.py', 'organismo_v142gN.py')}
    shas['PREREGISTRO_n7.md'] = h16(os.path.join(AQUI, 'PREREGISTRO_n7.md')) if os.path.exists(os.path.join(AQUI, 'PREREGISTRO_n7.md')) else None
    print(f'N7-NL {nombre}\n  semillas {SEEDS[0]}-{SEEDS[-1]}  k {KS}  T {T}  brazos {brz}  pool {POOL}\n  sha {shas}', flush=True)
    t0 = time.time()
    ok, dif = identidad_rapida()
    print(f'  identidad dentro del runner (mundo_n7 apagado == mundo_composicion_v14; kwargs == organismo_v142): {"OK" if ok else "FALLA " + str(dif)}', flush=True)
    if not ok: sys.exit(1)
    tareas = [(b, k, s, T) for k in KS for b in brz for s in SEEDS]
    res = []
    if POOL == 1:
        for i, a in enumerate(tareas):
            r = tarea(a); res.append(r)
            print(f"  [{time.time()-t0:6.0f}s] {r['brazo']:5s} k={r['k']} s{r['seed']}: sep {r['sep']:+.3f} lift_q4 {r['lift_q4']:.3f}"
                  f"{' (None)' if r['lift_q4_none'] else ''} celdas {r['celdas']} splits {r['splits']} n_des {r['n_des']}"
                  f" muertes {r['deaths']} mordidas {r['mordidas']}", flush=True)
    else:
        from multiprocessing import Pool
        with Pool(POOL) as p:
            for i, r in enumerate(p.imap_unordered(tarea, tareas, chunksize=1)):
                res.append(r)
                if (i + 1) % 20 == 0: print(f'  [{time.time()-t0:6.0f}s] {i+1}/{len(tareas)}', flush=True)
    V, kmax = criterios(res, KS, len(SEEDS))
    print('\n  k  brazo   sep    lift_q4  celdas splits n_des muertes mordidas  compone')
    for k in KS:
        for b in brz:
            v = V[k].get(b)
            if not v: continue
            print(f"  {k}  {b:6s} {v['sep']:+6.2f}  {v['lift_q4']:6.3f}   {v['celdas']:5}  {v['splits']:5}  {v['n_des']:4}  {v['muertes']:6}  {v['mordidas']:7}   {v['compone']}"
                  + (f"  T5 {v.get('T5_n')}" if v.get('T5_n') is not None else ''))
    print(f'\n  K_max por brazo (todos los k <= K componen, letra 3T-k): {kmax}')
    if HUMO: print('  [HUMO: una semilla; los umbrales T1/T5 por conteo no aplican; no es dato]')
    out = dict(bloque='N7-NL', humo=HUMO, semillas=SEEDS, ks=KS, T=T, brazos={b: BRAZOS[b] for b in brz},
               TRONCO=TRONCO, MUNDO=MUNDO, umbrales=U, sha=shas, identidad_runner=ok,
               veredicto_por_k={str(k): V[k] for k in KS}, K_max=kmax, crudos=res, seg=round(time.time() - t0, 1))
    ruta = os.path.join(carpeta, nombre + '.json')
    with open(ruta, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(out, f, ensure_ascii=False, indent=1, default=str)
    print(f'\n  JSON -> {os.path.relpath(ruta, RAIZ)}  sha {h16(ruta)}  ({time.time()-t0:.0f}s)')
