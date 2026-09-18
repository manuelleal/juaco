"""MINI-PRUEBA C1-bis — AUTOMODELO A h PASOS: "cuanta energia voy a ganar / cuantas veces voy a morder en los
proximos h pasos", contra un predictor que solo ve el mundo y contra el mismo con el hambre de OTRA ventana.

UN proceso, sin Pool. Tanda = 3 corridas de 200 000 pasos (semillas 1-3), escenario del bloque 6 (invertir_en = T/2).
Instrumento: experimentos/creacion_C/organismo_v13s.py (por anclas del tronco; identidades I1/I2/I3 18/18 cada una).

Perillas y por que (ninguna buscada):
  eta_e   = 0.05   orden del eta del tronco (0.03); LMS estable porque |x|^2 ~ 4 y 2/|x|^2 = 0.5.
  h_pred  = 100    ~1/3 del intervalo medio entre bocados medido en la tanda 1 (200000/737 = 271 pasos): la ventana
                   contiene 0 o 1 bocado, asi que el objetivo "n_bocados" es casi binario y no se lo come el promedio.
  buf_e   = 200 ventanas (= 20 000 pasos): el control baraja el hambre entre ventanas MUY separadas. Corregido tras el
                   diagnostico de la tanda 1, donde buf_auto = 10 encuentros (~100 pasos) NO decorrelaciona el hambre
                   (el control aprendia Whh = 0.49 en vez de 0) -> candidato a ERR de control demasiado debil.
  eta_b   = 0.03, buf_auto = 1000 encuentros (~10 000 pasos), por la misma razon.

PREDICCIONES ESCRITAS ANTES DE CORRER (objetivo primario = n_bocados; dE se informa pero NO sostiene la afirmacion,
porque parte de su predictibilidad es reversion a la media por el techo E<=1.5 y el reinicio E=0.6 al morir):
  MP-H1  r2(SELF_h) >= 0.10 sobre n_bocados, en 3/3.
  MP-H2  r2(SELF_h) - r2(MUNDO_h) >= 0.05 sobre n_bocados, en 3/3.
  MP-H3  r2(SELF_SHUF_h) <= r2(MUNDO_h) + 0.01 sobre n_bocados, en 3/3  (el control puede fallarlo).
  MP-H4  W_hambre > 0 en los dos objetivos, en 3/3.

Uso:  python experimentos/creacion_C/mini_automodelo_h.py [T] [n_semillas]
"""
import os, sys, json, time, statistics as st

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, 'organismo'))
sys.path.insert(0, AQUI)
import organismo_v13s as V13S

ARM = ['CONST ', 'MUNDO ', 'SELF  ', 'S_SHUF']
OBJ = ['dE      ', 'n_bocados']


def main():
    T = int(sys.argv[1]) if len(sys.argv) > 1 else 200000
    N = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    print(f"MINI C1-bis automodelo a h pasos — T={T}, invertir_en={T//2}, semillas 1-{N}, "
          f"eta_e=0.05 h=100 buf_e=200 | eta_b=0.03 buf_auto=1000")
    filas = []
    t0 = time.time()
    for s in range(1, N + 1):
        t1 = time.time()
        r = V13S.run(s, T=T, invertir_en=T // 2, eta_b=0.03, k_auto=0.0, buf_auto=1000,
                     eta_e=0.05, h_pred=100, buf_e=200)
        filas.append(r)
        h = r['auto_h']
        bo = sum(sum(v) for v in r['mord'].values())
        print(f"\n--- semilla {s}  ({round(time.time()-t1,1)} s)  ventanas={h['n']}  bocados={bo}")
        for y in range(2):
            print(f"    objetivo {OBJ[y]}: media={h['media_y'][y]}  var={h['var_y'][y]}")
            print(f"       mse  {[h['mse'][y][i] for i in range(4)]}")
            print(f"       r2   " + "  ".join(f"{ARM[i]}={h['r2'][y][i]}" for i in range(4)))
        print(f"    W_hambre={h['W_hambre']}   W_hambre_shuf(control)={h['W_hambre_shuf']}")
        print(f"    [encuentro] d_in={round(r['auto_ll'][1][0]-r['auto_ll'][0][0],4)} "
              f"dH_in={round(r['auto_ll'][2][0]-r['auto_ll'][0][0],4)} "
              f"ll[S,M,H,O]_in={[r['auto_ll'][i][0] for i in range(4)]}  Wbh={r['Wbh']} Whh={r['Whh']}")
        print(f"    W={r['W']}  deaths={r['deaths']}")

    print("\n=== VEREDICTO de la mini-prueba (criterios escritos antes; objetivo primario n_bocados) ===")
    r2S = [r['auto_h']['r2'][1][2] for r in filas]
    r2M = [r['auto_h']['r2'][1][1] for r in filas]
    r2Z = [r['auto_h']['r2'][1][3] for r in filas]
    ok1 = sum(1 for x in r2S if x >= 0.10)
    ok2 = sum(1 for a, b in zip(r2S, r2M) if a - b >= 0.05)
    ok3 = sum(1 for z, m in zip(r2Z, r2M) if z <= m + 0.01)
    ok4 = sum(1 for r in filas if all(w > 0 for w in r['auto_h']['W_hambre']))
    print(f"  MP-H1 r2(SELF)   : {r2S} (>=0.10) -> {ok1}/{len(filas)}")
    print(f"  MP-H2 SELF-MUNDO : {[round(a-b,4) for a,b in zip(r2S,r2M)]} (>=0.05) -> {ok2}/{len(filas)}  [MUNDO={r2M}]")
    print(f"  MP-H3 control    : r2(S_SHUF)={r2Z} <= MUNDO+0.01 -> {ok3}/{len(filas)}")
    print(f"  MP-H4 signo      : W_hambre={[r['auto_h']['W_hambre'] for r in filas]} -> {ok4}/{len(filas)}")
    print(f"  (informativo, NO sostiene nada) dE: r2 SELF={[r['auto_h']['r2'][0][2] for r in filas]} "
          f"MUNDO={[r['auto_h']['r2'][0][1] for r in filas]} S_SHUF={[r['auto_h']['r2'][0][3] for r in filas]}")
    print(f"  medianas: r2_SELF={round(st.median(r2S),4)}  r2_MUNDO={round(st.median(r2M),4)}  r2_SHUF={round(st.median(r2Z),4)}")
    print(f"  ({round(time.time()-t0,1)} s totales)")
    out = os.path.join(AQUI, 'mini_automodelo_h_salida.json')
    json.dump([{k: v for k, v in r.items() if k != 'log'} for r in filas], open(out, 'w'), default=str, indent=1)
    print(f"  json: {out}")


if __name__ == '__main__':
    main()
