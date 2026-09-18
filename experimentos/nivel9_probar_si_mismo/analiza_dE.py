"""Análisis PREREGISTRADO (enmienda 1 de PREREGISTRO_probar_si_mismo.md, 18 sep 00:35) del brazo dE-TEST — la sorpresa
de dE en la boca — sobre los JSON de datos/. No simula nada; lee 'principal' y aplica los criterios de la enmienda:
  P1'  recup(dE-TEST) mediana <= 0.60 x recup(V13) y pareado (dE < V13) >= 14/20
  P4'  se apaga solo (forma relativa, adenda 00:40): Q2 <= 0.10, Q4 <= 0.10, Q2 <= 0.35*Q3 y Q4 <= 0.35*Q3 en >= 16/20
  P7'  veneno_post mediana <= 4 x V13 y deaths mediana <= 1.5 x V13
Se imprime también SELF-TEST con los mismos cálculos, para comparar. Uso:
  python experimentos/nivel9_probar_si_mismo/analiza_dE.py datos/probar_si_mismo_s41-60_*.json [más]
"""
import json, os, sys, glob, statistics as st

BRAZOS = ('SELF-TEST', 'dE-TEST')


def analiza(path):
    d = json.load(open(path, encoding='utf-8'))
    por = {}
    for r in d['principal']:
        if r.get('tipo') == 'T':
            por.setdefault(r['seed'], {})[r['brazo']] = r
    seeds = sorted(s for s in por if 'V13' in por[s] and all(b in por[s] for b in BRAZOS))
    med = lambda xs: st.median(xs) if xs else float('nan')
    v13_rec = med([por[s]['V13']['recup'] for s in seeds])
    v13_ven = med([por[s]['V13']['veneno_post'] for s in seeds])
    v13_dea = med([por[s]['V13']['deaths'] for s in seeds])
    out = {}
    for b in BRAZOS:
        rec = med([por[s][b]['recup'] for s in seeds])
        par = sum(por[s][b]['recup'] < por[s]['V13']['recup'] for s in seeds)
        apaga = sum(1 for s in seeds if (por[s][b]['sesgo_boca'][1] <= 0.10 and por[s][b]['sesgo_boca'][3] <= 0.10
                                         and por[s][b]['sesgo_boca'][1] <= 0.35 * por[s][b]['sesgo_boca'][2]
                                         and por[s][b]['sesgo_boca'][3] <= 0.35 * por[s][b]['sesgo_boca'][2]))
        ven = med([por[s][b]['veneno_post'] for s in seeds]); dea = med([por[s][b]['deaths'] for s in seeds])
        out[b] = dict(n=len(seeds), razon=rec / v13_rec if v13_rec else float('nan'), rec=rec, pareado=par, apaga=apaga,
                      ven=ven, dea=dea,
                      P1=(rec <= 0.60 * v13_rec and par >= 14), P4=(apaga >= 16),
                      P7=(ven <= 4 * v13_ven and dea <= 1.5 * v13_dea))
    return os.path.basename(path), v13_rec, out


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    rutas = [p for a in sys.argv[1:] for p in sorted(glob.glob(a))] or sorted(glob.glob('datos/probar_si_mismo_s*.json'))
    for p in rutas:
        nombre, v13_rec, out = analiza(p)
        print(f"{nombre}  (V13 recup mediana {v13_rec:.0f})")
        for b, f in out.items():
            print(f"   {b:<9} n={f['n']}  recup {f['rec']:.0f} ({f['razon']:.3f}x)  pareado<V13 {f['pareado']}/{f['n']}  "
                  f"se apaga {f['apaga']}/{f['n']}  veneno_post {f['ven']:.1f}  muertes {f['dea']:.1f}  ->  "
                  f"P1' {'OK' if f['P1'] else 'NO'}  P4' {'OK' if f['P4'] else 'NO'}  P7' {'OK' if f['P7'] else 'NO'}")
