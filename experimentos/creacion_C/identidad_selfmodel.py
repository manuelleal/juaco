"""Arnes de IDENTIDAD del instrumento de automodelo (creador C).

I1  organismo_v13s.run(eta_b=0,   k_auto=0) == organismo_v13.run(...)   -> el instrumento apagado ES el tronco
I2  organismo_v13s.run(eta_b=0.1, k_auto=0) == organismo_v13.run(...)   -> las tres lecturas SOLO MIDEN

Se comparan TODAS las claves que devuelve el tronco (las claves nuevas quedan fuera por construccion).
Un proceso, sin Pool. Uso:  python experimentos/creacion_C/identidad_selfmodel.py [T]
"""
import os, sys, json, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, 'organismo'))
sys.path.insert(0, AQUI)

import organismo_v13 as V13
import organismo_v13s as V13S

ESCENARIOS = [
    ('base', {}),
    ('invertido', {'invertir_en': 5000}),
    ('nuevo_C', {'nuevo': 'C', 'nuevo_en': 5000}),
]


def igual(a, b):
    ka = sorted(a)
    dif = []
    for k in ka:
        if json.dumps(a[k], sort_keys=True, default=str) != json.dumps(b[k], sort_keys=True, default=str):
            dif.append(k)
    return dif


def main():
    T = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
    semillas = [1, 2, 3, 4, 5, 6]
    print(f"IDENTIDAD automodelo — T={T}, semillas {semillas[0]}-{semillas[-1]}, {len(ESCENARIOS)} escenarios")
    t0 = time.time()
    tot = {'I1': [0, 0], 'I2': [0, 0], 'I3': [0, 0]}
    for nom, kw in ESCENARIOS:
        kw = dict(kw)
        if 'invertir_en' in kw:
            kw['invertir_en'] = T // 2
        if 'nuevo_en' in kw:
            kw['nuevo_en'] = T // 2
        for s in semillas:
            ref = V13.run(s, T=T, **kw)
            for etiq, extra in (('I1', dict(eta_b=0.0, k_auto=0.0)),
                                ('I2', dict(eta_b=0.1, k_auto=0.0)),
                                ('I3', dict(eta_b=0.1, k_auto=0.0, eta_e=0.05, h_pred=100))):
                got = V13S.run(s, T=T, **kw, **extra)
                dif = igual(ref, {k: got[k] for k in ref})
                tot[etiq][1] += 1
                if not dif:
                    tot[etiq][0] += 1
                else:
                    print(f"  DIFIERE {etiq} {nom} s={s}: {dif}")
    for etiq in ('I1', 'I2', 'I3'):
        ok, n = tot[etiq]
        print(f"  {etiq}: {ok}/{n} {'OK' if ok == n else 'FALLA'}")
    print(f"  ({round(time.time()-t0,1)} s)")
    return 0 if all(v[0] == v[1] for v in tot.values()) else 1


if __name__ == '__main__':
    sys.exit(main())
