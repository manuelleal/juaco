"""corre_bloques6.py — runner EXPLORATORIO: inversion DENTRO de una vida (Opus M, 28-sep-2026, noche). Mision: llegar a la AGI por este camino.
Importa corre_bloques5 (90a01b9a7ba05f91) sin tocarlo; gemelo motor_bloques6 (inv 0/1 == motor_bloques5 bit a bit; inv 2 = inversion en el
nucleo, cualquier periodo). Vivero 100k, T 300k. Periodos 500, 2 000 y 10 000. Brazos: ING_SEL_C_V · SEL_OLV_V (15 genes + gen de olvido del
cerebro) · BLOQ4_V (kit 4) · BLOQ4_AZA_V.
Uso: python corre_bloques6.py --explora --semillas 48631 --brazos ... --T 300000 --carpeta vida | --lee vida
"""
import argparse, glob, json, os, sys, time, types
import numpy as np

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import corre_bloques5 as C5   # noqa: E402
C4 = C5.C4; C2 = C5.C2; CB = C5.CB; NS = C5.NS
SHAS6 = {os.path.join(AQUI, 'corre_bloques5.py'): '90a01b9a7ba05f91', os.path.join(AQUI, 'motor_bloques5.py'): 'a727e6aea0fca8da',
         os.path.join(AQUI, 'motor_bloques6.py'): '1c46de780d65ff3c'}
SEM = tuple(range(48631, 48637))   # 48631-48636 (grep: libres)
PRACT = tuple(range(48685, 48690))
PER = (500, 2000, 10000)
BASE = {k: C5.BASE[k] for k in ('ING_SEL_C_V', 'SEL_OLV_V', 'BLOQ4_V', 'BLOQ4_AZA_V')}
ARMS = {}
for _p in PER:
    for _b, (_g, _cfg) in BASE.items():
        _n = f'{_b}_p{_p}'; ARMS[_n] = (_b, _p)
        NS.BRAZOS[_n] = (_g, CB.FAB, 100000); CB.BQ[_n] = dict(_cfg, inv=2, inv_cada=_p)


def usa_bloques6():
    import motor_bloques6 as MB
    g = types.ModuleType('motor_bloques6_gemelo')
    g.__dict__.update({k: v for k, v in NS.ME_PY.__dict__.items() if not k.startswith('__')})

    def _rs(*a, **k):
        r = MB.run_solapadas(*a, **k); P = r['pista']
        CB.MUNDO_ULT.clear(); CB.MUNDO_ULT.update(comp_mundo=P['comp_mundo'], nobj_medio=P['nobj_medio'], llegadas=P['llegadas'],
                                                  perdidas=P['llegadas_perdidas'])
        return r
    g.run_solapadas = _rs
    g._MF = MB
    NS.CR.ME = g
    return MB


CB.usa_bloques = usa_bloques6


def verifica():
    for p, h in SHAS6.items():
        if CB.h16(p) != h: raise SystemExit(f'{os.path.basename(p)} cambio: {CB.h16(p)} != {h}')
    C5.verifica()


def tasas(d):
    B = d.get('bloques') or {}; vv = B.get('vivos_T') or []
    listas = [x[3] for x in vv] if vv else (B.get('banco_T') or [])
    lc = [C5.lam_cerebro(R) for R in listas]; ol = [C4.olvido_lista(R) for R in listas]
    f = lambda xs: (sum(1 for x in xs if x is not None) / max(1, len(listas)), (float(np.median([x for x in xs if x is not None])) if any(x is not None for x in xs) else None))
    return ('vivos' if vv else 'banco'), len(listas), f(lc), f([o[0] for o in ol]), f([o[1] for o in ol])


def lee(car):
    D = {}
    for f in sorted(glob.glob(os.path.join(car, 'M_*.json'))):
        d = json.load(open(f, encoding='utf-8')); D.setdefault(d['brazo'], {})[d['seed']] = d
    print(f'carpeta {car} · vivero 100 000')
    te = lambda d: d.get('t_ext') or 10 ** 9
    for p in PER:
        print(f'-- inversion cada {p} pasos')
        for b in BASE:
            n = f'{b}_p{p}'
            if n not in D: continue
            v = [D[n][s] for s in sorted(D[n])]
            print(f"{n:22s} persiste {sum(1 for d in v if d.get('persiste'))}/{len(v)} · K med {np.median([d['K'] for d in v]):6.2f} · "
                  f"K {[round(d['K'], 1) for d in v]} · t_ext {[d.get('t_ext') for d in v]}")
            if b != 'ING_SEL_C_V':
                for d in v:
                    fu, nl, lc, lo, rp = tasas(d)
                    print(f"     s{d['seed']} {fu} {nl}: olvido cerebro en {lc[0]:.2f} (λ med {lc[1] if lc[1] is None else f'{lc[1]:.1e}'}) · "
                          f"olvido reglas en {lo[0]:.2f} (λ {lo[1] if lo[1] is None else f'{lo[1]:.1e}'}) · reprobar en {rp[0]:.2f} (p {rp[1] if rp[1] is None else f'{rp[1]:.1e}'})")
        for a_, b_ in (('SEL_OLV_V', 'ING_SEL_C_V'), ('BLOQ4_V', 'BLOQ4_AZA_V'), ('BLOQ4_V', 'ING_SEL_C_V')):
            A_ = D.get(f'{a_}_p{p}'); B_ = D.get(f'{b_}_p{p}')
            if A_ and B_:
                ss = sorted(set(A_) & set(B_))
                print(f"   {a_} vs {b_}: K > en {sum(A_[s]['K'] > B_[s]['K'] for s in ss)}/{len(ss)} · vive mas en {sum(te(A_[s]) > te(B_[s]) for s in ss)}/{len(ss)}")
    print('-- CURVA: λ del olvido del cerebro fijado en SEL_OLV_V (mediana de las medianas por semilla)')
    for p in PER:
        v = list(D.get(f'SEL_OLV_V_p{p}', {}).values())
        ls = [tasas(d)[2][1] for d in v if tasas(d)[2][1] is not None]
        print(f"   periodo {p:6d}: λ {(f'{np.median(ls):.1e}' if ls else None)} (por semilla {[f'{x:.1e}' for x in ls]})")
    return D


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False, add_help=False)
    ap.add_argument('--explora', action='store_true'); ap.add_argument('--semillas', default=None); ap.add_argument('--brazos', default=None)
    ap.add_argument('--T', type=int, default=300000); ap.add_argument('--carpeta', default=None); ap.add_argument('--lee', default=None)
    a, resto = ap.parse_known_args()
    if resto: raise SystemExit(f'banderas desconocidas: {resto}')
    if a.lee: lee(a.lee if os.path.isabs(a.lee) else os.path.join(CB.DATOS, a.lee)); return
    if not a.explora: raise SystemExit('usa --explora o --lee')
    if a.T > 500000: raise SystemExit('T > 500 000 no se corre aqui')
    verifica()
    car = os.path.join(CB.DATOS, a.carpeta or 'vida'); sem = [int(x) for x in a.semillas.split(',')]; brs = a.brazos.split(',')
    for s in sem:
        if s not in SEM and s not in PRACT: raise SystemExit(f'semilla {s} fuera de las declaradas')
    for b in brs:
        if b not in ARMS: raise SystemExit(f'brazo desconocido {b}')
    t0 = time.time()
    for s in sem:
        for b in brs:
            o = CB.corre(s, b, a.T, car)
            print(f"[{time.strftime('%H:%M:%S')}] {b} s{s} T{a.T}: persiste {o['persiste']} · K {o['K']:.2f} · t_ext {o.get('t_ext')} · "
                  f"aborto {o['aborto']} ({o['seg']} s; {time.time() - t0:.0f} s)", flush=True)


if __name__ == '__main__':
    main()
