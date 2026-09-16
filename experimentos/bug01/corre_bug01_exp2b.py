"""BUG-01 exp. 2b: reejecucion de P2 con el instrumento corregido (ERR-07).

Ejecuta PREREGISTRO_exp2b.md. No decide nada que no este escrito alli.

Diferencias con corre_bug01_exp2.py, y son las UNICAS:
  1. ERR-07: la comparacion de inercia ignora las claves de etiqueta (esc, lam, seed). Antes comparaba
     los dicts enteros, que incluyen 'lam', asi que era estructuralmente False.
  2. SIN_CONFLICTO se CALCULA por (escenario, semilla) midiendo el solapamiento de codigos. No hay
     ninguna lista de semillas escrita a mano.
  3. Control positivo P2b: donde SI hay conflicto, el resultado NO debe ser identico.
  4. Control 3: la sonda de codigos debe ser bit-identica a organismo_v7e en las claves compartidas.

El organismo bajo examen, organismo_v7e.py, NO se toca.

Uso:  python corre_bug01_exp2b.py [semillas]      (por defecto 20, ~8 min con 16 nucleos)
"""
import sys, os, json, time, hashlib, platform
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo')]

LAM = 0.05                              # fijado a priori en PREREGISTRO_exp2.md seccion 2. NO se recalibra.
ETA, K = 0.03, 3

ESCENARIOS = {
    'BUG':  dict(plast=False, solap_AB=3),
    'E1':   dict(),
    'E2':   dict(invertir_en=50000),
    'E2I':  dict(nuevo='C'),
    'E2J':  dict(nuevo='D', nuevo_val='comida', solap_B=1),
    'E2K':  dict(nuevo='D', nuevo_val='comida', solap_B=2),
    'E2L':  dict(solap_AB=3),
}
NUEVO = {'E2I': 'C', 'E2J': 'D', 'E2K': 'D'}     # que estimulo extra vive en cada escenario

T_EXP = 100000


def tarea(args):
    esc, lam, seed = args
    import organismo_v7e as o
    r = o.run(seed, T=T_EXP, lam=lam, **ESCENARIOS[esc])
    return dict(esc=esc, lam=lam, seed=seed, W=r['W'], comp=r['comp'], deaths=r['deaths'],
                splits=r['splits'], split_t=r['split_t'], celdas=r['celdas'], solap=r['solap'],
                mord={k: list(v) for k, v in r['mord'].items()},
                vis={k: list(v) for k, v in r['vis'].items()})


def clasifica(args):
    """Mide el solapamiento real de codigos. Devuelve True si el par (esc, seed) es SIN_CONFLICTO.

    Definicion de PREREGISTRO_exp2b.md seccion 3: cero solapamiento entre TODOS los codigos presentes.
    Se mide, no se decide.
    """
    esc, seed = args
    import sonda_codigos as s
    r = s.run(seed, T=T_EXP, lam=0.0, **ESCENARIOS[esc])
    c = {k: set(v) for k, v in r['codigos'].items()}
    ov = {'AB': len(c['A'] & c['B'])}
    n = NUEVO.get(esc)
    if n:
        ov['nA'] = len(c[n] & c['A'])
        ov['nB'] = len(c[n] & c['B'])
    return dict(esc=esc, seed=seed, solapamientos=ov, sin_conflicto=all(v == 0 for v in ov.values()))


# claves de etiqueta: son indice, no resultado. ERR-07 estaba en no excluirlas.
ETIQUETAS = ('esc', 'lam', 'seed')
sin_etq = lambda r: {k: v for k, v in r.items() if k not in ETIQUETAS}


def controles():
    """Controles 1, 2 y 3 del preregistro. Devuelve True solo si los tres pasan."""
    import organismo_v7 as v7, organismo_v7e as v7e, sonda_codigos as sc
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
    print(f"  Control 1 (inercia lam=0 vs v7): {tot-dif}/{tot} identicos -> {'OK' if c1 else 'FALLA'}")

    r = v7e.run(1, lam=0.0, plast=False, solap_AB=3)
    c2 = r['comp']['A'] == (9.0, 9.0) and r['W']['A'] == 0.0
    print(f"  Control 2 (el bug se reproduce con lam=0): comp={r['comp']['A']} W={r['W']['A']} -> "
          f"{'OK' if c2 else 'FALLA'}")

    tot3 = dif3 = 0
    for esc, kw in ESCENARIOS.items():
        for s in range(1, 7):
            a = v7e.run(s, lam=0.0, **kw)
            b = sc.run(s, lam=0.0, **kw)
            tot3 += 1
            if any(a[k] != b[k] for k in a):          # solo las claves compartidas; la sonda anade 'codigos'
                dif3 += 1
                print(f"  SONDA DIFIERE {esc} semilla {s}")
    c3 = dif3 == 0
    print(f"  Control 3 (la sonda es el mismo organismo): {tot3-dif3}/{tot3} identicos -> "
          f"{'OK' if c3 else 'FALLA'}")
    return c1 and c2 and c3


med = lambda xs: (float(np.median(xs)), float(np.min(xs)), float(np.max(xs)))
fmt = lambda t: f"{t[0]:+.3f} [{t[1]:+.3f}, {t[2]:+.3f}]"


if __name__ == '__main__':
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    S = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    seeds = list(range(1, S + 1))

    if not controles():
        print("\n*** CONTROLES FALLIDOS. No se corre el experimento. Primero el instrumento (regla 5).")
        sys.exit(1)

    t0 = time.time()
    trabajos = [(esc, lam, s) for esc in ESCENARIOS for lam in (0.0, LAM) for s in seeds]
    clases = [(esc, s) for esc in ESCENARIOS for s in seeds]
    print(f"\nBUG-01 exp.2b — P2 con instrumento corregido. {len(trabajos)} corridas + "
          f"{len(clases)} clasificaciones, {S} semillas, lam={LAM}\n")
    with mp.Pool(min(16, os.cpu_count())) as pool:
        res = pool.map(tarea, trabajos)
        cls = pool.map(clasifica, clases)
    print(f"({time.time()-t0:.0f} s de pared)\n")

    R = lambda esc, lam: sorted([r for r in res if r['esc'] == esc and r['lam'] == lam],
                                key=lambda r: r['seed'])
    SC = {(c['esc'], c['seed']): c for c in cls}

    # ---------- clasificacion medida ----------
    print("=" * 78); print("CLASIFICACION MEDIDA (no declarada): solapamiento cero de TODOS los codigos")
    print("=" * 78)
    for esc in ESCENARIOS:
        libres = [s for s in seeds if SC[(esc, s)]['sin_conflicto']]
        print(f"  {esc:4s} sin conflicto: {len(libres):2d}/{S}"
              + (f"  semillas {libres}" if 0 < len(libres) < S else ""))

    # ---------- P2a / P2b ----------
    print("\n" + "=" * 78)
    print("P2a — INERCIA donde solap=0 (debe ser 100%) | P2b — CONTROL POSITIVO donde hay conflicto (0%)")
    print("=" * 78)
    n_lib = n_lib_id = n_con = n_con_id = 0
    for esc in ESCENARIOS:
        a, b = R(esc, 0.0), R(esc, LAM)
        for x, y in zip(a, b):
            ident = sin_etq(x) == sin_etq(y)
            if SC[(esc, x['seed'])]['sin_conflicto']:
                n_lib += 1; n_lib_id += ident
            else:
                n_con += 1; n_con_id += ident
        det_l = [s for s in seeds if SC[(esc, s)]['sin_conflicto']]
        idl = sum(sin_etq(x) == sin_etq(y) for x, y in zip(a, b) if SC[(esc, x['seed'])]['sin_conflicto'])
        idc = sum(sin_etq(x) == sin_etq(y) for x, y in zip(a, b) if not SC[(esc, x['seed'])]['sin_conflicto'])
        print(f"  {esc:4s} sin_conflicto {idl}/{len(det_l):2d} identicos   "
              f"con_conflicto {idc}/{S-len(det_l):2d} identicos")
    P2a = (n_lib_id == n_lib)
    P2b = (n_con_id == 0)
    print(f"\n  P2a: {n_lib_id}/{n_lib} identicos donde solap=0  -> {'SOSTENIDA' if P2a else 'REFUTADA'}")
    print(f"  P2b: {n_con_id}/{n_con} identicos donde hay conflicto (debe ser 0) -> "
          f"{'SOSTENIDA' if P2b else 'REFUTADA'}")

    # ---------- P2c: criterios cientificos ----------
    print("\n" + "=" * 78); print("P2c — CRITERIOS CIENTIFICOS DE LAS SEIS ETAPAS"); print("=" * 78)
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
    P2c = True
    for esc, crit in CRIT.items():
        rs = R(esc, LAM)
        det = " ".join(f"{n}:{sum(c(r) for r in rs)}/{S}" for n, c in crit.items())
        ok = all(all(c(r) for c in crit.values()) for r in rs)
        P2c &= ok
        print(f"  {esc:4s} {'PASA ' if ok else 'FALLA'} [{det}]")
    print(f"\n  P2c -> {'SOSTENIDA' if P2c else 'REFUTADA'}")

    P2 = P2a and P2b and P2c
    print(f"\n  P2 (corregida) -> {'SOSTENIDA' if P2 else 'REFUTADA'}")

    # ---------- salida ----------
    h = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
    stamp = time.strftime('%Y%m%d_%H%M%S')
    meta = dict(experimento='BUG01_parte_comun_exp2b_ERR07', fecha=time.strftime('%Y-%m-%dT%H:%M:%S'),
                corrige='bug01_exp2_20260915_183244.json', lam=LAM, n_semillas=S, T=T_EXP,
                escenarios={k: {kk: str(vv) for kk, vv in v.items()} for k, v in ESCENARIOS.items()},
                sha_organismo_v7e=h(os.path.join(AQUI, 'organismo_v7e.py')),
                sha_sonda_codigos=h(os.path.join(AQUI, 'sonda_codigos.py')),
                sha_organismo_v7=h(os.path.join(RAIZ, 'organismo', 'organismo_v7.py')),
                sha_script=h(os.path.abspath(__file__)),
                sha_preregistro=h(os.path.join(AQUI, 'PREREGISTRO_exp2b.md')),
                python=platform.python_version(), numpy=np.__version__, plataforma=platform.platform(),
                veredictos=dict(P2a=bool(P2a), P2b=bool(P2b), P2c=bool(P2c), P2=bool(P2)))
    dst = os.path.join(RAIZ, 'datos', f'bug01_exp2b_{stamp}.json')
    assert not os.path.exists(dst), f'ya existe: {dst}'
    json.dump(dict(meta=meta, clasificacion=cls, corridas=res), open(dst, 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    print(f"\ndatos -> {dst}\n        sha256_16 = {h(dst)}")
    print(f"\nVEREDICTO exp.2b: P2a={P2a} P2b={P2b} P2c={P2c}  ->  P2={P2}")
    print("\nPega en el registro la linea con: fecha, veredictos y hashes de arriba (regla 7).")
