"""Arnes de identidad de experimentos/nivel10_composicion_v14/organismo_v14t.py (COMPOSICION DE TRES: hija dispersa
+ puerta por codigo + "la sorpresa del mundo en la boca", dosis 5). Con las TRES perillas APAGADAS, el instrumento
debe ser organismo_v13 BIT A BIT (regla 2 de EQUIPO.md). Ademas (b)/(c) prueban algo mas fuerte que "no rompe
nada": con SOLO un subconjunto de perillas ON, la composicion debe ser identica al instrumento de ESE subconjunto
YA VALIDADO (organismo_v14c_on para las dos primeras, organismo_v13E_k5 para la sorpresa sola) -- evidencia de que
ninguna interfiere con las otras cuando estan inactivas, semilla a semilla, en TODAS las claves.

  (a) organismo_v14t(apagado)                                    == organismo_v13           (3 semillas x 3 escenarios)
  (b) organismo_v14t(mask_rel=2, puerta_pat=5,pat_min=1)          == organismo_v14c_on        (3 semillas)
  (c) organismo_v14t(eta_pred=0.03,ema_pred=0.05,k_testE=5.0)     == organismo_v13E_k5        (3 semillas)
  (d) organismo_v14t_on(eta_s=0,puerta=None,k_testE=0,eta_pred=0) == organismo_v11            (3 semillas, como identidad_v13E)
      -- CRITERIO 5 del preregistro (ERR-30, v3'' para organos en la boca): mask_rel/puerta_pat NO se apagan aqui
      (organismo_v14t_on los trae ON por defecto) -- es LA MISMA reduccion que usara bateria_v14t.py, asi que esta
      es la prueba de que esa prediccion (estructural para puerta_pat, empirica para mask_rel) se cumple.

Extra, no pedido por nombre pero obligatorio por la regla 2 de EQUIPO.md para CUALQUIER instrumento nuevo:
  (e) organismo_v14gt(apagado)                              == organismo_v13g            (3 semillas, mundo de regla, 2 reglas)
  (f) bateria_generaliza_v14t.py organismo_v14t 3           == bateria_generaliza.py organismo_v13 3   (linea a linea)

OJO (ERR-28): organismo/ va PRIMERO en sys.path, siempre. experimentos/v13_dos_vias/ tiene su PROPIO
organismo_v13.py (88c3574cf9cf38bf), distinto del tronco congelado (cc8b16b492d4d324) -- nunca se importa ese
nombre ambiguo con esa carpeta delante.
Regla: si esto no da 100%, el paquete no corre (ni T1-T4 del preregistro son medibles).
Uso:  python experimentos/nivel10_composicion_v14/identidad_v14t.py
"""
import hashlib, json, os, subprocess, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo'), os.path.join(RAIZ, 'experimentos', 'v13_dos_vias'),
                os.path.join(RAIZ, 'experimentos', 'nivel9_probar_si_mismo')]

import organismo_v11 as V11
import organismo_v13 as V13
import organismo_v13g as V13G
import organismo_v13E_k5 as V13EK5    # dE-TEST dosis 5 (construye_v13E.py --k 5), leido, no tocado
import organismo_v14c_on as V14CON    # composicion de DOS: hija dispersa + puerta por codigo, ya validada (identidad_v14c.py 30/30)
import organismo_v14t as V14T
import organismo_v14t_on as V14TON
import organismo_v14gt as V14GT

NUEVAS_G = {'mundo', 'regla', 'tren', 'test', 'W_apriori', 'codigos_f2', 'primer', 'W_final', 'sonda', 'codigos_fin'}


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def N(x):
    return json.loads(json.dumps(x, default=str))


def dif_sub(a, b):
    """Claves de a (el mas chico/referencia) que difieren en b; b puede traer claves de mas (se ignoran)."""
    return [k for k in a if N(a[k]) != N(b.get(k, '<falta>'))]


def cmp(nombre, dif, t0):
    ok = not dif
    print(f"  [{time.time()-t0:6.1f}s] {nombre:44s} {'IDENTICO' if ok else 'DIFIERE ' + str(dif[:6])}", flush=True)
    return ok


def _sinmod(l, modulo):   # el nombre del modulo aparece en el VEREDICTO: es del arnes, no del instrumento
    return l.replace(modulo, '<MOD>')


if __name__ == '__main__':
    t0 = time.time()
    for nom, p in [('organismo_v13 (congelado)', os.path.join(RAIZ, 'organismo', 'organismo_v13.py')),
                   ('organismo_v11 (congelado)', os.path.join(RAIZ, 'organismo', 'organismo_v11.py')),
                   ('organismo_v13g', os.path.join(RAIZ, 'experimentos', 'v13_dos_vias', 'organismo_v13g.py')),
                   ('organismo_v13E_k5', os.path.join(RAIZ, 'experimentos', 'nivel9_probar_si_mismo', 'organismo_v13E_k5.py')),
                   ('organismo_v14c_on', os.path.join(AQUI, 'organismo_v14c_on.py')),
                   ('construye_v14t.py', os.path.join(AQUI, 'construye_v14t.py')),
                   ('organismo_v14t', os.path.join(AQUI, 'organismo_v14t.py')),
                   ('organismo_v14t_on', os.path.join(AQUI, 'organismo_v14t_on.py')),
                   ('organismo_v14gt', os.path.join(AQUI, 'organismo_v14gt.py')),
                   ('bateria_v14t', os.path.join(AQUI, 'bateria_v14t.py')),
                   ('bateria_generaliza_v14t', os.path.join(AQUI, 'bateria_generaliza_v14t.py'))]:
        print(f"  sha {nom:34s} {h16(p)}")
    print(f"  modulo organismo_v13 importado desde: {V13.__file__}")
    ok = tot = 0

    ESCENARIOS = [('base T=100k', dict()), ('inversion en 50k', dict(invertir_en=50000)),
                  ('estimulo nuevo C veneno', dict(nuevo='C', nuevo_en=50000, nuevo_val='veneno'))]

    print("\n(a) organismo_v14t(apagado) == organismo_v13, todas las claves de v13, 3 escenarios")
    for etiq, kw in ESCENARIOS:
        for s in (1, 2, 3):
            a = V13.run(s, **kw)
            b = V14T.run(s, **kw)
            tot += 1; ok += cmp(f"{etiq} s{s}", dif_sub(a, b), t0)

    print("\n(b) organismo_v14t(mask_rel=2, puerta_pat=5,pat_min=1) == organismo_v14c_on (dos primeras perillas)")
    for s in (1, 2, 3):
        a = V14CON.run(s)
        b = V14T.run(s, mask_rel=2, del_s=0.25, del_c=0.25, ema_c=0.05, puerta_pat=5, pat_shuf=0, pat_min=1)
        tot += 1; ok += cmp(f"s{s}", dif_sub(a, b), t0)

    print("\n(c) organismo_v14t(eta_pred=0.03,ema_pred=0.05,k_testE=5.0) == organismo_v13E_k5 (solo la sorpresa)")
    for s in (1, 2, 3):
        a = V13EK5.run(s)
        b = V14T.run(s, eta_pred=0.03, ema_pred=0.05, k_testE=5.0)
        tot += 1; ok += cmp(f"s{s}", dif_sub(a, b), t0)

    print("\n(d) organismo_v14t_on(eta_s=0,puerta=None,k_testE=0,eta_pred=0) == organismo_v11  [ERR-30, criterio 5 del preregistro]")
    for s in (1, 2, 3):
        a = V11.run(s)
        b = V14TON.run(s, eta_s=0.0, puerta=None, k_testE=0.0, eta_pred=0.0)
        tot += 1; ok += cmp(f"s{s}", dif_sub(a, b), t0)

    print("\n(e) [extra, regla 2] organismo_v14gt(apagado) == organismo_v13g (mundo de regla)")
    for regla in ('px0', 'azar'):
        for s in (1, 2, 3):
            kw = dict(T=60000, mundo='regla', regla=regla, eta_s=0.015, puerta=3)
            a = V13G.run(s, **kw)
            b = V14GT.run(s, **kw)
            tot += 1; ok += cmp(f"regla={regla} s{s}", dif_sub(a, b), t0)

    print("\n(f) [extra, regla 2] bateria_generaliza_v14t(organismo_v14t) == bateria_generaliza(organismo_v13), 3 semillas, linea a linea")
    env = dict(os.environ, PYTHONIOENCODING='utf-8'); sal = {}
    for etiq, script, modulo in [('original', os.path.join(RAIZ, 'organismo', 'bateria_generaliza.py'), 'organismo_v13'),
                                 ('copia v14t', os.path.join(AQUI, 'bateria_generaliza_v14t.py'), 'organismo_v14t')]:
        p = subprocess.run([sys.executable, script, modulo, '3'], capture_output=True, text=True, env=env,
                           cwd=os.path.join(RAIZ, 'organismo'), timeout=3600)
        lin = [l for l in p.stdout.splitlines() if ('PASA' in l or 'FALLA' in l or 'VEREDICTO' in l or 'CONSERVA' in l)]
        sal[etiq] = [_sinmod(l.split('] ', 1)[-1].strip(), modulo) for l in lin]
        print(f"  [{time.time()-t0:6.1f}s] {etiq}: " + " | ".join(sal[etiq][:3]))
        if p.returncode != 0:
            print(f"      *** codigo de salida {p.returncode}\n{p.stderr[-800:]}")
    tot += 1
    igual_bat = sal.get('original') == sal.get('copia v14t')
    ok += igual_bat
    print(f"  [{time.time()-t0:6.1f}s] bateria identica linea a linea: {'SI' if igual_bat else 'NO'}")

    print(f"\nIDENTIDAD {ok}/{tot}  ({time.time()-t0:.1f} s)")
    sys.exit(0 if ok == tot else 1)
