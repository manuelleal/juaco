"""3T — corre los 6 brazos preregistrados, 20 semillas, T=100000. Guarda CSV + JSON con procedencia."""
import sys, os, json, csv, time, hashlib, platform
import numpy as np
from multiprocessing import Pool, get_context
try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import mundo_temporal as mt

ARMS = ['C1', 'C1p', 'C2', 'C2b', 'C3', 'C3C']
SEEDS = list(range(1, 21))
T = 100000


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def tarea(a):
    arm, seed, kw = a
    return mt.run(seed, arm, **kw)


def med(v):
    v = [x for x in v if x is not None]
    return (round(float(np.median(v)), 4), round(float(min(v)), 4), round(float(max(v)), 4)) if v else (None, None, None)


def main(arms=ARMS, seeds=SEEDS, T=T, tag='3T', extra=None):
    kw = dict(T=T); kw.update(extra or {})
    tareas = [(a, s, kw) for a in arms for s in seeds]
    t0 = time.time()
    with get_context('spawn').Pool(min(16, len(tareas))) as p:
        res = p.map(tarea, tareas)
    dt = time.time() - t0
    print(f"{len(tareas)} corridas en {dt:.1f}s")

    proc = dict(fecha=time.strftime('%Y-%m-%d %H:%M:%S'), rama='3T_temporal', tag=tag,
                sha_mundo_temporal=sha(os.path.join(AQUI, 'mundo_temporal.py')),
                sha_corre_3T=sha(os.path.join(AQUI, 'corre_3T.py')),
                python=platform.python_version(), numpy=np.__version__,
                arms=arms, seeds=seeds, kwargs=kw,
                constantes=dict(L=mt.L, NK=mt.NK, NKMAX=mt.NKMAX, K=mt.K,
                                R_VAL=mt.R_VAL, E_VAL=mt.E_VAL),
                segundos=round(dt, 1))

    cols = (['arm', 'seed', 'W_AA', 'W_AB', 'W_BA', 'W_BB', 'sep',
             'Wp_AA', 'Wn_AA', 'Wp_AB', 'Wn_AB', 'solap_A', 'solap_B'] +
            [f'solap_A_s{i}' for i in range(5)] +
            [f'rho_s{i}' for i in range(5)] + [f'rho_cod_s{i}' for i in range(5)] +
            ['splits', 'celdas', 't_pool', 'fracTemp_med'] +
            [f'acc_q{i+1}' for i in range(4)] + [f'base_q{i+1}' for i in range(4)] +
            [f'lift_q{i+1}' for i in range(4)] +
            ['early_acc', 'early_base', 'early_lift', 'early_nbit'] +
            [f'nAB_q{i+1}' for i in range(4)] + [f'nAA_q{i+1}' for i in range(4)] +
            [f'nB_q{i+1}' for i in range(4)] + ['deaths', 'Rtot', 'E_fin'])

    filas = []
    for r in res:
        ft = [s[3] for s in r['split_t']]
        f = dict(arm=r['arm'], seed=r['seed'], sep=r['sep'], solap_A=r['solap_A'], solap_B=r['solap_B'],
                 splits=r['splits'], celdas=r['celdas'], t_pool=r['t_pool'],
                 fracTemp_med=round(float(np.median(ft)), 3) if ft else None,
                 deaths=r['deaths'], Rtot=r['Rtot'], E_fin=r['E_fin'],
                 early_acc=r['early']['acc'], early_base=r['early']['base'],
                 early_lift=r['early']['lift'], early_nbit=r['early']['nbit'])
        for k, v in r['W'].items(): f['W_' + k.replace('|', '')] = v
        for k in ('A|A', 'A|B'):
            f['Wp_' + k.replace('|', '')] = r['comp'][k][0]; f['Wn_' + k.replace('|', '')] = r['comp'][k][1]
        for i in range(5):
            f[f'solap_A_s{i}'] = r['solap_A_q'][i]; f[f'rho_s{i}'] = r['rho_q'][i]; f[f'rho_cod_s{i}'] = r['rho_cod_q'][i]
        for i in range(4):
            f[f'acc_q{i+1}'] = r['acc'][i]; f[f'base_q{i+1}'] = r['base'][i]; f[f'lift_q{i+1}'] = r['lift'][i]
            f[f'nAB_q{i+1}'] = r['n_AB'][i]; f[f'nAA_q{i+1}'] = r['n_AA'][i]; f[f'nB_q{i+1}'] = r['n_B'][i]
        filas.append(f)

    ts = time.strftime('%Y%m%d_%H%M%S')
    base = os.path.join(AQUI, f'{tag}_{ts}')
    with open(base + '.csv', 'w', newline='', encoding='utf-8') as fh:
        for k, v in proc.items(): fh.write(f'# {k}: {v}\n')
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader()
        for f in filas: w.writerow({c: f.get(c) for c in cols})
    with open(base + '.json', 'w', encoding='utf-8') as fh:
        json.dump(dict(procedencia=proc, corridas=res), fh, default=str)
    print('->', base + '.csv')
    resumen(filas, arms)
    return base, filas, res


def resumen(filas, arms):
    print('\n' + '=' * 108)
    print(f"{'arm':5} {'sep':>18} {'W_AB':>17} {'W_AA':>17} {'solapA':>8} {'lift_q4':>17} {'Rtot':>16} {'muertes':>7} {'splits':>7}")
    print('-' * 108)
    for a in arms:
        F = [f for f in filas if f['arm'] == a]
        g = lambda c: med([f[c] for f in F])
        fmt = lambda t: f"{t[0]:.2f}[{t[1]:.2f},{t[2]:.2f}]" if t[0] is not None else 'NA'
        print(f"{a:5} {fmt(g('sep')):>18} {fmt(g('W_AB')):>17} {fmt(g('W_AA')):>17} "
              f"{g('solap_A')[0]:>8} {fmt(g('lift_q4')):>17} {fmt(g('Rtot')):>16} "
              f"{g('deaths')[0]:>7.0f} {g('splits')[0]:>7.0f}")
    print('=' * 108)


if __name__ == '__main__':
    main()
