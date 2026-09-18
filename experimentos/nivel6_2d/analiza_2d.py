"""Análisis por regla 10 (EQUIPO.md) de una serie 2D: la puerta de validez V1 (M con todos los sitios) cayó en algunas
semillas de T2/T4; se recalculan los criterios ORIGINALES del §5 y P3b (enmienda 0) por mundo sobre el subconjunto de
semillas válidas (M_llenas == nº de sitios en MAPA) y se reporta el conjunto completo al lado. No simula nada.
Uso: python experimentos/nivel6_2d/analiza_2d.py datos/2d_s21-40_*.json
"""
import json, os, sys, glob, statistics as st

CASO = {'T1': 'rodeo', 'T2': 'h2', 'T3': 'sec', 'T4': 'falso'}
med = lambda xs: st.median(xs) if xs else float('nan')


def analiza(path):
    d = json.load(open(path, encoding='utf-8'))
    por = {}
    for r in d['corridas']:
        if r.get('tipo') == 'T':
            por.setdefault(r['mundo'], {}).setdefault(r['seed'], {})[r['brazo']] = r
    print(os.path.basename(path))
    for mundo in ('T1', 'T4', 'T3', 'T2'):
        k = CASO[mundo]; S = por[mundo]
        R = lambda s, b: S[s][b]['tel']['R'][k]
        nsit = {s: len(S[s]['MAPA']['tel']['sitios']) for s in S}
        val = [s for s in sorted(S) if S[s]['MAPA'].get('M_llenas') == nsit[s] and S[s]['INVERTIDO'].get('M_llenas') == nsit[s]]
        todas = sorted(S)
        for nombre, ss in (('completo', todas), ('validas', val)):
            if not ss:
                print(f"  {mundo} {nombre}: 0 semillas"); continue
            linea = f"  {mundo} {nombre:<8} n={len(ss):>2}  MAPA R {med([R(s,'MAPA') for s in ss]):.3f}  SINMAPA {med([R(s,'SINMAPA') for s in ss]):.3f}  INVERTIDO {med([R(s,'INVERTIDO') for s in ss]):.3f}  pareado MAPA>SINMAPA {sum(R(s,'MAPA')>R(s,'SINMAPA') for s in ss)}/{len(ss)}"
            if mundo == 'T3':
                c2 = lambda s, b: S[s][b]['tel']['come2'][k]
                dif = [c2(s, 'MAPA_borra') - c2(s, 'MAPA') for s in ss]
                linea += (f"  | come2 MAPA {med([c2(s,'MAPA') for s in ss]):.3f} borra_M {med([c2(s,'MAPA_borra') for s in ss]):.3f}"
                          f"  P3b dif>=0.15 en {sum(x>=0.15 for x in dif)}/{len(ss)}  llega_A {med([S[s]['MAPA']['tel']['llega'][k] for s in ss]):.2f}")
            if mundo == 'T2':
                rr = {s: abs(S[s]['MAPA']['tel']['v_B']) / S[s]['MAPA']['tel']['v_A'] for s in ss}
                ven = [s for s in ss if 1.37 < rr[s] < 2.74]
                dif = [R(s, 'MAPA_h2') - R(s, 'MAPA') for s in ven]
                linea += f"  | MAPA_h2 R {med([R(s,'MAPA_h2') for s in ss]):.3f}; ventana V-T2 {len(ven)}/{len(ss)}: dif h2-h1 {med(dif) if dif else float('nan'):.3f}, >=0.15 en {sum(x>=0.15 for x in dif)}/{len(ven)}"
            print(linea)


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    for p in [q for a in sys.argv[1:] for q in sorted(glob.glob(a))] or sorted(glob.glob('datos/2d_s*.json')):
        analiza(p)
