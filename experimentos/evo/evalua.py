"""JUACO-EVO — evaluador automatico de un genoma (archivo Python con la interfaz de organismo_v10m).
Ejecuta el curriculo fijado en PREREGISTRO_evo.md: seis etapas del examen v3 + CTRL + bloque M de retencion, sobre un
conjunto de semillas (entrenamiento 1-10 o retenidas 11-20). Devuelve restricciones H1-H3 y puntuacion R, S, E, C.
No decide nada que no este en el preregistro. Igualdades numericas. Un genoma que no importa o revienta = "roto".

Uso:  python evalua.py <genoma.py> --padre <padre.py> [--semillas train|heldout] [--out <json>] [--pool 14]
"""
import sys, os, json, time, hashlib, difflib, importlib.util, traceback, argparse
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

EVENTO = 50000
ETAPAS = {'E1': dict(), 'E2': dict(invertir_en=EVENTO), 'E2I': dict(nuevo='C'),
          'E2J': dict(nuevo='D', nuevo_val='comida', solap_B=1), 'E2K': dict(nuevo='D', nuevo_val='comida', solap_B=2),
          'E2L': dict(solap_AB=3), 'CTRL': dict(solap_AB=3, plast=False)}
FASES = {50000: (['C', 'D'], {'C': 'veneno', 'D': 'comida'}), 100000: (['A', 'B'], {'A': 'comida', 'B': 'veneno'})}
tasa = lambda r, k, i: 100 * r['mord'][k][i] / max(r['vis'][k][i], 1)
CRIT = {
    'E1':  [lambda r: r['mord']['B'][3] < r['mord']['B'][0], lambda r: abs(r['W']['A'] - 1) < .15, lambda r: abs(r['W']['B'] + 3) < .3],
    'E2':  [lambda r: abs(r['W']['A'] + 3) < .3, lambda r: abs(r['W']['B'] - 1) < .15, lambda r: r['mord']['B'][3] >= 50],
    'E2I': [lambda r: r['W']['C'] <= -2.5, lambda r: abs(r['W']['A'] - 1) < .15, lambda r: r['W']['B'] <= -2.8,
            lambda r: tasa(r, 'A', 3) >= .8 * tasa(r, 'A', 1)],
    'E2J': [lambda r: r['W']['D'] >= .85, lambda r: r['W']['B'] <= -2.7],
    'E2K': [lambda r: r['W']['D'] >= .8, lambda r: r['W']['B'] <= -2.4],
    'E2L': [lambda r: abs(r['W']['A'] - 1) < .15, lambda r: abs(r['W']['B'] + 3) < .3, lambda r: r['solap']['AB'] == 0],
    'CTRL': [lambda r: abs(r['W']['A'] - 1) < .15, lambda r: abs(r['W']['B'] + 3) < .3],   # debe FALLAR
}


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def carga(path):
    spec = importlib.util.spec_from_file_location('genoma_' + h16(path), path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod


def tarea(args):
    path, etapa, seed = args
    try:
        mod = carga(path)
        if etapa == 'M':
            r = mod.run(seed, T=150000, fases=FASES)
            s50 = r['sondas'][50000]; s100 = r['sondas'][100000]
            return dict(etapa=etapa, seed=seed, ok=True, W50={k: float(v) for k, v in s50.items()}, W100={k: float(v) for k, v in s100.items()},
                        deaths=r['deaths'], splits=r['splits'], celdas=r['celdas'])
        r = mod.run(seed, **ETAPAS[etapa])
        return dict(etapa=etapa, seed=seed, ok=True, W=r['W'], mord=r['mord'], vis=r['vis'], deaths=r['deaths'],
                    splits=r['splits'], celdas=r['celdas'], solap=r['solap'])
    except Exception as e:
        return dict(etapa=etapa, seed=seed, ok=False, error=traceback.format_exc()[-800:])


def lineas_cambiadas(padre, hijo):
    a = open(padre, encoding='utf-8').read().splitlines(); b = open(hijo, encoding='utf-8').read().splitlines()
    d = [l for l in difflib.unified_diff(a, b, lineterm='', n=0) if (l.startswith('+') or l.startswith('-')) and not l.startswith(('+++', '---'))]
    return len(d)


def evalua(path, padre, seeds, pool_n=14, log=print):
    import multiprocessing as mp
    t0 = time.time()
    trabajos = [(path, e, s) for e in ETAPAS for s in seeds] + [(path, 'M', s) for s in seeds]
    with mp.get_context('spawn').Pool(pool_n) as pool:
        res = pool.map(tarea, trabajos, chunksize=1)
    rotas = [r for r in res if not r['ok']]
    out = dict(genoma=os.path.relpath(path), sha=h16(path), padre=os.path.relpath(padre) if padre else None, semillas=list(seeds),
               segundos=round(time.time() - t0, 1), rotas=len(rotas), error=(rotas[0]['error'] if rotas else None))
    if rotas:
        out.update(valido=False, motivo='roto'); return out
    R_ = {e: [r for r in res if r['etapa'] == e] for e in list(ETAPAS) + ['M']}
    pasa = {e: sum(all(c(r) for c in CRIT[e]) for r in R_[e]) for e in ETAPAS}
    n = len(seeds)
    H1 = all(pasa[e] >= 0.9 * n for e in ETAPAS if e != 'CTRL') and pasa['CTRL'] <= 0.1 * n
    H2 = all(r['celdas'] <= 45 for e in ETAPAS for r in R_[e])
    guarda = sum(r['W100']['C'] <= -2.5 and r['W100']['D'] >= 0.85 for r in R_['M'])
    H3 = guarda >= 0.8 * n
    ret = sum(r['W100']['B'] <= -2 and r['W100']['A'] >= 0.5 for r in R_['M'])
    R = ret / n
    S = max(0.0, 1 - float(np.median([r['deaths'] for r in R_['E1']])) / 200)
    E = max(0.0, 1 - float(np.median([r['splits'] for r in R_['E2L']])) / 9)
    C = (lineas_cambiadas(padre, path) / 15) if padre else 0.0
    out.update(valido=bool(H1 and H2 and H3), H1=H1, H2=H2, H3=H3, pasa=pasa, guarda=guarda, retencion=ret, R=R, S=round(S, 4), E=round(E, 4), C=round(C, 4),
               SEC=round(S + E - C, 4), W_B100_mediana=float(np.median([r['W100']['B'] for r in R_['M']])),
               W_A100_mediana=float(np.median([r['W100']['A'] for r in R_['M']])),
               muertes_E1=float(np.median([r['deaths'] for r in R_['E1']])), splits_E2L=float(np.median([r['splits'] for r in R_['E2L']])),
               splits_M=float(np.median([r['splits'] for r in R_['M']])))
    return out


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('genoma'); ap.add_argument('--padre', default=None)
    ap.add_argument('--semillas', default='train'); ap.add_argument('--out', default=None); ap.add_argument('--pool', type=int, default=14)
    a = ap.parse_args()
    seeds = list(range(1, 11)) if a.semillas == 'train' else list(range(11, 21))
    o = evalua(os.path.abspath(a.genoma), os.path.abspath(a.padre) if a.padre else None, seeds, a.pool)
    print(json.dumps({k: v for k, v in o.items() if k != 'error'}, ensure_ascii=False))
    if o.get('error'): print('ERROR:', o['error'][-300:])
    if a.out:
        json.dump(o, open(a.out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
