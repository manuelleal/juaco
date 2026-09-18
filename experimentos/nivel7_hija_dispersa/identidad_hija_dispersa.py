"""Arnes de identidad de mundo_hija_dispersa.py con las perillas APAGADAS (recic=0, mask_rel=0, n_cf=1) contra
mundo_temporal_k.py (68736baafe7c8cdb). Compara campo a campo tras ida y vuelta por JSON; las claves NUEVAS
(diagnostico y perillas) se excluyen porque son anadido, no cambio.

Regla: si esto no da 7/7, el instrumento no se usa para confirmar nada.
Uso:  python experimentos/nivel7_hija_dispersa/identidad_hija_dispersa.py
"""
import json, os, sys, time, hashlib

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'experimentos', 'nivel7_3T_k')]

import mundo_temporal_k as ORI
import mundo_hija_dispersa as B

NUEVAS = {'div_bloq', 'n_recic', 'diag', 'recic', 'tau_r', 'mask_rel', 'div_diag', 'n_cf'}
V13 = dict(mu_norm=True, div_signo=True, eta_s=0.015, puerta=3)
APAGADO = dict(recic=0, tau_r=0, mask_rel=0, n_cf=1)

CASOS = [
    ('C3  k=1 T=20k', dict(arm='C3', kprof=1, T=20000), [61, 62]),
    ('C3  k=4 T=20k', dict(arm='C3', kprof=4, T=20000), [61, 62]),
    ('C3C k=4 T=20k', dict(arm='C3C', kprof=4, T=20000), [61]),
    ('C1p k=1 T=20k', dict(arm='C1p', kprof=1, T=20000), [61]),
    ('C3  k=5 T=100k (pool agotado)', dict(arm='C3', kprof=5, T=100000), [61]),
]


def norm(d):
    return json.loads(json.dumps({k: v for k, v in d.items() if k not in NUEVAS}))


if __name__ == '__main__':
    t0 = time.time()
    print(f"origen mundo_temporal_k.py     {hashlib.sha256(open(ORI.__file__,'rb').read()).hexdigest()[:16]}")
    print(f"gemelo mundo_hija_dispersa.py  {hashlib.sha256(open(B.__file__,'rb').read()).hexdigest()[:16]}")
    ok = tot = 0
    for etiq, cfg, seeds in CASOS:
        for s in seeds:
            a = norm(ORI.run(s, **cfg, **V13))
            b = norm(B.run(s, **cfg, **V13, **APAGADO))
            tot += 1; igual = a == b; ok += igual
            if not igual:
                print(f"  DIFIERE {etiq} seed={s}: {[k for k in a if a[k] != b.get(k)][:8]}")
            print(f"  [{time.time()-t0:6.1f}s] {etiq:32s} seed={s}  {'IDENTICO' if igual else 'DIFIERE'}", flush=True)
    print(f"\nIDENTIDAD {ok}/{tot}  ({time.time()-t0:.1f} s)")
    sys.exit(0 if ok == tot else 1)
