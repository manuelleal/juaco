"""Arnes de identidad de organismo_capB.py (puerta_pat=0) contra organismo_capD13.py (fd8e10435801646c).
Compara campo a campo tras ida y vuelta por JSON; las claves nuevas se excluyen (son anadido, no cambio).
Uso:  python experimentos/creacion_B/identidad_Bpuerta.py
"""
import json, os, sys, time, hashlib

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'experimentos', 'v13_reverificacion'),
                os.path.join(RAIZ, 'experimentos', 'capacidad_grande'),
                os.path.join(RAIZ, 'experimentos', 'v11_evo_division'), os.path.join(RAIZ, 'organismo')]
import mundo_grande as G
import organismo_capD13 as ORI
import organismo_capB as B

NUEVAS = {'nofam_est', 'ncod_est', 'puerta_pat'}
BASE = dict(plast=True, lam=0.05, memoria_rechazo=20, mu_norm=True, div_signo=True)
CASOS = [
    ('v13 puerta=3  n=12 paso=3000', dict(eta_s=0.015, puerta=3), 12, 3000, [41, 42]),
    ('v11 puerta=None n=12 paso=3000', dict(), 12, 3000, [41]),
    ('v13 puerta=2  n=20 paso=2000', dict(eta_s=0.015, puerta=2), 20, 2000, [43]),
]


def norm(d):
    return json.loads(json.dumps({k: v for k, v in d.items() if k not in NUEVAS}))


if __name__ == '__main__':
    t0 = time.time()
    print(f"origen organismo_capD13.py  {hashlib.sha256(open(ORI.__file__,'rb').read()).hexdigest()[:16]}")
    print(f"gemelo organismo_capB.py    {hashlib.sha256(open(B.__file__,'rb').read()).hexdigest()[:16]}")
    ok = tot = 0
    for etiq, cfg, n_est, paso_t, seeds in CASOS:
        nom, pats, val, R = G.mundo(10, n_est)
        kw = dict(T=G.T_de(paso_t, n_est), plan=G.plan_de(paso_t, nom, val), pats=pats, chk=G.chks(paso_t, n_est))
        for s in seeds:
            a = norm(ORI.run(s, **kw, **BASE, **cfg))
            b = norm(B.run(s, **kw, **BASE, **cfg, puerta_pat=0))
            tot += 1; igual = a == b; ok += igual
            if not igual:
                print(f"  DIFIERE {etiq} seed={s}: {[k for k in a if a[k] != b.get(k)][:8]}")
            print(f"  [{time.time()-t0:6.1f}s] {etiq:32s} seed={s}  {'IDENTICO' if igual else 'DIFIERE'}", flush=True)
    print(f"\nIDENTIDAD {ok}/{tot}  ({time.time()-t0:.1f} s)")
    sys.exit(0 if ok == tot else 1)
