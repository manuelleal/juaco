# EXPLORATORIO, no es dato
"""dibuja.py — HTML estático con SVG inline: poblaciones de las 4 especies, veneno vs escudo, velocidades, fotos del mundo 2D.
Uso: python dibuja.py datos/EVO_32001.json [más json...]  → cadena_<brazo>_<seed>.html por cada uno + tabla en datos/TABLA.md
Sin dependencias fuera de la biblioteca estándar."""
import json, sys, os, math

COL = {'gusano': '#c9a227', 'gallina': '#d9553f', 'oso': '#5b3a29', 'humano': '#2b6cb0'}
NOM = ('gusano', 'gallina', 'oso', 'humano')
W, H, ML, MB, MT = 860, 260, 60, 34, 26


def _lin(t, ys, ymax, ymin=0.0, log=False):
    n = len(t); tmax = max(t[-1], 1)
    pts = []
    for x, y in zip(t, ys):
        if y is None or (log and y <= 0): pts.append(None); continue
        yy = math.log10(y) if log else y
        px = ML + (W - ML - 10) * x / tmax
        py = MT + (H - MT - MB) * (1 - (yy - ymin) / (ymax - ymin + 1e-12))
        pts.append((px, py))
    # tramos continuos
    out = []; cur = []
    for p in pts:
        if p is None:
            if cur: out.append(cur); cur = []
        else: cur.append(p)
    if cur: out.append(cur)
    return ' '.join('M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in seg) if len(seg) > 1 else f'M{seg[0][0]:.1f},{seg[0][1]:.1f} l0.1,0' for seg in out)


def panel(titulo, t, series, log=False, ylabel='', ymax=None):
    """series: lista de (nombre, color, ys, dash)."""
    vals = [y for _, _, ys, _ in series for y in ys if y is not None and (not log or y > 0)]
    if not vals: vals = [1]
    if ymax is None: ymax = max(vals) * 1.05
    ymin = 0.0
    if log: ymax = math.log10(max(ymax, 10)); ymin = 0.0
    s = [f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" style="font-family:sans-serif;background:#fbfaf6;border:1px solid #ddd">']
    s.append(f'<text x="{ML}" y="16" font-size="13" font-weight="bold" fill="#222">{titulo}</text>')
    # ejes
    s.append(f'<line x1="{ML}" y1="{MT}" x2="{ML}" y2="{H-MB}" stroke="#888"/><line x1="{ML}" y1="{H-MB}" x2="{W-10}" y2="{H-MB}" stroke="#888"/>')
    nt = 5
    for k in range(nt + 1):
        yy = ymin + (ymax - ymin) * k / nt
        py = MT + (H - MT - MB) * (1 - k / nt)
        lab = f'{10**yy:.0f}' if log else (f'{yy:.2f}' if ymax < 10 else f'{yy:.0f}')
        s.append(f'<text x="{ML-4}" y="{py+4}" font-size="10" text-anchor="end" fill="#555">{lab}</text><line x1="{ML}" y1="{py:.1f}" x2="{W-10}" y2="{py:.1f}" stroke="#eee"/>')
    tmax = max(t[-1], 1)
    for k in range(6):
        px = ML + (W - ML - 10) * k / 5
        s.append(f'<text x="{px:.1f}" y="{H-MB+14}" font-size="10" text-anchor="middle" fill="#555">{int(tmax*k/5)}</text>')
    s.append(f'<text x="{W//2}" y="{H-4}" font-size="10" text-anchor="middle" fill="#555">paso</text>')
    if ylabel: s.append(f'<text x="12" y="{H//2}" font-size="10" fill="#555" transform="rotate(-90 12,{H//2})" text-anchor="middle">{ylabel}</text>')
    for nombre, color, ys, dash in series:
        d = _lin(t, ys, ymax, ymin, log)
        if d: s.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="1.8"{" stroke-dasharray=\"6,3\"" if dash else ""}/>')
    # leyenda
    x = ML + 8
    for nombre, color, ys, dash in series:
        s.append(f'<line x1="{x}" y1="{MT+8}" x2="{x+18}" y2="{MT+8}" stroke="{color}" stroke-width="2"{" stroke-dasharray=\"6,3\"" if dash else ""}/><text x="{x+22}" y="{MT+12}" font-size="11" fill="#222">{nombre}</text>')
        x += 30 + 7 * len(nombre)
    s.append('</svg>')
    return '\n'.join(s)


def foto_svg(f, L, titulo):
    sz = 300; k = sz / L
    s = [f'<svg viewBox="0 0 {sz} {sz+18}" width="{sz}" height="{sz+18}" style="background:#f4f1e6;border:1px solid #ccc">',
         f'<text x="4" y="12" font-size="11" font-family="sans-serif">{titulo}</text>']
    for e in f:
        col = COL[e['n']]; r = {'gusano': 1.2, 'gallina': 2.2, 'oso': 3.2, 'humano': 4.2}[e['n']]
        for (x, y), v in zip(e['pos'], e['veneno']):
            op = 0.35 + min(1.0, v) * 0.65 if e['n'] == 'gusano' else 0.9
            s.append(f'<circle cx="{x*k:.1f}" cy="{18+y*k:.1f}" r="{r}" fill="{col}" fill-opacity="{op:.2f}"/>')
    s.append('</svg>')
    return '\n'.join(s)


def html_de(d):
    S = d['serie']; t = S['t']; brazo = 'EVO' if d['evo'] and d['veneno_ok'] else ('FIJO' if not d['evo'] else 'SINVENENO')
    P = []
    P.append(panel(f'Poblaciones (escala log) — {brazo} semilla {d["seed"]}', t, [(NOM[s], COL[NOM[s]], S['pop'][s], False) for s in range(4)], log=True, ylabel='individuos'))
    P.append(panel('Carrera armamentista 1: veneno del gusano vs escudo de la gallina', t,
                   [('veneno gusano', COL['gusano'], S['rasgos']['veneno'][0], False), ('escudo gallina', COL['gallina'], S['rasgos']['escudo'][1], True),
                    ('veneno gallina', COL['gallina'], S['rasgos']['veneno'][1], False), ('escudo oso', COL['oso'], S['rasgos']['escudo'][2], True)], ylabel='rasgo medio'))
    P.append(panel('Carrera armamentista 2: velocidades medias', t, [(NOM[s], COL[NOM[s]], S['rasgos']['vel'][s], False) for s in range(4)], ylabel='velocidad'))
    P.append(panel('Vista media', t, [(NOM[s], COL[NOM[s]], S['rasgos']['vista'][s], False) for s in range(4)], ylabel='vista'))
    P.append(panel('Tamaño medio y huida media (punteada)', t, [(NOM[s], COL[NOM[s]], S['rasgos']['tam'][s], False) for s in range(4)] + [(NOM[s] + ' huida', COL[NOM[s]], S['rasgos']['huida'][s], True) for s in range(4)], ylabel='rasgo'))
    P.append(panel('Generación media', t, [(NOM[s], COL[NOM[s]], S['gen'][s], False) for s in range(4)], ylabel='generaciones'))
    P.append(panel('Largo medio de la cinta', t, [(NOM[s], COL[NOM[s]], S['largo_cinta'][s], False) for s in range(4)], ylabel='instrucciones'))
    fotos = ''.join(foto_svg(f, d['params']['L'], f'paso {k}') for k, f in sorted(d['fotos'].items(), key=lambda kv: int(kv[0])))
    ext = ', '.join(f'{NOM[s]}: {"vive" if d["extincion"][s] is None else "extinto en " + str(d["extincion"][s])}' for s in range(4))
    return f'''<!doctype html><html><head><meta charset="utf-8"><title>Cadena trófica {brazo} {d["seed"]}</title></head>
<body style="font-family:sans-serif;max-width:900px;margin:auto;background:#fff">
<h2>EXPLORATORIO, no es dato — cadena trófica de 4 especies ({brazo}, semilla {d["seed"]}, T {d["T"]})</h2>
<p>gusano (sol) → gallina → oso → humano. {ext}. Tiempo de cómputo {d["segundos"]:.0f} s.</p>
{"".join(P)}
<h3>Fotos del mundo (gusanos más oscuros = más veneno)</h3>
<div style="display:flex;flex-wrap:wrap;gap:6px">{fotos}</div>
</body></html>'''


def fila(d):
    S = d['serie']; brazo = 'EVO' if d['evo'] and d['veneno_ok'] else ('FIJO' if not d['evo'] else 'SINVENENO')
    def ult(x):
        v = [y for y in x if y is not None]; return f'{v[-1]:.2f}' if v else '—'
    def mx(x):
        v = [y for y in x if y is not None]; return f'{max(v):.2f}' if v else '—'
    ext = [('vive' if e is None else str(e)) for e in d['extincion']]
    f = d['finales']
    return (f"| {brazo} | {d['seed']} | {' / '.join(ext)} | {' / '.join(str(f[n]['n']) for n in NOM)} | {' / '.join(str(f[n]['gen_max']) for n in NOM)} | "
            f"{ult(S['rasgos']['veneno'][0])} (máx {mx(S['rasgos']['veneno'][0])}) | {ult(S['rasgos']['escudo'][1])} (máx {mx(S['rasgos']['escudo'][1])}) | "
            f"{ult(S['rasgos']['vel'][0])} / {ult(S['rasgos']['vel'][1])} / {ult(S['rasgos']['vel'][2])} / {ult(S['rasgos']['vel'][3])} | "
            f"{ult(S['rasgos']['vista'][1])} | {ult(S['rasgos']['huida'][0])} | {f['gallina']['muertes']['por_veneno_al_comer']} | {d['segundos']:.0f} |")


if __name__ == '__main__':
    aqui = os.path.dirname(os.path.abspath(__file__))
    filas = ['| brazo | semilla | extinción (g/ga/o/h) | pobl. final | gen. máx | veneno gusano fin | escudo gallina fin | vel fin g/ga/o/h | vista gallina | huida gusano | gallinas muertas por veneno | s |',
             '|---|---|---|---|---|---|---|---|---|---|---|---|']
    for ruta in sys.argv[1:]:
        d = json.load(open(ruta, encoding='utf-8'))
        brazo = 'EVO' if d['evo'] and d['veneno_ok'] else ('FIJO' if not d['evo'] else 'SINVENENO')
        out = os.path.join(aqui, f'cadena_{brazo}_{d["seed"]}.html')
        open(out, 'w', encoding='utf-8').write(html_de(d)); print('->', out)
        filas.append(fila(d))
    open(os.path.join(aqui, 'datos', 'TABLA.md'), 'w', encoding='utf-8').write('# EXPLORATORIO, no es dato\n\n' + '\n'.join(filas) + '\n')
    print('\n'.join(filas))
