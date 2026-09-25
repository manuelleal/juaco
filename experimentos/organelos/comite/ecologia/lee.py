# EXPLORATORIO, no es dato
"""lee.py — tabla por mecanismo (CON contra SIN, misma semilla) de una carpeta de JSON del comite de ecologia.
Uso: python lee.py <carpeta> [--md]
persisten = vivos en T; R0>=0.9 = corridas con R0 nacidos (cohorte hasta T-10000) >= 0.90; PARADA = persiste y R0 >= 0.90.
"""
import glob, json, os, sys
from collections import defaultdict

carpeta = sys.argv[1]; md = '--md' in sys.argv
R = [json.load(open(p, encoding='utf-8')) for p in sorted(glob.glob(os.path.join(carpeta, '*_w*_s*.json')))]
por = defaultdict(dict)
for x in R: por[x['mec']][x['seed']] = x
seeds = sorted(set(x['seed'] for x in R))
sin = por.get('SIN', {})


def f(v, nd=2):
    return '—' if v is None else (f"{v:.{nd}f}" if isinstance(v, float) else str(v))


def med(vs):
    vs = [v for v in vs if v is not None]
    if not vs: return None
    vs = sorted(vs); n = len(vs)
    return float(vs[n // 2]) if n % 2 else (vs[n // 2 - 1] + vs[n // 2]) / 2


filas = []
for mec in sorted(por, key=lambda m: (m != 'SIN', m)):
    xs = [por[mec][s] for s in seeds if s in por[mec]]
    n = len(xs)
    pers = sum(x['persiste'] for x in xs)
    r0ok = sum(1 for x in xs if (x['R0'] or 0) >= 0.90)
    parada = sum(1 for x in xs if x['persiste'] and (x['R0'] or 0) >= 0.90)
    mas_que_sin = sum(1 for x in xs if x['seed'] in sin and (x['t_ext'] or 10 ** 9) > (sin[x['seed']]['t_ext'] or 10 ** 9))
    filas.append(dict(mec=mec, n=n, persisten=pers, r0ok=r0ok, parada=parada,
                      R0_med=med([(x['R0'] if x['R0'] is not None else (0.0 if x['nacidos'] else None)) for x in xs]),
                      t_ext_med=med([(x['t_ext'] if x['t_ext'] is not None else x['T']) for x in xs]),
                      max_med=med([x['max_vivos'] for x in xs]), vivosT_med=med([x['vivos_T'] for x in xs]),
                      nac_med=med([x['nacidos'] for x in xs]), vida_med=med([x['vida_media'] for x in xs]),
                      gen_med=med([x['gen_max'] for x in xs]), mas_que_sin=mas_que_sin,
                      malas=med([(x['mord']['B'] + x['mord']['D']) / max(1, sum(x['mord'].values())) for x in xs]),
                      seg=sum(x['seg'] for x in xs)))
cab = ['mecanismo', 'n', 'persisten', 'R0>=0.9', 'PARADA', 'R0 med', 't_ext med', 'max vivos med', 'vivos T med', 'nacidos med', 'vida med', 'gen max med', 'fraccion mordidas malas', 'vive mas que SIN (misma semilla)', 'seg']
if md:
    print('| ' + ' | '.join(cab) + ' |'); print('|' + '---|' * len(cab))
for r in filas:
    v = [r['mec'], r['n'], f"{r['persisten']}/{r['n']}", f"{r['r0ok']}/{r['n']}", f"{r['parada']}/{r['n']}", f(r['R0_med']), f(r['t_ext_med'], 0), f(r['max_med'], 0), f(r['vivosT_med'], 0),
         f(r['nac_med'], 0), f(r['vida_med'], 0), f(r['gen_med'], 0), f(r['malas']), f"{r['mas_que_sin']}/{r['n']}", f(r['seg'], 0)]
    print(('| ' + ' | '.join(map(str, v)) + ' |') if md else '\t'.join(map(str, v)))
if '--detalle' in sys.argv:
    print()
    for mec in por:
        for s in seeds:
            if s in por[mec]:
                x = por[mec][s]
                print(f"{mec:24s} s{s} persiste {x['persiste']} vivosT {x['vivos_T']:4d} max {x['max_vivos']:4d} t_ext {x['t_ext']} nac {x['nacidos']:5d} coh {x['n_coh']:5d} R0 {x['R0']} vida {x['vida_media']} causas {x['causas']} gen {x['gen_max']} cad {x['cadaveres']} comp {x['comp_mundo']}")
