# EXPLORATORIO, no es dato
"""corre_fable.py — runner EXPLORATORIO de mundos que cambian: CODIGO vs PERILLAS (vs CODIGO_SIN_SOS) en el MISMO mundo y semilla.
(Fable, equipo organelos, 24-sep-2026). MISION: llegar a la AGI por este camino.

Reusa corre_codigo.trabajo() SIN tocarlo: en este proceso se le cambia el motor (MC -> motor_fable) y eco_de (agrega el spec del mundo).
Un proceso por invocacion, sin Pool. Semillas 28001-28999.

Uso:
  python corre_fable.py --mundo golpe --semillas 28001,28002,28003 --brazos CODIGO,PERILLAS [--tl corto|medio]
  python corre_fable.py --lee                       # tabla de todos los mundos en datos/
"""
import argparse, glob, json, os, sys, time
import numpy as np
AQUI = os.path.dirname(os.path.abspath(__file__)); CODIGO = os.path.dirname(AQUI)
for d in (AQUI, CODIGO):
    if d not in sys.path: sys.path.insert(0, d)
import corre_codigo as CC
import motor_fable as MF
import fable_mundos as FB

DATOS = os.path.join(AQUI, 'datos')
TLS = dict(corto=dict(T=36000, t_cambio=8000, t_corte=24000, r0_margen=4000),
           medio=dict(T=50000, t_cambio=10000, t_corte=34000, r0_margen=5000))
BRAZOS_OK = ('CODIGO', 'PERILLAS', 'CODIGO_SIN_SOS', 'MUT0', 'AZAR', 'QUIETO')

_eco_de0 = CC.eco_de
_SPEC = [None]; _ULT = [None]


def eco_de_fable(brazo, t_corte, t_cambio, **extra):
    e = _eco_de0(brazo, t_corte, t_cambio, **extra)
    if brazo != 'QUIETO' and _SPEC[0] is not None: e['cambio'] = dict(_SPEC[0]); _ULT[0] = e['cambio']   # copia por corrida (estado de 'reina')
    return e


CC.MC = MF; CC.eco_de = eco_de_fable   # monkeypatch SOLO en este proceso


def corre(mundo, semillas, brazos, tl_nombre):
    tl = dict(TLS[tl_nombre]); spec = FB.catalogo(tl['t_cambio'])[mundo]; _SPEC[0] = spec
    carpeta = os.path.join(DATOS, f"{mundo}_{tl_nombre}"); os.makedirs(carpeta, exist_ok=True)
    flog = open(os.path.join(carpeta, 'progreso.log'), 'a', encoding='utf-8')
    def log(s):
        s = f"[{time.strftime('%H:%M:%S')}] {s}"; print(s, flush=True); flog.write(s + '\n'); flog.flush()
    log(f"EXPLORATORIO FABLE mundo {mundo} {spec} · {tl} · brazos {brazos} · semillas {semillas}")
    for s in semillas:
        for b in brazos:
            fin = os.path.join(carpeta, f"{b}_s{s}.json")
            if os.path.exists(fin): log(f"ya existe {os.path.basename(fin)}"); continue
            x = CC.trabajo((s, b, tl, carpeta, False))
            x['mundo_fable'] = dict(nombre=mundo, spec=spec, estado=((_ULT[0] or {}).get('_st') if _ULT[0] is not None else None))
            with open(fin, 'w', encoding='utf-8') as f: json.dump(x, f)
            log(resumen(x))
    flog.close()


def medidas(x):
    """Medidas EXPLORATORIAS por corrida, desde ventanas_r0 = [inicio, R0, nacidos] por 2000 pasos."""
    tl = x['tl']; V = x.get('ventanas_r0') or []; n = {v[0]: v[2] for v in V}; W = CC.W_NAC
    tc, tk, T, mg = tl['t_cambio'], tl['t_corte'], tl['T'], tl['r0_margen']
    pre = [n.get(a, 0) for a in range(tc - 3 * W, tc, W) if a >= 0]
    post = [n.get(a, 0) for a in range(tc, tk, W)]
    solo = [n.get(a, 0) for a in range(tk, T - mg, W)]
    Bp = float(np.mean(pre)) if pre else 0.0
    return dict(persiste=int(x.get('persiste') or 0), vivos_T=x.get('vivos_T'), t_ext=x.get('t_ext'),
                r0_final=(x.get('r0_final') if x.get('r0_final') is not None else 0.0), n_final=x.get('n_final'),
                B_pre=round(Bp, 1), nac_post_rel=(round(float(np.mean(post)) / Bp, 3) if Bp > 0 and post else None),
                nac_solo=int(sum(solo)), t_rec=x.get('t_rec'),
                sos_pre=((x.get('nac_pre') or {}).get('sos_frac')), sos_post=((x.get('nac_post') or {}).get('sos_frac')),
                seg=x.get('seg'))


def resumen(x):
    m = medidas(x)
    return (f"{x['brazo']:<15} s{x['seed']}: {m['seg']} s · persiste {m['persiste']} (vivos {m['vivos_T']}, t_ext {m['t_ext']}) · B_pre {m['B_pre']} · "
            f"nac post/pre {m['nac_post_rel']} · t_rec {m['t_rec']} · R0 final solo {m['r0_final']} (n {m['n_final']}) · nac solo {m['nac_solo']} · SOS {m['sos_pre']}->{m['sos_post']}")


def lee(solo=None):
    filas = []
    for carpeta in sorted(glob.glob(os.path.join(DATOS, '*'))):
        if not os.path.isdir(carpeta): continue
        if solo and os.path.basename(carpeta) not in solo: continue
        R = [json.load(open(p, encoding='utf-8')) for p in sorted(glob.glob(os.path.join(carpeta, '*_s*.json')))]
        R = [x for x in R if not x.get('abortado')]
        if not R: continue
        by = {}
        for x in R: by.setdefault(x['brazo'], {})[x['seed']] = medidas(x)
        nombre = os.path.basename(carpeta)
        print(f"\n== {nombre}  spec {R[0].get('mundo_fable', {}).get('spec')}  TL {R[0]['tl']}")
        for b, d in by.items():
            ss = sorted(d)
            print(f"  {b:<15} n {len(ss):2d} · persiste {sum(d[s]['persiste'] for s in ss)}/{len(ss)} · R0 final med {np.median([d[s]['r0_final'] for s in ss]):.3f} "
                  f"· nac post/pre med {np.median([d[s]['nac_post_rel'] or 0 for s in ss]):.3f} · nac solo med {np.median([d[s]['nac_solo'] for s in ss]):.0f} "
                  f"· t_rec {[d[s]['t_rec'] for s in ss]} · SOS post med {np.median([d[s]['sos_post'] or 0 for s in ss]):.3f}")
        if 'CODIGO' in by and 'PERILLAS' in by:
            com = sorted(set(by['CODIGO']) & set(by['PERILLAS']))
            g_r0 = sum(int(by['CODIGO'][s]['r0_final'] > by['PERILLAS'][s]['r0_final']) for s in com)
            e_r0 = sum(int(by['CODIGO'][s]['r0_final'] == by['PERILLAS'][s]['r0_final']) for s in com)
            g_nac = sum(int((by['CODIGO'][s]['nac_post_rel'] or 0) > (by['PERILLAS'][s]['nac_post_rel'] or 0)) for s in com)
            g_solo = sum(int(by['CODIGO'][s]['nac_solo'] > by['PERILLAS'][s]['nac_solo']) for s in com)
            g_p = sum(by['CODIGO'][s]['persiste'] for s in com) - sum(by['PERILLAS'][s]['persiste'] for s in com)
            print(f"  CODIGO vs PERILLAS ({len(com)} semillas): gana R0 final {g_r0} (empata {e_r0}) · gana nac post/pre {g_nac} · gana nac solo {g_solo} · persistencia dif {g_p:+d}")
            if 'CODIGO_SIN_SOS' in by:
                com2 = sorted(set(by['CODIGO']) & set(by['CODIGO_SIN_SOS']))
                print(f"  CODIGO vs SIN_SOS ({len(com2)}): gana R0 final {sum(int(by['CODIGO'][s]['r0_final'] > by['CODIGO_SIN_SOS'][s]['r0_final']) for s in com2)} · "
                      f"gana nac solo {sum(int(by['CODIGO'][s]['nac_solo'] > by['CODIGO_SIN_SOS'][s]['nac_solo']) for s in com2)}")
            filas.append((nombre, len(com), g_r0, g_nac, g_solo, g_p))
    return filas


def tabla_md():
    """La tabla (a) de HALLAZGOS.md: una fila por mundo. Celda por brazo: persiste/n · R0 final mediana · nac solo mediana · t_rec mediana (cens = 16001)."""
    print("| mundo | parámetros | semillas | CODIGO | PERILLAS | CODIGO_SIN_SOS | CODIGO vs PERILLAS (R0 final, pareado) | nac solo (pareado) | persist. dif | ganador |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    def cel(d):
        if not d: return '—'
        ss = sorted(d); tr = [d[s]['t_rec'] if d[s]['t_rec'] is not None else 16001 for s in ss]
        return (f"{sum(d[s]['persiste'] for s in ss)}/{len(ss)} · R0 {np.median([d[s]['r0_final'] for s in ss]):.2f} · "
                f"nac solo {np.median([d[s]['nac_solo'] for s in ss]):.0f} · t_rec {np.median(tr):.0f}")
    for carpeta in sorted(glob.glob(os.path.join(DATOS, '*'))):
        if not os.path.isdir(carpeta): continue
        R = [json.load(open(p, encoding='utf-8')) for p in sorted(glob.glob(os.path.join(carpeta, '*_s*.json')))]
        R = [x for x in R if not x.get('abortado')]
        if not R: continue
        by = {}
        for x in R: by.setdefault(x['brazo'], {})[x['seed']] = medidas(x)
        spec = dict(R[0].get('mundo_fable', {}).get('spec') or {}); spec.pop('t', None); tipo = spec.pop('tipo', '?')
        com = sorted(set(by.get('CODIGO', {})) & set(by.get('PERILLAS', {})))
        g = sum(int(by['CODIGO'][s]['r0_final'] > by['PERILLAS'][s]['r0_final']) for s in com)
        gs = sum(int(by['CODIGO'][s]['nac_solo'] > by['PERILLAS'][s]['nac_solo']) for s in com)
        dp = sum(by['CODIGO'][s]['persiste'] for s in com) - sum(by['PERILLAS'][s]['persiste'] for s in com)
        n = len(com)
        if n and g >= n - (0 if n <= 3 else 1) and gs >= n / 2 and dp >= 0: gan = '**CODIGO**'
        elif n and g <= 1 and gs <= n / 2 - 1: gan = 'PERILLAS'
        else: gan = 'empate / ruido'
        sem = f"{min(com)}–{max(com)} ({n})" if com else '—'
        print(f"| {os.path.basename(carpeta).replace('_corto', '')} | {tipo} {spec if spec else ''} | {sem} | {cel(by.get('CODIGO'))} | {cel(by.get('PERILLAS'))} | "
              f"{cel(by.get('CODIGO_SIN_SOS'))} | {g}/{n} | {gs}/{n} | {dp:+d} | {gan} |")


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--mundo'); ap.add_argument('--semillas', default='28001,28002,28003'); ap.add_argument('--brazos', default='CODIGO,PERILLAS')
    ap.add_argument('--tl', default='corto'); ap.add_argument('--lee', action='store_true'); ap.add_argument('--solo', default=None); ap.add_argument('--md', action='store_true')
    a = ap.parse_args()
    if a.md: tabla_md(); sys.exit(0)
    if a.lee: lee(a.solo.split(',') if a.solo else None); sys.exit(0)
    sem = [int(s) for s in a.semillas.split(',')]; br = a.brazos.split(',')
    if any(not 28001 <= s <= 28999 for s in sem): raise SystemExit('FABLE: semillas 28001-28999')
    if any(b not in BRAZOS_OK for b in br): raise SystemExit(f'FABLE: brazos {BRAZOS_OK}')
    corre(a.mundo, sem, br, a.tl)
