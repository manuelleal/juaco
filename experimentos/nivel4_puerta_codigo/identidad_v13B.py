"""Arnes de identidad del paquete B-2 (puerta por evidencia del codigo exacto). Con las perillas APAGADAS
(puerta_pat=0, pat_shuf=0) los tres instrumentos deben ser sus originales BIT A BIT, todas las claves.

  A) organismo_v13B   == organismo/organismo_v13.py                    (cc8b16b492d4d324)  3 semillas x 3 escenarios
  B) organismo_v13gB  == experimentos/v13_dos_vias/organismo_v13g.py   (2a80e125f8593bf2)  3 semillas (mundo de regla)
  C) organismo_capB   == experimentos/v13_reverificacion/organismo_capD13.py (fd8e10435801646c)  3 casos
  D) bateria_generaliza_B.py organismo_v13B 3   ==   bateria_generaliza.py organismo_v13 3
     (mismas semillas; se comparan acc, ba, cobertura, divisiones, celdas y muertes semilla a semilla)

Las claves NUEVAS (puerta_pat, pat_shuf, n_cod, nofam_est, ncod_est) se excluyen: son anadido, no cambio.
Regla: si esto no da 100 %, el paquete no corre.
Uso:  python experimentos/nivel4_puerta_codigo/identidad_v13B.py
"""
import json, os, subprocess, sys, time, hashlib

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo'), os.path.join(RAIZ, 'experimentos', 'v13_dos_vias'),
                os.path.join(RAIZ, 'experimentos', 'v13_reverificacion'),
                os.path.join(RAIZ, 'experimentos', 'capacidad_grande'),
                os.path.join(RAIZ, 'experimentos', 'v11_evo_division')]

import mundo_grande as G
import organismo_v13 as V13
import organismo_v13B as V13B
import organismo_v13g as V13G
import organismo_v13gB as V13GB
import organismo_capD13 as CAP
import organismo_capB as CAPB

NUEVAS = {'puerta_pat', 'pat_shuf', 'pat_min', 'n_cod', 'nofam_est', 'ncod_est'}
APAG = dict(puerta_pat=0, pat_shuf=0, pat_min=0)
BASE_CAP = dict(plast=True, lam=0.05, memoria_rechazo=20, mu_norm=True, div_signo=True)


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
                   ('organismo_v13B', os.path.join(AQUI, 'organismo_v13B.py')),
                   ('organismo_v13g', os.path.join(RAIZ, 'experimentos', 'v13_dos_vias', 'organismo_v13g.py')),
                   ('organismo_v13gB', os.path.join(AQUI, 'organismo_v13gB.py')),
                   ('organismo_capD13', os.path.join(RAIZ, 'experimentos', 'v13_reverificacion', 'organismo_capD13.py')),
                   ('organismo_capB', os.path.join(AQUI, 'organismo_capB.py')),
                   ('bateria_generaliza (original)', os.path.join(RAIZ, 'organismo', 'bateria_generaliza.py')),
                   ('bateria_generaliza_B', os.path.join(AQUI, 'bateria_generaliza_B.py'))]:
        print(f"  sha {nom:34s} {h16(p)}")
    ok = tot = 0

    print("\nA) organismo_v13B == organismo_v13 (perilla apagada)")
    for etiq, kw in [('base T=100k', dict()),
                     ('inversion en 50k', dict(invertir_en=50000)),
                     ('estimulo nuevo C veneno', dict(nuevo='C', nuevo_en=50000, nuevo_val='veneno'))]:
        for s in (1, 2, 3):
            tot += 1; ok += cmp(V13.run(s, **kw), V13B.run(s, **kw, **APAG), f"{etiq} s{s}", t0)

    print("\nB) organismo_v13gB == organismo_v13g (mundo de regla, perilla apagada)")
    for regla in ('px0', 'azar'):
        for s in (1, 2, 3):
            kw = dict(T=60000, mundo='regla', regla=regla, eta_s=0.015, puerta=3)
            tot += 1; ok += cmp(V13G.run(s, **kw), V13GB.run(s, **kw, **APAG), f"regla={regla} T=60k s{s}", t0)

    print("\nC) organismo_capB == organismo_capD13 (mundo grande, perilla apagada)")
    for etiq, n_est, pt, cfg in [('v13 puerta=3 n=12', 12, 3000, dict(eta_s=0.015, puerta=3)),
                                 ('v11 puerta=None n=12', 12, 3000, dict()),
                                 ('v13 puerta=2 n=20', 20, 2000, dict(eta_s=0.015, puerta=2))]:
        nom_, pats, val, R = G.mundo(10, n_est)
        kw = dict(T=G.T_de(pt, n_est), plan=G.plan_de(pt, nom_, val), pats=pats, chk=G.chks(pt, n_est))
        for s in ((41, 42) if n_est == 12 else (43,)):
            tot += 1; ok += cmp(CAP.run(s, **kw, **BASE_CAP, **cfg), CAPB.run(s, **kw, **BASE_CAP, **cfg, **APAG), f"{etiq} s{s}", t0)

    print("\nD) bateria_generaliza_B(organismo_v13B) == bateria_generaliza(organismo_v13), 3 semillas")
    env = dict(os.environ, PYTHONIOENCODING='utf-8')
    sal = {}
    for etiq, script, modulo in [('original', os.path.join(RAIZ, 'organismo', 'bateria_generaliza.py'), 'organismo_v13'),
                                 ('copia B ', os.path.join(AQUI, 'bateria_generaliza_B.py'), 'organismo_v13B')]:
        p = subprocess.run([sys.executable, script, modulo, '3'], capture_output=True, text=True, env=env,
                           cwd=os.path.join(RAIZ, 'organismo'), timeout=3600)
        lin = [l for l in p.stdout.splitlines() if ('PASA' in l or 'FALLA' in l or 'VEREDICTO' in l or 'CONSERVA' in l)]
        sal[etiq] = [_sinmod(l.split('] ', 1)[-1].strip(), modulo) for l in lin]
        print(f"  [{time.time()-t0:6.1f}s] {etiq}: " + " | ".join(sal[etiq][:3]))
        if p.returncode != 0:
            print(f"      *** codigo de salida {p.returncode}\n{p.stderr[-800:]}")
    tot += 1
    igual_bat = sal.get('original') == sal.get('copia B ')
    ok += igual_bat
    print(f"  [{time.time()-t0:6.1f}s] bateria identica: {'SI' if igual_bat else 'NO'}")

    print(f"\nIDENTIDAD {ok}/{tot}  ({time.time()-t0:.1f} s)")
    sys.exit(0 if ok == tot else 1)
