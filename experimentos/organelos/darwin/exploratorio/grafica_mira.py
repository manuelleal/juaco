# EXPLORATORIO, no es dato. Gráfica SVG (sin dependencias) de mira_endo_largo.py (coordinador, 24-sep-2026).
import glob, json, os
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
COL = {'VIDA_S': '#2a78d6', 'INERTE': '#eb6834'}
NOM = {'VIDA_S': 'simbionte que actúa', 'INERTE': 'simbionte inerte (control)'}
INK, INK2, GRID, SURF = '#0b0b0b', '#52514e', '#e4e3df', '#fcfcfb'
W, H = 900, 720; L, R = 110, 30
PANELES = [dict(y0=110, h=240, clave='gap', titulo='domesticación (índice adentro − libres)', lo=-0.4, hi=1.4, ticks=[-0.4, 0, 0.4, 0.8, 1.2]),
           dict(y0=420, h=240, clave='fr', titulo='fracción de bichos con simbionte', lo=0, hi=1, ticks=[0, 0.25, 0.5, 0.75, 1])]
TMAX = 300


def suave(y, k=15):
    y = np.asarray(y, float); out = np.full_like(y, np.nan)
    for i in range(len(y)):
        w = y[max(0, i - k):i + 1]; w = w[~np.isnan(w)]
        if len(w): out[i] = w.mean()
    return out


def X(t): return L + (W - L - R) * t / TMAX


datos = {}
for b in ('INERTE', 'VIDA_S'):
    for p in sorted(glob.glob(os.path.join(AQUI, f'mira_{b}_s*.json'))):
        S = json.load(open(p, encoding='utf-8'))['serie_simb']
        t = np.array([r[0] for r in S]) / 1000
        gap = suave([(r[5] - r[4]) if (r[4] is not None and r[5] is not None) else np.nan for r in S])
        fr = suave([(r[2] / r[1]) if r[1] else np.nan for r in S])
        datos.setdefault(b, []).append(dict(t=t, gap=gap, fr=fr))

o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Segoe UI, Arial, sans-serif">',
     f'<rect width="{W}" height="{H}" fill="{SURF}"/>',
     f'<text x="{L - 60}" y="40" font-size="19" fill="{INK}" font-weight="600">Endosimbiosis vista de cerca: el simbionte que actúa se domestica, el inerte no</text>',
     f'<text x="{L - 60}" y="64" font-size="12" fill="{INK2}">EXPLORATORIO, no es dato · 3 semillas por brazo (22996–22998) · 300 000 pasos · w30 · vivero encendido todo el tiempo · media móvil de 15 muestras</text>']
# leyenda
lx = L; ly = 88
for b in ('VIDA_S', 'INERTE'):
    o.append(f'<line x1="{lx}" y1="{ly}" x2="{lx + 26}" y2="{ly}" stroke="{COL[b]}" stroke-width="3" stroke-linecap="round"/>')
    o.append(f'<text x="{lx + 34}" y="{ly + 4}" font-size="12.5" fill="{INK}">{NOM[b]}</text>'); lx += 250
for P in PANELES:
    y0, h, lo, hi = P['y0'], P['h'], P['lo'], P['hi']
    Y = lambda v: y0 + h - h * (v - lo) / (hi - lo)
    o.append(f'<text x="{L}" y="{y0 - 12}" font-size="13" fill="{INK}" font-weight="600">{P["titulo"]}</text>')
    for tk in P['ticks']:
        o.append(f'<line x1="{L}" y1="{Y(tk):.1f}" x2="{W - R}" y2="{Y(tk):.1f}" stroke="{GRID}" stroke-width="1"/>')
        o.append(f'<text x="{L - 10}" y="{Y(tk) + 4:.1f}" font-size="11" fill="{INK2}" text-anchor="end">{tk:g}</text>')
    if lo < 0 < hi:
        o.append(f'<line x1="{L}" y1="{Y(0):.1f}" x2="{W - R}" y2="{Y(0):.1f}" stroke="{INK2}" stroke-width="1.2" stroke-dasharray="5 4"/>')
    for b in ('INERTE', 'VIDA_S'):
        for d in datos[b]:
            pts = [(X(t), Y(min(max(v, lo), hi))) for t, v in zip(d['t'], d[P['clave']]) if not np.isnan(v)]
            o.append(f'<polyline fill="none" stroke="{COL[b]}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round" opacity="0.9" points="'
                     + ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts) + '"/>')
for tt in range(0, TMAX + 1, 50):
    o.append(f'<text x="{X(tt):.1f}" y="{PANELES[-1]["y0"] + PANELES[-1]["h"] + 20}" font-size="11" fill="{INK2}" text-anchor="middle">{tt}</text>')
o.append(f'<text x="{(L + W - R) / 2}" y="{H - 14}" font-size="12" fill="{INK2}" text-anchor="middle">tiempo (miles de pasos)</text>')
o.append('</svg>')
open(os.path.join(AQUI, 'mira_endo_largo.svg'), 'w', encoding='utf-8').write('\n'.join(o))
print('ok')
