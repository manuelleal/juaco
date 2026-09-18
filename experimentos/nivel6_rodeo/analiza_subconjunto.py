"""Análisis PREREGISTRADO (enmienda 1 de PREREGISTRO_rodeo.md, escrita antes de la serie 61-80) sobre el SUBCONJUNTO
VÁLIDO de semillas de una serie de rodeo. No simula nada: lee los JSON de `datos/` y aplica la enmienda tal cual.

Semilla VÁLIDA  <=>  V0: el mecanismo predice rodeo en el brazo MAPA, `v_B < -0.308 * v_A` (desigualdad en dp = 4)
                 y  V1: la tabla M del brazo MAPA tiene los tres sitios (`M_llenas == 3`).
Criterios de la enmienda (sobre el subconjunto): válidas >= 12; R1 rodeo mediana >= 0.70; pareado MAPA > SINMAPA en
>= 75 % del subconjunto; R2 atajo >= 0.70; llega sin pisar veneno >= 0.60. El conjunto completo se imprime al lado.

Uso:  python experimentos/nivel6_rodeo/analiza_subconjunto.py datos/rodeo_s41-60_*.json datos/rodeo_s61-80_*.json
(Añadido tras la auditoría del día 7, hallazgo 2: el análisis se había hecho en línea; aquí queda reproducible.)
"""
import json, os, sys, glob, statistics as st

UMBRAL_V0 = 0.308
MIN_VALIDAS, MIN_R1, MIN_PAREADO, MIN_R2, MIN_LLEGA = 12, 0.70, 0.75, 0.70, 0.60


def analiza(path):
    d = json.load(open(path, encoding='utf-8'))
    por = {}
    for r in d['corridas']:
        if r.get('tipo') == 'T':
            por.setdefault(r['seed'], {})[r['brazo']] = r
    seeds = sorted(s for s in por if 'MAPA' in por[s] and 'SINMAPA' in por[s])

    def valida(s):
        t = por[s]['MAPA']['tel']
        return t['v_B'] < -UMBRAL_V0 * t['v_A'] and por[s]['MAPA'].get('M_llenas') == 3

    def tel(s, b, k): return por[s][b]['tel'][k]
    val = [s for s in seeds if valida(s)]
    nov = [s for s in seeds if s not in val]
    med = lambda xs: st.median(xs) if xs else float('nan')
    fila = dict(
        archivo=os.path.basename(path), n=len(seeds), validas=len(val),
        R1_val=med([tel(s, 'MAPA', 'R1') for s in val]),
        pareado=sum(tel(s, 'MAPA', 'R1') > tel(s, 'SINMAPA', 'R1') for s in val),
        R2_val=med([tel(s, 'MAPA', 'R2') for s in val]),
        llega_val=med([tel(s, 'MAPA', 'llega_limpio') for s in val]),
        R1_noval=med([tel(s, 'MAPA', 'R1') for s in nov]),
        R1_todas=med([tel(s, 'MAPA', 'R1') for s in seeds]),
        pareado_todas=sum(tel(s, 'MAPA', 'R1') > tel(s, 'SINMAPA', 'R1') for s in seeds),
        R1_inv=med([tel(s, 'INVERTIDO', 'R1') for s in seeds if 'INVERTIDO' in por[s]]),
    )
    fila['PASA'] = (fila['validas'] >= MIN_VALIDAS and fila['R1_val'] >= MIN_R1
                    and fila['pareado'] >= MIN_PAREADO * fila['validas'] and fila['R2_val'] >= MIN_R2
                    and fila['llega_val'] >= MIN_LLEGA)
    return fila


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    rutas = [p for a in sys.argv[1:] for p in sorted(glob.glob(a))]
    if not rutas:
        rutas = sorted(glob.glob('datos/rodeo_s*.json'))
    print('serie                              | n  | validas | R1 val | pareado | R2 val | llega | R1 no val | R1 todas | pareado todas | R1 inv | ')
    for p in rutas:
        f = analiza(p)
        print(f"{f['archivo']:<34} | {f['n']:>2} | {f['validas']:>2}/{f['n']:<4} | {f['R1_val']:.3f}  | {f['pareado']:>2}/{f['validas']:<4} | "
              f"{f['R2_val']:.3f}  | {f['llega_val']:.3f} | {f['R1_noval']:.3f}     | {f['R1_todas']:.3f}    | {f['pareado_todas']:>2}/{f['n']:<11} | "
              f"{f['R1_inv']:.3f}  | {'PASA' if f['PASA'] else 'NO PASA'}")
