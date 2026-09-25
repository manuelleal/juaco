"""explora_muro.py — EXPLORATORIO (no es dato): UNA corrida por proceso, semillas de PRACTICA 37901-37909, para elegir el candidato.

MISION: llegar a la AGI por este camino. Cada corrida ES corre_v143.tarea (importada) con el carro del brazo; escribe su JSON en
muro/datos/explora/<brazo>_s<semilla>.json. Sin Pool. El coordinador no lo necesita para la serie.

    python experimentos/organelos/muro/explora_muro.py 37901 paga [--T 100000]
    python experimentos/organelos/muro/explora_muro.py --lee
"""
import argparse, glob, json, os, statistics as st, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import corre_muro as CM

DEST = os.path.join(CM.DATOS, 'explora')


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('seed', type=int, nargs='?')
    ap.add_argument('brazo', nargs='?')
    ap.add_argument('--T', type=int, default=100000)
    ap.add_argument('--lee', action='store_true')
    a = ap.parse_args(argv)
    if a.lee: return lee()
    if a.seed not in CM.PRACTICA: raise SystemExit("explora: solo semillas de practica 37901-37909")
    os.makedirs(DEST, exist_ok=True)
    x = CM.trabajo((a.seed, a.brazo, a.T, DEST, False))
    print(a.brazo, a.seed, x.get('seg'), x['aborto'], 'R0 real med', st.median([l['R0_real'] for l in x['linajes']]) if x['linajes'] else None)
    return 0


def lee():
    R = {}
    for f in sorted(glob.glob(os.path.join(DEST, '*_s*.json'))):
        x = json.load(open(f, encoding='utf-8'))
        if x.get('aborto'): print('ABORTO', f, x['aborto']); continue
        R.setdefault(x['brazo'], {})[x['seed']] = x
    for b, d in R.items():
        L = [l for x in d.values() for l in x['linajes']]
        est = [l for l in L if l['fund_post10k'] == 0]
        cz = {k: sum(l['causas'][k] for l in L) for k in ('hambre', 'sed', 'veneno', 'sal')}
        mm = {s: round(st.median([l['R0_real'] for l in x['linajes']]), 3) for s, x in sorted(d.items())}
        may = {s: sum(l['cruza_real'] for l in x['linajes']) for s, x in sorted(d.items())}
        print(f"{b:8s} n{len(d)} R0 real por semilla {mm} · cruzan {may} · establecidos {len(est)}/{len(L)} "
              f"R0 est {round(st.median([l['R0_real'] for l in est]),3) if est else None} · B+D {st.median([l['mord']['B']+l['mord']['D'] for l in L])} "
              f"A+C {st.median([l['mord']['A']+l['mord']['C'] for l in L])} · causas {cz} · vida {st.median([l['vida_med'] for l in L])}")
        tm = [t for x in d.values() for t in (x.get('tel_muro') or []) if t]
        if tm:
            s = {k: sum(t[k] for t in tm) for k in tm[0] if isinstance(tm[0][k], int) and k not in ('paga', 'telem')}
            print(f"          telemetria muro (ultima instancia) {s}")
    base = R.get('v143', {})
    for b, d in R.items():
        if b == 'v143': continue
        com = sorted(set(d) & set(base))
        if not com: continue
        dif = [st.median([l['R0_real'] for l in d[s]['linajes']]) - st.median([l['R0_real'] for l in base[s]['linajes']]) for s in com]
        print(f"  {b} vs v143: gana {sum(x > 0 for x in dif)}/{len(com)} · dif mediana {round(st.median(dif), 4)} · {[round(x, 3) for x in dif]}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
