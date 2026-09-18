"""Arnes de identidad de organismo_v14gL.py (sem=0) contra organismo/organismo_v14g.py (1f1318480cd34cde,
CONGELADO). Dos bloques, exactamente como pide el encargo:

  BLOQUE A -- perillas del tronco en su propio default (APAGADAS, como trae organismo_v14g.py): sem=0 debe ser
  organismo_v14g EXACTO en TODAS las claves comunes, en los 3 mundos del mundo de regla (px0, xor01, azar) por
  3 semillas cada uno = 9 casos.

  BLOQUE B -- perillas del tronco ENCENDIDAS (los kwargs de bateria_generaliza.py INSTRUMENTOS['organismo_v14']:
  eta_s=0.015, puerta=3, mask_rel=2, del_s=0.25, del_c=0.25, ema_c=0.05, puerta_pat=5, pat_shuf=0, pat_min=1):
  sem=0 debe seguir siendo organismo_v14g EXACTO con las MISMAS perillas, en los 3 mundos (px0, xor01, azar) a
  1 semilla cada uno = 3 casos (el organo de asociacion no debe cambiar nada cuando esta apagado, este donde este
  el resto del tronco).

Las claves NUEVAS (medida y organo: sem, exp_hasta, n_mord, n_sem, n_des, sem_log, rel_arista, n_nodos) se
excluyen de la comparacion: son anadido, no cambio (mismo criterio que identidad_B4.py de creacion_B). El resto
-- TODAS las demas claves que ya devuelve organismo_v14g.py -- se compara sin excepcion.

T=40000 (fase2_en=20000): pasa de sobra el punto en el que entran los patrones de test (T//2), asi que el bloque
posterior a la sonda a priori tambien queda ejercitado, no solo el arranque.

Uso:  python experimentos/nivel3_asociacion/identidad_v14gL.py
"""
import json, os, sys, time, hashlib
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [os.path.join(RAIZ, 'organismo'), AQUI]   # organismo/ PRIMERO (ERR-28)
import organismo_v14g as ORI
import organismo_v14gL as L

T = 40000
REGLAS = ['px0', 'xor01', 'azar']
TRUNK_ON = dict(eta_s=0.015, puerta=3, mask_rel=2, del_s=0.25, del_c=0.25, ema_c=0.05,
                puerta_pat=5, pat_shuf=0, pat_min=1)   # bateria_generaliza.py INSTRUMENTOS['organismo_v14']

NUEVAS = {'sem', 'exp_hasta', 'n_mord', 'n_sem', 'n_des', 'sem_log', 'rel_arista', 'n_nodos'}


def norm(d):
    return {k: v for k, v in json.loads(json.dumps(d, default=str)).items() if k not in NUEVAS}


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def compara(etiq, kw, seed):
    a = ORI.run(seed, **kw)
    b = L.run(seed, **kw, sem=0)
    na, nb = norm(a), norm(b)
    dif = [k for k in na if na[k] != nb.get(k)]
    claves_nuevas = sorted(k for k in json.loads(json.dumps(b, default=str)) if k not in na)
    return dict(etiq=etiq, seed=seed, identico=not dif, difieren=dif, n_claves=len(na), claves_nuevas=claves_nuevas)


if __name__ == '__main__':
    t0 = time.time()
    print(f"origen  organismo_v14g.py  {h16(ORI.__file__)}  (se esperaba 1f1318480cd34cde)")
    print(f"gemelo  organismo_v14gL.py {h16(L.__file__)}")
    print(f"T={T} (fase2_en={T // 2})  TRUNK_ON={TRUNK_ON}")
    print()

    resA, resB = [], []
    print(f"BLOQUE A -- perillas del tronco APAGADAS (default de organismo_v14g.py): 3 mundos x 3 semillas = 9 casos")
    for regla in REGLAS:
        for s in (1, 2, 3):
            r = compara(f'A mundo={regla}', dict(T=T, mundo='regla', regla=regla), s)
            resA.append(r)
            print(f"  [{time.time() - t0:6.1f}s] {r['etiq']:16s} s{s}  "
                  f"{'IDENTICO' if r['identico'] else 'DIFIERE ' + str(r['difieren'][:6])}  ({r['n_claves']} claves comunes)")

    print()
    print(f"BLOQUE B -- perillas del tronco ENCENDIDAS ({', '.join(f'{k}={v}' for k, v in TRUNK_ON.items())}): "
          f"3 mundos x 1 semilla = 3 casos")
    for regla in REGLAS:
        r = compara(f'B mundo={regla} TRUNK_ON', dict(T=T, mundo='regla', regla=regla, **TRUNK_ON), 1)
        resB.append(r)
        print(f"  [{time.time() - t0:6.1f}s] {r['etiq']:24s} s1  "
              f"{'IDENTICO' if r['identico'] else 'DIFIERE ' + str(r['difieren'][:6])}  ({r['n_claves']} claves comunes)")

    todos = resA + resB
    ok = sum(r['identico'] for r in todos)
    tot = len(todos)
    print()
    print(f"claves nuevas (excluidas de la comparacion, presentes solo en el gemelo): {todos[0]['claves_nuevas']}")
    print(f"IDENTIDAD {ok}/{tot}  (A: {sum(r['identico'] for r in resA)}/{len(resA)}, "
          f"B: {sum(r['identico'] for r in resB)}/{len(resB)})  ({time.time() - t0:.1f} s)")
    sys.exit(0 if ok == tot else 1)
