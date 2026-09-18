"""MINI-PRUEBA C1 — AUTOMODELO: la sorpresa sobre SI MISMO, y la banda que la distingue de un predictor del mundo.

UN proceso, sin Pool. Tanda = 3 corridas de 200 000 pasos (semillas 1-3), escenario del bloque 6 (invertir_en = T/2).
Instrumento: experimentos/creacion_C/organismo_v13s.py (por anclas desde el tronco; identidades I1/I2 18/18).
Perillas: eta_b = 0.03 = EL MISMO eta del tronco (no se busco), k_auto = 0 (las lecturas SOLO MIDEN: conducta = v13
bit a bit por I2). buf_auto = 10 (la ventana del control, como el buf_sorpresa del bloque 6 tras su enmienda 2).

PREDICCIONES ESCRITAS ANTES DE CORRER (no se recalibran; si fallan, se registra el fallo):
  MP-1 [la banda]      ll(MUNDO) - ll(SELF) >= 0.05 nats/encuentro DENTRO de la banda  y  <= 0.01 FUERA, en 3/3.
  MP-2 [el control]    ll(H_SHUF) >= ll(SELF) dentro de la banda en 3/3: el hambre BARAJADA no compra nada.
  MP-3 [el peso]       Wbh >= 0.30  y  |Whh| <= 0.3*Wbh  en 3/3.
  MP-4 [el techo]      ll(ORACULO) <= ll(SELF) <= ll(MUNDO) dentro de la banda en 3/3 (el oraculo es cota inferior).
  MP-5 [la densidad]   encuentros >= 5 x bocados: el automodelo aprende de CADA encuentro; el predictor de dE (bloque 6)
                       solo de los bocados.
  MP-6 [la sorpresa]   sorpresa_auto sube del cuarto Q2 al Q3 (la inversion) en 3/3.

Uso:  python experimentos/creacion_C/mini_automodelo.py [T] [n_semillas]
"""
import os, sys, json, time, statistics as st

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, 'organismo'))
sys.path.insert(0, AQUI)
import organismo_v13s as V13S

NOM = ['SELF  ', 'MUNDO ', 'H_SHUF', 'ORACUL']


def main():
    T = int(sys.argv[1]) if len(sys.argv) > 1 else 200000
    N = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    print(f"MINI C1 automodelo — T={T}, invertir_en={T//2}, semillas 1-{N}, eta_b=0.03, k_auto=0")
    filas = []
    t0 = time.time()
    for s in range(1, N + 1):
        t1 = time.time()
        r = V13S.run(s, T=T, invertir_en=T // 2, eta_b=0.03, k_auto=0.0)
        filas.append(r)
        bo = sum(sum(v) for v in r['mord'].values()); en = sum(r['encuentros'])
        print(f"\n--- semilla {s}  ({round(time.time()-t1,1)} s)  banda={r['auto_banda']}  "
              f"encuentros={en} bocados={bo}  razon={round(en/max(bo,1),2)}")
        print(f"    n por banda [no muerde, muerde]: dentro={r['auto_n'][0]}  fuera={r['auto_n'][1]}")
        print("    lectura          ll_dentro  ll_fuera  ba_dentro  ba_fuera")
        for i in range(4):
            ll, ba = r['auto_ll'][i], r['auto_ba'][i]
            print(f"    {NOM[i]}          {ll[0]}     {ll[1]}     {ba[0]}      {ba[1]}")
        print(f"    Wbh={r['Wbh']}  Whh={r['Whh']}  Wb0={r['Wb0']}  Wm0={r['Wm0']}")
        print(f"    sorpresa_auto por cuarto={r['sorpresa_auto']}  encuentros={r['encuentros']}")
        print(f"    W={r['W']}  deaths={r['deaths']}  celdas={r['celdas']}  splits={r['splits']}")

    print("\n=== VEREDICTO de la mini-prueba (criterios escritos antes) ===")
    def g(k, f):
        return [f(r) for r in filas]
    d_in = g(None, lambda r: r['auto_ll'][1][0] - r['auto_ll'][0][0])
    d_out = g(None, lambda r: r['auto_ll'][1][1] - r['auto_ll'][0][1])
    h_in = g(None, lambda r: r['auto_ll'][2][0] - r['auto_ll'][0][0])
    ok1 = sum(1 for a, b in zip(d_in, d_out) if a >= 0.05 and b <= 0.01)
    ok2 = sum(1 for a in h_in if a >= 0)
    ok3 = sum(1 for r in filas if r['Wbh'] >= 0.30 and abs(r['Whh']) <= 0.3 * r['Wbh'])
    ok4 = sum(1 for r in filas if r['auto_ll'][3][0] <= r['auto_ll'][0][0] <= r['auto_ll'][1][0])
    ok5 = sum(1 for r in filas if sum(r['encuentros']) >= 5 * sum(sum(v) for v in r['mord'].values()))
    ok6 = sum(1 for r in filas if (r['sorpresa_auto'][2] or 0) > (r['sorpresa_auto'][1] or 0))
    print(f"  MP-1 banda    : dentro {[round(x,4) for x in d_in]} (>=0.05) | fuera {[round(x,4) for x in d_out]} (<=0.01) -> {ok1}/{len(filas)}")
    print(f"  MP-2 control  : ll(H_SHUF)-ll(SELF) dentro {[round(x,4) for x in h_in]} (>=0) -> {ok2}/{len(filas)}")
    print(f"  MP-3 peso     : Wbh {[r['Wbh'] for r in filas]}  Whh {[r['Whh'] for r in filas]} -> {ok3}/{len(filas)}")
    print(f"  MP-4 techo    : ORACULO <= SELF <= MUNDO dentro -> {ok4}/{len(filas)}")
    print(f"  MP-5 densidad : razon encuentros/bocados {[round(sum(r['encuentros'])/max(sum(sum(v) for v in r['mord'].values()),1),2) for r in filas]} -> {ok5}/{len(filas)}")
    print(f"  MP-6 sorpresa : Q2->Q3 {[(r['sorpresa_auto'][1], r['sorpresa_auto'][2]) for r in filas]} -> {ok6}/{len(filas)}")
    print(f"  medianas: d_in={round(st.median(d_in),4)}  d_out={round(st.median(d_out),4)}  "
          f"ll_SELF_in={round(st.median([r['auto_ll'][0][0] for r in filas]),4)}  "
          f"ll_ORACULO_in={round(st.median([r['auto_ll'][3][0] for r in filas]),4)}")
    print(f"  ({round(time.time()-t0,1)} s totales)")
    out = os.path.join(AQUI, 'mini_automodelo_salida.json')
    json.dump([{k: v for k, v in r.items() if k != 'log'} for r in filas], open(out, 'w'), default=str, indent=1)
    print(f"  json: {out}")


if __name__ == '__main__':
    main()
