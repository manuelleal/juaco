"""bateria_v13E = organismo/bateria_v13.py (1a027bcb37eb536e, CONGELADO: solo se leyo) apuntando a
organismo_v13E (organismo_v13p + dE-TEST fijo ON) en vez de organismo_v13. Las SEIS etapas, los CRIT
importados y los umbrales del criterio v3' quedan INTACTOS. Salida en datos/examen_v13E_<fecha>.
ERR-30: el CRITERIO 5 esta ADAPTADO (v3'' para organos en la boca, precedente ERR-21): la reduccion a
v11/v10 apaga TAMBIEN k_testE y eta_pred (si no, un organo que actua en la boca sin pasar por eta_s/
puerta nunca podria pasar el criterio 5, y no mide nada). Ver PREREGISTRO_v13E.md.
Generado por construye_v13E.py. NO editar. La bateria original NO se modifico."""
"""Batería de v13 — examen de congelación (CRITERIO v3, sin cambiar un umbral) y, una vez congelado, regresión del tronco.

    python bateria_v13.py [semillas] [--desde N] [--log]        (desde organismo/)
    --desde N  primera semilla (por defecto 1); el confirmatorio de v13 usa --desde 81
    --log  escribe datos/examen_v13_<fecha>.log y .json (regla 10: log desde el arranque)

Preregistro: experimentos/v13_dos_vias/PREREGISTRO_tronco_v13.md.
Criterio v3': el v3 (experimentos/congelacion_v8/PREREGISTRO_congelacion_v8.md, d2924e69128fe0f6) con el criterio 3
desdoblado (PREREGISTRO_tronco_v13.md, ENMIENDA 1, ERR-21).

  5. Identidad de instrumentos (primero; si falla, no se corre el examen):
       v13(eta_s=0, puerta=None) == v11 en claves de v11, y v13(eta_s=0, puerta=None, div_signo=False) == v10;
       7 escenarios x semillas 1..6 cada una.
  1. Criterios científicos heredados de v6/v7, 20/20 en E1, E2, E2I, E2J, E2K, E2L.
  2. celdas <= 45 en las seis etapas y en E2I-misma.
  3. (v3', ERR-21) 3': A∩B=3 sin plasticidad y SIN via lenta (eta_s=0, puerta=None), <=1/20 pasa E2L;
     3'': A∩B=3 sin plasticidad CON via lenta, >=19/20 pasa E2L (la lenta separa por pixeles).
  4a'. [IDENTIDAD, NO EVIDENCIA] cada division activa exactamente una celda: celdas == 30 + splits y
       len(split_t) == splits, con celdas<90. (La 4a de v8-v10, splits<=>err_max>0.6, era una identidad de la
       regla err>theta, que v11 ya no usa; se sustituye por la identidad de contabilidad, declarado en el
       preregistro antes de correr.) Si falla: instrumento roto.
  4b. Sin conflicto no hay división: toda corrida que divide tuvo t_conflicto <= primera división.
      Guarda: t_conflicto nulo en E1 20/20 y no nulo en E2L 20/20; si no, 4b no se cumple.
  4c. E2I-misma (C veneno con C∩B=3): splits==0 y W_C<=-2.5, 20/20.
      Guarda: solap nB==3 y mordidas de C en Q3+Q4 > 0, 20/20; si no, 4c no se cumple.
  4d. Disparo anclado a la causa: E1 sin divisiones; E2/E2I/E2J/E2K divisiones sólo en t>=50.000;
      E2L divide y termina antes de t=25.000.
  6. (fuera de esta batería) organismo/bateria_v9.py 6 PASA y manifiesto.py --check.
"""
import sys, os, time, json, hashlib, platform
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

_D = os.path.dirname(os.path.abspath(__file__))   # esta copia vive fuera de organismo/
AQUI = os.path.join(os.path.dirname(os.path.dirname(_D)), 'organismo')
RAIZ = os.path.dirname(AQUI)
sys.path[:0] = [_D, AQUI, os.path.join(RAIZ, 'experimentos', 'bug01')]
EVENTO = 50000
N_PARALELO = 14

ETAPAS = {
    'E1':        dict(),
    'E2':        dict(invertir_en=EVENTO),
    'E2I':       dict(nuevo='C'),
    'E2J':       dict(nuevo='D', nuevo_val='comida', solap_B=1),
    'E2K':       dict(nuevo='D', nuevo_val='comida', solap_B=2),
    'E2L':       dict(solap_AB=3),
    'CTRL':      dict(solap_AB=3, plast=False, eta_s=0.0, puerta=None),   # v3' 3': la via rapida sola (= control de v11) debe FALLAR
    'CTRL2':     dict(solap_AB=3, plast=False),                         # v3' 3'': la via lenta activa separa por pixeles
    'E2I-misma': dict(nuevo='C', solap_B=3),
}
SEIS = ['E1', 'E2', 'E2I', 'E2J', 'E2K', 'E2L']
ESC_ID = {'BUG': dict(plast=False, solap_AB=3), 'E1': dict(), 'E2': dict(invertir_en=50000),
          'E2I': dict(nuevo='C'), 'E2J': dict(nuevo='D', nuevo_val='comida', solap_B=1),
          'E2K': dict(nuevo='D', nuevo_val='comida', solap_B=2), 'E2L': dict(solap_AB=3)}

tasa = lambda r, k, i: 100 * r['mord'][k][i] / max(r['vis'][k][i], 1)
CRIT = {
    'E1':  {"venenoQ4<Q1": lambda r: r['mord']['B'][3] < r['mord']['B'][0],
            "W_A≈+1": lambda r: abs(r['W']['A'] - 1) < .15, "W_B≈-3": lambda r: abs(r['W']['B'] + 3) < .3},
    'E2':  {"W_A→-3": lambda r: abs(r['W']['A'] + 3) < .3, "W_B→+1": lambda r: abs(r['W']['B'] - 1) < .15,
            "come B Q4≥50": lambda r: r['mord']['B'][3] >= 50},
    'E2I': {"W_C≤-2.5": lambda r: r['W']['C'] <= -2.5, "W_A≈+1": lambda r: abs(r['W']['A'] - 1) < .15,
            "W_B≤-2.8": lambda r: r['W']['B'] <= -2.8, "tasaA Q4≥80%Q2": lambda r: tasa(r, 'A', 3) >= .8 * tasa(r, 'A', 1)},
    'E2J': {"W_D≥0.85": lambda r: r['W']['D'] >= .85, "W_B≤-2.7": lambda r: r['W']['B'] <= -2.7},
    'E2K': {"W_D≥0.8": lambda r: r['W']['D'] >= .8, "W_B≤-2.4": lambda r: r['W']['B'] <= -2.4},
    'E2L': {"W_A≈+1": lambda r: abs(r['W']['A'] - 1) < .15, "W_B≈-3": lambda r: abs(r['W']['B'] + 3) < .3,
            "solap→0": lambda r: r['solap']['AB'] == 0},
}

_log = {'f': None, 't0': time.time()}


def log(msg=""):
    linea = f"[{time.strftime('%H:%M:%S')} +{time.time()-_log['t0']:6.1f}s] {msg}"
    print(linea, flush=True)
    if _log['f']:
        _log['f'].write(linea + "\n"); _log['f'].flush(); os.fsync(_log['f'].fileno())


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def tarea_id(args):
    cual, esc, seed = args
    import organismo_v13E as v13   # dE-TEST (sorpresa del mundo en la boca) FIJO ON
    if cual == 'v11':
        import organismo_v11 as ref
        a, b = ref.run(seed, **ESC_ID[esc]), v13.run(seed, eta_s=0.0, puerta=None, k_testE=0.0, eta_pred=0.0, **ESC_ID[esc])   # ERR-30: v3'' (organos en la boca)
    else:
        import organismo_v10 as ref
        a, b = ref.run(seed, **ESC_ID[esc]), v13.run(seed, eta_s=0.0, puerta=None, div_signo=False, k_testE=0.0, eta_pred=0.0, **ESC_ID[esc])   # ERR-30: v3'' (organos en la boca)
    dif = [k for k in a if a[k] != b[k]]
    return dict(cual=cual, esc=esc, seed=seed, identico=not dif, difieren=dif)


def tarea(args):
    etapa, seed = args
    import organismo_v13E as v13   # dE-TEST (sorpresa del mundo en la boca) FIJO ON
    r = v13.run(seed, **ETAPAS[etapa])
    return dict(etapa=etapa, seed=seed, W=r['W'], comp=r['comp'], mord=r['mord'], vis=r['vis'], deaths=r['deaths'],
                splits=r['splits'], split_t=r['split_t'], celdas=r['celdas'], solap=r['solap'],
                err_max=round(r['err_max'], 6), t_conflicto=r['t_conflicto'], t_techo=r['t_techo'], n_techo=r['n_techo'])


if __name__ == '__main__':
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    desde = 1
    if '--desde' in sys.argv:
        desde = int(sys.argv[sys.argv.index('--desde') + 1])
    argv = [a for i, a in enumerate(sys.argv[1:], 1) if a not in ('--log', '--desde') and sys.argv[i - 1] != '--desde']
    S = int(argv[0]) if argv else 6
    seeds = list(range(desde, desde + S))
    stamp = time.strftime('%Y%m%d_%H%M%S')
    if '--log' in sys.argv:
        _log['f'] = open(os.path.join(RAIZ, 'datos', f'examen_v13E_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    prereg = os.path.join(RAIZ, 'experimentos', 'v13_dos_vias', 'PREREGISTRO_tronco_v13.md')
    log(f"=== Batería v13 — CRITERIO v3, {S} semillas ({seeds[0]}..{seeds[-1]}), Pool({N_PARALELO}) ===")
    log(f"sha organismo_v13 {h16(os.path.join(_D, 'organismo_v13E.py'))}  bateria_v13 {h16(os.path.abspath(__file__))}"
        f"  preregistro {h16(prereg)}")
    V = {}

    with mp.Pool(N_PARALELO) as pool:
        # ---------- 5. identidad ----------
        trabajos = [(c, e, s) for c in ('v11', 'v10') for e in ESC_ID for s in range(1, 7)]
        log(f"ETAPA 1/3 — criterio 5, identidad de instrumentos ({len(trabajos)} comparaciones)...")
        ids = []
        for i, r in enumerate(pool.imap_unordered(tarea_id, trabajos, chunksize=1), 1):
            ids.append(r)
            if i % 21 == 0 or i == len(trabajos):
                log(f"          {i}/{len(trabajos)}  ({sum(x['identico'] for x in ids)} idénticas)")
        for c, nombre in (('v11', "v13E(eta_s=0,puerta=None,k_testE=0,eta_pred=0) == v11  [v3'' ERR-30]"), ('v10', "v13E(eta_s=0,puerta=None,div_signo=False,k_testE=0,eta_pred=0) == v10  [v3'' ERR-30]")):
            g = [x for x in ids if x['cual'] == c]
            log(f"  {nombre:22s}: {sum(x['identico'] for x in g)}/{len(g)}")
            for x in g:
                if not x['identico']:
                    log(f"      DIFIERE {x['esc']} semilla {x['seed']}: {x['difieren']}")
        V['5_identidad'] = all(x['identico'] for x in ids)
        if not V['5_identidad']:
            log("*** CRITERIO 5 FALLIDO: v13 no es el organismo que dice ser. No se corre el examen.")
            sys.exit(1)

        # ---------- corridas ----------
        trabajos = [(e, s) for e in ETAPAS for s in seeds]
        log(f"ETAPA 2/3 — {len(trabajos)} corridas ({len(ETAPAS)} etapas x {S} semillas)...")
        res = []
        for i, r in enumerate(pool.imap_unordered(tarea, trabajos, chunksize=1), 1):
            res.append(r)
            if i % 40 == 0 or i == len(trabajos):
                log(f"          {i}/{len(trabajos)}")
    R = {e: sorted([r for r in res if r['etapa'] == e], key=lambda r: r['seed']) for e in ETAPAS}

    log("ETAPA 3/3 — criterios.")
    log()
    # ---------- 1 y 2 ----------
    ok1 = True
    for e in SEIS:
        det = " ".join(f"{n}:{sum(c(r) for r in R[e])}/{S}" for n, c in CRIT[e].items())
        todas = sum(all(c(r) for c in CRIT[e].values()) for r in R[e])
        ok1 &= todas == S
        log(f"  {'PASA' if todas == S else 'FALLA':5s} 1 {e:9s} {todas}/{S}  [{det}]")
        log(f"        splits={[r['splits'] for r in R[e]]}  celdas_max={max(r['celdas'] for r in R[e])}"
            f"  techo={sum(r['t_techo'] is not None for r in R[e])}/{S}")
    V['1_cientificos'] = ok1
    c2 = {e: sum(r['celdas'] <= 45 for r in R[e]) for e in SEIS + ['E2I-misma']}
    V['2_celdas'] = all(v == S for v in c2.values())
    log(f"  {'PASA' if V['2_celdas'] else 'FALLA':5s} 2 celdas<=45: {c2}")

    # ---------- 3 ----------
    pasan = sum(abs(r['W']['A'] - 1) < .15 and abs(r['W']['B'] + 3) < .3 for r in R['CTRL'])
    pasan2 = sum(abs(r['W']['A'] - 1) < .15 and abs(r['W']['B'] + 3) < .3 for r in R['CTRL2'])
    V['3_control'] = pasan <= 1 and pasan2 >= S - 1   # v3' (ERR-21): 3' y 3''
    log(f"  {'PASA' if pasan <= 1 else 'FALLA':5s} 3' via rapida sola sin plasticidad (A∩B=3): {pasan}/{S} lo pasan (<=1)"
        f"  W_A={sorted(set(r['W']['A'] for r in R['CTRL']))[:4]}")
    log(f"  {'PASA' if pasan2 >= S - 1 else 'FALLA':5s} 3'' via lenta activa sin plasticidad (A∩B=3): {pasan2}/{S} lo pasan (>={S-1})")

    # ---------- 4a ----------
    con_plast = [r for e in ETAPAS if e != 'CTRL' for r in R[e] if r['celdas'] < 90]
    disc = [(r['etapa'], r['seed'], r['splits'], r['celdas'], len(r['split_t'])) for r in con_plast
            if r['celdas'] != 30 + r['splits'] or len(r['split_t']) != r['splits']]
    V['4a_identidad'] = not disc
    log(f"  {'OK' if not disc else 'ROTO':5s} 4a' [identidad, NO evidencia] celdas==30+splits y len(split_t)==splits: "
        f"{len(con_plast)-len(disc)}/{len(con_plast)}  {disc[:5]}")
    if disc:
        log("*** 4a' FALLIDA: la instrumentación está rota. Se para; no se lee nada más.")

    # ---------- 4b ----------
    g_neg = sum(r['t_conflicto'] is None for r in R['E1'])
    g_pos = sum(r['t_conflicto'] is not None for r in R['E2L'])
    guarda_b = g_neg == S and g_pos == S
    dividen = [r for e in SEIS + ['E2I-misma'] for r in R[e] if r['splits'] > 0]
    viol_b = [(r['etapa'], r['seed'], r['t_conflicto'], r['split_t'][0][0]) for r in dividen
              if r['t_conflicto'] is None or r['t_conflicto'] > r['split_t'][0][0]]
    V['4b_sin_conflicto_no_divide'] = guarda_b and not viol_b
    log(f"  {'PASA' if V['4b_sin_conflicto_no_divide'] else 'FALLA':5s} 4b sin conflicto no hay división: "
        f"guarda E1 sin conflicto {g_neg}/{S}, E2L con conflicto {g_pos}/{S}; "
        f"corridas que dividen {len(dividen)}, violaciones {viol_b[:5] or 'ninguna'}")

    # ---------- 4c ----------
    M = R['E2I-misma']
    g_c = sum(r['solap']['nB'] == 3 and (r['mord']['C'][2] + r['mord']['C'][3]) > 0 for r in M)
    s0 = sum(r['splits'] == 0 for r in M); wc = sum(r['W']['C'] <= -2.5 for r in M)
    V['4c_misma_valencia'] = g_c == S and s0 == S and wc == S
    log(f"  {'PASA' if V['4c_misma_valencia'] else 'FALLA':5s} 4c C∩B=3 misma valencia: guarda {g_c}/{S}, "
        f"splits==0 {s0}/{S}, W_C<=-2.5 {wc}/{S}  (W_C mediana {np.median([r['W']['C'] for r in M]):+.2f}, "
        f"mordidas de C Q3+Q4 mediana {np.median([r['mord']['C'][2]+r['mord']['C'][3] for r in M]):.0f})")

    # ---------- 4d ----------
    d_e1 = sum(r['splits'] == 0 for r in R['E1'])
    d_ev = {e: sum(all(t >= EVENTO for t, _ in r['split_t']) for r in R[e]) for e in ('E2', 'E2I', 'E2J', 'E2K')}
    d_l = sum(r['splits'] > 0 and max(t for t, _ in r['split_t']) < 25000 for r in R['E2L'])
    V['4d_causa'] = d_e1 == S and all(v == S for v in d_ev.values()) and d_l == S
    log(f"  {'PASA' if V['4d_causa'] else 'FALLA':5s} 4d disparo anclado a la causa: E1 sin divisiones {d_e1}/{S}; "
        f"t>=50k {d_ev}; E2L termina <25k {d_l}/{S}")

    log()
    decisivos = ['5_identidad', '1_cientificos', '2_celdas', '3_control', '4a_identidad',
                 '4b_sin_conflicto_no_divide', '4c_misma_valencia', '4d_causa']
    todo = all(V[k] for k in decisivos)
    log("VEREDICTO bateria_v13: " + " ".join(f"{k}={V[k]}" for k in decisivos))
    if todo and S >= 20:
        log("*** v13 CUMPLE EL CRITERIO v3 con 20 semillas. Por el preregistro: CONGELAR v13 como tronco (si pasa tambien X2 y X3).")
    elif todo:
        log(f"*** v13 cumple el criterio v3 con {S} semillas. Congelar sólo con S>=20.")
    else:
        log("*** v13 NO cumple el criterio v3. No se congela; v11 sigue siendo el tronco. No recalibrar (regla 3).")

    if _log['f']:
        dj = os.path.join(RAIZ, 'datos', f'examen_v13E_{stamp}.json')
        meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), semillas=S, semilla_inicial=seeds[0], veredictos=V, congelar=bool(todo and S >= 20),
                    sha_organismo_v13=h16(os.path.join(_D, 'organismo_v13E.py')), sha_bateria_v13=h16(os.path.abspath(__file__)),
                    sha_preregistro=h16(prereg), sha_organismo_v11=h16(os.path.join(AQUI, 'organismo_v11.py')), sha_organismo_v10=h16(os.path.join(AQUI, 'organismo_v10.py')),
                    sha_criterio_v3=h16(os.path.join(RAIZ, 'experimentos', 'congelacion_v8', 'PREREGISTRO_congelacion_v8.md')),
                    python=platform.python_version(), numpy=np.__version__, plataforma=platform.platform())
        json.dump(dict(meta=meta, identidad=ids, corridas=res), open(dj, 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=1, default=str)
        log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
        _log['f'].close()
