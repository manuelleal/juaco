"""Arnes de IDENTIDAD del instrumento de C-P1 (un proceso, sin Pool).

J1  organismo_v13p  con TODAS las perillas apagadas            == organismo_v13     (todas las claves de v13)
J2  organismo_v13p  con las lecturas encendidas, sin usarlas   == organismo_v13     ("solo miden")
J3  organismo_v13p  con el brazo SELF-TEST completo            == organismo_v13s    (continuidad con la mini-prueba)
J4  organismo_v13pg con TODAS las perillas apagadas            == organismo_v13g    (mundo de regla)

Uso:  python experimentos/nivel9_probar_si_mismo/identidad_probar.py [T]
"""
import os, sys, json, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo'), os.path.join(RAIZ, 'experimentos', 'v13_dos_vias'),
                os.path.join(RAIZ, 'experimentos', 'creacion_C')]

import organismo_v13 as V13
import organismo_v13g as V13G
import organismo_v13s as V13S
import organismo_v13p as V13P
import organismo_v13pg as V13PG

ESCENARIOS = [('base', {}), ('invertido', {'invertir_en': None}), ('nuevo_C', {'nuevo': 'C', 'nuevo_en': None})]
SEMILLAS = [1, 2, 3, 4, 5, 6]

APAGADO = dict(eta_b=0.0, k_auto=0.0, k_test=0.0, test_fijo=0.0, eta_e=0.0, eta_pred=0.0, k_testE=0.0, n_traza=0)
SOLO_MIDE = dict(eta_b=0.03, k_auto=0.0, ema_auto=0.05, k_test=0.0, test_fijo=0.0, eta_e=0.05, h_pred=100,
                 eta_pred=0.03, ema_pred=0.05, k_testE=0.0, n_traza=2000)
SELF_TEST = dict(eta_b=0.03, ema_auto=0.05, k_test=10.0, buf_auto=1000, n_traza=2000)


def dif(a, b):
    return [k for k in a if json.dumps(a[k], sort_keys=True, default=str) != json.dumps(b[k], sort_keys=True, default=str)]


def main():
    T = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
    print(f"IDENTIDAD C-P1 — T={T}, semillas {SEMILLAS[0]}-{SEMILLAS[-1]}")
    t0 = time.time()
    tot = {k: [0, 0] for k in ('J1', 'J2', 'J3', 'J4')}

    for nom, kw0 in ESCENARIOS:
        kw = {k: (T // 2 if v is None else v) for k, v in kw0.items()}
        for s in SEMILLAS:
            ref = V13.run(s, T=T, **kw)
            for et, extra in (('J1', APAGADO), ('J2', SOLO_MIDE)):
                got = V13P.run(s, T=T, **kw, **extra)
                d = dif(ref, {k: got[k] for k in ref}); tot[et][1] += 1
                tot[et][0] += not d
                if d:
                    print(f"  DIFIERE {et} {nom} s={s}: {d}")
            a = V13S.run(s, T=T, **kw, **SELF_TEST_v13s())
            b = V13P.run(s, T=T, **kw, **SELF_TEST)
            d = dif(a, {k: b[k] for k in a}); tot['J3'][1] += 1
            tot['J3'][0] += not d
            if d:
                print(f"  DIFIERE J3 {nom} s={s}: {d}")

    for regla in ('px0', 'azar'):
        for s in (1, 2, 3):
            kw = dict(T=T, mundo='regla', regla=regla, eta_s=0.015, puerta=3)
            a = V13G.run(s, **kw)
            b = V13PG.run(s, **kw, **APAGADO)
            d = dif(a, {k: b[k] for k in a}); tot['J4'][1] += 1
            tot['J4'][0] += not d
            if d:
                print(f"  DIFIERE J4 {regla} s={s}: {d}")

    for et in ('J1', 'J2', 'J3', 'J4'):
        ok, n = tot[et]
        print(f"  {et}: {ok}/{n} {'OK' if ok == n else 'FALLA'}")
    print(f"  ({round(time.time()-t0,1)} s)")
    return 0 if all(v[0] == v[1] for v in tot.values()) else 1


def SELF_TEST_v13s():
    """El mismo brazo SELF-TEST, con las perillas que SI existen en organismo_v13s (sin n_traza)."""
    return {k: v for k, v in SELF_TEST.items() if k != 'n_traza'}


if __name__ == '__main__':
    sys.exit(main())
