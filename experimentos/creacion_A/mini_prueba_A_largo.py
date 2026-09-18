"""CREADOR A — mini-prueba de UN proceso: metaplasticidad por masa de conflicto contra la retencion de lo ausente.

ETAPA 1 (identidad, no cuenta contra el cupo): `mundo_largo_A` con `beta_m=None` == `mundo_largo` en TODAS las
claves, en varias semillas y a T corto.
ETAPA 2 (calibracion, lectura): una corrida con `m_stats=True` para saber que magnitud tiene la masa de conflicto.
ETAPA 3 (mini-prueba): brazo V13 del mundo largo (T=200000, T_INV=100000, pool de 50, `usa_M=False`), baseline
contra `beta_m`, en TANDAS DE <= 3 CORRIDAS. Medida que manda: `ret_no_inv` (signo correcto en los 6 patrones
nunca invertidos y AUSENTES al final) — la que el registro mide en 0.67. Controles que pueden fallar y se miden
en la misma corrida: `adq_final` (adquisicion; no debe caer) y `rec` (recuperacion tras el cambio de regla en
t=100000; no debe empeorar), mas `celdas`/`splits`.
Uso:  python mini_prueba_A_largo.py identidad
      python mini_prueba_A_largo.py calibra
      python mini_prueba_A_largo.py tanda <beta_m|base> <s1> <s2> <s3>
Sin Pool. Nunca mas de 3 corridas de T=200000 por invocacion.
"""
import sys, os, json, time
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
LARGO = os.path.join(RAIZ, 'experimentos', 'nivel8_mundo_largo')
sys.path[:0] = [AQUI, LARGO, os.path.join(RAIZ, 'experimentos', 'nivel6_mapa'), os.path.join(RAIZ, 'organismo')]

import corre_mundo_largo as C   # solo pool_de / sitios_de / recuperacion / T (no se edita)
import mundo_largo as ORIG
import mundo_largo_A as NUEVO


def N(x):
    return json.loads(json.dumps(x, default=str))


def kw_de(seed, T=C.T, **extra):
    pool = C.pool_de(seed)
    kw = dict(T=T, r_vis=3, sitios=C.sitios_de(pool, seed), pool=pool, T_nuevo=C.T_NUEVO,
              invertir_largo=(C.T_INV if T >= C.T else None), usa_M=False)
    kw.update(extra)
    return kw


def metricas(r):
    cv = r['curva']; vf = r['val_final']; vs = r['vistos']; W = r['W']
    ok = lambda n: (W[n] > 0) == (vf[n] == 'comida')
    hasta30 = [c[2] for c in cv if c[1] <= 30]; fin = cv[-1] if cv else (None, None, None, None)
    m = dict(ret_no_inv=float(np.mean([ok(n) for n in vs[4:10]])) if len(vs) >= 10 else None,
             ret_inv=float(np.mean([ok(n) for n in vs[:4]])),
             adq_hasta30=float(np.median(hasta30)) if hasta30 else None, adq_final=fin[2], ret_final=fin[3],
             n_vistos=len(vs), deaths=r['deaths'], celdas=r['celdas'], splits=r['splits'])
    m.update(C.recuperacion(r['comida_bin'], r['muertes_bin']))
    return m


if __name__ == '__main__':
    modo = sys.argv[1] if len(sys.argv) > 1 else 'identidad'

    if modo == 'identidad':
        malas = []
        for seed in (1, 2, 3):
            for T in (20000, 40000):
                kw = kw_de(seed, T=T)
                a, b = ORIG.run(seed, **kw), NUEVO.run(seed, **kw)
                dif = [k for k in a if N(a[k]) != N(b[k])]
                print(f'  s{seed} T={T}: {"IDENTICO" if not dif else "DIFIEREN " + str(dif)} ({len(a)} claves)')
                if dif: malas.append((seed, T, dif))
            kw = kw_de(seed, T=20000, usa_M=True)   # tambien con mapa, por cobertura
            a, b = ORIG.run(seed, **kw), NUEVO.run(seed, **kw)
            dif = [k for k in a if N(a[k]) != N(b[k])]
            print(f'  s{seed} T=20000 mapa: {"IDENTICO" if not dif else "DIFIEREN " + str(dif)}')
            if dif: malas.append((seed, 'mapa', dif))
        print('IDENTIDAD:', 'OK 9/9' if not malas else f'FALLA {malas}')

    elif modo == 'calibra':
        for seed in (1, 2, 3):
            r = NUEVO.run(seed, m_stats=True, **kw_de(seed))
            print(f'  s{seed}  m: {r["m_stats"]}  ret_no_inv={metricas(r)["ret_no_inv"]:.3f}')

    elif modo == 'tanda':
        arg = sys.argv[2]; beta = None if arg == 'base' else float(arg)
        seeds = [int(x) for x in sys.argv[3:]]
        assert len(seeds) <= 3, 'maximo 3 corridas de 200000 por tanda'
        out = []
        for s in seeds:
            t0 = time.time()
            r = NUEVO.run(s, beta_m=beta, m_stats=True, **kw_de(s))
            m = metricas(r); m.update(seed=s, beta_m=beta, seg=round(time.time() - t0, 1), m_stats=r['m_stats'])
            out.append(m)
            print(f'  s{s:>3} beta_m={arg:>6}  ret_no_inv={m["ret_no_inv"]:.3f}  ret_inv={m["ret_inv"]:.3f}  '
                  f'adq={m["adq_final"]}  rec={m["rec"]}  celdas={m["celdas"]}  splits={m["splits"]}  '
                  f'muertes={m["deaths"]}  m_max={r["m_stats"]["max"]:.3f}  ({m["seg"]}s)')
        f = os.path.join(AQUI, f'mini_largo_{arg}.json')
        viejo = json.load(open(f)) if os.path.exists(f) else []
        json.dump(viejo + out, open(f, 'w'), indent=1)
        print('->', f)
    else:
        print(__doc__)
