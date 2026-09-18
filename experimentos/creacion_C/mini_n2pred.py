"""MINI-PRUEBA C-P6 — N2 POR PREDICCION: el receptor aprende QUE VA A SENTIR de la conducta visible del emisor, y con
eso aprende el valor de un objeto SIN morderlo. Un proceso, sin Pool.

Instrumento `experimentos/creacion_C/mundo_social_pred.py` (por anclas desde `mundo_social_n3.py`, ef227f833c5bf46a;
identidades L1/L2/L3 = 21/21 cada una sobre las SIETE condiciones de N3d, semillas 1-3). Montaje de N3d: 4 parejas con
la misma vista para el receptor y valencia opuesta, `regen = 50`, mascaras MR/ME, solo el receptor escucha.

Brazos (T = 100000, semillas 1-3):
  SOLO_R          el receptor ciego, solo con sus mordidas (la linea base: "solo bocados")
  INNATO (=CONV)  N3d tal cual: la conducta ajena se traduce a R = +1 / -3 POR CONSTRUCCION (significado DADO)
  PRED            el nuevo: u[c] aprendido con su propio cuerpo (eta_sym=0.05), gamma_pred = 1/3 = el f_vicaria de N3d
  PRED_SHUF       control: emisor barajado (la conducta no informa)
  PRED_SACIEDAD   control: emisor que no sabe (alpha=0: su conducta no sigue al valor)

PREDICCIONES ESCRITAS ANTES DE CORRER:
  MP-N1 [aprende el significado] u[1] >= +0.5 y u[0] <= -0.15 en 3/3 (los valores del mundo son +0.8 y -0.4).
  MP-N2 [aprende sin morder]     mord_crit(PRED) <= 0.70 x mord_crit(SOLO_R) en 3/3.
  MP-N3 [no peor que el innato]  acierto_q4(PRED) >= 0.75 y >= acierto_q4(INNATO) - 0.10.
  MP-N4 [los controles caen]     SHUF y SACIEDAD: mord_crit >= 0.90 x SOLO_R, y u[1]-u[0] <= 0.3.
  MP-N5 [cuanto cuesta el significado] mord_crit(PRED) >= mord_crit(INNATO). Es el numero que el brazo INNATO no puede
                                 dar: cuantas mordidas cuesta APRENDER el significado que a el se le regala.

Uso:  python experimentos/creacion_C/mini_n2pred.py [T] [n_semillas]
"""
import os, sys, json, time, statistics as st
import numpy as np

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'experimentos', 'etapa5_comunicacion'),
                os.path.join(RAIZ, 'organismo'), os.path.join(RAIZ, 'experimentos', 'v13_dos_vias')]
import mundo_social_pred as PRED
from organismo_v13g import split_regla
from identidad_n2pred import parejas, MR, ME

BASE = dict(mundo='regla', regla='px0', d_senal=5, f_vicaria=1 / 3, regen=50, win_crit=400, crit_rec=0.75)
G = 1 / 3
BRAZOS = {
    'SOLO_R':        dict(n=1, mascaras=[MR]),
    'INNATO(CONV)':  dict(n=2, mascaras=[MR, ME], senal='conducta',
                          kw_por_org=[dict(gamma_soc=1.5), dict(escucha=False)]),
    'PRED':          dict(n=2, mascaras=[MR, ME], senal='conducta',
                          kw_por_org=[dict(gamma_soc=1.5, eta_sym=0.05, gamma_pred=G), dict(escucha=False)]),
    'PRED_SHUF':     dict(n=2, mascaras=[MR, ME], senal='barajada_conducta',
                          kw_por_org=[dict(gamma_soc=1.5, eta_sym=0.05, gamma_pred=G), dict(escucha=False)]),
    'PRED_SACIEDAD': dict(n=2, mascaras=[MR, ME], senal='conducta',
                          kw_por_org=[dict(gamma_soc=1.5, eta_sym=0.05, gamma_pred=G), dict(escucha=False, alpha=0.0)]),
}


def acierto_q4(r, val):   # copiada literal de experimentos/etapa5_comunicacion/corre_N3d.py
    vc = sum(r['vis'][k][3] for k in r['vis'] if val[k] == 'comida'); mc = sum(r['mord'][k][3] for k in r['vis'] if val[k] == 'comida')
    vv = sum(r['vis'][k][3] for k in r['vis'] if val[k] == 'veneno'); mv = sum(r['mord'][k][3] for k in r['vis'] if val[k] == 'veneno')
    partes = ([mc / vc] if vc else []) + ([(vv - mv) / vv] if vv else [])
    return (sum(partes) / len(partes)) if partes else None


def med(xs):
    xs = [x for x in xs if x is not None]
    return st.median(xs) if xs else None


def main():
    T = int(sys.argv[1]) if len(sys.argv) > 1 else 100000
    N = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    print(f"MINI C-P6 — N2 por prediccion. T={T}, semillas 1-{N}, montaje N3d, ventana 400, criterio 0.75")
    print(f"{'brazo':>14} {'sem':>4} | {'acierto_q4':>10} | {'expo_crit':>9} {'mord_crit':>9} | {'expo':>6} {'mord':>6} | {'u[0]':>7} {'u[1]':>7} {'n_u':>10} {'vic':>5} {'s':>5}")
    R = {}
    t0 = time.time()
    for nom, kwb in BRAZOS.items():
        R[nom] = []
        for s in range(1, N + 1):
            _, _, _, val = split_regla(s, 'px0'); val = dict(val)
            t1 = time.time()
            out = PRED.run(s, T=T, tipos_fijos=parejas(s, val), **BASE, **kwb)
            r = out[0]
            R[nom].append(dict(acc=acierto_q4(r, val), expo_crit=r['expo_crit'], mord_crit=r['mord_crit'],
                               expo=r['expo_rec'], mord=r['mord_rec'], u=r['u'], n_u=r['n_u'],
                               vic=r['n_pred_vic'], deaths=r['deaths']))
            x = R[nom][-1]
            print(f"{nom:>14} {s:>4} | {x['acc']:>10.3f} | {str(x['expo_crit']):>9} {str(x['mord_crit']):>9} | "
                  f"{x['expo']:>6} {x['mord']:>6} | {x['u'][0]:>7.3f} {x['u'][1]:>7.3f} {str(x['n_u']):>10} {x['vic']:>5} {time.time()-t1:>5.1f}")

    print("\n=== VEREDICTO (criterios escritos antes) ===")
    def c(nom, k):
        return [x[k] for x in R[nom]]
    base_m = med(c('SOLO_R', 'mord_crit'))
    ok1 = sum(1 for x in R['PRED'] if x['u'][1] >= 0.5 and x['u'][0] <= -0.15)
    print(f"  MP-N1 significado: u de PRED {[x['u'] for x in R['PRED']]} (u[1]>=+0.5, u[0]<=-0.15) -> {ok1}/{N}")
    pm = c('PRED', 'mord_crit')
    ok2 = sum(1 for a, b in zip(pm, c('SOLO_R', 'mord_crit')) if a is not None and b is not None and a <= 0.70 * b)
    print(f"  MP-N2 sin morder : mord_crit PRED {pm} contra SOLO_R {c('SOLO_R','mord_crit')} (<=0.70x) -> {ok2}/{N}   medianas {med(pm)} / {base_m}")
    a_p, a_i = med(c('PRED', 'acc')), med(c('INNATO(CONV)', 'acc'))
    ok3 = (a_p is not None and a_p >= 0.75 and a_i is not None and a_p >= a_i - 0.10)
    print(f"  MP-N3 no peor    : acierto_q4 PRED {round(a_p,3)} (>=0.75) contra INNATO {round(a_i,3)} (-0.10), SOLO_R {round(med(c('SOLO_R','acc')),3)} -> {'OK' if ok3 else 'NO'}")
    for ctl in ('PRED_SHUF', 'PRED_SACIEDAD'):
        du = [round(x['u'][1] - x['u'][0], 3) for x in R[ctl]]
        mc = c(ctl, 'mord_crit')
        ok = sum(1 for a, b in zip(mc, c('SOLO_R', 'mord_crit')) if a is None or b is None or a >= 0.90 * b)
        print(f"  MP-N4 control {ctl:13s}: u[1]-u[0] {du} (<=0.3), mord_crit {mc} (>=0.90x SOLO_R en {ok}/{N}), acierto {round(med(c(ctl,'acc')),3)}")
    im = c('INNATO(CONV)', 'mord_crit')
    ok5 = sum(1 for a, b in zip(pm, im) if a is not None and b is not None and a >= b)
    print(f"  MP-N5 coste del significado: mord_crit PRED {pm} contra INNATO {im} (PRED >= INNATO en {ok5}/{N}); medianas {med(pm)} / {med(im)}")
    print(f"  ({round(time.time()-t0,1)} s, {sum(len(v) for v in R.values())} corridas de {T} pasos)")
    json.dump(R, open(os.path.join(AQUI, 'mini_n2pred_salida.json'), 'w'), default=str, indent=1)


if __name__ == '__main__':
    main()
