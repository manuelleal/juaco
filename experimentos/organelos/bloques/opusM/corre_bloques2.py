"""corre_bloques2.py — runner EXPLORATORIO del KIT GRANDE de BLOQUES (Opus M, 28-sep-2026, noche; canal bloques/CANAL.md).
Mision: llegar a la AGI por este camino. Pregunta del director: "¿y si le damos mas cosas?".

Reutiliza corre_bloques.py (sha a090b82eae9f1ee3, el de la serie FUNCIONA x2) IMPORTADO: corre(), trabajo() del nucleo, K, persistencia,
vivero finito (t_corte 100 000). Cambia solo el gemelo: motor_bloques2 (kit = 1 == motor_bloques bit a bit, arnes) para TODOS los brazos.
Brazos: BLOQ_V (kit actual, referencia) · BLOQ2_V (kit grande, heredable) · BLOQ2_AZA_V (kit grande, sin herencia).
Uso (un proceso por llamada; sin Pool):
  python corre_bloques2.py --humo                                   # 48795, T 200 000, BLOQ2_V y BLOQ2_AZA_V
  python corre_bloques2.py --explora --semillas 48701,48702 --brazos BLOQ_V,BLOQ2_V,BLOQ2_AZA_V --T 500000 --carpeta k2
  python corre_bloques2.py --lee k2
"""
import argparse, glob, json, os, sys, time, types
import numpy as np

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import corre_bloques as CB   # noqa: E402
NS = CB.NS
SHAS2 = {os.path.join(AQUI, 'corre_bloques.py'): 'a090b82eae9f1ee3', os.path.join(AQUI, 'motor_bloques.py'): 'ff782697e54585a5',
         os.path.join(AQUI, 'motor_bloques2.py'): 'e365506be24bb490'}
usa_bloques1 = CB.usa_bloques   # el original (motor_bloques): SOLO el arnes


def usa_bloques2():
    import motor_bloques2 as MB
    g = types.ModuleType('motor_bloques2_gemelo')
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


CB.usa_bloques = usa_bloques2   # desde aqui corre() usa motor_bloques2 en TODOS los brazos (kit 1 == motor_bloques, arnes)
CB.DEF.update(kit=1, tope=12)
for _b in ('BLOQ2_V', 'BLOQ2_AZA_V'): NS.BRAZOS[_b] = ('MUT0', CB.FAB, 100000)
CB.BQ.update({'BLOQ2_V': dict(on=1, donante='padre', kit=2, tope=16), 'BLOQ2_AZA_V': dict(on=1, donante='azar', kit=2, tope=16)})
# VIVERO LARGO (anadido 20:57, tras ver k2 y ANTES de correrlo): t_corte 250 000 (el doble y medio de tiempo para encontrar organos
# antes de quedarse sin subsidio); K se mide en [250 000, 500 000], toda la ventana sin subsidio.
for _b, _k in (('BLOQ_VL', 1), ('BLOQ2_VL', 2)): NS.BRAZOS[_b] = ('MUT0', CB.FAB, 250000)
CB.BQ.update({'BLOQ_VL': dict(on=1, donante='padre'), 'BLOQ2_VL': dict(on=1, donante='padre', kit=2, tope=16)})
SENT = CB.SENT + ['resE', 'resA', 'memF', 'memL', 'vecCerca', 'vecMordio', 'tParto']
ACC = CB.ACC + ['vecino', 'ventana']
SEM = tuple(range(48701, 48709))   # 48701-48708 (grep: 487xx libre salvo 48759)
PRACT = tuple(range(48791, 48796))
FAMILIA = {'boca': 'boca', 'hacia': 'patas', 'quieto': 'patas', 'vecino': 'social', 'parir': 'parto', 'ventana': 'parto'}


def tipo2(r):
    s, p, c, th, a, w = r
    s = int(s); a = int(a)
    sen = SENT[s] + (f'{int(p)}' if s in (3, 4) else (f'{"ABCD"[int(p) % 4]}' if s == 9 else ''))
    return f"{sen}{'>' if c > 0.5 else '<'}θ -> {ACC[a]}{'+' if w > 0 else '-'}"


def inerte(r):
    """La condicion no puede cumplirse nunca (sentidos en [0, 1]) o el peso es despreciable."""
    s, p, c, th, a, w = r
    return (c > 0.5 and th >= 0.999) or (c <= 0.5 and th <= 0.001) or abs(w) < 0.3


def organos(d, umbral=0.5):
    """Formas de regla presentes en >= umbral de los vivos en T. Devuelve [(forma, fraccion, theta mediana, w mediano, activa)]."""
    vv = (d.get('bloques') or {}).get('vivos_T') or []
    if not vv: return []
    cnt = {}; th = {}; ws = {}; act = {}
    for x in vv:
        vistos = set()
        for r in x[3]:
            f = tipo2(r)
            th.setdefault(f, []).append(r[3]); ws.setdefault(f, []).append(r[5]); act.setdefault(f, []).append(not inerte(r))
            if f not in vistos: cnt[f] = cnt.get(f, 0) + 1; vistos.add(f)
    out = [(f, c / len(vv), float(np.median(th[f])), float(np.median(ws[f])), float(np.mean(act[f])) >= 0.5) for f, c in cnt.items()
           if c / len(vv) >= umbral]
    return sorted(out, key=lambda z: -z[1])


def verifica():
    for p, h in SHAS2.items():
        if CB.h16(p) != h: raise SystemExit(f'{os.path.basename(p)} cambio: {CB.h16(p)} != {h}')
    CB.verifica()


def lee(carpeta):
    D = {}
    for f in sorted(glob.glob(os.path.join(carpeta, 'M_*.json'))):
        d = json.load(open(f, encoding='utf-8')); D.setdefault(d['brazo'], {})[d['seed']] = d
    br = [b for b in ('BLOQ_V', 'BLOQ2_V', 'BLOQ2_AZA_V', 'BLOQ_VL', 'BLOQ2_VL') if b in D]
    print(f'carpeta {carpeta}')
    print(f"{'brazo':12s} {'n':>2s} {'persiste':>8s} {'K med':>7s} {'K rango':>14s} {'largo':>6s} {'organos act (med)':>18s} {'rechazo':>8s}")
    for b in br:
        v = [D[b][s] for s in sorted(D[b])]
        per = sum(1 for d in v if d.get('persiste'))
        Ks = [d['K'] for d in v]
        lar = [np.mean([len(x[3]) for x in d['bloques']['vivos_T']]) for d in v if d['bloques'].get('vivos_T')]
        no = [sum(1 for o in organos(d) if o[4]) for d in v if d['bloques'].get('vivos_T')]
        rj = [d.get('frac_rechazo') for d in v]
        print(f"{b:12s} {len(v):2d} {per:5d}/{len(v):<2d} {np.median(Ks):7.2f} {min(Ks):6.2f}-{max(Ks):6.2f} "
              f"{(np.median(lar) if lar else float('nan')):6.2f} {(np.median(no) if no else float('nan')):18.1f} "
              f"{sum(1 for f in rj if f is not None and f >= 0.5):5d}/{len(v)}")
    for a, b in (('BLOQ2_V', 'BLOQ_V'), ('BLOQ2_V', 'BLOQ2_AZA_V'), ('BLOQ2_VL', 'BLOQ_VL')):
        if a in D and b in D:
            ss = sorted(set(D[a]) & set(D[b])); dd = [D[a][s]['K'] - D[b][s]['K'] for s in ss]
            print(f"  K {a} - {b}: {sum(x > 0 for x in dd)}/{len(dd)} > 0, mediana {np.median(dd):+.2f} ({[round(x, 2) for x in dd]})")
    for b in br:
        print(f'--- {b}: organos (formas en >= 50 % de los vivos en T; * = activa: theta alcanzable y |w| >= 0.3)')
        fam_tot = {}
        for s in sorted(D[b]):
            d = D[b][s]; og = organos(d)
            fams = sorted(set(FAMILIA[o[0].split('-> ')[1][:-1]] for o in og if o[4]))
            for f_ in fams: fam_tot[f_] = fam_tot.get(f_, 0) + 1
            vv = d['bloques'].get('vivos_T') or []
            print(f"  s{s}: persiste {d.get('persiste')} K {d['K']:.2f} vivos {len(vv)} · {sum(1 for o in og if o[4])} activos {fams}: " +
                  ' | '.join(f"{'*' if o[4] else ''}{o[0]} {o[1]:.2f} (θ {o[2]:.2f}, w {o[3]:+.2f})" for o in og))
        print(f'  familias con organo activo (semillas): {fam_tot}')
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
        car = os.path.join(CB.DATOS, 'humo2'); sem = [48795]; brs = ['BLOQ2_V', 'BLOQ2_AZA_V']; T = 200000
    elif a.explora:
        car = os.path.join(CB.DATOS, a.carpeta or 'k2'); sem = [int(x) for x in a.semillas.split(',')]; brs = a.brazos.split(','); T = a.T
        for s in sem:
            if s not in SEM and s not in PRACT: raise SystemExit(f'semilla {s} fuera de las declaradas')
    else:
        raise SystemExit('usa --humo, --explora o --lee')
    for b in brs:
        if b not in ('BLOQ_V', 'BLOQ2_V', 'BLOQ2_AZA_V', 'BLOQ_VL', 'BLOQ2_VL'): raise SystemExit(f'brazo desconocido {b}')
    t0 = time.time()
    for s in sem:
        for b in brs:
            o = CB.corre(s, b, T, car)
            og = organos(o)
            print(f"[{time.strftime('%H:%M:%S')}] {b} s{s} T{T}: persiste {o['persiste']} · K {o['K']:.2f} · rechazo {o.get('frac_rechazo')} · "
                  f"organos activos {sum(1 for x in og if x[4])} · aborto {o['aborto']} ({o['seg']} s; {time.time() - t0:.0f} s)", flush=True)


if __name__ == '__main__':
    main()
