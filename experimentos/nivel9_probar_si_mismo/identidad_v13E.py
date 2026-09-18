"""Arnes de IDENTIDAD del paquete v13E ("la sorpresa del mundo en la boca", dE-TEST -- PROPUESTA_v14.md, segundo
candidato; REGISTRO_etapas_1_2.md "Bloque C-P1" -- como candidato a organo del TRONCO):

  A) organismo_v13p  (perillas en su propio default = apagadas)         == organismo/organismo_v13.py
                      3 semillas x 3 escenarios, TODAS las claves de v13 (cc8b16b492d4d324)
  B) organismo_v13E  (defecto = dE-TEST fijo ON)                        == organismo_v13p(kwargs del brazo dE-TEST)
                      3 semillas x 3 escenarios, mundo AB, mismas claves exactas
  C) organismo_v13gE (defecto = dE-TEST fijo ON, mundo de regla)        == organismo_v13pg(kwargs del brazo dE-TEST)
                      3 semillas x 2 reglas, mismas claves exactas
  D) bateria_generaliza_E.py organismo_v13p 3  ==  organismo/bateria_generaliza.py organismo_v13 3   (linea a linea)
  E) organismo_v13E(eta_s=0,puerta=None,k_testE=0,eta_pred=0)           == organismo/organismo_v11.py
                      -- CRITERIO 5 ADAPTADO (ERR-30, v3'' para organos en la boca) -- 3 semillas, todas las claves de v11

A confirma la base sobre la que construye este paquete (ya la prueba identidad_probar.py; se repite aqui porque
es el punto de partida de construye_v13E.py). B y C confirman que ESTE constructor no rompio nada al fijar tres
defaults (eta_pred=0.03, ema_pred=0.05, k_testE=10.0 -- BRAZOS['dE-TEST'] de corre_probar_si_mismo.py). NINGUNA
de B/C/D prueba que la perilla ON sea inerte -- a diferencia de la hija dispersa (nivel7_hija_dispersa), aqui NO
se espera inercia: es el mecanismo activo cuya aceleracion de la recuperacion ya se midio en 41-60, 61-80 y
81-100. Ver PREREGISTRO_v13E.md.

E prueba el PARCHE ERR-30 que construye_v13E.py aplico a bateria_v13E.py (criterio 5 adaptado): apagar SOLO
eta_s/puerta no alcanza para reducir v13E a v11 (k_testE actua en la BOCA sin pasar por ninguna de las dos); con
las CUATRO perillas apagadas (eta_s, puerta, k_testE, eta_pred) si debe serlo, bit a bit. Si E falla, el parche
de bateria_v13E.py esta mal y su criterio 5 no mide nada -- ver PREREGISTRO_v13E.md, seccion "Criterio 5 adaptado
(v3'' para organos en la boca)".

OJO (trampa real, la misma de identidad_v13D.py): experimentos/v13_dos_vias/ tiene SU PROPIO organismo_v13.py
(88c3574cf9cf38bf), distinto del tronco congelado (cc8b16b492d4d324). `organismo/` va PRIMERO en sys.path,
siempre (ERR-28). Regla: si esto no da 100%, el paquete no corre.

Uso:  python experimentos/nivel9_probar_si_mismo/identidad_v13E.py [T]   (T por defecto 10000, como identidad_probar.py)
"""
import hashlib, json, os, subprocess, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo')]

import organismo_v13 as V13
import organismo_v11 as V11   # accesible igual que en organismo/bateria_v13.py (organismo/ primero en sys.path)
import organismo_v13p as V13P
import organismo_v13pg as V13PG
import organismo_v13E as V13E
import organismo_v13gE as V13GE

DE_TEST = dict(eta_pred=0.03, ema_pred=0.05, k_testE=10.0)   # BRAZOS['dE-TEST'] de corre_probar_si_mismo.py (K_TEST=10.0)
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
    print(f"  [{time.time()-t0:6.1f}s] {nombre:44s} {'IDENTICO' if ok else 'DIFIERE ' + str(dif[:6])}", flush=True)
    return ok


if __name__ == '__main__':
    t0 = time.time()
    T = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
    for nom, p in [('organismo_v13 (congelado)', os.path.join(RAIZ, 'organismo', 'organismo_v13.py')),
                   ('organismo_v11 (congelado)', os.path.join(RAIZ, 'organismo', 'organismo_v11.py')),
                   ('organismo_v13p (leido, no tocado)', os.path.join(AQUI, 'organismo_v13p.py')),
                   ('organismo_v13pg (leido, no tocado)', os.path.join(AQUI, 'organismo_v13pg.py')),
                   ('organismo_v13E', os.path.join(AQUI, 'organismo_v13E.py')),
                   ('organismo_v13gE', os.path.join(AQUI, 'organismo_v13gE.py')),
                   ('bateria_v13E', os.path.join(AQUI, 'bateria_v13E.py')),
                   ('bateria_generaliza_E', os.path.join(AQUI, 'bateria_generaliza_E.py')),
                   ('bateria_v13 (congelada)', os.path.join(RAIZ, 'organismo', 'bateria_v13.py')),
                   ('bateria_generaliza (original)', os.path.join(RAIZ, 'organismo', 'bateria_generaliza.py'))]:
        print(f"  sha {nom:34s} {h16(p)}")
    print(f"  modulo organismo_v13 importado desde: {V13.__file__}")
    print(f"  T = {T}")
    ok = tot = 0

    ESCENARIOS = [('base', dict(T=T)), ('inversion en T/2', dict(T=T, invertir_en=T // 2)),
                  ('estimulo nuevo C veneno', dict(T=T, nuevo='C', nuevo_en=T // 2, nuevo_val='veneno'))]

    print("\nA) organismo_v13p (perillas en su default = apagadas) == organismo_v13  [todas las claves de v13]")
    for etiq, kw in ESCENARIOS:
        for s in SEMILLAS:
            ref = V13.run(s, **kw)
            got = V13P.run(s, **kw)
            tot += 1; ok += cmp(f"{etiq} s{s}", dif_sub(ref, got), t0)

    print("\nB) organismo_v13E (defecto = dE-TEST ON) == organismo_v13p(kwargs del brazo dE-TEST)  [mundo AB]")
    for etiq, kw in ESCENARIOS:
        for s in SEMILLAS:
            a = V13E.run(s, **kw)              # ya trae dE-TEST fijo ON por defecto
            b = V13P.run(s, **kw, **DE_TEST)    # el mismo mecanismo, pedido explicito
            tot += 1; ok += cmp(f"{etiq} s{s}", dif_igual(a, b), t0)

    print("\nC) organismo_v13gE (defecto = dE-TEST ON) == organismo_v13pg(kwargs del brazo dE-TEST)  [mundo de regla]")
    for regla in ('px0', 'azar'):
        for s in SEMILLAS:
            kw = dict(T=T, mundo='regla', regla=regla, eta_s=0.015, puerta=3)
            a = V13GE.run(s, **kw)
            b = V13PG.run(s, **kw, **DE_TEST)
            tot += 1; ok += cmp(f"regla={regla} s{s}", dif_igual(a, b), t0)

    print("\nD) bateria_generaliza_E.py organismo_v13p 3  ==  bateria_generaliza.py organismo_v13 3  (linea a linea)")
    env = dict(os.environ, PYTHONIOENCODING='utf-8'); sal = {}
    for etiq, script, modulo in [('original', os.path.join(RAIZ, 'organismo', 'bateria_generaliza.py'), 'organismo_v13'),
                                 ('copia E ', os.path.join(AQUI, 'bateria_generaliza_E.py'), 'organismo_v13p')]:
        p = subprocess.run([sys.executable, script, modulo, '3'], capture_output=True, text=True, env=env,
                           cwd=os.path.join(RAIZ, 'organismo'), timeout=3600)
        sal[etiq] = [l.split('] ', 1)[-1].strip().replace(modulo, '<MOD>') for l in p.stdout.splitlines()
                     if ('PASA' in l or 'FALLA' in l or 'VEREDICTO' in l or 'CONSERVA' in l)]
        print(f"  [{time.time()-t0:6.1f}s] {etiq}: " + " | ".join(sal[etiq][:2]))
        if p.returncode != 0:
            print(f"      *** codigo de salida {p.returncode}\n{p.stderr[-600:]}")
    tot += 1; igual = sal.get('original') == sal.get('copia E ')
    ok += igual
    print(f"  [{time.time()-t0:6.1f}s] bateria identica: {'SI' if igual else 'NO'}")

    print("\nE) organismo_v13E(eta_s=0,puerta=None,k_testE=0,eta_pred=0) == organismo_v11  [ERR-30, todas las claves de v11]")
    for s in SEMILLAS:
        ref = V11.run(s, T=T)
        got = V13E.run(s, T=T, **CRIT5_OFF)
        tot += 1; ok += cmp(f"s{s}", dif_sub(ref, got), t0)

    print(f"\nIDENTIDAD {ok}/{tot}  ({time.time()-t0:.1f} s)")
    sys.exit(0 if ok == tot else 1)
