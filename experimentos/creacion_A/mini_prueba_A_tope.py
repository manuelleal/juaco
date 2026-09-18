"""CREADOR A — mini-prueba de UN proceso: el TOPE `clip_s` como causa del 0.625 del bloque 3e.

Hallazgo del banco: sobre los rasgos del oraculo {P0,P1,P0P1,1} la solucion de xor01 es UNICA y vale
    y = -3 + 4*P0 + 4*P1 - 8*P0*P1     ->    |w| llega a 8
y el tronco tiene `clip_s = 3.0`. Con clip_s=3 la regla delta se queda pegada al tope (|w|max = 3.00 exacto,
residuo 1.8-2.0) y satura en 0.625 PARA SIEMPRE (n = 5000 actualizaciones no ayuda, eta tampoco): es exactamente
el 0.625 que midio 3e. Con clip_s >= 10 la misma regla, mismos rasgos, mismo eta, llega a 1.000 con residuo 0.000
y pesos (3.99, 4.00, -7.99, -3.00). En cambio con la lectura CUADRATICA subir el tope no cambia NADA (0.562 con
clip_s = 3, 10, 30 y 100): alli el cuello es la seleccion de rasgos, no el tope. Las dos cosas son independientes.

Esta mini-prueba lo comprueba EN EL ORGANISMO con el instrumento que ya existe (`organismo_v13q3.py`,
`aaebe073308a40c2`, el de 3e): `clip_s` ya es parametro, no hace falta instrumento nuevo ni tocar nada.
Brazos: oraculo01 + constante + delta con signo, `clip_s` = 3 (como 3e) contra 30, mismo `eta_s`.
Controles en la misma tanda: px0 (debe seguir en 1.000) y la lectura cuadratica con clip_s=30 (NO debe subir).
Uso:  python mini_prueba_A_tope.py <clip_s> <eta_s> <regla> <lectura> <s1> <s2> <s3>
Sin Pool. Maximo 3 corridas por invocacion.
"""
import sys, os, json, time
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
XOR = os.path.join(AQUI, '..', 'nivel7_xor_lectura')
sys.path[:0] = [AQUI, XOR]
import organismo_v13q3 as Q   # original de 3e, NO se toca


def signo_acc(Wd, test, vr):
    f = [1.0 if Wd[k] > 0 else (0.5 if Wd[k] == 0 else 0.0) for k in test if vr[k] == 'comida']
    p = [1.0 if Wd[k] < 0 else (0.5 if Wd[k] == 0 else 0.0) for k in test if vr[k] == 'veneno']
    if not f or not p: return None
    return 0.5 * float(np.mean(f)) + 0.5 * float(np.mean(p))


if __name__ == '__main__':
    clip_s = float(sys.argv[1]); eta_s = float(sys.argv[2]); regla = sys.argv[3]; lectura = sys.argv[4]
    seeds = [int(x) for x in sys.argv[5:]]
    assert len(seeds) <= 3, 'maximo 3 corridas por tanda'
    T = 200000
    out = []
    for s in seeds:
        t0 = time.time()
        r = Q.run(s, T=T, mundo='regla', regla=regla, lectura=lectura, constante=True,
                  regla_lenta='delta_signo', lam_lenta=0.0, eta_s=eta_s, clip_s=clip_s, puerta=3)
        _, tren, test, vr = Q.split_regla(s, regla)
        a = signo_acc(r['W_apriori'], test, vr); al = signo_acc(r['W_lenta_apriori'], test, vr)
        Wsa = r['Ws_apriori']
        fila = dict(seed=s, clip_s=clip_s, eta_s=eta_s, regla=regla, lectura=lectura, acc=a, acc_lenta=al,
                    Ws_apriori=[round(x, 3) for x in Wsa], max_abs_Ws=round(float(np.abs(Wsa).max()), 3),
                    pegado_al_tope=bool(np.abs(Wsa).max() >= clip_s - 1e-9),
                    splits=r['splits'], celdas=r['celdas'], deaths=r['deaths'], seg=round(time.time() - t0, 1))
        out.append(fila)
        print(f'  s{s:>2} {lectura:>10} {regla:>6} clip_s={clip_s:<5} eta_s={eta_s:<6} acc_lenta={al}  acc={a}  '
              f'Ws={fila["Ws_apriori"]}  |Ws|max={fila["max_abs_Ws"]}  tope={"SI" if fila["pegado_al_tope"] else "no"}  '
              f'({fila["seg"]}s)', flush=True)
    f = os.path.join(AQUI, 'mini_tope.json')
    viejo = json.load(open(f)) if os.path.exists(f) else []
    json.dump(viejo + out, open(f, 'w'), indent=1)
    print('->', f)
