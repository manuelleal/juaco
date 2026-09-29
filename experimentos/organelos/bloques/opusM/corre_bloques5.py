"""corre_bloques5.py — runner EXPLORATORIO de OLVIDAR LO QUE APRENDIO EL CEREBRO en el mundo que cambia (Opus M, 28-sep-2026, noche).
Mision: llegar a la AGI por este camino. Importa corre_bloques4 (1a7b1ffcb5baee17) sin tocarlo; gemelo motor_bloques5 (kit 1..3 ==
motor_bloques4 bit a bit, arnes). Inversion A<->B, C<->D cada 100 000; condiciones a = vivero 100k, b = vivero 250k.
Brazos: BLOQ3_V (kit 3, referencia) · BLOQ4_V (kit 4: + olvidar el cerebro) · BLOQ4_AZA_V (sin herencia) · ING_SEL_C_V ·
SEL_OLV_V (15 genes + el GEN de olvido del cerebro, kit 5, sin otras reglas; el valor inicial de cada fundador es al azar).
Uso: python corre_bloques5.py --explora --semillas 48621 --brazos ... --T 500000 --carpeta olvc | --lee olvc
"""
import argparse, glob, json, os, sys, time, types
import numpy as np

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import corre_bloques4 as C4   # noqa: E402
C3 = C4.C3; C2 = C4.C2; CB = C4.CB; NS = C4.NS
SHAS5 = {os.path.join(AQUI, 'corre_bloques4.py'): '1a7b1ffcb5baee17', os.path.join(AQUI, 'motor_bloques4.py'): 'ad5bd2eb59f6279d',
         os.path.join(AQUI, 'motor_bloques5.py'): 'a727e6aea0fca8da'}
SEM = tuple(range(48621, 48627))   # 48621-48626 (grep: libre)
PRACT = tuple(range(48681, 48686))
if len(C2.ACC) == 8: C2.ACC.append('olvCerebro')
C2.FAMILIA.update(olvCerebro='memoria')
COND = {'a': (100000, 100000), 'b': (100000, 250000)}
GEN = dict(on=1, donante='padre', kit=5, tope=1, inicial=1, p_dup=0, p_hgt=0, p_del=0)
BASE = {'BLOQ3_V': ('MUT0', dict(on=1, donante='padre', kit=3, tope=16)), 'BLOQ4_V': ('MUT0', dict(on=1, donante='padre', kit=4, tope=16)),
        'BLOQ4_AZA_V': ('MUT0', dict(on=1, donante='azar', kit=4, tope=16)), 'ING_SEL_C_V': ('CEREBRO', dict(on=0)),
        'SEL_OLV_V': ('CEREBRO', GEN)}
ARMS = {}
for _c, (_inv, _tc) in COND.items():
    for _b, (_g, _cfg) in BASE.items():
        _n = _b + '5' + _c; ARMS[_n] = _b
        NS.BRAZOS[_n] = (_g, CB.FAB, _tc); CB.BQ[_n] = dict(_cfg, inv=1, inv_cada=_inv)
for _b in ('BLOQ4_V', 'SEL_OLV_V'):   # sin inversion (arnes)
    NS.BRAZOS[_b + '_0'] = (BASE[_b][0], CB.FAB, 100000); CB.BQ[_b + '_0'] = dict(BASE[_b][1])


def usa_bloques5():
    import motor_bloques5 as MB
    g = types.ModuleType('motor_bloques5_gemelo')
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


CB.usa_bloques = usa_bloques5


def verifica():
    for p, h in SHAS5.items():
        if CB.h16(p) != h: raise SystemExit(f'{os.path.basename(p)} cambio: {CB.h16(p)} != {h}')
    C4.verifica()


def lam_cerebro(R):
    w = [r[5] for r in R if int(r[4]) == 8 and not C2.inerte(r)]
    return min(1.0, 10 ** (sum(w) - 4)) if w else None


def lee(car):
    D = {}
    for f in sorted(glob.glob(os.path.join(car, 'M_*.json'))):
        d = json.load(open(f, encoding='utf-8')); D.setdefault(d['brazo'], {})[d['seed']] = d
    print(f'carpeta {car} · inversion cada 100 000')
    for c in COND:
        print(f"-- condicion {c}: vivero hasta {COND[c][1]}")
        for b in BASE:
            n = b + '5' + c
            if n not in D: continue
            v = [D[n][s] for s in sorted(D[n])]
            print(f"{n:16s} persiste {sum(1 for d in v if d.get('persiste'))}/{len(v)} · K med {np.median([d['K'] for d in v]):6.2f} · "
                  f"t_ext {[d.get('t_ext') for d in v]} · K {[round(d['K'], 1) for d in v]}")
        te = lambda d: d.get('t_ext') or 10 ** 9
        for a_, b_ in (('BLOQ4_V', 'BLOQ3_V'), ('BLOQ4_V', 'BLOQ4_AZA_V'), ('SEL_OLV_V', 'ING_SEL_C_V'), ('BLOQ4_V', 'ING_SEL_C_V')):
            A_ = D.get(a_ + '5' + c); B_ = D.get(b_ + '5' + c)
            if A_ and B_:
                ss = sorted(set(A_) & set(B_))
                print(f"   {a_} vs {b_}: vive mas en {sum(te(A_[s]) > te(B_[s]) for s in ss)}/{len(ss)} · K > en {sum(A_[s]['K'] > B_[s]['K'] for s in ss)}/{len(ss)}")
    for n in sorted(D):
        if not (n.startswith('BLOQ4') or n.startswith('SEL_OLV')): continue
        print(f'--- {n}: olvido del cerebro (lambda por paso) en vivos en T, o en el banco de padres al final; organos >= 50 %')
        for s in sorted(D[n]):
            d = D[n][s]; B = d['bloques']; vv = B.get('vivos_T') or []
            listas = [x[3] for x in vv] if vv else (B.get('banco_T') or [])
            lam = [lam_cerebro(R) for R in listas]; fl = sum(1 for x in lam if x is not None) / max(1, len(listas))
            lm = [x for x in lam if x is not None]
            cnt = {}
            for R in listas:
                for t_ in set(C2.tipo2(r) for r in R if not C2.inerte(r)): cnt[t_] = cnt.get(t_, 0) + 1
            top = sorted(((k / max(1, len(listas)), t_) for t_, k in cnt.items()), reverse=True)
            print(f"  s{s} {'vivos' if vv else 'banco'} {len(listas)} · persiste {d.get('persiste')} t_ext {d.get('t_ext')} · olvido cerebro en {fl:.2f}"
                  f" · lambda mediana {(f'{np.median(lm):.2e}' if lm else None)} (memoria ~{(f'{1 / np.median(lm):.0f}' if lm else '-')} pasos)")
            if not n.startswith('SEL_OLV'): print('     ' + ' | '.join(f'{t_} {x:.2f}' for x, t_ in top if x >= 0.5))
    return D


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False, add_help=False)
    ap.add_argument('--explora', action='store_true'); ap.add_argument('--semillas', default=None); ap.add_argument('--brazos', default=None)
    ap.add_argument('--T', type=int, default=500000); ap.add_argument('--carpeta', default=None); ap.add_argument('--lee', default=None)
    a, resto = ap.parse_known_args()
    if resto: raise SystemExit(f'banderas desconocidas: {resto}')
    if a.lee: lee(a.lee if os.path.isabs(a.lee) else os.path.join(CB.DATOS, a.lee)); return
    if not a.explora: raise SystemExit('usa --explora o --lee')
    if a.T > 500000: raise SystemExit('T > 500 000 no se corre aqui')
    verifica()
    car = os.path.join(CB.DATOS, a.carpeta or 'olvc'); sem = [int(x) for x in a.semillas.split(',')]; brs = a.brazos.split(',')
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
