"""Prueba de AHORRO — el coste del arreglo de BUG-01.

Ejecuta PREREGISTRO_ahorro.md (sha ca6638df5682212e). No decide nada que no este escrito alli.

REGLA 10 (nueva, dia 3): todo script de mas de un minuto emite una linea de progreso por etapa con
marca de tiempo, y escribe a archivo DESDE EL ARRANQUE, no solo al final. El log vive en
datos/ahorro_<fecha>.log y se puede seguir con `tail -f` mientras corre.

Aclaracion escrita ANTES de correr (el preregistro no la fijaba): el brazo primario para el criterio
del 50% es **solap_AB=0**, porque es la unica condicion que v6 comparte canonicamente — v6 no tiene el
parametro solap_AB, su solapamiento es 0 siempre. solap_AB=1 se reporta al lado, sin agregarse.

Uso:  python experimentos/bug01/corre_ahorro.py [semillas]
"""
import sys, os, json, time, hashlib, platform, csv
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo')]

T_EXP = 200000
T_ADQ, T_EXT, T_REV = 0, 60000, 120000          # fases: [0,60k) [60k,120k) [120k,200k)
SIN_B = (120000, 160000)                         # ventana sin B del bloque B
CRIT = -2.5                                      # criterio de miedo. NO se toca (regla 3).
UMBRAL_VENDE = 0.50                              # criterio de direccion, literal

BRAZOS = [
    ('v6',         'v6s', dict()),
    ('v7_control', 'v7g', dict(lam=0.0)),
    ('exp2',       'v7g', dict(lam=0.05, piso=0.0)),
    ('total',      'v7g', dict(lam=1.0,  piso=0.0)),
    ('piso_025',   'v7g', dict(lam=1.0,  piso=0.25)),
    ('piso_050',   'v7g', dict(lam=1.0,  piso=0.5)),
    ('piso_100',   'v7g', dict(lam=1.0,  piso=1.0)),
]

# escenarios del control de inercia. v6 no tiene plast/solap_AB, asi que corre los 5 que soporta.
ESC_V7 = {'BUG': dict(plast=False, solap_AB=3), 'E1': dict(), 'E2': dict(invertir_en=50000),
          'E2I': dict(nuevo='C'), 'E2J': dict(nuevo='D', nuevo_val='comida', solap_B=1),
          'E2K': dict(nuevo='D', nuevo_val='comida', solap_B=2), 'E2L': dict(solap_AB=3)}
ESC_V6 = {k: ESC_V7[k] for k in ('E1', 'E2', 'E2I', 'E2J', 'E2K')}

_log = {'f': None, 't0': None}


def log(msg):
    """REGLA 10: marca de tiempo, a pantalla y a archivo, con flush inmediato."""
    dt = time.time() - _log['t0']
    linea = f"[{time.strftime('%H:%M:%S')} +{dt:7.1f}s] {msg}"
    print(linea, flush=True)
    if _log['f']:
        _log['f'].write(linea + "\n")
        _log['f'].flush()
        os.fsync(_log['f'].fileno())


# ---------------------------------------------------------------------------------------------
# tareas para el pool
# ---------------------------------------------------------------------------------------------
def carga(mod):
    import importlib
    return importlib.import_module('organismo_' + mod)


def tarea_ahorro(args):
    brazo, mod, kw, solap, bloque, seed = args
    o = carga(mod)
    extra = dict(kw)
    if mod == 'v7g' and solap:
        extra['solap_AB'] = solap
    if bloque == 'A':
        extra.update(invertir_en=T_EXT, revertir_en=T_REV)
    else:
        extra.update(invertir_en=T_EXT, sin_B=SIN_B)
    r = o.run(seed, T=T_EXP, crit_miedo=CRIT, **extra)
    fila = dict(brazo=brazo, mod=mod, bloque=bloque, solap_AB=solap, seed=seed,
                lam=kw.get('lam'), piso=kw.get('piso'),
                n1=r['n1'], n3=r['n3'], nB=r['nB'], nB3=r['nB3'],
                wB_ext=r['wB_ext'], wB_pre=r['wB_pre'], wB_post=r['wB_post'],
                W_A=r['W']['A'], W_B=r['W']['B'],
                Wp_B=r['comp']['B'][0], Wn_B=r['comp']['B'][1],
                deaths=r['deaths'], splits=r.get('splits'), celdas=r.get('celdas'))
    techo = 9.0 if mod == 'v7g' else 3.0
    fila['techo_B'] = int(fila['Wp_B'] >= techo or fila['Wn_B'] >= techo)
    return fila


def tarea_control(args):
    """Control 1: la variante con parametros neutros debe ser bit-identica al original."""
    cual, esc, seed = args
    if cual == 'v6':
        import organismo_v6 as base, organismo_v6s as var
        kw = ESC_V6[esc]
        a, b = base.run(seed, **kw), var.run(seed, **kw)
    else:
        import organismo_v7 as base, organismo_v7g as var
        kw = ESC_V7[esc]
        a, b = base.run(seed, **kw), var.run(seed, lam=0.0, **kw)
    dif = [k for k in a if a[k] != b[k]]          # solo claves compartidas; la variante anade mas
    return dict(cual=cual, esc=esc, seed=seed, identico=not dif, difieren=dif)


# ---------------------------------------------------------------------------------------------
med = lambda xs: (float(np.median(xs)), float(np.min(xs)), float(np.max(xs))) if xs else (None, None, None)
fmt = lambda t: "sin datos" if t[0] is None else f"{t[0]:+.3f} [{t[1]:+.3f}, {t[2]:+.3f}]"


def ahorros(filas):
    """Ahorro por semilla = (n1-n3)/n1, solo donde ambos estan definidos (censura explicita)."""
    vals, cens = [], 0
    for f in filas:
        if f['n1'] and f['n3'] is not None and f['n1'] > 0:
            vals.append((f['n1'] - f['n3']) / f['n1'])
        else:
            cens += 1
    return vals, cens


if __name__ == '__main__':
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    S = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    seeds = list(range(1, S + 1))
    stamp = time.strftime('%Y%m%d_%H%M%S')

    _log['t0'] = time.time()
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'ahorro_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    NUC = min(16, os.cpu_count())
    log(f"ARRANQUE. prueba de ahorro, {S} semillas, T={T_EXP}, {NUC} nucleos.")
    log(f"log -> datos/ahorro_{stamp}.log   (regla 10: se escribe desde ya, no al final)")

    with mp.Pool(NUC) as pool:
        # ---------- CONTROL 1 ----------
        trabajos = ([('v6', e, s) for e in ESC_V6 for s in range(1, 7)]
                    + [('v7', e, s) for e in ESC_V7 for s in range(1, 7)])
        log(f"ETAPA 1/4 — control de inercia de las variantes ({len(trabajos)} comparaciones)...")
        ctrl = []
        for i, r in enumerate(pool.imap_unordered(tarea_control, trabajos, chunksize=2), 1):
            ctrl.append(r)
            if i % 20 == 0 or i == len(trabajos):
                log(f"          control {i}/{len(trabajos)}  ({sum(c['identico'] for c in ctrl)} identicos)")
        for c in ctrl:
            if not c['identico']:
                log(f"  DIFIERE {c['cual']} {c['esc']} semilla {c['seed']}: {c['difieren']}")
        n6 = [c for c in ctrl if c['cual'] == 'v6']
        n7 = [c for c in ctrl if c['cual'] == 'v7']
        c6 = all(c['identico'] for c in n6)
        c7 = all(c['identico'] for c in n7)
        log(f"  v6s vs v6: {sum(c['identico'] for c in n6)}/{len(n6)} -> {'OK' if c6 else 'FALLA'}")
        log(f"  v7g vs v7: {sum(c['identico'] for c in n7)}/{len(n7)} -> {'OK' if c7 else 'FALLA'}")
        if not (c6 and c7):
            log("*** CONTROL 1 FALLIDO. Las variantes no son el mismo organismo. No se corre nada mas.")
            sys.exit(1)

        # ---------- BLOQUES A y B ----------
        trabajos = []
        for brazo, mod, kw in BRAZOS:
            solaps_A = [0] if mod == 'v6s' else [0, 1]
            solaps_B = [0] if mod == 'v6s' else [0, 1, 2]
            trabajos += [(brazo, mod, kw, sp, 'A', s) for sp in solaps_A for s in seeds]
            trabajos += [(brazo, mod, kw, sp, 'B', s) for sp in solaps_B for s in seeds]
        nA = sum(1 for t in trabajos if t[4] == 'A')
        log(f"ETAPA 2/4 — corridas: bloque A (ahorro) {nA}, bloque B (recuperacion) "
            f"{len(trabajos)-nA}, total {len(trabajos)} a T={T_EXP}...")
        res = []
        for i, r in enumerate(pool.imap_unordered(tarea_ahorro, trabajos, chunksize=1), 1):
            res.append(r)
            if i % 40 == 0 or i == len(trabajos):
                log(f"          corrida {i}/{len(trabajos)}  ({100*i/len(trabajos):.0f}%)")

    log("ETAPA 3/4 — analisis.")
    F = lambda b, bl, sp: [r for r in res if r['brazo'] == b and r['bloque'] == bl and r['solap_AB'] == sp]

    # ---------- A1..A4 ----------
    log("")
    log("=" * 88)
    log("BLOQUE A — AHORRO.  Ahorro = (n1-n3)/n1 en mordidas de B.  primario: solap_AB=0")
    log("=" * 88)
    tabla = {}
    for sp in (0, 1):
        log(f"  --- solap_AB={sp} ---")
        log(f"  {'brazo':12s} {'n1 mediana':>11s} {'n3 mediana':>11s} {'ahorro':>22s} {'censuradas':>11s}")
        for brazo, mod, kw in BRAZOS:
            fl = F(brazo, 'A', sp)
            if not fl:
                continue
            v, cens = ahorros(fl)
            tabla[(brazo, sp)] = (med(v)[0], cens, len(v))
            n1s = [f['n1'] for f in fl if f['n1']]
            n3s = [f['n3'] for f in fl if f['n3'] is not None]
            log(f"  {brazo:12s} {(med(n1s)[0] or -1):11.0f} {(med(n3s)[0] or -1):11.0f} "
                f"{fmt(med(v)):>22s} {cens:8d}/{S}")

    a_v6 = tabla.get(('v6', 0), (None,))[0]
    A1 = a_v6 is not None and a_v6 > 0
    log("")
    log(f"  A1 (control del instrumento: Ahorro(v6) > 0): "
        f"{'SOSTENIDA' if A1 else 'REFUTADA'}  -> {a_v6}")
    if not A1:
        log("  *** A1 refutada: la prueba no mide ahorro. NO se lee ningun otro brazo (preregistro sec.4).")

    vende = {}
    if A1:
        log(f"  criterio de direccion: VENDE_MEMORIA(b) si Ahorro(b) < {UMBRAL_VENDE} * {a_v6:.4f} "
            f"= {UMBRAL_VENDE*a_v6:.4f}")
        for brazo, mod, kw in BRAZOS:
            if brazo == 'v6':
                continue
            a = tabla.get((brazo, 0), (None,))[0]
            vende[brazo] = (a is not None and a < UMBRAL_VENDE * a_v6)
            log(f"    {brazo:12s} ahorro={a if a is None else round(a,4)}  "
                f"VENDE_MEMORIA={vende[brazo]}")
        A2 = vende.get('total') is True
        A3 = vende.get('exp2') is False
        orden = [tabla.get((b, 0), (None,))[0] for b in ('total', 'piso_025', 'piso_050', 'piso_100')]
        A4 = all(x is not None for x in orden) and all(orden[i] <= orden[i+1] + 1e-12 for i in range(3))
        log("")
        log(f"  A2 (total VENDE memoria):        {'SOSTENIDA' if A2 else 'REFUTADA'}")
        log(f"  A3 (exp2 NO vende memoria):      {'SOSTENIDA' if A3 else 'REFUTADA'}   <-- decide el paso 1")
        log(f"  A4 (ahorro crece con el piso):   {'SOSTENIDA' if A4 else 'REFUTADA'}   orden={[None if o is None else round(o,4) for o in orden]}")
    else:
        A2 = A3 = A4 = None

    # ---------- A5, A6 ----------
    log("")
    log("=" * 88)
    log("BLOQUE B — RECUPERACION ESPONTANEA.  delta = wB_post - wB_pre  (negativo = el miedo vuelve)")
    log("=" * 88)
    A5 = True
    for sp in (0, 1, 2):
        log(f"  --- solap_AB={sp} ---")
        for brazo, mod, kw in BRAZOS:
            fl = F(brazo, 'B', sp)
            if not fl:
                continue
            d = [f['wB_post'] - f['wB_pre'] for f in fl
                 if f['wB_post'] is not None and f['wB_pre'] is not None]
            neg = sum(1 for x in d if x < 0)
            exacto0 = all(x == 0.0 for x in d) if d else False
            if sp == 0:
                A5 &= exacto0
            log(f"  {brazo:12s} delta {fmt(med(d)):>22s}  vuelve el miedo: {neg}/{len(d)}"
                + ("   exacto 0.000: " + ("SI" if exacto0 else "NO <- ROMPE EL CONTROL") if sp == 0 else ""))
    log("")
    log(f"  A5 (control negativo: con solap_AB=0 delta es 0.000 exacto): "
        f"{'SOSTENIDA' if A5 else 'REFUTADA'}")
    log("  A6 es direccional y sin cifra preregistrada: se reporta arriba, no se vota.")

    # ---------- salida ----------
    log("ETAPA 4/4 — escritura de datos.")
    h = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
    cols = ['brazo', 'mod', 'bloque', 'solap_AB', 'lam', 'piso', 'seed', 'n1', 'n3', 'nB', 'nB3',
            'wB_ext', 'wB_pre', 'wB_post', 'W_A', 'W_B', 'Wp_B', 'Wn_B', 'techo_B', 'splits',
            'celdas', 'deaths']
    dcsv = os.path.join(RAIZ, 'datos', f'ahorro_{stamp}.csv')
    with open(dcsv, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction='ignore')
        w.writeheader()
        for r in sorted(res, key=lambda r: (r['bloque'], r['brazo'], r['solap_AB'], r['seed'])):
            w.writerow({k: ('' if r.get(k) is None else r.get(k)) for k in cols})

    meta = dict(experimento='BUG01_prueba_ahorro', fecha=time.strftime('%Y-%m-%dT%H:%M:%S'),
                T=T_EXP, fases=dict(adquisicion=[T_ADQ, T_EXT], extincion=[T_EXT, T_REV],
                                    reaprendizaje=[T_REV, T_EXP]), sin_B=list(SIN_B),
                crit_miedo=CRIT, umbral_vende=UMBRAL_VENDE, n_semillas=S,
                brazo_primario='solap_AB=0',
                sha_organismo_v6=h(os.path.join(RAIZ, 'organismo', 'organismo_v6.py')),
                sha_organismo_v6s=h(os.path.join(AQUI, 'organismo_v6s.py')),
                sha_organismo_v7=h(os.path.join(RAIZ, 'organismo', 'organismo_v7.py')),
                sha_organismo_v7e=h(os.path.join(AQUI, 'organismo_v7e.py')),
                sha_organismo_v7g=h(os.path.join(AQUI, 'organismo_v7g.py')),
                sha_constructor=h(os.path.join(AQUI, 'construye_ahorro.py')),
                sha_script=h(os.path.abspath(__file__)),
                sha_preregistro=h(os.path.join(AQUI, 'PREREGISTRO_ahorro.md')),
                python=platform.python_version(), numpy=np.__version__, plataforma=platform.platform(),
                veredictos=dict(A1=A1, A2=A2, A3=A3, A4=A4, A5=bool(A5)))
    djson = os.path.join(RAIZ, 'datos', f'ahorro_{stamp}.json')
    json.dump(dict(meta=meta, control_inercia=ctrl, corridas=res),
              open(djson, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    log(f"datos -> {os.path.basename(djson)}  sha256_16 = {h(djson)}")
    log(f"         {os.path.basename(dcsv)}  sha256_16 = {h(dcsv)}")
    log("")
    log(f"VEREDICTO ahorro: A1={A1} A2={A2} A3={A3} A4={A4} A5={A5}")
    log("Pega en el registro la linea con: fecha, veredictos y hashes de arriba (regla 7).")
    _log['f'].close()
