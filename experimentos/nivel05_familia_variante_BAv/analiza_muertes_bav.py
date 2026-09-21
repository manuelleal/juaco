"""DIAGNOSTICO de las 104 muertes de `BA-v` (regla 10: el analisis lo ejecuta un script del repositorio sobre los
JSON, nunca en linea). UN proceso, sin Pool, sin simular NADA: solo lee los dos crudos de la serie BA.

MISION: llegar a la AGI por este camino -- organismo minimo, reglas locales, sin retropropagacion, peldanos
preregistrados con controles y replicas. Aqui: entender el COSTE de la lectura candidata ANTES de escribir su
criterio, porque una puerta de coste sin causa medida es una puerta que no sabe lo que mata.

Preguntas (encargo del coordinador, 21-sep 16:30):
  Q1  por semilla y por brazo: una semilla catastrofica o un desplazamiento general?
  Q2  correlaciona con `okU`?
  Q3  correlaciona con CORTADO 0 (la abstinencia: el mensaje se obedece siempre)?

    python experimentos/nivel05_familia_variante_BAv/analiza_muertes_bav.py
"""
import sys, os, json, time, hashlib, statistics as st

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
BA = os.path.join(RAIZ, 'experimentos', 'junta_fase5', 'BA')

CRUDOS = [('921-940', 'serie_ba_s921-940_20260921_130939_crudo.json'),
          ('941-960', 'serie_ba_s941-960_20260921_132923_crudo.json')]
CELDAS = ['b5k3', 'b6suf', 'A1', 'BA', 'BA-v']
BRAZOS = ['CANAL', 'CORTADO', 'BAR-H', 'BAR-T', 'VALOR', 'PAR', 'PAR0']
UMBRAL_CAT = 200          # "regimen de hambre": declarado ANTES de mirar (ver DIAG: el histograma es bimodal
                          # con un hueco entre ~180 y ~450 en las dos series y en las cinco celdas)


def h16(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(65536), b''):
            h.update(b)
    return h.hexdigest()[:16]


def spearman(x, y):
    """rho de Spearman con empates por rango medio (sin scipy)."""
    def rangos(v):
        idx = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v); i = 0
        while i < len(idx):
            j = i
            while j + 1 < len(idx) and v[idx[j + 1]] == v[idx[i]]:
                j += 1
            m = (i + j) / 2.0 + 1.0
            for k in range(i, j + 1):
                r[idx[k]] = m
            i = j + 1
        return r
    rx, ry = rangos(x), rangos(y)
    n = len(x)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** 0.5
    return (num / den) if den else float('nan')


def carga():
    D = {}
    for nom, f in CRUDOS:
        p = os.path.join(BA, f)
        d = json.load(open(p, encoding='utf-8'))
        D[nom] = dict(sha=h16(p), arch=f, R=d['brazos'], meta=d['meta'])
    return D


def main():
    L = []
    pr = lambda s='': (L.append(s), print(s))
    D = carga()
    pr("# DIAG_muertes — por que `BA-v` muere 104 en 941–960 (diagnostico, no veredicto)")
    pr("")
    pr("> Script `analiza_muertes_bav.py` (regla 10: el analisis lo ejecuta un script sobre los JSON). UN proceso,")
    pr("> sin Pool, sin simular: solo lee los dos crudos de la serie BA. Fecha %s." % time.strftime('%Y-%m-%d %H:%M'))
    pr("")
    for nom, dd in D.items():
        pr("- crudo **%s** `%s` sha256_16 `%s` — %d filas, celdas %s"
           % (nom, dd['arch'], dd['sha'], len(dd['R']), list(dd['meta']['celdas'])))
    pr("")
    pr("La columna `muertes` de la tabla registrada es la **mediana sobre semillas de `deaths` del brazo CANAL**")
    pr("(`corre_familias_ba.py:214`). Todo lo de abajo usa esa misma definicion salvo donde diga otra cosa.")
    pr("")

    # ---------------------------------------------------------------- Q1a: la forma de la distribucion
    pr("## 1. La distribucion de `deaths` es BIMODAL: hay dos regimenes, no una cola")
    pr("")
    pr("| serie | celda | n | mediana | media | min | max | semillas >= %d (regimen de hambre) |" % UMBRAL_CAT)
    pr("|---|---|---|---|---|---|---|---|")
    reg = {}
    for nom, dd in D.items():
        for c in CELDAS:
            v = sorted((r['seed'], r['deaths']) for r in dd['R'] if r['cel'] == c and r['base'] == 'CANAL')
            ds = [x[1] for x in v]
            cat = [s for s, x in v if x >= UMBRAL_CAT]
            reg[(nom, c)] = dict(v=dict(v), cat=set(cat))
            pr("| %s | %s | %d | **%.0f** | %.0f | %d | %d | %d %s |"
               % (nom, c, len(ds), st.median(ds), sum(ds) / len(ds), min(ds), max(ds), len(cat), sorted(cat)))
    pr("")
    huecos = []
    for (nom, c), z in reg.items():
        ds = sorted(z['v'].values())
        bajo = [x for x in ds if x < UMBRAL_CAT]
        alto = [x for x in ds if x >= UMBRAL_CAT]
        if bajo and alto:
            huecos.append((max(bajo), min(alto)))
    pr("Hueco entre los dos regimenes (max del bajo, min del alto) en las 10 combinaciones serie x celda: %s."
       % sorted(set(huecos)))
    pr("")

    # ---------------------------------------------------------------- Q1b: por semilla, pareado
    pr("## 2. Por semilla (brazo CANAL): `deaths` de las cinco celdas en el MISMO mundo")
    pr("")
    for nom, dd in D.items():
        seeds = sorted({r['seed'] for r in dd['R']})
        pr("**Serie %s** (`*` = >= %d)" % (nom, UMBRAL_CAT))
        pr("")
        pr("| semilla | " + " | ".join(CELDAS) + " | BA-v − A1 | BA-v − BA | okU(BA-v) | comio ref (CANAL) |")
        pr("|---|" + "---|" * (len(CELDAS) + 4))
        dif_a, dif_b, flip = [], [], []
        for s in seeds:
            g = {c: reg[(nom, c)]['v'][s] for c in CELDAS}
            rv = [r for r in dd['R'] if r['cel'] == 'BA-v' and r['base'] == 'CANAL' and r['seed'] == s][0]
            dif_a.append(g['BA-v'] - g['A1']); dif_b.append(g['BA-v'] - g['BA'])
            if g['BA-v'] >= UMBRAL_CAT and max(g['A1'], g['BA']) < UMBRAL_CAT:
                flip.append(s)
            pr("| %d | " % s + " | ".join(('**%d***' % g[c]) if g[c] >= UMBRAL_CAT else '%d' % g[c] for c in CELDAS)
               + " | %+d | %+d | %s | %s |" % (g['BA-v'] - g['A1'], g['BA-v'] - g['BA'],
                                               rv['B4']['okU'], 'si' if rv['B4']['evX'] == 0.0 else 'no'))
        pr("")
        pr("- mediana de la diferencia pareada **BA-v − A1 = %+.0f** (sube en %d/%d semillas, baja en %d);"
           " **BA-v − BA = %+.0f** (sube %d, baja %d, identica %d)."
           % (st.median(dif_a), sum(1 for x in dif_a if x > 0), len(dif_a), sum(1 for x in dif_a if x < 0),
              st.median(dif_b), sum(1 for x in dif_b if x > 0), sum(1 for x in dif_b if x < 0),
              sum(1 for x in dif_b if x == 0)))
        pr("- semillas donde **solo BA-v** entra en regimen de hambre (A1 y BA no): %s" % (flip or 'ninguna'))
        pr("")

    # ---------------------------------------------------------------- Q1c: por brazo
    pr("## 3. Por brazo: mediana de `deaths` en los siete brazos")
    pr("")
    pr("| serie | celda | " + " | ".join(BRAZOS) + " |")
    pr("|---|---|" + "---|" * len(BRAZOS))
    for nom, dd in D.items():
        for c in CELDAS:
            fila = []
            for b in BRAZOS:
                ds = [r['deaths'] for r in dd['R'] if r['cel'] == c and r['base'] == b]
                fila.append('%.0f' % st.median(ds) if ds else '-')
            pr("| %s | %s | " % (nom, c) + " | ".join(fila) + " |")
    pr("")
    pr("El brazo cambia el mundo del mensaje, no el mundo del receptor: si `BA-v` muriera por el mensaje, el")
    pr("efecto estaria en CANAL y no en CORTADO (gemelo mudo) ni en VALOR (ceros).")
    pr("")

    # ---------------------------------------------------------------- Q2 / Q3
    pr("## 4. Q2 y Q3: con que correlaciona `deaths` de BA-v")
    pr("")
    pr("| serie | pareja | rho de Spearman (n = 19) |")
    pr("|---|---|---|")
    for nom, dd in D.items():
        R = [r for r in dd['R'] if r['cel'] == 'BA-v' and r['base'] == 'CANAL']
        R.sort(key=lambda r: r['seed'])
        d = [r['deaths'] for r in R]
        ok = [r['B4']['okU'] if r['B4']['okU'] is not None else 0.0 for r in R]
        mo = [r['B4']['mord_ref'] or 0 for r in R]
        vi = [r['vistas'] or 0 for r in R]
        co = [r['cobertura'] or 0 for r in R]
        ce = [r['celdas'] or 0 for r in R]
        b5 = [reg[(nom, 'b5k3')]['v'][r['seed']] for r in R]
        a1 = [reg[(nom, 'A1')]['v'][r['seed']] for r in R]
        pr("| %s | deaths(BA-v) vs `okU` | %+.3f |" % (nom, spearman(d, ok)))
        pr("| %s | deaths(BA-v) vs mordidas del referente | %+.3f |" % (nom, spearman(d, mo)))
        pr("| %s | deaths(BA-v) vs `mem_vistas` (exposiciones) | %+.3f |" % (nom, spearman(d, vi)))
        pr("| %s | deaths(BA-v) vs `mem_cobertura` | %+.3f |" % (nom, spearman(d, co)))
        pr("| %s | deaths(BA-v) vs celdas usadas | %+.3f |" % (nom, spearman(d, ce)))
        pr("| %s | **deaths(BA-v) vs deaths(b5k3) en el mismo mundo** | %+.3f |" % (nom, spearman(d, b5)))
        pr("| %s | **deaths(BA-v) vs deaths(A1) en el mismo mundo** | %+.3f |" % (nom, spearman(d, a1)))
    pr("")
    pr("**Q3 (CORTADO 0 = el receptor NUNCA muerde al referente sin mensaje).** CORTADO es una medida de UNA")
    pr("mordida (la primera exposicion de la vida al referente) en el brazo mudo; no es una tasa de abstinencia.")
    pr("Lo que si es tasa esta abajo: `mord_ref` (cuantas veces mordio el referente en toda la vida) y `mem_vistas`.")
    pr("")
    pr("| serie | celda | CORTADO (com/n) | mediana `mord_ref` (CANAL) | mediana `mem_vistas` (CANAL) | mediana celdas |")
    pr("|---|---|---|---|---|---|")
    for nom, dd in D.items():
        for c in CELDAS:
            rs = [r for r in dd['R'] if r['cel'] == c and r['base'] == 'CORTADO']
            n = len([r for r in rs if r['B4']['evX'] is not None])
            com = sum(1 for r in rs if r['B4']['evX'] == 0.0)
            ca = [r for r in dd['R'] if r['cel'] == c and r['base'] == 'CANAL']
            pr("| %s | %s | %d/%d | %.0f | %.0f | %.0f |"
               % (nom, c, com, n, st.median([r['B4']['mord_ref'] or 0 for r in ca]),
                  st.median([r['vistas'] or 0 for r in ca]), st.median([r['celdas'] or 0 for r in ca])))
    pr("")

    # ---------------------------------------------------------------- la base que faltaba (R6)
    pr("## 5. Lo que NO se puede contestar con estos crudos")
    pr("")
    pr("- **`b4b` (la base de R6) no esta en ninguna de las dos series** (`meta.celdas` = %s): el cociente de R6"
       % list(D['941-960']['meta']['celdas']))
    pr("  no existe todavia. Por eso el criterio nuevo lo obliga a estar en `--celdas` (ERR-89).")
    pr("- Estos crudos no traen serie temporal de energia ni de mordidas por paso: no se puede decir *cuando*")
    pr("  muere, solo *cuanto*. El criterio nuevo anade el diagnostico, no lo suple.")
    pr("")

    out = os.path.join(AQUI, 'DIAG_muertes.md')
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        f.write("\n".join(L) + "\n")
    print("\n-> %s  sha256_16 = %s" % (out, h16(out)))


if __name__ == '__main__':
    main()
