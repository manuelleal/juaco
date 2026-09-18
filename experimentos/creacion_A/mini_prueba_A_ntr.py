"""CREADOR A — mini-prueba A-6: la TRANSICION del tamano del tren dentro del organismo.

Por que (medido, ver PREREGISTRO_xor_6.md §1): con la particion de hoy (4 comida + 4 veneno = 8 patrones) el
estadistico IDEAL de seleccion — el residuo del ajuste elemental EXACTO, que ninguna regla local puede superar —
pone `P0*P1` en primer lugar solo en 3/20 semillas. La transicion medida fuera del organismo es brusca: a
8c+6v = 14 patrones pasa a 12/20 y el acierto, si se abre el ganador, salta de 0.625 a 1.000. Aqui se comprueba
DENTRO del organismo, con la regla local y las constantes de A-4 (eta_s=0.15, clip_s=10).

Uso: python mini_prueba_A_ntr.py <ntr|base> <s1> ... (maximo 6 corridas por invocacion)
Sin Pool. `ntr` no esta en el gemelo compilado: este brazo va interpretado (declarado).
"""
import sys, os, json, time
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [AQUI, os.path.join(AQUI, '..', 'nivel7_xor_lectura')]
import organismo_v13q6 as Q

T = 100000
BASE = dict(mundo='regla', regla='xor01', lectura='cuadratica', constante=True, regla_lenta='delta_signo',
            lam_lenta=0.0, eta_s=0.15, clip_s=10.0, puerta=3, lab=True,
            seleccion='wta', sel_theta=0.3, sel_rho=0.02, sel_cupo=1, sel_estad='cond')
IDX = 6   # P0*P1 en la lectura cuadratica


def signo_acc(Wd, test, vr):
    f = [1.0 if Wd[k] > 0 else (0.5 if Wd[k] == 0 else 0.0) for k in test if vr[k] == 'comida']
    p = [1.0 if Wd[k] < 0 else (0.5 if Wd[k] == 0 else 0.0) for k in test if vr[k] == 'veneno']
    if not f or not p: return None
    return 0.5 * float(np.mean(f)) + 0.5 * float(np.mean(p))


if __name__ == '__main__':
    arg = sys.argv[1]
    ntr = None if arg == 'base' else tuple(int(x) for x in arg.split(','))
    seeds = [int(x) for x in sys.argv[2:]]
    assert len(seeds) <= 6, 'maximo 6 corridas por invocacion (EQUIPO regla 3)'
    out = []
    for s in seeds:
        t0 = time.time()
        r = Q.run(s, T=T, ntr=ntr, **BASE)
        pats, tren, test, vr = Q.split_regla(s, 'xor01', ntr)
        al = signo_acc(r['W_lenta_apriori'], test, vr)
        npre = len([e for e in r['lenta_eventos'] if e[0] < r['fase2_en']])
        cls = {}
        for e in r['lenta_eventos']:
            if e[0] < r['fase2_en']: cls[e[1][:2]] = cls.get(e[1][:2], 0) + 1
        ab = r.get('sel_abiertos') or []
        fila = dict(ntr=arg, seed=s, n_tren=len(tren), n_test=len(test), acc_lenta=al,
                    acc=signo_acc(r['W_apriori'], test, vr), abre_prod=bool(IDX in ab), abiertos=[int(x) for x in ab],
                    n_pre=npre, clases_pre=cls, clases_sin_morder=4 - len(cls), seg=round(time.time() - t0, 1))
        out.append(fila)
        print(f'  s{s:>3} ntr={arg:>5} tren={len(tren):>2}/test={len(test):>2}  acc_lenta={al}  acc={fila["acc"]}  '
              f'abre P0*P1={"SI" if fila["abre_prod"] else "no"}  eventos={npre}  '
              f'clases sin morder={fila["clases_sin_morder"]}  ({fila["seg"]}s)', flush=True)
    f = os.path.join(AQUI, 'mini_ntr.json')
    viejo = json.load(open(f)) if os.path.exists(f) else []
    json.dump(viejo + out, open(f, 'w'), indent=1)
    v = [x['acc_lenta'] for x in out if x['acc_lenta'] is not None]
    print(f'  mediana acc_lenta {np.median(v):.3f}   abre P0*P1 {sum(x["abre_prod"] for x in out)}/{len(out)}')
    print('->', f)
