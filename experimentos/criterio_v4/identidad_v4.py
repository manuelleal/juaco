"""ARNES DE IDENTIDAD de lo NUEVO de V4-CAL (lo reusado, organismo_v3cal, lo cubre identidad_criterio_v3.py: 54/54).
UN proceso, sin Pool. Se corre ANTES de mirar cualquier numero. Escribe su JSON en datos/humo/ (ERR-42).

IDENTIDADES (bit a bit, todas las claves):
  J1  tarea_vivo(OFF, s) del runner == organismo_v3cal.run(s, **corre_vivo_rep2.BRAZOS[b], desambiguar=1) (VIVO y CUELLO_MIN)
      -> el brazo OFF del runner ES el tronco v14.2 en el montaje de T-A.
  J2  tarea_vivo(TRONCO_B, s) == organismo_v3cal.run(s + 100000, mismos kwargs que OFF)
      -> TRONCO_B es el tronco, sin perilla, en la semilla desplazada (ley identica por construccion).
  J3  tarea_rev(OFF, s) == organismo_v3cal.run(s, **mini_vivo.BRAZOS['VIVO'], desambiguar=1, invertir_vivo_en=T/2)
  J4  tarea_rev(TRONCO_B, s) == organismo_v3cal.run(s + 100000, mismos kwargs que J3)
  J5  el juez es simetrico: la letra v4 aplicada a (x, x) PASA en T-A, T-C ii y T-F (lista identica contra si misma)

CONTROLES QUE DEBEN FALLAR:
  K1  TRONCO_B != OFF en la misma semilla-etiqueta (si fueran iguales, el tronco contra si mismo seria trivial: d = 0)
  K2  PLACEBO != OFF (la perilla actua)
  K3  PEOR != OFF
  K4  paja del juez: la letra v4 con el candidato desplazado delta = -40 en r / rev CAE (el juez puede decir que no)
  K5  paja del juez T-F: el candidato con muertes x1.5 CAE T-F

    python experimentos/criterio_v4/identidad_v4.py [T]     (T por defecto 20000)
"""
import sys, os, json, time
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import corre_criterio_v4 as R     # pone sys.path (organismo/, nivel11, criterio_v3) y verifica nada al importar

T = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 20000
DATOS_HUMO = R.DATOS_HUMO


def N(x):
    return json.dumps(x, sort_keys=True, default=str)


OK = [0]; NO = [0]; DET = []


def igual(nombre, a, b, debe_igual=True, claves=None):
    ks = claves or sorted(set(a) | set(b))
    dif = [k for k in ks if N(a.get(k)) != N(b.get(k))]
    bien = (not dif) if debe_igual else bool(dif)
    (OK if bien else NO)[0] += 1
    DET.append(f"  {'OK ' if bien else '***'} {nombre}" + ('' if bien else f"  (difieren {dif[:6]})" if debe_igual else '  (SALIO IDENTICO)'))
    print(DET[-1], flush=True)


def cond(nombre, x):
    (OK if x else NO)[0] += 1
    DET.append(f"  {'OK ' if x else '***'} {nombre}"); print(DET[-1], flush=True)


if __name__ == '__main__':
    R.verifica_anclas()
    import organismo_v3cal as CAL, corre_vivo_rep2 as CR2, mini_vivo as MV
    t0 = time.time(); s = 2923   # semilla de RESERVA (no es de la serie ni del humo)
    print(f"ARNES V4 — T={T}, semilla {s} (reserva), TRONCO_B = s + {R.DESPL}")
    print("--- J1/J2: el montaje de T-A")
    for b in R.BRAZOS_TA:
        kw = dict(CR2.BRAZOS[b], desambiguar=1)
        oA = R.tarea_vivo((b, s, 'OFF', T)); ref = CR2.resumen2(b, s, CAL.run(s, T=T, **kw), kw, T)
        cl = [k for k in ref if k not in ('seed',)]
        igual(f"J1 {b}: OFF del runner == tronco v14.2 (resumen2, {len(cl)} claves)", oA, ref, claves=cl)
        oB = R.tarea_vivo((b, s, 'TRONCO_B', T)); refB = CR2.resumen2(b, s + R.DESPL, CAL.run(s + R.DESPL, T=T, **kw), kw, T)
        igual(f"J2 {b}: TRONCO_B == tronco en s+{R.DESPL}", oB, refB, claves=cl)
        igual(f"K1 {b}: TRONCO_B != OFF (DEBE diferir)", oB, oA, debe_igual=False, claves=['r', 'deaths', 'descendientes', 'splits'])
        if b == 'VIVO':
            oP = R.tarea_vivo((b, s, 'PLACEBO', T)); oW = R.tarea_vivo((b, s, 'PEOR', T))
            igual("K2 VIVO: PLACEBO != OFF (DEBE diferir)", oP, oA, debe_igual=False, claves=['r', 'deaths', 'descendientes', 'splits'])
            igual("K3 VIVO: PEOR != OFF (DEBE diferir)", oW, oA, debe_igual=False, claves=['r', 'deaths', 'descendientes', 'splits'])
    print("--- J3/J4: el montaje de T-C (ii)")
    kwr = dict(MV.BRAZOS['VIVO'], desambiguar=1, invertir_vivo_en=T // 2)
    rA = R.tarea_rev((s, 'OFF', T)); x = CAL.run(s, T=T, **kwr)
    igual("J3 T-C ii: OFF del runner == tronco (mord, vis, deaths, celdas, splits)", rA,
          dict(mordA=x['mord']['A'], mordB=x['mord']['B'], visA=x['vis']['A'], visB=x['vis']['B'], deaths=x['deaths'],
               celdas=x['celdas'], splits=x['splits']), claves=['mordA', 'mordB', 'visA', 'visB', 'deaths', 'celdas', 'splits'])
    rB = R.tarea_rev((s, 'TRONCO_B', T)); y = CAL.run(s + R.DESPL, T=T, **kwr)
    igual("J4 T-C ii: TRONCO_B == tronco en s+100000", rB,
          dict(mordA=y['mord']['A'], mordB=y['mord']['B'], visA=y['vis']['A'], visB=y['vis']['B'], deaths=y['deaths'],
               celdas=y['celdas'], splits=y['splits']), claves=['mordA', 'mordB', 'visA', 'visB', 'deaths', 'celdas', 'splits'])
    print("--- J5 / K4 / K5: el juez (listas sinteticas de 80, sin simulacion)")
    import numpy as np
    g = np.random.default_rng(7)
    L = [dict(seed=i, r=float(g.normal(-75, 12)), deaths=float(g.normal(95, 10)), celdas=37.0, splits=7.0, rev=float(g.normal(42, 20))) for i in range(80)]
    cond("J5 T-A v4 (x, x) PASA", R.letra_TA(L, L, R.U.V4['T-A'])[0])
    cond("J5 T-C ii v4 (x, x) PASA", R.letra_TC(L, L, R.U.V4['T-C_ii'])[0])
    cond("J5 T-F (x, x) PASA", R.letra_TF(L, L)[0])
    cond("K4 T-A v4 con delta = -40 CAE", not R.letra_TA(L, L, R.U.V4['T-A'], delta=-40.0)[0])
    cond("K4 T-C ii v4 con delta = -40 CAE", not R.letra_TC(L, L, R.U.V4['T-C_ii'], delta=-40.0)[0])
    Lm = [dict(d, deaths=d['deaths'] * 1.5) for d in L]
    cond("K5 T-F con muertes x1.5 CAE", not R.letra_TF(L, Lm)[0])
    tot = f"ARNES V4 TOTAL: {OK[0]}/{OK[0] + NO[0]} {'OK' if NO[0] == 0 else 'FALLA'}"
    print(f"{tot}  ({time.time() - t0:.1f} s)")
    os.makedirs(DATOS_HUMO, exist_ok=True)
    f = os.path.join(DATOS_HUMO, f"identidad_v4_{time.strftime('%Y%m%d_%H%M%S')}.json")
    json.dump(dict(T=T, semilla=s, total=tot, detalle=DET, seg=round(time.time() - t0, 1)), open(f, 'w', encoding='utf-8'), ensure_ascii=False)
    print(f"datos -> {os.path.basename(f)}")
    sys.exit(0 if NO[0] == 0 else 1)
