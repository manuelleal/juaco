"""SALA 2 -- humo: UNA corrida de UN proceso, T=50000 (tope de la regla del encargo). E2L (solap_AB=3), semilla 101, token=1.
Escrito DESPUES de fijar la prediccion en DISENO_radical.md (S8). organismo/ PRIMERO en sys.path (ERR-28)."""
import sys, os, json, time, hashlib
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
sys.path[:0] = [os.path.join(RAIZ, 'organismo'), AQUI]
import organismo_v16 as V16
h16 = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
t0 = time.time()
r = V16.run(101, T=50000, solap_AB=3, token=1, log_cada=5000)
dt = time.time() - t0
out = dict(sha_v16=h16(os.path.join(AQUI, 'organismo_v16.py')), sha_v14=h16(os.path.join(RAIZ, 'organismo', 'organismo_v14.py')),
           montaje='E2L solap_AB=3 s101 T=50000 token=1 tok_var=1', segundos=round(dt, 2),
           W=r['W'], W_lenta=r['W_lenta'], comp=r['comp'], mord=r['mord'], vis=r['vis'], deaths=r['deaths'], splits=r['splits'],
           split_t=r['split_t'], solap=r['solap'], celdas=r['celdas'], t_conflicto=r['t_conflicto'], n_tok=r['n_tok'], tok=r['tok'],
           n_cod=r['n_cod'], log=r['log'])
json.dump(out, open(os.path.join(AQUI, 'humo_v16_E2L_s101.json'), 'w', encoding='utf-8'), indent=1, default=str)
for k in ('sha_v16', 'sha_v14', 'montaje', 'segundos', 'W', 'W_lenta', 'comp', 'mord', 'vis', 'deaths', 'splits', 'split_t', 'solap', 'celdas', 't_conflicto', 'n_tok', 'tok', 'n_cod'):
    print(f'{k:12s} {out[k]}')
print('log (t, W_A, W_B, W_C, W_D):'); [print('  ', x) for x in out['log']]
