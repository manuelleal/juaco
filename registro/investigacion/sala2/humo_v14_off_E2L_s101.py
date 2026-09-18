"""SALA 2 -- REFUTADOR (lente localidad). Par OFF del humo de DISENO_radical.md S8: organismo/organismo_v14.py (v14.1, CONGELADO,
solo se lee) en E2L (solap_AB=3), semilla 101, T=50000, UN proceso (la unica corrida permitida al refutador). No toca nada del repo;
escribe humo_v14_off_E2L_s101.json en esta carpeta. organismo/ PRIMERO en sys.path (ERR-28)."""
import sys, os, json, time, hashlib
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
sys.path[:0] = [os.path.join(RAIZ, 'organismo')]
import organismo_v14 as V14
h16 = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
t0 = time.time()
r = V14.run(101, T=50000, solap_AB=3, log_cada=5000)
dt = time.time() - t0
out = dict(sha_v14=h16(os.path.join(RAIZ, 'organismo', 'organismo_v14.py')), montaje='OFF = v14.1 E2L solap_AB=3 s101 T=50000',
           segundos=round(dt, 2), W=r['W'], W_lenta=r['W_lenta'], comp=r['comp'], mord=r['mord'], vis=r['vis'], deaths=r['deaths'],
           splits=r['splits'], split_t=r['split_t'], solap=r['solap'], celdas=r['celdas'], t_conflicto=r['t_conflicto'],
           n_cod=r['n_cod'], sobre=r['sobre'], llegadas=r['llegadas'], log=r['log'])
json.dump(out, open(os.path.join(AQUI, 'humo_v14_off_E2L_s101.json'), 'w', encoding='utf-8'), indent=1, default=str)
for k in ('sha_v14', 'montaje', 'segundos', 'W', 'W_lenta', 'comp', 'mord', 'vis', 'deaths', 'splits', 'split_t', 'solap', 'celdas', 't_conflicto', 'n_cod', 'sobre', 'llegadas'):
    print(f'{k:12s} {out[k]}')
print('log (t, W_A, W_B, W_C, W_D):'); [print('  ', x) for x in out['log']]
