"""LAS CUATRO SERIES PREVIAS, en una tabla, para JUSTIFICAR los umbrales ABSOLUTOS de ERR-90 ANTES de correr
semillas nuevas (regla 4: el criterio se fija con datos ya vistos, el veredicto con datos nuevos).

MISION: llegar a la AGI por este camino. Aqui: que cada umbral de un criterio nuevo tenga detras un numero
medido, y no la cifra que le conviene al candidato.

Lee SOLO crudos de series ya registradas (821-840, 841-860 de la junta; 921-940, 941-960 de BA). No simula.
UN proceso, sin Pool.

    python experimentos/nivel05_familia_variante_BAv/analiza_previas_bav.py
"""
import sys, os, json, time, hashlib, statistics as st

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))

FUENTES = [
    ('821-840', os.path.join(RAIZ, 'experimentos', 'junta_fase5', 'A', 'serie_a1_s821-840_20260919_184918_crudo.json')),
    ('841-860', os.path.join(RAIZ, 'experimentos', 'junta_fase5', 'A', 'serie_a1_s841-860_20260919_190332_crudo.json')),
    ('921-940', os.path.join(RAIZ, 'experimentos', 'junta_fase5', 'BA', 'serie_ba_s921-940_20260921_130939_crudo.json')),
    ('941-960', os.path.join(RAIZ, 'experimentos', 'junta_fase5', 'BA', 'serie_ba_s941-960_20260921_132923_crudo.json')),
]
CELDAS = ['b5k3', 'b6suf', 'A1', 'BA', 'BA-v']
BRAZOS = ['CANAL', 'CORTADO', 'BAR-H', 'BAR-T', 'VALOR']


def h16(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(65536), b''):
            h.update(b)
    return h.hexdigest()[:16]


def main():
    L = []
    pr = lambda s='': (L.append(s), print(s))
    pr("# PREVIAS — las cuatro series ya corridas, en una tabla (base de los umbrales de ERR-90)")
    pr("")
    pr("> `analiza_previas_bav.py`, %s. Solo lee crudos de series REGISTRADAS; no simula nada." % time.strftime('%Y-%m-%d %H:%M'))
    pr("> `com` = la boca mordio al referente en su PRIMERA exposicion de la vida (ERR-44). `dist` = par referente/hermana.")
    pr("")
    for nom, p in FUENTES:
        pr("- %s `%s` sha256_16 `%s`" % (nom, os.path.basename(p), h16(p)))
    pr("")
    pr("| serie | celda | n | CANAL | CORTADO | BAR-H | BAR-T | VALOR | dist(PAR) | dist(PAR0) | muertes | okU |")
    pr("|---|---|---|---|---|---|---|---|---|---|---|---|")
    G = {}
    for nom, p in FUENTES:
        d = json.load(open(p, encoding='utf-8'))
        R = d['brazos']
        for c in CELDAS:
            rs0 = [r for r in R if r['cel'] == c]
            if not rs0:
                continue
            fila = {}
            for b in BRAZOS:
                rs = [r for r in rs0 if r['base'] == b]
                n = len([r for r in rs if r['B4']['evX'] is not None])
                fila[b] = (sum(1 for r in rs if r['B4']['evX'] == 0.0), n)
            dP = [r['B4']['dist'] for r in rs0 if r['base'] == 'PAR' and r['B4']['dist'] is not None]
            d0 = [r['B4']['dist'] for r in rs0 if r['base'] == 'PAR0' and r['B4']['dist'] is not None]
            ca = [r for r in rs0 if r['base'] == 'CANAL']
            mu = st.median([r['deaths'] for r in ca])
            ok = st.median([r['B4']['okU'] for r in ca if r['B4']['okU'] is not None])
            G[(nom, c)] = dict(fila=fila, dP=(int(sum(dP)), len(dP)), d0=(int(sum(d0)), len(d0)), mu=mu, okU=ok)
            pr("| %s | %s | %d | %d | %d | %d | %d | %d | %d/%d | %d/%d | %.0f | %.4f |"
               % (nom, c, fila['CANAL'][1], fila['CANAL'][0], fila['CORTADO'][0], fila['BAR-H'][0],
                  fila['BAR-T'][0], fila['VALOR'][0], int(sum(dP)), len(dP), int(sum(d0)), len(d0), mu, ok))
    pr("")
    pr("## Rango observado por brazo (las 4 series, todas las celdas)")
    pr("")
    pr("| brazo | b5k3 (forma sola) | b6suf (sufijo) | A1 | BA | BA-v | min–max global |")
    pr("|---|---|---|---|---|---|---|")
    for b in BRAZOS + ['dist']:
        cols, todo = [], []
        for c in CELDAS:
            v = []
            for nom, _ in FUENTES:
                if (nom, c) in G:
                    v.append(G[(nom, c)]['dP'][0] if b == 'dist' else G[(nom, c)]['fila'][b][0])
            cols.append(', '.join(str(x) for x in v) if v else '—')
            todo += v
        pr("| %s | %s | %d–%d |" % (b, ' | '.join(cols), min(todo), max(todo)))
    pr("")
    pr("## Contrastes dentro de la celda (diagnostico, NO son puertas en ERR-90)")
    pr("")
    pr("| serie | celda | CANAL−CORTADO | CANAL−BAR-H | CANAL−BAR-T | CANAL−VALOR | dist−dist0 |")
    pr("|---|---|---|---|---|---|---|")
    for nom, _ in FUENTES:
        for c in CELDAS:
            if (nom, c) not in G:
                continue
            f = G[(nom, c)]['fila']
            pr("| %s | %s | %+d | %+d | %+d | %+d | %+d |"
               % (nom, c, f['CANAL'][0] - f['CORTADO'][0], f['CANAL'][0] - f['BAR-H'][0],
                  f['CANAL'][0] - f['BAR-T'][0], f['CANAL'][0] - f['VALOR'][0],
                  G[(nom, c)]['dP'][0] - G[(nom, c)]['d0'][0]))
    out = os.path.join(AQUI, 'PREVIAS_4series.md')
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        f.write("\n".join(L) + "\n")
    print("\n-> %s  sha256_16 = %s" % (out, h16(out)))


if __name__ == '__main__':
    main()
