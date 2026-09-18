"""CREADOR A — mini-prueba de UN proceso del mecanismo A-1(ii): seleccion de rasgos conjuntivos por competencia.

Brazos (mundo de regla, T=200000, `constante=True`, `regla_lenta='delta_signo'`, `lam_lenta=0`, `eta_s=0.05`,
`clip_s=10`, `puerta=3`, lectura `cuadratica` salvo que se pida otra):
  SIN      v13q3 sin seleccion (baseline: es el brazo del 3d/3e con el tope subido)
  COND     v13q4 `seleccion='wta'`, `sel_estad='cond'` (media movil del residuo bajo el rasgo)
  COV      v13q4 `seleccion='wta'`, `sel_estad='cov'`  (correlacion acumulada; la de cascade-correlation)
Se mide `acc_lenta` (sonda a priori, formula `signo_acc` del registro), `acc` total, y CUANTAS veces abre el
conjuntivo CORRECTO (indice 6 = P0*P1 en la lectura cuadratica; indice 2 en el oraculo).
Controles en sus propias tandas: `px0` (debe quedar 1.000) y `azar` (debe quedar en [0.35, 0.65]).
Uso: python mini_prueba_A_seleccion.py <SIN|COND|COV> <regla> [lectura] <s1> <s2> <s3>
Sin Pool. Maximo 3 corridas de T=200000 por invocacion.
"""
import sys, os, json, time
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [AQUI, os.path.join(AQUI, '..', 'nivel7_xor_lectura')]
import organismo_v13q3 as ORIG
import organismo_v13q4 as NUEVO

T = 200000
BASE = dict(mundo='regla', constante=True, regla_lenta='delta_signo', lam_lenta=0.0,
            eta_s=0.05, clip_s=10.0, puerta=3)
SEL = dict(seleccion='wta', sel_theta=0.6, sel_rho=0.05, sel_cupo=1, sel_calienta=0)
CORRECTO = {'cuadratica': 6, 'oraculo01': 2}   # indice del rasgo P0*P1 en phi


def signo_acc(Wd, test, vr):
    f = [1.0 if Wd[k] > 0 else (0.5 if Wd[k] == 0 else 0.0) for k in test if vr[k] == 'comida']
    p = [1.0 if Wd[k] < 0 else (0.5 if Wd[k] == 0 else 0.0) for k in test if vr[k] == 'veneno']
    if not f or not p: return None
    return 0.5 * float(np.mean(f)) + 0.5 * float(np.mean(p))


if __name__ == '__main__':
    brazo = sys.argv[1].upper(); regla = sys.argv[2]
    i = 3; lectura = 'cuadratica'
    if sys.argv[3] in ('cuadratica', 'oraculo01', 'oraculo01_ruido', 'random15', 'lineal'):
        lectura = sys.argv[3]; i = 4
    seeds = [int(x) for x in sys.argv[i:]]
    assert len(seeds) <= 3, 'maximo 3 corridas de T=200000 por tanda'
    out = []
    for s in seeds:
        t0 = time.time()
        if brazo == 'SIN':
            r = ORIG.run(s, T=T, regla=regla, lectura=lectura, **BASE)
        else:
            r = NUEVO.run(s, T=T, regla=regla, lectura=lectura, sel_estad=brazo.lower(), **SEL, **BASE)
        _, tren, test, vr = ORIG.split_regla(s, regla)
        a = signo_acc(r['W_apriori'], test, vr); al = signo_acc(r['W_lenta_apriori'], test, vr)
        ab = r.get('sel_abiertos', []); correcto = CORRECTO.get(lectura)
        fila = dict(brazo=brazo, regla=regla, lectura=lectura, seed=s, acc=a, acc_lenta=al,
                    abiertos=ab, abre_correcto=bool(correcto in ab), sel_abre=r.get('sel_abre', []),
                    sel_n=r.get('sel_n'), Ws_apriori=[round(x, 3) for x in r['Ws_apriori']],
                    max_abs_Ws=round(float(np.abs(r['Ws_apriori']).max()), 3),
                    splits=r['splits'], celdas=r['celdas'], deaths=r['deaths'], seg=round(time.time() - t0, 1))
        out.append(fila)
        print(f'  s{s:>3} {brazo:>4} {regla:>6} {lectura:>11} acc_lenta={al}  acc={a}  abiertos={ab} '
              f'{"(CORRECTO)" if fila["abre_correcto"] else ""}  n_mordidas_lenta={fila["sel_n"]}  '
              f'|Ws|max={fila["max_abs_Ws"]}  ({fila["seg"]}s)', flush=True)
    f = os.path.join(AQUI, 'mini_seleccion.json')
    viejo = json.load(open(f)) if os.path.exists(f) else []
    json.dump(viejo + out, open(f, 'w'), indent=1)
    print('->', f)
