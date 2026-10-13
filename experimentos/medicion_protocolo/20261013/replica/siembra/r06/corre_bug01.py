"""BUG-01 experimento 1: decaimiento local en Wp/Wn.  Ejecuta el preregistro de PREREGISTRO.md.

No decide nada que no esté escrito allí. Evalúa P1 (desbloqueo), P2 (no regresión), P3 (precisión del
valor contra el equilibrio analítico) y P4 (ley de disparo). El barrido de lambda es descriptivo y NO
decide (declarado de antemano).

Uso:  python corre_bug01.py [semillas]      (por defecto 20)
"""
import sys, os, json, time, hashlib, platform
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo')]

LAM = 0.001          # fijado a priori: equilibrio dentro del 1.1% de R. Ver PREREGISTRO seccion 2.
SENS = [0.0003, 0.003, 0.01]   # descriptivo, NO decide
ETA = 0.03
EQ = lambda R, lam: 3 * ETA * R / (3 * ETA + lam)   # equilibrio analitico

ESCENARIOS = {
    'BUG':  dict(plast=False, solap_AB=3),      # el escenario del bug
    'E1':   dict(),
    'E2':   dict(invertir_en=50000),
    'E2I':  dict(nuevo='C'),
    'E2J':  dict(nuevo='D', nuevo_val='comida', solap_B=1),
    'E2K':  dict(nuevo='D', nuevo_val='comida', solap_B=2),
    'E2L':  dict(solap_AB=3),
}


def tarea(args):
    esc, lam, seed = args
    import organismo_v7d as o
    r = o.run(seed, lam=lam, **ESCENARIOS[esc])
    return dict(esc=esc, lam=lam, seed=seed, W=r['W'], comp=r['comp'], deaths=r['deaths'],
                splits=r['splits'], split_t=r['split_t'], celdas=r['celdas'], solap=r['solap'],
                mord={k: list(v) for k, v in r['mord'].items()},
                vis={k: list(v) for k, v in r['vis'].items()})


def med(xs):
    return (float(np.median(xs)), float(np.min(xs)), float(np.max(xs)))


def fmt(t):
    return f"{t[0]:+.3f} [{t[1]:+.3f}, {t[2]:+.3f}]"


if __name__ == '__main__':
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    S = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    seeds = list(range(1, S + 1))
    t0 = time.time()

    trabajos = []
    for esc in ESCENARIOS:
        for lam in (0.0, LAM):
            trabajos += [(esc, lam, s) for s in seeds]
    for lam in SENS:                                  # sensibilidad solo en BUG y E1
        for esc in ('BUG', 'E1'):
            trabajos += [(esc, lam, s) for s in seeds]

    print(f"BUG-01 exp.1 — decaimiento local. {len(trabajos)} corridas, {S} semillas, "
          f"lambda primario={LAM}\n")
    with mp.Pool(min(16, os.cpu_count())) as pool:
        res = pool.map(tarea, trabajos)
    print(f"({time.time()-t0:.0f} s de pared)\n")

    R = lambda esc, lam: [r for r in res if r['esc'] == esc and r['lam'] == lam]

    # ---------------- P1 desbloqueo ----------------
    print("=" * 78)
    print("P1 — DESBLOQUEO (criterio primario). Escenario del bug: plast=False, solap_AB=3")
    print("=" * 78)
    for lam in (0.0, LAM):
        rs = R('BUG', lam)
        wpA = [r['comp']['A'][0] for r in rs]; wnA = [r['comp']['A'][1] for r in rs]
        wA = [r['W']['A'] for r in rs]
        bajo = sum(p < 9.0 and n < 9.0 for p, n in zip(wpA, wnA))
        enrango = sum(-1.5 <= w <= -0.5 for w in wA)
        print(f"  lam={lam:<7} Wp={fmt(med(wpA))}  Wn={fmt(med(wnA))}  W_A={fmt(med(wA))}")
        print(f"  {'':12} canales por debajo del techo: {bajo}/{S}    W en [-1.5,-0.5]: {enrango}/{S}")
    rs = R('BUG', LAM)
    p1a = sum(r['comp']['A'][0] < 9.0 and r['comp']['A'][1] < 9.0 for r in rs) == S
    p1b = sum(-1.5 <= r['W']['A'] <= -0.5 for r in rs) >= 18
    print(f"\n  P1 -> {'SOSTENIDA' if (p1a and p1b) else 'REFUTADA'}"
          f"   (canales bajo techo 20/20: {p1a} | W en rango >=18/20: {p1b})")

    # ---------------- P2 no regresion ----------------
    print("\n" + "=" * 78)
    print("P2 — NO REGRESION. Criterios de la bateria, con el decaimiento activo")
    print("=" * 78)
    tasa = lambda r, k, i: 100 * r['mord'][k][i] / max(r['vis'][k][i], 1)
    CRIT = {
        'E1':  {"venenoQ4<Q1": lambda r: r['mord']['B'][3] < r['mord']['B'][0],
                "W_A~+1": lambda r: abs(r['W']['A'] - 1) < .15, "W_B~-3": lambda r: abs(r['W']['B'] + 3) < .3},
        'E2':  {"W_A->-3": lambda r: abs(r['W']['A'] + 3) < .3, "W_B->+1": lambda r: abs(r['W']['B'] - 1) < .15,
                "comeB_Q4>=50": lambda r: r['mord']['B'][3] >= 50},
        'E2I': {"W_C<=-2.5": lambda r: r['W']['C'] <= -2.5, "W_A~+1": lambda r: abs(r['W']['A'] - 1) < .15,
                "W_B<=-2.8": lambda r: r['W']['B'] <= -2.8,
                "tasaA_Q4>=80%Q2": lambda r: tasa(r, 'A', 3) >= .8 * tasa(r, 'A', 1)},
        'E2J': {"W_D>=0.85": lambda r: r['W']['D'] >= .85, "W_B<=-2.7": lambda r: r['W']['B'] <= -2.7},
        'E2K': {"W_D>=0.8": lambda r: r['W']['D'] >= .8, "W_B<=-2.4": lambda r: r['W']['B'] <= -2.4},
        'E2L': {"W_A~+1": lambda r: abs(r['W']['A'] - 1) < .15, "W_B~-3": lambda r: abs(r['W']['B'] + 3) < .3,
                "solap->0": lambda r: r['solap']['AB'] == 0},
    }
    p2 = True
    for esc, crit in CRIT.items():
        for lam in (0.0, LAM):
            rs = R(esc, lam)
            det = " ".join(f"{n}:{sum(c(r) for r in rs)}/{S}" for n, c in crit.items())
            ok = all(all(c(r) for c in crit.values()) for r in rs)
            if lam == LAM and not ok: p2 = False
            print(f"  {esc:4s} lam={lam:<7} {'PASA ' if ok else 'FALLA'} [{det}]")
    print(f"\n  P2 -> {'SOSTENIDA' if p2 else 'REFUTADA'}")

    # ---------------- P3 precision del valor ----------------
    print("\n" + "=" * 78)
    print("P3 — PRECISION DEL VALOR contra el equilibrio analitico W* = 3*eta*R/(3*eta+lam)")
    print("=" * 78)
    p3 = True
    for lam in [0.0, LAM] + SENS:
        rs = R('E1', lam)
        if not rs: continue
        wa, wb = med([r['W']['A'] for r in rs]), med([r['W']['B'] for r in rs])
        pa, pb = EQ(1.0, lam), EQ(-3.0, lam)
        da, db = abs(wa[0] - pa), abs(wb[0] - pb)
        marca = ''
        if lam == LAM:
            p3 = da <= 0.02 and db <= 0.02
            marca = '  <- primario'
        print(f"  lam={lam:<7} W_A obs {wa[0]:+.4f} pred {pa:+.4f} (d={da:.4f}) | "
              f"W_B obs {wb[0]:+.4f} pred {pb:+.4f} (d={db:.4f}){marca}")
    print(f"\n  P3 -> {'SOSTENIDA' if p3 else 'REFUTADA'}  (ambas desviaciones <= 0.02)")

    # ---------------- P4 ley de disparo ----------------
    print("\n" + "=" * 78)
    print("P4 — LEY DE DISPARO: el decaimiento no debe cambiar el patron de divisiones")
    print("=" * 78)
    p4 = True
    for esc in ('E1', 'E2', 'E2I', 'E2J', 'E2K', 'E2L'):
        a = [r['splits'] for r in sorted(R(esc, 0.0), key=lambda r: r['seed'])]
        b = [r['splits'] for r in sorted(R(esc, LAM), key=lambda r: r['seed'])]
        fa, fb = sum(x > 0 for x in a), sum(x > 0 for x in b)
        igual = fa == fb
        p4 &= igual
        print(f"  {esc:4s} dividen  lam=0: {fa}/{S}   lam={LAM}: {fb}/{S}   "
              f"splits medianos {np.median(a):.0f} -> {np.median(b):.0f}  {'ok' if igual else 'CAMBIA'}")
    print(f"\n  P4 -> {'SOSTENIDA' if p4 else 'REFUTADA'}")

    # ---------------- salida ----------------
    h = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
    stamp = time.strftime('%Y%m%d_%H%M%S')
    meta = dict(experimento='BUG01_decaimiento_exp1', fecha=time.strftime('%Y-%m-%dT%H:%M:%S'),
                lam_primario=LAM, lam_sensibilidad=SENS, n_semillas=S, T=100000,
                escenarios={k: {kk: str(vv) for kk, vv in v.items()} for k, v in ESCENARIOS.items()},
                sha_organismo_v7d=h(os.path.join(AQUI, 'organismo_v7d.py')),
                sha_organismo_v7=h(os.path.join(RAIZ, 'organismo', 'organismo_v7.py')),
                sha_script=h(os.path.abspath(__file__)),
                sha_preregistro=h(os.path.join(AQUI, 'PREREGISTRO.md')),
                python=platform.python_version(), numpy=np.__version__, plataforma=platform.platform(),
                veredictos=dict(P1=bool(p1a and p1b), P2=bool(p2), P3=bool(p3), P4=bool(p4)))
    dst = os.path.join(RAIZ, 'datos', f'bug01_decaimiento_{stamp}.json')
    assert not os.path.exists(dst), f'ya existe: {dst}'
    json.dump(dict(meta=meta, corridas=res), open(dst, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f"\ndatos -> {dst}")
    print(f"        sha256_16 = {h(dst)}")
    print(f"\nVEREDICTO GLOBAL exp.1: P1={meta['veredictos']['P1']} P2={meta['veredictos']['P2']} "
          f"P3={meta['veredictos']['P3']} P4={meta['veredictos']['P4']}")
