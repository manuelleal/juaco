"""MINI-PRUEBA C-P5 — APRENDER SIN MORDER por codificacion predictiva, y el canal de retorno.

UN proceso, sin Pool. Instrumento experimentos/creacion_C/organismo_v14pc.py (por anclas desde organismo/organismo_v14g.py,
sha 1f1318480cd34cde; identidad K1 12/12 con todo apagado). Mundo de regla del tronco v14 (mask_rel=2, puerta_pat=5,
pat_min=1), T = 100 000, fase 2 en 50 000, sonda cada 2 000 pasos, criterio 0.90, semillas 1-3.

Perillas, ninguna buscada: eta_pred = 0.03 (= eta del tronco, como el bloque 6) · eta_c = 0.015 (= eta_s, la tasa de la
propia via lenta) · n_pred_min = 20 bocados (el orden en que W_pred llega al 93.5 % del objetivo, medido en C2-a).

HUMO DECLARADO (semilla 1, px0, ya visto antes de escribir esto): SOLO-BOCADOS expo 2 298 encuentros / 157 bocados;
CONSOL-directo 1 703 / 165. Es decir: **menos encuentros, NO menos bocados.** Las predicciones se escriben sabiendolo.

PREDICCIONES ESCRITAS ANTES DE CORRER LAS 3 SEMILLAS:
  MP-K1 [exposiciones]  mediana de expo_criterio (ENCUENTROS) de CONSOL-directo <= 0.80 x la de SOLO-BOCADOS, 3/3 pareado.
  MP-K2 [sin morder]    mediana de expo_criterio_bocados <= 0.80 x la de SOLO-BOCADOS.  **PREDIGO QUE FALLA** (humo 1.05 x).
                        Lectura preregistrada si falla: la consolidacion acelera POR EXPOSICION, no ahorra mordidas;
                        el mecanismo no es "aprender sin morder" sino "sacar antes la regla de lo ya mordido".
  MP-K3 [canal]         el canal ALEATORIO no compra: expo_criterio de 'fa' >= 1.0 x la de SOLO-BOCADOS en 3/3, y
                        'fa' no mejor que su control 'fa_shuf' (pareado <= 2/3). 'directo' si mejora (MP-K1).
  MP-K4 [xor01]         acc_lenta_f2 de CONSOL-directo en xor01 <= 0.60 y no supera a SOLO-BOCADOS en mas de 0.05.
                        La via lenta es LINEAL: no puede representar XOR y la consolidacion no cambia eso. Es el control
                        que dice de que NO va este mecanismo.
  MP-K5 [no dana]       acc_lenta_f2 en px0 >= 0.90 en 3/3 para todos los brazos de consolidacion.

Uso:  python experimentos/creacion_C/mini_codpred.py [T] [n_semillas]
"""
import os, sys, json, time, statistics as st

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo')]
import organismo_v14pc as PC

BRAZOS = {
    'SOLO-BOCADOS': dict(eta_c=0.0),
    'CONSOL-directo': dict(eta_c=0.015, canal='directo'),
    'CONSOL-transp': dict(eta_c=0.015, canal='transp'),
    'CONSOL-fa': dict(eta_c=0.015, canal='fa'),
    'CONSOL-fa_shuf': dict(eta_c=0.015, canal='fa_shuf'),
}


def med(xs):
    xs = [x for x in xs if x is not None]
    return st.median(xs) if xs else None


def main():
    T = int(sys.argv[1]) if len(sys.argv) > 1 else 100000
    N = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    base = dict(T=T, mundo='regla', eta_s=0.015, puerta=3, mask_rel=2, puerta_pat=5, pat_min=1,
                eta_pred=0.03, probe_cada=2000, crit_expo=0.90)
    print(f"MINI C-P5 — aprender sin morder. T={T}, fase2={T//2}, semillas 1-{N}, sonda cada 2000, criterio 0.90")
    R = {}
    t0 = time.time()
    for regla in ('px0', 'xor01'):
        print(f"\n=== mundo de regla: {regla} ===")
        print(f"{'brazo':>16} {'sem':>4} | {'expo_enc':>8} {'expo_boc':>8} | {'acc_f2':>6} {'acc_fin':>7} | {'enc_tren':>8} {'mord_tren':>9} {'celdas':>6} {'s':>5}")
        for nom, kw in BRAZOS.items():
            if regla == 'xor01' and nom in ('CONSOL-transp', 'CONSOL-fa_shuf'):
                continue                                  # xor01 solo necesita el contraste principal (MP-K4)
            R[(regla, nom)] = []
            for s in range(1, N + 1):
                t1 = time.time()
                r = PC.run(s, regla=regla, **base, **kw)
                R[(regla, nom)].append(r)
                print(f"{nom:>16} {s:>4} | {str(r['expo_criterio']):>8} {str(r['expo_criterio_bocados']):>8} | "
                      f"{str(r['acc_lenta_f2']):>6} {str(r['acc_lenta_fin']):>7} | {r['enc_tren']:>8} {r['mord_tren']:>9} "
                      f"{r['celdas']:>6} {time.time()-t1:>5.1f}")

    print("\n=== VEREDICTO (criterios escritos antes; el humo de la semilla 1 estaba declarado) ===")
    def g(regla, nom, clave):
        return [x[clave] for x in R[(regla, nom)]]

    base_e = g('px0', 'SOLO-BOCADOS', 'expo_criterio'); base_b = g('px0', 'SOLO-BOCADOS', 'expo_criterio_bocados')
    dir_e = g('px0', 'CONSOL-directo', 'expo_criterio'); dir_b = g('px0', 'CONSOL-directo', 'expo_criterio_bocados')
    r1 = (med(dir_e) / med(base_e)) if med(base_e) else None
    p1 = sum(1 for a, b in zip(dir_e, base_e) if a is not None and b is not None and a < b)
    print(f"  MP-K1 encuentros: mediana {med(dir_e)} / {med(base_e)} = {None if r1 is None else round(r1,3)} (<=0.80), pareado {p1}/{N} -> {'OK' if (r1 is not None and r1<=0.80 and p1==N) else 'NO'}")
    r2 = (med(dir_b) / med(base_b)) if med(base_b) else None
    print(f"  MP-K2 bocados   : mediana {med(dir_b)} / {med(base_b)} = {None if r2 is None else round(r2,3)} (<=0.80) -> {'OK' if (r2 is not None and r2<=0.80) else 'NO (lo predicho)'}")
    fa_e = g('px0', 'CONSOL-fa', 'expo_criterio'); sh_e = g('px0', 'CONSOL-fa_shuf', 'expo_criterio')
    tr_e = g('px0', 'CONSOL-transp', 'expo_criterio')
    nfa = sum(1 for a, b in zip(fa_e, base_e) if a is not None and b is not None and a >= b)
    nfs = sum(1 for a, b in zip(fa_e, sh_e) if a is not None and b is not None and a < b)
    print(f"  MP-K3 canal     : fa {fa_e} (mediana {med(fa_e)}), fa_shuf {sh_e} ({med(sh_e)}), transp {tr_e} ({med(tr_e)}), base {base_e} ({med(base_e)})")
    print(f"                    fa >= base en {nfa}/{N}; fa mejor que fa_shuf en {nfs}/{N} (<=2 para que el canal NO compre) -> {'OK' if (nfa==N and nfs<=2) else 'NO'}")
    xa = g('xor01', 'CONSOL-directo', 'acc_lenta_f2'); xb = g('xor01', 'SOLO-BOCADOS', 'acc_lenta_f2')
    ok4 = (med(xa) is not None and med(xa) <= 0.60 and med(xa) <= (med(xb) or 0) + 0.05)
    print(f"  MP-K4 xor01     : acc_lenta_f2 CONSOL {xa} (mediana {med(xa)}) contra SOLO-BOCADOS {xb} ({med(xb)}) -> {'OK' if ok4 else 'NO'}")
    ok5 = all(all((v or 0) >= 0.90 for v in g('px0', n, 'acc_lenta_f2')) for n in BRAZOS if n != 'SOLO-BOCADOS')
    print(f"  MP-K5 no dana   : acc_lenta_f2 px0 por brazo " + ", ".join(f"{n}={g('px0',n,'acc_lenta_f2')}" for n in BRAZOS) + f" -> {'OK' if ok5 else 'NO'}")
    print(f"  ({round(time.time()-t0,1)} s totales, {sum(len(v) for v in R.values())} corridas de {T} pasos)")
    json.dump({f"{a}|{b}": [{k: v for k, v in x.items() if k not in ('log',)} for x in c] for (a, b), c in R.items()},
              open(os.path.join(AQUI, 'mini_codpred_salida.json'), 'w'), default=str, indent=1)


if __name__ == '__main__':
    main()
