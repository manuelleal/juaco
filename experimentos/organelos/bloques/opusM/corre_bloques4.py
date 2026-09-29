"""corre_bloques4.py — runner EXPLORATORIO de OLVIDAR / REPROBAR en el mundo que cambia (Opus M, 28-sep-2026, noche).
Mision: llegar a la AGI por este camino. Importa corre_bloques3 (3f65f87615b76b24) sin tocarlo; cambia el gemelo a motor_bloques4 (kit 1 y 2
== motor_bloques3 bit a bit, arnes). Condiciones (inversion A<->B, C<->D): a = cada 100k con vivero 100k · b = cada 100k con vivero 250k ·
c = cada 50k con vivero 250k. Brazos por condicion: BLOQ2_V (kit 2, sin olvido) · BLOQ3_V (kit 3) · BLOQ3_AZA_V (kit 3 sin herencia) · ING_SEL_C_V.
Uso: python corre_bloques4.py --explora --semillas 48611 --brazos BLOQ3_Va,... --T 500000 --carpeta olv | --lee olv
"""
import argparse, glob, json, os, sys, time, types
import numpy as np

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import corre_bloques3 as C3   # noqa: E402
C2 = C3.C2; CB = C3.CB; NS = C3.NS
SHAS4 = {os.path.join(AQUI, 'corre_bloques3.py'): '3f65f87615b76b24', os.path.join(AQUI, 'motor_bloques3.py'): '21b5ee28d086b3be',
         os.path.join(AQUI, 'motor_bloques4.py'): 'ad5bd2eb59f6279d'}
SEM = tuple(range(48611, 48617))   # 48611-48616 (grep: 486[1-9]x libre salvo 48675)
PRACT = tuple(range(48691, 48696))
C2.ACC.extend(['olvido', 'reprobar']) if len(C2.ACC) == 6 else None
C2.FAMILIA.update(olvido='memoria', reprobar='memoria')
COND = {'a': (100000, 100000), 'b': (100000, 250000), 'c': (50000, 250000)}   # (inv_cada, t_corte)
BASE = {'BLOQ2_V': ('MUT0', dict(on=1, donante='padre', kit=2, tope=16)), 'BLOQ3_V': ('MUT0', dict(on=1, donante='padre', kit=3, tope=16)),
        'BLOQ3_AZA_V': ('MUT0', dict(on=1, donante='azar', kit=3, tope=16)), 'ING_SEL_C_V': ('CEREBRO', dict(on=0))}
ARMS = {}
for _c, (_inv, _tc) in COND.items():
    for _b, (_g, _cfg) in BASE.items():
        _n = _b + _c; ARMS[_n] = _b
        NS.BRAZOS[_n] = (_g, CB.FAB, _tc); CB.BQ[_n] = dict(_cfg, inv=1, inv_cada=_inv)
NS.BRAZOS['BLOQ3_V'] = ('MUT0', CB.FAB, 100000); CB.BQ['BLOQ3_V'] = dict(BASE['BLOQ3_V'][1])   # sin inversion (arnes)


def usa_bloques4():
    import motor_bloques4 as MB
    g = types.ModuleType('motor_bloques4_gemelo')
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


CB.usa_bloques = usa_bloques4


def verifica():
    for p, h in SHAS4.items():
        if CB.h16(p) != h: raise SystemExit(f'{os.path.basename(p)} cambio: {CB.h16(p)} != {h}')
    C3.verifica()


def olvido_lista(R):
    """Tasa de olvido por paso (suma de w de las reglas de olvido activas, sin mirar la condicion) y p de reprobar, de una lista de reglas."""
    fo = [r[5] for r in R if int(r[4]) == 6 and not C2.inerte(r)]; rp = [r[5] for r in R if int(r[4]) == 7 and not C2.inerte(r)]
    return (min(1.0, 10 ** (sum(fo) - 4)) if fo else None), (min(1.0, 10 ** (sum(rp) - 3)) if rp else None)


def lee(car):
    D = {}
    for f in sorted(glob.glob(os.path.join(car, 'M_*.json'))):
        d = json.load(open(f, encoding='utf-8')); D.setdefault(d['brazo'], {})[d['seed']] = d
    print(f'carpeta {car}')
    print(f"{'brazo':14s} {'n':>2s} {'persiste':>8s} {'K med':>7s} {'t_ext (por semilla)':>40s}")
    for c in COND:
        print(f"-- condicion {c}: inversion cada {COND[c][0]}, vivero hasta {COND[c][1]}")
        for b in BASE:
            n = b + c
            if n not in D: continue
            v = [D[n][s] for s in sorted(D[n])]
            print(f"{n:14s} {len(v):2d} {sum(1 for d in v if d.get('persiste')):5d}/{len(v):<2d} {np.median([d['K'] for d in v]):7.2f}   "
                  f"{[d.get('t_ext') for d in v]}  K {[round(d['K'], 1) for d in v]}")
        for a_, b_ in (('BLOQ3_V', 'BLOQ2_V'), ('BLOQ3_V', 'BLOQ3_AZA_V'), ('BLOQ3_V', 'ING_SEL_C_V')):
            A_ = D.get(a_ + c); B_ = D.get(b_ + c)
            if A_ and B_:
                ss = sorted(set(A_) & set(B_))
                te = lambda d: d.get('t_ext') or 10 ** 9
                print(f"   {a_} vs {b_}: K > en {sum(A_[s]['K'] > B_[s]['K'] for s in ss)}/{len(ss)} · vive mas en {sum(te(A_[s]) > te(B_[s]) for s in ss)}/{len(ss)}")
    for n in sorted(D):
        if not n.startswith('BLOQ3'): continue
        print(f'--- {n}: organos (vivos en T si hay; si no, banco de padres al final) y tasas')
        for s in sorted(D[n]):
            d = D[n][s]; B = d['bloques']; vv = B.get('vivos_T') or []
            listas = [x[3] for x in vv] if vv else (B.get('banco_T') or [])
            cnt = {}
            for R in listas:
                for t_ in set(C2.tipo2(r) for r in R if not C2.inerte(r)): cnt[t_] = cnt.get(t_, 0) + 1
            top = sorted(((k / max(1, len(listas)), t_) for t_, k in cnt.items()), reverse=True)
            lam = [olvido_lista(R)[0] for R in listas]; pr = [olvido_lista(R)[1] for R in listas]
            fl = sum(1 for x in lam if x is not None) / max(1, len(listas)); fp = sum(1 for x in pr if x is not None) / max(1, len(listas))
            lm = np.median([x for x in lam if x is not None]) if fl else None; pm = np.median([x for x in pr if x is not None]) if fp else None
            print(f"  s{s} {'vivos' if vv else 'banco'} {len(listas)} · persiste {d.get('persiste')} t_ext {d.get('t_ext')} · olvido en {fl:.2f} "
                  f"(lambda med {lm if lm is None else f'{lm:.2e}'}) · reprobar en {fp:.2f} (p med {pm if pm is None else f'{pm:.2e}'})")
            print('     ' + ' | '.join(f'{t_} {x:.2f}' for x, t_ in top if x >= 0.5))
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
    car = os.path.join(CB.DATOS, a.carpeta or 'olv'); sem = [int(x) for x in a.semillas.split(',')]; brs = a.brazos.split(',')
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
