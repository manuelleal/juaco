"""Arnes de IDENTIDAD de N2 POR PREDICCION (creador C). Un proceso, sin Pool.

L1  mundo_social_pred con eta_sym=0, gamma_pred=0, theta_a=0           == mundo_social_n3   (todas las claves, los n organismos)
L2  idem + win_crit=400 (la sonda de exposiciones ENCENDIDA)           == mundo_social_n3   (la sonda SOLO LEE)
L3  idem + eta_sym=0.05 (el receptor aprende u[c]) y gamma_pred=0      == mundo_social_n3   (u[c] SOLO MIDE mientras no se use)

Casos (>= 9, como pidio el coordinador): las seis condiciones de N3d — TECHO, SOLO_E, SOLO_R, N0, CONV, SHUF y
SACIEDAD — con el montaje de N3d (4 parejas misma vista / valencia opuesta, regen=50, mascaras), x 3 semillas.

Uso:  python experimentos/creacion_C/identidad_n2pred.py [T]
"""
import os, sys, json, time
import numpy as np

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
COM = os.path.join(RAIZ, 'experimentos', 'etapa5_comunicacion')
sys.path[:0] = [AQUI, COM, os.path.join(RAIZ, 'organismo'), os.path.join(RAIZ, 'experimentos', 'v13_dos_vias')]

import mundo_social_n3 as REF
import mundo_social_pred as PRED
from organismo_v13g import split_regla

MR = [0, 0, 0, 1, 1, 1.]; ME = [1, 1, 1, 0, 0, 0.]
BASE = dict(mundo='regla', regla='px0', d_senal=5, f_vicaria=1 / 3, regen=50)
COND = {
    'TECHO':    dict(n=1),
    'SOLO_E':   dict(n=1, mascaras=[ME]),
    'SOLO_R':   dict(n=1, mascaras=[MR]),
    'N0':       dict(n=2, mascaras=[MR, ME]),
    'CONV':     dict(n=2, mascaras=[MR, ME], senal='conducta', kw_por_org=[dict(gamma_soc=1.5), dict(escucha=False)]),
    'SHUF':     dict(n=2, mascaras=[MR, ME], senal='barajada_conducta', kw_por_org=[dict(gamma_soc=1.5), dict(escucha=False)]),
    'SACIEDAD': dict(n=2, mascaras=[MR, ME], senal='conducta', kw_por_org=[dict(gamma_soc=1.5), dict(escucha=False, alpha=0.0)]),
}
CASOS = {'L1': dict(eta_sym=0.0, gamma_pred=0.0, theta_a=0.0),
         'L2': dict(eta_sym=0.0, gamma_pred=0.0, theta_a=0.0, win_crit=400),
         'L3': dict(eta_sym=0.05, gamma_pred=0.0, theta_a=0.0, win_crit=400)}


def parejas(seed, val):
    """4 parejas con la MISMA vista para el receptor (px 3-5) y valencia opuesta: el montaje de N3d (corre_N3d.py)."""
    r = np.random.default_rng(seed + 800000)
    pats, tren, test, _ = split_regla(seed, 'px0')
    porvista = {}
    for k in pats:
        porvista.setdefault(k[3:], []).append(k)
    tipos = []
    for v, ks in sorted(porvista.items()):
        cand_c = [k for k in ks if val[k] == 'comida']; cand_v = [k for k in ks if val[k] == 'veneno']
        if not (cand_c and cand_v) or len(tipos) >= 8:
            continue
        tipos.append(cand_c[int(r.integers(len(cand_c)))]); tipos.append(cand_v[int(r.integers(len(cand_v)))])
    return tipos


def N(x):
    return json.loads(json.dumps(x, default=str))


def main():
    T = int(sys.argv[1]) if len(sys.argv) > 1 else 30000
    print(f"IDENTIDAD N2 por prediccion — T={T}, semillas 1-3, {len(COND)} condiciones de N3d")
    t0 = time.time()
    tot = {k: [0, 0] for k in CASOS}
    for cond, kwc in COND.items():
        for s in (1, 2, 3):
            _, _, _, val = split_regla(s, 'px0')
            kw = dict(BASE, T=T, tipos_fijos=parejas(s, dict(val)), **kwc)
            a = REF.run(s, **kw)
            for et, extra in CASOS.items():
                b = PRED.run(s, **kw, **extra)
                d = [(j, k) for j in range(len(a)) for k in a[j] if N(a[j][k]) != N(b[j][k])]
                tot[et][1] += 1
                tot[et][0] += not d
                if d:
                    print(f"  DIFIERE {et} {cond} s={s}: {d[:6]}")
    for et in CASOS:
        ok, n = tot[et]
        print(f"  {et}: {ok}/{n} {'OK' if ok == n else 'FALLA'}")
    print(f"  ({round(time.time()-t0,1)} s)")
    return 0 if all(v[0] == v[1] for v in tot.values()) else 1


if __name__ == '__main__':
    sys.exit(main())
