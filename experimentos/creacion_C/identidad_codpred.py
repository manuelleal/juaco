"""Arnes de IDENTIDAD del instrumento de codificacion predictiva (creador C). Un proceso, sin Pool.

K1  organismo_v14pc con eta_pred=0, eta_c=0, probe_cada=0   == organismo_v14g   (todas las claves de v14g)
K2  organismo_v14pc con eta_pred=0.03 y eta_c=0             == organismo_v14g   (el predictor SOLO MIDE)
K3  organismo_v14pc con probe_cada=2000 y eta_c=0           == organismo_v14g   (la sonda de exposiciones SOLO LEE)

Mundos: 'regla' con px0 / xor01 / azar, y el mundo 'AB' del tronco. Uso:
    python experimentos/creacion_C/identidad_codpred.py [T]
"""
import os, sys, json, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo')]

import organismo_v14g as G
import organismo_v14pc as PC

V14 = dict(eta_s=0.015, puerta=3, mask_rel=2, puerta_pat=5, pat_min=1)
CASOS = {'K1': dict(eta_pred=0.0, eta_c=0.0, probe_cada=0),
         'K2': dict(eta_pred=0.03, eta_c=0.0, probe_cada=0),
         'K3': dict(eta_pred=0.03, eta_c=0.0, probe_cada=2000)}


def dif(a, b):
    return [k for k in a if json.dumps(a[k], default=str, sort_keys=True) != json.dumps(b[k], default=str, sort_keys=True)]


def main():
    T = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
    print(f"IDENTIDAD codificacion predictiva — T={T}, semillas 1-3")
    t0 = time.time()
    tot = {k: [0, 0] for k in CASOS}
    escenarios = [dict(mundo='regla', regla=r, **V14) for r in ('px0', 'xor01', 'azar')] + [dict(**V14)]
    for kw in escenarios:
        nom = kw.get('regla', 'AB')
        for s in (1, 2, 3):
            ref = G.run(s, T=T, **kw)
            for et, extra in CASOS.items():
                got = PC.run(s, T=T, **kw, **extra)
                d = dif(ref, {k: got[k] for k in ref})
                tot[et][1] += 1
                tot[et][0] += not d
                if d:
                    print(f"  DIFIERE {et} {nom} s={s}: {d}")
    for et in CASOS:
        ok, n = tot[et]
        print(f"  {et}: {ok}/{n} {'OK' if ok == n else 'FALLA'}")
    print(f"  ({round(time.time()-t0,1)} s)")
    return 0 if all(v[0] == v[1] for v in tot.values()) else 1


if __name__ == '__main__':
    sys.exit(main())
