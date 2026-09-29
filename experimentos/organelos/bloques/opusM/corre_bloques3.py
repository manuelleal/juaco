"""corre_bloques3.py — runner EXPLORATORIO de UN MUNDO QUE CAMBIA (Opus M, 28-sep-2026, ultima ronda). Mision: llegar a la AGI por este camino.
Importa corre_bloques2 (0d894a522e93766f) y corre_bloques (a090b82eae9f1ee3) sin tocarlos; cambia el gemelo a motor_bloques3 (inv = 0 ==
motor_bloques2 bit a bit, arnes). Vivero finito t_corte 100 000. Inversion A<->B, C<->D cada INV_CADA pasos.
Brazos: BLOQ_V_I (kit actual) · BLOQ2_V_I (kit grande: memoria y vecino) · BLOQ2_AZA_V_I (kit grande sin herencia) · (ING_F1_V_I base, opcional).
Uso: python corre_bloques3.py --humo | --explora --semillas ... --brazos ... --T ... --carpeta ... | --lee <carpeta>
"""
import argparse, glob, json, os, sys, time, types
import numpy as np

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import corre_bloques2 as C2   # noqa: E402
CB = C2.CB; NS = C2.NS
SHAS3 = {os.path.join(AQUI, 'corre_bloques2.py'): '0d894a522e93766f', os.path.join(AQUI, 'motor_bloques2.py'): 'e365506be24bb490',
         os.path.join(AQUI, 'motor_bloques3.py'): '21b5ee28d086b3be'}
INV_CADA = 20000
SEM = tuple(range(48901, 48907))   # 48901-48906 (grep: 489xx libre salvo 48965)
PRACT = tuple(range(48991, 48996))


def usa_bloques3():
    import motor_bloques3 as MB
    g = types.ModuleType('motor_bloques3_gemelo')
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


CB.usa_bloques = usa_bloques3
CB.DEF.update(inv=0, inv_cada=INV_CADA)
ARMS = {'BLOQ_V_I': ('MUT0', dict(on=1, donante='padre')), 'BLOQ2_V_I': ('MUT0', dict(on=1, donante='padre', kit=2, tope=16)),
        'BLOQ2_AZA_V_I': ('MUT0', dict(on=1, donante='azar', kit=2, tope=16)), 'ING_F1_V_I': ('MUT0', dict(on=0)),
        'ING_SEL_C_V_I': ('CEREBRO', dict(on=0))}
for _b, (_g, _c) in ARMS.items():
    NS.BRAZOS[_b] = (_g, CB.FAB, 100000)
    CB.BQ[_b] = dict(_c, inv=1, inv_cada=INV_CADA)
# PERIODOS LARGOS (anadido 21:59, tras ver que con 20 000 TODO se extingue, y ANTES de correrlos): inversion cada 50 000 (_I50) y 100 000 (_I100)
for _per, _suf in ((50000, '50'), (100000, '100')):
    for _b, (_g, _c) in list(ARMS.items())[:5]:
        _n = _b + _suf
        NS.BRAZOS[_n] = (_g, CB.FAB, 100000); CB.BQ[_n] = dict(_c, inv=1, inv_cada=_per)
ARMS.update({_b + _s: ARMS[_b] for _s in ('50', '100') for _b in list(ARMS)[:5]})
# VIVERO LARGO CON CAMBIO (anadido 22:04, tras ver 0/90 persistir y ANTES de correrlo): t_corte 250 000, inversion cada 50 000 (_IL):
# 5 inversiones CON subsidio (la seleccion ve el cambio mientras el vivero sostiene al linaje) y 5 sin el.
for _b in ('BLOQ_V_I', 'BLOQ2_V_I', 'BLOQ2_AZA_V_I', 'ING_SEL_C_V_I'):
    _g, _c = ARMS[_b]; NS.BRAZOS[_b + 'L'] = (_g, CB.FAB, 250000); CB.BQ[_b + 'L'] = dict(_c, inv=1, inv_cada=50000); ARMS[_b + 'L'] = ARMS[_b]


def verifica():
    for p, h in SHAS3.items():
        if CB.h16(p) != h: raise SystemExit(f'{os.path.basename(p)} cambio: {CB.h16(p)} != {h}')
    C2.verifica()


def lee(car):
    D = {}
    for f in sorted(glob.glob(os.path.join(car, 'M_*.json'))):
        d = json.load(open(f, encoding='utf-8')); D.setdefault(d['brazo'], {})[d['seed']] = d
    br = [b for b in ARMS if b in D]
    print(f'carpeta {car} · inversion A<->B, C<->D cada {INV_CADA} pasos (_I), 50 000 (_I50), 100 000 (_I100)')
    print(f"{'brazo':14s} {'n':>2s} {'persiste':>8s} {'K med':>7s} {'K rango':>14s} {'t_ext med':>10s} {'largo':>6s}")
    for b in br:
        v = [D[b][s] for s in sorted(D[b])]
        Ks = [d['K'] for d in v]; te = [d['t_ext'] for d in v if d.get('t_ext')]
        lar = [np.mean([len(x[3]) for x in d['bloques']['vivos_T']]) for d in v if d.get('bloques') and d['bloques'].get('vivos_T')]
        print(f"{b:14s} {len(v):2d} {sum(1 for d in v if d.get('persiste')):5d}/{len(v):<2d} {np.median(Ks):7.2f} {min(Ks):6.2f}-{max(Ks):6.2f} "
              f"{(np.median(te) if te else float('nan')):10.0f} {(np.median(lar) if lar else float('nan')):6.2f}")
    for a, b in [(x + s_, y + s_) for s_ in ('', '50', '100') for x, y in (('BLOQ2_V_I', 'BLOQ_V_I'), ('BLOQ2_V_I', 'BLOQ2_AZA_V_I'),
                                                                        ('BLOQ_V_I', 'ING_SEL_C_V_I'), ('BLOQ2_V_I', 'ING_SEL_C_V_I'))]:
        if a in D and b in D:
            ss = sorted(set(D[a]) & set(D[b])); dd = [D[a][s]['K'] - D[b][s]['K'] for s in ss]
            print(f"  K {a} - {b}: {sum(x > 0 for x in dd)}/{len(dd)} > 0, mediana {np.median(dd):+.2f} ({[round(x, 2) for x in dd]})")
    for b in br:
        if not ARMS[b][1].get('on'): continue
        print(f'--- {b}: organos (formas en >= 50 % de los vivos en T; * activa)')
        for s in sorted(D[b]):
            d = D[b][s]; og = C2.organos(d); vv = d['bloques'].get('vivos_T') or []
            print(f"  s{s}: persiste {d.get('persiste')} K {d['K']:.2f} t_ext {d.get('t_ext')} vivos {len(vv)} inversiones {d['bloques'].get('n_inv')}: " +
                  ' | '.join(f"{'*' if o[4] else ''}{o[0]} {o[1]:.2f} (θ {o[2]:.2f}, w {o[3]:+.2f})" for o in og))
    return D


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False, add_help=False)
    ap.add_argument('--humo', action='store_true'); ap.add_argument('--explora', action='store_true')
    ap.add_argument('--semillas', default=None); ap.add_argument('--brazos', default=None)
    ap.add_argument('--T', type=int, default=500000); ap.add_argument('--carpeta', default=None); ap.add_argument('--lee', default=None)
    a, resto = ap.parse_known_args()
    if resto: raise SystemExit(f'banderas desconocidas: {resto}')
    if a.lee: lee(a.lee if os.path.isabs(a.lee) else os.path.join(CB.DATOS, a.lee)); return
    if a.T > 500000: raise SystemExit('T > 500 000 no se corre aqui')
    verifica()
    if a.humo:
        car = os.path.join(CB.DATOS, 'humo3'); sem = [48995]; brs = ['BLOQ2_V_I']; T = 200000
    elif a.explora:
        car = os.path.join(CB.DATOS, a.carpeta or 'inv'); sem = [int(x) for x in a.semillas.split(',')]; brs = a.brazos.split(','); T = a.T
        for s in sem:
            if s not in SEM and s not in PRACT: raise SystemExit(f'semilla {s} fuera de las declaradas')
    else:
        raise SystemExit('usa --humo, --explora o --lee')
    for b in brs:
        if b not in ARMS: raise SystemExit(f'brazo desconocido {b}')
    t0 = time.time()
    for s in sem:
        for b in brs:
            o = CB.corre(s, b, T, car)
            og = C2.organos(o) if o.get('bloques') else []
            print(f"[{time.strftime('%H:%M:%S')}] {b} s{s} T{T}: persiste {o['persiste']} · K {o['K']:.2f} · t_ext {o.get('t_ext')} · "
                  f"organos activos {sum(1 for x in og if x[4])} · aborto {o['aborto']} ({o['seg']} s; {time.time() - t0:.0f} s)", flush=True)


if __name__ == '__main__':
    main()
