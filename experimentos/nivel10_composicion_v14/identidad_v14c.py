"""Arnes de identidad de experimentos/nivel10_composicion_v14/ (COMPOSICION v14c = HIJA DISPERSA + PUERTA POR
CODIGO). Con las DOS perillas APAGADAS, todo instrumento nuevo debe ser su original BIT A BIT (regla 2 de
EQUIPO.md). Ademas (b)/(c) prueban algo mas fuerte que "no rompe nada": con UNA perilla ON y la OTRA apagada, la
composicion debe ser identica a los instrumentos de UNA sola perilla YA VALIDADOS (organismo_v13Don,
organismo_v13Bn5c) -- evidencia de que ninguna interfiere con la otra cuando esta inactiva, semilla a semilla,
en TODAS las claves (no solo W).

  (a) organismo_v14c(apagado)                          == organismo_v13                (3 semillas x 3 escenarios)
  (b) organismo_v14c(mask_rel=2, puerta_pat=0)          == organismo_v13Don             (3 semillas)
  (c) organismo_v14c(mask_rel=0, puerta_pat=5,pat_min=1)== organismo_v13Bn5c            (3 semillas)
  (d) bateria_generaliza_v14c.py organismo_v14c 3       == bateria_generaliza.py organismo_v13 3   (linea a linea)

Extra, no pedido por nombre pero obligatorio por la regla 2 de EQUIPO.md para CUALQUIER instrumento nuevo (los
instrumentos de C3/C4 del preregistro):
  (e) organismo_v14gc(apagado)     == organismo_v13g            (3 semillas, mundo de regla, 2 reglas)
  (f) organismo_capBD(apagado)     == organismo_capB             (3 casos, mismos que identidad_v13B.py parte C)
  (g) mundo_composicion_v14(apagado) == mundo_temporal_k          (3 semillas, arm C3, kprof=5)

Nota sobre el criterio 5 de bateria_v14c.py (identidad interna a v11/v10 con eta_s=0,puerta=None): NO se repite
aqui porque ES la etapa 1 de bateria_v14c.py misma (aborta con sys.exit(1) si falla) -- se preregistra como
control que puede fallar en el PREREGISTRO_composicion_v14.md en vez de duplicarse en este arnes.

OJO (ERR-28): organismo/ va PRIMERO en sys.path, siempre. experimentos/v13_dos_vias/ tiene su PROPIO
organismo_v13.py (88c3574cf9cf38bf), distinto del tronco congelado (cc8b16b492d4d324) -- nunca se importa ese
nombre ambiguo con esa carpeta delante.
Regla: si esto no da 100%, el paquete no corre (ni C1-C4 del preregistro son medibles).
Uso:  python experimentos/nivel10_composicion_v14/identidad_v14c.py
"""
import json, os, subprocess, sys, time, hashlib

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo'), os.path.join(RAIZ, 'experimentos', 'v13_dos_vias'),
                os.path.join(RAIZ, 'experimentos', 'nivel7_hija_dispersa'), os.path.join(RAIZ, 'experimentos', 'nivel4_puerta_codigo'),
                os.path.join(RAIZ, 'experimentos', 'v13_reverificacion'), os.path.join(RAIZ, 'experimentos', 'capacidad_grande'),
                os.path.join(RAIZ, 'experimentos', 'v11_evo_division'), os.path.join(RAIZ, 'experimentos', 'nivel7_3T_k')]

import mundo_grande as G
import organismo_v13 as V13
import organismo_v13D as V13D            # solo para comparar defaults de linaje si hiciera falta (no se usa directo)
import organismo_v13Don as V13DON
import organismo_v13B as V13B            # idem
import organismo_v13Bn5c as V13BN5C
import organismo_v13g as V13G
import organismo_capB as CAPB
import mundo_temporal_k as MTK
import organismo_v14c as V14C
import organismo_v14gc as V14GC
import organismo_capBD as CAPBD
import mundo_composicion_v14 as MC14

NUEVAS = {'mask_rel', 'del_s', 'del_c', 'ema_c', 'puerta_pat', 'pat_shuf', 'pat_min', 'n_cod',
          'div_bloq', 'n_recic', 'diag', 'recic', 'tau_r', 'div_diag', 'n_cf'}
APAG = dict(mask_rel=0, puerta_pat=0, pat_shuf=0, pat_min=0)


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
                   ('organismo_v13Don', os.path.join(RAIZ, 'experimentos', 'nivel7_hija_dispersa', 'organismo_v13Don.py')),
                   ('organismo_v13Bn5c', os.path.join(RAIZ, 'experimentos', 'nivel4_puerta_codigo', 'organismo_v13Bn5c.py')),
                   ('organismo_v13g', os.path.join(RAIZ, 'experimentos', 'v13_dos_vias', 'organismo_v13g.py')),
                   ('organismo_capB', os.path.join(RAIZ, 'experimentos', 'nivel4_puerta_codigo', 'organismo_capB.py')),
                   ('mundo_temporal_k', os.path.join(RAIZ, 'experimentos', 'nivel7_3T_k', 'mundo_temporal_k.py')),
                   ('construye_v14c.py', os.path.join(AQUI, 'construye_v14c.py')),
                   ('organismo_v14c', os.path.join(AQUI, 'organismo_v14c.py')),
                   ('organismo_v14c_on', os.path.join(AQUI, 'organismo_v14c_on.py')),
                   ('organismo_v14gc', os.path.join(AQUI, 'organismo_v14gc.py')),
                   ('bateria_v14c', os.path.join(AQUI, 'bateria_v14c.py')),
                   ('bateria_generaliza_v14c', os.path.join(AQUI, 'bateria_generaliza_v14c.py')),
                   ('organismo_capBD', os.path.join(AQUI, 'organismo_capBD.py')),
                   ('organismo_capBD_on', os.path.join(AQUI, 'organismo_capBD_on.py')),
                   ('mundo_composicion_v14', os.path.join(AQUI, 'mundo_composicion_v14.py'))]:
        print(f"  sha {nom:34s} {h16(p)}")
    print(f"  modulo organismo_v13 importado desde: {V13.__file__}")
    ok = tot = 0

    print("\n(a) organismo_v14c(apagado) == organismo_v13, todas las claves")
    for etiq, kw in [('base T=100k', dict()), ('inversion en 50k', dict(invertir_en=50000)),
                     ('estimulo nuevo C veneno', dict(nuevo='C', nuevo_en=50000, nuevo_val='veneno'))]:
        for s in (1, 2, 3):
            tot += 1; ok += cmp(V13.run(s, **kw), V14C.run(s, **kw, **APAG), f"{etiq} s{s}", t0)

    print("\n(b) organismo_v14c(mask_rel=2, puerta_pat=0) == organismo_v13Don (hija dispersa sola)")
    for s in (1, 2, 3):
        a = V13DON.run(s)
        b = V14C.run(s, mask_rel=2, del_s=0.25, del_c=0.25, ema_c=0.05, puerta_pat=0, pat_shuf=0, pat_min=0)
        tot += 1; ok += cmp(a, b, f"s{s}", t0)

    print("\n(c) organismo_v14c(mask_rel=0, puerta_pat=5,pat_min=1) == organismo_v13Bn5c (PATC sola)")
    for s in (1, 2, 3):
        a = V13BN5C.run(s)
        b = V14C.run(s, mask_rel=0, puerta_pat=5, pat_shuf=0, pat_min=1)
        tot += 1; ok += cmp(a, b, f"s{s}", t0)

    print("\n(d) bateria_generaliza_v14c(organismo_v14c) == bateria_generaliza(organismo_v13), 3 semillas, linea a linea")
    env = dict(os.environ, PYTHONIOENCODING='utf-8'); sal = {}
    for etiq, script, modulo in [('original', os.path.join(RAIZ, 'organismo', 'bateria_generaliza.py'), 'organismo_v13'),
                                 ('copia v14c', os.path.join(AQUI, 'bateria_generaliza_v14c.py'), 'organismo_v14c')]:
        p = subprocess.run([sys.executable, script, modulo, '3'], capture_output=True, text=True, env=env,
                           cwd=os.path.join(RAIZ, 'organismo'), timeout=3600)
        lin = [l for l in p.stdout.splitlines() if ('PASA' in l or 'FALLA' in l or 'VEREDICTO' in l or 'CONSERVA' in l)]
        sal[etiq] = [_sinmod(l.split('] ', 1)[-1].strip(), modulo) for l in lin]
        print(f"  [{time.time()-t0:6.1f}s] {etiq}: " + " | ".join(sal[etiq][:3]))
        if p.returncode != 0:
            print(f"      *** codigo de salida {p.returncode}\n{p.stderr[-800:]}")
    tot += 1
    igual_bat = sal.get('original') == sal.get('copia v14c')
    ok += igual_bat
    print(f"  [{time.time()-t0:6.1f}s] bateria identica linea a linea: {'SI' if igual_bat else 'NO'}")

    print("\n(e) [extra, regla 2] organismo_v14gc(apagado) == organismo_v13g (mundo de regla)")
    for regla in ('px0', 'azar'):
        for s in (1, 2, 3):
            kw = dict(T=60000, mundo='regla', regla=regla, eta_s=0.015, puerta=3)
            tot += 1; ok += cmp(V13G.run(s, **kw), V14GC.run(s, **kw, **APAG), f"regla={regla} T=60k s{s}", t0)

    print("\n(f) [extra, regla 2] organismo_capBD(apagado) == organismo_capB (mundo grande)")
    BASE_CAP = dict(plast=True, lam=0.05, memoria_rechazo=20, mu_norm=True, div_signo=True)
    for etiq, n_est, pt, cfg in [('v13 puerta=3 n=12', 12, 3000, dict(eta_s=0.015, puerta=3)),
                                 ('v11 puerta=None n=12', 12, 3000, dict()),
                                 ('v13 puerta=2 n=20', 20, 2000, dict(eta_s=0.015, puerta=2))]:
        nom_, pats, val, R = G.mundo(10, n_est)
        kw = dict(T=G.T_de(pt, n_est), plan=G.plan_de(pt, nom_, val), pats=pats, chk=G.chks(pt, n_est))
        for s in ((41, 42) if n_est == 12 else (43,)):
            tot += 1
            ok += cmp(CAPB.run(s, **kw, **BASE_CAP, **cfg), CAPBD.run(s, **kw, **BASE_CAP, **cfg, mask_rel=0, del_s=0.25, del_c=0.25, ema_c=0.05), f"{etiq} s{s}", t0)

    print("\n(g) [extra, regla 2] mundo_composicion_v14(apagado) == mundo_temporal_k (3T-k, arm C3, kprof=5)")
    V13KW = dict(mu_norm=True, div_signo=True, eta_s=0.015, puerta=3)
    for s in (1, 2, 3):
        kw = dict(arm='C3', kprof=5, T=100000, **V13KW)
        a = MTK.run(s, **kw)
        b = MC14.run(s, **kw, mask_rel=0, del_s=0.25, del_c=0.25, n_cf=1, puerta_pat=0, pat_shuf=0, pat_min=0)
        tot += 1; ok += cmp(a, b, f"s{s}", t0)

    print(f"\nIDENTIDAD {ok}/{tot}  ({time.time()-t0:.1f} s)")
    sys.exit(0 if ok == tot else 1)
