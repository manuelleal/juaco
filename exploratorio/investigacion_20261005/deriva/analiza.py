"""analiza.py — tablas del experimento de deriva: mediana [min-max] por prueba x metodo, recuperacion, pareadas por semilla
(en cuantas de N gana la celula A a cada rival), costo y memoria. Lee datos/deriva.json; escribe datos/tablas.md."""
import json, sys, numpy as np

ARCH = sys.argv[1] if len(sys.argv) > 1 else 'datos/deriva.json'
todo = json.load(open(ARCH)); out = []
P = lambda s: out.append(s)
GENS = ['SEA', 'hiperplano', 'STAGGER', 'RBF']; DER = ['abrupto', 'gradual']; CS = [20, 50, 200]
INDEP = ['base congelado', 'SGD en linea', 'SGD + DDM', 'Naive Bayes olvido', 'DWM']
DEP = ['kNN ventana', 'reentrenar ventana', 'celula A', 'celula B (sola)', 'celula A barajada', 'celula A sin compuerta']
METS = INDEP + DEP


def serie(g, d, C, m, campo, idx=None):
    """lista por semilla; los metodos independientes de C se toman de C=50."""
    key = f"{g}|{d}|C{C}"; key50 = f"{g}|{d}|C50"
    rs = todo[key50] if m in INDEP else todo[key]
    v = [r[m][campo] if idx is None else r[m][campo][idx] for r in rs]
    return v


def mr(v, f='.3f'):
    v = [x for x in v if x is not None]
    if not v: return 'nunca'
    return f"{np.median(v):{f}} [{min(v):{f}}-{max(v):{f}}]"


def mr_rec(v, L):
    n = len(v); ok = [x for x in v if x is not None]
    if not ok: return f"nunca (0/{n})"
    return f"{int(np.median(ok))} [{min(ok)}-{max(ok)}] ({len(ok)}/{n})"


def gana(a, b):
    a, b = np.array(a, float), np.array(b, float); return int((a > b + 1e-9).sum()), int((b > a + 1e-9).sum()), float(np.median(a - b))


N = len(next(iter(todo.values())))
P(f"# Tablas (mediana [min-max], {N} semillas). Metodos independientes de la memoria C (base, SGD, SGD+DDM, NB, DWM) se corrieron una vez (en C=50).\n")
acc0 = [r['_acc0'] for g in GENS for r in todo[f'{g}|abrupto|C50']]
P(f"Base congelado, paso 0 (acierto en el concepto A con ruido 10 %, techo 0.90): {mr(acc0)}\n")

# --- tabla 1: acierto prequential global por prueba x metodo, por C
for C in CS:
    P(f"\n## Tabla 1.C{C} — acierto prequential global (memoria C={C} para kNN, reentrenar y celulas)\n")
    P("| prueba | " + " | ".join(METS) + " |"); P("|---|" + "---|" * len(METS))
    for g in GENS:
        for d in DER:
            P(f"| {g} {d} | " + " | ".join(mr(serie(g, d, C, m, 'preq'), '.2f') for m in METS) + " |")

# --- tabla 2: recuperacion: acierto en ventana de 200 tras cada cambio y pasos hasta 0.80 (C=50)
for C in (50,):
    P(f"\n## Tabla 2 — tras cada cambio (C={C}): acierto en los 200 pasos siguientes al cambio 1 (A→B) / 2 (B→A, RECURRENTE) / 3 (A→C); y pasos hasta ventana-50 >= 0.80\n")
    P("| prueba | metodo | post cambio 1 | post 2 (vuelve A) | post 3 | rec 1 | rec 2 (vuelve A) | rec 3 |"); P("|---|---|---|---|---|---|---|---|")
    for g in GENS:
        for d in DER:
            for m in METS:
                po = [mr(serie(g, d, C, m, 'post', i), '.2f') for i in range(3)]
                re = [mr_rec(serie(g, d, C, m, 'rec', i), 1000) for i in range(3)]
                P(f"| {g} {d} | {m} | {po[0]} | {po[1]} | {po[2]} | {re[0]} | {re[1]} | {re[2]} |")

# --- tabla 3: pareadas: celula A vs cada rival, acierto global, por C
P("\n## Tabla 3 — pareadas por semilla: en cuantas de N gana la celula A a cada rival (gana/pierde, mediana de la diferencia), acierto prequential global\n")
rivales = [m for m in METS if m != 'celula A']
for C in CS:
    P(f"\n### C={C}\n"); P("| prueba | " + " | ".join(rivales) + " |"); P("|---|" + "---|" * len(rivales))
    tot = {m: [0, 0] for m in rivales}
    for g in GENS:
        for d in DER:
            a = serie(g, d, C, 'celula A', 'preq'); fila = []
            for m in rivales:
                w, l, md = gana(a, serie(g, d, C, m, 'preq')); tot[m][0] += w; tot[m][1] += l
                fila.append(f"{w}/{l} ({md:+.3f})")
            P(f"| {g} {d} | " + " | ".join(fila) + " |")
    P(f"| **total (de {8*N})** | " + " | ".join(f"{tot[m][0]}/{tot[m][1]}" for m in rivales) + " |")

# --- tabla 3b: pareadas en la ventana tras la VUELTA (recurrente) y tras el cambio 1 y 3
for idx, nom in ((1, 'tras la VUELTA de A (cambio 2)'), (0, 'tras el cambio 1 (A→B)'), (2, 'tras el cambio 3 (A→C)')):
    P(f"\n## Tabla 3b.{idx} — pareadas celula A vs rival en acierto de los 200 pasos {nom}, C=50\n")
    P("| prueba | " + " | ".join(rivales) + " |"); P("|---|" + "---|" * len(rivales))
    tot = {m: [0, 0] for m in rivales}
    for g in GENS:
        for d in DER:
            a = serie(g, d, 50, 'celula A', 'post', idx); fila = []
            for m in rivales:
                w, l, md = gana(a, serie(g, d, 50, m, 'post', idx)); tot[m][0] += w; tot[m][1] += l; fila.append(f"{w}/{l} ({md:+.2f})")
            P(f"| {g} {d} | " + " | ".join(fila) + " |")
    P(f"| **total (de {8*N})** | " + " | ".join(f"{tot[m][0]}/{tot[m][1]}" for m in rivales) + " |")

# --- tabla 4: costo y memoria
P("\n## Tabla 4 — costo (ops por ejemplo, mediana) y memoria final (ejemplos o celulas), por C, abrupto\n")
P("| prueba | C | " + " | ".join(METS) + " |"); P("|---|---|" + "---|" * len(METS))
for g in GENS:
    for C in CS:
        P(f"| {g} | {C} | " + " | ".join(f"{int(np.median(serie(g, 'abrupto', C, m, 'ops')))} ops · mem {int(np.median(serie(g, 'abrupto', C, m, 'mem')))}" for m in METS) + " |")
P("\nCelula A: nacimientos / muertes / pisadas por corrida (mediana), abrupto C=50: " + "; ".join(
    f"{g}: {int(np.median(serie(g,'abrupto',50,'celula A','nac')))}/{int(np.median(serie(g,'abrupto',50,'celula A','mue')))}/{int(np.median(serie(g,'abrupto',50,'celula A','pisadas')))}" for g in GENS))

# --- resumen por tramo: acierto en el tramo 3 (A recurrente) vs tramo 1 (A inicial)
P("\n## Tabla 5 — acierto por tramo (A | B | A vuelve | C), abrupto, C=50\n")
P("| prueba | metodo | A | B | A (vuelve) | C |"); P("|---|---|---|---|---|---|")
for g in GENS:
    for m in METS:
        tr = [mr(serie(g, 'abrupto', 50, m, 'tramos', i), '.2f') for i in range(4)]
        P(f"| {g} | {m} | " + " | ".join(tr) + " |")

open('datos/tablas.md', 'w', encoding='utf-8').write("\n".join(out)); print("\n".join(out))
