"""corre_g50.py — RUNNER de 50 GENES (Opus G, 28-sep-2026, EXPLORATORIO; sin Pool: cada proceso corre su lista en serie).

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas); el metodo manda sobre el como.

La corrida es nucleo_g50.trabajo (construido por anclas; arnes identidad_g50.py). La medida (kbar) se IMPORTA de
eco_sel_ing/corre_eco_sel_ing.py (la misma funcion; K_nac y fund_2a los da el nucleo). Brazos:
  ING_F1 (sin mutacion) · ING_SEL_C (15, la referencia) · ING_SEL_25 (15 + 10 del cerebro) · ING_SEL_47 (50 sin historia de vida)
  · ING_SEL_50 (los 50) · ING_AZA_50 (los 50 SIN herencia).
GUARDIA (declarada antes de los numeros): TOPE COMPUTACIONAL 600 cuerpos (la base usa 3000; su max_vivos ronda 120, asi que con la base
no cambia nada). Una corrida con bloqueados > 0 alcanzo el tope: la historia de vida se disparo -> NO EVALUABLE (se dice, no se esconde).

Uso:
  python corre_g50.py --humo                                               # 1 proceso, 48895, ING_SEL_C / ING_SEL_50 / ING_AZA_50, T 200 000
  python corre_g50.py --explora --semillas 48801-48810 --brazos ING_SEL_50,ING_F1 --T 500000 --tag p1   # UN proceso, en serie
  python corre_g50.py --lee datos/explora_T500000
"""
import argparse, glob, hashlib, importlib.util, json, os, sys, time
import numpy as np

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
if AQUI not in sys.path: sys.path.insert(0, AQUI)


def _carga(nombre, ruta):
    spec = importlib.util.spec_from_file_location(nombre, ruta); m = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = m; spec.loader.exec_module(m); return m


BASE_RUNNER = os.path.join(EXP, 'organelos', 'eco_sel_ing', 'corre_eco_sel_ing.py')
CB = _carga('corre_eco_sel_ing', BASE_RUNNER)   # solo por kbar (la misma funcion de la base)
import nucleo_g50 as N
import construye_g50 as CG
kbar = CB.kbar
TOPE_G50 = 600
DATOS = os.path.join(AQUI, 'datos')
REF = 'ING_SEL_C'
BRAZOS_OK = ('ING_F1', 'ING_SEL_C', 'ING_AZA_C', 'ING_SEL_25', 'ING_SEL_47', 'ING_AZA_47', 'ING_SEL_50', 'ING_AZA_50', 'ING_SEL_C_V', 'ING_SEL_47_V', 'ING_AZA_47_V')


def prepara():
    if not CG.main(['--verifica']): raise SystemExit('corre_g50: los archivos no son los construidos por anclas')
    N.MUNDO['tope'] = TOPE_G50
    N.usa_gemelo()


def linea(r, T):
    return (f"{r['brazo']} s{r['seed']}: {r['seg']} s · K {None if r.get('tam_total') is None else round(kbar(r, T), 2)} · K_nac {r.get('K_nac')} · "
            f"fund_2a {r.get('fund_2a')} · n_nac {r.get('n_nac')} · max_vivos {r.get('max_vivos')} · bloqueados {r.get('bloqueados')} · "
            f"persiste {r.get('persiste')} · aborto {r.get('aborto')}")


def corre_lista(jobs, carpeta, log):
    R = []
    for s, b, T in jobs:
        r = N.trabajo((s, b, T, N.tc_de(b, T), N.FRIO['T_lect'], carpeta, True)); R.append(r); log(linea(r, T))
    return R


def humo():
    prepara()
    T = N.HUMO['T']; s = N.HUMO['semilla']
    carpeta = os.path.join(DATOS, 'humo', f"g50_humo_s{s}_T{T}_{time.strftime('%Y%m%d_%H%M%S')}"); os.makedirs(carpeta, exist_ok=True)
    t0 = time.time()
    R = corre_lista([(s, b, T) for b in ('ING_SEL_C', 'ING_SEL_50', 'ING_AZA_50')], carpeta,
                    lambda z: print(f"[{time.strftime('%H:%M:%S')}] {z}", flush=True))
    res = dict(humo=dict(semilla=s, T=T), tope=TOPE_G50, R=[{k: v for k, v in r.items() if k not in ('gen_t', 'vivos_final', 'tam_total', 'vivos_t')}
                                                       | dict(K=kbar(r, T)) for r in R], seg=round(time.time() - t0, 1))
    ruta = carpeta + '.json'; json.dump(res, open(ruta, 'w', encoding='utf-8'), default=str)
    print(f"JSON {ruta} ({res['seg']} s)")


def _semillas(txt):
    """'48801-48804' (rango) o '48801,48805' (lista)."""
    if '-' in txt:
        s0, s1 = [int(x) for x in txt.split('-')]; return list(range(s0, s1 + 1))
    return [int(x) for x in txt.split(',')]


def explora(a):
    prepara()
    sems = _semillas(a.semillas)
    brazos = a.brazos.split(',')
    if set(brazos) - set(BRAZOS_OK): raise SystemExit(f"corre_g50: brazos desconocidos {set(brazos) - set(BRAZOS_OK)}")
    carpeta = os.path.join(DATOS, f"explora_T{a.T}"); os.makedirs(carpeta, exist_ok=True)
    flog = open(os.path.join(carpeta, f"progreso_{a.tag}.log"), 'a', encoding='utf-8')

    def log(z):
        z = f"[{time.strftime('%H:%M:%S')}] {z}"; print(z, flush=True); flog.write(z + '\n'); flog.flush()
    log(f"EXPLORA {a.tag}: semillas {sems} · brazos {brazos} · T {a.T} · tope {TOPE_G50} · shas "
        f"{ {f: CG.h16(os.path.join(AQUI, f)) for f in ('motor_eco50.py', 'motor_g50.py', 'nucleo_g50.py', 'corre_g50.py')} }")
    corre_lista([(s, b, a.T) for s in sems for b in brazos], carpeta, log)
    log('FIN'); flog.close()


def lee(carpeta, T=None):
    R = [json.load(open(p, encoding='utf-8')) for p in sorted(glob.glob(os.path.join(carpeta, '*_s*.json')))]
    if not R: print('sin resultados'); return
    T = T or R[0]['T']
    by = {}
    for r in R: by.setdefault(r['brazo'], {})[r['seed']] = r
    ev = lambda r: (r.get('aborto') is None and int(r.get('bloqueados') or 0) == 0)
    out = []
    P = lambda z: (print(z), out.append(z))
    P(f"T {T} · brazos {sorted(by)} · semillas por brazo { {b: len(v) for b, v in by.items()} }")
    REF_ = REF if REF in by else 'ING_SEL_C_V'
    ref = by.get(REF_, {})
    for b in [x for x in BRAZOS_OK if x in by]:
        v = by[b]; ss = sorted(v)
        K = {s: kbar(v[s], T) for s in ss if ev(v[s])}; Kn = {s: v[s].get('K_nac') for s in ss if ev(v[s])}
        F2 = {s: v[s].get('fund_2a') for s in ss if ev(v[s])}
        nev = [s for s in ss if not ev(v[s])]
        med = lambda d: round(float(np.median(list(d.values()))), 2) if d else None
        z = (f"{b:11s} n {len(ss)} (NO EVALUABLES por tope/aborto: {nev}) · K {med(K)} · K_nac {med(Kn)} · fund_2a {med(F2)} · "
             f"persiste {sum(int(v[s].get('persiste') or 0) for s in ss)}/{len(ss)} · n_nac {round(float(np.median([v[s]['n_nac'] for s in ss])))} · max_vivos {max(v[s].get('max_vivos') or 0 for s in ss)}")
        if b != REF_ and ref:
            com = [s for s in K if s in ref and ev(ref[s])]
            dK = [K[s] - kbar(ref[s], T) for s in com]; dKn = [Kn[s] - ref[s]['K_nac'] for s in com]
            dF = [F2[s] - ref[s]['fund_2a'] for s in com]
            if com:
                z += (f" || vs {REF_} (pareado, {len(com)}): K gana {sum(d > 0 for d in dK)}/{len(com)} (med {round(float(np.median(dK)), 2)}) · "
                      f"K_nac gana {sum(d > 0 for d in dKn)}/{len(com)} (med {round(float(np.median(dKn)), 2)}) · "
                      f"fund_2a menos {sum(d < 0 for d in dF)}/{len(com)} (med {round(float(np.median(dF)))})")
        P(z)
    # genes de los vivos en T: log(g/G0) mediana por gen en los brazos de 50 (cuales se movieron)
    for b in ('ING_SEL_50', 'ING_AZA_50', 'ING_SEL_47', 'ING_AZA_47', 'ING_SEL_25'):
        if b not in by: continue
        v = [r for r in by[b].values() if r.get('genes_vivos_T')]
        if not v: continue
        G0 = dict(zip(v[0]['genes'], v[0]['G0']))
        lg = {g: float(np.median([np.log(r['genes_vivos_T'][g] / G0[g]) for r in v])) for g in v[0]['genes_vivos_T']}
        top = sorted(lg.items(), key=lambda kv: -abs(kv[1]))[:10]
        P(f"{b} genes vivos en T, mediana de log(g/G0), los 10 que mas se mueven: " + ', '.join(f"{g} {x:+.2f}" for g, x in top))
    json.dump(dict(lineas=out), open(os.path.join(carpeta, 'RESUMEN_lee.json'), 'w', encoding='utf-8'), indent=1)


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--humo', action='store_true'); ap.add_argument('--explora', action='store_true'); ap.add_argument('--lee', default=None)
    ap.add_argument('--semillas'); ap.add_argument('--brazos'); ap.add_argument('--T', type=int); ap.add_argument('--tag', default='x')
    a = ap.parse_args()
    if a.humo: humo()
    elif a.explora:
        if not all(48801 <= x <= 48810 for x in _semillas(a.semillas)): raise SystemExit('corre_g50: exploracion solo con 48801-48810')
        explora(a)
    elif a.lee: lee(a.lee)
    else: raise SystemExit('corre_g50: --humo | --explora | --lee')


if __name__ == '__main__':
    main()
