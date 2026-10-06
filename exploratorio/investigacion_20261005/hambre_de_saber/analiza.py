# -*- coding: utf-8 -*-
"""tablas (mediana [min-max]) y pareadas por semilla: completo vs cada rival.  Uso: python analiza.py datos/honesto.json ..."""
import json, sys
import numpy as np

def mr(v, f='{:.2f}'):
    v = [x for x in v if x is not None]
    if not v: return '—'
    return (f + ' [' + f + '–' + f + ']').format(np.median(v), min(v), max(v))

def pareada(res, a, b, key, mayor_mejor=True):
    g = p = 0; d = []
    for s in res:
        if a not in res[s] or b not in res[s]: continue
        x, y = res[s][a].get(key), res[s][b].get(key)
        if x is None or y is None: continue
        d.append(x - y)
        if (x > y) == mayor_mejor and x != y: g += 1
        elif x != y: p += 1
    return g, p, (float(np.median(d)) if d else 0.0)

def tabla(path):
    D = json.load(open(path, encoding='utf-8')); res = D['res']; brazos = D['brazos']
    out = [f"\n## {D['regimen']} (T={D['T']}, K={D['K']}, {len(res)} semillas, extra={D['extra']})\n"]
    cols = [('acierto', 'acierto fin'), ('errores', 'errores fin'), ('abstiene', 'abstiene'), ('mentiras', 'mentiras creídas'),
            ('acierto_medio', 'acierto medio (vida)'), ('t_070', 'pasos hasta 0.70'), ('t_cambio', 'pasos hasta enterarse'),
            ('t_det_mentirosa', 'paso rep<0.4 mentirosas'), ('copias_det', 'copias detectadas'), ('grupos_falsos', 'grupos falsos'),
            ('tv_bimodal', 'hip→val bimodal'), ('tv_unimodal', 'hip→val unimodal')]
    out.append('| brazo | ' + ' | '.join(c[1] for c in cols) + ' | prefiere (×azar) fiable/especial/mentirosa/copia_m/ruidosa |')
    out.append('|' + '---|' * (len(cols) + 2))
    for b in brazos:
        fila = [b]
        for k, _ in cols:
            vals = [res[s][b].get(k) for s in res]
            fmt = '{:.0f}' if k in ('mentiras', 't_070', 't_cambio', 't_det_mentirosa', 'copias_det', 'grupos_falsos', 'tv_bimodal', 'tv_unimodal') else '{:.2f}'
            fila.append(mr(vals, fmt))
        pr = lambda tp: np.median([res[s][b]['pref_rel'].get(tp, 0) for s in res])
        fila.append(f"{pr('fiable'):.1f}/{pr('especial'):.1f}/{pr('mentirosa'):.1f}/{pr('copia_m'):.1f}/{pr('ruidosa'):.1f}")
        out.append('| ' + ' | '.join(fila) + ' |')
    # pareadas
    out.append('\nPareadas por semilla, completo vs rival (gana/pierde de %d; mediana de la diferencia):' % len(res))
    for b in brazos:
        if b == 'completo': continue
        partes = []
        for k, mm, nom in [('acierto', True, 'acierto'), ('errores', False, 'errores'), ('mentiras', False, 'mentiras'), ('acierto_medio', True, 'ac.medio'), ('t_cambio', False, 't_cambio')]:
            g, p, d = pareada(res, 'completo', b, k, mm)
            partes.append(f"{nom} {g}/{p} ({d:+.2f})")
        out.append(f"- vs **{b}**: " + '; '.join(partes))
    # amarre: bimodal vs unimodal dentro del completo
    bi = [res[s]['completo']['tv_bimodal'] for s in res]; uni = [res[s]['completo']['tv_unimodal'] for s in res]
    g = sum(1 for x, y in zip(bi, uni) if x is not None and y is not None and x < y)
    out.append(f"- amarre dentro del completo: bimodal valida antes que unimodal en {g}/{len(res)} semillas (bimodal {mr(bi, '{:.0f}')}, unimodal {mr(uni, '{:.0f}')}); n hechos bimodales {mr([res[s]['completo']['n_bimodal'] for s in res], '{:.0f}')}")
    # via de cambio
    from collections import Counter
    for b in ('completo', 'mayoria', 'oraculo'):
        if b in brazos:
            c = Counter(); [c.update(res[s][b]['via_cambio']) for s in res]
            out.append(f"- {b}: primera fuente que trajo el valor nuevo tras un cambio: {dict(c.most_common())}")
    # curva de acierto por checkpoints
    out.append('\nAcierto a lo largo de la vida (mediana; t=50,100,200,300,400,500,599) — eficiencia por ítem consumido (3 ítems/paso):')
    for b in brazos:
        pts = []
        for tq in (49, 99, 199, 299, 399, 499, 599):
            vals = [next((a for (tt, a, e) in res[s][b]['curva'] if tt == tq), None) for s in res]
            pts.append(mr(vals, '{:.2f}').split(' ')[0])
        out.append(f"- {b}: " + ' → '.join(pts))
    if 'sueno_fijo' in brazos:
        out.append('\nSueño: ' + '; '.join(f"{b}: sueños {mr([res[s][b]['suenos'] for s in res], '{:.0f}')}, consolidadas {mr([res[s][b]['consolidadas'] for s in res], '{:.0f}')}, base correcta al final {mr([res[s][b]['base_ok_fin'] for s in res])}" for b in ('completo', 'sueno_fijo', 'sueno_decide')))
    return '\n'.join(out)

def sociedad(path):
    D = json.load(open(path, encoding='utf-8'))
    out = ['\n## sociedad de 3 colonias (col0 a dieta, col1 y col2 honestas; %d semillas)\n' % len(D)]
    out.append('| modo | colonia | acierto fin | errores | abstiene | mentiras creídas | lee a otras colonias | apetito por colonias | rep de colonias |')
    out.append('|---|---|---|---|---|---|---|---|---|')
    for modo in ('sola', 'mutua', 'ciega'):
        for j in range(3):
            r = [D[s][modo][f'col{j}'] for s in D]
            out.append(f"| {modo} | col{j} ({'dieta' if j == 0 else 'honesto'}) | {mr([x['acierto'] for x in r])} | {mr([x['errores'] for x in r])} | {mr([x['abstiene'] for x in r])} | {mr([x['mentiras'] for x in r], '{:.0f}')} | {mr([x['lee_colonias'] for x in r])} | {mr([x['apetito'].get('colonia') for x in r])} | {mr([x['reputacion'].get('colonia') for x in r])} |")
    for j in range(3):
        for modo in ('mutua', 'ciega'):
            g = sum(1 for s in D if D[s][modo][f'col{j}']['mentiras'] > D[s]['sola'][f'col{j}']['mentiras'])
            m = sum(1 for s in D if D[s][modo][f'col{j}']['acierto'] > D[s]['sola'][f'col{j}']['acierto'])
            out.append(f"- col{j} {modo} vs sola: más mentiras en {g}/{len(D)} semillas; más acierto en {m}/{len(D)}")
    return '\n'.join(out)

if __name__ == '__main__':
    txt = []
    for p in sys.argv[1:]:
        txt.append(sociedad(p) if 'sociedad' in p else tabla(p))
    s = '\n'.join(txt); print(s)
    open('datos/tablas.md', 'w', encoding='utf-8').write(s)
