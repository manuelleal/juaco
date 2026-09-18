"""Arnes de identidad del paquete v13D (hija dispersa sobre el tronco). Con la perilla APAGADA (mask_rel=0) los
dos organismos deben ser sus originales BIT A BIT, todas las claves:

  A) organismo_v13D  == organismo/organismo_v13.py                  (cc8b16b492d4d324)  3 semillas x 3 escenarios
  B) organismo_v13gD == experimentos/v13_dos_vias/organismo_v13g.py (2a80e125f8593bf2)  3 semillas x 2 reglas
  C) bateria_generaliza_D.py organismo_v13D 3  ==  organismo/bateria_generaliza.py organismo_v13 3

OJO (trampa real): experimentos/v13_dos_vias/ tiene SU PROPIO organismo_v13.py (88c3574cf9cf38bf), distinto del
tronco congelado. `organismo/` va PRIMERO en sys.path, siempre.
Regla: si esto no da 100 %, el paquete no corre.
Uso:  python experimentos/nivel7_hija_dispersa/identidad_v13D.py
"""
import json, os, subprocess, sys, time, hashlib

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo'), os.path.join(RAIZ, 'experimentos', 'v13_dos_vias')]

import organismo_v13 as V13
import organismo_v13D as V13D
import organismo_v13g as V13G
import organismo_v13gD as V13GD

NUEVAS = {'mask_rel', 'del_s', 'del_c', 'ema_c'}
APAG = dict(mask_rel=0)


def norm(d):
    return json.loads(json.dumps({k: v for k, v in d.items() if k not in NUEVAS}, default=str))


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def _sinmod(l, modulo):   # el nombre del modulo aparece en el VEREDICTO: es del arnes, no del instrumento
    return l.replace(modulo, '<MOD>')


def cmp(a, b, etiq, t0):
    a, b = norm(a), norm(b)
    dif = [k for k in a if a[k] != b.get(k)]
    print(f"  [{time.time()-t0:6.1f}s] {etiq:44s} {'IDENTICO' if not dif else 'DIFIERE ' + str(dif[:6])}", flush=True)
    return not dif


if __name__ == '__main__':
    t0 = time.time()
    for nom, p in [('organismo_v13 (congelado)', os.path.join(RAIZ, 'organismo', 'organismo_v13.py')),
                   ('organismo_v13D', os.path.join(AQUI, 'organismo_v13D.py')),
                   ('organismo_v13Don', os.path.join(AQUI, 'organismo_v13Don.py')),
                   ('organismo_v13g', os.path.join(RAIZ, 'experimentos', 'v13_dos_vias', 'organismo_v13g.py')),
                   ('organismo_v13gD', os.path.join(AQUI, 'organismo_v13gD.py')),
                   ('bateria_v13 (congelada)', os.path.join(RAIZ, 'organismo', 'bateria_v13.py')),
                   ('bateria_v13D', os.path.join(AQUI, 'bateria_v13D.py')),
                   ('bateria_generaliza (original)', os.path.join(RAIZ, 'organismo', 'bateria_generaliza.py')),
                   ('bateria_generaliza_D', os.path.join(AQUI, 'bateria_generaliza_D.py'))]:
        print(f"  sha {nom:34s} {h16(p)}")
    print(f"  modulo organismo_v13 importado desde: {V13.__file__}")
    ok = tot = 0

    print("\nA) organismo_v13D == organismo_v13 (perilla apagada)")
    for etiq, kw in [('base T=100k', dict()), ('inversion en 50k', dict(invertir_en=50000)),
                     ('estimulo nuevo C veneno', dict(nuevo='C', nuevo_en=50000, nuevo_val='veneno'))]:
        for s in (1, 2, 3):
            tot += 1; ok += cmp(V13.run(s, **kw), V13D.run(s, **kw, **APAG), f"{etiq} s{s}", t0)

    print("\nB) organismo_v13gD == organismo_v13g (mundo de regla, perilla apagada)")
    for regla in ('px0', 'azar'):
        for s in (1, 2, 3):
            kw = dict(T=60000, mundo='regla', regla=regla, eta_s=0.015, puerta=3)
            tot += 1; ok += cmp(V13G.run(s, **kw), V13GD.run(s, **kw, **APAG), f"regla={regla} T=60k s{s}", t0)

    print("\nC) bateria_generaliza_D(organismo_v13D) == bateria_generaliza(organismo_v13), 3 semillas")
    env = dict(os.environ, PYTHONIOENCODING='utf-8'); sal = {}
    for etiq, script, modulo in [('original', os.path.join(RAIZ, 'organismo', 'bateria_generaliza.py'), 'organismo_v13'),
                                 ('copia D ', os.path.join(AQUI, 'bateria_generaliza_D.py'), 'organismo_v13D')]:
        p = subprocess.run([sys.executable, script, modulo, '3'], capture_output=True, text=True, env=env,
                           cwd=os.path.join(RAIZ, 'organismo'), timeout=3600)
        sal[etiq] = [_sinmod(l.split('] ', 1)[-1].strip(), modulo) for l in p.stdout.splitlines()
                     if ('PASA' in l or 'FALLA' in l or 'VEREDICTO' in l or 'CONSERVA' in l)]
        print(f"  [{time.time()-t0:6.1f}s] {etiq}: " + " | ".join(sal[etiq][:2]))
        if p.returncode != 0:
            print(f"      *** codigo de salida {p.returncode}\n{p.stderr[-600:]}")
    tot += 1; igual = sal.get('original') == sal.get('copia D ')
    ok += igual
    print(f"  [{time.time()-t0:6.1f}s] bateria identica: {'SI' if igual else 'NO'}")

    print(f"\nIDENTIDAD {ok}/{tot}  ({time.time()-t0:.1f} s)")
    sys.exit(0 if ok == tot else 1)
