"""Arnes de IDENTIDAD del paquete DOSIS (PREREGISTRO_dosis_dE.md, 18 sep 2026): "la sorpresa del mundo en la boca"
(dE-TEST) con ganancia menor -- k_testE en {3, 5} en vez de 10 -- generado por construye_v13E.py --k 3 / --k 5.

Copiado de identidad_v13E.py (mismo patron; B/C/E ahi), pero SOLO para las DOS dosis -- las partes A y D de
identidad_v13E.py (organismo_v13p == organismo_v13, y bateria_generaliza_E.py organismo_v13p 3 == la original) ya
quedaron probadas ahi con el MISMO organismo_v13p.py/organismo_v13pg.py sin tocar; construye_v13E.py --k no los
vuelve a leer de otro sitio, asi que no hace falta repetirlas aqui.

  B_k) organismo_v13E_k{K}  (defecto = dE-TEST fijo a la dosis K)   == organismo_v13p(kwargs dE-TEST, k_testE=K)
                            3 semillas x 3 escenarios, mundo AB, mismas claves exactas
  C_k) organismo_v13gE_k{K} (idem, mundo de regla)                  == organismo_v13pg(kwargs dE-TEST, k_testE=K)
                            3 semillas x 2 reglas, mismas claves exactas
  E_k) organismo_v13E_k{K}(eta_s=0,puerta=None,k_testE=0,eta_pred=0) == organismo/organismo_v11.py
                            -- CRITERIO 5 ADAPTADO (ERR-30, v3'' para organos en la boca), el MISMO parche que
                            bateria_v13E_k{K}.py usa -- 3 semillas, todas las claves de v11

k_testE=0.0 se pasa EXPLICITO en E_k (sobreescribe el default del modulo, sea 3, 5 o 10): por eso la reduccion a
v11 no depende de la dosis, y se prueba para las DOS por separado -- es el patch de CADA bateria_v13E_k{K}.py el
que se esta validando, no uno solo. Para K=10 (organismo_v13E/bateria_v13E) esto ya lo probo identidad_v13E.py
parte E; aqui se repite para K=3 y K=5 porque son instrumentos DISTINTOS (archivos distintos, propio import).

OJO (trampa real, la misma de identidad_v13D.py / identidad_v13E.py): experimentos/v13_dos_vias/ tiene SU PROPIO
organismo_v13.py (88c3574cf9cf38bf), distinto del tronco congelado (cc8b16b492d4d324). `organismo/` va PRIMERO en
sys.path, siempre (ERR-28). Regla: si esto no da 100%, el paquete no corre.

Uso:  python experimentos/nivel9_probar_si_mismo/identidad_dosis.py [T]   (T por defecto 10000, como identidad_v13E.py)
"""
import hashlib, json, os, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo')]

import organismo_v11 as V11   # accesible igual que en organismo/bateria_v13.py (organismo/ primero en sys.path)
import organismo_v13p as V13P
import organismo_v13pg as V13PG
import organismo_v13E_k3 as V13E_K3
import organismo_v13gE_k3 as V13GE_K3
import organismo_v13E_k5 as V13E_K5
import organismo_v13gE_k5 as V13GE_K5

DOSIS = (3, 5)
MODS = {3: (V13E_K3, V13GE_K3), 5: (V13E_K5, V13GE_K5)}
DE_TEST_K = {K: dict(eta_pred=0.03, ema_pred=0.05, k_testE=float(K)) for K in DOSIS}   # BRAZOS['dE3'/'dE5'] de corre_probar_si_mismo.py
CRIT5_OFF = dict(eta_s=0.0, puerta=None, k_testE=0.0, eta_pred=0.0)   # ERR-30: criterio 5 adaptado (v3'' para organos en la boca)
SEMILLAS = (1, 2, 3)


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def N(x):
    return json.loads(json.dumps(x, default=str))


def dif_sub(a, b):
    """Claves de a (el mas chico) que difieren en b; b puede traer claves de mas (se ignoran)."""
    return [k for k in a if N(a[k]) != N(b.get(k, '<falta>'))]


def dif_igual(a, b):
    """a y b deben traer EXACTAMENTE las mismas claves (misma estirpe: incluye faltantes/sobrantes en el reporte)."""
    faltan = sorted(set(a) ^ set(b))
    dif = [k for k in a if k in b and N(a[k]) != N(b[k])]
    return (dif + [f'CLAVES-DISTINTAS:{faltan}']) if faltan else dif


def cmp(nombre, dif, t0):
    ok = not dif
    print(f"  [{time.time()-t0:6.1f}s] {nombre:50s} {'IDENTICO' if ok else 'DIFIERE ' + str(dif[:6])}", flush=True)
    return ok


if __name__ == '__main__':
    t0 = time.time()
    T = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
    for nom, p in [('organismo_v11 (congelado)', os.path.join(RAIZ, 'organismo', 'organismo_v11.py')),
                   ('organismo_v13p (leido, no tocado)', os.path.join(AQUI, 'organismo_v13p.py')),
                   ('organismo_v13pg (leido, no tocado)', os.path.join(AQUI, 'organismo_v13pg.py')),
                   ('organismo_v13E_k3', os.path.join(AQUI, 'organismo_v13E_k3.py')),
                   ('organismo_v13gE_k3', os.path.join(AQUI, 'organismo_v13gE_k3.py')),
                   ('bateria_v13E_k3', os.path.join(AQUI, 'bateria_v13E_k3.py')),
                   ('organismo_v13E_k5', os.path.join(AQUI, 'organismo_v13E_k5.py')),
                   ('organismo_v13gE_k5', os.path.join(AQUI, 'organismo_v13gE_k5.py')),
                   ('bateria_v13E_k5', os.path.join(AQUI, 'bateria_v13E_k5.py')),
                   ('bateria_generaliza_E (extendida con k3/k5)', os.path.join(AQUI, 'bateria_generaliza_E.py')),
                   ('construye_v13E', os.path.join(AQUI, 'construye_v13E.py'))]:
        print(f"  sha {nom:44s} {h16(p)}")
    print(f"  T = {T}")
    ok = tot = 0

    ESCENARIOS = [('base', dict(T=T)), ('inversion en T/2', dict(T=T, invertir_en=T // 2)),
                  ('estimulo nuevo C veneno', dict(T=T, nuevo='C', nuevo_en=T // 2, nuevo_val='veneno'))]

    for K in DOSIS:
        v13E_k, v13gE_k = MODS[K]

        print(f"\nB_{K}) organismo_v13E_k{K} (defecto = dE-TEST ON, k_testE={K}) == organismo_v13p(kwargs dosis k_testE={K})  [mundo AB]")
        for etiq, kw in ESCENARIOS:
            for s in SEMILLAS:
                a = v13E_k.run(s, **kw)                       # ya trae dE-TEST fijo ON a la dosis K por defecto
                b = V13P.run(s, **kw, **DE_TEST_K[K])          # el mismo mecanismo, pedido explicito
                tot += 1; ok += cmp(f"{etiq} s{s}", dif_igual(a, b), t0)

        print(f"\nC_{K}) organismo_v13gE_k{K} (defecto = dE-TEST ON, k_testE={K}) == organismo_v13pg(kwargs dosis k_testE={K})  [mundo de regla]")
        for regla in ('px0', 'azar'):
            for s in SEMILLAS:
                kw = dict(T=T, mundo='regla', regla=regla, eta_s=0.015, puerta=3)
                a = v13gE_k.run(s, **kw)
                b = V13PG.run(s, **kw, **DE_TEST_K[K])
                tot += 1; ok += cmp(f"regla={regla} s{s}", dif_igual(a, b), t0)

        print(f"\nE_{K}) organismo_v13E_k{K}(eta_s=0,puerta=None,k_testE=0,eta_pred=0) == organismo_v11  [ERR-30, todas las claves de v11]")
        for s in SEMILLAS:
            ref = V11.run(s, T=T)
            got = v13E_k.run(s, T=T, **CRIT5_OFF)
            tot += 1; ok += cmp(f"s{s}", dif_sub(ref, got), t0)

    print(f"\nIDENTIDAD {ok}/{tot}  ({time.time()-t0:.1f} s)")
    sys.exit(0 if ok == tot else 1)
