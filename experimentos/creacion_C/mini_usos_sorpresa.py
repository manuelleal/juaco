"""MINI-PRUEBA C1-c — ¿QUE SORPRESA SIRVE?: la del MUNDO (dE, bloque 6) contra la de SI MISMO (la accion propia),
a la MISMA ganancia, midiendo la recuperacion tras la inversion con el criterio del bloque 6 (t_ext_B).

Tres brazos, mismas semillas, mismo mundo (T = 200 000, invertir_en = 100 000). Los tres instrumentos son
bit-a-bit identicos al tronco con sus perillas apagadas (v13a: I1/I2 del bloque 6; v13s: I1/I2/I3, 18/18 cada una).
  V13    organismo_v13s con k_auto = 0                       -> el tronco
  AUTO   organismo_v13s con eta_b = 0.03, k_auto = 1.0        -> eta_ef = eta*(1 + 1.0*|mordio - b_SELF|)
  dE     organismo_v13a con eta_pred = 0.03, k_sorpresa = 1.0 -> eta_ef = eta*(1 + 1.0*|dE - dE_pred|)   (bloque 6)

PREDICCION ESCRITA ANTES DE CORRER (es una prediccion de ESCALA, y dice que mi propio mecanismo NO alcanza):
  MP-C1a  eta_media[Q3] de AUTO <= 1.10  y  de dE >= 1.30. La sorpresa sobre si mismo es un orden de magnitud mas
          pequena que la de dE porque el 96 % de los encuentros se predicen bien (ba_fuera = 0.96 en la tanda 1).
  MP-C1b  (t_ext_B - invertir_en) de AUTO dentro de +-20 % del de V13 en 3/3: a ganancia 1.0 no cambia nada.
  MP-C1c  se informa la ganancia k_auto que haria falta para igualar el exceso de eta de dE:
          k* = (eta_media_dE[Q3] - 1) / sorpresa_media_AUTO_en_bocados.  Es el numero que necesita el preregistro.

Uso:  python experimentos/creacion_C/mini_usos_sorpresa.py [T] [n_semillas]
"""
import os, sys, json, time, statistics as st

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, 'organismo'))
sys.path.insert(0, os.path.join(RAIZ, 'experimentos', 'nivel9_allostasis'))
sys.path.insert(0, AQUI)
import organismo_v13s as V13S
import organismo_v13a as V13A


def main():
    T = int(sys.argv[1]) if len(sys.argv) > 1 else 200000
    N = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    INV = T // 2
    print(f"MINI C1-c — que sorpresa sirve. T={T}, invertir_en={INV}, semillas 1-{N}")
    print(f"{'sem':>4} {'brazo':>6} | {'t_ext_B-inv':>11} {'deaths':>6} {'d_post':>6} | {'eta_med Q1..Q4':>34} | {'sorpresa Q1..Q4':>30}")
    res = {a: [] for a in ('V13', 'AUTO', 'dE')}
    t0 = time.time()
    for s in range(1, N + 1):
        for brazo in ('V13', 'AUTO', 'dE'):
            if brazo == 'V13':
                r = V13S.run(s, T=T, invertir_en=INV, eta_b=0.03, k_auto=0.0, buf_auto=1000)
                sor = r['sorpresa_auto']
            elif brazo == 'AUTO':
                r = V13S.run(s, T=T, invertir_en=INV, eta_b=0.03, k_auto=1.0, buf_auto=1000)
                sor = r['sorpresa_auto']
            else:
                r = V13A.run(s, T=T, invertir_en=INV, eta_pred=0.03, k_sorpresa=1.0)
                sor = r['sorpresa_media']
            rec = (r['t_ext_B'] - INV) if r['t_ext_B'] is not None else None
            res[brazo].append(dict(rec=rec, deaths=r['deaths'], dp=r.get('deaths_post'),
                                   eta=r['eta_media'], sor=[float(x) if x is not None else None for x in sor],
                                   W=r['W']))
            print(f"{s:>4} {brazo:>6} | {str(rec):>11} {r['deaths']:>6} {str(r.get('deaths_post')):>6} | "
                  f"{str([round(float(x),3) if x is not None else None for x in r['eta_media']]):>34} | "
                  f"{str([round(float(x),4) if x is not None else None for x in sor]):>30}")
    print("\n=== VEREDICTO (criterios escritos antes) ===")
    e3 = {a: [f['eta'][2] for f in res[a]] for a in res}
    rc = {a: [f['rec'] for f in res[a]] for a in res}
    okA = sum(1 for x in e3['AUTO'] if x is not None and x <= 1.10)
    okB = sum(1 for x in e3['dE'] if x is not None and x >= 1.30)
    okC = sum(1 for a, v in zip(rc['AUTO'], rc['V13'])
              if a is not None and v is not None and abs(a - v) <= 0.20 * v)
    print(f"  MP-C1a  eta_media[Q3]: AUTO={[round(float(x),4) for x in e3['AUTO']]} (<=1.10) -> {okA}/{N} | "
          f"dE={[round(float(x),4) for x in e3['dE']]} (>=1.30) -> {okB}/{N}")
    print(f"  MP-C1b  recuperacion (t_ext_B - inv): V13={rc['V13']}  AUTO={rc['AUTO']}  dE={rc['dE']} "
          f"-> AUTO dentro de +-20% de V13 en {okC}/{N}")
    sA = [f['sor'][2] for f in res['AUTO'] if f['sor'][2] is not None]
    exc = [float(x) - 1 for x in e3['dE'] if x is not None]
    if sA and exc:
        print(f"  MP-C1c  ganancia necesaria k* = exceso_eta(dE,Q3)/sorpresa_AUTO(Q3) = "
              f"{round(st.median(exc),4)} / {round(st.median(sA),4)} = {round(st.median(exc)/max(st.median(sA),1e-9),1)}")
    for a in res:
        v = [x for x in rc[a] if x is not None]
        print(f"  mediana recuperacion {a:>5}: {st.median(v) if v else None}   muertes {st.median([f['deaths'] for f in res[a]])}")
    print(f"  ({round(time.time()-t0,1)} s totales)")
    json.dump(res, open(os.path.join(AQUI, 'mini_usos_sorpresa_salida.json'), 'w'), default=str, indent=1)


if __name__ == '__main__':
    main()
