"""BUG-01 experimento 2: decaimiento de la PARTE COMUN de Wp/Wn.

Ejecuta el preregistro de PREREGISTRO_exp2.md. No decide nada que no este escrito alli.
Corre primero los CONTROLES y ABORTA si alguno falla: si el instrumento esta sucio, el
resultado no vale (regla 5 del proyecto).

Uso:  python corre_bug01_exp2.py [semillas]      (por defecto 20, ~4 min con 16 nucleos)
"""
import sys, os, json, time, hashlib, platform
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo')]

LAM = 0.05                              # fijado a priori. Ver PREREGISTRO_exp2.md seccion 2.
SENS = [0.0125, 0.02, 0.1, 0.3]         # descriptivo, NO decide
ETA, K = 0.03, 3
WP_PRED, WN_PRED, TOL_PRED = 1.8, 2.8, 0.5   # prediccion puntual de P1
SIN_CONFLICTO = ('E1', 'E2I', 'E2J')    # aqui min(Wp,Wn)=0 -> la operacion debe ser INERTE

ESCENARIOS = {
    'BUG':  dict(plast=False, solap_AB=3),
    'E1':   dict(),
    'E2':   dict(invertir_en=50000),
    'E2I':  dict(nuevo='C'),
    'E2J':  dict(nuevo='D', nuevo_val='comida', solap_B=1),
    'E2K':  dict(nuevo='D', nuevo_val='comida', solap_B=2),
    'E2L':  dict(solap_AB=3),
}


T_EXP = 100000   # el preregistro fija T=100.000. Solo se cambia para probar fontaneria.


def tarea(args):
    esc, lam, seed = args
    import organismo_v7e as o
    r = o.run(seed, T=T_EXP, lam=lam, **ESCENARIOS[esc])
    return dict(esc=esc, lam=lam, seed=seed, W=r['W'], comp=r['comp'], deaths=r['deaths'],
                splits=r['splits'], split_t=r['split_t'], celdas=r['celdas'], solap=r['solap'],
                mord={k: list(v) for k, v in r['mord'].items()},
                vis={k: list(v) for k, v in r['vis'].items()})


def controles():
    """Controles 1 y 2 del preregistro. Devuelve True solo si los dos pasan."""
    import organismo_v7 as v7, organismo_v7e as v7e
    print("=" * 78)
    print("CONTROLES (si fallan, el experimento no se corre)")
    print("=" * 78)
    tot = dif = 0
    for esc, kw in ESCENARIOS.items():
        for s in range(1, 7):
            a, b = v7.run(s, **kw), v7e.run(s, lam=0.0, **kw)
            tot += 1
            if a != b:
                dif += 1
                print(f"  DIFIERE {esc} semilla {s}: {[k for k in a if a[k] != b[k]]}")
    c1 = dif == 0
    print(f"  Control 1 (inercia lam=0 vs v7): {tot-dif}/{tot} identicos -> "
          f"{'OK' if c1 else 'FALLA'}")
    r = v7e.run(1, lam=0.0, plast=False, solap_AB=3)
    c2 = r['comp']['A'] == (9.0, 9.0) and r['W']['A'] == 0.0
    print(f"  Control 2 (el bug se reproduce con lam=0): comp={r['comp']['A']} W={r['W']['A']} -> "
          f"{'OK' if c2 else 'FALLA'}")
    return c1 and c2


med = lambda xs: (float(np.median(xs)), float(np.min(xs)), float(np.max(xs)))
fmt = lambda t: f"{t[0]:+.3f} [{t[1]:+.3f}, {t[2]:+.3f}]"


if __name__ == '__main__':
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    S = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    if len(sys.argv) > 2:                      # solo para probar fontaneria; NO es el experimento
        T_EXP = int(sys.argv[2])
        globals()['T_EXP'] = T_EXP
        print(f"*** AVISO: T={T_EXP} != 100000. Esto NO es el experimento preregistrado,\n"
              f"*** es una prueba de que el script corre. Los veredictos que salgan NO valen.\n")
    seeds = list(range(1, S + 1))

    if not controles():
        print("\n*** CONTROLES FALLIDOS. No se corre el experimento. Primero el instrumento (regla 5).")
        sys.exit(1)

    t0 = time.time()
    trabajos = []
    for esc in ESCENARIOS:
        for lam in (0.0, LAM):
            trabajos += [(esc, lam, s) for s in seeds]
    for lam in SENS:
        for esc in ('BUG', 'E1'):
            trabajos += [(esc, lam, s) for s in seeds]

    print(f"\nBUG-01 exp.2 — decaimiento de la parte comun. {len(trabajos)} corridas, "
          f"{S} semillas, lam_c primario={LAM}\n")
    with mp.Pool(min(16, os.cpu_count())) as pool:
        res = pool.map(tarea, trabajos)
    print(f"({time.time()-t0:.0f} s de pared)\n")
    R = lambda esc, lam: sorted([r for r in res if r['esc'] == esc and r['lam'] == lam],
                                key=lambda r: r['seed'])

    # ---------- P1 ----------
    print("=" * 78); print("P1 — DESBLOQUEO (primario). plast=False, solap_AB=3"); print("=" * 78)
    for lam in [0.0, LAM] + SENS:
        rs = R('BUG', lam)
        if not rs: continue
        wp = [r['comp']['A'][0] for r in rs]; wn = [r['comp']['A'][1] for r in rs]
        w = [r['W']['A'] for r in rs]
        print(f"  lam={lam:<7} Wp={fmt(med(wp))}  Wn={fmt(med(wn))}  W={fmt(med(w))}  "
              f"bajo techo {sum(p < 9 and n < 9 for p, n in zip(wp, wn))}/{S}")
    rs = R('BUG', LAM)
    wp, wn = [r['comp']['A'][0] for r in rs], [r['comp']['A'][1] for r in rs]
    a1 = all(p < 9.0 and n < 9.0 for p, n in zip(wp, wn))
    a2 = abs(np.median(wp) - WP_PRED) <= TOL_PRED and abs(np.median(wn) - WN_PRED) <= TOL_PRED
    a3 = sum(-1.5 <= r['W']['A'] <= -0.5 for r in rs) >= int(0.9 * S)
    P1 = a1 and a2 and a3
    print(f"\n  bajo techo 20/20: {a1} | Wp~{WP_PRED} y Wn~{WN_PRED} +-{TOL_PRED}: {a2} "
          f"(obs {np.median(wp):.2f}, {np.median(wn):.2f}) | W en [-1.5,-0.5] >=90%: {a3}")
    print(f"  P1 -> {'SOSTENIDA' if P1 else 'REFUTADA'}")

    # ---------- P2 ----------
    print("\n" + "=" * 78); print("P2 — NO REGRESION (+ inercia exacta donde no hay conflicto)"); print("=" * 78)
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
    P2 = True
    for esc, crit in CRIT.items():
        rs = R(esc, LAM)
        det = " ".join(f"{n}:{sum(c(r) for r in rs)}/{S}" for n, c in crit.items())
        ok = all(all(c(r) for c in crit.values()) for r in rs)
        extra = ""
        if esc in SIN_CONFLICTO:
            ident = all(a == b for a, b in zip(R(esc, 0.0), rs))
            ok &= ident
            extra = f"  inerte(bit-identico a lam=0): {'SI' if ident else 'NO <- REFUTA'}"
        P2 &= ok
        print(f"  {esc:4s} {'PASA ' if ok else 'FALLA'} [{det}]{extra}")
    print(f"\n  P2 -> {'SOSTENIDA' if P2 else 'REFUTADA'}")

    # ---------- P3 ----------
    print("\n" + "=" * 78); print("P3 — EXACTITUD DEL VALOR (sin sesgo: el decaimiento no toca Wp-Wn)"); print("=" * 78)
    rs = R('E1', LAM)
    wa, wb = med([r['W']['A'] for r in rs]), med([r['W']['B'] for r in rs])
    da, db = abs(wa[0] - 1.0), abs(wb[0] + 3.0)
    P3 = da <= 0.002 and db <= 0.002
    print(f"  W_A {fmt(wa)}  desv de +1: {da:.4f}")
    print(f"  W_B {fmt(wb)}  desv de -3: {db:.4f}")
    print(f"  (exp.1 con decaimiento uniforme daba +0.990 / -2.970: sesgo del 1.1%)")
    print(f"\n  P3 -> {'SOSTENIDA' if P3 else 'REFUTADA'}  (ambas desviaciones <= 0.002)")

    # ---------- P4 ----------
    print("\n" + "=" * 78); print("P4 — LEY DE DISPARO: no debe cambiar QUIEN divide"); print("=" * 78)
    P4 = True
    for esc in ('E1', 'E2', 'E2I', 'E2J', 'E2K', 'E2L'):
        a = [r['splits'] > 0 for r in R(esc, 0.0)]; b = [r['splits'] > 0 for r in R(esc, LAM)]
        igual = a == b
        P4 &= igual
        print(f"  {esc:4s} dividen  lam=0: {sum(a)}/{S}   lam={LAM}: {sum(b)}/{S}   "
              f"mismos individuos: {'si' if igual else 'NO <- REFUTA'}   "
              f"splits medianos {np.median([r['splits'] for r in R(esc,0.0)]):.0f} -> "
              f"{np.median([r['splits'] for r in R(esc,LAM)]):.0f}")
    print(f"\n  P4 -> {'SOSTENIDA' if P4 else 'REFUTADA'}")

    # ---------- salida ----------
    h = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
    stamp = time.strftime('%Y%m%d_%H%M%S')
    meta = dict(experimento='BUG01_parte_comun_exp2', fecha=time.strftime('%Y-%m-%dT%H:%M:%S'),
                lam_primario=LAM, lam_sensibilidad=SENS, n_semillas=S, T=100000,
                prediccion_puntual=dict(Wp=WP_PRED, Wn=WN_PRED, tol=TOL_PRED),
                escenarios={k: {kk: str(vv) for kk, vv in v.items()} for k, v in ESCENARIOS.items()},
                sha_organismo_v7e=h(os.path.join(AQUI, 'organismo_v7e.py')),
                sha_organismo_v7=h(os.path.join(RAIZ, 'organismo', 'organismo_v7.py')),
                sha_script=h(os.path.abspath(__file__)),
                sha_preregistro=h(os.path.join(AQUI, 'PREREGISTRO_exp2.md')),
                python=platform.python_version(), numpy=np.__version__, plataforma=platform.platform(),
                veredictos=dict(P1=bool(P1), P2=bool(P2), P3=bool(P3), P4=bool(P4)))
    dst = os.path.join(RAIZ, 'datos', f'bug01_exp2_{stamp}.json')
    assert not os.path.exists(dst), f'ya existe: {dst}'
    json.dump(dict(meta=meta, corridas=res), open(dst, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f"\ndatos -> {dst}\n        sha256_16 = {h(dst)}")
    print(f"\nVEREDICTO exp.2: P1={P1} P2={P2} P3={P3} P4={P4}")
    print("\nPega en el registro la linea con: fecha, los 4 veredictos, y los hashes de arriba (regla 7).")
    if P1 and P2 and P3 and P4:
        print("Si los cuatro se sostienen: siguiente paso, repetir 3T como CONFIRMATORIO con este arreglo.")
    else:
        print("Si P1 se refuta: experimento 3 (normalizacion opuesta completa), ya descrito en el preregistro.")
