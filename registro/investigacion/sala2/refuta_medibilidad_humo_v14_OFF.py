"""SALA 2 -- REFUTADOR (lente medibilidad). UNA corrida de UN proceso, T=50000: el PAR OFF que le falta al humo del diseno radical
(humo_v16_E2L_s101.json: E2L solap_AB=3, s101, token=1, T=50000; reporta 58 muertes "sin par OFF"). Aqui: organismo_v14 (v14.1,
feefc88b1fd8d434) con el MISMO montaje, la misma semilla y el mismo T. organismo/ PRIMERO en sys.path (ERR-28). No toca nada del repo."""
import sys, os, json, time, hashlib
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
sys.path[:0] = [os.path.join(RAIZ, 'organismo')]
import organismo_v14 as V14
h16 = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
t0 = time.time()
r = V14.run(101, T=50000, solap_AB=3, log_cada=5000)
dt = time.time() - t0
out = dict(sha_v14=h16(os.path.join(RAIZ, 'organismo', 'organismo_v14.py')), montaje='E2L solap_AB=3 s101 T=50000 v14.1 (OFF, par del humo v16)',
           segundos=round(dt, 2), W=r['W'], W_lenta=r['W_lenta'], comp=r['comp'], mord=r['mord'], vis=r['vis'], deaths=r['deaths'],
           splits=r['splits'], split_t=r['split_t'], solap=r['solap'], celdas=r['celdas'], t_conflicto=r['t_conflicto'], n_cod=r['n_cod'], log=r['log'])
json.dump(out, open(os.path.join(AQUI, 'refuta_medibilidad_humo_v14_E2L_s101_OFF.json'), 'w', encoding='utf-8'), indent=1, default=str)
for k in ('sha_v14', 'montaje', 'segundos', 'W', 'W_lenta', 'comp', 'mord', 'vis', 'deaths', 'splits', 'split_t', 'solap', 'celdas', 't_conflicto', 'n_cod'):
    print(f'{k:12s} {out[k]}')
